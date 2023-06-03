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

            return (data[first]["id"], data[first]["name"], data[first])

async def get_journey_info(start: int, end: int, when=None, age:int=None, bahncard=None) -> list:
    """
    GET THE JOUNRY INFO
    RETURNS: (LEGS, PRICE)
    """
    async with aiohttp.ClientSession() as session:
        url = f"https://v6.db.transport.rest/journeys?from={start}&to={end}"
        if when != None:
            url+=f"&departure={when}"
        if age != None:
            url+=f"&age={age}"
        if bahncard != None:
            url+=f"&loyaltyCard={bahncard}"

        async with session.get(url) as response:
            if response.status != 200:
                return [0]
            
            data = await response.json()
            print(data["journeys"])
            return data["journeys"]