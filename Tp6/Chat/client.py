import asyncio
import aioconsole
import aiofiles
import sys
import json
import os
import argparse
from ascii_magic import AsciiArt

async def get_client_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Port du serveur", type=int, required=False)
    parser.add_argument("-a", "--addr", help="Adresse du serveur", type=str, required=False)
    args = parser.parse_args()
    if os.path.isfile("./Tp6/Chat/config.client.json") and args.addr == None and args.port == None:
        os.chdir("./Tp6/Chat")
        with open("config.client.json", "r") as f:
            config = json.load(f)
            os.chdir("../..")
            return config
    else:
        return {"server":args.addr, "port":args.port}
    
def supprimer_derniere_ligne():
    sys.stdout.write("\033[F")  # Déplacer le curseur en haut
    sys.stdout.write("\033[K")  # Supprimer la ligne
    
async def get_input(writer):
    while True:
        try:
            msg = await aioconsole.ainput()
            if msg=="exit":
                writer.write(f"exit|{msg}".encode())
                await writer.drain()
                os._exit(0)
            elif msg.startswith("/image"):
                if os.path.isfile('./Tp6/Chat/img/'+msg.split(' ')[1]):
                    supprimer_derniere_ligne()
                    print(f"Image envoyée : {msg.split(' ')[1]}")
                    my_image= AsciiArt.from_image('./Tp6/Chat/img/'+msg.split(' ')[1])
                    writer.write(f"image|{my_image.to_ascii()}".encode())
                    await writer.drain()
                else:
                    print("L'image n'existe pas ou alors elle n'est pas dans le dossier img")
            elif msg!="":
                supprimer_derniere_ligne()
                print(f"Message envoyé : {msg}")
                writer.write(f"message|{msg}".encode())
                await writer.drain()
        except asyncio.CancelledError or ConnectionResetError:
            os._exit(0)

async def async_receive(reader):
    while True:
        try:
            data = await reader.read(5000000)
            if not data:
                print("Serveur déconnecté")
                os._exit(0)
            message = data.decode()
            if (message.split("|")[0] == 'join'):
                print(message.split("|")[1])
            elif (message.split("|")[0] == 'exit'):
                print(message.split("|")[1])
            elif (message.split("|")[0] == 'message'):
                print(message.split("|")[1])
            elif (message.split("|")[0] == 'image'):
                print(message.split("image|")[1])
            else:
                pass
        except asyncio.CancelledError or ConnectionResetError:
            os._exit(0)
    
#Voir avec Léo si c'est bien ça qu'il faut faire
async def join_chat(writer, reader):
    os.system("clear") if os.name == "posix" else os.system("cls")
    try:
        pseudo = input("Entre un pseudo siteplé : ")
        writer.write(f"join|Hello|{pseudo}".encode())
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
            message = data.decode()
            if (message.split("|")[0] == 'color'):
                return message.split("|")[1].split(",")
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