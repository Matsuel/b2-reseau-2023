from sys import argv
import os


def is_up(args):
    response=-1
    if len(args) < 2:
        return("Veuillez préciser une adresse IP")
        # exit()
    else:
        if (os.name=="posix"):
            response=os.system("ping -c 1 " + args[1]+" >/dev/null")
        else:
            response = os.system("ping -n 1 " + args[1]+" > nul")
    if response == 0:
        return ("UP !")
    else:
        return("DOWN !")

print(is_up(argv))
