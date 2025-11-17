configuration = {
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
        "claim": True,
        "buttons": {},
        "categories": {
            "nouveaux": None,
            "pris_en_charge": None,
            "en_pause": None,
            "fermes": None
        }
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
            "active": False,
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
    }
}