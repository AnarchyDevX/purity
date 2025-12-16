# 🎯 Système de Statut Rotatif

## 📋 Description

Le bot affiche maintenant automatiquement des statistiques utiles et fun qui changent toutes les 30 secondes.

## 📊 Statistiques affichées

Le statut du bot affiche en rotation :

1. **Nombre total de membres** (sans doublons)
2. **Nombre de serveurs**
3. **Nombre de membres en ligne**
4. **Nombre d'utilisateurs réels** (non-bots)
5. **Nombre total de salons**
6. **Nombre de commandes**
7. **Uptime du bot** (temps depuis le démarrage)
8. **Message d'aide** (/help)
9. **Nom du bot** (Purity Bot)

## ⚙️ Configuration

### Modifier l'intervalle de rotation

Dans `events/utils/rotatingStatus.py`, ligne 99 :
```python
@tasks.loop(seconds=30)  # Change toutes les 30 secondes
```
Modifiez `30` pour changer l'intervalle (en secondes).

### Ajouter/Modifier des statuts

Dans la fonction `get_status_messages()`, ajoutez de nouveaux statuts dans la liste `statuses` :

```python
{
    "type": discord.ActivityType.watching,  # ou playing, listening, streaming
    "name": "Votre message ici"
}
```

**Types disponibles :**
- `discord.ActivityType.watching` → "Regarde ..."
- `discord.ActivityType.playing` → "Joue à ..."
- `discord.ActivityType.listening` → "Écoute ..."
- `discord.ActivityType.streaming` → "Stream ..." (nécessite une URL)

## 🔧 Désactiver l'ancien système Roblox

Le fichier `events/utils/robloxStatus.py` a été désactivé pour éviter les conflits. Si vous voulez le réactiver, décommentez la ligne 10 :

```python
self.update_status.start()
```

## 📝 Notes

- Les statistiques sont calculées en temps réel
- Le système démarre automatiquement au chargement du bot
- Les nombres sont formatés avec des espaces (ex: 1 000 au lieu de 1000)
- L'uptime est calculé depuis le démarrage du bot

## 🚀 Fonctionnalités

- ✅ Rotation automatique toutes les 30 secondes
- ✅ Statistiques en temps réel
- ✅ Formatage des nombres
- ✅ Calcul de l'uptime
- ✅ Gestion des erreurs
- ✅ Pas de conflit avec d'autres systèmes




