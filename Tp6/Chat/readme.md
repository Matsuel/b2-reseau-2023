# Chat

## Lancement du serveur:

```py
python ./Tp6/Chat/server.py -p port_pour_le_serveur -a ladresse_pour_le_serveur
```

*Possibilité d'utiliser des arguments afin de lancer le serveur sur une ip voulue avec les arguments -p ou --port et -a ou --addr*

## Lancement d'un client

```py
python ./Tp6/Chat/client.py -p le_port_du_serveur -a ladresse_du_serveur
```

*Possibilité d'utiliser des arguments afin de lancer le serveur sur une ip voulue avec les arguments -p ou --port et -a ou --addr*

*Lors du démarrage du client on vous demandera un nom d'utilisateur*

## Commandes disponibles dans le chat

-> Tout d'abord l'envoie de message sou forme de string est disponible avec un prompt d'affichage "Message envoyé: <message>"

-> Possibilité d'envoyer des images avec la commande

```bash
/image +le-nom-de-l'image
```

*L'image doit être dans le dossier img disponible ici [Img](./img/) afin de pouvoir être lue par le client*