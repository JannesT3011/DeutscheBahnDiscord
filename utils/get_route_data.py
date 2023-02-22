import aiohttp

async def get_station_id(station: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v5.db.transport.rest/stations?query={station}") as response:
            if response.status != 200:
                return 0
            
            data = await response.json()
            first = next(iter(data))

            return data[first]["id"]

async def get_journey_info(start: int, end: int) -> tuple:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v5.db.transport.rest/journeys?from={start}&to={end}&results=1") as response:
            if response.status != 200:
                print(response.status)
                return {"success": False}
            
            data = await response.json() # TODO PRICE IST MIT IN DER URL
            return (data["journeys"][0]["legs"], data["journeys"][0]["price"]["amount"])