# 🖥️ Commandes VPS - Mise à jour et redémarrage

## 📥 Récupérer les changements (Git Pull)

```bash
cd /opt/purity
git pull origin main
```

## 🔄 Redémarrer le bot (PM2)

### Redémarrer le bot
```bash
pm2 restart purity-bot
```

### Redémarrer avec mise à jour de l'environnement
```bash
pm2 restart purity-bot --update-env
```

### Arrêter le bot
```bash
pm2 stop purity-bot
```

### Démarrer le bot
```bash
pm2 start purity-bot
```

## 📊 Vérifier le statut

### Voir le statut du bot
```bash
pm2 status
```

### Voir les logs en temps réel
```bash
pm2 logs purity-bot
```

### Voir les logs (dernières 50 lignes)
```bash
pm2 logs purity-bot --lines 50
```

## 🔧 Commandes complètes (tout en une fois)

### Mise à jour complète et redémarrage
```bash
cd /opt/purity && git pull origin main && pm2 restart purity-bot
```

### Mise à jour avec logs
```bash
cd /opt/purity && git pull origin main && pm2 restart purity-bot && pm2 logs purity-bot --lines 20
```

## ⚠️ En cas de problème

### Si le bot ne démarre pas
```bash
cd /opt/purity
source venv/bin/activate
python3 main.py
```

### Vérifier les erreurs
```bash
pm2 logs purity-bot --err
```

### Redémarrer PM2 complètement
```bash
pm2 kill
pm2 start ecosystem.config.js
pm2 save
```

