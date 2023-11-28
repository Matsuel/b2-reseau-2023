import socket 

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('127.0.0.1', 9999))

# on récup une string saisie par l'utilisateur
operation= input('Entrer une expression arithmétique simple: ')

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
    # on peut envoyer ça sur le réseau  


    sock.close()
else:
    raise RuntimeError('Invalid input bro')