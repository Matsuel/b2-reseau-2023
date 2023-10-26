import socket
from sys import argv

def lookup(args):
    if len(args) < 2:
        return("Veuillez préciser un nom de domaine")
        exit()
    return(socket.gethostbyname(args[-1]))

print(lookup(argv))