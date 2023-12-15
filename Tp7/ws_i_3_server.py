import asyncio
import os
import json
import websockets

global CLIENTS
CLIENTS = {}

async def handle_client_msg(websocket, path):
    addr = websocket.remote_address
    while True:
        try:
            message = await websocket.recv()
            if not message:
                break
            message = json.loads(message)
            if message["type"] == "join":
                pseudo = message["pseudo"].capitalize()
                print(f"{pseudo} joined : {addr}")
                add_client(addr, websocket, pseudo)
                await send_join(pseudo, websocket)
            else:
                print(f"Message received from {CLIENTS[addr]['pseudo']} : {message["message"]} ")
                await send_to_all(f"{CLIENTS[addr]['pseudo']} : {message["message"]}", websocket)

        except:
            print(f"{CLIENTS[addr]['pseudo']} disconnected")
            CLIENTS.pop(addr)
            break

def add_client(addr, websocket, pseudo):
    CLIENTS[addr] = {}
    CLIENTS[addr]["ws"] = websocket
    CLIENTS[addr]["pseudo"] = pseudo

async def send_to_all(message, websocket):
    for client in CLIENTS:
        if client != websocket.remote_address:
            await CLIENTS[client]["ws"].send(message)

async def send_join(pseudo, websocket):
    for client in CLIENTS:
        if client != websocket.remote_address:
            await CLIENTS[client]["ws"].send(f"{pseudo} a rejoint le chat !")
        else:
            clientList= [CLIENTS[client]["pseudo"] for client in CLIENTS if client != websocket.remote_address]
            if len(clientList)>0:
                await CLIENTS[client]["ws"].send(f"Bienvenue sur le chat ! Vous pouvez commencer à discuter avec {clientList} !")
            else:
                await CLIENTS[client]["ws"].send(f"Bienvenue sur le chat ! Vous êtes seul pour le moment !")

async def main():
    server = await websockets.serve(handle_client_msg, 'localhost', 8000)

    os.system("clear") if os.name == "posix" else os.system("cls")
    print(f'Serving on 127.0.0.1:8000')

    async with server:
        await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())