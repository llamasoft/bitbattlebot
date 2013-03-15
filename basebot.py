
from time import sleep
from decimal import Decimal
from socketIO_client import SocketIO, BaseNamespace
from jsonrpc import ServiceProxy
import json
import sys
import argparse

class BaseBot(object):

    def __init__(self, args):
        self.uuid = args.uuid
        self.socketIO = SocketIO(args.host, args.port)
        self.connect_events()
        self.socketIO.wait()

    def start(self):
        # Override this in your bot implementation
        print("Basebot has started. Now place some bets and observe the output.")

    def stop(self):
        print("Disconnecting...")
        self.socketIO.disconnect()

    def connect_events(self):
        self.socketIO.on('connect', self.on_connect)
        self.socketIO.on('disconnect', self.on_disconnect)
        self.socketIO.on('error', self.on_error)
        self.socketIO.on('joined', self.on_joined)
        self.socketIO.on('message', self.on_message)
        self.socketIO.on('reconnect', self.on_reconnect)
        self.socketIO.on('sessionstart', self.on_sessionstart)
        self.socketIO.on('sessionstate', self.on_sessionstate)
        self.socketIO.on('bet', self.on_bet)
        self.socketIO.on('payment', self.on_payment)
        self.socketIO.on('sessionstop', self.on_sessionstop)

    def on_connect(self, *args):
        print('Connected. Now subscribing to player channel %s' %(self.uuid))
        self.socketIO.emit('subscribe', self.uuid);

    def on_disconnect(self):
        print('Disconnect.')

    def on_reconnect(self, *args):
        print("Reconnect.")

    def on_error(self, name, message):
        print('Error: %s: %s' % (name, message))

    def on_joined(self, channel):
        print("Joined channel %s. Now starting bot." % channel)
        self.start()

    def on_message(self, channel, message):
        message = json.loads(message)
        print("on_message")
        print(json.dumps(message, sort_keys=True, indent=4, separators=(',', ': ')))

    def on_sessionstart(self, channel, message):
        message = json.loads(message)
        print("on_sessionstart")
        print(json.dumps(message, sort_keys=True, indent=4, separators=(',', ': ')))

    def on_sessionstate(self, channel, message):
        message = json.loads(message)
        print("on_sessionstate")
        print(json.dumps(message, sort_keys=True, indent=4, separators=(',', ': ')))

    def on_bet(self, channel, message):
        message = json.loads(message)
        print("on_bet")
        print(json.dumps(message, sort_keys=True, indent=4, separators=(',', ': ')))

    def on_payment(self, channel, message):
        message = json.loads(message)
        print("on_payment")
        print(json.dumps(message, sort_keys=True, indent=4, separators=(',', ': ')))

    def on_sessionstop(self, channel, message):
        message = json.loads(message)
        print("on_sessionstop")
        print(json.dumps(message, sort_keys=True, indent=4, separators=(',', ': ')))

if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Observing-only bot for bitbattle.me. Extend/subclass this bot to do something useful.")
    parser.add_argument("uuid", help="The uuid of the player to use (Obtain it from your player's dashboard)")
    parser.add_argument("--host", help="Host to connect to. Defaults to 'api.bitbattle.me'", default="api.bitbattle.me")
    parser.add_argument("--port", help="Port to connect to. Defaults to 80", type=int, default=80)
    args = parser.parse_args()
    bot = BaseBot(args)
