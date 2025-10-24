# Purity Discord Bot

Purity est un bot Discord modulaire et complet, conçu pour gérer, modérer et améliorer l’expérience de ton serveur. Il propose de nombreuses commandes et options de configuration pour les administrateurs et les utilisateurs.

## Fonctionnalités principales
- **Modération** : Ban, kick, mute, warn, jail, ajout/suppression de rôles, etc.
- **Antiraid & Sécurité** : Anti-bot, anti-spam de salons, protection ghost ping, vérification captcha, autorole, gestion blacklist.
- **Sauvegarde & Restauration** : Création, liste et chargement de sauvegardes du serveur.
- **Giveaways** : Lancement et reroll de giveaways.
- **Informations** : Statistiques serveur, infos membres, suivi des invitations, etc.
- **Logs** : Logs automatiques et personnalisés des événements du serveur.
- **Utilitaires** : Embeds, gestion des emojis, liens d’invitation, snipe des messages supprimés, etc.
- **Gestion des salons vocaux** : Lock/unlock, déplacement, mute/deaf, AFK, salons vocaux temporaires.
- **Messages personnalisés** : Messages de bienvenue, système de tickets, soutien, etc.

## Structure du projet
- `commands/` : Modules de commandes par catégorie
- `events/` : Gestionnaires d’événements Discord
- `functions/` : Fonctions utilitaires principales
- `models/` : Modèles de données et configuration
- `views/` : UI Discord personnalisée
- `configs/` : Fichiers de configuration
- `lang/` : Fichiers de langue (français, anglais)
- `core/` : Logique centrale du bot
- `loaders/` : Chargeurs de commandes et d’événements

## Démarrage rapide
1. **Clone le repo**
   ```powershell
   git clone https://github.com/Celentroft/purity.git
   ```
2. **Installe les dépendances**
   ```powershell
   pip install -r requirements.txt
   ```
3. **Configure le bot**
   - Modifie `config.json` avec le token de ton bot et les paramètres du serveur.
4. **Lance le bot**
   ```powershell
   python main.py
   ```

## Configuration
- Les paramètres principaux sont dans `config.json`.
- Les fichiers de langue sont dans `lang/`.
- Les modules de commandes et d’événements sont activables/désactivables dans leurs dossiers respectifs.

## Contribuer
N’hésite pas à ouvrir des issues ou des pull requests pour améliorer le bot ou ajouter des fonctionnalités.

## Licence
Ce projet est sous licence MIT.

---
Made by Celentroft et contributeurs.
