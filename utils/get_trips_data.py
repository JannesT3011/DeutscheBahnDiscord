import aiohttp
from datetime import datetime

async def get_train_info(zugnr: str) -> dict:
    now = datetime.now()
    year, month, day = now.year, now.month, now.day

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v6.db.transport.rest/trips?query={zugnr}&onlyCurrentlyRunning=false&fromWhen={year}-{month}-{day} 00:00&untilWhen=2023-02-25%2023:59") as response:
            # &onlyCurrentlyRunning=false gibt alles, aber hier checken was gerade aktuell ist
            #https://v6.db.transport.rest/trips?query=EC113&onlyCurrentlyRunning=false&fromWhen=2023-02-25%2000:00&untilWhen=2023-02-25%2023:59
            # mit der iD und /trips/id stops bekommen?
            if response.status != 200:
                return 0
            
            data = await response.json()
            
            return data["trips"][0]

async def get_train_stopovers(tripid) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v6.db.transport.rest/trips/{tripid}") as response:
            if response.status != 200:
                return 0
            
            data = await response.json()
            
            return data["trip"]["stopovers"]