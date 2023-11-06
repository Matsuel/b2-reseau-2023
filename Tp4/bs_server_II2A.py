import argparse
import socket
import sys
import logging
import time

dateStart = time.time()

logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

parser=argparse.ArgumentParser()
parser.add_argument("-p", "--port", type=int, default=13337, action="store", help="Port d'écoute du serveur" )
# parser.add_argument("-h","--help", action="store", help="Affiche l'aide")

args=parser.parse_args()

port=0

if not args.port:
    port=13337
if args.port <0 or args.port > 65535:
    print("ERROR Le port spécifié n'est pas un port possible (de 0 à 65535).")
    exit(1)
elif args.port < 1024:
    print("ERROR Le port spécifié est un port privilégié. Spécifiez un port au dessus de 1024.")
    exit(2)
else:
    port=args.port

host = '10.1.1.112'





s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  
logging.info(f"Le serveur tourne sur {host}:{port}")

s.listen(1)
conn, addr = s.accept()
print(f"Un client vient de se co et son IP c'est {addr[0]}.")
logging.info(f"Un client {addr[0]} s'est connecté.")

while True:

    if (time.time() - dateStart) > 60:
        dateStart = time.time()
        logging.warn("Aucun client depuis plus de une minute.")

    try:
        data = conn.recv(1024)
        if not data: break
        else:
            logging.info(f"Le client {addr[0]} a envoyé {data.decode()}.")
            if str(data).__contains__("meo"):
                conn.sendall(b"Meo a toi confrere.")
                logging.info(f"Réponse envoyée au client {addr[0]} : Meo a toi confrere.")
            elif str(data).__contains__("waf"):
                conn.sendall(b"ptdr t ki")
                logging.info(f"Réponse envoyée au client {addr[0]} : ptdr t ki.")
            else:
                conn.sendall(b"Mes respects humble humain.")
                logging.info(f"Réponse envoyée au client {addr[0]} : Mes respects humble humain.")

    except socket.error:
        print("Error Occured.")
        break

# On ferme proprement la connexion TCP
conn.close()
