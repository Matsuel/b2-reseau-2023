import socket

host = '10.1.1.112'
port = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  

s.listen(1)
conn, addr = s.accept()
print('Hi mate !', addr)

while True:

    try:
        data = conn.recv(1024)
        if not data: break
        print(f"Données reçues du client : {data}")
        conn.sendall(bytes("Salut mec."))

    except socket.error:
        print("Error Occured.")
        break

# On ferme proprement la connexion TCP
conn.close()
