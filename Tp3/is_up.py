from sys import argv
import os


def is_up(args):
    response=0
    if len(args) < 2:
        print("Veuillez préciser une adresse IP")
        exit()
    else:
        if (os.name=="posix"):
            response=os.system("ping -c 1" + args[1]+" >/dev/null")
        else:
            response = os.system("ping -n 1 " + args[1]+" > nul")
    if response == 0:
        print("UP !")
    else:
        print("DOWN !")

is_up(argv)
