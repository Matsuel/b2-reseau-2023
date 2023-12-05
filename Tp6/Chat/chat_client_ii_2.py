import os
import json
import socket

def get_client_config():
    os.chdir("./Tp6/Chat")
    with open("config.json", "r") as f:
        config = json.load(f)
        os.chdir("../..")
        return config

def main():
    config = get_client_config()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((config["server"], config["port"]))
    s.send("Hello".encode())
    while True:
        data = s.recv(1024)
        print(data.decode())
        break

    s.close()
 
if __name__ == "__main__":
    main()