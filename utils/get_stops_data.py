import aiohttp

async def get_departure_data(stationid: int, only_fernverkehr:bool=False, duration:int=60) -> dict:
    """
    GET DEPARTURE DATA OF GIVEN STATIONID
    RETURNS: DEPARTURES
    """
    url = f"https://v6.db.transport.rest/stops/{stationid}/departures?bus=false&tram=false&taxi=false&subway=false&results=13&duration={duration}"
    if only_fernverkehr:
        url = url + "&nationalExpress=true&national=true&regional=false&suburban=false"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return 0
            
            data = await response.json()

            return data["departures"]