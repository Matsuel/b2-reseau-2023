from sys import argv
import os
import socket
import psutil



def network(args):
    rep=""
    if len(args)==3:
        if args[1] == "ping":
            rep=ping(args[2])
        elif args[1] == "lookup":
            rep=lookup(args)
        else:
            rep=(f"'{args[1]}' is not an available command. Déso.")
    elif (len(args)==2):
        if(args[1]=="ip"):
            rep=ip()
        else:
            rep=(f"'{args[1]}' is not an available command. Déso.")
    print(rep)



def ping(ip):
    response=0
    if (os.name=="posix"):
        response=os.system("ping -c 1 " + ip+" >/dev/null")
    else:
        response = os.system("ping -n 1 " + ip+" > nul")
    if response == 0:
        return("UP !")
    else:
        return("DOWN !")

def lookup(args):
    if len(args) < 2:
        return("Veuillez préciser un nom de domaine")
    return(socket.gethostbyname(args[-1]))

def ip():
    if(os.name=="posix"):
        return(psutil.net_if_addrs()[list(psutil.net_if_addrs().keys())[1]][0][1])
    else:
        return(psutil.net_if_addrs()['Wi-Fi'][1][1])

network(argv)