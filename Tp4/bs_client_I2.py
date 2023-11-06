import socket
import sys

# On définit la destination de la connexion
host = '10.1.1.112'  # IP du serveur
port = 13337               # Port choisir par le serveur

# Création de l'objet socket de type TCP (SOCK_STREAM)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connexion au serveur
    s.connect((host, port))
    print(f"Connecté avec succès au serveur {host} sur le port {port}")
except ConnectionRefusedError:
    print("Le serveur n'est pas joignable")
    exit(1)

strClient= input(str("Que veux-tu envoyer au serveur : "))
# Envoi de data bidon
s.sendall(strClient.encode())

# On reçoit 1024 bytes qui contiennent peut-être une réponse du serveur
data = s.recv(1024)

# On libère le socket TCP
s.close()

# Affichage de la réponse reçue du serveur
print(f"Le serveur a répondu {repr(data)}")

# On quitte le programme
exit(0)