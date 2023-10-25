# TP2 : Environnement virtuel

Dans ce TP, on remanipule toujours les mêmes concepts qu'au TP1, mais en environnement virtuel avec une posture un peu plus orientée administrateur qu'au TP1.

- [TP2 : Environnement virtuel](#tp2--environnement-virtuel)
- [0. Prérequis](#0-prérequis)
- [I. Topologie réseau](#i-topologie-réseau)
  - [Topologie](#topologie)
  - [Tableau d'adressage](#tableau-dadressage)
  - [Hints](#hints)
  - [Marche à suivre recommandée](#marche-à-suivre-recommandée)
  - [Compte-rendu](#compte-rendu)
- [II. Interlude accès internet](#ii-interlude-accès-internet)
- [III. Services réseau](#iii-services-réseau)
  - [1. DHCP](#1-dhcp)
  - [2. Web web web](#2-web-web-web)

# 0. Prérequis

# I. Topologie réseau

Vous allez dans cette première partie préparer toutes les VMs et vous assurez que leur connectivité réseau fonctionne bien.

On va donc parler essentiellement IP et routage ici.

## Topologie

## Tableau d'adressage

| Node             | LAN1 `10.1.1.0/24` | LAN2 `10.1.2.0/24` |
| ---------------- | ------------------ | ------------------ |
| `node1.lan1.tp1` | `10.1.1.11`        | x                  | fé
| `node2.lan1.tp1` | `10.1.1.12`        | x                  | fe
| `node1.lan2.tp1` | x                  | `10.1.2.11`        | fé
| `node2.lan2.tp1` | x                  | `10.1.2.12`        | fé
| `router.tp1`     | `10.1.1.254`       | `10.1.2.254`       | fé


![Fatigué](https://media.giphy.com/media/xT8qBvH1pAhtfSx52U/giphy.gif)

## Hints

➜ **Sur le `router.tp1`**

Il sera nécessaire d'**activer le routage**. Par défaut Rocky n'agit pas comme un routeur. C'est à dire que par défaut il ignore les paquets qu'il reçoit s'il l'IP de destination n'est pas la sienne. Or, c'est précisément le job d'un routeur.

> Dans notre cas, si `node1.lan1.tp1` ping `node1.lan2.tp1`, le paquet a pour IP source `10.1.1.11` et pour IP de destination `10.1.2.11`. Le paquet passe par le routeur. Le routeur reçoit donc un paquet qui a pour destination `10.1.2.11`, une IP qui n'est pas la sienne. S'il agit comme un routeur, il comprend qu'il doit retransmettre le paquet dans l'autre réseau. Par défaut, la plupart de nos OS ignorent ces paquets, car ils ne sont pas des routeurs.

Pour activer le routage donc, sur une machine Rocky :

```bash
$ firewall-cmd --add-masquerade
$ firewall-cmd --add-masquerade --permanent
$ sysctl -w net.ipv4.ip_forward=1

[user1@router ~]$ sudo firewall-cmd --add-masquerade
[sudo] password for user1:
success
[user1@router ~]$ sudo firewall-cmd --add-masquerade --permanent
success
[user1@router ~]$ sudo sysctl -w net.ipv4.ip_forward=1
net.ipv4.ip_forward = 1
```

![Hacker](https://media.giphy.com/media/B4dt6rXq6nABilHTYM/giphy.gif)

---

➜ **Les switches sont les host-only de VirtualBox pour vous**

Vous allez donc avoir besoin de créer deux réseaux host-only. Faites bien attention à connecter vos VMs au bon switch host-only.

---

➜ **Aucune carte NAT**


## Compte-rendu

☀️ Sur **`node1.lan1.tp1`**

- afficher ses cartes réseau

```bash
[user1@node1 ~]$ ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enp0s3: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 08:00:27:45:46:3f brd ff:ff:ff:ff:ff:ff
    inet 10.1.1.11/24 brd 10.1.1.255 scope global noprefixroute enp0s3
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe45:463f/64 scope link
       valid_lft forever preferred_lft forever
```

- afficher sa table de routage

```bash
[user1@node1 ~]$ ip r s
10.1.1.0/24 dev enp0s3 proto kernel scope link src 10.1.1.11 metric 100
10.1.2.0/24 via 10.1.1.254 dev enp0s3 proto static metric 100
```

- prouvez qu'il peut joindre `node2.lan2.tp2`

```bash
[user1@node1 ~]$ ping node2.lan2.tp1 -c 4
PING node2.lan2.tp1 (10.1.2.12) 56(84) bytes of data.
64 bytes from node2.lan2.tp1 (10.1.2.12): icmp_seq=1 ttl=63 time=1.76 ms
64 bytes from node2.lan2.tp1 (10.1.2.12): icmp_seq=2 ttl=63 time=1.29 ms
64 bytes from node2.lan2.tp1 (10.1.2.12): icmp_seq=3 ttl=63 time=1.44 ms
64 bytes from node2.lan2.tp1 (10.1.2.12): icmp_seq=4 ttl=63 time=1.29 ms

--- node2.lan2.tp1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3004ms
rtt min/avg/max/mdev = 1.290/1.445/1.761/0.192 ms
```

- prouvez avec un `traceroute` que le paquet passe bien par `router.tp1`

```bash
[user1@node1 ~]$ traceroute node2.lan2.tp1
traceroute to node2.lan2.tp1 (10.1.2.12), 30 hops max, 60 byte packets
 1  10.1.1.254 (10.1.1.254)  1.637 ms  1.393 ms  1.491 ms
 2  10.1.2.12 (10.1.2.12)  2.545 ms !X  5.023 ms !X  4.819 ms !X
```

# II. Interlude accès internet

**On va donner accès internet à tout le monde.** Le routeur aura un accès internet, et permettra à tout le monde d'y accéder : il sera la passerelle par défaut des membres du LAN1 et des membres du LAN2.

**Ajoutez une carte NAT au routeur pour qu'il ait un accès internet.**

☀️ **Sur `router.tp1`**

- prouvez que vous avez un accès internet (ping d'une IP publique)

```bash
[user1@router ~]$ ping -c 4 172.67.74.226 | grep packets
4 packets transmitted, 4 received, 0% packet loss, time 3007ms
```

- prouvez que vous pouvez résoudre des noms publics (ping d'un nom de domaine public)

```bash
[user1@router ~]$ ping -c 4 instagram.com | grep packets
4 packets transmitted, 4 received, 0% packet loss, time 3008ms
```

☀️ **Accès internet LAN1 et LAN2**

- ajoutez une route par défaut sur les deux machines du LAN1
- ajoutez une route par défaut sur les deux machines du LAN2
- configurez l'adresse d'un serveur DNS que vos machines peuvent utiliser pour résoudre des noms
- dans le compte-rendu, mettez-moi que la conf des points précédents sur `node2.lan1.tp1`

```bash
[user1@node2 ~]$ sudo cat /etc/sysconfig/network-scripts/route-enp0s3 | grep default
[sudo] password for user1:
default via 10.1.1.254 dev eth0

[user1@node2 ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s3 | grep DNS
DNS1=1.1.1.1
```

**Ces 2 lignes permmettent de donner une route par défaut qui permettra à node2.lan1.tp1 d'accéder à internet et la seconde ligne lui permettra d'avoir un serveur DNS afin d'être capable de pouvoir ping des noms de domaines**

**Pour lan2 on remplacer 10.1.1.254 par 10.1.2.254 dans le fichier de configuration des interfaces**

- prouvez que `node2.lan1.tp1` a un accès internet :
  - il peut ping une IP publique
  ```bash
  [user1@node2 ~]$ ping -c 4 172.67.74.226 | grep packets
  4 packets transmitted, 4 received, 0% packet loss, time 3008ms
  ```
  - il peut ping un nom de domaine public
  ```bash
  [user1@node2 ~]$ ping -c 4 twitter.com | grep packets
  4 packets transmitted, 4 received, 0% packet loss, time 3007ms
  ```


# III. Services réseau

**Adresses IP et routage OK, maintenant, il s'agirait d'en faire quelque chose nan ?**

Dans cette partie, on va **monter quelques services orientés réseau** au sein de la topologie, afin de la rendre un peu utile que diable. Des machines qui se `ping` c'est rigolo mais ça sert à rien, des machines qui font des trucs c'est mieux.

## 1. DHCP

![Technology](https://media.giphy.com/media/CTX0ivSQbI78A/giphy.gif)

Petite **install d'un serveur DHCP** dans cette partie. Par soucis d'économie de ressources, on recycle une des machines précédentes : `node2.lan1.tp1` devient `dhcp.lan1.tp1`.

**Pour rappel**, un serveur DHCP, on en trouve un dans la plupart des LANs auxquels vous vous êtes connectés. Si quand tu te connectes dans un réseau, tu n'es pas **obligé** de saisir une IP statique à la mano, et que t'as un accès internet wala, alors il y a **forcément** un serveur DHCP dans le réseau qui t'a proposé une IP disponible.

> Le serveur DHCP a aussi pour rôle de donner, en plus d'une IP disponible, deux informations primordiales pour l'accès internet : l'adresse IP de la passerelle du réseau, et l'adresse d'un serveur DNS joignable depuis ce réseau.

**Dans notre TP, son rôle sera de proposer une IP libre à toute machine qui le demande dans le LAN1.**

> Vous pouvez vous référer à [ce lien](https://www.server-world.info/en/note?os=Rocky_Linux_8&p=dhcp&f=1) ou n'importe quel autre truc sur internet (je sais c'est du Rocky 8, m'enfin, la conf de ce serveur DHCP ça bouge pas trop).
---

Pour ce qui est de la configuration du serveur DHCP, quelques précisions :

- vous ferez en sorte qu'il propose des adresses IPs entre `10.1.1.100` et `10.1.1.200`
- vous utiliserez aussi une option DHCP pour indiquer aux clients que la passerelle du réseau est `10.1.1.254` : le routeur
- vous utiliserez aussi une option DHCP pour indiquer aux clients qu'un serveur DNS joignable depuis le réseau c'est `1.1.1.1`

---

☀️ **Sur `dhcp.lan1.tp1`**

- n'oubliez pas de renommer la machine (`node2.lan1.tp1` devient `dhcp.lan1.tp1`)
- changez son adresse IP en `10.1.1.253`
- setup du serveur DHCP
  - commande d'installation du paquet
  - fichier de conf
  - service actif

```bash
[user1@dhcp ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s3 | grep IP
IPADDR=10.1.1.253
```

```bash
[user1@dhcp ~]$ sudo dnf install dhcp-server -y
```

*Fichier de configuration DHCP*

```bash
[user1@dhcp ~]$ sudo cat /etc/dhcp/dhcpd.conf
[sudo] password for user1:

# default lease time
default-lease-time 600;
# max lease time
max-lease-time 7200;
# this DHCP server to be declared valid
authoritative;

subnet 10.1.1.0 netmask 255.255.255.0 {
    # Ip between 10.1.1.100 and 10.1.1.200
    range 10.1.1.100 10.1.1.200;

    # gateway address
    option routers 10.1.1.254;

    # net mask of the network
    option subnet-mask 255.255.255.0;

    # DNS server to use
   option domain-name-servers 1.1.1.1;
}
```

*Activation du service au démarrage et autorisation du service dhcpd dans le firewall*

```bash
[user1@dhcp ~]$ sudo systemctl start dhcpd
[user1@dhcp ~]$ sudo systemctl enable dhcpd
Created symlink /etc/systemd/system/multi-user.target.wants/dhcpd.service → /usr/lib/systemd/system/dhcpd.service.

[user1@dhcp ~]$ sudo systemctl status dhcpd | head
● dhcpd.service - DHCPv4 Server Daemon
     Loaded: loaded (/usr/lib/systemd/system/dhcpd.service; enabled; preset: disabled)
     Active: active (running) since Tue 2023-10-24 11:22:36 CEST; 8min ago
       Docs: man:dhcpd(8)
             man:dhcpd.conf(5)
   Main PID: 1312 (dhcpd)
     Status: "Dispatching packets..."
      Tasks: 1 (limit: 4611)
     Memory: 4.6M
        CPU: 7ms

[user1@dhcp ~]$ sudo firewall-cmd --zone=public --add-service=dhcp --permanent
success
[user1@dhcp ~]$ sudo firewall-cmd --reload
success
```

☀️ **Sur `node1.lan1.tp1`**

- demandez une IP au serveur DHCP

![Give me it](https://media.giphy.com/media/XwtIKC8Kp8lO0/giphy.gif)

*Tout d'abord il faut edit le fichier de conf de l'interface pour la passer en dhcp le serveur dhcp nous en donnera une automatiquement*

```bash
[user1@node1 ~]$ sudo cat /etc/sysconfig/network-scripts/ifcfg-enp0s3
[sudo] password for user1:
NAME=enp0s3
DEVICE=enp0s3

BOOTPROTO=dhcp
ONBOOT=yes
```

*Si on en veut absolument une autre*

![use the force](https://media.giphy.com/media/wZp0Vh3LjSeFopua87/giphy.gif)

- prouvez que vous avez bien récupéré une IP *via* le DHCP

```bash
[user1@node1 ~]$ sudo dhclient -v enp0s3
[sudo] password for user1:
Internet Systems Consortium DHCP Client 4.4.2b1
Copyright 2004-2019 Internet Systems Consortium.
All rights reserved.
For info, please visit https://www.isc.org/software/dhcp/

Listening on LPF/enp0s3/08:00:27:45:46:3f
Sending on   LPF/enp0s3/08:00:27:45:46:3f
Sending on   Socket/fallback
DHCPREQUEST for 10.1.1.101 on enp0s3 to 255.255.255.255 port 67 (xid=0xa11f766b)
DHCPACK of 10.1.1.101 from 10.1.1.253 (xid=0xa11f766b)
bound to 10.1.1.101 -- renewal in 294 seconds.
```

- prouvez que vous avez bien récupéré l'IP de la passerelle

```bash
[user1@node1 ~]$ ip r s | grep 10.1.1.101
default via 10.1.1.254 dev enp0s3 proto dhcp src 10.1.1.101 metric 100
```

- prouvez que vous pouvez `ping node1.lan2.tp1`

```bash
[user1@node1 ~]$ ping node1.lan2.tp1 -c 4
PING node1.lan2.tp1 (10.1.2.11) 56(84) bytes of data.
64 bytes from node1.lan2.tp1 (10.1.2.11): icmp_seq=1 ttl=63 time=1.62 ms
64 bytes from node1.lan2.tp1 (10.1.2.11): icmp_seq=2 ttl=63 time=2.39 ms
64 bytes from node1.lan2.tp1 (10.1.2.11): icmp_seq=3 ttl=63 time=2.01 ms
64 bytes from node1.lan2.tp1 (10.1.2.11): icmp_seq=4 ttl=63 time=2.79 ms

--- node1.lan2.tp1 ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3006ms
rtt min/avg/max/mdev = 1.615/2.201/2.791/0.437 ms
```

## 2. Web web web

![woooooo](https://media.giphy.com/media/k1OosBWew4EKs/giphy.gif)

---

☀️ **Sur `web.lan2.tp1`**

- n'oubliez pas de renommer la machine (`node2.lan2.tp1` devient `web.lan2.tp1`)
- setup du service Web
  - installation de NGINX
  - gestion de la racine web `/var/www/site_nul/`
  - configuration NGINX
  - service actif
  - ouverture du port firewall
- prouvez qu'il y a un programme NGINX qui tourne derrière le port 80 de la machine (commande `ss`)
- prouvez que le firewall est bien configuré

```bash
[user1@node2 ~]$ echo web.lan2.tp1 | sudo tee /etc/hostname
[sudo] password for user1:
web.lan2.tp1

[user1@web ~]$ sudo dnf install nginx -y

[user1@web ~]$ sudo mkdir -p /var/www/site_nul

[user1@web ~]$ sudo nano /var/www/site_nul/index.html
[user1@web ~]$ sudo cat /var/www/site_nul/index.html
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Un site avec un magnifique design</title>
  <link rel="stylesheet" href="style.css">
  <script src="script.js"></script>
</head>
<body>
  <h1>Bojowwwwwww</h1>
</body>
</html>
```

*Configuration de nginx*

```bash
[user1@web ~]$ sudo nano /etc/nginx/conf.d/tp1.conf
[user1@web ~]$ sudo cat /etc/nginx/conf.d/tp1.conf
server {
  listen 80;
  server_name site_nul.tp1;

  root /var/www/site_nul;
}
```

*Démarrage du serveur nginx tout de suite et au démarrage de la machine*

```bash
[user1@web ~]$ sudo systemctl start nginx
[user1@web ~]$ sudo systemctl enable nginx
[user1@web ~]$ sudo systemctl status nginx | grep Active:
     Active: active (running) since Sun 2023-10-22 14:48:37 CEST; 3min 43s ago
```

*Ouverture du port 80 dans le firewall*

```bash
[user1@web ~]$ sudo firewall-cmd --add-port=80/tcp --permanent
success
[user1@web ~]$ sudo firewall-cmd --reload
success
[user1@web ~]$ sudo firewall-cmd --list-all | grep -m 1 ports
  ports: 80/tcp
```

*Preuve que le service nginx tourne derrière le port 80*

```bash
[user1@web ~]$ sudo ss -alnpt | grep 80
LISTEN 0      511          0.0.0.0:80        0.0.0.0:*    users:(("nginx",pid=1588,fd=6),("nginx",pid=1587,fd=6))
LISTEN 0      511             [::]:80           [::]:*    users:(("nginx",pid=1588,fd=7),("nginx",pid=1587,fd=7))
```

☀️ **Sur `node1.lan1.tp1`**

- éditez le fichier `hosts` pour que `site_nul.tp1` pointe vers l'IP de `web.lan2.tp1`
- visitez le site nul avec une commande `curl` et en utilisant le nom `site_nul.tp1`

*Modification du fichier hosts*

```bash
[user1@node1 ~]$ sudo nano /etc/hosts
[sudo] password for user1:
[user1@node1 ~]$ cat /etc/hosts | grep 10.1.2.12
10.1.2.12   site_nul.tp1
```

*Curl site_nul.tp1*

```bash
[user1@node1 ~]$ curl site_nul.tp1
<!doctype html>
<html lang="fr">
<head>
  <meta charset="utf-8">
  <title>Un site avec un magnifique design</title>
  <link rel="stylesheet" href="style.css">
  <script src="script.js"></script>
</head>
<body>
  <h1>Bojowwwwwww</h1>
</body>
</html>
```

![Cr7 siuuuuuuuuuuuuuuuuuuu](https://media.giphy.com/media/R312C3MEVg4SCYAber/giphy-downsized-large.gif)