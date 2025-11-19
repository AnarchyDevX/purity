# 🖥️ Commandes VPS - Mise à jour et redémarrage

## 📥 Récupérer les changements (Git Pull)

### Si erreur "dubious ownership" (première fois)
```bash
git config --global --add safe.directory /opt/purity
```

### Puis récupérer les changements
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

## 🔄 Réinstallation complète (supprimer et tout re-télécharger)

### ⚠️ ATTENTION : Cette commande supprime TOUT et réinstalle depuis zéro

```bash
# Arrêter le bot
pm2 stop purity-bot
pm2 delete purity-bot

# Supprimer le répertoire
sudo rm -rf /opt/purity

# Recréer le répertoire
sudo mkdir -p /opt/purity
sudo chown -R ubuntu:ubuntu /opt/purity

# Cloner le repo
cd /opt
git clone https://github.com/AnarchyDevX/purity.git

# Aller dans le dossier
cd /opt/purity

# Créer le venv
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install --upgrade pip
pip install -r requirements.txt

# Créer les dossiers nécessaires
mkdir -p configs logs backups

# Créer le fichier config.json (IMPORTANT : ajouter votre token)
nano config.json
# Ou utiliser cat :
# cat > config.json << 'EOF'
# {
#   "token": "VOTRE_TOKEN_ICI",
#   "buyer": []
# }
# EOF

# Créer le fichier ecosystem.config.js
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'purity-bot',
    script: 'main.py',
    interpreter: 'python3',
    interpreter_args: '-u',
    cwd: '/opt/purity',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    error_file: '/opt/purity/logs/pm2-error.log',
    out_file: '/opt/purity/logs/pm2-out.log',
    env: {
      VIRTUAL_ENV: '/opt/purity/venv',
      PATH: '/opt/purity/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
    }
  }]
};
EOF

# Configurer Git (si nécessaire)
git config --global --add safe.directory /opt/purity

# Démarrer avec PM2
pm2 start ecosystem.config.js
pm2 save
pm2 startup

# Vérifier les logs
pm2 logs purity-bot --lines 30
```

### 🚀 Commande tout-en-un (après avoir créé config.json manuellement)

```bash
pm2 stop purity-bot && pm2 delete purity-bot && sudo rm -rf /opt/purity && sudo mkdir -p /opt/purity && sudo chown -R ubuntu:ubuntu /opt/purity && cd /opt && git clone https://github.com/AnarchyDevX/purity.git && cd /opt/purity && python3 -m venv venv && source venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt && mkdir -p configs logs backups && git config --global --add safe.directory /opt/purity && cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'purity-bot',
    script: 'main.py',
    interpreter: 'python3',
    interpreter_args: '-u',
    cwd: '/opt/purity',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    error_file: '/opt/purity/logs/pm2-error.log',
    out_file: '/opt/purity/logs/pm2-out.log',
    env: {
      VIRTUAL_ENV: '/opt/purity/venv',
      PATH: '/opt/purity/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
    }
  }]
};
EOF
pm2 start ecosystem.config.js && pm2 save && pm2 logs purity-bot --lines 30
```

**⚠️ IMPORTANT :** N'oubliez pas de créer le fichier `config.json` avec votre token avant de démarrer !

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

