import aiohttp
import asyncio
from rich import print

async def main():

    async with aiohttp.ClientSession() as session:

        async with session.get('http://localhost:9000/tick/') as resp:

            info = await resp.json()
#             info['timestamp'] = datetime.timestamp(datetime.now())
#             data = yaml.dump(info)
#             filename = f"./tick/data/{datetime.now().isoformat()}.yaml"
#             with open(filename, "w") as f:
#                 f.write(data)
            print(info)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())