# 🚀 Guide Rapide - Système de Tickets

Guide de démarrage rapide pour le nouveau système de tickets avec pré-formulaires.

---

## ⚡ Configuration en 5 minutes

### 1️⃣ Configurer la catégorie des pré-tickets
```
/ticket-preticket-category-config category: [Votre Catégorie]
```
> **Important :** Cette étape est obligatoire pour que le système fonctionne !

### 2️⃣ Créer votre première catégorie de ticket
```
/ticket-category-add name: Support emoji: 🎫 role: @Support
```

### 3️⃣ Personnaliser l'embed (optionnel)
```
/ticket-embed-config
```

### 4️⃣ Créer le panel de tickets
```
/ticket-config channel: #tickets category: [Catégorie par défaut]
```
Ajoutez vos options et envoyez le panel !

---

## 🎯 Commandes principales

| Commande | Description |
|----------|-------------|
| `/ticket-category-add` | Ajouter une catégorie de ticket |
| `/ticket-category-list` | Voir toutes les catégories |
| `/ticket-category-remove` | Supprimer une catégorie |
| `/set-role-ticket` | Définir le rôle d'une catégorie |
| `/ticket-embed-config` | Personnaliser l'embed |
| `/ticket-preticket-category-config` | Définir où créer les pré-tickets |
| `/ticket-adduser-role-config` | Définir qui peut utiliser /add |
| `/add user: @membre` | Ajouter un membre à un ticket |

---

## 📝 Comment ça marche ?

### Pour l'utilisateur :
1. Clic sur le menu de tickets
2. Sélection d'une catégorie
3. Channel temporaire créé automatiquement
4. 2 questions posées :
   - Pseudo Roblox ?
   - Raison de la demande ?
5. Ticket officiel créé avec embed récapitulatif
6. Channel temporaire supprimé

### Pour le staff :
- Mention automatique selon la catégorie
- Accès immédiat au ticket
- Embed personnalisable
- Ajout de membres avec `/add`

---

## 🎨 Variables dans les embeds

Utilisez ces variables dans le titre et la description :

- `{category}` → Nom de la catégorie
- `{user}` → @Mention de l'utilisateur
- `{username}` → Nom de l'utilisateur
- `{roblox}` → Pseudo Roblox
- `{reason}` → Raison du ticket

**Exemple :**
```
Titre: 🎫 {category} - {username}
Description: Bonjour {user} ! Pseudo Roblox: {roblox}
```

---

## ⏱️ Système de timeout

- **5 minutes** par question
- Si pas de réponse → pré-ticket supprimé
- Message d'avertissement avant suppression

---

## ❓ FAQ Rapide

**Q: Puis-je avoir des tickets sans pré-formulaire ?**
→ Oui ! Les anciennes options (via `/ticket-config`) fonctionnent sans pré-formulaire.

**Q: Comment modifier un rôle de catégorie ?**
→ Utilisez `/set-role-ticket category: [nom] role: @role`

**Q: Comment réinitialiser l'embed ?**
→ Dans `/ticket-embed-config`, cliquez sur "Réinitialiser"

**Q: Qui peut utiliser /add ?**
→ Admins + rôle staff tickets + rôle défini avec `/ticket-adduser-role-config`

---

## 🔗 Documentation complète

Pour plus de détails, consultez `TICKET_SYSTEM_GUIDE.md`

---

**Version 1.0** | Système de tickets dynamiques avec pré-formulaires

