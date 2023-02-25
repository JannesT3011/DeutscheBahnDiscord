import aiohttp
from datetime import datetime

async def get_train_info(zugnr: str) -> dict:
    now = datetime.now()
    year, month, day = now.year, now.month, now.day

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v6.db.transport.rest/trips?query={zugnr}&onlyCurrentlyRunning=false&fromWhen={year}-{month}-{day} 00:01&untilWhen={year}-{month}-{day}%2023:59&operatorNames=DB%20Fernverkehr%20AG") as response:
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