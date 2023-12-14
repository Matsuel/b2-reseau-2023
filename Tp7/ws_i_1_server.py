import asyncio
from websockets.server import serve

async def handler(websocket, path):
    while True:
        try:
            data = await websocket.recv()
            print(f"Received: {data}")
            await websocket.send(f"Hello client ! Received {data}")
        except :
            break

async def main():
    async with serve(handler, 'localhost', 8000):
        while True:
            await asyncio.Future()  # run forever

if __name__ == '__main__':
    asyncio.run(main())