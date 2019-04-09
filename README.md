# DiscworldMUD-TinTin

Created by [Ruhsbaar](http://discworld.starturtle.net/lpc/secure/finger.c?player=ruhsbaar) of the Venerable Council of Seers.

## Overview
A collection of configurations and scripts for use with [DiscworldMUD](http://discworld.starturtle.net) in the [TinTin++](https://tintin.sourceforge.io) MUD client. Many features are meant to be run in their own "miniwindow" for which I make liberal use of Tmux panes. 

For reference, I host this configuration on a Linux VPS and thus am able to "take over" the Tmux session as I move between devices/lose internet without being disconnected from the game. This may help to explain some decisions made.

![Screenshot](https://i.imgur.com/WVZaQwn.png)


## Features and Bits


### Windows

* Chat Monitor
* Map Door Text parser
* Hotspot timers
* Group shield monitor
* ASCII map

### Commands and Scripts

#### Dead Letter Solver
* Command: `sl`
* File: `src/deadletter.tin`

Read a letter in your inventory and print a solution, with the term to scry highlighted. Mostly uses the data from the Dead Letters page on the [wiki](https://dwwiki.mooo.com/wiki/Dead_letter_office_jobs). Works only for **difficult customers** and **distant lands**.

#### Prompt: TPA/XP/Quota Monitor
* Files: `src/prompt.tin`, `src/xpmonitor.tin`, `src/tpamonitor.tin`, `src/quota.tin`

A tintin++ split across the top of the MUD window proper that displays a few bits of information:
1) How long has the session been running
2) How much XP you've earned total this session
3) The average XP/hour rate over that time
4) Do you have a TPA active
5) What colour is your TPA currently
6) How long until quota flips (appears if relevant)
7) Quota timer is coloured when in the last hour
8) In-game alerts for 1 hour, 30m, 10m left of quota

