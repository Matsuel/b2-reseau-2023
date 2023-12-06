import asyncio
import aioconsole
import aiofiles
import sys
import json
import os

async def get_client_config():
    os.chdir("./Tp6/Chat")
    async with aiofiles.open("config.json", "r") as f:
        config = json.loads(await f.read())
        os.chdir("../..")
        return config
    
async def get_input(writer):
    while True:
        msg = await aioconsole.ainput()
        writer.write(json.dumps({'action': 'message', 'message': msg}).encode())
        await writer.drain()
            

async def async_receive(reader):
    while True:
        data = await reader.read(1024)
        print(data.decode())
    
async def join_chat(writer):
    writer.write(json.dumps({'action': 'join'}).encode())
    await writer.drain()

async def main():
    config = await get_client_config()
    reader, writer = await asyncio.open_connection(config["server"], config["port"])
    await join_chat(writer)
    await asyncio.gather(get_input(writer), async_receive(reader))
    
if __name__ == "__main__":
    asyncio.run(main())