from aiohttp import ClientSession

async def AsyncGet(szUrl, pHeaders=None):
    try:
        async with ClientSession() as session:
            async with session.get(szUrl, headers=pHeaders) as response:
                data = await response.text()
                return data
    except:
        return False
