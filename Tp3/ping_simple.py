import os

def ping_simple():
    if(os.name=="posix"):
        return os.system("ping -c 4 8.8.8.8")
    else:
        return os.system("ping 8.8.8.8")  # ping google

print(ping_simple())