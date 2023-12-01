from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import logging

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
        self.send_header('Content/type', 'text/html')
        self.protocol_version= 'HTTP/1.0'
        self.end_headers()

        if (self.path == "/toto.html"):
            file = open('./Tp5/htdocs/toto.html')
            content= file.read()
            file.close()
            content= f"{self.protocol_version} 200 OK\n\n {content}"
            self.wfile.write(bytes(content,"utf8"))
            logging.info(f"Nouveau client qui a GET {self.path}")
        elif (self.path=="/"):
            file = open('./Tp5/htdocs/index.html')
            content= file.read()
            file.close()
            content= f"{self.protocol_version} 200 OK\n\n {content}"
            self.wfile.write(bytes(content,"utf8"))
            logging.info(f"Nouveau client qui a GET {self.path}")

if __name__== "__main__":
    host="127.0.0.1"
    port=8000
    logging.info(f"Le serveur tourne sur {host}:{port}")
    server= HTTPServer((host, port),handler)
    print(f"Le serveur est disponible à l'adresse {host} sur le port {port}")
    server.serve_forever()