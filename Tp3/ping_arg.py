from sys import argv
import os


def ping(args):
    if len(args) <2:
        return ("Veuillez préciser une adresse IP")
        # exit()
    else:
        if (os.name=="posix"):
            return os.system("ping -c 4 " + args[-1])
        else:
            return os.system("ping " + args[-1])

print(ping(argv))