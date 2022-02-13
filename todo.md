


_ceci est le todo à faire hehe_


**EN COURS**

# adapt colors
  créer une vraie teinte par jour afin que les batiments gris au loin soient frais

# street
  stations de metro disponibles dans différentes rues : permet de se déplacer plus vite, potentiellement fuir police
  -faire des quartiers

# ajouter des putains de moyens d'ameliorer la relation
  pcq là tlm se fout sur la gueule
  idées :
    -> 'pk tu m'insultes' quand on recoit une insulte
    -> possibilité de pas taper quand on sfait taper, mais demander pardon/pitié
    -> compliments pop kan t qqun genti
    -> une simple conv (bjr,au revoir,cv ?) augmente la relat°
    -> amis dès qu'ils te voient ils te disent "oh yo"

# nodes de commuincation
  en gros pour l'instant c'est pas ouf les communications, très basique
  il faudrait inventer un système de nodes :
    -> en gros il y a deja des chemins de discussions pré tracées et lors d'une conversation
      toi ou meme les bots choissisent la voie qu'il veulent suivre
      (toi via la roll et les bots via un algorithme) qui va amener la discussion à un point presque intéressant

      EX concret :

        t'es dans la rue tu vois un mec qui coure : la roll te propose automatiquement la question "pourquoi tu cours ?"
        après le bot te répond "je fais mon jogging" ou alors "jme fais courser par les keufs" en fonction de son algo

        Soit. Il se fait courser par les keufs, la roll te propose "pk t'as fait quoi"

        Il dit "drogue", tu lui dis "tu veux venir te cacher chez moi ?"

        hop tu lui envoie un act et il te suit chez toi

# ajouter de la plouiiii

# LABELS

	pour publier un son tu as 2 moyens différents:
	-soit tu passes par un label (coute cher)
	-soit tu vas voir distrokid (coute pas cher)

	les labels c'est bien parce que tu auras la possibilité de choisir des plans de com : plus tu payes cher plus tu auras de la promo
				-> on peut voir afficher dans la rue des affiches "delta nouvel ep" et meme sur les batiments au loin
	distrokid ça fait le taf (tu paye genre 2 euros pour mettre en ligne 1 son) mais t'as aucune com

	c'est auprès de ces 2 bails que tu vas pouvoir récup ta thune après en fonction de tes streams:
		-labels tu récup 50% voir moins (ça dépend de ton contrat, encore une fois plus tu paye cher plus tu gagnes)
		-distrokid tu gagnes 100%

# BATIMENTS SPECIAUX A AJOUTER:
  -centre commercial
  -petit shop pour acheter tout et r
  -metro
  -shop de son
  -bars (open mic ?)
  -police (prison)

# pouvoir bouger en y suivant les builds


**BUGS**

# \!\ *bertran.get_time()* \!\_
  bug : quand on recoit un act le temps continue de filer si est en pause
  -> utiliser la clock bertran pour compter le temps qui passe pour les acts/dials ?

#  \!\ *nb bots ?* \!\_
  j'ai eu 694 fans alors que y'avait apparement que 690 bots (+ alphonse)
  et en plus j'en ai tué en chemin et ça m'a pas baissé des fans
  --> à régler

#  \!\ *spr mauvais groups ?* \!\_
  ex : train qui arrive au début de kamour str. -> visible une fract de sec au dessus des builds
  ex : button inventaire des fois en début de partie, affiche pas le clair


**DONE**

# tableau d'appreciation d'une personne
  que les bots (et toi) aient des avis sur chaque personne qu'ils croisent
  un mec qui t'a insulté bah tu l'aimes pas etc.
  -> influence le langage utilisé par les bots pour te répondre, et tout en fait

# animations mdr

  alors deja finir les putains de 3 sprites pour le skin du poto alphonse,
  puis le poto pénis
  et mettre genre des ptites anim des décors ça pourrait être lourdax (mais bon ça sera dans longtemps jimagijn)

# meilleure création de la ville :
    qu'elle se déploit depuis une seule et unique rue celle de la maison
    -> permet d'ouvrir des rues au fur et à mesure qu'on devient de plus en plus connu
    -> au début t'as qu'une station de métro

# STREETS

  -faire des escalators qui montent/descendent pour aller d'une rue horizontale à une rue verticale

# que les bots passent des portes

# \!\ *régler mauvais endroits streets map*  \!\_

## BARRE OUTILS UTILISABLES
  type minecraft
  4 slots possibles : on les remplit depuis l'inventaire
  scroll de souris change l'outil séléctionné
  -> hud affiche les détails de l'outil en cours
  -> rien : main (affiche le dmg)
  -> plume pour écrire
  barre d'espace active l'outil:
      arme -> frappe
      plume -> écrit
      food -> mange/boit

# \\!\\ amélioration de perf :
  -> la fonction g.sman.addCol() pas du tout optimisée:
    recrée une texture à chaque fois qu'on l'appelle, il faudrait plutot créer une texture
    par couleur et rescale le sprite pour avoir la bonne taille -> a faire



**LINKS**

https://www.konbini.com/fr/inspiration-2/scenes-de-vie-japonaises-reconstituees-gifs-animes-pixel-art/
https://www.pinterest.fr/search/pins/?q=pixel%20art%20city&rs=typed&term_meta[]=pixel%7Ctyped&term_meta[]=art%7Ctyped&term_meta[]=city%7Ctyped


**IDEES**

# mode histoire

# pote beatmaker qui t'aide au début

# mixer de plume :
  deux "A" -> une "A+"
  -> pour faire une S il faut 16 384 F
  -> X = 131 072 F

# ajouter drogue:
  -> colore de ouf l'écran de milliers de couleurs:
    rend le jeu très beau du coup ça peut reellement rendre addict le joueur ptdrr

# s bahn:

  différent du métro de base souterrain:
  -> sbahn est situé derrière les builds des streets :
    on le voit passer de temps en temps derrière
    permet de bouger d'un quartier à l'autre

  -> lorsqu'on le prend on reste sur la même street (même vision)
  mais le sprite passe derrière les builds et avance très vite puis ça bascule sur une nouvelle street d'un nouveau quartier

  -> cool pour les bots : pas obligé de se déplacer tout le temps à pied, on peut les voir arriver en sbahn oklm pour aller au taf

# avoir un metier a part
