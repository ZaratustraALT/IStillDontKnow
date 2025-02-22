# gu_data.py

objects = {
    # --------------------
    # Level 1 Gu
    # --------------------
    "Moonlight Gu": {
        "name": "Moonlight Gu",
        "color": "#c0c3f2",
        "level": 1,
        "effect": "Creates a small crescent blade of light that can be shot at high speeds to distances up to 5 meters, causing good damage with its cutting power.",
        "recipe": [],
        "fusions": ["Moonglow Gu", "Moonscar Gu", "Moonwhirl Gu"],
        "affinity": "Moon",
        "family": "Moon Gu"
    },
    "Little Light Gu": {
        "name": "Little Light Gu",
        "color": "#eeeeff",
        "level": 1,
        "effect": "Creates a small amount of concentrated light.",
        "recipe": [],
        "fusions": ["Moonglow Gu"],
        "affinity": "Light",
        "family": "???"
    },
    "Liquor Worm Gu": {
        "name": "Liquor Worm Gu",
        "color": "#ffefee",
        "level": 1,
        "effect": "Allows the user to refine their first level green copper primeval essence to a small tier above.",
        "recipe": [],
        "fusions": ["Moon Harbinger Gu"],
        "affinity": "Water",
        "family": "Liquor Gu"
    },
    "Jade Skin Gu": {
        "name": "Jade Skin Gu",
        "color": "#00a86b",
        "level": 1,
        "effect": "Generates a dim jade-like aura around the user's body that enhances his physical durability.",
        "recipe": [],
        "fusions": ["Moonglow Gu", "White Jade Gu"],
        "affinity": "Earth",
        "family": "Skin Gu"
    },
    "Black Boar Gu": {
        "name": "Black Boar Gu",
        "color": "#312d3d",
        "level": 1,
        "effect": "Provides the strength of one boar to the user permanently.",
        "recipe": [],
        "fusions": ["Black Mane Gu"],
        "affinity": "Life",
        "family": "Boar Gu"
    },
    "White Boar Gu": {
        "name": "White Boar Gu",
        "color": "#f9f0db",
        "level": 1,
        "effect": "Provides the strength of one boar to the user permanently.",
        "recipe": [],
        "fusions": ["White Jade Gu"],
        "affinity": "Life",
        "family": "Boar Gu"
    },
    "Green Silk Gu": {
        "name": "Green Silk Gu",
        "color": "#a4d0bc",
        "level": 1,
        "effect": "Enhances the user’s capillary growth one-hundred fold.",
        "recipe": [],
        "fusions": ["Black Mane Gu"],
        "affinity": "Life",
        "family": "???"
    },
    "Scar Rock Gu": {
        "name": "Scar Rock Gu",
        "color": "#edebe7",
        "level": 1,
        "effect": "???",
        "recipe": [],
        "fusions": ["Moonscar Gu"],
        "affinity": "Earth",
        "family": "???"
    },
    "Whirlwind Gu": {
        "name": "Whirlwind Gu",
        "color": "#c7f0d7",
        "level": 1,
        "effect": "Creates a small current of spinning wind under the user’s control.",
        "recipe": [],
        "fusions": ["Moonglow Gu"],
        "affinity": "Wind",
        "family": "???"
    },
    "Stealth Rock Gu": {
        "name": "Stealth Rock Gu",
        "color": "#d5d1cb",
        "level": 1,
        "effect": "Allows the user to conceal their body visually, but not their clothes or items.",
        "recipe": [],
        "fusions": ["Stealth Scale Gu"],
        "affinity": "Light",
        "family": "???"
    },
    "Fish Scale Gu": {
        "name": "Fish Scale Gu",
        "color": "#2da0c6",
        "level": 1,
        "effect": "???",
        "recipe": [],
        "fusions": ["Stealth Scale Gu"],
        "affinity": "Water",
        "family": "Water Stream Gu"
    },

    # --------------------
    # Level 2 Gu
    # --------------------
    "Black Mane Gu": {
        "name": "Black Mane Gu",
        "color": "#1a0e14",
        "level": 2,
        "effect": "Grows a dense layer of human hair atop the user’s skin that serves as extremely flexible armor.",
        "recipe": ["Black Boar Gu", "Green Silk Gu"],
        "fusions": ["Steel Mane Gu"],
        "affinity": "Life",
        "family": "???"
    },
    "Moonglow Gu": {
        "name": "Moonglow Gu",
        "color": "#5b5eb1",
        "level": 2,
        "effect": "Creates a crescent blade of light that can be shot at high speeds to distances up to 5 meters, causing severe damage with its cutting power. A significant increase in power.",
        "recipe": ["Moonlight Gu", "Little Light Gu", "Little Light Gu"],
        "fusions": ["Golden Moon Gu", "Frost Moon Gu", "Illusory Moon Gu", "Blood Moon Gu"],
        "affinity": "Moon & Light",
        "family": "Moon Gu"
    },
    "White Jade Gu": {
        "name": "White Jade Gu",
        "color": "#d2f1e8",
        "level": 2,
        "effect": "Generates a dim white-jade like aura around the user's body that greatly enhances his physical durability.",
        "recipe": ["White Boar Gu", "Jade Skin Gu", "A Boar’s Tusk"],
        "fusions": ["White Jade Ginseng Gu", "Sky Canopy Gu"],
        "affinity": "Earth & Light",
        "family": "???"
    },
    "Moon Raiment Gu": {
        "name": "Moon Raiment Gu",
        "color": "#33539f",
        "level": 2,
        "effect": "Generates a dim sapphire and silky aura around the user's body in the form of floating robes that are capable of dispersing the force of physical attacks.",
        "recipe": ["Moonlight Gu", "Jade Skin Gu", "Pieces of Jade", "Natural Moonlight"],
        "fusions": [],
        "affinity": "Light",
        "family": "Moon Gu"
    },
    "Moonscar Gu": {
        "name": "Moonscar Gu",
        "color": "#dddbf8",
        "level": 2,
        "effect": "Creates a crescent blade of light that can be shot at high speeds to distances up to 10 meters, causing damage with its cutting power. A significant increase in range.",
        "recipe": ["Moonlight Gu", "Scar Rock Gu"],
        "fusions": [],
        "affinity": "Moon",
        "family": "Moon Gu"
    },
    "Moonwhirl Gu": {
        "name": "Moonwhirl Gu",
        "color": "#bbffdd",
        "level": 2,
        "effect": "Creates a crescent blade of green light that can be shot at high speeds to distances up to 5 meters, causing damage with its cutting power. This projectile can make curved paths when gliding through the air.",
        "recipe": ["Moonlight Gu", "Whirlwind Gu"],
        "fusions": [],
        "affinity": "Moon & Wind",
        "family": "Moon Gu"
    },
    "Moon Harbinger Gu": {
        "name": "Moon Harbinger Gu",
        "color": "#8b74cb",
        "level": 2,
        "effect": "???",
        "recipe": ["Liquor Worm Gu", "???"],
        "fusions": ["Seven Fragrances Liquor Worm"],
        "affinity": "Moon",
        "family": "Moon Gu"
    },
    "Four Flavors Liquor Worm Gu": {
        "name": "Four Flavors Liquor Worm Gu",
        "color": "#f4e8f8",
        "level": 2,
        "effect": "Allows the user to refine their second level red iron primeval essence to a small tier above.",
        "recipe": ["Liquor Worm Gu", "Liquor Worm Gu", "Spicy Wine", "Sweet Wine", "Sour Wine", "Bitter Wine"],
        "fusions": ["Seven Fragrances Liquor Worm"],
        "affinity": "Water",
        "family": "Liquor Gu"
    },
    "Stone Scales Gu": {
        "name": "Stone Scales Gu",
        "color": "#dbd6e3",
        "level": 2,
        "effect": "Allows the user to flicker out of sight of any living being, making not only themselves but also their clothes and others in their hold.",
        "recipe": ["Stealth Rock Gu", "Fish Scale Gu"],
        "fusions": [],
        "affinity": "Earth",
        "family": "???"
    },
    "Blood Essence Gu": {
        "name": "Blood Essence Gu",
        "color": "#a00909",
        "level": 2,
        "effect": "Allows the user to convert his primeval essence into his own blood, diminishing any blood loss effect.",
        "recipe": ["???"],
        "fusions": ["Blood Moon Gu"],
        "affinity": "Life",
        "family": "???"
    },
    "Water Shield Gu": {
        "name": "Water Shield Gu",
        "color": "#4f92e8",
        "level": 2,
        "effect": "Creates a stream of water vapor that, when blown through the user’s nostrils, forms a watery bubble capable of dispersing the force of enemy attacks.",
        "recipe": ["???"],
        "fusions": ["Sky Canopy Gu"],
        "affinity": "Water",
        "family": "???"
    },

    # --------------------
    # Level 3 Gu
    # --------------------
    "Seven Fragrances Liquor Worm Gu": {
        "name": "Seven Fragrances Liquor Worm Gu",
        "color": "#fcd7e8",
        "level": 3,
        "effect": "Allows the user to refine their third level white silver primeval essence to a small tier above.",
        "recipe": ["Moon Harbinger Gu", "???", "Four Flavors Liquor Worm Gu", "???"],
        "fusions": [],
        "affinity": "Water",
        "family": "Liquor Gu"
    },
    "Golden Moon Gu": {
        "name": "Golden Moon Gu",
        "color": "#ffcc66",
        "level": 3,
        "effect": "Creates a big crescent blade of golden light that can be shot at high speeds to distances up to 5 meters, causing brutal damage with its cutting power. An enormous increase in destructive power.",
        "recipe": ["Moonglow Gu", "???"],
        "fusions": [],
        "affinity": "Moon",
        "family": "Moon Gu"
    },
    "Sky Canopy Gu": {
        "name": "Sky Canopy Gu",
        "color": "#87cefa",
        "level": 3,
        "effect": "Generates a white-sky like aura around the user's body that makes them impervious to most physical attacks.",
        "recipe": ["White Jade Gu", "Water Shield Gu", "Aqua Defense"],
        "fusions": [],
        "affinity": "Water, Light & Earth",
        "family": "???"
    },
    "Frost Moon Gu": {
        "name": "Frost Moon Gu",
        "color": "#eeeeff",
        "level": 3,
        "effect": "Creates a crescent blade of light that can be shot at high speeds to distances up to 5 meters, causing severe damage with its cutting power. Cuts made by this Gu are infused with freezing energy capable of slowing movements and dropping body temperature.",
        "recipe": ["Moonglow Gu", "???"],
        "fusions": [],
        "affinity": "Moon & Ice",
        "family": "Moon Gu"
    },
    "Illusory Moon Gu": {
        "name": "Illusory Moon Gu",
        "color": "#c8a2c8",
        "level": 3,
        "effect": "Allows the user to create an illusory copy of himself that fools enemies without a detection-type Gu.",
        "recipe": ["Moonglow Gu", "???"],
        "fusions": ["Moonshadow Gu"],
        "affinity": "Moon & Darkness",
        "family": "Moon Gu"
    },
    "Blood Moon Gu": {
        "name": "Blood Moon Gu",
        "color": "#880808",
        "level": 3,
        "effect": "Creates a crescent blade of crimson light that can be shot at high speeds to distances up to 5 meters, causing severe damage and inducing profuse bleeding.",
        "recipe": ["Moonglow Gu", "Blood Essence Gu"],
        "fusions": [],
        "affinity": "Moon & Life",
        "family": "Moon Gu"
    },

    # --------------------
    # Level 4 Gu
    # --------------------
    "Moonshadow Gu": {
        "name": "Moonshadow",
        "color": "#7051d9",
        "level": 4,
        "effect": "Allows the user to infect another Gu Master with this insidious worm, reducing the maximum amount of primeval essence available (reductions vary by rank).",
        "recipe": ["Illusory Moon Gu", "???"],
        "fusions": [],
        "affinity": "Light",
        "family": "Moon Gu"
    }
}
