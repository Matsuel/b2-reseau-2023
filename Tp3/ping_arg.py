from sys import argv
import os


def ping(args):
    if len(args) <2:
        print("Veuillez préciser une adresse IP")
        exit()
    else:
        if (os.name=="posix"):
            os.system("ping -c 4 " + args[-1])
        else:
            os.system("ping " + args[-1])

ping(argv)