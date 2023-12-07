import asyncio
import aioconsole
import aiofiles
import sys
import json
import os
import concurrent.futures

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
    
#Voir avec Léo si c'est bien ça qu'il faut faire
async def join_chat(writer):
    os.system("clear") if os.name == "posix" else os.system("cls")
    pseudo = input("Enter your pseudo : ")
    writer.write(json.dumps({'action': 'join', 'pseudo': f"Hello|{pseudo}"}).encode())
    os.system("clear") if os.name == "posix" else os.system("cls")
    print(f"Welcome to the chatroom ! {pseudo}")
    await writer.drain()

async def main():
    config = await get_client_config()
    reader, writer = await asyncio.open_connection(config["server"], config["port"])
    await join_chat(writer)
    await asyncio.gather(get_input(writer), async_receive(reader))
    
if __name__ == "__main__":
    asyncio.run(main())