#### Map Door Text GMCP Parser
* Files: `src/mdtparse.py`, `mdtconfig.json`, `src/gmcp.tin`
* Blatantly copied from [Quow's](http://quow.co.uk) wonderful work for his MUSHclient configs.

This python script (`src/mdtparse.py`) parses the mapdoortext data delivered by GMCP as you move rooms and displays a nice formatted list. Customizable with a configuration file (`mdtconfig.json`) that allows for picking out particular NPCs, assigning them point values, and colouring.

#### Item/NPC/Room Search
* Files: `src/db.tin`
* Made possible by [Quow's](http://quow.co.uk) fantastic data collection and publicly available database.

A series of TinTin aliases that invoke SQLite to search through Quow's database and retrieve various information about game items, people and places.

##### Item Search
> `db item sword`, `db npcitem sword`
```
Results for items matching "sword":
  [0]: sword necklace (A$4.25) found in occult jewellery stall, Ankh-Morpork
  [1]: short sword (2,66Gl) found in dwarfish blacksmith's, Genua
  [2]: long sword (4,0Gl) found in dwarfish blacksmith's, Genua
  [3]: bastard sword (20Rh 100s) found in illegal contraband stall, Bes Pelargic
  [4]: double-edged broad sword (A$112.50) found in weapon shop, Ankh-Morpork
  [5]: watered-steel long sword (A$180) found in weapon shop, Ankh-Morpork
  [6]: rose-hilted long sword (A$180) found in weapon shop, Ankh-Morpork
  [7]: heavy sword [build-a-bear] (8Rh 60s) found in Assemble an Animal Workshop, Bes Pelargic
  [8]: short sword [build-a-bear] (8Rh 60s) found in Assemble an Animal Workshop, Bes Pelargic
  [9]: short sword scabbard (A$1) found in Sartorn and Son Scabbard Store, Ankh-Morpork
```

The "item" keyword is searching shops, while "npcitem" searches NPC inventories.

##### NPC Search
> `db npc villager`
```
Results for NPCs matching "villager".
  [0]: villager [Hillshire] found in road running through Hillshire, Sto Plains Region
  [1]: bumpkin, local, oaf, peasant, villager, yokel found in commercial side street, Slippery Hollow
  [2]: villager found in western edge of the square, Bois
  [3]: Sheepridge villager found in Sheepridge village square, Sto Plains Region
  [4]: villager found in cobbled road in Blackglass, Uberwald Region
  [5]: villager [ramtop villages] found in road outside of Brass Neck, Ramtops Regions
  [6]: villager [Blackglass] found in cobbled road in Blackglass, Uberwald Region
```

##### Room Search
> `db room launder`
```
Results for rooms matching "launder".
  [0]: launder room (inside) found in AM Thieves
  [1]: launder room (inside) found in Genua Sewers
```

##### Gatherable Spice Search
> `db gatherable thyme`
```
Results for gatherables matching "thyme".
  [0]: some thyme found in garden, Bes Pelargic
  [1]: some thyme found in bottom part of the Temple gardens, Temple of Small Gods
  [2]: some thyme found in conservatory, BP Estates
  [3]: some thyme found in neat herb garden, Ramtops Regions
  [4]: some thyme found in service entrance to the Chronides farmstead, Klatchian Farmsteads
  [5]: some thyme found in northeast garden, Sto Plains Region
  [6]: some thyme found in garden, Ramtops Regions
  [7]: some thyme found in cottage herb garden, Ramtops Regions
```

#### Speedwalking
* Files: `src/maproute.py`, `src/gmcp.tin`, `src/db.tin`
* Route-finding logic and of course the database taken directly from [Quow's](http://quow.co.uk) lovely MUSHclient package.

A python script (`src/maproute.py`) is handed the room_identifier of your current location and of your target location and attempts to create an alias to walk you there. This functionality can be invoked in-game with the `db route #` command, where `#`  is the result number (0-9) that preceeds the results in any of the previously mentioned database search commands (`db item`, `db npc`, `db room`, `db gatherable`)

**Example:**

Here I am at Baldwin's smithy. But I need to make my way to the Mended Drum, let's speedwalk there (very contrived example but short and sweet).
```
[smithy]
    @
    +
This is a small, cramped room with a large, roaring fire blazing in the forge on the east wall of the room.
There are various assorted tools of metalwork scattered around the fire and hanging on the walls, most notably
the anvil in the centre of the room.  The smithy is obviously very busy as there is a large, dirty order book
lying open on a small desk near the door.
There is one obvious exit: south.
A cute goose, a young truffle pig, Baldwin "the Disemboweler" MacAvrik and Baldwin's apprentice are standing
here.
A piece of embroidered tartan is hanging on the wall and two iron chains and a copper short sword are on the
floor.
<unhurt | alert | rather warm | unburdened [25%] | 9626360xp>
```

First lets search for the Mended Drum
> `db room Mended Drum`
```
Results for rooms matching "Mended Drum".
  [0]: north end of Short Street outside the Mended Drum (outside) found in Ankh-Morpork
  [1]: entrance to the Mended Drum (inside) found in AM Buildings
  [2]: bar of the Mended Drum (inside) found in AM Buildings
  [3]: western part of the Mended Drum (inside) found in AM Buildings
  [4]: toilets of the Mended Drum (inside) found in AM Buildings
  [5]: cubicle in the toilets of the Mended Drum (inside) found in AM Buildings
  [6]: cubicle in the toilets of the Mended Drum (inside) found in AM Buildings
  [7]: landing on the first floor in the Mended Drum (inside) found in AM Buildings
  [8]: front wall of the Mended Drum (outside) found in AM Buildings
  [9]: roof of the Mended Drum (outside) found in AM Buildings
```

Great, we got a list of results back. Let's aim for the `entrance to the Mended Drum`, which is result number `1` in our list.

> `db route 1`
```
[speedwalk] Generating speedwalk from current location to entrance to the Mended Drum, AM Buildings...
[speedwalk] A route was found, type "speedwalk" to fast travel.
Changed alias "RuhsSpeedRun" from "nw;nw;w;nw;nw;sw;sw;sw $*$".
<unhurt | fully rested | rather warm | unburdened [25%] | 9626384xp>
alias RuhsSpeedRun
RuhsSpeedRun: s;e;e;n $*$
```

We found a way there, and our speedwalking alias was updated. Now typing `speedwalk` would walk us over to the Mended Drum (s;e;e;n).


#### Hunting Hotspot Timers (with Syncing!)
* File: `src/spottimers.tin`

This set of configs is checking against a list of saved NPCs/Rooms (that I've determined, I think my hunting route is the bestest one, you might disagree, that's good for you) every time we see something die, or enter a new room, and records the time it happened.

```
.:: Death Timers ::.
 - (99m)  delbert
 - (11m)  hlakket
 - (???)  stables
 - (???)  casino
 - (???)  rogues
 - (???)  grflx
 - (32m)  shaker lions
 - (???)  snail
 - (72m)  dojo
 - (22m)  medina boss
 - (???)  zoon liar
 - (???)  bandit leader
 - (???)  cguards
 - (???)  giant leader


.:: Visit Timers ::.
 - (???)  parades
 - (05m)  offler
 - (09m)  shades
 - (37m)  smugglers
 - (???)  black market
```

Output like above is written to a file (so that it can be displayed next to the MUD, I keep it in a tintin pane above my ASCII map as you can see in the initial screenshot).

Along with this come various commands to interact with the spot timers from within TinTin++ itself:

##### List timers in-line
> `dt`

The `dt` command will print the list of timers in the MUD output, allowing for them to be referenced even when not displaying the file output in real time. I make use of this when on mobile or having the MUD in a more compact window.

##### Reset all or individual timers
> `dtreset all`, `dtreset hlakket`

I've heard sometimes you can miss a spot or lose it to competition. Sounds like excuses to me, but just in case, you can note that you've lost a spot or otherwise know it went down by manually setting it's timer to "just now" with the `dtreset <spot_name>` command.

Similarly, people tell me that on occasion real life requires that they *stop* hunting for a while, letting any previously recorded timers go stale and become useless. In this scenario you can use `dtreset all` to return all spots to the `Unseen/???` status and start fresh.

##### Share the timer list with your group
> `gsdt`

On occasion you have to group with folks who don't use my hotspot timer for TinTin++ or MUSHclient, leaving you unable to sync with them. You can take pity on these poor souls by sharing a snapshot of your current timers with them via group chat with the `gsdt` command.

```
[groupname] Ruhsbaar: delbert: 99m | hlakket: 11m | stables: ??? | casino: ??? | rogues: ??? | grflx:
     ??? | shaker lions: 32m | snail: ??? | dojo: 72m | medina boss: 22m | zoon liar: ??? | bandit leader: ???
     | cguards: ??? | giant leader: ??? | parades: ??? | offler: 05m | shades: 09m | smugglers: 37m | black
     market: ???
```

##### Sync timers to another player
> `dtsync <playername>`

It's often useful to share your timers with another player, if they are freshly joining the group and taking a lead, or maybe you want to be nice and share with someone before going to bed! This can be done with the `dtsync` command.

The syncing is done via a `tell` in game, and works between both my tt++ and MUSH plugins, allowing you to sync between players using the other client. When a players syncs their timers to yours, the plugin compares them to your existing values and only takes updates (e.g. if someone who killed Hlakket 90 minutes ago syncs to you, but you killed Hlakket 11 minutes ago, your 11 minute timer will not be overwritten).

Note that because the tell containing sync information is full of lengthy unix timestamps, you'll need to make sure to set your `cols 999` in-game before having another player sync to you (this is only needed on tt++, MUSH handles this gracefully).


#### Group Shield Monitor
* File `src/group.tin`
> Show the shield output inline: `sgs` (show group shields)
> Reset the monitor and re-capture: `rgs` (reset group shields)
Window appears above the ASCII map to display output at all times.


### Highlights/Actions/Other
* HP loss and XP gain notifications
* Dagger/Unarmed outgoing attacks
* Outgoing special attempts/lands/fails
* Outgoing backstabs
* Incoming attacks
* TPA shield drops
* T-Shop rooms
* Snatch/Filch
* Rumbling doors
* Inventory fumbles
* Copperhead mines gases
* Per day separated log files
* More...

### Layouts
The "Discworld" shell script will configure a slim (mobile friendly) layout when run with no arguments. This adds a split for chat and MDT stacked above the MUD window itself. If run with "full" as an argument, the timers, shield monitor, ascii-map will be off to the right hand side. If you are already inside of the "discworld" tmux session, running "Discworld" will re-arrange the layout as specified for easy switching between desktop and mobile.


## Credit Where It's Due
I've spent a lot of time and effort on this setup to make it perfect for my use and the contents herein have all been touched or modified by me in some way if not created outright, but I've been inspired by and blatantly stolen bits of it from two folks in particular:

### Quow
You don't play this game without knowing who Quow is and at least having heard about all the work he's done on both various extensions for MUSHClient as well as the immense data collection effort that resulted in his database of rooms, npcs, items and more.

The "mapdoortext" and "speedwalking" functionality present in my TinTin++ configurations is merely a port of the Lua code that exists in his plugins that I copied to and modified to work in my terminal-only environment.

You can find Quow's work on his website: <http://quow.co.uk>

### Oki
I've never even met Oki in game, but I stumbled upon their repository of tintin scripts some time ago and happily copied some of their magic/combat substitutions and highlights for my own use.

There's some cool stuff in here I  haven't gotten around to copying over yet but plan to, like Thief quota monitoring etc.

You can find Oki's repository here: <https://git.tubul.net/richard/tt_dw.git>


## Disclaimer
The files in this repository were created/modified/copied by me for my own personal use and come with no guarantee to work for you or your fairy godmother. I provide these files "as-is" and offer no support whatsoever to get them working. 
Any content herein that is my own is released under the terms and conditions of the [GNU Affero General Public Licence v3.0](https://www.gnu.org/licenses/agpl-3.0.en.html)

