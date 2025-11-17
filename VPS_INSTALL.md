# 🚀 Installation rapide sur VPS

## Option 1 : Script automatique (Recommandé)

```bash
# Télécharger et exécuter le script d'installation
curl -o install_vps.sh https://raw.githubusercontent.com/AnarchyDevX/purity/main/install_vps.sh
chmod +x install_vps.sh
bash install_vps.sh
```

## Option 2 : Commandes manuelles

### 1. Installation des dépendances système
```bash
sudo apt update
sudo apt install -y git python3 python3-pip python3-venv nodejs npm
sudo npm install -g pm2
```

### 2. Cloner le repository
```bash
sudo mkdir -p /opt/purity
sudo chown -R $USER:$USER /opt/purity
cd /opt
git clone https://github.com/AnarchyDevX/purity.git
cd purity
```

### 3. Installer les dépendances Python
```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configurer le bot
```bash
# Créer config.json si nécessaire
nano config.json
# Ajoutez votre token Discord
```

### 5. Lancer avec PM2
```bash
# Créer la configuration PM2
cat > ecosystem.config.js << 'EOF'
module.exports = {
  apps: [{
    name: 'purity-bot',
    script: 'main.py',
    interpreter: '/opt/purity/venv/bin/python3',
    cwd: '/opt/purity',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    error_file: '/opt/purity/logs/pm2-error.log',
    out_file: '/opt/purity/logs/pm2-out.log'
  }]
};
EOF

# Démarrer le bot
pm2 start ecosystem.config.js
pm2 save
pm2 startup
```

## 📊 Commandes PM2 utiles

```bash
# Voir les logs en temps réel
pm2 logs purity-bot

# Voir le statut
pm2 status

# Redémarrer le bot
pm2 restart purity-bot

# Arrêter le bot
pm2 stop purity-bot

# Voir les logs (dernières 100 lignes)
pm2 logs purity-bot --lines 100

# Surveiller les ressources
pm2 monit
```

## 🔄 Mise à jour du bot

```bash
cd /opt/purity
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
pm2 restart purity-bot
```

## ⚠️ Important

- N'oubliez pas de configurer votre token Discord dans `config.json`
- Le bot sera automatiquement relancé au redémarrage du VPS grâce à PM2
- Les logs sont disponibles dans `/opt/purity/logs/`

