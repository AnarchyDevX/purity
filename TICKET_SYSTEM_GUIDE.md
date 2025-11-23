# 🎫 Guide du Système de Tickets Dynamiques

Ce guide explique comment utiliser le nouveau système de tickets avec pré-formulaires et catégories dynamiques.

---

## 📋 Table des matières

1. [Configuration initiale](#configuration-initiale)
2. [Gestion des catégories dynamiques](#gestion-des-catégories-dynamiques)
3. [Configuration du pré-formulaire](#configuration-du-pré-formulaire)
4. [Attribution des rôles par catégorie](#attribution-des-rôles-par-catégorie)
5. [Personnalisation de l'embed des tickets](#personnalisation-de-lembed-des-tickets)
6. [Ajout de membres aux tickets](#ajout-de-membres-aux-tickets)
7. [Utilisation](#utilisation)

---

## 🔧 Configuration initiale

### 1. Configurer la catégorie des pré-tickets

Avant que le système de pré-formulaire fonctionne, vous devez définir où les channels temporaires seront créés :

```
/ticket-preticket-category-config category: [Votre Catégorie]
```

**Exemple :** `/ticket-preticket-category-config category: 🎫 Pré-Tickets`

> ⚠️ **Important :** Sans cette configuration, le système de pré-formulaire ne fonctionnera pas !

### 2. Configurer le rôle pour /add user (optionnel)

Si vous voulez permettre à un rôle spécifique d'ajouter des membres aux tickets :

```
/ticket-adduser-role-config role: [Votre Rôle]
```

**Exemple :** `/ticket-adduser-role-config role: @Modérateur`

> 📝 **Note :** Les administrateurs et le rôle staff des tickets peuvent toujours utiliser cette commande.

---

## 📁 Gestion des catégories dynamiques

### Ajouter une catégorie

```
/ticket-category-add name: [Nom] emoji: [Emoji] role: [@Role] category: [Catégorie Discord]
```

**Paramètres :**
- `name` (obligatoire) : Le nom de la catégorie (ex: Support, Report Discord, Report In-Game)
- `emoji` (optionnel) : L'emoji pour cette catégorie
- `role` (optionnel) : Le rôle à mentionner lors de la création d'un ticket de cette catégorie
- `category` (optionnel) : La catégorie Discord où créer les tickets. Si non fournie, une catégorie sera créée automatiquement.

**Exemples :**

```
/ticket-category-add name: Support emoji: 🎫 role: @Support category: Support Tickets
/ticket-category-add name: Report Discord emoji: ⚠️ role: @Modération
/ticket-category-add name: Report In-Game emoji: 🎮 role: @Staff In-Game
```

### Lister les catégories

```
/ticket-category-list
```

Affiche toutes les catégories configurées avec leurs informations.

### Supprimer une catégorie

```
/ticket-category-remove name: [Nom] delete_category: [True/False]
```

**Paramètres :**
- `name` (obligatoire) : Le nom exact de la catégorie à supprimer
- `delete_category` (optionnel, défaut: False) : Supprimer aussi la catégorie Discord

**Exemples :**

```
/ticket-category-remove name: Support delete_category: False
/ticket-category-remove name: Report Discord delete_category: True
```

---

## 🎯 Configuration du pré-formulaire

Le système de pré-formulaire fonctionne automatiquement pour toutes les catégories dynamiques créées avec `/ticket-category-add`.

### Fonctionnement

1. L'utilisateur sélectionne une catégorie dans le menu de tickets
2. Un channel temporaire `pre-ticket-USERNAME` est créé
3. Le bot pose 2 questions :
   - **Question 1 :** Quel est ton pseudo Roblox ?
   - **Question 2 :** Quelle est la raison de ta demande ?
4. L'utilisateur a **5 minutes** pour répondre à chaque question
5. Une fois les réponses reçues, le ticket officiel est créé avec un embed récapitulatif
6. Le channel temporaire est supprimé automatiquement

### Timeout

- Si l'utilisateur ne répond pas dans les **5 minutes**, le pré-ticket est annulé et supprimé
- Un message d'avertissement est envoyé avant la suppression

---

## 👥 Attribution des rôles par catégorie

### Définir un rôle pour une catégorie

```
/set-role-ticket category: [Nom] role: [@Role]
```

**Paramètres :**
- `category` (obligatoire) : Le nom exact de la catégorie (autocomplétion disponible)
- `role` (optionnel) : Le rôle à mentionner. Laisser vide pour supprimer.

**Exemples :**

```
/set-role-ticket category: Support role: @Support
/set-role-ticket category: Report Discord role: @Modération
/set-role-ticket category: Report In-Game
```

> 💡 **Astuce :** La commande propose l'autocomplétion pour le nom de la catégorie !

### Rôle mentionné automatiquement

Lorsqu'un ticket est créé dans une catégorie avec un rôle configuré :
- Le rôle est mentionné dans le premier message du ticket
- Les membres avec ce rôle reçoivent une notification

---

## 🎨 Personnalisation de l'embed des tickets

Vous pouvez personnaliser complètement l'apparence de l'embed qui apparaît dans les tickets.

### Configuration de l'embed

```
/ticket-embed-config
```

Cette commande ouvre un menu interactif avec les options suivantes :

#### ✏️ Modifier le titre

Personnalisez le titre de l'embed. Vous pouvez utiliser des variables :
- `{category}` - Le nom de la catégorie
- `{user}` - Mention de l'utilisateur
- `{username}` - Nom de l'utilisateur
- `{roblox}` - Pseudo Roblox
- `{reason}` - Raison du ticket

**Exemple :** `🎫 Support - {category} | {username}`

#### 📝 Modifier la description

Personnalisez la description de l'embed. Supporte les mêmes variables que le titre.

**Exemple :** `Bienvenue {user} ! Votre demande concernant **{category}** sera traitée rapidement.`

#### 🎨 Modifier la couleur

Définissez une couleur personnalisée pour l'embed en format hexadécimal.

**Exemples :**
- `FF5733` (rouge-orange)
- `#00FF00` (vert)
- `3498DB` (bleu)

Laisser vide pour utiliser la couleur par défaut.

#### 📌 Modifier le footer

Personnalisez le texte du footer de l'embed.

**Exemple :** `Ticket System - Support disponible 24/7`

Laisser vide pour utiliser le footer par défaut.

#### 👁️ Affichage des champs

Choisissez quels champs afficher dans l'embed :
- ✅ **Utilisateur** - Affiche qui a créé le ticket
- ✅ **Pseudo Roblox** - Affiche le pseudo Roblox
- ✅ **Catégorie** - Affiche la catégorie du ticket
- ✅ **Raison** - Affiche la raison du ticket

Vous pouvez activer ou désactiver chaque champ individuellement.

#### 🔄 Réinitialiser

Réinitialise le template aux valeurs par défaut.

#### ✅ Terminer

Sauvegarde et ferme le menu de configuration.

### Aperçu en temps réel

Le menu affiche un aperçu en temps réel de l'embed avec vos modifications. Vous voyez exactement ce que les utilisateurs verront dans leurs tickets.

### Variables disponibles

| Variable | Description | Exemple |
|----------|-------------|---------|
| `{category}` | Nom de la catégorie | Support |
| `{user}` | Mention de l'utilisateur | @Jean |
| `{username}` | Nom de l'utilisateur | Jean |
| `{roblox}` | Pseudo Roblox | Player123 |
| `{reason}` | Raison du ticket | J'ai besoin d'aide |

### Exemples de configurations

**Configuration minimaliste :**
```
Titre: 🎫 {category}
Description: {user}, merci de patienter.
Champs: Raison uniquement
```

**Configuration détaillée :**
```
Titre: 🎫 Support - {category} | Ticket de {username}
Description: Bonjour {user} ! 👋\n\nVotre demande concernant **{category}** a été reçue.\nUn membre de notre équipe va vous prendre en charge dans les plus brefs délais.
Couleur: 5865F2
Champs: Tous activés
Footer: Support disponible 24/7 - Merci de votre patience
```

**Configuration gaming :**
```
Titre: 🎮 {category} - Joueur: {roblox}
Description: Salut {user} ! Notre équipe vérifie votre demande.\n\n**Raison:** {reason}
Couleur: FF6B6B
Champs: Pseudo Roblox, Raison
Footer: Temps de réponse moyen: 5 minutes
```

---

## ➕ Ajout de membres aux tickets

### Commande /add

```
/add user: [@Membre]
```

**Qui peut utiliser cette commande ?**
1. Les administrateurs (toujours)
2. Le rôle staff des tickets (défini dans `/tickets-staff-config`)
3. Le rôle défini avec `/ticket-adduser-role-config`

**Vérifications automatiques :**
- ✅ Vérifie que c'est un channel de ticket
- ✅ Vérifie que le membre n'est pas déjà dans le ticket
- ✅ Vérifie les permissions de l'utilisateur qui exécute la commande

**Exemple :**

```
/add user: @Jean
```

---

## 🎮 Utilisation

### Pour les utilisateurs

1. Cliquez sur le bouton de création de tickets
2. Sélectionnez une catégorie dans le menu déroulant
3. Un channel temporaire est créé pour vous
4. Répondez aux 2 questions posées par le bot
5. Votre ticket officiel est créé automatiquement
6. Un embed récapitulatif est affiché avec vos informations

### Pour le staff

1. Vous êtes mentionné automatiquement dans les tickets de votre catégorie
2. Vous pouvez ajouter des membres avec `/add user: @membre`
3. Vous pouvez claim le ticket avec le bouton "Claim"
4. Vous pouvez fermer le ticket avec le bouton "Fermer"

---

## 📊 Structure de données (JSON)

Pour référence, voici la structure des données dans le fichier de configuration :

```json
{
  "tickets": {
    "preticket_category": 1234567890123456789,
    "add_user_role": 9876543210987654321,
    "ticket_categories": {
      "Support": {
        "role_id": 123456789012345678,
        "discord_category_id": 987654321098765432,
        "emoji": "🎫"
      },
      "Report Discord": {
        "role_id": 234567890123456789,
        "discord_category_id": 876543210987654321,
        "emoji": "⚠️"
      }
    }
  }
}
```

---

## ❓ FAQ

### Q: Puis-je avoir des catégories sans pré-formulaire ?

**R:** Oui ! Les catégories ajoutées via `/ticket-config` (ancien système) fonctionnent toujours sans pré-formulaire. Seules les catégories créées avec `/ticket-category-add` utilisent le pré-formulaire.

### Q: Que se passe-t-il si je ne configure pas de catégorie de pré-tickets ?

**R:** Les utilisateurs verront un message d'erreur leur indiquant que la catégorie n'est pas configurée. Utilisez `/ticket-preticket-category-config` pour la configurer.

### Q: Puis-je modifier un rôle après avoir créé une catégorie ?

**R:** Oui ! Utilisez simplement `/set-role-ticket` avec le nom de la catégorie et le nouveau rôle.

### Q: Comment supprimer le rôle d'une catégorie ?

**R:** Utilisez `/set-role-ticket category: [Nom]` sans spécifier de rôle.

### Q: Puis-je avoir plusieurs rôles pour une catégorie ?

**R:** Non, actuellement une seule mention de rôle est supportée par catégorie. Vous pouvez utiliser le système de rôles staff général avec `/tickets-roles-config` pour ajouter plusieurs rôles à tous les tickets.

---

## 🔒 Sécurité

- Le rôle hardcodé (`SUPPORT_ROLE_ID = 1366762115594977300`) reste en fallback
- Les permissions sont vérifiées à chaque commande
- Les utilisateurs ne peuvent pas avoir plusieurs pré-tickets simultanés
- Les pré-tickets expirent après 5 minutes d'inactivité

---

## 🚀 Améliorations futures possibles

- [ ] Questions personnalisables par catégorie
- [ ] Nombre de questions configurable
- [ ] Timeout personnalisable
- [ ] Support de plusieurs rôles par catégorie
- [ ] Système de templates pour les messages de pré-tickets

---

**Développé pour Purity**
*Version 1.0 - Système de tickets dynamiques avec pré-formulaires*

