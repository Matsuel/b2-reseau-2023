import socket
from sys import argv

def lookup(args):
    if len(args) < 2:
        print("Veuillez préciser un nom de domaine")
        exit()
    print(socket.gethostbyname(args[-1]))

lookup(argv)