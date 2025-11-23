#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de migration des configurations
Ajoute automatiquement les champs manquants dans toutes les configs JSON
"""

import json
import os
import shutil
from datetime import datetime
from typing import Dict, Any

# Structure complète par défaut
DEFAULT_CONFIG = {
    "ownerlist": [],
    "whitelist": [],
    "badwords": [],
    "lockedvoice": [],
    "logs": {
        "modlogs": {
            "alive": False,
            "channel": None
        },
        "msglogs": {
            "alive": False,
            "channel": None
        },
        "raidlogs": {
            "alive": False,
            "channel": None
        },
        "voicelogs": {
            "alive": False,
            "channel": None
        },
        "ranklogs": {
            "alive": False,
            "channel": None
        },
        "joinleavelogs": {
            "alive": False,
            "channel": None
        }
    },
    "antiraid": {
        "antibot": False,
        "antilien": False,
        "badwords": False,
        "antimassjoin": False,
        "channels": {
            "create": False,
            "edit": False,
            "delete": False
        },
        "roles": {
            "create": False,
            "edit": False,
            "delete": False
        },
        "rank": {
            "up": False,
            "down": False
        },
        "webhook": False
    },
    "configuration": {
        "autoreact": {},
        "rolereact": {},
        "autorole": [],
        "tempvoices": {
            "active": [],
            "configs": {}
        }
    },
    "warndb": {
        "maxwarn": 10,
        "sanction": "kick",
        "users": {}
    },
    "tickets": {
        "logs": None,
        "transcripts": True,
        "roles": [],
        "staff_role": None,
        "claim": True,
        "buttons": {},
        "categories": {
            "nouveaux": None,
            "pris_en_charge": None,
            "en_pause": None,
            "fermes": None
        },
        "adduser_role": None,
        "preticket_category": None
    },
    "onlypic": [],
    "greeting": {
        "active": False,
        "type": "message",
        "channel": None,
        "mention": False
    },
    "greetmsg": {
        "alive": False,
        "content": ""
    },
    "soutien": {
        "active": False,
        "needed": "rien",
        "role": None
    },
    "jail": {
        "active": False,
        "role": None
    },
    "ghostping": [],
    "compteurs": {},
    "antispam": {
        "message": {
            "timeout": 1000,
            "active": False
        },
        "mentions": {
            "timeout": 1000,
            "active": False
        }
    },
    "badwords_learning": {
        "enabled": False,
        "suspicion_channel": None,
        "threshold": 3,
        "suspicions": {}
    },
    "captcha": {
        "active": False,
        "channel_id": None,
        "message_id": None,
        "role_id": None
    }
}


def merge_dict(source: Dict, default: Dict) -> tuple[Dict, list]:
    """
    Merge source dict with default, adding missing keys
    Returns (merged_dict, list_of_added_keys)
    """
    result = source.copy()
    added_keys = []
    
    for key, default_value in default.items():
        if key not in result:
            result[key] = default_value
            added_keys.append(key)
        elif isinstance(default_value, dict) and isinstance(result[key], dict):
            # Récursivement merger les sous-dictionnaires
            merged, sub_added = merge_dict(result[key], default_value)
            result[key] = merged
            if sub_added:
                added_keys.extend([f"{key}.{k}" for k in sub_added])
    
    return result, added_keys


def backup_config(config_path: str, backup_dir: str) -> str:
    """Crée un backup de la config"""
    os.makedirs(backup_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(config_path)
    backup_path = os.path.join(backup_dir, f"{timestamp}_{filename}")
    shutil.copy2(config_path, backup_path)
    return backup_path


def migrate_config_file(config_path: str, backup_dir: str = "./migration_backups") -> Dict[str, Any]:
    """Migre un fichier de configuration"""
    print(f"\n{'='*60}")
    print(f"Migration: {config_path}")
    print(f"{'='*60}")
    
    # Charger la config existante
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            current_config = json.load(f)
    except Exception as e:
        print(f"❌ Erreur lors de la lecture: {e}")
        return {"status": "error", "error": str(e)}
    
    # Faire un backup
    try:
        backup_path = backup_config(config_path, backup_dir)
        print(f"✅ Backup créé: {backup_path}")
    except Exception as e:
        print(f"⚠️  Impossible de créer le backup: {e}")
        return {"status": "error", "error": f"Backup failed: {e}"}
    
    # Merger avec la structure par défaut
    merged_config, added_keys = merge_dict(current_config, DEFAULT_CONFIG)
    
    if not added_keys:
        print("✅ Configuration déjà à jour (aucun champ manquant)")
        return {
            "status": "up_to_date",
            "file": config_path,
            "added_keys": []
        }
    
    # Sauvegarder la config migrée
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(merged_config, f, indent=4, ensure_ascii=False)
        
        print(f"✅ Configuration migrée avec succès!")
        print(f"📝 Champs ajoutés ({len(added_keys)}):")
        for key in added_keys:
            print(f"   - {key}")
        
        return {
            "status": "migrated",
            "file": config_path,
            "added_keys": added_keys,
            "backup": backup_path
        }
    except Exception as e:
        print(f"❌ Erreur lors de l'écriture: {e}")
        return {"status": "error", "error": str(e)}


def migrate_all_configs(configs_dir: str = "./configs") -> Dict[str, Any]:
    """Migre toutes les configurations du dossier"""
    print("\n" + "="*60)
    print("🚀 MIGRATION DES CONFIGURATIONS")
    print("="*60)
    
    if not os.path.exists(configs_dir):
        print(f"❌ Le dossier {configs_dir} n'existe pas!")
        return {"status": "error", "error": "Config directory not found"}
    
    # Lister tous les fichiers JSON
    config_files = [
        os.path.join(configs_dir, f) 
        for f in os.listdir(configs_dir) 
        if f.endswith('.json')
    ]
    
    if not config_files:
        print(f"⚠️  Aucun fichier de configuration trouvé dans {configs_dir}")
        return {"status": "no_files"}
    
    print(f"📁 {len(config_files)} fichier(s) de configuration trouvé(s)")
    
    # Migrer chaque fichier
    results = []
    for config_file in config_files:
        result = migrate_config_file(config_file)
        results.append(result)
    
    # Résumé
    print("\n" + "="*60)
    print("📊 RÉSUMÉ DE LA MIGRATION")
    print("="*60)
    
    migrated = sum(1 for r in results if r["status"] == "migrated")
    up_to_date = sum(1 for r in results if r["status"] == "up_to_date")
    errors = sum(1 for r in results if r["status"] == "error")
    
    print(f"✅ Fichiers migrés: {migrated}")
    print(f"✔️  Fichiers déjà à jour: {up_to_date}")
    print(f"❌ Erreurs: {errors}")
    print(f"📁 Total: {len(results)}")
    
    if errors > 0:
        print("\n❌ Fichiers en erreur:")
        for r in results:
            if r["status"] == "error":
                print(f"   - {r.get('file', 'unknown')}: {r.get('error', 'unknown error')}")
    
    return {
        "status": "completed",
        "total": len(results),
        "migrated": migrated,
        "up_to_date": up_to_date,
        "errors": errors,
        "results": results
    }


if __name__ == "__main__":
    print("🔧 Script de Migration des Configurations Purity Bot")
    print("Développé par Celentroft\n")
    
    # Migration
    result = migrate_all_configs()
    
    print("\n" + "="*60)
    if result["status"] == "completed" and result["errors"] == 0:
        print("✅ Migration terminée avec succès!")
    elif result["status"] == "completed":
        print("⚠️  Migration terminée avec des erreurs!")
    else:
        print("❌ Migration échouée!")
    print("="*60)
    
    print("\n💡 Les backups sont dans le dossier './migration_backups'")
    print("💡 En cas de problème, vous pouvez restaurer les backups manuellement\n")

