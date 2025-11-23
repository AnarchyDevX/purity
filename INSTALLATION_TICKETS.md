# 📦 Installation du Système de Tickets

Guide d'installation et de mise à jour du nouveau système de tickets.

---

## 🆕 Nouveaux fichiers ajoutés

### Commandes (dans `commands/`)

```
commands/
├── moderation/
│   └── add-user.py                              # Commande /add user
├── configuration/
│   ├── ticket-category-manage.py                # Gestion des catégories
│   ├── set-role-ticket.py                       # Attribution des rôles
│   ├── tickets-adduser-role-config.py           # Config rôle /add
│   ├── tickets-preticket-category-config.py     # Config catégorie pré-tickets
│   └── ticket-embed-config.py                   # Config embed personnalisé
```

### Fonctions (dans `functions/`)

```
functions/
└── preticketHandler.py                          # Gestionnaire pré-formulaires
```

### Vues (dans `views/`)

```
views/
└── ticketView/
    └── ticketEmbedEdit.py                       # Interface d'édition embed
```

### Fichiers modifiés

```
views/ticketView/ticketSelectButton.py           # Support pré-formulaire
events/utils/ready.py                            # Initialisation handler
```

---

## ⚙️ Installation

### 1. Téléchargement

Tous les fichiers ont déjà été créés dans votre projet. Aucun téléchargement nécessaire.

### 2. Vérification des dépendances

Le système utilise les dépendances Discord.py déjà présentes :
- `discord.py` >= 2.0
- `asyncio` (inclus dans Python)
- `json` (inclus dans Python)

### 3. Redémarrage du bot

```bash
# Arrêter le bot
Ctrl+C

# Relancer le bot
python main.py
```

Le bot chargera automatiquement les nouvelles commandes au démarrage.

---

## 🔄 Migration depuis l'ancien système

### Compatibilité

✅ **Le nouveau système est 100% compatible avec l'ancien !**

- Les anciens panels de tickets continuent de fonctionner
- Les catégories de statut (nouveaux/en cours/pause/fermés) sont conservées
- Les configurations existantes ne sont pas modifiées

### Différences

| Ancien système | Nouveau système |
|----------------|-----------------|
| Options fixes dans le panel | Catégories dynamiques |
| Pas de pré-formulaire | Pré-formulaire avec 2 questions |
| Pas de mention de rôle auto | Mention automatique par catégorie |
| Embed fixe | Embed personnalisable |
| Pas de commande /add | Commande /add user disponible |

---

## 📝 Configuration initiale

### Étape 1 : Créer la catégorie des pré-tickets

```
/ticket-preticket-category-config category: @Pré-Tickets
```

> ⚠️ **Obligatoire** pour que le système fonctionne !

### Étape 2 : Créer vos catégories

```
/ticket-category-add name: "Support" emoji: 🎫 role: @Support
/ticket-category-add name: "Report Discord" emoji: ⚠️ role: @Modération
/ticket-category-add name: "Report In-Game" emoji: 🎮 role: @Staff
```

### Étape 3 : Personnaliser l'embed (optionnel)

```
/ticket-embed-config
```

Modifiez le titre, la description, la couleur, etc.

### Étape 4 : Créer le panel

Utilisez `/ticket-config` comme d'habitude, mais ajoutez vos nouvelles catégories dynamiques comme options !

---

## 🔍 Vérification de l'installation

### Test complet

1. **Vérifier les commandes**
   ```
   /ticket-category-list
   ```
   Devrait afficher vos catégories ou "Aucune catégorie".

2. **Créer une catégorie test**
   ```
   /ticket-category-add name: Test emoji: ✅
   ```

3. **Tester le pré-formulaire**
   - Créez un panel avec la catégorie "Test"
   - Sélectionnez la catégorie
   - Vérifiez que le pré-ticket est créé
   - Répondez aux 2 questions
   - Vérifiez que le ticket officiel est créé

4. **Tester /add**
   ```
   /add user: @UnMembre
   ```
   Dans un ticket actif.

### Résolution des problèmes

#### Le bot ne charge pas les nouvelles commandes

```bash
# Vérifier les logs au démarrage
# Les commandes devraient apparaître dans "Commands loaded: XX"

# Forcer la synchronisation
/ticket-category-list
```

#### Le pré-formulaire ne fonctionne pas

1. Vérifiez que la catégorie des pré-tickets est configurée :
   ```
   /ticket-preticket-category-config category: @Votre-Catégorie
   ```

2. Vérifiez que le bot a les permissions :
   - Gérer les salons
   - Voir les salons
   - Envoyer des messages
   - Gérer les permissions

#### /add ne fonctionne pas

1. Vérifiez que vous avez les permissions (admin, staff, ou rôle autorisé)
2. Vérifiez que vous êtes dans un ticket
3. Configurez le rôle autorisé :
   ```
   /ticket-adduser-role-config role: @VotreRôle
   ```

---

## 🗑️ Désinstallation (si nécessaire)

Si vous voulez revenir à l'ancien système :

1. Supprimer les nouveaux fichiers
2. Restaurer `ticketSelectButton.py` depuis un backup
3. Restaurer `ready.py` depuis un backup
4. Redémarrer le bot

> ⚠️ **Attention :** Les catégories dynamiques seront perdues.

---

## 🆘 Support

En cas de problème :

1. Vérifiez les logs du bot
2. Vérifiez les permissions Discord du bot
3. Consultez `TICKET_SYSTEM_GUIDE.md` pour la documentation complète
4. Consultez `TICKETS_QUICK_START.md` pour un guide rapide

---

## 📊 Statistiques d'installation

**Fichiers ajoutés :** 8
**Fichiers modifiés :** 2
**Nouvelles commandes :** 8
**Temps d'installation :** ~5 minutes

---

**Installation terminée ! 🎉**

Vous pouvez maintenant utiliser le nouveau système de tickets avec pré-formulaires et catégories dynamiques.

