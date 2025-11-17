# 📋 Documentation des Permissions - Purity Bot

## 🔐 Système de Permissions

- **`check_perms()`** : Commandes (interactions)
- **`check_id_perms()`** : Événements antiraid

---

## 👥 Rangs

| Rang | Défini dans | Accès |
|------|-------------|-------|
| **🟢 BUYER** | `config.json` → `buyer[]` | Niveaux 1, 2, 3 |
| **🟡 OWNER** | `configs/{guild_id}.json` → `ownerlist[]` | Niveaux 1, 2 |
| **🔵 WHITELIST** | `configs/{guild_id}.json` → `whitelist[]` | Niveau 1 |

---

## 📊 Permissions par Niveau

| Niveau | Buyer | Owner | Whitelist |
|--------|-------|-------|-----------|
| **1** | ✅ | ✅ | ✅ |
| **2** | ✅ | ✅ | ❌ |
| **3** | ✅ | ❌ | ❌ |

---

## 🎯 Niveau 1

**Accès :** Buyer ✅ | Owner ✅ | Whitelist ✅

**Commandes :**
- `/ban`, `/kick`, `/mute`, `/warn`, `/member-warn`, `/clear`
- `/voice-mute`, `/voice-deaf`, `/voice-kick`, `/voice-move`, `/voice-afk`
- `/say`, `/mp`, `/snipe`
- `/all-admins`, `/all-bot-admin`, `/all-ban`, `/booster-list`, `/role-members-list`

**Exemptions Antiraid :**
- Antilien
- Badwords

---

## ⚙️ Niveau 2

**Accès :** Buyer ✅ | Owner ✅ | Whitelist ❌

**Configuration :**
- `/antiraid-panel`, `/logs-panel`
- `/tickets-config`, `/tickets-categories-config`, `/tickets-transcripts-config`
- `/badwords-config`, `/autorole-config`
- `/greeting-config`, `/join-message-config`
- `/captcha-config`, `/jail-config`, `/soutien-config`
- `/onlypic-config`, `/ghostping-config`, `/compteurs-config`
- `/tempVocie-panel`, `/role-react`, `/roblox-config`

**Gestion :**
- `/lock`, `/unlock`, `/channel-rename`
- `/clear-target`, `/derank`, `/renew`
- `/add-role`, `/remove-role`, `/jail`
- `/gstart`, `/reroll`
- `/embed`, `/verify-roblox`
- `/whitelist`, `/name-edit`
- `/voice-lock-all`, `/voice-unlock-all`, `/voice-lock`, `/unlock-voice`, `/move-all`

**Exemptions Antiraid :**
- Antichannels
- Antiroles
- Antiranks

---

## 🔴 Niveau 3

**Accès :** Buyer ✅ | Owner ❌ | Whitelist ❌

**Commandes :**
- `/backup-create`, `/backup-list`, `/backup-load`
- `/owner`
- `/pfp-edit`, `/banner-edit`, `/set-status`
- `/guild-list`, `/leave`
- `/invite-link`, `/blacklist`

**Exemptions Antiraid :**
- Antiwebhook

---

## 📌 Exemptions Antiraid

| Module | Niveau | Exemptions |
|--------|--------|------------|
| Antilien | 1 | Buyer, Owner, Whitelist |
| Badwords | 1 | Buyer, Owner, Whitelist |
| Antichannels | 2 | Buyer, Owner |
| Antiroles | 2 | Buyer, Owner |
| Antiranks | 2 | Buyer, Owner |
| Antiwebhook | 3 | Buyer uniquement |

---

## ⚠️ Notes

- **Permissions Discord natives (administrateur) ne sont PAS vérifiées**
- **Permissions cumulatives** : Buyer (1+2+3), Owner (1+2), Whitelist (1)
- **Configuration :** `ownerlist`/`whitelist` par serveur, `buyer` global

---

## 📝 Exemples

**`config.json` (Global)**
```json
{
  "buyer": [123456789012345678]
}
```

**`configs/{guild_id}.json` (Par serveur)**
```json
{
  "ownerlist": [111111111111111111],
  "whitelist": [333333333333333333]
}
```
