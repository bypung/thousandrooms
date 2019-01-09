monsters = [
  {
    "id": 1,
    "name": "Goblin",
    "level": 1,
    "hd": 4,
    "atk": 2,
    "ac": 2,
    "type": "humanoid",
    "subtype": "",
    "atk_type": "slash",
    "resist": "",
    "vulnerability": "",
    "special": ""
  },
  {
    "id": 2,
    "name": "Kobold",
    "level": 1,
    "hd": 3,
    "atk": 3,
    "ac": 1,
    "type": "humanoid",
    "subtype": "",
    "atk_type": "pierce",
    "resist": "",
    "vulnerability": "",
    "special": ""
  },
  {
    "id": 3,
    "name": "Dog",
    "level": 1,
    "hd": 2,
    "atk": 4,
    "ac": 2,
    "type": "animal",
    "subtype": "mammal",
    "atk_type": "pierce",
    "resist": "",
    "vulnerability": "",
    "special": ""
  },
  {
    "id": 4,
    "name": "Jelly",
    "level": 1,
    "hd": 5,
    "atk": 1,
    "ac": 4,
    "type": "aberration",
    "subtype": "",
    "atk_type": "acid",
    "resist": "acid",
    "vulnerability": "electric",
    "special": "melt"
  },
  {
    "id": 5,
    "name": "Skeleton",
    "level": 2,
    "hd": 3,
    "atk": 4,
    "ac": 3,
    "type": "humanoid",
    "subtype": "undead",
    "atk_type": "slash",
    "resist": "slash",
    "vulnerability": "blunt",
    "special": ""
  },
  {
    "id": 6,
    "name": "Orc",
    "level": 2,
    "hd": 4,
    "atk": 3,
    "ac": 3,
    "type": "humanoid",
    "subtype": "",
    "atk_type": "blunt",
    "resist": "",
    "vulnerability": "",
    "special": ""
  },
  {
    "id": 7,
    "name": "Slime",
    "level": 2,
    "hd": 7,
    "atk": 3,
    "ac": 5,
    "type": "aberration",
    "subtype": "",
    "atk_type": "acid",
    "resist": "acid",
    "vulnerability": "electric",
    "special": "melt"
  },
  {
    "id": 8,
    "name": "Wolf",
    "level": 2,
    "hd": 3,
    "atk": 4,
    "ac": 3,
    "type": "animal",
    "subtype": "mammal",
    "atk_type": "pierce",
    "resist": "",
    "vulnerability": "",
    "special": ""
  },
  {
    "id": 9,
    "name": "Imp",
    "level": 2,
    "hd": 2,
    "atk": 5,
    "ac": 1,
    "type": "demon",
    "subtype": "",
    "atk_type": "fire",
    "resist": "fire",
    "vulnerability": "cold",
    "special": "burn"
  },
  {
    "id": 10,
    "name": "Gnoll",
    "level": 3,
    "hd": 4,
    "atk": 4,
    "ac": 3,
    "type": "humanoid",
    "subtype": "",
    "atk_type": "blunt",
    "resist": "",
    "vulnerability": "",
    "special": ""
  },
  {
    "id": 11,
    "name": "Zombie",
    "level": 3,
    "hd": 6,
    "atk": 2,
    "ac": 4,
    "type": "humanoid",
    "subtype": "undead",
    "atk_type": "blunt",
    "resist": "cold",
    "vulnerability": "fire",
    "special": ""
  },
  {
    "id": 12,
    "name": "Python",
    "level": 3,
    "hd": 4,
    "atk": 4,
    "ac": 4,
    "type": "animal",
    "subtype": "reptile",
    "atk_type": "grab",
    "resist": "",
    "vulnerability": "",
    "special": ""
  },
  {
    "id": 13,
    "name": "Spectre",
    "level": 4,
    "hd": 5,
    "atk": 5,
    "ac": 3,
    "type": "humanoid",
    "subtype": "undead",
    "atk_type": "slash",
    "resist": "",
    "vulnerability": "",
    "special": "drain"
  },
  {
    "id": 14,
    "name": "Griffon",
    "level": 4,
    "hd": 4,
    "atk": 6,
    "ac": 3,
    "type": "animal",
    "subtype": "",
    "atk_type": "slash",
    "resist": "",
    "vulnerability": "",
    "special": ""
  },
  {
    "id": 15,
    "name": "Ogre",
    "level": 4,
    "hd": 6,
    "atk": 6,
    "ac": 4,
    "type": "humanoid",
    "subtype": "",
    "atk_type": "blunt",
    "resist": "",
    "vulnerability": "",
    "special": ""
  },
  {
    "id": 16,
    "name": "Quasit",
    "level": 4,
    "hd": 3,
    "atk": 4,
    "ac": 6,
    "type": "demon",
    "subtype": "",
    "atk_type": "pierce",
    "resist": "",
    "vulnerability": "",
    "special": ""
  },
  {
    "id": 17,
    "name": "Ooze",
    "level": 4,
    "hd": 7,
    "atk": 2,
    "ac": 4,
    "type": "aberration",
    "subtype": "",
    "atk_type": "acid",
    "resist": "electric",
    "vulnerability": "fire",
    "special": "melt"
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
    "reptile" : [
        "Hissing",
        "Lurking",
        "Vicious",
        "Striking",
        "Dire"
    ],
    "undead" : [
        "Spooky",
        "Moaning",
        "Rotting",
        "Wailing",
        "Eternal"
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
        ],
        "blunt": [
            "bashes",
            "smashes",
            "crushes"
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
        ],
        "grab": [
            "grabs",
            "squeezes",
            "crushes"
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
        ],
        "slash": [
            "slashes",
            "cuts",
            "hacks"
        ],
        "pierce": [
            "stabs",
            "pokes",
            "impales"
        ],
        "blunt": [
            "bashes",
            "smashes",
            "crushes"
        ]
    }
}