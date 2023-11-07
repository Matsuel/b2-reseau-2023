import socket
import sys
import re 
import os
import logging

# Création du dossier de log

if not os.path.exists('/var/log/bs_client'):
    os.makedirs('/var/log/bs_client')

logging.basicConfig(filename='/var/log/bs_client/bs_client.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

strClient= input("Que veux-tu envoyer au serveur : ")
pattern = r"(meo|waf)"

if type(strClient) != str:
    raise TypeError("La donnée envoyée au serveur doit être de type str")
if re.search(pattern, strClient) == None:
    raise ValueError("La donnée envoyée au serveur doit contenir le mot 'meo' ou 'waf'")

# On définit la destination de la connexion
host = '10.1.1.112'  # IP du serveur
port = 13337               # Port choisir par le serveur

# Création de l'objet socket de type TCP (SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connexion au serveur
    s.connect((host, port))
    # print(f"Connecté avec succès au serveur {host} sur le port {port}")
    logging.info(f"Connexion réussie à {host}:{port}.")
except ConnectionRefusedError:
    logging.error(f"Impossible de se connecter au serveur {host} sur le port {port}.")
    # print ERROR Impossible de se connecter au serveur {host} sur le port {port}. en rouge
    print("\033[91m" + f"ERROR Impossible de se connecter au serveur {host} sur le port {port}."+ "\033[0m",)
    exit(1)

# Envoi de data bidon
s.sendall(strClient.encode())
logging.info(f"Message envoyé au serveur {host} : {strClient}.")

# On reçoit 1024 bytes qui contiennent peut-être une réponse du serveur
data = s.recv(1024)
logging.info(f"Réponse reçue du serveur {host} : {data.decode()}.")

# On libère le socket TCP
s.close()

# Affichage de la réponse reçue du serveur
print(f"Le serveur a répondu {repr(data.decode())}")

# On quitte le programme
exit(0)