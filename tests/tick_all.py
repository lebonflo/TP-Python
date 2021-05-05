import aiohttp
import asyncio
from rich import print
from datetime import datetime
import yaml

async def main():

    try:

        async with aiohttp.ClientSession() as session:
            async with session.get('http://51.15.17.205:9000/tick/Mohamed') as resp:

                info = await resp.json()
                info['timestamp'] = datetime.timestamp(datetime.now())
                data = yaml.dump(info)
                filename = f"./tick/data/{datetime.now().isoformat()}.yaml"
                with open(filename, "w") as f:
                    f.write(data)

        return aiohttp.web.json_response(info)
    except Exception as e:
        print(e)
        raise e

loop = asyncio.get_event_loop()
loop.run_until_complete(main())