bitbattlebot
============

This is a sample implementation of a bot for the bitcoin gambling website [bitbattle.me](http://bitbattle.me/).

See the [API description](http://bitbattle.me/) for details on the API.

BaseBot
-------
This is a skeleton bot that does noting but connect to the API and display all json event data it receives. Use this bot
to get an understanding of the API events and json objects: Startup the bot and watch it's output while manually placing
bets on bitbattle.me.
You only need to provide the uuid of the player you want to use to the bot.

SimpleMartingaleBot
-------------------
This is an extension of the BaseBot which implements a very simple martingale betting strategy. You need to provide:
- player uuid
- betting address
- start wager
- maximum wager
- number of rounds
- connection details to bitcoind

The betting strategy is very simple:
When a round starts, the bot will bet <start wager> on the provided betting address. If the bet is lost, the wager
will be doubled and bet again. This will repeat until either the maxium wager is reached or a bet is won. In both cases
the current round is considered over and the next round will start again with the start wager.
If the specified number of rounds have been played the bot will disconnect from the API and exit.

Note that the bot is totally session-agnostic. The sessionstart and sessioneend-events are ignored as they do not have
any influence on the betting strategy.
