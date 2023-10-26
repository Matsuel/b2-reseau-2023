from sys import argv
import os
import socket
import psutil



def network(args):
    if len(args)==3:
        if args[1] == "ping":
            ping(args[2])
        elif args[1] == "lookup":
            lookup(args)
        else:
            print(f"'{args[1]}' is not an available command. Déso.")
    elif (len(args)==2):
        if(args[1]=="ip"):
            ip()
        else:
            print(f"'{args[1]}' is not an available command. Déso.")



def ping(ip):
    response=0
    if (os.name=="posix"):
        response=os.system("ping -c 1 " + ip+" >/dev/null")
    response = os.system("ping -n 1 " + ip+" > nul")
    if response == 0:
        print("UP !")
    else:
        print("DOWN !")

def lookup(args):
    if len(args) < 2:
        print("Veuillez préciser un nom de domaine")
        exit()
    print(socket.gethostbyname(args[-1]))

def ip():
    if(os.name=="posix"):
        print(psutil.net_if_addrs()['wlp2s0'][0][1])
    print(psutil.net_if_addrs()['Wi-Fi'][1][1])

network(argv)