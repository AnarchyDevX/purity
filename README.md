# 💜 Purity Official Repository 💜

Purity est un bot Discord complet et modulaire, conçu pour faciliter la gestion, la modération et la sécurité de votre serveur.  
Développé en [Python](https://python.org/) avec [discord.py](https://discordpy.readthedocs.io/en/stable/).

---

## 📜 Sommaire 📜

- 🧩 Options et fonctionnalités
- 🧱 Arborescence du dossier
- ⚙️ Installation et configuration
- 📜 Licence & protection du code
- ✨ Soutien du projet
- 🔎 Contact et liens

---

## 🧩 Options et fonctionnalités 🧩

- Antiraid
- Modération
- Logs
- Gestion des salons vocaux
- Système de tickets
- Création d’embeds
- Commandes fun
- Configuration avancée
- Et bien plus encore...

---

## 🧱 Arborescence du dossier 🧱

```
Purity/
├── backups/                  # configuration et sauvergardes des backups
├── commands/                 # slash commands (13 dossiers)
│   ├── antiraid/
│   ├── client/
│   ├── gestion/
│   └── .../                  # autres dossier de commandes
├── configs/                  # configuration des serveurs (serverId.json)
├── core/
│   ├── _colors.py            # class de couleur dans du texte dans le shell
│   └── embedBuilder.py       # rework et optimisation de l'appel des embeds
├── events/                   # events Discord (9 dossiers)
│   ├── antiraid/
│   ├── configuration/
│   ├── logs/
│   └── .../                  # autres dossier d'events
├── functions/
│   └── functions.py          # fonctions réutilisables pour le bot
├── langs/                    # dossier des langues du bot (non achevé)
│   ├── en.json
│   └── fr.json
├── loaders/                  # loaders des commandes et events
│   ├── commandsLoader.py
│   └── eventsLoader.py
├── logs/                     # logs erreur, event, commands (sera retiré)
│   └── logs.log
├── models/                   
│   └── configuration.py      # modèle de configuration des serveurs 
├── views/                    # views discord (buttons, modal, select...)(22 dossiers)
│   ├── antiraidView/
│   ├── autoRole/
│   ├── embedView/
│   └── .../                  # autres dossier de views
├── arial.ttf                 # police d'écriture pour la génération des captcha
├── config.json               # configuration de base du bot
├── main.py                   # fichier de lancement
└── requirements.txt          # modules requis
```

---

## ⚙️ Installation et configuration ⚙️

### Prérequis

1. Python 3.11+
2. Un bot discord configuré
3. Windows 10/11 ou Linux (seulement les couleurs ne fonctionnerons pas sur linux)
4. Savoir lire 👀

### Installaton
1. Cloner le repository
```bash
git clone https://github.com/Celentroft/purity.git
cd purity
```

2. Installer les modules nécessaires
```bash
pip install -r requirements.txt
```

### Configuration

1. Configuration du fichier `config.json`
```json
{
    "token": "token",           -> token du bot
    "color": "color",           -> couleur des embeds (HEX color code)
    "buyer": [
        940965110443302974,     -> Id Discord des owner bot
        940483098403840284
    ], 
    "blacklist": [],            -> ne pas modifier
    "guildjoin": true,          -> ne pas modifier
    "lang": "fr.json",          -> ne pas modifier
    "apichannel": null          -> Id du salon d'actualisation du ping du bot
}
```

2. Créer le bot Discord
- Allez sur [Discord Developer Portal](https://discord.com/developers/applications)
- Créez une nouvelle application
- Dans "Bot", activez tous les **Privileged Gateway Intents**
- Copiez le token
- Dans "OAuth2 > URL Generator" :
  - Scopes: `bot`, `applications.commands`
  - Permissions: Administrator (ou personnalisées)
  - Utilisez l'URL générée pour inviter le bot

---

## 📜 Licence & protection du code 📜

**Copyright © [2025] [Celentroft]. Tous droits réservés.**

Le code source de *Purity* (le « Projet ») est la propriété exclusive de son auteur. Toute reproduction, redistribution, modification publique, re-packaging ou utilisation commerciale non autorisée du code est **strictement interdite**.

### Ce que cela signifie
- Vous **n’êtes pas autorisé** à forker, republier, distribuer ou vendre ce code sans une autorisation écrite explicite.
- Si vous souhaitez utiliser le projet (ou des parties), contactez l'auteur pour obtenir une **licence** ou une permission explicite.
- Les versions compilées / obfusquées livrées sous forme de binaires restent la propriété de l'auteur et ne donnent pas de droit de redistribution.

---

## ✨ Soutien du projet ✨

Si vous appréciez **Purity** et souhaitez soutenir son développement, vous pouvez :  

- ⭐ **Star** ce projet sur GitHub pour nous encourager et montrer votre soutien.  
- 🌟 **Partager le projet** avec d'autres communautés Discord ou développeurs.  
- 🐛 **Signaler des bugs** ou proposer des améliorations via GitHub pour aider le projet à s'améliorer.  

Chaque geste, petit ou grand, contribue à maintenir et améliorer Purity !

---

## 🔎 Contact et liens 🔎

- 💻 **Discord du développeur** : scarlxrd_zk (ID : 940965110443302974)  
- 🟣 **Serveur Discord officiel** : [Deepshell](https://discord.gg/deepshell)  
- ✈️ **Telegram** : [https://t.me/scarlxrd_1337](https://t.me/scarlxrd_1337)  
- ⭐ **GitHub** : [Purity Repository](https://github.com/Celentroft/purity)
