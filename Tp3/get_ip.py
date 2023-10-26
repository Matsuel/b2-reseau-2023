import psutil
import os


"""
Note à moi-même:
La fonction psutil.net_if_addrs() retourne un dictionnaire contenant les interfaces réseaux de la machine.
On renvoie donc la valeur de la clé 'Wi-Fi' (qui est le nom de l'interface réseau de mon ordinateur) et on prend
le deuxième élément de la liste qui est un tuple. On prend ensuite le deuxième élément de ce tuple qui est l'adresse Ip wifi de mon ordinateur.
"""
def ip():
    if(os.name=="posix"):
        print(psutil.net_if_addrs()[list(psutil.net_if_addrs().keys())[1]][0][1])
        # print(psutil.net_if_addrs()['wlp2s0'][0][1])
    print(psutil.net_if_addrs()['Wi-Fi'][1][1])


ip()