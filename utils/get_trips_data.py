import aiohttp

async def get_train_info(zugnr: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://v6.db.transport.rest/trips?query={zugnr}") as response:
            if response.status != 200:
                return 0
            
            data = await response.json()
            
            return data["trips"][0]