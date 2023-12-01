import http.client

connection= http.client.HTTPConnection("127.0.0.1:8000")
# connection= http.client.HTTPConnection("ynov.com") # 302 car http
# connection= http.client.HTTPSConnection("ynov.com") renvoie le contenu de la page
connection.request('GET','/')
# connection.request('GET','/toto.html')
# response= connection.getresponse()
# print(f"Content : {response.read().decode()}")

response = connection.getresponse()

def downloadFileWithChunks(file_size):
    bytes_received = 0
    chunks = []
    while bytes_received < file_size:
        chunks.append(response.read(8))
        if not chunks:
            raise RuntimeError('Invalid chunk received bro')

        # on ajoute la quantité d'octets reçus au compteur
        bytes_received += len(chunks[-1])
    return chunks

def writeChunksToFile(chunks, file_name):
    f= open(file_name, 'wb')
    for chunk in chunks:
        f.write(chunk)
    f.close()

if response.status == 200:
    file_size = int(response.headers['Content-length'])
    file_name = response.headers['Filename']
    print(file_size)
    match(response.headers['Content-type']):
        case 'text/html':
            print(response.read().decode())
        case 'image/jpg':
            writeChunksToFile(downloadFileWithChunks(file_size), f'./Tp5/receive/{file_name}')
        case 'audio/mpeg':
            writeChunksToFile(downloadFileWithChunks(file_size), f'./Tp5/receive/{file_name}')