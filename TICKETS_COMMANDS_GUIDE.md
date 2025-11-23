# 📋 Guide complet des commandes Tickets

## 🎯 Vue d'ensemble

Le système de tickets de Purity Bot est organisé en **deux systèmes** :

### 1️⃣ **Système Simple** (Sans questions)
- ✅ Création instantanée du ticket
- ❌ Pas de questions préalables
- 👉 Utilise : `/ticket-embed-config` sans catégories dynamiques

### 2️⃣ **Système Avancé** (Avec formulaire de questions)
- ✅ Pose 2 questions avant création
- ✅ Plus professionnel et organisé
- ✅ Collecte d'informations structurées
- 👉 Utilise : Catégories dynamiques + pré-tickets

---

## 📚 Liste complète des commandes

### 🎨 Configuration de base

#### `/ticket-embed-config`
**Obsolète - Ne PAS utiliser pour le nouveau système**
Créer un panel de tickets avec embed personnalisé.
- ⚠️ Cette commande n'est plus à jour
- 👉 Utilisez plutôt le nouveau système avec catégories dynamiques

---

### 🆕 Système de catégories dynamiques (RECOMMANDÉ)

#### `/ticket-category-add`
Créer une catégorie de ticket dynamique (avec questions).

**Paramètres :**
- `name` : Nom de la catégorie (ex: "Bug Report")
- `emoji` : Emoji (optionnel, ex: 🛠️)
- `role` : Rôle à mentionner (optionnel)
- `category` : Catégorie Discord (optionnel, créée auto sinon)

**Exemple :**
```
/ticket-category-add name:Bug Report emoji:🛠️ role:@Staff
```

---

#### `/ticket-category-remove`
Supprimer une catégorie dynamique.

**Paramètres :**
- `name` : Nom de la catégorie à supprimer
- `delete_category` : Supprimer aussi la catégorie Discord (optionnel)

---

#### `/ticket-category-list`
Lister toutes les catégories dynamiques configurées.

---

#### `/set-role-ticket`
Modifier le rôle à mentionner pour une catégorie existante.

**Paramètres :**
- `category` : Nom de la catégorie
- `role` : Nouveau rôle à mentionner

---

### 🕐 Configuration des pré-tickets

#### `/ticket-preticket-category-config`
**OBLIGATOIRE pour le système avec questions !**

Définir la catégorie où les channels temporaires seront créés pour poser les questions.

**Paramètres :**
- `category` : Catégorie Discord (créez "🕐 Pré-Tickets")

**Important :** Sans cette configuration, les questions ne seront PAS posées !

---

### 🗂️ Gestion des catégories de tickets

#### `/tickets-categories-config`
Configurer les 4 catégories de gestion des tickets :

**Paramètres :**
- `nouveaux` : Catégorie pour les nouveaux tickets
- `pris_en_charge` : Catégorie pour les tickets pris en charge
- `en_pause` : Catégorie pour les tickets en pause
- `fermes` : Catégorie pour les tickets fermés

---

### 👥 Permissions et rôles

#### `/tickets-staff-config`
Définir le rôle staff qui peut gérer les tickets.

**Paramètres :**
- `role` : Rôle du staff

---

#### `/tickets-roles-config`
Ajouter/retirer des rôles supplémentaires qui peuvent voir les tickets.

**Paramètres :**
- `action` : `add` ou `remove`
- `role` : Le rôle concerné

---

#### `/tickets-adduser-role-config`
Définir un rôle automatiquement ajouté aux utilisateurs qui ouvrent un ticket.

**Paramètres :**
- `role` : Le rôle à ajouter (ou None pour désactiver)

---

### 📝 Logs et transcripts

#### `/tickets-transcripts-config`
Configurer les transcripts des tickets fermés.

**Paramètres :**
- `enabled` : Activer/désactiver
- `channel` : Canal où envoyer les transcripts

---

### 🎨 Personnalisation avancée

#### `/ticket-embed-config`
**NOUVELLE VERSION - Personnaliser l'apparence des tickets**

