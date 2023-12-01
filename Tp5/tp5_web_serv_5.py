from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import logging
import argparse

parser=argparse.ArgumentParser()
parser.add_argument("-t", "--type", type=str, default="image/jpg", action="store", help="Type de fichier à envoyer image/jpg, text/html, audio/mpeg" )

args= parser.parse_args()

print(args.type)

if (os.name=="posix"):
    # Création du dossier de log
    if not os.path.exists('/var/log/web_server'):
        os.makedirs('/var/log/web_server')
        logging.basicConfig(filename='/var/log/web_server/serv4.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
else:
    #Création du dossier de log
    if not os.path.exists('./Tp5/log/web_server'):
        os.makedirs('./Tp5/log/web_server')
        logging.basicConfig(filename='./Tp5/log/web_server/serv4.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.protocol_version= 'HTTP/1.0'
        self.send_header('Content-type', args.type)
        file_name=""
        if args.type == "image/jpg":
            file_name= "issou.jpg"
            file = open(f'./Tp5/src/{file_name}', 'rb')
        elif args.type == "text/html":
            file = open('./Tp5/htdocs/index.html')
        elif args.type== "audio/mpeg":
            file_name= "issou.mp3"
            file = open(f'./Tp5/src/{file_name}', 'rb')
        content= file.read()
        file_size= os.path.getsize(f'./Tp5/src/{file_name}')
        self.send_header('Content-length', str(file_size))
        self.send_header('Filename', file_name)
        self.end_headers()
        file.close()
        chunks= [content[i:i+8] for i in range(0, len(content), 8)]
        for chunk in chunks:
            self.wfile.write(chunk)
        logging.info(f"Nouveau client qui a GET {self.path}")

if __name__== "__main__":
    host="127.0.0.1"
    port=8000
    logging.info(f"Le serveur tourne sur {host}:{port}")
    server= HTTPServer((host, port),handler)
    print(f"Le serveur est disponible à l'adresse {host} sur le port {port}")
    server.serve_forever()