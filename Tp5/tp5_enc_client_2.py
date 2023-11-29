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
    
def getOperator(inputStr:str)-> str:
    if inputStr.__contains__("+"):
        return "+"
    elif inputStr.__contains__("-"):
        return "-"
    elif inputStr.__contains__("*"):
        return "*"

while True:
    # on récup une string saisie par l'utilisateur
    operation= input('Entrer une expression arithmétique simple: ')
    try:
        if checkInput(operation) :

            #On récupère le signe de l'opération
            operator= getOperator(operation)

            #On récupère ensuite le premier nombre de l'opération
            first_number= int(operation.split(operator)[0].replace(' ','')).to_bytes(1, byteorder='big')
            #On récupère le deuxième nombre
            second_number= int(operation.split(operator)[1].replace(' ','')).to_bytes(1,byteorder='big')
            #On définit ensuite + à 01, - à 10 et *à 11
            operator= 1 if operator=="+" else 10 if operator=="-" else 11
            print(operator)
            operator= operator.to_bytes(1,byteorder='big')

            # on calcule sa taille, en nombre d'octets 3, 2chiffres et 1 opérateur
            msg_len = 3

            # on encode ce nombre d'octets sur une taille fixe de 4 octets
            header = msg_len.to_bytes(4, byteorder='big')

            # on peut concaténer ce header avec le message, avant d'envoyer sur le réseau
            payload = header + first_number+ operator+ second_number

            sock.send(payload)
            print(f"Opération {operation} envoyé au serveur.")
            # on peut envoyer ça sur le réseau  

            ope_result= sock.recv(1024).decode()

            print(f"Résultat de l'opération : {ope_result}")


        else:
            print('Invalid input bro')
            continue
    
    except KeyboardInterrupt:
        print("Interruption de l'utilisateur")
        sock.close()
        exit(1)


sock.close()