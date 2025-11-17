#!/bin/bash

# Script d'installation automatique de Purity Bot sur VPS
# Usage: bash install_vps.sh

set -e

# Couleurs pour les messages
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration
BOT_DIR="/opt/purity"
REPO_URL="https://github.com/AnarchyDevX/purity.git"
PM2_APP_NAME="purity-bot"

echo -e "${GREEN}🚀 Installation de Purity Bot sur VPS${NC}\n"

# Vérifier si on est root ou utiliser sudo
if [ "$EUID" -ne 0 ]; then 
    echo -e "${YELLOW}⚠️  Exécution en tant qu'utilisateur normal, sudo sera utilisé si nécessaire${NC}\n"
    SUDO="sudo"
else
    SUDO=""
fi

# Mettre à jour le système
echo -e "${YELLOW}📦 Mise à jour du système...${NC}"
$SUDO apt update -qq

# Installer les dépendances système
echo -e "${YELLOW}📦 Installation des dépendances système...${NC}"
$SUDO apt install -y git python3 python3-pip python3-venv nodejs npm

# Installer PM2 globalement
echo -e "${YELLOW}📦 Installation de PM2...${NC}"
$SUDO npm install -g pm2

# Créer le dossier du bot
echo -e "${YELLOW}📁 Création du dossier du bot...${NC}"
$SUDO mkdir -p $BOT_DIR
$SUDO chown -R $USER:$USER $BOT_DIR

# Cloner ou mettre à jour le repository
if [ -d "$BOT_DIR/.git" ]; then
    echo -e "${YELLOW}🔄 Mise à jour du repository existant...${NC}"
    cd $BOT_DIR
    git pull origin main
else
    echo -e "${YELLOW}📥 Clonage du repository...${NC}"
    git clone $REPO_URL $BOT_DIR
    cd $BOT_DIR
fi

# Créer un environnement virtuel Python
echo -e "${YELLOW}🐍 Création de l'environnement virtuel Python...${NC}"
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances Python
echo -e "${YELLOW}📦 Installation des dépendances Python...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Vérifier si config.json existe, sinon créer un template
if [ ! -f "$BOT_DIR/config.json" ]; then
    echo -e "${YELLOW}⚙️  Création du fichier config.json...${NC}"
    cat > $BOT_DIR/config.json << EOF
{
    "token": "VOTRE_TOKEN_ICI",
    "color": "#9b59b6",
    "buyer": [
        940965110443302974
    ],
    "blacklist": [],
    "guildjoin": true,
    "lang": "fr.json",
    "apichannel": null
}
EOF
    echo -e "${RED}⚠️  IMPORTANT: Modifiez config.json avec votre token avant de démarrer le bot!${NC}"
fi

# Arrêter PM2 si le bot tourne déjà
echo -e "${YELLOW}🛑 Arrêt de l'instance PM2 existante (si elle existe)...${NC}"
pm2 delete $PM2_APP_NAME 2>/dev/null || true

# Créer le fichier de configuration PM2
echo -e "${YELLOW}⚙️  Configuration de PM2...${NC}"
cat > $BOT_DIR/ecosystem.config.js << EOF
module.exports = {
  apps: [{
    name: '$PM2_APP_NAME',
    script: 'main.py',
    interpreter: '$BOT_DIR/venv/bin/python3',
    cwd: '$BOT_DIR',
    instances: 1,
    autorestart: true,
    watch: false,
    max_memory_restart: '500M',
    env: {
      NODE_ENV: 'production'
    },
    error_file: '$BOT_DIR/logs/pm2-error.log',
    out_file: '$BOT_DIR/logs/pm2-out.log',
    log_date_format: 'YYYY-MM-DD HH:mm:ss Z',
    merge_logs: true
  }]
};
EOF

# Créer le dossier logs si nécessaire
mkdir -p $BOT_DIR/logs

# Démarrer le bot avec PM2
echo -e "${YELLOW}🚀 Démarrage du bot avec PM2...${NC}"
cd $BOT_DIR
pm2 start ecosystem.config.js

# Sauvegarder la configuration PM2 pour le démarrage automatique
echo -e "${YELLOW}💾 Configuration du démarrage automatique PM2...${NC}"
pm2 save
pm2 startup | tail -1 | bash || true

echo -e "\n${GREEN}✅ Installation terminée avec succès!${NC}\n"
echo -e "${GREEN}📊 Commandes utiles:${NC}"
echo -e "  - Voir les logs: ${YELLOW}pm2 logs $PM2_APP_NAME${NC}"
echo -e "  - Statut: ${YELLOW}pm2 status${NC}"
echo -e "  - Redémarrer: ${YELLOW}pm2 restart $PM2_APP_NAME${NC}"
echo -e "  - Arrêter: ${YELLOW}pm2 stop $PM2_APP_NAME${NC}"
echo -e "  - Dossier du bot: ${YELLOW}$BOT_DIR${NC}\n"
echo -e "${RED}⚠️  N'oubliez pas de configurer votre token dans $BOT_DIR/config.json avant de démarrer!${NC}\n"

