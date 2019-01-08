monsters = [
  {
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
        ]
    }
}