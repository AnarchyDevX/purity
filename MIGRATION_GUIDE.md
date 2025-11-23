# Guide de Migration des Configurations

## 🎯 Objectif

Ce script met à jour automatiquement toutes les configurations JSON de vos serveurs pour inclure les nouveaux champs ajoutés au bot.

## ✨ Fonctionnalités

- ✅ Ajoute automatiquement les champs manquants
- ✅ Préserve toutes les données existantes
- ✅ Crée des backups automatiques
- ✅ Affiche un rapport détaillé
- ✅ Gère tous les fichiers du dossier `configs/`

## 🚀 Utilisation

### Sur votre machine locale

```bash
python migrate_configs.py
```

### Sur le VPS

```bash
cd /opt/purity
python3 migrate_configs.py
```

## 📋 Nouveaux champs ajoutés

Le script ajoute automatiquement ces champs s'ils manquent :

### Tickets
- `tickets.adduser_role` - Rôle ajouté automatiquement aux tickets
- `tickets.preticket_category` - Catégorie pour les pré-tickets

### Captcha
- `captcha.active` - Activation du système de captcha
- `captcha.channel_id` - Canal du captcha
- `captcha.message_id` - Message du captcha
- `captcha.role_id` - Rôle donné après vérification

### Autres
- Tous les champs de la structure complète si manquants

## 📁 Structure des fichiers

```
purity/
├── configs/
│   ├── 1338074160261369867.json  # Vos configs
│   ├── 1434314086325420043.json
│   └── ...
├── migration_backups/             # Créé automatiquement
│   ├── 20251123_140530_1338074160261369867.json
│   └── ...
└── migrate_configs.py             # Le script
```

## 🔄 Processus de migration

1. **Backup** : Copie de chaque config avant modification
2. **Analyse** : Détection des champs manquants
3. **Fusion** : Ajout des champs manquants avec valeurs par défaut
4. **Sauvegarde** : Écriture de la config mise à jour
5. **Rapport** : Affichage des modifications

## 📊 Exemple de sortie

```
============================================================
🚀 MIGRATION DES CONFIGURATIONS
============================================================
📁 3 fichier(s) de configuration trouvé(s)

============================================================
Migration: ./configs/1338074160261369867.json
============================================================
✅ Backup créé: ./migration_backups/20251123_140530_1338074160261369867.json
✅ Configuration migrée avec succès!
📝 Champs ajoutés (2):
   - tickets.adduser_role
   - tickets.preticket_category

============================================================
📊 RÉSUMÉ DE LA MIGRATION
============================================================
✅ Fichiers migrés: 2
✔️  Fichiers déjà à jour: 1
❌ Erreurs: 0
📁 Total: 3

============================================================
✅ Migration terminée avec succès!
============================================================

💡 Les backups sont dans le dossier './migration_backups'
💡 En cas de problème, vous pouvez restaurer les backups manuellement
```

## 🛡️ Sécurité

- ✅ Backups automatiques avant toute modification
- ✅ Aucune suppression de données existantes
- ✅ Fusion intelligente des configurations
- ✅ Gestion des erreurs avec rapports détaillés

## 🔧 Restauration d'un backup

En cas de problème, restaurez manuellement :

```bash
# Copier le backup vers configs/
cp migration_backups/20251123_140530_GUILD_ID.json configs/GUILD_ID.json

# Ou sur VPS
sudo cp migration_backups/20251123_140530_GUILD_ID.json configs/GUILD_ID.json
```

## ⚠️ Important

- Arrêtez le bot avant de lancer la migration (recommandé mais pas obligatoire)
- Les backups sont horodatés et conservés indéfiniment
- Le script peut être relancé sans danger (idempotent)

## 🎓 Commandes complètes

### Local
```bash
# Lancer la migration
python migrate_configs.py

# Si besoin de restaurer
cp migration_backups/LATEST_BACKUP.json configs/GUILD_ID.json
```

### VPS
```bash
# Se connecter au VPS
ssh utilisateur@votre-vps

# Aller dans le dossier
cd /opt/purity

# Arrêter le bot (recommandé)
pm2 stop purity-bot

# Lancer la migration
python3 migrate_configs.py

# Redémarrer le bot
pm2 start purity-bot
pm2 save
```

## 📞 Support

En cas de problème, les logs détaillés vous indiqueront :
- Quel fichier pose problème
- Quelle erreur s'est produite
- Où se trouve le backup

Tous vos fichiers sont sauvegardés avant modification ! 🛡️

