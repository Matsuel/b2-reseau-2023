import asyncio
from websockets.client import connect
import websockets
import aioconsole

async def handle_server(websocket):
    while True:
        try:
            message = await websocket.recv()
            print(message)
        except websockets.ConnectionClosed:
            break

async def handle_input(websocket):
    while True:
        message = await aioconsole.ainput()
        await websocket.send(message)

async def main():
    async with connect('ws://localhost:8000') as websocket:
        while True:
            try:
                await asyncio.gather(
                    handle_server(websocket),
                    handle_input(websocket),
                )
            except :
                break
        

if __name__ == '__main__':
    asyncio.run(main())