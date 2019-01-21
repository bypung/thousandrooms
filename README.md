# Dungeon of a Thousand Rooms

This is a simple Rogue-like RPG written as an exercise in teaching myself Python. It was written using Python 3.7.2.

## Installation

The easiest way to install is using pip:

```
pip install thousandrooms
```

The game was designed for a 80 x 24 terminal, with white text on a black background (and vice versa). Other sizes and default colors may be suboptimal. Colors are likely not to work on Windows based terminals, sorry!

## The Game

The goal of the game is to get to the bottom level of the dungeon, retrieve the Idol of Onekrum, and return to the surface alive. You will face monsters in every room, with stronger monsters guarding each set of stairs down to the next level. Additionally, all the monsters in the dungeon will gain in strength over time, so speed is of the essence!

Once you retrieve the Idol, all rooms will fill with monsters again, but at least you know the way out...

## Actions

### The Beginning

Every great legend starts somewhere. Yours starts here.

##### Load
Load a previously saved game. There may be more than one adventurer saved, so make sure you pick the right one!

##### New
Start a brand new adventure. You will be able to choose your hero's name. 

You can also choose to start in Ironman mode, which will not allow you to restore a saved game if you die. Your game will also not be saved if you kill the program or it crashes, so be careful!

### An Empty Room

A room without a monster is a peaceful place. You can use this time to do a nummber of things:

##### Inventory
Manage your equipment and other items. Some items can only be used outside of combat. Examining your inventory and equipping items takes no time. Using an item takes one turn, unless otherwise specified.

##### Merchant
Take a trip back up to the surface to buy and sell items. Every time you visit the store it will have a new selection of items appropriate to the current difficulty level of the dungeon. This trip will take 10 turns for every level you have descended in the dungeon. After you retrieve the Idol, rampaging monsters will block the path to the surface.

##### Rest
Take a break and bandage your wounds. Resting will heal all of your injuries, but the more you heal, the more turns you will spend resting.

##### Continue
Journey deeper into the dungeon! This will open the map and allow you to choose your next destination.

##### Save
Put a bookmark in the tale of your adventure. This will always overwrite your previous save. You will then be able to either continue your journey or quit for now.

##### Quit
Stop playing. Be sure to save first!

### Your Inventory

##### Equip
You can equip one weapon, one armor, and one ring at any given time. Choose wisely! Some weapons may be more effective against certain monsters.

##### Use
Items like scrolls and potions may be used to produce magical effects. Some may not be work outside of combat.

##### Filter
If you have a lot of items, you can filter the list to just a certain type of item to make them easier to find.

##### Next, Previous, and Close
You an flip through the pages of your inventory or close it and journey onward.

### The Map

The map will show you places you've been, as well as places you are aware of but haven't visited yet.

##### North, South, West, East, Up, Down
You can move in any direction where there is an available door or stair. Moving takes only one turn.

##### Listen
After spending three turns listening, you may be able to detect unseen monsters in adjacent rooms. The more lore you have collected about monsters in the dungeon, the more likely you are to recognize the noises.

##### Back
Close the map and return to the current room.

### Combat!

There are many fierce monsters standing between you and your goal. You don't have to fight them all, but you may need the experience and treasure you gain to be ready for the guardians of the stairs to lower levels.

Whatever action you take during combat, the monster you are facing will be able to attack you (unless your action is escaping). The monster may also prepare for a special attack the next turn, so pay attention!

##### Attack
Attacking the monster takes one turn. If your weapon is more or less effective than normal, you will be alerted to that fact and it will be automatically added to the lore you know about the creature.

##### Defend
If the monster is going to use its special attack against you, you may want to spend a turn defending yourself instead. This will greatly increase your chances of not being struck by the attack. If you think you can kill the monster before it gets a chance to strike (or you think that your nromal defense is good enough) you may forego this sensible action.

##### Xamine
You may spend a turn studying your opponent to learn its strengths and weaknesses. Each turn spent this way will five you one piece of information. The monster will still attack, so be careful!

##### Use Item
Some items are usable during combat, whether for attack, healing, or escape. As usual, using an item will cost you one turn.

##### Run
Often discretion is the better part of valor, especially if you realize that your current weapon is not well suited for the monster you need to defeat. Running away will cost you ten turns, and the monster will heal a quarter of its maximum health in the meantime.

## Items

There are many items that you will find in the dungeon or for sale in the store. You may also sell items you no longer need to the merchant.

### Weapons
Weapons come in three main varieties: slashing, pieercing, and blunt. Each type may be strong or weak against some opponents, so it behooves you to maintain a variety of weapons. Some rare weapons may have an elemental enchantment that changes the type of damage the weapon does as well as increasing it. Other rare weapons may simply do far more damage than normal. Weapons are vulnerable to being destroyed by acid attacks.

### Armor
Armor may be made of cloth, leather, or metal, and some rare armors may give special benefits or elemntal resistances. Cloth and leather armors are susceptible to destruction by fire, while metal armors are vulnerable to acid.

### Rings
Rings give a variety of special effects when worn. Only one ring may be worn at a time. Rings may be destroyed by acid.

### Equipped Item Effects

##### Shielding
This ring augments the defensive bonus of your armor.

##### Traveling
This effect increases your walking speed; sometimes moving between rooms will not cost you a turn. It also decreases the amount of time it takes to return to the store.

##### Running
Sometimes retreat is the best option. This effect reduces the turn cost of running away from a fight, and the escaped monster regains less of its health. Both rings and armor may give this effect.

##### Regeneration
Healing takes less time when this effect is active. This effect is usually found on rings, but sometimes on rare armors.

### Usable Items

There are a variety of single use items that may save you time and effort, or may even save your life. Use them wisely, for they may make the difference between victory and defeat!

##### Potion of Healing
This drink will instantly heal half of your maximim health. It can be used in or out of combat, though when used in combat the monster will still get to attack you again.

##### Scroll of Digging
Sometimes the stairs to the next level are in a section of the dungeon that does not connect to the point where you came in. Sometimes you just want to take a shortcut. In either case, the magic of this scroll will make a door where there was none before. Only usable out of combat.

##### Scroll of Blinking
Reading this scroll will magically transport you to a room within two rooms of your current location, which can be good for exploring disconnected areas or a quick escape from a fight. If there is a monster in the room where you appear, it will immediately attack!

##### Scroll of Teleport
This scroll will also magically transport you, but in a direction of your choosing. Similarly, you may find yourself under attack in your new location.

##### Potion of Invisibility
When quaffed during combat, this potion will allow you to slip back the way you came without incurring a turn penalty or allowing the monster to heal.

##### Scroll of Shopping
Reading this scroll will instantly transport you to the merchant on the surface, as well as giving you a little extra pocket change to spend when you get there. When you finish shopping it will also transport you back where you came from.

##### Scroll of Time Warp
If you have spent more time than you would like exploring the dungeon, this scroll will turn back the clock, giving you a little more time before things get more difficult.

##### Scroll of Fireball
This scroll delivers a blast of fire to the monster you are facing. Keep in mind that some monsters are resistant to fire...

##### Potion of Knowledge
If you want to take the shortest path to the next level, this potion will extend your consciousness and reveal the stairs to you. Unfortunately, it will also reveal you to the monsters, causing them to become more powerful sooner.

