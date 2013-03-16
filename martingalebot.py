from decimal import Decimal
from jsonrpc import ServiceProxy
import json
from basebot import BaseBot
import argparse

class SimpleMartingaleBot(BaseBot):

    def __init__(self, args):
        self.bitcoind_api = ServiceProxy(args.bitcoind_connection_string)
        self.bet_address = args.betaddress
        self.startamount = args.startamount
        self.lastamount = args.startamount
        self.limit = args.limitamount
        self.num_rounds = args.rounds
        self.current_round = 1
        self.sessionID = None
        super(SimpleMartingaleBot, self).__init__(args)

    def start(self):
        print("Starting round %d!" % (self.current_round))
        self.place_bet(self.startamount)

    def place_bet(self, amount):
        print("Betting %.8f on %s" %(amount, self.bet_address))
        self.bitcoind_api.sendtoaddress(self.bet_address, float(amount))
        self.lastamount = amount

    # This is a very simply Martingale strategy:
    #  - If the last bet was won start a new round again with the start_amount.
    #  - If the last bet was lost place another bet with double stake
    #  - If the doubled stake is above the bet limit consider the round "lost" and start a new round by placing again
    #    a bet with start_amount
    #  - If no more bets shall be placed return False
    def check_bet(self, bet):
        if bet['won']:
            if self.current_round < self.num_rounds:
                # WON! Now start next round
                self.current_round += 1
                print("Starting round %d!" % (self.current_round))
                self.place_bet(self.startamount)
            else:
                print("Last round finished.")
                return False
        else:
            # double stake
            newstake = self.lastamount * 2
            if newstake <= self.limit:
                self.place_bet(newstake)
            else:
                print("Reached bet limit - Can't double stake! Closing this round...")
                if self.current_round < self.num_rounds:
                    self.current_round += 1
                    print("Starting next round %d!" % (self.current_round))
                    self.place_bet(self.startamount)
                else:
                    print("Last round finished.")
                    return False

    def on_bet(self, channel, message):
        bet = json.loads(message)
        if bet['player']['uuid'] != self.uuid:
            print("Error! Received bet for wrong player %s (My player: %s)" %(bet['player']['uuid'], self.uuid))
            return

        print('[Bet]: %s, drawn: %d, result: %s, stake: %.8f, win: %.8f' %
              (bet['betname'], bet['lucky_number'], bet['won'], bet['wager'], bet['payout']))

        if self.check_bet(bet) == False:
            # bot is done, no more bet placed. disconnect.
            self.stop()
            
    def on_payment(self, channel, message):
        payment = json.loads(message)
        print('[Payment]: %s %.8f to %s, status %s' % (payment['payment_type'], payment['amount'], payment['receiver'], payment['payment_status']))

    def on_sessionstart(self, channel, message):
        message = json.loads(message)
        self.sessionID = message['id']
        print('[Sessionstart]: SessionID %s' %(self.sessionID))

    def on_sessionstate(self, channel, message):
        message = json.loads(message)
        sessionID = message['id']

        if self.sessionID == None:
            # Probably bot started while player has a running session, so the sessionstart-event was not received.
            # Assume that it is safe to continue current session.
            self.sessionID = sessionID

        if sessionID != self.sessionID:
            print("Error! Received sessionstate for unknown session %s (My session: %s)" %(sessionID, self.sessionID))
            return
            
        play = message['plays'][0] # There should be only one play as this is singleplayer
        if play['player']['uuid'] != self.uuid:
            print("Error! Received sessionstate for wrong player %s (My player: %s)" %(play['player']['uuid'], self.uuid))
            return
        
        print("[Sessionstate]: %dw/%dl/%dr - Stake: %.8f - Payout: %.8f" %(
            play['bets_won'],
            play['bets_lost'],
            play['bets_remaining'],
            play['stake'],
            play['payout']
            ))

    def on_sessionstop(self, channel, message):
        message = json.loads(message)
        sessionID = message['id']
        if sessionID != self.sessionID:
            print("Error! Received sessionstop for unknown session %s (My session: %s)" %(sessionID, self.sessionID))
            return
        print('[Sessionstop]: SessionID %s (%s)' %(self.sessionID, message['reason']))
        self.sessionID = None


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Simple Martingale-style bot for bitbattle.me. Use on your own risk!")
    parser.add_argument("uuid", help="The uuid of the player to use (Obtain it from your player's dashboard)")
    parser.add_argument("bitcoind_connection_string", help="Bitcoind connection string: 'http://<rpcuser>:<rpcpass>@<host>:<port>'")
    parser.add_argument("betaddress", help="The bitcoin address to place bets on")
    parser.add_argument("startamount", help="Start amount to bet, e.g. '0.01'", type=Decimal)
    parser.add_argument("limitamount", help="Max. amount to bet, e.g. '1.0'", type=Decimal)
    parser.add_argument("rounds", help="Number of rounds to play (A round ends either when a bet is won or the max. bet amount is reached).", type=int)
    parser.add_argument("--host", help="Host to connect to. Defaults to 'api.bitbattle.me'", default="api.bitbattle.me")
    parser.add_argument("--port", help="Port to connect to. Defaults to 80", type=int, default=80)
    args = parser.parse_args()
    bot = SimpleMartingaleBot(args)
