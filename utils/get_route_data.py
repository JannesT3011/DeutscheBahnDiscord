import aiohttp

async def get_station_info(station: str) -> tuple:
    """
    GET STATION INFO
    RETURNS: (stationID, stationName)
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v6.db.transport.rest/stations?query={station}") as response:
            if response.status != 200:
                return (0)
            
            data = await response.json()
            if data == {}:
                return (0)
            
            first = next(iter(data))

            return (data[first]["id"], data[first]["name"])

async def get_journey_info(start: int, end: int, when=None) -> list:
    """
    GET THE JOUNRY INFO
    RETURNS: (LEGS, PRICE)
    """
    async with aiohttp.ClientSession() as session:
        url = f"https://v6.db.transport.rest/journeys?from={start}&to={end}"
        if when != None:
            url+=f"&departure={when}"

        async with session.get(url) as response:
            if response.status != 200:
                return [0]
            
            data = await response.json()
            return data["journeys"]