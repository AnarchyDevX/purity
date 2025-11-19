# 🎫 Système de Tickets Complet - Documentation

## 📋 Vue d'ensemble

Ce système de tickets est complet, robuste et prêt pour la production. Il inclut :
- ✅ Gestion automatique du rôle staff
- ✅ Système de transcript robuste avec fallbacks
- ✅ Vérification automatique des permissions
- ✅ Gestion d'erreurs complète

## 🚀 Installation

Aucune dépendance supplémentaire requise. Le système utilise uniquement :
- `discord.py` (version 2.x)
- `aiohttp` (déjà dans requirements.txt)
- Bibliothèques Python standard

## ⚙️ Configuration

### 1. Définir le rôle staff

Utilisez la commande `/setstaffrole <role>` pour définir le rôle qui aura automatiquement accès à tous les tickets.

**Exemple :**
```
/setstaffrole @Modérateur
```

**Permissions requises :** Niveau 2 (owner ou buyer)

### 2. Configurer les catégories de tickets

Utilisez `/ticket-categories-config` pour définir les catégories :
- **Nouveaux tickets** : Où les nouveaux tickets sont créés
- **Pris en charge** : Tickets pris en charge par le staff
- **En pause** : Tickets mis en pause
- **Fermés** : Tickets fermés (seront supprimés après transcript)

### 3. Configurer le canal de logs

Utilisez `/tickets-transcripts-config` pour définir où les transcripts seront envoyés.

## 🎯 Fonctionnalités

### ✅ Rôle Staff Automatique

- Le rôle staff défini avec `/setstaffrole` a **automatiquement** accès à tous les tickets créés
- Permissions complètes : voir, envoyer, lire l'historique, joindre des fichiers
- Aucune configuration supplémentaire nécessaire

### ✅ Système de Transcript Robuste

Le système de transcript a **3 niveaux de fallback** :

1. **Format TXT** (recommandé) - Format texte simple et lisible
2. **Format HTML** - Si le TXT échoue, fallback vers HTML
3. **Format minimal** - En cas d'erreur critique, transcript minimal avec message d'erreur

**Fonctionnalités :**
- Capture tous les messages, embeds, pièces jointes
- Gestion d'erreurs par message (continue même si un message échoue)
- Compteur d'erreurs dans le transcript
- Fallback automatique si une méthode échoue

### ✅ Vérification Automatique des Permissions

Un système de vérification automatique s'exécute **toutes les 5 minutes** pour :
- Vérifier que tous les tickets ont les bonnes permissions pour le rôle staff
- Corriger automatiquement les permissions manquantes
- Logger les corrections dans la console

### ✅ Gestion d'Erreurs Complète

- Toutes les erreurs sont catch et log
- Le système continue de fonctionner même en cas d'erreur partielle
- Messages d'erreur clairs pour l'utilisateur
- Logs détaillés dans la console pour le debugging

## 📝 Structure des Fichiers

```
commands/configuration/tickets-staff-config.py    # Commande /setstaffrole
events/tickets/permissionChecker.py              # Vérification automatique
functions/ticketTranscript.py                    # Système de transcript
views/ticketView/ticketSelectButton.py           # Création de tickets (modifié)
views/ticketView/close.py                        # Fermeture de tickets (modifié)
models/configuration.py                          # Modèle de config (modifié)
```

## 🔧 Utilisation

### Créer un ticket

1. L'utilisateur sélectionne une option dans le menu déroulant
2. Un ticket est créé avec :
   - L'utilisateur a accès
   - Le bot a accès
   - Le rôle staff a accès (automatique)
   - Les rôles administrateurs ont accès
   - Les autres rôles configurés ont accès

### Fermer un ticket

1. Cliquer sur le bouton "Fermer" dans le ticket
2. Le transcript est généré automatiquement
3. Le transcript est envoyé dans le canal de logs configuré
4. Le ticket est déplacé vers la catégorie "fermes" ou supprimé

## 🛡️ Sécurité

- Vérification des permissions avant chaque action
- Échappement HTML pour éviter XSS dans les transcripts
- Validation des rôles avant attribution
- Gestion des erreurs de permissions

## 📊 Logs

Le système log automatiquement :
- Définition du rôle staff
- Corrections de permissions
- Erreurs de génération de transcript
- Erreurs de permissions

## 🔍 Dépannage

### Le rôle staff n'a pas accès à un ticket

Le système de vérification automatique corrigera cela dans les 5 minutes. Vous pouvez aussi :
1. Vérifier que le rôle staff est bien configuré : `/setstaffrole`
2. Vérifier que le rôle existe toujours
3. Vérifier que le bot a les permissions nécessaires

### Le transcript ne se génère pas

1. Vérifier que les transcripts sont activés dans la config
2. Vérifier que le canal de logs est configuré
3. Vérifier les permissions du bot dans le canal de logs
4. Consulter les logs de la console pour plus de détails

### Erreur "Configuration manquante"

Utilisez `/create-config` pour créer la configuration du serveur.

## 📌 Notes Importantes

- Le système vérifie automatiquement les permissions toutes les 5 minutes
- Les transcripts sont générés en format TXT par défaut (plus fiable)
- Le système continue de fonctionner même si le transcript échoue
- Tous les IDs sont persistés dans `./configs/{guild_id}.json`

