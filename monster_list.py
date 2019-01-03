monsters = [
  {
    "name": "Goblin",
    "level": 1,
    "hd": 4,
    "atk": 2,
    "ac": 2,
    "type": "humanoid",
    "atk_type": "slash",
    "resist": "none"
  },
  {
    "name": "Kobold",
    "level": 1,
    "hd": 3,
    "atk": 3,
    "ac": 1,
    "type": "humanoid",
    "atk_type": "pierce",
    "resist": "none"
  },
  {
    "name": "Dog",
    "level": 1,
    "hd": 2,
    "atk": 4,
    "ac": 2,
    "type": "animal",
    "atk_type": "pierce",
    "resist": "none"
  },
  {
    "name": "Jelly",
    "level": 1,
    "hd": 5,
    "atk": 1,
    "ac": 4,
    "type": "aberration",
    "atk_type": "acid",
    "resist": "acid"
  },
  {
    "name": "Orc",
    "level": 2,
    "hd": 4,
    "atk": 3,
    "ac": 3,
    "type": "humanoid",
    "atk_type": "blunt",
    "resist": "none"
  },
  {
    "name": "Slime",
    "level": 2,
    "hd": 7,
    "atk": 3,
    "ac": 5,
    "type": "aberration",
    "atk_type": "acid",
    "resist": "acid"
  },
  {
    "name": "Wolf",
    "level": 2,
    "hd": 3,
    "atk": 4,
    "ac": 3,
    "type": "animal",
    "atk_type": "pierce",
    "resist": "none"
  },
  {
    "name": "Imp",
    "level": 2,
    "hd": 2,
    "atk": 5,
    "ac": 1,
    "type": "demon",
    "atk_type": "fire",
    "resist": "fire"
  }
]

descriptors = {
    "humanoid" : [
        "Big",
        "Burly",
        "Massive",
        "Hulking",
        "Monstrous"
    ],
    "animal" : [
        "Wild",
        "Snarling",
        "Vicious",
        "Rabid",
        "Dire"
    ],
    "aberration" : [
        "Weird",
        "Strange",
        "Confusing",
        "Horrifying",
        "Insane"
    ],
    "demon" : [
        "Smoking",
        "Glowing",
        "Flaming",
        "Inferno",
        "Holocaust"
    ]
}

atkVerbs = {
    "humanoid": {
        "slash": [
            "slashes",
            "cuts",
            "hacks"
        ],
        "pierce": [
            "stabs",
            "pokes",
            "impales"
        ]
    },
    "animal": {
        "slash": [
            "claws",
            "rakes",
            "slashes"
        ],
        "pierce": [
            "bites",
            "gnaws",
            "chews"
        ]
    },
    "aberration": {
        "acid": [
            "dissolves",
            "burns",
            "melts"
        ]
    },
    "demon": {
        "fire": [
            "scorches",
            "burns",
            "chars"
        ]
    }
}