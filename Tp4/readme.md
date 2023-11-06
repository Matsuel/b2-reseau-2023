# I. Simple bs program

# Serveur:

## Ouverture du port dans le firewall

```bash
[user1@node1 Tp4]$ sudo firewall-cmd --add-port=13337/tcp --permanent
success
[user1@node1 Tp4]$ sudo firewall-cmd --reload
success
```

## Execution sur le seveur

```bash
[user1@node1 Tp4]$ python bs_server_I1.py
Connected by ('10.1.1.113', 45200)
Données reçues du client : b'Meooooo !'
```

## SS surle serveur

```bash
[user1@node1 Tp4]$ sudo ss -alnpt | grep python
LISTEN 0      1         10.1.1.112:13337      0.0.0.0:*    users:(("python",pid=1402,fd=3))
```

# Cliet:

```bash
[user1@node1 Tp4]$ python bs_client_I1.py
Le serveur a répondu b'Hi mate !'
```