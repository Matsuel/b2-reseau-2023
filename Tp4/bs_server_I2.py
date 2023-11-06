import socket

host = '10.1.1.112'
port = 13337

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))  

s.listen(1)
conn, addr = s.accept()
print(f"Un client vient de se co et son IP c'est {addr}.")

while True:

    try:
        data = conn.recv(1024)
        if not data: break
        if str(data).__contains__("meo"):
            conn.sendall(b"Meo a toi confrere.")
        elif str(data).__contains__("waf"):
            conn.sendall(b"ptdr t ki")
        else:
            conn.sendall(b"Mes respects humble humain.")

    except socket.error:
        print("Error Occured.")
        break

# On ferme proprement la connexion TCP
conn.close()
