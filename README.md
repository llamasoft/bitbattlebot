bitbattlebot
============

This is a sample implementation of a bot for the bitcoin gambling website [bitbattle.me](http://bitbattle.me/).

The communication with the server relies on [socket.io](http://socket.io/) technology. See the [API description](http://bitbattle.me/api/) for details on the API.

Requirements
------------
- [socket.io client library](https://github.com/invisibleroads/socketIO-client)
- Python 2.7+ (Not tested with 3.x)

BaseBot
-------
This is a skeleton bot that does nothing but connect to the API and display all json event data it receives. Use this bot
to get an understanding of the API events and json objects: Startup the bot and watch it's output while manually placing
bets on [bitbattle.me](http://bitbattle.me/).
You only need to provide the uuid of the player you want to use to the bot.

### Usage
`> python basebot.py 82ac02f7dd4a420395367281ce074601`

SimpleMartingaleBot
-------------------
This is an extension of the BaseBot which implements a very simple martingale betting strategy. You need to provide:
- player uuid
- betting address
- start wager
- maximum wager
- number of rounds
- connection details to a running bitcoind to place bets through the rpc interface

The betting strategy is very simple:
When a round starts, the bot will bet <start wager> on the provided betting address. If the bet is lost, the wager
will be doubled and bet again. This will repeat until either the maxium wager is reached or a bet is won. In both cases
the current round is considered over and the next round will start again with the start wager.
If the specified number of rounds have been played the bot will disconnect from the API and exit.

*Notes:*
- The bot is totally session-agnostic. The sessionstart and sessionend-events are ignored as they do not have any
influence on the betting strategy.
- The bot does not contain any error-handling e.g. for rejected bets. You have to take care not to exceed or underrun bet limits.
- Don't forget to unlock your wallet before starting the bot.

### Usage
    > python martingalebot.py 82ac02f7dd4a420395367281ce074601 http://rpcuser:rpcpass@localhost:8332 15fJphb2USKDCZJexnKHpK4sUtQaTVNaif 0.001 0.1 12
    
This command will start a martingale session for player [Herbert](http://bitbattle.me/player/herbert/) with bet address 15fJphb2USKDCZJexnKHpK4sUtQaTVNaif (This is Herbert's 50% address). Each martingale round will start with 0.001 BTC wager and double it up to 0.1. The bot will play 12 rounds.
