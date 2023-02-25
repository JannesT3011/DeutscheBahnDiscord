import aiohttp
from typing import Literal

async def get_station_info(station: str) -> tuple:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v6.db.transport.rest/stations?query={station}") as response:
            if response.status != 200:
                return (0)
            
            data = await response.json()
            first = next(iter(data))

            return (data[first]["id"], data[first]["name"])

async def get_journey_info(start: int, end: int) -> tuple:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v6.db.transport.rest/journeys?from={start}&to={end}&results=1") as response:
            if response.status != 200:
                return (0)
            
            data = await response.json()
            return (data["journeys"][0]["legs"], data["journeys"][0]["price"])