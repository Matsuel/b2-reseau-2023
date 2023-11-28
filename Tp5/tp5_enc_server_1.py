import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 9999))
sock.listen()
client, client_addr = sock.accept()

while True:
    # On lit les 4 premiers octets qui arrivent du client
    # Car dans le client, on a fixé la taille du header à 4 octets
    header = client.recv(4)
    if not header:
        break

    # On lit la valeur
    msg_len = int.from_bytes(header[0:4], byteorder='big')

    print(f"Lecture des {msg_len} prochains octets")

    # Une liste qui va contenir les données reçues
    chunks = []

    bytes_received = 0
    while bytes_received < msg_len:
        # Si on reçoit + que la taille annoncée, on lit 1024 par 1024 octets
        chunk = client.recv(min(msg_len - bytes_received,
                                1024))
        if not chunk:
            raise RuntimeError('Invalid chunk received bro')

        # on ajoute le morceau de 1024 ou moins à notre liste
        chunks.append(chunk)

        # on ajoute la quantité d'octets reçus au compteur
        bytes_received += len(chunk)

    # ptit one-liner pas combliqué à comprendre pour assembler la liste en un seul message
    message_received = b"".join(chunks).decode('utf-8')
    print(f"Received from client {message_received} result {eval(message_received)}")

client.close()
sock.close()
