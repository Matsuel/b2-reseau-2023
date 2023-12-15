import asyncio
import os
import json
import websockets
import redis.asyncio as redis

global Sockets
Sockets = {}

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
                await add_client(addr, websocket, pseudo)
                await send_join(pseudo, websocket)
            else:
                print(f"Message reçu de {addr} a dit {message["message"]} ")
                await send_to_all(f"{await get_client(addr)} a dit {message["message"]}", websocket)
        except:
            print(f"Client {await get_client(addr)} déconnecté")
            await remove_client(addr)
            break

async def remove_client(addr):
    await clients.delete(str(addr))
    Sockets.pop(str(addr))

async def add_client(addr, websocket, pseudo):
    await clients.set(str(addr), json.dumps({"pseudo":pseudo}))
    Sockets[str(addr)] = websocket

async def get_client(addr):
    datas= json.loads(await clients.get(str(addr)))
    return datas["pseudo"]


async def send_to_all(message, websocket):
    for client in await clients.keys():
        client= client.decode()
        datas = json.loads(await clients.get(client))
        if client != str(websocket.remote_address):
            await Sockets[client].send(message)

async def get_users(websocket):
    list_clients=[]
    for client in await clients.keys():
        client= client.decode()
        if client != str(websocket.remote_address):
            datas = json.loads(await clients.get(client))
            list_clients.append(datas['pseudo'])
    return list_clients


async def send_join(pseudo, websocket):
    for client in await clients.keys():
        client= client.decode()
        datas = json.loads(await clients.get(client))
        if client != str(websocket.remote_address):
            await Sockets[client].send(f"{pseudo} a rejoint le chat !")
        else:
            clientList= await get_users(websocket)
            if len(clientList)==1:
                await Sockets[client].send(f"Bienvenue sur le chat ! Vous pouvez commencer à discuter avec {clientList} !")
            else:
                await Sockets[client].send(f"Bienvenue sur le chat ! Vous êtes seul pour le moment !")


async def main():
    server = await websockets.serve(handle_client_msg, 'localhost', 8000)

    global clients
    clients = await redis.Redis(host='localhost', port=6379)

    await clients.flushall()

    os.system("clear") if os.name == "posix" else os.system("cls")
    print(f'Serving on 127.0.0.1:8000')

    async with server:
        await server.wait_closed()

if __name__ == '__main__':
    asyncio.run(main())