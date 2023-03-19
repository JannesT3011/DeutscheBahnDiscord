# DeutscheBahnDiscord
Discord Bot with Deutsche Bahn features<br />
Plan your Route, see departures of given station or check infos about a Long-Distance train.<br />

➡️ [Invite the Bot](https://discord.com/api/oauth2/authorize?client_id=1079486233618677782&permissions=0&scope=bot%20applications.commands)
<br />
The bot is using the [Hafas-Client](https://github.com/public-transport/hafas-client) 


### Commands:
/route [start] [end] (date) -> Get a complete route description for you trip <br />
/trainfino [trainNo] -> Get infos about a train <br />
/departures [station] (onlyLongDistance) (duration in hours) (date) -> Get staion departures <br />

[] arguments = requires <br />
() arguments = optional <br />
date format = dd-mm-yy HH:MM <br />

### Examples:

#### /route:
![Route command example](/img/route.png "route example")

#### /traininfo:
![traininfo command example](/img/traininfo.png "traininfo example")

#### /departures:
![departures command example](/img/departures.png "departures example")

### Setup:
1. Create config.py file like this:
```python
TOKEN = ""
COGS = [
    "cogs.route",
    "cogs.traininfo",
    "cogs.departures",
    "cogs.help"
]

# Bot misc
ACTIVITY = "Deutsche Bahn Bot"
DESCRIPTION= "DeutscheBahn Bot by Bambus#8446"
EMBED_COLOR = "#a21917"
```
2. Run the bot with `python3 bot.py`

### Todos:
- [X] add date to /route
- [X] departures when
- [ ] add loyaltyCard 
- [ ] price analyze
- [ ] reminder for cheap prices
- [ ] reminder for journy 
- [ ] Price Calander (like bahn.guru)
- [ ] /price from to age card
- [X] add duration to /route
- [X] multiple pages for /route 
- [ ] and /departures
- [ ] Watchlist for routes/trains/stations