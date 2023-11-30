import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(('127.0.0.1', 9999))
sock.listen()
client, client_addr = sock.accept()

while True:
    # On lit les 4 premiers octets qui arrivent du client
    # Car dans le client, on a fixé la taille du header à 4 octets
    try:
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
            chunks.append(client.recv(1))
            if not chunks:
                raise RuntimeError('Invalid chunk received bro')

            # on ajoute la quantité d'octets reçus au compteur
            bytes_received += len(chunks[-1])

            #On décode les 2 nombres et l'opérateur
        first_number= int.from_bytes(chunks[0], byteorder='big')
        ope= int.from_bytes(chunks[1], byteorder='big')
        ope= "+" if ope == 1 else "-" if ope == 10 else "*"
        second_number= int.from_bytes(chunks[2], byteorder='big')
        # ptit one-liner pas combliqué à comprendre pour assembler la liste en un seul message
        message_received = "".join([str(first_number), ope, str(second_number)])
        print(f"Received from client {message_received} result {eval(message_received)}")

        res= eval(message_received)

        msg_len=1

        header= msg_len.to_bytes(4, byteorder='big')

        payload= header+ res.to_bytes(1, byteorder='big')

        client.send(payload)

        print(f"Result send to client {res}")
        # client.send(str(res).encode('utf-8'))

    except socket.error:
        print("Error occured bro.")
        exit(1)

client.close()
sock.close()
