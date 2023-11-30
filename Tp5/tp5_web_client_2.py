import http.client

# connection= http.client.HTTPConnection("127.0.0.1:8000")
connection= http.client.HTTPConnection("ynov.com") # 302 car http
# connection= http.client.HTTPSConnection("ynov.com") renvoie le contenu de la page
connection.request('GET','/')
response= connection.getresponse()
print(f"Content : {response.read().decode()}")