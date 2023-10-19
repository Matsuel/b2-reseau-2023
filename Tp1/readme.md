# TP1 : Maîtrise réseau du poste

Pour ce TP, on va utiliser **uniquement votre poste** (pas de VM, rien, quedal, quetchi).

Le but du TP : se remettre dans le bain tranquillement en manipulant pas mal de concepts qu'on a vu l'an dernier.

C'est un premier TP *chill*, qui vous(ré)apprend à maîtriser votre poste en ce qui concerne le réseau. Faites le seul ou avec votre mate préféré bien sûr, mais jouez le jeu, faites vos propres recherches.

La "difficulté" va crescendo au fil du TP, mais la solution tombe très vite avec une ptite recherche Google si vos connaissances de l'an dernier deviennent floues.

- [TP1 : Maîtrise réseau du poste](#tp1--maîtrise-réseau-du-poste)
- [I. Basics](#i-basics)
- [II. Go further](#ii-go-further)
- [III. Le requin](#iii-le-requin)

# I. Basics

> Tout est à faire en ligne de commande, sauf si précision contraire.

☀️ **Carte réseau WiFi**

Déterminer...

- l'adresse MAC de votre carte WiFi
- l'adresse IP de votre carte WiFi


```bash
C:\Users\matsu>ipconfig /all

Carte réseau sans fil Wi-Fi :
    Adresse physique . . . . . . . . . . . : DC-21-5C-96-22-51
    Adresse IPv4. . . . . . . . . . . . . .: 10.33.79.156
```

- le masque de sous-réseau du réseau LAN auquel vous êtes connectés en WiFi
  - en notation CIDR, par exemple `/16`
  ```bash
    C:\Users\matsu>ipconfig /all
        Masque de sous-réseau. . . . . . . . . : 255.255.240.0/20
  ```
  - ET en notation décimale, par exemple `255.255.0.0`

  ```bash
    C:\Users\matsu>ipconfig /all
        Masque de sous-réseau. . . . . . . . . : 255.255.240.0
  ```

---

☀️ **Déso pas déso**

Pas besoin d'un terminal là, juste une feuille, ou votre tête, ou un tool qui calcule tout hihi. Déterminer...

- l'adresse de réseau du LAN auquel vous êtes connectés en WiFi
    	```bash
            10.33.64.0
        ```
- l'adresse de broadcast
        ```bash
            10.33.79.255
        ```
- le nombre d'adresses IP disponibles dans ce réseau
        ```bash
            4094 sans adresse de broadcast et de routeur
            4096 au total
        ```

---

☀️ **Hostname**

- déterminer le hostname de votre PC

```bash
    C:\Users\matsu>hostname
    Matsuel
```

---

☀️ **Passerelle du réseau**

Déterminer...

- l'adresse IP de la passerelle du réseau
- l'adresse MAC de la passerelle du réseau

```bash
C:\Users\matsu>ipconfig /all

Carte réseau sans fil Wi-Fi :
Passerelle par défaut. . . . . . . . . : 10.33.79.254

C:\Users\matsu>arp -a

Interface : 10.33.79.156 --- 0x14
Adresse Internet      Adresse physique      Type
10.33.79.254          7c-5a-1c-d3-d8-76     dynamique
```

---

☀️ **Serveur DHCP et DNS**

Déterminer...

- l'adresse IP du serveur DHCP qui vous a filé une IP
- l'adresse IP du serveur DNS que vous utilisez quand vous allez sur internet

```bash
C:\Users\matsu>ipconfig /all

Carte réseau sans fil Wi-Fi :
Serveur DHCP . . . . . . . . . . . . . : 10.33.79.254
Serveurs DNS. . .  . . . . . . . . . . : 8.8.8.8
                                       1.1.1.1
```
---

☀️ **Table de routage**

Déterminer...

- dans votre table de routage, laquelle est la route par défaut

```bash
C:\Users\matsu>route print 0.0.0.0

Itinéraires actifs :
Destination réseau    Masque réseau  Adr. passerelle   Adr. interface Métrique
          0.0.0.0          0.0.0.0     10.33.79.254     10.33.79.156     30
```

---

![Not sure](./img/notsure.png)

# II. Go further

> Toujours tout en ligne de commande.

---

☀️ **Hosts ?**

- faites en sorte que pour votre PC, le nom `b2.hello.vous` corresponde à l'IP `1.1.1.1`
- prouvez avec un `ping b2.hello.vous` que ça ping bien `1.1.1.1`

> Vous pouvez éditer en GUI, et juste me montrer le contenu du fichier depuis le terminal pour le compte-rendu.

```bash
C:\Users\matsu>ping b2.hello.vous

Envoi d’une requête 'ping' sur b2.hello.vous [1.1.1.1] avec 32 octets de données :
Réponse de 1.1.1.1 : octets=32 temps=11 ms TTL=57
Réponse de 1.1.1.1 : octets=32 temps=11 ms TTL=57
Réponse de 1.1.1.1 : octets=32 temps=10 ms TTL=57
Réponse de 1.1.1.1 : octets=32 temps=11 ms TTL=57

Statistiques Ping pour 1.1.1.1:
    Paquets : envoyés = 4, reçus = 4, perdus = 0 (perte 0%),
Durée approximative des boucles en millisecondes :
    Minimum = 10ms, Maximum = 11ms, Moyenne = 10ms
```

```bash
C:\Windows\System32\drivers\etc>type hosts | findstr "1.1.1.1"
        1.1.1.1         b2.hello.vous
```

---

☀️ **Go mater une vidéo youtube et déterminer, pendant qu'elle tourne...**

- l'adresse IP du serveur auquel vous êtes connectés pour regarder la vidéo
- le port du serveur auquel vous êtes connectés
- le port que votre PC a ouvert en local pour se connecter au port du serveur distant


```bash
C:\Users\matsu>netstat -n

Connexions actives

  Proto  Adresse locale         Adresse distante       État
  TCP    10.33.79.156:51552     172.217.20.163:443     ESTABLISHED
  TCP    10.33.79.156:51535     172.65.251.78:443      ESTABLISHED

  Adresses Ips Yotube: 172.217.20.163 172.65.251.78 
  Port du serveur 443
  Ports de mon pc 51552 et 51535

```

---

☀️ **Requêtes DNS**

Déterminer...

- à quelle adresse IP correspond le nom de domaine `www.ynov.com`

> Ca s'appelle faire un "lookup DNS".

```bash
C:\Users\matsu>nslookup www.ynov.com
Serveur :   dns.google
Address:  8.8.8.8

Réponse ne faisant pas autorité :
Nom :    www.ynov.com
Addresses:  2606:4700:20::681a:ae9
          2606:4700:20::ac43:4ae2
          2606:4700:20::681a:be9
          104.26.10.233
          172.67.74.226
          104.26.11.233
```

- à quel nom de domaine correspond l'IP `174.43.238.89`

> Ca s'appelle faire un "reverse lookup DNS".

```bash
C:\Users\matsu>nslookup 174.43.238.89
Serveur :   dns.google
Address:  8.8.8.8

Nom :    89.sub-174-43-238.myvzw.com
Address:  174.43.238.89
```

---

☀️ **Hop hop hop**

Déterminer...

- par combien de machines vos paquets passent quand vous essayez de joindre `www.ynov.com`

```bash
C:\Users\matsu>tracert -4 www.ynov.com

Détermination de l’itinéraire vers www.ynov.com [104.26.11.233]
avec un maximum de 30 sauts :

  1     2 ms     1 ms     1 ms  10.33.79.254
  2     4 ms     2 ms     1 ms  145.117.7.195.rev.sfr.net [195.7.117.145]
  3     2 ms     2 ms     3 ms  237.195.79.86.rev.sfr.net [86.79.195.237]
  4     4 ms     3 ms     3 ms  196.224.65.86.rev.sfr.net [86.65.224.196]
  5    12 ms    11 ms    11 ms  12.148.6.194.rev.sfr.net [194.6.148.12]
  6    11 ms    10 ms    10 ms  12.148.6.194.rev.sfr.net [194.6.148.12]
  7    11 ms    11 ms    11 ms  141.101.67.48
  8    11 ms    11 ms    10 ms  172.71.124.4
  9    11 ms    10 ms    11 ms  104.26.11.233

Itinéraire déterminé.

9 machines pour joindre ynov.com
```

---

☀️ **IP publique**

Déterminer...

- l'adresse IP publique de la passerelle du réseau (le routeur d'YNOV donc si vous êtes dans les locaux d'YNOV quand vous faites le TP)

```bash
C:\Users\matsu>curl ifconfig.me
195.7.117.146
```

---

☀️ **Scan réseau**

Déterminer...

- combien il y a de machines dans le LAN auquel vous êtes connectés

```bash
213ms matsu ❯ nmap -sn 10.33.64.0/20
Starting Nmap 7.94 ( https://nmap.org ) at 2023-10-19 11:38 Paris, Madrid (heure dÆÚtÚ)
Nmap scan report for 10.33.64.0
Host is up (0.0020s latency).
Nmap done: 4096 IP addresses (894 hosts up) scanned in 169.64 seconds
```

> Allez-y mollo, on va vite flood le réseau sinon. :)

![Stop it](./img/stop.png)

# III. Le requin

Faites chauffer Wireshark. Pour chaque point, je veux que vous me livrez une capture Wireshark, format `.pcap` donc.

Faites *clean* 🧹, vous êtes des grands now :

- livrez moi des captures réseau avec uniquement ce que je demande et pas 40000 autres paquets autour
  - vous pouvez sélectionner seulement certains paquets quand vous enregistrez la capture dans Wireshark
- stockez les fichiers `.pcap` dans le dépôt git et côté rendu Markdown, vous me faites un lien vers le fichier, c'est cette syntaxe :

```markdown
[Lien vers capture ARP](./captures/arp.pcap)
```

---

☀️ **Capture ARP**

- 📁 fichier `arp.pcap`
- capturez un échange ARP entre votre PC et la passerelle du réseau

[Capture ARP Wiresharkp](./src/arp.pcap)

- Filtrage par nom de protocol arp.

---

☀️ **Capture DNS**

- 📁 fichier `dns.pcap`
- capturez une requête DNS vers le domaine de votre choix et la réponse
- vous effectuerez la requête DNS en ligne de commande

```bash
nslookup instagram.com
```

[Lien capture DNS](./src/dns.pcap)

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

---

☀️ **Capture TCP**

- 📁 fichier `tcp.pcap`
- effectuez une connexion qui sollicite le protocole TCP
- je veux voir dans la capture :
  - un 3-way handshake
  - un peu de trafic
  - la fin de la connexion TCP

  [Lien capture TCP](./src/tcp.pcap)

  ```bash
  Filtre: (tcp) && (ip.addr=162.159.61.3)
  ```

> Si vous utilisez un filtre Wireshark pour mieux voir ce trafic, précisez-le moi dans le compte-rendu.

---

![Packet sniffer](img/wireshark.jpg)

> *Je sais que je vous l'ai déjà servi l'an dernier lui, mais j'aime trop ce meme hihi 🐈*