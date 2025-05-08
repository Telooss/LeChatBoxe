# 🔐 Secure Chat App (Client-Serveur)

Une application de chat sécurisée en ligne de commande, développée en Python.  
Elle utilise un serveur TCP multi-client, une base de données SQLite pour la gestion des utilisateurs et messages, et intègre plusieurs couches de chiffrement (Fernet + chiffrement personnalisé).

## 🧩 Fonctionnalités

### ✅ Côté utilisateur :
- Authentification (inscription/connexion)
- Communication en temps réel avec plusieurs utilisateurs
- Commandes intégrées :
  - `/users` — Affiche les utilisateurs connectés
  - `/help` — Liste les commandes disponibles
  - `exit` — Quitte le chat

### 🔐 Côté sécurité :
- Chiffrement **Fernet** des communications réseau
- Chiffrement **personnalisé** (XOR avec clé dérivée) des messages stockés dans la base
- Hachage des mots de passe avec **bcrypt**
- Mot de passe d’accès au serveur généré dynamiquement à chaque lancement

### 👑 Côté administrateur :
- `/kick <username>` — Expulse un utilisateur
- `/regen` — Régénère le mot de passe d’accès au serveur
- `/stop` — Éteint le serveur proprement

## 🗃️ Structure du projet

```

socket/
├── client/
│   ├── client.py
│   └── receiver.py
├── config/
│   └── config.py
├── database/
│   └── chat\_db.py
├── security/
│   └── crypt.py
├── server/
│   ├── server.py
│   ├── handlers.py
│   ├── commands.py
│   └── utils.py
└── chat.db

````

## ⚙️ Prérequis

- Python 3.10+ recommandé
- Installer les dépendances :

```bash
pip install -r requirements.txt
````

Fichier `requirements.txt` :

```
bcrypt
cryptography
```

## 🚀 Lancement

### Serveur :

Depuis le dossier racine du projet :

```bash
python -m server.server
```

### Client :

Dans un autre terminal, toujours depuis la racine :

```bash
python -m client.client
```

Le mot de passe du serveur est affiché au démarrage du serveur.

## 🛡️ Sécurité

* Les mots de passe sont hachés avec **bcrypt**.
* Les messages sont chiffrés avec :

  * **Fernet** en transit
  * **Chiffrement maison** en base (clé dérivée + XOR)
* Impossible de déchiffrer les messages sans le programme `security/crypt.py`.

## 🧠 À venir (améliorations possibles)

* Ajout de clés asymétriques par utilisateur
* Historique côté client
* Authentification 2FA
* Interface graphique (Tkinter ou Web)

## 👨‍💻 Auteur

Projet développé par **Telos** – étudiant en cybersécurité 🛡️

