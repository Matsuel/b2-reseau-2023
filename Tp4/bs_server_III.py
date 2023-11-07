import argparse
import socket
import sys
import logging
import time
import threading
import os

# Création du dossier de log
if not os.path.exists('/var/log/bs_server'):
    os.makedirs('/var/log/bs_server')


logging.basicConfig(filename='/var/log/bs_server/bs_server.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

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
print("\033[255m" + "INFO" + "\033[0m", f"Le serveur tourne sur {host}:{port}")


last_connection_time = time.time()

def check_connections():
    global last_connection_time
    while True:
        time.sleep(60)  # Attendre une minute
        if time.time() - last_connection_time > 60:
            logging.warning("Aucun client depuis plus de une minute.")
            print("\033[93m" + "WARN" + "\033[0m", "Aucun client depuis plus de une minute.")

# Démarrer le thread de vérification des connexions
threading.Thread(target=check_connections, daemon=True).start()



s.listen(1)


while True:
    conn, addr = s.accept()
    last_connection_time = time.time() 
    print(f"Un client vient de se co et son IP c'est {addr[0]}.")
    logging.info(f"Un client {addr[0]} s'est connecté.")
    print("\033[255m" + "INFO" + "\033[0m", f"Un client {addr[0]} s'est connecté.")
    try:
        data = conn.recv(1024)
        if not data: break
        else:
            logging.info(f"Le client {addr[0]} a envoyé {data.decode()}.")
            print("\033[255m" + "INFO" + "\033[0m", f"Le client {addr[0]} a envoyé une opération : {data.decode()}.")
            conn.sendall(str(eval(data.decode())).encode())
            logging.info(f"Resultat envoyé au client {addr[0]} : {eval(data.decode())}.")
    except socket.error:
        print("Error Occured.")
        break

# On ferme proprement la connexion TCP
conn.close()
