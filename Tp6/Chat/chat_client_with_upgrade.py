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
    
def supprimer_derniere_ligne():
    sys.stdout.write("\033[F")  # Déplacer le curseur en haut
    sys.stdout.write("\033[K")  # Supprimer la ligne
    
async def get_input(writer):
    while True:
        try:
            msg = await aioconsole.ainput()
            if msg=="exit":
                writer.write(json.dumps({'action': 'exit', 'message':''}).encode())
                await writer.drain()
                os._exit()
            elif msg!="":
                supprimer_derniere_ligne()
                print(f"Message envoyé : {msg}")
                writer.write(json.dumps({'action': 'message', 'message': msg}).encode())
                await writer.drain()
        except asyncio.CancelledError or ConnectionResetError:
            os._exit()

async def async_receive(reader):
    while True:
        try:
            data = await reader.read(1024)
            if not data:
                print("Serveur déconnecté")
                os._exit(0)
            message = json.loads(data.decode())
            if (message['action']=='join'):
                print(f"\033[38;2;{message['color'][0]};{message['color'][1]};{message['color'][2]}m{message['pseudo']}\033[0m {message['message']}")
            elif (message['action']=='exit'):
                print(f"Annonce \033[38;2;{message['color'][0]};{message['color'][1]};{message['color'][2]}m{message['pseudo']}\033[0m {message['message']}")
            elif (message['action']=='message'):
                print(f"[{str(message['hour'])}] \033[38;2;{message['color'][0]};{message['color'][1]};{message['color'][2]}m{message['pseudo']}\033[0m : {message['message']}")
            else:
                pass
        except asyncio.CancelledError or ConnectionResetError:
            os._exit(0)
    
#Voir avec Léo si c'est bien ça qu'il faut faire
async def join_chat(writer, reader):
    os.system("clear") if os.name == "posix" else os.system("cls")
    try:
        pseudo = input("Entre un pseudo siteplé : ")
        writer.write(json.dumps({'action': 'join', 'pseudo': f"Hello|{pseudo}"}).encode())
        os.system("clear") if os.name == "posix" else os.system("cls")
        await writer.drain()
        color = await get_color(reader)
        print(f"Bienvenue dans le chat bro ! \033[38;2;{color[0]};{color[1]};{color[2]}m{pseudo}\033[0m")
    except asyncio.CancelledError:
        sys.exit(0)

async def get_color(reader):
    while True:
        try:
            data = await reader.read(1024)
            if not data:
                print("Serveur déconnecté")
                os._exit(0)
            message = json.loads(data.decode())
            if (message['action']=='color'):
                return message['color']
        except asyncio.CancelledError or ConnectionResetError:
            os._exit(0)

async def main():
    config = await get_client_config()
    try:
        reader, writer = await asyncio.open_connection(config["server"], config["port"])
    except OSError or ConnectionRefusedError or ConnectionResetError or ConnectionError:
        print("Le serveur n'est pas disponible")
        sys.exit(1)
    await join_chat(writer, reader)
    try:
        await asyncio.gather(get_input(writer), async_receive(reader))
    except asyncio.CancelledError or ConnectionResetError:
        sys.exit(0)
    
if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        os._exit(0)