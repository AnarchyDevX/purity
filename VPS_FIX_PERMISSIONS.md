# 🔧 Fix Complet des Permissions VPS

## ⚠️ Commandes à exécuter dans l'ordre

```bash
# 1. Corriger les permissions de TOUT le dossier
sudo chown -R ubuntu:ubuntu /opt/purity

# 2. S'assurer que le dossier configs existe et a les bonnes permissions
sudo mkdir -p /opt/purity/configs
sudo chown -R ubuntu:ubuntu /opt/purity/configs
sudo chmod -R 755 /opt/purity/configs

# 3. Mettre à jour le code
cd /opt/purity
git pull origin main

# 4. Redémarrer le bot
pm2 restart purity-bot

# 5. Vérifier les logs
pm2 logs purity-bot --lines 30
```

## 🚀 Commande tout-en-un

```bash
sudo chown -R ubuntu:ubuntu /opt/purity && sudo mkdir -p /opt/purity/configs && sudo chown -R ubuntu:ubuntu /opt/purity/configs && sudo chmod -R 755 /opt/purity/configs && cd /opt/purity && git pull origin main && pm2 restart purity-bot && pm2 logs purity-bot --lines 30
```

## ✅ Vérifications

Après avoir exécuté les commandes, vérifiez que :
- Plus d'erreurs `PermissionError` dans les logs
- Le bot démarre correctement
- Les commandes fonctionnent

