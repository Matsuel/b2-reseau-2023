from http.server import BaseHTTPRequestHandler, HTTPServer

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content/type', 'text/html')
        self.protocol_version= 'HTTP/1.0'
        self.end_headers()

        content=f"{self.protocol_version} 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>"
        # HTTP/1.0 200 OK\n\n<h1>Hello je suis un serveur HTTP</h1>
        self.wfile.write(bytes(content,'utf8'))

if __name__== "__main__":
    host="127.0.0.1"
    port=8000
    server= HTTPServer((host, port),handler)
    print(f"Le serveur est disponible à l'adresse {host} sur le port {port}")
    server.serve_forever()