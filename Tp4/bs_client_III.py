import socket
import sys
import re 
import os
import logging

# Création du dossier de log

if not os.path.exists('/var/log/bs_client'):
    os.makedirs('/var/log/bs_client')

logging.basicConfig(filename='/var/log/bs_client/bs_client.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

opeClient= input("Saissisez l'opération que vous voulez effectuer : ")


def check_input(user_input):
    pattern = r"^([+-]?[0-9]{1,6})[-+*]([+-]?[0-9]{1,6})$"
    if re.match(pattern, user_input):
        numbers = re.findall(r"[+-]?[0-9]+", user_input)
        if len(numbers) == 2 and all(-100000 <= int(num) <= 100000 for num in numbers):
            return "True"
        else:
            return "L'opération nécessite exactement deux nombres valides"
    return "L'opération n'est pas valide. Seulement les opérations +, -, * sont autorisées et il ne doit y avoir qu'un seul signe d'opération."

if check_input(opeClient) != "True":
    raise ValueError(check_input(opeClient))

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
s.sendall(opeClient.encode())
logging.info(f"Opération envoyée au serveur {host} : {opeClient}.")

# On reçoit 1024 bytes qui contiennent peut-être une réponse du serveur
data = s.recv(1024)
logging.info(f"Réponse reçue du serveur {host} : {data.decode()}.")

# On libère le socket TCP
s.close()

# Affichage de la réponse reçue du serveur
print(f"Resultat de l'operation : {data.decode()}")

# On quitte le programme
exit(0)