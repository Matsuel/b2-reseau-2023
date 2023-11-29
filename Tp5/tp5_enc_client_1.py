import socket 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host='127.0.0.1'
port=9999

try:
    sock.connect((host,port))
except:
    print(f"Impossible de se connecter à {host} sur le port {port} déso bro.")
    exit(1)

def checkInput(inputUsr:str)->bool:
    if inputUsr.__contains__("+") or inputUsr.__contains__("-") or inputUsr.__contains__("*"):
        operator= '+' if inputUsr.__contains__("+") else '-'if inputUsr.__contains__("-") else '*'
        if inputUsr.split(operator).__len__()==2:
            numbers= inputUsr.split(operator)
            if int(numbers[0])<4294967295  or int(numbers[1])<4294967295 :
                print(inputUsr.split(operator)[0])
                return True
            else:
                return False
        else:
            return False
    else:
        return False

while True:
    # on récup une string saisie par l'utilisateur
    operation= input('Entrer une expression arithmétique simple: ')
    if checkInput(operation) :
        # on encode le message explicitement en UTF-8 pour récup un tableau de bytes
        encoded_msg = operation.replace(' ', '').encode('utf-8')

        # on calcule sa taille, en nombre d'octets
        msg_len = len(encoded_msg)

        # on encode ce nombre d'octets sur une taille fixe de 4 octets
        header = msg_len.to_bytes(4, byteorder='big')

        # on peut concaténer ce header avec le message, avant d'envoyer sur le réseau
        payload = header + encoded_msg

        sock.send(payload)
        print(f"Opération {encoded_msg.decode('utf-8')} envoyé au serveur.")
        # on peut envoyer ça sur le réseau  

        ope_result= sock.recv(1024).decode()

        print(f"Résultat de l'opération : {ope_result}")


    else:
        print('Invalid input bro')
        continue

sock.close()