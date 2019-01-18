class MonsterList:
    monsters = [
    {
        "id": 1,
        "name": "Goblin",
        "level": 1,
        "hd": 4,
        "atk": 2,
        "ac": 2,
        "total": 8,
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
        "total": 7,
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
        "total": 8,
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
        "total": 10,
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
        "total": 10,
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
        "total": 10,
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
        "total": 15,
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
        "total": 10,
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
        "hd": 3,
        "atk": 5,
        "ac": 3,
        "total": 11,
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
        "total": 11,
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
        "hd": 7,
        "atk": 3,
        "ac": 5,
        "total": 15,
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
        "hd": 5,
        "atk": 5,
        "ac": 5,
        "total": 15,
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
        "hd": 6,
        "atk": 6,
        "ac": 4,
        "total": 16,
        "type": "humanoid",
        "subtype": "undead",
        "atk_type": "touch",
        "resist": "",
        "vulnerability": "",
        "special": "drain"
    },
    {
        "id": 14,
        "name": "Griffon",
        "level": 4,
        "hd": 5,
        "atk": 7,
        "ac": 4,
        "total": 16,
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
        "hd": 7,
        "atk": 7,
        "ac": 5,
        "total": 19,
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
        "hd": 4,
        "atk": 5,
        "ac": 7,
        "total": 16,
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
        "hd": 8,
        "atk": 3,
        "ac": 5,
        "total": 16,
        "type": "aberration",
        "subtype": "",
        "atk_type": "acid",
        "resist": "electric",
        "vulnerability": "fire",
        "special": "melt"
    },
    {
        "id": 18,
        "name": "Spider",
        "level": 5,
        "hd": 6,
        "atk": 8,
        "ac": 7,
        "total": 21,
        "type": "animal",
        "subtype": "insect",
        "atk_type": "pierce",
        "resist": "pierce",
        "vulnerability": "fire",
        "special": "drain"
    },
    {
        "id": 19,
        "name": "Shambler",
        "level": 5,
        "hd": 7,
        "atk": 8,
        "ac": 5,
        "total": 20,
        "type": "aberration",
        "subtype": "",
        "atk_type": "blunt",
        "resist": "fire",
        "vulnerability": "slash",
        "special": ""
    },
    {
        "id": 20,
        "name": "Wraith",
        "level": 5,
        "hd": 5,
        "atk": 8,
        "ac": 11,
        "total": 24,
        "type": "humanoid",
        "subtype": "undead",
        "atk_type": "cold",
        "resist": "cold",
        "vulnerability": "electric",
        "special": "drain"
    },
    {
        "id": 21,
        "name": "Werewolf",
        "level": 5,
        "hd": 6,
        "atk": 8,
        "ac": 7,
        "total": 21,
        "type": "animal",
        "subtype": "mammal",
        "atk_type": "slash",
        "resist": "blunt",
        "vulnerability": "",
        "special": ""
    },
    {
        "id": 22,
        "name": "Drake",
        "level": 5,
        "hd": 9,
        "atk": 8,
        "ac": 9,
        "total": 26,
        "type": "dragon",
        "subtype": "",
        "atk_type": "slash",
        "resist": "fire",
        "vulnerability": "cold",
        "special": "burn"
    },
    {
        "id": 23,
        "name": "Gremlin",
        "level": 6,
        "hd": 7,
        "atk": 9,
        "ac": 8,
        "total": 24,
        "type": "demon",
        "subtype": "",
        "atk_type": "acid",
        "resist": "fire",
        "vulnerability": "blunt",
        "special": "melt"
    },
    {
        "id": 24,
        "name": "Panther",
        "level": 6,
        "hd": 6,
        "atk": 11,
        "ac": 9,
        "total": 26,
        "type": "animal",
        "subtype": "",
        "atk_type": "slash",
        "resist": "",
        "vulnerability": "",
        "special": ""
    },
    {
        "id": 25,
        "name": "Automaton",
        "level": 6,
        "hd": 10,
        "atk": 8,
        "ac": 8,
        "total": 26,
        "type": "humanoid",
        "subtype": "construct",
        "atk_type": "electric",
        "resist": "blunt",
        "vulnerability": "pierce",
        "special": ""
    },
    {
        "id": 26,
        "name": "Bugbear",
        "level": 6,
        "hd": 8,
        "atk": 10,
        "ac": 9,
        "total": 27,
        "type": "humanoid",
        "subtype": "",
        "atk_type": "blunt",
        "resist": "",
        "vulnerability": "",
        "special": ""
    },
    {
        "id": 27,
        "name": "Crab",
        "level": 7,
        "hd": 8,
        "atk": 10,
        "ac": 12,
        "total": 30,
        "type": "animal",
        "subtype": "insect",
        "atk_type": "slash",
        "resist": "slash",
        "vulnerability": "cold",
        "special": ""
    },
    {
        "id": 28,
        "name": "Lizardman",
        "level": 7,
        "hd": 10,
        "atk": 10,
        "ac": 10,
        "total": 30,
        "type": "humanoid",
        "subtype": "",
        "atk_type": "pierce",
        "resist": "",
        "vulnerability": "",
        "special": ""
    },
    {
        "id": 29,
        "name": "Ghoul",
        "level": 7,
        "hd": 9,
        "atk": 11,
        "ac": 11,
        "total": 31,
        "type": "humanoid",
        "subtype": "undead",
        "atk_type": "slash",
        "resist": "cold",
        "vulnerability": "fire",
        "special": "drain"
    },
    {
        "id": 30,
        "name": "Gargoyle",
        "level": 7,
        "hd": 12,
        "atk": 8,
        "ac": 10,
        "total": 30,
        "type": "humanoid",
        "subtype": "construct",
        "atk_type": "slash",
        "resist": "blunt",
        "vulnerability": "cold",
        "special": ""
    },
    {
        "id": 31,
        "name": "Minotaur",
        "level": 8,
        "hd": 10,
        "atk": 13,
        "ac": 11,
        "total": 34,
        "type": "humanoid",
        "subtype": "",
        "atk_type": "slash",
        "resist": "",
        "vulnerability": "",
        "special": ""
    },
    {
        "id": 32,
        "name": "Bear",
        "level": 8,
        "hd": 11,
        "atk": 13,
        "ac": 7,
        "total": 31,
        "type": "animal",
        "subtype": "",
        "atk_type": "grab",
        "resist": "",
        "vulnerability": "",
        "special": ""
    },
    {
        "id": 33,
        "name": "Golem",
        "level": 8,
        "hd": 12,
        "atk": 12,
        "ac": 12,
        "total": 36,
        "type": "humanoid",
        "subtype": "construct",
        "atk_type": "blunt",
        "resist": "slash",
        "vulnerability": "electric",
        "special": ""
    },
    {
        "id": 34,
        "name": "Shadow",
        "level": 8,
        "hd": 9,
        "atk": 15,
        "ac": 9,
        "total": 33,
        "type": "humanoid",
        "subtype": "undead",
        "atk_type": "touch",
        "resist": "electric",
        "vulnerability": "fire",
        "special": "drain"
    },
    {
        "id": 35,
        "name": "Centaur",
        "level": 9,
        "hd": 12,
        "atk": 14,
        "ac": 13,
        "total": 39,
        "type": "humanoid",
        "subtype": "",
        "atk_type": "slash",
        "resist": "",
        "vulnerability": "",
        "special": ""
    },
    {
        "id": 36,
        "name": "Eagle",
        "level": 9,
        "hd": 11,
        "atk": 16,
        "ac": 14,
        "total": 41,
        "type": "animal",
        "subtype": "bird",
        "atk_type": "pierce",
        "resist": "",
        "vulnerability": "",
        "special": ""
    },
    {
        "id": 37,
        "name": "Yeti",
        "level": 9,
        "hd": 15,
        "atk": 13,
        "ac": 13,
        "total": 41,
        "type": "humanoid",
        "subtype": "",
        "atk_type": "blunt",
        "resist": "cold",
        "vulnerability": "fire",
        "special": "freeze"
    },
    {
        "id": 38,
        "name": "Wyvern",
        "level": 9,
        "hd": 13,
        "atk": 15,
        "ac": 14,
        "total": 42,
        "type": "dragon",
        "subtype": "",
        "atk_type": "pierce",
        "resist": "",
        "vulnerability": "",
        "special": "drain"
    },
    {
        "id": 39,
        "name": "Ghost",
        "level": 10,
        "hd": 13,
        "atk": 15,
        "ac": 17,
        "total": 45,
        "type": "humanoid",
        "subtype": "undead",
        "atk_type": "touch",
        "resist": "slash",
        "vulnerability": "",
        "special": "drain"
    },
    {
        "id": 40,
        "name": "Giant",
        "level": 10,
        "hd": 15,
        "atk": 15,
        "ac": 15,
        "total": 45,
        "type": "humanoid",
        "subtype": "",
        "atk_type": "blunt",
        "resist": "",
        "vulnerability": "",
        "special": ""
    },
    {
        "id": 41,
        "name": "Wyrm",
        "level": 10,
        "hd": 14,
        "atk": 16,
        "ac": 16,
        "total": 46,
        "type": "dragon",
        "subtype": "",
        "atk_type": "fire",
        "resist": "pierce",
        "vulnerability": "cold",
        "special": "burn"
    },
    {
        "id": 42,
        "name": "Horror",
        "level": 10,
        "hd": 17,
        "atk": 13,
        "ac": 15,
        "total": 45,
        "type": "aberration",
        "subtype": "",
        "atk_type": "grab",
        "resist": "fire",
        "vulnerability": "electric",
        "special": "drain"
    },
    {
        "id": 43,
        "name": "Death Knight",
        "level": 11,
        "hd": 15,
        "atk": 18,
        "ac": 16,
        "total": 49,
        "type": "humanoid",
        "subtype": "undead",
        "atk_type": "slash",
        "resist": "",
        "vulnerability": "",
        "special": "freeze"
    },
    {
        "id": 44,
        "name": "Hydra",
        "level": 11,
        "hd": 16,
        "atk": 18,
        "ac": 12,
        "total": 46,
        "type": "animal",
        "subtype": "reptile",
        "atk_type": "pierce",
        "resist": "slash",
        "vulnerability": "fire",
        "special": ""
    },
    {
        "id": 45,
        "name": "Titan",
        "level": 11,
        "hd": 17,
        "atk": 17,
        "ac": 17,
        "total": 51,
        "type": "humanoid",
        "subtype": "",
        "atk_type": "slash",
        "resist": "",
        "vulnerability": "",
        "special": ""
    },
    {
        "id": 46,
        "name": "Demon",
        "level": 11,
        "hd": 14,
        "atk": 20,
        "ac": 14,
        "total": 48,
        "type": "demon",
        "subtype": "",
        "atk_type": "pierce",
        "resist": "fire",
        "vulnerability": "acid",
        "special": "burn"
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
        "insect" : [
            "Shiny",
            "Chittering",
            "Gangly",
            "Chitinous",
            "Looming"
        ],
        "undead" : [
            "Spooky",
            "Moaning",
            "Rotting",
            "Wailing",
            "Eternal"
        ],
        "construct" : [
            "Wooden",
            "Clay",
            "Stone",
            "Iron",
            "Crystal"
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
        ],
        "dragon" : [
            "Young",
            "Mature",
            "Gleaming",
            "Ancent",
            "Elder"
        ]
    }

    bossDescriptors = {
        "humanoid" : [
            ("", "King"),
            ("Mighty", "Warrior"),
            ("Ultimate", "")
        ],
        "animal" : [
            ("Prehistoric", ""),
            ("Legendary", ""),
            ("", "of the Wildlands")
        ],
        "reptile" : [
            ("Enormous", ""),
            ("Cthonic", ""),
            ("Fanged", "")
        ],
        "insect" : [
            ("", "Queen"),
            ("Emerald", ""),
            ("Winged", "")
        ],
        "undead" : [
            ("", "Lord"),
            ("Unholy", ""),
            ("", "of Nightmares")
        ],
        "aberration" : [
            ("Royal", ""),
            ("Great Old", ""),
            ("", "That Never Sleeps")
        ],
        "demon" : [
            ("Noble", "of Dis"),
            ("Damned", ""),
            ("", "Torturer")
        ],
        "dragon" : [
            ("Mother", ""),
            ("Golden-Winged", ""),
            ("Black", "of the Pit")
        ]
    }

    bossQuotes = {
        "humanoid" : [
            '"You\'ll never survive me!"',
            '"I\'m your worst nightmare!"',
            '"Come a little closer..."'
        ],
        "animal" : [
            "It roars a challenge!",
            "The ground shakes as it stomps toward you!"
            "You feel its eyes on you..."
        ],
        "insect" : [
            "Venom drips from its fangs!",
            "It chitters menacingly...",
            "It gathers itself to strike..."
        ],
        "undead" : [
            '"Join me in the world beyond life!"',
            "Its eyes glow with a cold light...",
            '"Life is wasted on the living!"'
        ],
        "construct" : [
            'Gears grind within its body...',
            "Lifeless eyes track your movement...",
            'It relentlessly pursues you!'
        ],
        "aberration" : [
            "It contorts weirdly...",
            "You see unnatural shapes in its surface...",
            "It surges toward you!"
        ],
        "demon" : [
            '"The underworld awaits!"',
            '"Time to pay for your sins!"',
            '"Feel the flames of the Abyss!"'
        ],
        "dragon" : [
            '"You look tasty..."',
            "It coils itself, ready to attack!",
            '"My treasures are mine alone!"'
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
            ],
            "touch": [
                "touches",
                "grips",
                "gropes"
            ],
            "cold": [
                "freezes",
                "chills",
                "frosts"
            ],
            "electric": [
                "zaps",
                "shocks",
                "jolts"
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
            ],
            "grab": [
                "engulfs",
                "smothers",
                "grapples"
            ],
            "blunt": [
                "slams",
                "stomps",
                "mangles"
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
        },
        "dragon": {
            "fire": [
                "scorches",
                "burns",
                "chars"
            ],
            "slash": [
                "claws",
                "rakes",
                "slashes"
            ],
            "pierce": [
                "impales",
                "stings",
                "bites"
            ]
        }
    }