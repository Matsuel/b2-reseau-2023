import asyncio
import os
import json
import random
import datetime

global CLIENTS 
CLIENTS = {}

async def get_server_config():
    os.chdir("./Tp6/Chat")
    with open("config.json", "r") as f:
        config = json.load(f)
        os.chdir("../..")
        return config

# cette fonction sera appelée à chaque fois qu'on reçoit une connexion d'un client
async def handle_client_msg(reader, writer):
    while True:
        # les objets reader et writer permettent de lire/envoyer des données auux clients

        try:

            # on lit les 1024 prochains octets
            # notez le await pour indiquer que cette opération peut produire de l'attente
            data = await reader.read(1024)
            addr = writer.get_extra_info('peername')

            # si le client n'envoie rien, il s'est sûrement déco
            if data == b'':
                break

            # on décode et affiche le msg du client
            message = json.loads(data.decode())
            if (message['action'] == 'join' and message['pseudo'].startswith("Hello")):
                pseudo = str(message['pseudo']).split("|")[1].capitalize()
                add_client(addr, reader, writer, pseudo)
                await send_color(addr)
                print(f"\033[38;2;{CLIENTS[addr]['color'][0]};{CLIENTS[addr]['color'][1]};{CLIENTS[addr]['color'][2]}m{pseudo}\033[0m joined : {addr}")
                await send_join(json.dumps({'action': 'join', 'pseudo': pseudo, 'color': CLIENTS[addr]["color"], 'message':'a rejoint la chatroom.', 'addr':addr}),pseudo)
            elif (message['action'] == 'exit'):
                print(f"\033[38;2;{CLIENTS[addr]['color'][0]};{CLIENTS[addr]['color'][1]};{CLIENTS[addr]['color'][2]}m{CLIENTS[addr]['pseudo']}\033[0m left : {addr}")
                await send_to_all(json.dumps({'action': 'exit', 'pseudo': CLIENTS[addr]['pseudo'], 'color': CLIENTS[addr]["color"], 'message':'a quitté la chatroom.', 'addr':addr}), addr)
                CLIENTS.pop(addr)
            else:
                hour = datetime.datetime.now().strftime("%H:%M")
                print(f"Message received from \033[38;2;{CLIENTS[addr]['color'][0]};{CLIENTS[addr]['color'][1]};{CLIENTS[addr]['color'][2]}m{CLIENTS[addr]['pseudo']}\033[0m : {message['message']} at {hour}")
                await send_to_all(json.dumps({'action': 'message', 'hour': hour  , 'pseudo': CLIENTS[addr]['pseudo'], 'color': CLIENTS[addr]["color"], 'message':message['message'], 'addr':addr}), addr)

        except Exception as e:
            break

def add_client(addr, reader, writer, pseudo):
    CLIENTS[addr]={}
    CLIENTS[addr]["r"] = reader
    CLIENTS[addr]["w"] = writer
    CLIENTS[addr]["pseudo"] = pseudo
    CLIENTS[addr]["color"] = [random.randint(0,255),random.randint(0,255),random.randint(0,255)]

async def send_to_all(message, addr):
    for client in CLIENTS:
        if client != addr:
            CLIENTS[client]["w"].write(message.encode())
            await CLIENTS[client]["w"].drain()

async def send_join(message,pseudo):
    for client in CLIENTS:
        if CLIENTS[client]["pseudo"] != pseudo:
            CLIENTS[client]["w"].write(message.encode())
            await CLIENTS[client]["w"].drain()

async def send_color(addr):
    CLIENTS[addr]["w"].write(json.dumps({'action': 'color', 'color': CLIENTS[addr]["color"]}).encode())
    await CLIENTS[addr]["w"].drain()

async def main():
    config= await get_server_config()
    # on crée un objet server avec asyncio.start_server()
    ## on précise une fonction à appeler quand un paquet est reçu
    ## on précise sur quelle IP et quel port écouter
    server = await asyncio.start_server(handle_client_msg, config["server"], config["port"])

    # ptit affichage côté serveur
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    os.system("clear") if os.name == "posix" else os.system("cls")
    print(f'Serving on {addrs}')

    # on lance le serveur
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    # lancement du main en asynchrone avec asyncio.run()
    asyncio.run(main())