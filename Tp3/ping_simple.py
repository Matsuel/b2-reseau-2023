import os

def ping_simple():
    if(os.name=="posix"):
        os.system("ping -c 4 8.8.8.8")
    else:
        os.system("ping 8.8.8.8")  # ping google

ping_simple()