Configure l'embed qui apparaît dans chaque ticket créé.

**Variables disponibles :**
- `{category}` - Nom de la catégorie
- `{user}` - Mention de l'utilisateur
- `{username}` - Nom de l'utilisateur
- `{roblox}` - Pseudo Roblox (du formulaire)
- `{reason}` - Raison (du formulaire)

---

## 🚀 Configuration recommandée (Étape par étape)

### Étape 1 : Créer les catégories Discord
Sur Discord, créez manuellement :
- 🕐 Pré-Tickets
- 📋 Tickets - Nouveaux
- ✅ Tickets - Pris en charge
- ⏸️ Tickets - En pause
- 🔒 Tickets - Fermés

### Étape 2 : Configurer le système de base
```
/ticket-preticket-category-config category:🕐 Pré-Tickets
/tickets-categories-config nouveaux:📋 Tickets - Nouveaux pris_en_charge:✅ Tickets - Pris en charge en_pause:⏸️ Tickets - En pause fermes:🔒 Tickets - Fermés
/tickets-staff-config role:@Staff
```

### Étape 3 : Créer vos catégories de tickets
```
/ticket-category-add name:Bug Report emoji:🛠️
/ticket-category-add name:Unban emoji:🔓
/ticket-category-add name:Partnership emoji:🤝
/ticket-category-add name:General Support emoji:🆘
/ticket-category-add name:Report Member emoji:🚨
```

### Étape 4 : (Optionnel) Personnaliser les embeds
```
/ticket-embed-config
```
Utilisez l'interface interactive pour personnaliser.

### Étape 5 : Créer le panel
Utilisez l'interface du bot pour créer un panel avec vos catégories.

---

## ❌ Commandes obsolètes (À NE PAS UTILISER)

- ~~`/ticket-config`~~ - Remplacée par le nouveau système

---

## 🔧 Dépannage

### Les questions ne sont pas posées ?
✅ Vérifiez que `/ticket-preticket-category-config` est bien configuré
✅ Vérifiez que vous utilisez des catégories dynamiques (créées avec `/ticket-category-add`)
✅ Les anciennes options de panel ne déclenchent PAS les questions

### Erreur "Failed to convert verification to TextChannel" ?
❌ Cette erreur vient de l'ancienne commande `/ticket-config`
✅ Utilisez le nouveau système avec catégories dynamiques

### Je ne vois pas mes catégories dans le menu ?
✅ Utilisez `/ticket-category-list` pour voir vos catégories
✅ Recréez le panel après avoir créé des catégories dynamiques

---

## 📊 Architecture du système

```
┌─────────────────────────────────────────┐
│  Utilisateur clique sur le menu         │
└──────────────┬──────────────────────────┘
               │
               ▼
┌──────────────────────────────────────────┐
│  Catégorie dynamique détectée ?          │
└───┬───────────────────────┬──────────────┘
    │ OUI                   │ NON
    ▼                       ▼
┌─────────────────┐   ┌──────────────────┐
│ Pré-Ticket      │   │ Ticket direct    │
│ (avec questions)│   │ (sans questions) │
└────────┬────────┘   └──────────────────┘
         │
         ▼
┌─────────────────────────────┐
│ 1. Channel temporaire créé  │
│ 2. Questions posées         │
│ 3. Ticket officiel créé     │
│ 4. Channel temporaire       │
│    supprimé                 │
└─────────────────────────────┘
```

---

## 💡 Conseils

1. **Toujours configurer** `/ticket-preticket-category-config` en premier
2. **Utilisez des noms clairs** pour vos catégories dynamiques
3. **Testez** après chaque configuration
4. **Activez les transcripts** pour garder un historique
5. **Définissez un rôle staff** pour une meilleure gestion

---

## 📞 Support

Si vous rencontrez des problèmes :
1. Vérifiez ce guide
2. Utilisez `/ticket-category-list` pour voir votre config
3. Assurez-vous que le bot a les permissions nécessaires
4. Recréez la configuration si nécessaire

---

**Développé par Celentroft**

