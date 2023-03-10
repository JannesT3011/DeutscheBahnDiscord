import aiohttp
from datetime import datetime

async def get_trip_id(zugnr: str) -> str:
    """
    GET THE TRIP ID OF GIVEN TRAIN
    RETURNS: TRIPID
    """
    now = datetime.utcnow()
    year, month, day = now.year, now.month, now.day

    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v6.db.transport.rest/trips?query={zugnr}&onlyCurrentlyRunning=false&fromWhen={year}-{month}-{day} 00:01&untilWhen={year}-{month}-{day}%2023:59&operatorNames=DB%20Fernverkehr%20AG") as response:
            if response.status != 200:
                return 0
            
            data = await response.json()
            
            return data["trips"][0]["id"]


async def get_trip_info(tripid) -> tuple:
    """
    GET THE TRIPINFO OF GIVEN ID
    RETURNS: (start, end, stops)
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v6.db.transport.rest/trips/{tripid}") as response:
            if response.status != 200:
                return (0)
            
            data = await response.json()

            return (data["trip"]["origin"]["name"], data["trip"]["destination"]["name"], data["trip"]["stopovers"], data["trip"]["line"]["name"])