# plumegang
Little (early version) 2d game coded in Python with Pyglet


### **DESCRIPTION**
You are a little rappeur in a new city to explore :

You begin in your own house and you need to earn money


Each day you lose some money and if you hit the 0$ bottom, this is a sad GAME OVER


In order to make money, you need to create and release 'sons' *(songs)*.

To create songs, you have to write some 'phases' *(lyrics)* in your bed with your 'plume' *(feather)*.

You also need to find an 'instru' *(instrumental)* and there you go !

**4 phases + 1 instru = 1 son**

Use the things in your house to make all this stuff !


***

### **FOR NOW**

For now the game is in a very early version so don't expect to see every thing right now hehe (cheh)

You can walk around using Z,S,Q,D (azerty keyboard lezgoo), and activate things around by long-hitting Z or S.
You can click with the mouse on the screen to move items in inventories OR to show the message screen -> use it to say things.
If you want to hit bots you need to activate the FIGHT MODE using ***F***.
You can scroll the mouse to select the item you want to use (like in minecraft)

You can also use the train (sbahn) to move faster inside the city

---


*Lit* - long press **Z** to create phase (/!\\ you need to have a plume)

*Studio* - long press **Z** to assemble your song (/!\\ 4 phases + 1 instru)

*Plumoir* - long press **Z** to get a new random plume

*Ordi* - short mouse click on an instru to see details, long click on the detailed instru to buy it




### **CONTROLS**

***Z*** - move up -- activate object in the background / deactivate activated object in foreground

***S*** - move down -- activate object in the foreground / deactivate activated object in bg

***Q*** - move left -
***D*** - move right

***F*** - scroll between modes : (FIGHT/PEACE)

***SPACE*** (peace mode) - grab item / use the selected item

***SPACE*** (fight mode) - grab item / attack w selected weapon / attack with your hand

***E*** - show inventory -
***M*** - show map -
***TAB*** - show the near bots / the bots you met -
~~***L*** - show the charts of rappers~~ (not workin)

***ESC***  - to close the hud of the thing you are using OR to pause the game -
***up***/***down*** - (in the menu) to control menu -
***ENTER***  - (in the menu) to activate action

***<-***/***->*** - to control camera

***A*** - to drop the selected item

***X*** - to hide your perso's menu

***scroll-up/down*** - scroll between your items in the selecter (little inventory bottom right) -
***1/2/3/4*** - select corresponding item

***T*** - open chat -
***/*** - open command chat

***ENTER*** - (in the chat) say your message -
***Y*** - hide/show the chat

### **COMMANDS**

useful :

`@` is yourself/your street

`#` is the nearest bot

`°` is a random bot/random street

`*` everyone/everything

`&` is the main street (certainly <kamour str.>)

`¤` is a little complicated so discover it urself

`<...>` to write thg with spaces inside : ex: <rue 23> -> rue 23

---

`/tp [personame] (x) (y) (street)`
`/tp [personame] (otherpersoname)`
`/tp [personame] (street)`

`/tp_self (x) (y) (street)` = `/tp @ (x) (y) (street)`

`/tp_street [personame] (street)` = `/tp [personame] (street)`

`/tp_to_perso [personame] (otherpersoname)` = `/tp [personame] (otherpersoname)`

`/give [personame] (itemname)` - (ex: try /give @ m16)

`/add_money [personame] (qty)`
`/set_money [personame] (qty)`
`/set_fans [personame] (qty)`
`/add_streams [personame] (qty)`
`/set_streams [personame] (qty)`

`/kill [personame]`
`/stop [personame]`
`/free [personame]`
`/dmg [personame] (qty)`
`/heal [personame] (qty)`

`/perso [personame]` - gives information about a perso

`/poto [personame]` - developper stuff

`/gex [personame]` - gives position

`/get_id [personame]` - gives id

`/street [street]` - gives information about street

`/sbahn_speed (qty)` - set/get speed of the train

`/tick (tick)` - set/get the tick

there may be other cheat commands ehe who knows ^^
