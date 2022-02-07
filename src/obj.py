"""
CODED by deltasfer
enjoy
"""

import random as r
import json,time,pyglet
from src.colors import *
from colors import red, green, blue
from src.utils import *
from src import graphic as g
from src import names as n
from src import obj2 as o2
from src import perso as p
from collections import OrderedDict

"""'''''''''''''''''''''''''''''''''
'''''''INIT'''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''"""

QUALITIES = ['F'
            ,'D-','D','D+'
            ,'C-','C','C+'
            ,'B-','B','B+'
            ,'A-','A','A+'
            ,'S-','S','S+'
            ,'S*']
QUALITIES_coeff = [0.1
            ,0.2,0.3,0.4
            ,0.5,0.6,0.7
            ,0.75,0.8,0.85
            ,0.9,0.92,0.94
            ,0.96,0.98,0.995
            ,1.1]
QUALITIES_up = {'F':0.1
            ,'D-':0.1,'D':0.1,'D+':0.1
            ,'C-':0.1,'C':0.1,'C+':0.1
            ,'B-':0.05,'B':0.05,'B+':0.05
            ,'A-':0.05,'A':0.02,'A+':0.02
            ,'S-':0.02,'S':0.02,'S+':0.015
            ,'S*':1}
QUALITIES_dwn = {'F':-1,'D-':-0.1
            ,'D':-0.1,'D+':-0.1,'C-':-0.1
            ,'C':-0.1,'C+':-0.1,'B-':-0.1
            ,'B':-0.05,'B+':-0.05,'A-':-0.05
            ,'A':-0.05,'A+':-0.02,'S-':-0.02
            ,'S':-0.02,'S+':-0.02,'S*':-0.015}

CRED = ['pire merde de la terre','sous-merde','merde'
        ,'victime','neutre','thug'
        ,'gangster','gros ganster','ennemi number one']
CRED = ['----','---','--'
        ,'-','/','*'
        ,'**','***','****']

CRED_coeff = [-95,-80,-50,-10,10,50,80,95,101]

with open('src/mots.json','r', encoding="utf-8") as f:
    MOTS = json.load(f)

THEMES = ['amour','argent','liberté','révolte','egotrip','ovni','famille','tristesse','notoriété','chill','rap']

MAX_STACK = 100

"""'''''''''''''''''''''''''''''''''
'''''''USEFUL FUNCTIONS'''''''''''''
'''''''''''''''''''''''''''''''''"""
def test():

    quality = r.random()
    cred = r.randint(-100,100)

    print(convert_quality(quality),convert_cred(cred))

    plum = Plume('delta',quality,cred)
    print('\n')
    for i in range(20):
        phaz = []
        for i in range(4):
            phaz.append(plum.rd_phase())
        btmker = Btmaker(r.random())
        Son(btmker.rd_instru(),phaz)

    #return Plume(quality,cred)

def test2():

    for i in range(11):

        qua = i/10

        a = (qua**4)/10 * 1000 *qua
        print(qua,a)
        #x = (qua-self.qua_score) * self.nb_fans

def test3(n=100000):

    instrus = []
    for i in range(n):
        ins = rinstru(rbt())
        instrus.append(ins)
    instrus.sort(reverse=True)

    for i in range(20):
        ins = instrus[i]
        print(ins.price,' : ',convert_quality(ins.quality),trunc(ins.quality,5),trunc(ins.author.quality,5))

def rplum(owner):

    quality = r.random()
    cred = r.randint(-100,100)

    #print(convert_quality(quality),convert_cred(cred))

    return Plume(owner,quality,cred)

def splum(owner):

    quality = 0.999 + r.random()/1000
    cred = r.randint(-100,100)

    return Plume(owner,quality,cred)

def sson(owner):

    b = Btmaker(0.999,'°')

    quains = 0.999 + r.random()/1000

    ins = Instru(quains,b)

    phz = []
    for i in range(4):
        quality = 0.999 + r.random()/1000
        cred = r.randint(-100,100)
        phz.append(Phase(quality,cred))

    return Son(ins,phz,owner)

def rinstru(bt=None):

    if bt == None:
        bt = r.choice(btmakers)

    return bt.rd_instru()

def rbt():
    return Btmaker(rqua())

def convert_quality(qua,test=(QUALITIES,QUALITIES_coeff)):


    if qua < test[1][0]:
        return test[0][0]
    else:
        return convert_quality(qua,(test[0][1:],test[1][1:]))

def convert_cred(cred,test=(CRED,CRED_coeff)):

    if cred < test[1][0]:
        return test[0][0]
    else:
        return convert_cred(cred,(test[0][1:],test[1][1:]))

def upgrade_qua(qua,bonus=True):

    if bonus:
        return qua + QUALITIES_up[convert_quality(qua)]
    else:
        return qua + QUALITIES_dwn[convert_quality(qua)]

def aff_phase(phase):

    print(phase.str())

def rqua():
    return r.random()

def rcred():
    return r.randint(-100,100)

def a(qua):

    basis = (qua)*10
    bonus = 0

    if qua > 0.6:
        bonus += (qua-0.6)*15
    if qua > 0.8:
        bonus += (qua-0.8)*50
    if qua > 0.92:
        bonus += (qua-0.92)*200
    if qua > 0.98:
        bonus += (qua-0.98)*800
    if qua > 0.995:
        bonus += (qua-0.995)*8400

    return int((basis + bonus)*10)

def instru_price(ins):

    bt_price = a(ins.author.quality)
    ins_price = a(ins.quality)

    p = 0.75
    price = p*ins_price + (1-p)*bt_price

    return int(price + (-0.1+r.random()/5)*price)

def get_perso_grp(gey):

    k = int(g.gman.nb_perso_group*gey/o2.maxY)
    if k > g.gman.nb_perso_group:
        grp = 'persoup'
    elif k < 0:
        grp = 'persodown'
    else:
        grp = 'perso'+str(k)

    return grp

"""'''''''''''''''''''''''''''''''''
'''''''ITEMS''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''"""
# -> items sans texture comportant seulement leur essence
class Item():
    def __init__(self):
        self.stacked = 1

    def details(self):
        return [type(self).__name__.lower()]

    def stackable(self,other):

        ## return 0 if unstackable
        ## return 1 if stackable
        return 0

class Key(Item):

    def __init__(self,street):
        super(Key,self).__init__()

        self.target = street
        self.cat = 'key'

    def __str__(self):
        return 'key for '+self.target.name

    def details(self):
        return self.target.name.split('-')

class Food_item(Item):

    def __init__(self):
        super(Food_item,self).__init__()
        self.cat = 'food'

class Bottle(Food_item):

    def __init__(self):
        super(Bottle,self).__init__()

        self.liquid = 'water'

        self.qt = 1000 #qté en mL
        # 1 litre d'eau recharge toute une "vie d'eau"
        self.single_act = False

    def act(self,perso):
        qté = 4
        if self.qt >= qté and perso.hyd <= 100-qté/10:
            perso.drink(qté)
            self.qt -= qté
        else:
            perso.actin = 'done'
            g.bertran.schedule_once(perso.undo,0.2,'drink')

    def __str__(self):
        return 'bottle of '+str(self.qt)+'mL of water'

    def details(self):
        return [self.liquid,str(self.qt)+' mL']

    def stackable(self,other):

        ## return 0 if unstackable
        ## return 1 if stackable

        if other.qt == self.qt and self.liquid == other.liquid and self.stacked + other.stacked  < MAX_STACK:
            return 1
        return 0

    def stack(self,nb=1):
        ## aucune vérif, on ajoute juste un au nb de stack
        self.stacked += nb


"""'''''''''''''''''''''''''''''''''
'''''''SOUND ITEMS''''''''''''''''''
'''''''''''''''''''''''''''''''''"""
# -> items sans texture comportant seulement leur essence


class Sound_item(Item):

    def __init__(self):
        super(Sound_item,self).__init__()

    def __lt__(self, other):
         return self.quality < other.quality

    def details(self):
        return [convert_quality(self.quality)]

#------# plum
class Plume(Sound_item):

    def __init__(self,owner,qua,cred):
        super(Plume,self).__init__()

        self.cat = 'plume'
        self.quality = qua
        self.cred = cred
        self.owner = owner

        self.level = 0

        # skins
        #self.hud = PlumHUD(self)

    def rplum(self):

        self.quality = r.random()
        self.cred = r.randint(-100,100)

    def rd_phase(self):

        x = 2
        qua = (self.quality*x + r.random())/(x+1)

        x = 3
        cred = (self.cred*x + r.randint(-100,100))/(x+1)

        phase = Phase(qua,cred)
        #print(phase.content)
        #print(convert_quality(qua),convert_cred(cred))

        return phase

    def __str__(self):
        return str(self.owner)+'\'s plume'

#------# phases
class Phase(Sound_item):

    def __init__(self,quality,cred,):
        super(Phase,self).__init__()

        self.cat = 'phase'

        self.quality = quality
        self.cred = cred

        self.content = self.generate_content()
        self.them = r.choice(THEMES)

    def generate_content(self):

        nb = r.randint(3,4)
        s = r.choice(MOTS)
        for i in range(nb-1):
            s += ' ' + r.choice(MOTS)
        return s

    def str(self):

        s= '\n'
        s += self.content + '\t:' + convert_quality(self.quality) + '  ' + convert_cred(self.cred) + '\n'
        s+= str(self.them)
        s+= '\n'

        return s

    def __str__(self):
        return 'phase ' + convert_quality(self.quality)

#------# instrus
class Btmaker():

    def __init__(self,qua=0.5,name='Bokusan'):

        self.name = name

        #self.money = 1000

        self.quality = qua

    def rd_instru(self):

        x = 2
        qua = (self.quality*x + r.random())/(x+1)

        instru = Instru(qua,self)
        #print('instru '+convert_quality(qua))
        return instru

    def __lt__(self, other):
         return self.quality < other.quality

btmakers = []
for name in n.btmakers:
    btmakers.append(Btmaker(rqua(),name))

class Instru(Sound_item):

    def __init__(self,qua,author):
        super(Instru,self).__init__()

        self.cat = 'instru'

        self.quality = qua
        self.author = author

        self.price = instru_price(self)
        self.owners = []

    def add_owner(self,owner):
        self.owners.append(owner)

    def __str__(self):
        return 'instru' + '  ' +convert_quality(self.quality) + '  ' + self.author.name

#------# sons
class Son(Sound_item):

    def __init__(self,instru,phases,name='cheh'):
        super(Son,self).__init__()

        self.cat = 'son'

        self.name = name

        self.instru = instru
        self.phases = phases

        self.quality = self.global_qua()
        if self.quality > 1:
            self.quality = 1

        self.cred = max([ x.cred for x in self.phases])

        self._released = False
        self.streams = 0

        self.release_date = None


        #print(convert_quality(self.quality),convert_cred(self.cred))

    def global_qua(self):

        x_instru = 1
        x_phases = 1

        qua_instru = self.instru.quality

        qua_phases = 0
        themes = []
        for ph in self.phases:
            qua_phases += ph.quality
            if ph.them not in themes:
                themes.append(ph.them)
        qua_phases/=len(self.phases)

        qua = (x_instru*qua_instru + x_phases*qua_phases)/(x_instru+x_phases)

        if len(themes) <= 1:
            qua = upgrade_qua(qua,1)
        elif len(themes) > 2:
            qua = upgrade_qua(qua,-1)

        return qua

    def release(self,perso,day,label):
        self._released = True
        self.author = perso
        self.release_date = day
        self.label = label
        self.label.release(self)

    def stream(self):
        self.streams+=1
        self.author.addstream()
        self.label.stream(self)

    def __str__(self):
        return 'son   ' + '  ' + trunc(self.quality,5) +' '+convert_quality(self.quality) + '  ' + str(self.cred)



"""'''''''''''''''''''''''''''''''''
'''''''LABELS'''''''''''''''''''''''
'''''''''''''''''''''''''''''''''"""

class Label():

    def __init__(self,nom='DefJam'):

        self.name = nom  #name of the label

        self.rappeurs = [] #each rapper workin with this label

        self.caisse = {}
        self.sons = {}
        self.streams = {}
        self.dailystreams = {}

        self.thune = 0

        ## argent gagné par stream :
        ## caisse = nb_streams * prix_stream * pourcentage_pour_artiste
        self.stream_price = 1 # prix du stream

    def sign(self,rapper):
        self.rappeurs.append(rapper)
        self.caisse[rapper] = 0
        self.streams[rapper] = {}
        self.sons[rapper] = {}
        self.dailystreams[rapper] = 0

        print(rapper.name,'a signé chez',self.name,'!')
        exp = rapper.name+' a signé chez '+self.name+' !'
        g.pman.alert(exp)

    def release(self,son,perc=0.5):
        if son not in self.sons:
            rapper = son.author
            self.sons[rapper][son] = perc
            self.streams[rapper][son] = 0

    def stream(self,son):
        self.streams[son.author][son] += 1
        self.dailystreams[son.author] += 1
        self.caisse[son.author] += self.price_stream*self.sons[son.author][son]
        self.thune += (1-self.sons[son.author][son])*self.price_stream

    def cashback(self,rapper):
        if rapper in self.rappeurs and self.caisse[rapper] > 0:
            rapper.add_money(self.caisse[rapper])
            self.caisse[rapper] = 0

    def update(self):
        # changer dans distrokid aussi
        for rapper in self.rappeurs:
            print(rapper.name,':\n\t','daily streams :',self.dailystreams[rapper],'\n\t','caisse :',self.caisse[rapper])
            self.dailystreams[rapper] = 0

class Distrokid(Label):

    def __init__(self):
        super(Distrokid,self).__init__('Distrokid')

        self.price_stream = 1
        # 0.1 dollar le stream
        self.daily_abo = 1
        # 1 euro l'abonnement par jour à distro

    def release(self,son):
        super(Distrokid,self).release(son,1)

    def update(self):
        for rapper in self.rappeurs:
            self.caisse[rapper] -= self.daily_abo
            print(rapper.name,':\n\t','daily streams :',self.dailystreams[rapper],'\n\t','caisse :',self.caisse[rapper])
            self.dailystreams[rapper] = 0

distro = Distrokid()


"""'''''''''''''''''''''''''''''''''
'''''''ZONES''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''"""

class Zone():

    def __init__(self,box,textid='white',group='mid',makeCol=False,vis=False):

        if textid[:4] == 'text':
            self.text_id = textid
        elif makeCol:
            self.text_id = g.tman.addCol(textid)
        self.loaded = False

        if vis: self.load()

        self.gex,self.gey = box.xy
        self.x,self.y = 0,0
        self.w,self.h = box.wh
        self.group = group

        self._hoover = False

    def load(self):

        if hasattr(self,'text_id') and not hasattr(self,'skin_id') :
            self.skin_id = g.sman.addSpr(self.text_id,self.box.xy,self.group)
            w,h = g.sman.sprites[self.skin_id].width,g.sman.sprites[self.skin_id].height
            g.sman.modify(self.skin_id,scale=(self.box.w/w,self.box.h/h))

        self.loaded = True
        #print(self.name,'loaded')

    def deload(self):

        if hasattr(self,'skin_id'):
            g.sman.delete(self.skin_id)
            del self.skin_id

        self.loaded = False


    def _realbox(self):
        return self.x,self.y,self.x+self.w,self.y+self.h
    realbox = property(_realbox)
    def _gebox(self):
        return self.gex,self.gey,self.gex+self.w,self.gey+self.h
    gebox = property(_gebox)

#------# elements

class Zone_ELEM(Zone):

    ## HOOVER WITH MOVEMENT OF PERSO

    def __init__(self,box,name='thing',textid='white',group='mid',long=False,makeCol=True,position='back'):
        super(Zone_ELEM,self).__init__(box,textid,group,makeCol)

        ## la position est différente que la pos !! (louis du futur stp trouve un autre nom là cé éclaté)
        #   elle régule la position de la zone PAR RAPPORT au perso afin de l'activer correctement
        #   3 positions : 'back','front','mid' :
        # si 'back', le perso doit monter (Z) pour activer la zone
        # si 'front', le perso doit descendre (S) pour activer la zone
        # si 'mid', inactivable (prendre avec E)

        self.position = position
        self.perso_anim = 'act'

        self.cooldown = 0.5

        self.name = name
        self.labtext = name
        self.longpress = long

        self.box = box

        # label
        #pos = box.x + box.w/2 , box.y + box.h + 20
        #self.label = g.lman.addLab(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20,group=group)

        self.color = c['coral']

        self.activated = False

    def move(self,x_r,y_r):
        if hasattr(self,'skin_id'):
            g.sman.modify(self.skin_id,(x_r,y_r),group=get_perso_grp(self.gey))
        self.x,self.y = x_r,y_r
        self.update()

    def hoover(self):
        if hasattr(self,'label'):
            g.lman.unhide(self.label)
            self._hoover = True

    def unhoover(self):
        if hasattr(self,'label'):
            g.lman.unhide(self.label,True)
            self._hoover = False

    def activate(self,perso):

        print(perso.name,'just activated',self.labtext)
        if hasattr(self,'label') and isinstance(perso,p.Perso):
            g.lman.modify(self.label,color=self.color)

            g.bertran.schedule_once(self.deactivate,0.5)

    def deactivate(self,dt):
        if hasattr(self,'label'):
            if self._hoover:
                g.lman.modify(self.label,color=c['white'])
            else:
                g.lman.modify(self.label,color=(255,255,255,0))

    def update(self):
        if hasattr(self,'label'):
            # label
            pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 20
            g.lman.modify(self.label,pos,group=get_perso_grp(self.gey))

    def deload(self):
        if hasattr(self,'skin_id'):
            g.Cyc.del_spr((self.skin_id,0.3))
        super(Zone_ELEM,self).deload()
        if hasattr(self,'label'):
            g.lman.delete(self.label)
            del self.label

    def load(self,street):
        super(Zone_ELEM,self).load()

        if hasattr(self,'skin_id') and street.outside:
            g.Cyc.add_spr((self.skin_id,0.3))

        if not hasattr(self,'label'):
            # label
            pos = self.box.x + self.box.w/2 , self.box.y + self.box.h + 20
            self.label = g.lman.addLab(self.labtext,pos,vis=False,anchor = ('center','bottom'),font_size=20,group='mid')

class Market(Zone_ELEM):

    def __init__(self,x,y):
        super(Market,self).__init__(box(x,y,300,320),'plumoir','pink','mid',True,False)

    def activate(self,perso):
        super(Market,self).activate(perso)
        perso.rplum()

class SimpleReleaser(Zone_ELEM):

    def __init__(self,x,y,label):
        super(SimpleReleaser,self).__init__(box(x,y,300,320),'releaser','pink','mid',True,False)
        self.LABEL = label

    def activate(self,perso):
        super(SimpleReleaser,self).activate(perso)
        if perso in self.LABEL.rappeurs:
            perso.auto_release(self.LABEL)

class Porte(Zone_ELEM):

    def __init__(self,street,box,destination,xdest,makeCol=False,text=None,anim='door'):

        super(Porte,self).__init__(box,get_id(destination.name),'grey','mid',makeCol=makeCol)
        self.destination = destination
        self.street = street
        self.xdest = xdest
        self.perso_anim = anim

        if self.street.pre.vert:
            #self.node = {'vert':self.street.name,'hor':self.destination.name}
            self.node = self.street.name + ' -<->- ' + self.destination.name
        else:
            #self.node = {'vert':self.destination.name,'hor':self.street.name}
            self.node = self.destination.name + ' -<->- ' + self.street.name

        if anim == 'stairs':
            self.cooldown = 1

        if text != None:
            self.labtext = text
        else:
            self.labtext = destination.name

        self.deload()

    def assign_door_tp(self,door):
        self.porte_tp = door

    def activate(self,perso):
        super(Porte,self).activate(perso)

        if self.openable(perso):
            x = self.xdest + r.randint(0,self.box.w)-self.box.w/2
            perso.tp(x=x,street=self.destination)
            return self.destination.name
        elif isinstance(perso,p.Perso):
            g.pman.alert('you can\'t go here !')

    def openable(self,perso):

        if self.destination.free_access:
            return True

        if self.destination in list(map(lambda x:x.target,perso.inventory['key'])):
            return True

        if self.destination in list(map( lambda x:x.target ,   list(filter(lambda x:type(x).__name__ == 'Key',list(perso.selecter.values()) )))):
            return True

        if perso.cheat:
            return True

        if isinstance(self.street,o2.House) and isinstance(self.destination,o2.Building):
            return True

        if isinstance(self.destination,o2.Building):
            for house in self.destination.houses:
                if house.free_access:
                    return True

                if house in list(map(lambda x:x.target,perso.inventory['key'])):
                    return True

                if house in list(map( lambda x:x.target ,   list(filter(lambda x:type(x).__name__ == 'Key',list(perso.selecter.values()) )))):
                    return True

        return False

class Cash(Zone_ELEM):

    def __init__(self,x,y,w=100,h=200,make_col=True):
        super(Cash,self).__init__(box(x,y,w,h),'ez cash','red','mid',makeCol=make_col)

    def activate(self,perso):
        super(Cash,self).activate(perso)
        perso.add_money(r.randint(20,230))

class Distrib(Zone_ELEM):

    def __init__(self,x,y):

        text = g.TEXTIDS['zone']['distrib']
        w,h = g.tman.textures[text].width,g.tman.textures[text].height

        super(Distrib,self).__init__(box(x,y,w,h),get_id('distrib'),text,'mid')
        self.labtext = 'distrib'

    def activate(self,perso):
        super(Distrib,self).activate(perso)
        perso.grab(Bottle())


#------# elements item -> item posable au sol dans une street

class Item_ELEM(Zone_ELEM):

    def __init__(self,item,poscentrale,street,size=64):
        nom = str(item)

        pos = poscentrale[0]-size/2,poscentrale[1]

        text = 'white'
        if isinstance(item,Sound_item):
            text = g.TEXTIDS[type(item).__name__.lower()][convert_quality(item.quality)[0]]
        else:
            text = g.TEXTIDS['items'][type(item).__name__.lower()]

        super(Item_ELEM,self).__init__(box(*pos,size,size),nom,text,group='perso0',makeCol=False)
        self.labtext = type(item).__name__.lower()
        o2.NY.CITY[street].add_item(self)
        self.item = item
        self.street = street

    def activate(self,perso):

        o2.NY.CITY[self.street].del_item(self)
        perso.grab(self.item)

        print(perso.name,'took',self.name)


#------# active elements

class Zone_ACTIV(Zone_ELEM):

    def __init__(self,box,name='thing',textid='white',group='mid',long=False,makeCol=True,position='back',hud=None):
        super(Zone_ACTIV,self).__init__(box,name,textid,group,long,makeCol,position)

        self.activate_inv = True
        self.inv_already_vis = False

        if hud:
            self.hud = hud
        else:
            self.hud = HUD()

    def activate(self,perso):
        super(Zone_ACTIV,self).activate(perso)
        self.activated = True

        if not self.hud.visible:
            ## première activation

            if perso.invhud.visible :
                self.inv_already_vis = True
            else:
                self.inv_already_vis = False
                perso.invhud.unhide()

            perso.invhud.eff_detail()
            perso.invhud.autorize_deta = False

    def close(self,perso):

        #print(self.hud.visible,self.activated)
        if self.hud.visible:
            self.activated = False
            perso.do()

            if not self.inv_already_vis:
                perso.invhud.unhide(True)
            perso.invhud.autorize_deta = True

class Ordi(Zone_ACTIV):

    def __init__(self,x,y,perso):
        super(Ordi,self).__init__(box(x,y,230,260+150),'ordi','red','mid',makeCol=False,long=True,position='front',hud=MarketHUD(perso))

    def activate(self,perso):
        super(Ordi,self).activate(perso)

        g.lman.modify(self.hud.labids['market'],color=self.color)

        if self.hud.visible:
            perso.do('write')
            perso.undo(0,'wait')

        else:
            perso.do('wait')
            self.hud.unhide()

    def deactivate(self,dt):
        super(Ordi,self).deactivate(0)
        if self.activated:
            g.lman.modify(self.hud.labids['market'],color=c['white'])
        else:
            g.lman.modify(self.hud.labids['market'],color=(255,255,255,0))

    def close(self,perso):
        super(Ordi,self).close(perso)
        self.hud.unhide(True)

class Studio(Zone_ACTIV):

    def __init__(self,x,y):
        super(Studio,self).__init__(box(x,y,50,200),'studio','blue','mid',makeCol=False,long=True,hud=StudHUD())

    def activate(self,perso):
        super(Studio,self).activate(perso)

        g.lman.modify(self.hud.labids['stud'],color=self.color)

        if self.hud.visible:
            perso.do('write')
            perso.undo(0,'wait')
            self.hud.assemble(perso)
        else:
            perso.do('wait')
            self.hud.unhide()

    def deactivate(self,dt):
        super(Studio,self).deactivate(0)
        if self.activated:
            g.lman.modify(self.hud.labids['stud'],color=c['white'])
        else:
            g.lman.modify(self.hud.labids['stud'],color=(255,255,255,0))

    def close(self,perso):
        super(Studio,self).close(perso)
        self.hud.unhide(True)

    def assemble(self,perso):

        son = perso.creer_son()
        if son != None:
            perso.grab(son)
        else:
            print('Frerooooo t\'as besoin d\'une instru et de 4 phases pour faire un son tu vas ou commas ?')

class Lit(Zone_ACTIV):

    def __init__(self,x,y):
        super(Lit,self).__init__(box(x,y,300,150),'lit','darkgreen','mid',long=True,hud=WriteHUD())

    def activate(self,perso):
        super(Lit,self).activate(perso)
        g.lman.modify(self.hud.labids['lit'],color=self.color)

        if self.hud.visible:
            perso.do('write')
            perso.undo(0,'wait')
            self.write(perso)
        else:
            perso.do('wait')
            self.hud.unhide()

    def deactivate(self,dt):
        super(Lit,self).deactivate(0)
        if self.activated:
            g.lman.modify(self.hud.labids['lit'],color=c['white'])
        else:
            g.lman.modify(self.hud.labids['lit'],color=(255,255,255,0))

    def close(self,perso):
        super(Lit,self).close(perso)
        self.hud.delete_phase()
        self.hud.unhide(True)

    def write(self,perso):

        if perso.plume != None:
            phase = perso.plume.rd_phase()
            #aff_phase(phase)
            self.hud.write(phase)



"""'''''''''''''''''''''''''''''''''
'''''''HUD  ''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''"""

#------# hud

class HUD():

    def __init__(self,group='hud1',name='main',vis=True):

        self.name = name
        self.group = group

        #---#

        self.sprids = {}
        self.labids = {}

        #---#

        self.visible = vis

    def addSpr(self,key,textid,xy_pos=(0,0),group=None):

        if key in self.sprids:
            g.sman.delete(self.sprids[key])

        if group == None:
            group = self.group

        self.sprids[key] = g.sman.addSpr(textid,xy_pos,group,vis=self.visible)

    def addCol(self,key,box,color='delta_purple',group=None):

        if key in self.sprids:
            g.sman.delete(self.sprids[key])

        if group == None:
            group = self.group

        self.sprids[key] = g.sman.addCol(color,box,group,vis=self.visible)

    def addLab(self,key,contenu,xy_pos=(0,0),group=None,font_name=0,font_size=30,anchor=('left','bottom'),color=(255,255,255,255),replace=True):

        if replace:
            if key in self.labids:
                g.lman.delete(self.labids[key])

            if group == None:
                group = self.group

            self.labids[key] = g.lman.addLab(str(contenu),xy_pos,group=group,font_name=font_name,font_size=font_size,anchor=anchor,color=color,vis=self.visible)

        elif key not in self.labids:
            if group == None:
                group = self.group

            self.labids[key] = g.lman.addLab(str(contenu),xy_pos,group=group,font_name=font_name,font_size=font_size,anchor=anchor,color=color,vis=self.visible)

    def delLab(self,key):
        if key in self.labids:
            g.lman.delete(self.labids[key])
            self.labids.pop(key)

    def delSpr(self,key):
        if key in self.sprids:
            g.sman.delete(self.sprids[key])
            self.sprids.pop(key)

    def modifySpr(self,key,pos=None,scale=None):
        g.sman.modify(self.sprids[key],pos,scale)

    def modifyLab(self,key,pos=None,col=None):
        g.lman.modify(self.labids[key],pos,color=col)

    def unhide(self,hide=False):

        g.sman.unhide(self.sprids,hide)
        g.lman.unhide(self.labids,hide)
        self.visible = not hide

    def rollhide(self):
        self.unhide(self.visible)

    def delete(self):
        g.lman.delete(self.labids)
        g.sman.delete(self.sprids)

    ## oeoe

    def spr(self,key):
        return g.sman.spr(self.sprids[key])

    def lab(self,key):
        return g.lman.labels[self.labids[key]]

class Map(HUD):

    def __init__(self,perso):

        #w_map = 100000

        super(Map, self).__init__(group='hud2',name='map',vis=False)

        self.perso = perso

        scrw,scrh=g.scr.size
        area = box(scrw//2-2*scrh//6,scrh//6,2*scrh//3,2*scrh//3)

        self.pad = 25
        self.box = box(area.x+self.pad,area.y+self.pad,area.w-2*self.pad,area.h-2*self.pad)

        self.larg_cube = 18
        self.larg_street = 6
        self.larg_house = 12
        #w = self.larg_cube*3*w_map
        #self.box = box(scrw/2-w/2,scrh/2-w/2,w,w)

        self.ax,self.ay = self.box.cxy

        self.addCol('bg',area,group='hud2-1',color='delta_blue_faded')
        self.addCol('bg2',area,group='hud2-1',color='delta_blue_faded')

        ## name
        self.addLab('name','MAP OF NY CITY',(area.cx,area.fy-self.pad),font_name=1,anchor=('center','center'),group='hud2')

    def load(self):
        self.create_map()

    def deload(self):
        for street in o2.NY.CITY:
            self.delSpr(o2.NY.CITY[street].name)

    def unhide(self,hide=False):
        super(Map,self).unhide(hide)
        if hide:
            self.deload()
        else:
            self.load()

    def create_map(self):

        for street in o2.NY.CITY:
            #print(street.name)
            street = o2.NY.CITY[street]

            if type(street) == o2.Street:

                vert = street.pre.vert

                if not vert:
                    x = self.ax + street.pre.x*self.larg_cube
                    y = self.ay + self.larg_cube/2 -self.larg_street/2 + street.pre.y*self.larg_cube
                else:
                    x = self.ax + self.larg_cube/2 -self.larg_street/2 + street.pre.x*self.larg_cube
                    y = self.ay + street.pre.y*self.larg_cube

                if vert:
                    w,h=self.larg_street,street.pre.w*self.larg_cube
                else:
                    h,w=self.larg_street,street.pre.w*self.larg_cube

                self.addCol(street.name,box(x,y,w,h),color='delta_purple',group='hud2')

            elif street.name == 'home':
                w,h=self.larg_house,self.larg_house

                x = self.ax + street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                y = self.ay + street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                self.addCol(street.name,box(x,y,w,h),color='red',group='hud21')

            elif isinstance(street,o2.Shop) or isinstance(street,o2.SpecialHouse):
                w,h=self.larg_house,self.larg_house

                x = self.ax + street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                y = self.ay + street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                self.addCol(street.name,box(x,y,w,h),color='blue',group='hud21')

    def update(self):

        if self.visible :
            perso_street = o2.NY.CITY[self.perso.street]

            # get pos
            if type(perso_street) == o2.Street: # si le perso se trouve dans une rue

                perc = perso_street.get_pos(self.perso)

                vert = perso_street.pre.vert
                if vert:
                    px = g.sman.spr(self.sprids[perso_street.name]).x - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                    py = g.sman.spr(self.sprids[perso_street.name]).y + perc*g.sman.spr(self.sprids[perso_street.name]).height
                else:
                    py = g.sman.spr(self.sprids[perso_street.name]).y - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                    px = g.sman.spr(self.sprids[perso_street.name]).x + perc*g.sman.spr(self.sprids[perso_street.name]).width
            else: #perso_street.name == 'home': # si le perso se trouve dans une maison
                px = self.ax + perso_street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                py = self.ay + perso_street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                px += self.larg_cube/2
                py += self.larg_cube/2


            # update anchor
            self.ax += self.box.cx-px
            self.ay += self.box.cy-py

            # update all streets
            for street in o2.NY.CITY:
                street = o2.NY.CITY[street]

                if type(street) == o2.Street:

                    vert = street.pre.vert

                    if not vert:
                        x = self.ax + street.pre.x*self.larg_cube
                        y = self.ay + self.larg_cube/2 -self.larg_street/2 + street.pre.y*self.larg_cube
                    else:
                        x = self.ax + self.larg_cube/2 -self.larg_street/2 + street.pre.x*self.larg_cube
                        y = self.ay + street.pre.y*self.larg_cube

                    g.sman.modify(self.sprids[street.name],(x,y))

                elif street.name == 'home':
                    x = self.ax + street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    y = self.ay + street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    g.sman.modify(self.sprids[street.name],(x,y))

                elif isinstance(street,o2.Shop) or isinstance(street,o2.SpecialHouse):
                    x = self.ax + street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    y = self.ay + street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    g.sman.modify(self.sprids[street.name],(x,y))

            # update all guys
            for guy in p.GUYS:

                guy_street = o2.NY.CITY[guy.street]

                # get pos
                if type(guy_street) == o2.Street: # si le perso se trouve dans une rue

                    perc = guy_street.get_pos(guy)

                    vert = guy_street.pre.vert
                    if vert:
                        px = g.sman.spr(self.sprids[guy_street.name]).x - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                        py = g.sman.spr(self.sprids[guy_street.name]).y + perc*g.sman.spr(self.sprids[guy_street.name]).height
                    else:
                        py = g.sman.spr(self.sprids[guy_street.name]).y - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                        px = g.sman.spr(self.sprids[guy_street.name]).x + perc*g.sman.spr(self.sprids[guy_street.name]).width
                else: #guy_street.name == 'home': # si le perso se trouve dans une maison
                    px = self.ax + guy_street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    py = self.ay + guy_street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    px += self.larg_cube/2
                    py += self.larg_cube/2

                if not 'perso_'+guy.name in self.sprids:
                    self.addSpr('perso_'+guy.name,guy.textids['nothing']['R'][0],(px,py), group='hud22')
                    scale = self.pad/g.sman.spr(self.sprids['perso_'+guy.name]).width
                    g.sman.modify(self.sprids['perso_'+guy.name],scale=(scale,scale),anchor='center')
                else:
                    g.sman.modify(self.sprids['perso_'+guy.name],pos=(px,py),anchor='center')

            # get pos
            if type(perso_street) == o2.Street: # si le perso se trouve dans une rue

                perc = perso_street.get_pos(self.perso)

                vert = perso_street.pre.vert
                if vert:
                    px = g.sman.spr(self.sprids[perso_street.name]).x - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                    py = g.sman.spr(self.sprids[perso_street.name]).y + perc*g.sman.spr(self.sprids[perso_street.name]).height
                else:
                    py = g.sman.spr(self.sprids[perso_street.name]).y - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                    px = g.sman.spr(self.sprids[perso_street.name]).x + perc*g.sman.spr(self.sprids[perso_street.name]).width
            else: #perso_street.name == 'home': # si le perso se trouve dans une maison
                px = self.ax + perso_street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                py = self.ay + perso_street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                px += self.larg_cube/2
                py += self.larg_cube/2

            # create and or change pos
            if not 'perso_spr' in self.sprids:
                self.addSpr('perso_spr',self.perso.textids['nothing']['R'][0],(px,py), group='hud22')
                scale = self.pad/g.sman.spr(self.sprids['perso_spr']).width
                g.sman.modify(self.sprids['perso_spr'],scale=(scale,scale),anchor='center')
            else:
                g.sman.modify(self.sprids['perso_spr'],pos=(px,py),anchor='center')

class PersoHUD(HUD):

    def __init__(self,perso):

        super(PersoHUD, self).__init__(group='ui',name='perso')
        #print(self.group)

        self.perso = perso

        self.box = box(1700,460+150,200,400)
        self.padding = 64

        self.addCol('bg',self.box,group='ui-1')

        ## name
        self.addLab('name',self.perso.name,(self.box.cx,self.box.y+self.box.h-50),anchor=('center','center'))

        ## coin

        xcoin = self.box.cx
        ycoin = self.lab('name').y  - self.padding

        self.addSpr('coin_spr',g.TEXTIDS['ux'][0],(xcoin,ycoin - g.tman.textures[g.TEXTIDS['ux'][0]].height/2))
        self.addLab('coin_lab',convert_huge_nb(self.perso.money),(xcoin ,ycoin),font_name=1,font_size=20,color=c['yellow'],anchor=('right','center'))

        ## fans

        xfan = self.box.cx
        yfan = self.lab('coin_lab').y - self.padding

        self.addSpr('fan_spr',g.TEXTIDS['ux'][1],(xfan,yfan - g.tman.textures[g.TEXTIDS['ux'][1]].height/2))
        self.addLab('fan_lab',convert_huge_nb(self.perso.nb_fans),(xfan ,yfan),font_name=1,font_size=20,color=c['lightgreen'],anchor=('right','center'))

        ## fans

        xstream = self.box.cx
        ystream = self.lab('fan_lab').y - self.padding

        self.addSpr('stream_spr',g.TEXTIDS['ux'][2],(xstream,ystream - g.tman.textures[g.TEXTIDS['ux'][2]].height/2))
        self.addLab('stream_lab',convert_huge_nb(self.perso.nb_streams),(xstream ,ystream),font_name=1,font_size=20,color=c['lightblue'],anchor=('right','center'))


        ## pressX
        self.addLab('pressX','X to hide',(self.box.cx,self.box.y+20),font_name=1,font_size=10,color=c['black'],anchor=('center','center'))

    def update(self):

        g.lman.set_text(self.labids['coin_lab'],convert_huge_nb(self.perso.money))
        g.lman.set_text(self.labids['fan_lab'],convert_huge_nb(self.perso.nb_fans))
        g.lman.set_text(self.labids['stream_lab'],convert_huge_nb(self.perso.nb_streams))

    def unhide(self,hide=False):

        g.sman.unhide(self.sprids,hide)
        g.lman.unhide(self.labids,hide)
        g.pman.unhide('icons',hide)
        self.visible = not hide

class LifeHUD(HUD):

    def __init__(self,perso):

        super(LifeHUD, self).__init__(group='hud2',name='life')
        #print(self.group)

        self.perso = perso

        #self.box = box(1700,460+150,200,400)
        self.anc = (20,20)

        size_lifebar = 400
        size_fill = (self.perso.life*size_lifebar)/self.perso.max_life


        self.addSpr('l',g.TEXTIDS['utils'][4],self.anc,group='hud2')
        self.addSpr('r',g.TEXTIDS['utils'][4],(self.anc[0]+size_lifebar,self.anc[1]),group='hud2')
        self.addSpr('mid',g.TEXTIDS['utils'][3],self.anc,group='hud2')
        g.sman.modify(self.sprids['mid'],scale=(size_lifebar/32,1))

        self.addSpr('fill',g.TEXTIDS['utils'][5],self.anc,group='hud2-1')
        g.sman.modify(self.sprids['fill'],scale=(size_fill/32,1))

        ### UI
        self.ui = Life_UI(box(*self.anc,self.spr('fill').width,self.spr('fill').height),self.perso)

    def update(self):

        size_lifebar = 400
        size_fill = (self.perso.life*size_lifebar)/self.perso.max_life
        g.sman.modify(self.sprids['r'],(self.anc[0]+size_lifebar,self.anc[1]))
        g.sman.modify(self.sprids['mid'],scale=(size_lifebar/32,1))
        g.sman.modify(self.sprids['fill'],scale=(size_fill/32,1))
        self.ui.update()

    def delete(self):
        super(LifeHUD,self).delete()
        self.ui.delete()

class CredHUD(HUD):

    def __init__(self,perso):

        super(CredHUD, self).__init__(group='hud2',name='cred')
        #print(self.group)

        self.perso = perso

        self.anc = (20,20+40)

        size_lifebar = 400
        size_fill = (abs(self.perso.cred)*size_lifebar/2)/100

        if self.perso.cred >=0:
            ancmid = self.anc[0]+size_lifebar/2,self.anc[1]
        else:
            ancmid = self.anc[0]+size_lifebar/2-size_fill,self.anc[1]

        self.addSpr('l',g.TEXTIDS['utils'][4],self.anc,group='hud2')
        self.addSpr('r',g.TEXTIDS['utils'][4],(self.anc[0]+size_lifebar,self.anc[1]),group='hud2')
        self.addSpr('mid',g.TEXTIDS['utils'][3],self.anc,group='hud2')
        g.sman.modify(self.sprids['mid'],scale=(size_lifebar/32,1))


        self.addSpr('fill',g.TEXTIDS['utils'][6],ancmid,group='hud2-1')
        g.sman.modify(self.sprids['fill'],scale=(size_fill/32,1))

        ### UI
        self.ui = Cred_UI(box(*self.anc,self.spr('mid').width,self.spr('mid').height),self.perso)

    def update(self):

        size_lifebar = 400
        size_fill = (abs(self.perso.cred)*size_lifebar/2)/100

        if self.perso.cred >=0:
            ancmid = self.anc[0]+size_lifebar/2,self.anc[1]
        else:
            ancmid = self.anc[0]+size_lifebar/2-size_fill,self.anc[1]

        g.sman.modify(self.sprids['r'],(self.anc[0]+size_lifebar,self.anc[1]))
        g.sman.modify(self.sprids['mid'],scale=(size_lifebar/32,1))
        g.sman.modify(self.sprids['fill'],pos=ancmid,scale=(size_fill/32,1))
        self.ui.update()

    def delete(self):
        super(CredHUD,self).delete()
        self.ui.delete()

class FedHydHUD(HUD):

    def __init__(self,perso):

        super(FedHydHUD, self).__init__(group='hud2',name='life')

        self.perso = perso
        self.anc = (20,60)
        dx = g.SPR + 10
        sy = g.SPR/3
        dy = g.SPR/2 - sy/2

        size_lifebar = 300
        size_fed = (self.perso.fed*size_lifebar)/100
        size_hyd = (self.perso.hyd*size_lifebar)/100

        #self.addSpr('l',g.TEXTIDS['utils'][4],self.anc,group='hud2')
        #self.addSpr('r',g.TEXTIDS['utils'][4],(self.anc[0]+size_lifebar,self.anc[1]),group='hud2')
        #self.addSpr('mid',g.TEXTIDS['utils'][3],self.anc,group='hud2')
        #g.sman.modify(self.sprids['mid'],scale=(size_lifebar/32,1))

        x,y = self.anc

        self.addSpr('water',g.TEXTIDS['items']['bottle'],(x,y),group='hud2-1')
        g.sman.modify(self.sprids['water'],scale=(0.5,0.5))
        self.addSpr('hyd',g.tman.addCol(color='clearwater'),(x+dx,y+dy),group='hud2-1')
        g.sman.modify(self.sprids['hyd'],scale=(size_hyd/g.SPR,sy/g.SPR))

        y += g.SPR + 5

        self.addSpr('food',g.TEXTIDS['items']['noodle'],(x,y),group='hud2-1')
        g.sman.modify(self.sprids['food'],scale=(0.5,0.5))
        self.addSpr('fed',g.tman.addCol(color='noodle'),(x+dx,y+dy),group='hud2-1')
        g.sman.modify(self.sprids['fed'],scale=(size_fed/g.SPR,sy/g.SPR))


        ### UI
        #self.ui = Life_UI(box(*self.anc,self.spr('fill').width,self.spr('fill').height),self.perso)

    def update(self):
        sy = g.SPR/3

        size_lifebar = 300
        size_fed = (self.perso.fed*size_lifebar)/100
        g.sman.modify(self.sprids['fed'],scale=(size_fed/g.SPR,sy/g.SPR))

        size_hyd = (self.perso.hyd*size_lifebar)/100
        g.sman.modify(self.sprids['hyd'],scale=(size_hyd/g.SPR,sy/g.SPR))

        #self.ui.update()

    def delete(self):
        super(FedHydHUD,self).delete()
        #self.ui.delete()

class RelHUD(HUD):

    def __init__(self,hum):

        super(RelHUD, self).__init__(group='hud2',name='relhud',vis=False)

        self.hum = hum

        cx,cy=g.scr.c
        self.box = box(cx-300,cy-450,600,900)

        self.pad = 25
        self.padding = 50

        #col = (*c['delta_blue'][:3],170)
        self.addCol('bg',self.box,color='delta_blue_faded',group='hud2-1')
        self.addLab('title','relations of '+self.hum.name,(self.box.cx,self.box.fy+self.padding),font_name=1,font_size=20,anchor=('center','center'))

    def update(self):

        if self.visible:

            max_aff = 10

            aff = 0
            y = self.box.fy-(3/4)*self.padding
            xname = self.box.cx - self.box.w/4
            xthg = self.box.cx + self.box.w/4

            size_max_bar = self.box.w/2

            ## EN 1er on affiche les humains dans l'environnement
            for hum in self.hum.hum_env:
                if aff <= max_aff:
                    if hum.id not in self.labids :
                        self.addLab(hum.id,hum.name,(xname,y),font_size=20,anchor=('center','center'),replace=False)
                        self.addLab(hum.id+'o','o',(xthg,y),anchor=('center','center'),replace=False,color=c['green'])

                        y -= self.pad

                        feel = self.hum.get_feel(hum)
                        size_fill = (abs(feel)*size_max_bar/2)/100
                        if feel >=0:
                            xfeel = self.box.cx
                        else:
                            xfeel = self.box.cx-size_fill

                        self.addSpr(hum.id+'hate/like',g.TEXTIDS['utils'][6],(xfeel,y))
                        self.modifySpr(hum.id+'hate/like',scale=(size_fill/32,5/32))
                    else:
                        self.modifyLab(hum.id,(xname,y),(255,255,255,255))
                        self.modifyLab(hum.id+'o',(xthg,y),c['green'])
                        y -= self.pad

                        feel = self.hum.get_feel(hum)
                        size_fill = (abs(feel)*size_max_bar/2)/100
                        if feel >=0:
                            xfeel = self.box.cx
                        else:
                            xfeel = self.box.cx-size_fill

                        self.modifySpr(hum.id+'hate/like',(xfeel,y),scale=(size_fill/32,None))


                    y -= self.padding
                    aff +=1

                elif hum.id in self.labids :
                    self.delLab(hum.id)
                    self.delLab(hum.id+'o')
                    self.delSpr(hum.id+'hate/like')


            # on laisse une ptite place vide pour bien voir
            if len(self.hum.hum_env) > 0:
                y -= self.padding+self.pad
            else:
                max_aff+=1

            col = (255,255,255,170)
            colred = (*c['red'][:3],170)

            ## ENsuite ceux qui n'y sont pas en faded
            #od = OrderedDict(self.hum.relations.items())
            #print(self.hum.relations.items())
            od = OrderedDict(sorted(self.hum.relations.items(), key=lambda t: t[1]['last'],reverse=True))
            for hum in od:
                if hum not in self.hum.hum_env:
                    if aff <= max_aff:
                        #name + time elapsed
                        if hum.id not in self.labids :
                            self.addLab(hum.id,hum.name,(xname,y),font_size=20,anchor=('center','center'),replace=False,color=col)
                            self.addLab(hum.id+'o','o',(xthg,y),anchor=('center','center'),replace=False,color=colred)

                            y -= self.pad

                            feel = self.hum.get_feel(hum)
                            size_fill = (abs(feel)*size_max_bar/2)/100
                            if feel >=0:
                                xfeel = self.box.cx
                            else:
                                xfeel = self.box.cx-size_fill

                            self.addSpr(hum.id+'hate/like',g.TEXTIDS['utils'][6],(xfeel,y))
                            self.modifySpr(hum.id+'hate/like',scale=(size_fill/32,5/32))
                        else:
                            self.modifyLab(hum.id,(xname,y),col)
                            self.modifyLab(hum.id+'o',(xthg,y),colred)
                            y -= self.pad

                            feel = self.hum.get_feel(hum)
                            size_fill = (abs(feel)*size_max_bar/2)/100
                            if feel >=0:
                                xfeel = self.box.cx
                            else:
                                xfeel = self.box.cx-size_fill

                            self.modifySpr(hum.id+'hate/like',(xfeel,y),scale=(size_fill/32,None))

                        y -= self.padding
                        aff +=1

                    elif hum.id in self.labids :
                        self.delLab(hum.id)
                        self.delLab(hum.id+'o')
                        self.delSpr(hum.id+'hate/like')

class MiniRelHUD(HUD):

    def __init__(self,hum):

        super(MiniRelHUD, self).__init__(group='hud2',name='minirelhud',vis=False)

        self.hum = hum
        self.target=None

        x,y = 20,100
        w,h = 300,80
        self.box = box(x,y,w,h)

        self.pad = 25
        self.padding = 50

        #col = (*c['delta_blue'][:3],170)
        self.addCol('bg',self.box,color='delta_blue_faded',group='hud2-1')

    def assign_target(self,hum):
        self.target = hum
        self.addLab('title','relations of '+self.target.name,(self.box.cx,self.box.fy+self.pad),font_name=1,font_size=20,anchor=('center','center'))

    def update(self):

        if self.visible and self.target!=None:

            y = self.box.fy-(3/4)*self.padding
            xname = self.box.cx - self.box.w/4
            xthg = self.box.cx + self.box.w/4

            size_max_bar = self.box.w/2

            hum = self.hum
            if hum in self.target.relations:

                feel = self.target.get_feel(hum)
                size_fill = (abs(feel)*size_max_bar/2)/100
                if feel >=0:
                    xfeel = self.box.cx
                else:
                    xfeel = self.box.cx-size_fill

                if hum in self.target.hum_env:
                    if hum.id not in self.labids :
                        self.addLab(hum.id,hum.name,(xname,y),font_size=20,anchor=('center','center'),replace=False)
                        self.addLab(hum.id+'o','o',(xthg,y),anchor=('center','center'),replace=False,color=c['green'])
                        y -= self.pad
                        self.addSpr(hum.id+'hate/like',g.TEXTIDS['utils'][6],(xfeel,y))
                        self.modifySpr(hum.id+'hate/like',scale=(size_fill/32,5/32))
                    else:
                        self.modifyLab(hum.id,(xname,y),(255,255,255,255))
                        self.modifyLab(hum.id+'o',(xthg,y),c['green'])
                        y -= self.pad
                        self.modifySpr(hum.id+'hate/like',(xfeel,y),scale=(size_fill/32,None))
                else:
                    col = (255,255,255,170)
                    colred = (*c['red'][:3],170)
                    if hum.id not in self.labids :
                        self.addLab(hum.id,hum.name,(xname,y),font_size=20,anchor=('center','center'),replace=False,color=col)
                        self.addLab(hum.id+'o','o',(xthg,y),anchor=('center','center'),replace=False,color=colred)
                        y -= self.pad
                        self.addSpr(hum.id+'hate/like',g.TEXTIDS['utils'][6],(xfeel,y))
                        self.modifySpr(hum.id+'hate/like',scale=(size_fill/32,5/32))
                    else:
                        self.modifyLab(hum.id,(xname,y),col)
                        self.modifyLab(hum.id+'o',(xthg,y),colred)
                        y -= self.pad
                        self.modifySpr(hum.id+'hate/like',(xfeel,y),scale=(size_fill/32,None))

class SonHUD(HUD):

    def __init__(self,perso):

        super(SonHUD, self).__init__(group='ui',name='son')
        #print(self.group)

        self.perso = perso

        self.box = box(1650-820,20,800,64)
        self.padding = 20

        #self.addCol('bg',self.box,group='ui-1')


    def update(self):

        for son in self.perso.invhud.inventory['son']:
            if son._released:
                pass

        """g.lman.set_text(self.labids['coin_lab'],convert_huge_nb(self.perso.money))
        g.lman.set_text(self.labids['fan_lab'],convert_huge_nb(self.perso.nb_fans))
        g.lman.set_text(self.labids['stream_lab'],convert_huge_nb(self.perso.nb_streams))"""
        pass

    def unhide(self,hide=False):

        """g.sman.unhide(self.sprids,hide)
        g.lman.unhide(self.labids,hide)
        g.pman.unhide('icons',hide)"""
        self.visible = not hide

class WriteHUD(HUD):

    def __init__(self):

        super(WriteHUD, self).__init__(group='hud1',name='write',vis=False)

        ##

        self.ui = None

        self.box = box(400,300,1000,600)
        self.padding = 50

        self.addCol('bg',self.box,group='hud-1')

        self.box2 = box(self.box.x+self.padding,self.box.y+2*self.padding,self.box.w-2*self.padding,self.box.h-3*self.padding)

        self.addCol('bg2',self.box2,color='delta_blue',group='hud')

        #self.addLab('quality',convert_quality(self.plum.quality),(self.box.x+self.box.w-self.padding,self.box.cy),anchor=('center','center'))
        self.addLab('pressE','E to write --- ESC to leave',(self.box.cx,self.box.y+self.padding),font_name=1,font_size=20,anchor=('center','center'))
        self.addLab('lit','LIT - zone d\'ecriture',(self.box.cx,self.box.y+self.box.h+self.padding),font_name=1,font_size=20,anchor=('center','center'))

    def delete_phase(self,ui=True):

        if 'phaz_spr' in self.sprids:
            g.sman.delete(self.sprids['phaz_spr'])
            del self.sprids['phaz_spr']

        if 'phaz_content' in self.labids:
            g.lman.delete(self.labids['phaz_content'])
            del self.labids['phaz_content']

        if 'phaz_qua' in self.labids:
            g.lman.delete(self.labids['phaz_qua'])
            del self.labids['phaz_qua']

        if 'phaz_cred' in self.labids:
            g.lman.delete(self.labids['phaz_cred'])
            del self.labids['phaz_cred']

        if 'phaz_them' in self.labids:
            g.lman.delete(self.labids['phaz_them'])
            del self.labids['phaz_them']

        if self.ui != None and ui:
            self.ui.delete()
            self.ui = None

    def write(self,phase):

        text = g.TEXTIDS['phase'][convert_quality(phase.quality)[0]]

        self.addSpr('phaz_spr',text)
        #g.sman.modify(self.sprids['phaz_spr'],scale=(0.8,0.8))
        g.sman.modify(self.sprids['phaz_spr'],pos=(self.box2.cx - self.spr('phaz_spr').width/2,self.box2.cy - self.spr('phaz_spr').height/2))

        y = (( self.box2.cy + self.spr('phaz_spr').height/2 )  +  (self.box2.y + self.box2.h) )/2
        self.addLab('phaz_content',phase.content,(self.box2.cx,y),anchor=('center','center'),color=c['black'])

        x = (self.box2.cx + self.spr('phaz_spr').width/2  +  (self.box2.x + self.box2.w) )/2
        self.addLab('phaz_qua',convert_quality(phase.quality),(x,self.box2.cy),anchor=('center','center'),color=c['black'],font_name=1,font_size=100)

        x = (self.box2.cx - self.spr('phaz_spr').width/2  +  (self.box2.x) )/2
        self.addLab('phaz_cred',convert_cred(phase.cred),(x,self.box2.cy),anchor=('center','center'),color=c['black'],font_name=1,font_size=100)

        #y = (( self.box2.cy - self.spr('phaz_spr').height/2 )  +  (self.box2.y) )/2
        y = ( self.box2.cy - self.spr('phaz_spr').height/2 ) - 30
        self.addLab('phaz_them','thème : '+phase.them,(self.box2.cx,y),anchor=('center','center'),font_size=20)

        x,y,w,h = self.box2.cx - self.spr('phaz_spr').width/2 , self.box2.cy - self.spr('phaz_spr').height/2 , self.spr('phaz_spr').width , self.spr('phaz_spr').height

        if self.ui != None:
            self.ui.delete()
        self.ui = Writingphase_UI(box(x,y,w,h),phase)

    def catch_or_drop(self,x,y,perso):

        self.ui.check_pressed()
        if self.ui.caught:
            perso.invhud.unhide()
            self.delete_phase(False)
            return 1
        elif self.ui.dropped:
            if collisionAX(self.box.realbox,(x,y)):
                self.write(self.ui.phase)
            elif perso.invhud.visible and collisionAX(perso.invhud.box.realbox,(x,y)):
                perso.grab(self.ui.phase,True)
                self.delete_phase()
            elif perso.selhud.visible and (collisionAX(perso.selhud.box.realbox,(x,y)) or collisionAX(perso.selhud.box2.realbox,(x,y))):
                perso.grab(self.ui.phase)
                self.delete_phase()
            else:
                self.delete_phase()
            return -1
        return 0

class StudHUD(HUD):

    def __init__(self):

        super(StudHUD, self).__init__(group='hud1',name='stud',vis=False)

        ##

        #self.ui = None

        self.box = box(400,300,1200,650)
        self.padding = 50

        self.item_caught = None

        self.uis = {}
        self.uis['instru'] = None
        self.uis['phase0'] = None
        self.uis['phase1'] = None
        self.uis['phase2'] = None
        self.uis['phase3'] = None
        self.uis['son'] = None

        self.boxs = {}
        self.boxs['instru'] = box( 400+75+11,300+275+11,128,128 )
        self.boxs['phase0'] = box( 400+325+11,300+440+11,128,128 )
        self.boxs['phase1'] = box( 400+675+11,300+440+11,128,128 )
        self.boxs['phase2'] = box( 400+325+11,300+110+11,128,128 )
        self.boxs['phase3'] = box( 400+675+11,300+110+11,128,128 )
        self.boxs['son'] = box( 400+950+11,300+275+11,128,128 )

        self.addSpr('bg',g.TEXTIDS['studhud'],(400,300),'hud')

        #self.addLab('quality',convert_quality(self.plum.quality),(self.box.x+self.box.w-self.padding,self.box.cy),anchor=('center','center'))
        self.addLab('pressE','E to assemble a song --- ESC to leave',(400+462.5,self.box.y+self.padding),font_name=1,font_size=20,anchor=('center','center'))
        self.addLab('stud','STUD - zone d\'enregistrement',(self.box.cx,self.box.y+self.box.h+self.padding),font_name=1,font_size=20,anchor=('center','center'))

        self.instru = 0
        self.phases = 0
        self.son = 0

    def assemble(self,perso):

        if self.phases == 4 and self.instru == 1 and self.son == 0: # on peut assembler

            instru = self.uis['instru'].item
            ph = []
            for i in range(4):
                ph.append(self.uis['phase'+str(i)].item)

            son = Son(instru,ph,perso.name)

            self.delete_ui('instru')
            for i in range(4):
                self.delete_ui('phase'+str(i))

            self.uis['son'] = Invent_UI(self.boxs['son'],son,self.visible,scale=(0.4,0.4))
            self.son = 1
        else:
            print('fréro ta r capté')

    def delete_ui(self,lab):

        self.uis[lab].delete()
        self.uis[lab] = None
        if lab[:3] == 'ins':
            self.instru = 0
        elif lab[:3] == 'pha':
            self.phases -= 1
        elif lab[:3] == 'son':
            self.son = 0

    def catch_or_drop(self,x,y,perso):

        if self.item_caught != None:
            ## on check kelui pour vwar si on l'drop

            if collisionAX(self.box.realbox,(x,y)):
                if type(self.item_caught.item).__name__ != 'Son':
                    self.catch(self.item_caught.item)
                    self.item_caught.delete()
                    self.item_caught = None
                else:
                    return 0

            elif perso.invhud.visible and collisionAX(perso.invhud.box.realbox,(x,y)):
                perso.grab(self.item_caught.item)
                self.item_caught.delete()
                self.item_caught = None
            else:
                self.item_caught.delete()
                self.item_caught = None
            return -1
        else:
            ## on check touu pour vwar si on en catch

            for lab in self.uis:
                ui = self.uis[lab]
                if ui != None:
                    ui.check_pressed()
                    if ui.caught:
                        self.item_caught = Invent_UI(self.boxs[lab],ui.item,self.visible)
                        self.item_caught.activate()
                        self.delete_ui(lab)

                        return 1
        return 0

    def catch(self,thg):

        if type(thg).__name__ == 'Phase' and self.phases < 4:
            for lab in self.uis:
                if lab[:3] == 'pha' and self.uis[lab] == None:
                    self.uis[lab] = Invent_UI(self.boxs[lab],thg,self.visible,scale=(0.4,0.4))
                    self.phases+=1
                    break

        elif type(thg).__name__ == 'Instru' and self.instru == 0:
            self.uis['instru'] = Invent_UI(self.boxs['instru'],thg,self.visible,scale=(0.4,0.4))
            self.instru = 1
        else:
            print('u cant drop this here cheh')

    def unhide(self,hide=False):
        super(StudHUD,self).unhide(hide)

        if hide and self.item_caught != None:
            self.catch(self.item_caught.item)
            self.item_caught.delete()
            self.item_caught = None

        for lab in self.uis:
            ui = self.uis[lab]
            if ui != None:
                ui.unhide(hide)

class MarketHUD(HUD):

    def __init__(self,perso):

        super(MarketHUD, self).__init__(group='hud1',name='market',vis=False)

        ##

        self.ui = None

        self.box = box(400,300,1000,650)
        self.padding = 50

        self.item_caught = None

        self.uis = {}
        self.uis['main'] = None
        self.uis['instru0'] = None
        self.uis['instru1'] = None
        self.uis['instru2'] = None
        self.uis['instru3'] = None

        self.old_main_pos = None

        self.boxs = {}
        self.boxs['main'] = box( 400+230,300+222,256,256 )
        self.boxs['instru0'] = box( 400+820+1,300+476+11,128,128 )
        self.boxs['instru1'] = box( 400+820+1,300+342+11,128,128 )
        self.boxs['instru2'] = box( 400+820+1,300+208+11,128,128 )
        self.boxs['instru3'] = box( 400+820+1,300+74+11,128,128 )

        self.addSpr('bg',g.TEXTIDS['ordhud'],(400,300),'hud')

        #self.addLab('quality',convert_quality(self.plum.quality),(self.box.x+self.box.w-self.padding,self.box.cy),anchor=('center','center'))
        self.addLab('longclick','longclick on an instru to buy --- ESC to leave',(self.box.cx,self.box.y+self.padding),font_name=1,font_size=20,anchor=('center','center'))
        self.addLab('market','Ordi - achat d\'instrus',(self.box.cx,self.box.y+self.box.h+self.padding),font_name=1,font_size=20,anchor=('center','center'))

        self.instru = 0
        self.perso = perso
        self.add_instru(0)

    def delete_ui(self,lab):

        self.uis[lab].delete()
        self.uis[lab] = None
        if lab[:3] == 'ins':
            self.instru -= 1
        elif lab == 'main':
            for lab2 in ['qua','bt','price','status']:
                g.lman.delete(self.labids[lab+'_'+lab2])
                del self.labids[lab+'_'+lab2]

            g.sman.delete(self.sprids[lab+'_price'])
            del self.sprids[lab+'_price']

    def catch_or_drop(self,x,y):

        #print("wesh")

        if self.item_caught != None:
            ## on check kelui pour vwar si on l'drop

            if collisionAX(self.box.realbox,(x,y)):
                self.inspect(self.item_caught.item)
            elif self.perso.invhud.visible and collisionAX(self.perso.invhud.box.realbox,(x,y)):
                self.perso.grab(self.item_caught.item)
            self.item_caught.delete()
            self.item_caught = None
            return -1
        else:
            ## on check touu pour vwar si on en catch

            for lab in self.uis:
                ui = self.uis[lab]

                if ui != None and lab != 'main':
                    ui.check_pressed()
                    if ui.caught:
                        self.inspect(ui.item,int(lab[-1]))
                        self.delete_ui(lab)
                        #ui.reset()

                elif ui != None: # on est dans le main
                    if self.perso in ui.item.owners:
                        ui.check_pressed()
                        if ui.caught:
                            self.item_caught = Invent_UI(self.boxs[lab],ui.item,self.visible)
                            self.item_caught.activate()
                            self.delete_ui(lab)

                            return 1

        return 0

    def inspect(self,ins,pos=None):

        if self.uis['main'] != None:

            if self.perso in self.uis['main'].item.owners:
                self.perso.grab(self.uis['main'].item)
            elif self.old_main_pos != None and self.old_main_pos <= 3:
                self.uis['instru'+str(self.old_main_pos)] = Invent_UI(self.boxs['instru'+str(self.old_main_pos)],self.uis['main'].item,self.visible,(0.4,0.4))
            self.delete_ui('main')

        self.old_main_pos = pos

        self.uis['main'] = Invent_UI(self.boxs['main'],ins,self.visible,(0.8,0.8))
        padding = 150

        # creating new details
        self.addLab('main_qua',convert_quality(ins.quality),(self.boxs['main'].cx,self.boxs['main'].cy+padding),font_name=1,anchor=('center','center'),color=c['white'],font_size=50)
        self.addLab('main_bt',ins.author.name,(self.boxs['main'].cx,self.boxs['main'].cy-padding),anchor=('center','center'),color=c['white'],font_size=30)
        self.addLab('main_price',convert_huge_nb(ins.price),(self.box.x+129,self.boxs['main'].cy),font_name=1,anchor=('right','center'),color=c['yellow'],font_size=30)
        self.addSpr('main_price',g.TEXTIDS['ux'][0],(self.box.x+129,self.boxs['main'].cy - g.tman.textures[g.TEXTIDS['ux'][0]].height/2))

        if self.perso in ins.owners:
            status,color = "purchased",c['green']
        else:
            status,color = "on sale",c['red']

        self.addLab('main_status',status,(self.box.x+609,self.boxs['main'].cy),anchor=('center','center'),color=color,font_size=30)

    def add_instru(self,dt):

        ins = rinstru()

        # deleting last instru
        if self.uis['instru3'] != None:
            self.delete_ui('instru3')

        # moving each instru and details to next box
        for i in range(2,-1,-1):

            # each instru
            self.uis['instru'+str(i+1)] = self.uis['instru'+str(i)]
            if self.uis['instru'+str(i+1)] != None:
                self.uis['instru'+str(i+1)].upbox(self.boxs['instru'+str(i+1)])
        if self.old_main_pos != None:
            self.old_main_pos += 1

        # replacing the first box with the new instru
        self.uis['instru0'] = Invent_UI(self.boxs['instru0'],ins,self.visible,(0.4,0.4))
        self.instru += 1
        # recalling this function
        t = r.randint(2,10)
        #print('wow new instru :',ins,'next in',t,'secondes')
        g.bertran.schedule_once(self.add_instru,t)

    def actualise(self):

        if self.uis['main'] != None:
            ins = self.uis['main'].item

            padding = 150

            # creating new details
            self.addLab('main_qua',convert_quality(ins.quality),(self.boxs['main'].cx,self.boxs['main'].cy+padding),anchor=('center','center'),color=c['white'],font_name=1,font_size=50)
            self.addLab('main_bt',ins.author.name,(self.boxs['main'].cx,self.boxs['main'].cy-padding),anchor=('center','center'),color=c['white'],font_size=30)
            self.addLab('main_price',convert_huge_nb(ins.price),(self.box.x+129,self.boxs['main'].cy),anchor=('right','center'),color=c['yellow'],font_name=1,font_size=30)
            self.addSpr('main_price',g.TEXTIDS['ux'][0],(self.box.x+129,self.boxs['main'].cy - g.tman.textures[g.TEXTIDS['ux'][0]].height/2))

            if self.perso in ins.owners:
                status,color = "purchased",c['green']
            else:
                status,color = "on sale",c['red']

            self.addLab('main_status',status,(self.box.x+609,self.boxs['main'].cy),anchor=('center','center'),color=color,font_size=30)

    def buy_instru(self):

        if self.uis['main'] != None and self.perso.money >= self.uis['main'].item.price:
            self.perso.add_money(-self.uis['main'].item.price)
            self.uis['main'].item.add_owner(self.perso)
            self.actualise()

        #print('u wanna buy instru n*'+str(k), 'it will cost'+convert_huge_nb(self.uis['instru'+str(k)].item.price),'$')

    def unhide(self,hide=False):
        super(MarketHUD,self).unhide(hide)

        if hide and self.item_caught != None:
            perso.grab(self.item_caught.item)
            self.item_caught.delete()
            self.item_caught = None

        for lab in self.uis:
            ui = self.uis[lab]
            if ui != None:
                ui.unhide(hide)

#---# hud spéciaux inventaire/selecteur

class InventHUD(HUD):

    def __init__(self,perso,fill=True):

        super(InventHUD, self).__init__(group='hud21',name='inv',vis=False)

        self.perso = perso

        self.item_caught = None

        # inventory
        self.uis = {}
        self.uis['phase'] = []
        self.uis['instru'] = []
        self.uis['son'] = []
        self.uis['general'] = []
        self.uis['plume'] = []

        ### GENERAL

        self.box = box(20,200,338,800)
        self.padding = 64
        self.padding2 = 20
        self.lilpadding = 12
        self.lilpadding2 = 6


        ### COLORS

        self.addCol('bg',self.box,group='hud2-1')

        self.box2 = box(self.box.x+self.padding2,self.box.y+self.padding2,self.box.w-2*self.padding2,self.box.h-self.padding2-100)

        self.addCol('bg2',self.box2,color='delta_blue',group='hud2')



        ### MENUS

        self.menus = ['general','sound']
        self.menu = 'general'
        self.btns = {}

        self.menus_cont = {}
        self.menus_cont['general'] = ['general']
        self.menus_cont['sound'] = ['plume','son','instru','phase']

        h = 90
        for i in range(len(self.menus)):
            zone_box = box(self.box2.fx,self.box2.y+i*h,h,h)
            x,y = zone_box.cxy
            x -= 32
            y -= 32
            self.addSpr('menu_'+self.menus[i],g.TEXTIDS['ux'][4+i],(x,y),group='hud3')
            self.btns[self.menus[i]] = Toggle(zone_box,self.roll_menu,[self.menus[i]],self.menus[i],vis=self.visible)

        self.btns[self.menu].toggle()

        ### PARTIE DETAILS

        self.autorize_deta = True
        self.deta_visible = False
        self.detaids = {}
        self.detaids['spr'] = {}
        self.detaids['bg'] = {}
        self.detaids['lab'] = {}

        height_detail = self.box.h-len(self.menus)*h-self.padding2
        width_detail = 180

        self.box3 = box(self.box.fx,self.box.fy-int(height_detail),width_detail,int(height_detail))
        #print(not self.deta_visible)
        self.addCol('bgdeta',self.box3,group='hud2-1',detail=True)
        #g.sman.unhide(self.sprids['bgdeta'],not self.deta_visible)
        #self.detaids.append(self.sprids['bgdeta'])



        ### LABEL inv
        self.addLab('inv_lab','inventory',(self.box.cx,self.box.fy-50),font_name=1,anchor=('center','center'))

        if fill and False:
            #self.update()
            for i in range(r.randint(2,10)):
                ins = Instru(r.random(),r.choice(btmakers))
                ins.add_owner(self.perso)
                self.perso.grab(ins)
            for i in range(r.randint(2,10)):
                ph = []
                for i in range(4):
                    ph.append(Phase(rqua(),rcred()))
                instru = Instru(r.random(),r.choice(btmakers))

                self.perso.grab(Son(instru,ph))

    # add/del/update

    def add_ui(self,item):

        if not isinstance(item,Sound_item):
            # on verifie si on le stacke avec qqch
            for ui in self.uis['general']:
                if type(ui.item) == type(item) and ui.item.stackable(item):
                    ui.item.stack(item.stacked)
                    ui.update()
                    self.update()
                    return
        print('oh yo')

        vis = True
        if not self.visible:
            vis = False
        if isinstance(item,Sound_item) and self.menu == 'general':
            vis = False
        if not isinstance(item,Sound_item) and self.menu == 'sound':
            vis = False

        if isinstance(item,Sound_item):
            scale = (0.25,0.25)
        else:
            scale = (1,1)

        # on stocke l'ui
        if isinstance(item,Sound_item):
            self.uis[type(item).__name__.lower()].append(Invent_UI(box(w=self.padding,h=self.padding),item,vis,scale=scale))
        else:
            self.uis['general'].append(Invent_UI(box(w=self.padding,h=self.padding),item,vis,scale=scale))

        self.update()

        #print(self.uis)

    def del_ui(self,item,up=True):

        #print(self.uis,item)
        #print(list(map(lambda x:x.item,self.uis['general'])))

        if type(item) == type([]):
            for subitem in item:
                self.del_ui(subitem,False)
        elif item != None:
            if isinstance(item,Sound_item):
                ui = list(filter(lambda x:x.item == item,self.uis[type(item).__name__.lower()]))[0]
                ui.delete()
                self.uis[type(item).__name__.lower()].remove(ui)
            else:
                ui = list(filter(lambda x:x.item == item,self.uis['general']))[0]
                #print(self.uis['general'])
                ui.delete()
                self.uis['general'].remove(ui)

        if up:
            self.update()

    def update(self):

        #self.create_uis()

        if self.menu == 'sound':
            yf = self.box2.fy

            for cquecé in self.menus_cont[self.menu]:
                tab = self.uis[cquecé]
                if tab != []:
                    #cquecé = type(tab[0].item).__name__.lower()
                    self.addLab(cquecé+'s_lab',cquecé+'s',(self.box.cx,yf-self.padding2),font_name=1,color=c['black'],font_size=20,anchor=('center','center'))
                    yf -= self.padding2*2

                    self.uis[cquecé].sort(reverse=True)

                    for i in range(len(self.uis[cquecé])):

                        x = self.box2.x + self.padding/2 + self.lilpadding + (self.padding + self.lilpadding2)*(i%4)
                        y = yf + self.padding/2 - (self.padding + self.lilpadding2)*(i//4 + 1)

                        self.uis[cquecé][i].move(x,y)
                    yf -= (self.padding + self.lilpadding2)*((len(self.uis[cquecé])-1)//4 + 1) + self.lilpadding - self.lilpadding2
                else:
                    if (cquecé+'s_lab') in self.labids:
                        g.lman.delete(self.labids[cquecé+'s_lab'])
                        del self.labids[cquecé+'s_lab']

        elif self.menu == 'general':
            yf = self.box2.fy

            for cquecé in self.menus_cont[self.menu]:
                tab = self.uis[cquecé]
                if tab != []:
                    #self.uis[cquecé].sort(reverse=True)
                    for i in range(len(self.uis[cquecé])):

                        x = self.box2.x + self.padding/2 + self.lilpadding + (self.padding + self.lilpadding2)*(i%4)
                        y = yf + self.padding/2 - (self.padding + self.lilpadding2)*(i//4 + 1)

                        self.uis[cquecé][i].move(x,y)
                    yf -= (self.padding + self.lilpadding2)*((len(self.uis[cquecé])-1)//4 + 1) + self.lilpadding - self.lilpadding2


    # general

    def unhide(self,hide=False):
        super(InventHUD,self).unhide(hide)

        if hide and self.item_caught != None:
            self.item_caught.drop()
            self.item_caught.reset()
            self.item_caught = None
            self.update()

        for cquecé in self.menus_cont[self.menu]:
            for ui in self.uis[cquecé]:
                ui.unhide(hide)

        for menu in self.btns:
            if not hide:
                if menu == self.menu:
                    self.btns[menu].set_act()
                else:
                    self.btns[menu].set_nap()

            self.btns[menu].unhide(hide)

        if (not hide) and (not self.deta_visible):
            self.eff_detail()
        elif hide and self.deta_visible:
            self.eff_detail()

    def catch_or_drop(self,x,y):

        if self.item_caught :
            ## on check kelui pour vwar si on l'drop

            self.item_caught.check_pressed()
            if self.item_caught.dropped:
                if collisionAX(self.box.realbox,(x,y)):
                    self.item_caught.reset()
                    self.item_caught = None
                    self.update()
                    return -1

                elif self.perso.selhud.visible and (collisionAX(self.perso.selhud.box.realbox,(x,y)) or collisionAX(self.perso.selhud.box2.realbox,(x,y))):
                    self.perso.drop(self.item_caught.item,False)
                    self.perso.grab(self.item_caught.item)
                    self.item_caught = None
                    return -1

                elif self.perso.element_colli != None and isinstance(self.perso.element_colli,Zone_ACTIV) and self.perso.element_colli.activated and collisionAX(self.perso.element_colli.hud.box.realbox,(x,y)): # and hasattr(self.perso.element_colli,'hud'):

                    if type(self.perso.element_colli) == Lit and type(self.item_caught.item).__name__ == 'Phase':
                        self.perso.drop(self.item_caught.item,create=False)
                        self.perso.element_colli.hud.write(self.item_caught.item)
                        self.item_caught = None
                        return -1

                    elif type(self.perso.element_colli) == Ordi and type(self.item_caught.item).__name__ == 'Instru':
                        self.perso.element_colli.hud.inspect(self.item_caught.item)
                        self.perso.drop(self.item_caught.item,create=False)
                        self.item_caught = None
                        return -1

                    elif type(self.perso.element_colli) == Studio:

                        if type(self.item_caught.item).__name__ == 'Phase' and self.perso.element_colli.hud.phases < 4:
                            self.perso.element_colli.hud.catch(self.item_caught.item)
                            self.perso.drop(self.item_caught.item,create=False)
                            self.item_caught = None
                            return -1
                        elif type(self.item_caught.item).__name__ == 'Instru' and self.perso.element_colli.hud.instru == 0:
                            self.perso.element_colli.hud.catch(self.item_caught.item)
                            self.perso.drop(self.item_caught.item,create=False)
                            self.item_caught = None
                            return -1

                        else:
                            self.item_caught.check_pressed()

                    else:
                        self.item_caught.check_pressed()

                else:
                    self.perso.drop(self.item_caught.item)
                    self.item_caught = None
                    return -1

        else:
            ## on check touu pour vwar si on en catch

            if self.menu == 'sound':
                for x in self.menus_cont[self.menu]:
                    tab = self.uis[x]
                    for ui in tab:
                        ui.check_pressed()
                        if ui.caught:
                            self.item_caught = ui
                            return 1

            elif self.menu == 'general':
                for ui in self.uis['general']:

                    ui.check_pressed()
                    if ui.caught:
                        self.item_caught = ui
                        return 1

        return 0

    def quick_catch_and_drop(self):

        selector = False

        if self.perso.element_colli != None and isinstance(self.perso.element_colli,Zone_ACTIV) and self.perso.element_colli.activated:

            if type(self.perso.element_colli) == Lit and type(self.item_caught.item).__name__ == 'Phase':
                self.perso.element_colli.hud.write(self.item_caught.item)
                self.perso.drop(self.item_caught.item,create=False)
                self.item_caught = None

            elif type(self.perso.element_colli) == Ordi and type(self.item_caught.item).__name__ == 'Instru':
                self.perso.element_colli.hud.inspect(self.item_caught.item)
                self.perso.drop(self.item_caught.item,create=False)
                self.item_caught = None

            elif type(self.perso.element_colli) == Studio:

                if type(self.item_caught.item).__name__ == 'Phase' and self.perso.element_colli.hud.phases < 4:
                    self.perso.element_colli.hud.catch(self.item_caught.item)
                    self.perso.drop(self.item_caught.item,create=False)
                    self.item_caught = None

                elif type(self.item_caught.item).__name__ == 'Instru' and self.perso.element_colli.hud.instru == 0:
                    self.perso.element_colli.hud.catch(self.item_caught.item)
                    self.perso.drop(self.item_caught.item,create=False)
                    self.item_caught = None

                else:
                    selector = True

            else:
                selector = True

        else:
            selector = True

        if selector:
            self.perso.drop(self.item_caught.item,False)
            self.perso.grab(self.item_caught.item)
            self.item_caught = None
            return -1

    def check_hoover(self,x,y):

        # inventory
        something_to_aff = False

        for cquecé in self.menus_cont[self.menu]:
            for ui in self.uis[cquecé]:
                ui.check_mouse(x,y)
                if ui._hoover:
                    something_to_aff = True
                    self.aff_detail(ui)

        if not something_to_aff:
            self.eff_detail()

        # menus
        for menu in self.btns:
            self.btns[menu].check_mouse(x,y)


    ## de base

    def addSpr(self,key,textid,xy_pos=(0,0),group=None,detail=False):
        super(InventHUD,self).addSpr(key,textid,xy_pos,group)
        if detail:
            self.detaids['spr'][key]=self.sprids[key]
            del self.sprids[key]

    def addCol(self,key,box,color='delta_purple',group=None,detail=False):
        super(InventHUD,self).addCol(key,box,color,group)
        if detail:
            self.detaids['bg'][key]=self.sprids[key]
            del self.sprids[key]

    def addLab(self,key,contenu,xy_pos=(0,0),group=None,font_name=1,font_size=30,anchor=('left','bottom'),color=(255,255,255,255),detail=False):
        super(InventHUD,self).addLab(key,contenu,xy_pos,group,font_name,font_size,anchor,color)
        if detail:
            self.detaids['lab'][key]=self.labids[key]
            del self.labids[key]

        #print(xy_pos)


    ## print

    def __str__(self):
        s = ''
        #print('waw')
        for item in self.uis['son']+self.uis['instru']+self.uis['phase']:
            s+=str(item.item)+'\n'
        return s

    ## details

    def aff_detail(self,ui):

        if self.autorize_deta:

            for fam in self.detaids:
                if fam == 'lab':
                    g.lman.delete(self.detaids[fam])
                elif fam == 'spr':
                    g.sman.delete(self.detaids[fam])
            self.detaids['spr'] = {}
            self.detaids['lab'] = {}

            if isinstance(ui.item,Sound_item):
                #skin
                self.addSpr('detail_spr',g.TEXTIDS[type(ui.item).__name__.lower()][convert_quality(ui.item.quality)[0]],detail=True)
                #self.detaids.append(self.sprids['detail_spr'])
                g.sman.modify(self.detaids['spr']['detail_spr'],scale=(0.5,0.5))
                g.sman.modify(self.detaids['spr']['detail_spr'],( self.box3.cx - g.sman.spr(self.detaids['spr']['detail_spr']).width/2 , self.box3.fy - 80 - g.sman.spr(self.detaids['spr']['detail_spr']).height/2 ))
                y = g.sman.spr(self.detaids['spr']['detail_spr']).y

                #qua
                self.addLab('detail_qua',convert_quality(ui.item.quality), ( self.box3.cx , y - 2*self.padding2 ), anchor = ('center','center'),detail=True)
                #self.detaids.append(self.detaids['lab']['detail_qua'])
                y = g.lman.labels[self.detaids['lab']['detail_qua']].y

                #cred / author
                if type(ui.item).__name__ != 'Instru':

                    self.addLab('detail_cred',convert_cred(ui.item.cred), ( self.box3.cx , y - self.padding ), anchor = ('center','center'),detail=True)
                    #    self.detaids.append(self.detaids['lab']['detail_cred'])
                    y = g.lman.labels[self.detaids['lab']['detail_cred']].y

                else:
                    self.addLab('detail_aut',ui.item.author.name, ( self.box3.cx , y - self.padding ),font_name=0, anchor = ('center','center'),font_size = 20,detail=True)
                    #    self.detaids.append(self.detaids['lab']['detail_aut'])
                    y = g.lman.labels[self.detaids['lab']['detail_aut']].y

                # phase
                if type(ui.item).__name__ == 'Phase':

                    tab = ui.item.content.split(' ')
                    #content = tab[0] + ' ' + tab[1] + '\n' + ' '.join(tab[2:])

                    self.addLab('detail_cont','\n'.join(tab), ( self.box3.cx , y - self.padding ),font_name=0, anchor = ('center','center'),font_size = 15,detail=True,color=c['black'])
                    #    self.detaids.append(self.detaids['lab']['detail_aut'])
                    y = g.lman.labels[self.detaids['lab']['detail_cont']].y

            else:
                self.addSpr('detail_spr',g.TEXTIDS['items'][type(ui.item).__name__.lower()],detail=True)
                g.sman.modify(self.detaids['spr']['detail_spr'],scale=(2,2))
                g.sman.modify(self.detaids['spr']['detail_spr'],( self.box3.cx - g.sman.spr(self.detaids['spr']['detail_spr']).width/2 , self.box3.fy - 80 - g.sman.spr(self.detaids['spr']['detail_spr']).height/2 ))

                if type(ui.item).__name__ == 'Key':
                    y = g.sman.spr(self.detaids['spr']['detail_spr']).y
                    self.addLab('detail_street',ui.item.target.name, ( self.box3.cx , y - 2*self.padding2 )\
                                    ,font_name=0, anchor = ('center','center'),font_size = 15,detail=True)

                elif type(ui.item).__name__ == 'Bottle':
                    y = g.sman.spr(self.detaids['spr']['detail_spr']).y
                    self.addLab('detail_liquid',ui.item.liquid, ( self.box3.cx , y - 2*self.padding2 )\
                                    ,font_name=0, anchor = ('center','center'),font_size = 15,detail=True)
                    y -= 2*self.padding2
                    self.addLab('detail_qté',str(ui.item.qt) +' mL', ( self.box3.cx , y - 2*self.padding2 )\
                                    ,font_name=0, anchor = ('center','center'),font_size = 15,detail=True)



            ## FINISH

            self.deta_visible = True
            for fam in self.detaids:
                if fam == 'lab':
                    g.lman.unhide(self.detaids[fam])
                else:
                    g.sman.unhide(self.detaids[fam])

    def eff_detail(self):
        self.deta_visible = False
        for fam in self.detaids:
            if fam == 'lab':
                g.lman.unhide(self.detaids[fam],True)
            else:
                g.sman.unhide(self.detaids[fam],True)

    ## menus

    def check_press_btns(self,x,y):

        for menu in self.btns:
            ui = self.btns[menu]
            ui.check_pressed()

    def roll_menu(self,menu='general'):

        if self.menu != menu:

            for lab in self.btns:
                if lab == menu:
                    self.btns[lab].set_act()
                else:
                    self.btns[lab].set_nap()

            if self.menu == 'sound':
                if 'sons_lab' in self.labids:
                    g.lman.delete(self.labids['sons_lab'])
                    del self.labids['sons_lab']
                if 'instrus_lab' in self.labids:
                    g.lman.delete(self.labids['instrus_lab'])
                    del self.labids['instrus_lab']
                if 'phases_lab' in self.labids:
                    g.lman.delete(self.labids['phases_lab'])
                    del self.labids['phases_lab']
                if 'plumes_lab' in self.labids:
                    g.lman.delete(self.labids['plumes_lab'])
                    del self.labids['plumes_lab']

            for cquecé in self.menus_cont[self.menu]:
                for ui in self.uis[cquecé]:
                    ui.unhide(True)
            self.menu = menu
            for cquecé in self.menus_cont[self.menu]:
                for ui in self.uis[cquecé]:
                    ui.unhide()

            self.update()

class SelectHUD(HUD):

    def __init__(self,perso):

        super(SelectHUD, self).__init__(group='hud2',name='selecter')

        self.perso = perso

        self.item_caught = None

        self.biggitem_w = 3*g.SPR
        self.smallitem_w = g.SPR
        self.padding = self.smallitem_w*1.8
        self.pad = 100


        # general : boxin
        self.box = box(1650,20,250,150)
        self.box2 = self.box.pop()
        self.box2.y += self.box.h
        self.box2.x = self.box.fx-self.padding
        self.box2.w = self.padding
        self.box2.h = (len(self.perso.selecter)-1)*self.padding


        self.addCol('bg',self.box,group='hud2-1')
        self.addCol('bg2',self.box2,group='hud2-1',color='delta_blue_faded')

        # inventory
        self.uis = {}
        for i in range(len(self.perso.selecter)):
            self.uis[i] = None

        # details
        self.details = {}
        self.details['up'] = None
        self.details['mid'] = None
        self.details['bottom'] = None

        self.update()

    def update(self):

        # on check les items dans le selecter du perso et on les mets à la bonne place

        # verif lequel est selected
        sel = []
        for i in range(len(self.uis)):
            x = self.perso.selected+i
            if x >= len(self.uis):
                x -= len(self.uis)
            sel.append(x)

        for k in range(len(sel)):
            i = sel[k]
            item = self.perso.selecter[i]

            if not self.item_caught or (self.item_caught and not self.uis[i] == self.item_caught):
                if item != None:

                    x,y = self.box2.cx,self.box2.y + (k-1)*(self.padding) + self.padding/2
                    w = self.smallitem_w

                    # si c'est l'element selectionné on met bien
                    if k == 0:
                        w = self.biggitem_w
                        x,y = self.box.fx-3*w/4,self.box.cy

                    # on crée si jamais
                    if self.uis[i] == None:
                        if isinstance(item,Sound_item):
                            scale = (0.25,0.25)
                        else:
                            scale = (1,1)
                        self.uis[i] = Invent_UI(box(x-w/2,y-w/2,w,w),item,spr_vis=self.visible,scale=scale)
                    else:
                        self.uis[i].upbox(box(x-w/2,y-w/2,w,w))

                    # on scale et on place
                    if g.sman.spr(self.uis[i].itemspr).width != w:
                        g.sman.modify(self.uis[i].itemspr,size=(w,w))

                    g.sman.modify(self.uis[i].itemspr,pos=(x,y),anchor='center')

                else:
                    if self.uis[i] != None:
                        self.uis[i].delete()
                        self.uis[i] = None


            if k == 0:
                # on update les details
                self.update_details(item)


    # hoover catch drop ...

    def check_hoover(self,x,y):
        for cquecé in self.uis:
            if self.uis[cquecé] != None:
                self.uis[cquecé].check_mouse(x,y)

    def catch_or_drop(self,x,y):

        if self.item_caught :
            ## on check kelui pour vwar si on l'drop
            self.item_caught.check_pressed()
            if self.item_caught.dropped:
                if collisionAX(self.box.realbox,(x,y)) or collisionAX(self.box2.realbox,(x,y)):
                    self.item_caught.reset()
                    self.item_caught = None
                    self.update()
                    return -1

                elif self.perso.invhud.visible and collisionAX(self.perso.invhud.box.realbox,(x,y)):
                    #print('oh yo')
                    self.perso.drop(self.item_caught.item,False)
                    self.perso.grab(self.item_caught.item,True)
                    self.item_caught = None
                    return -1

                elif self.perso.element_colli != None and isinstance(self.perso.element_colli,Zone_ACTIV) and self.perso.element_colli.activated and collisionAX(self.perso.element_colli.hud.box.realbox,(x,y)): # and hasattr(self.perso.element_colli,'hud'):

                    if type(self.perso.element_colli) == Lit and type(self.item_caught.item).__name__ == 'Phase':
                        self.perso.drop(self.item_caught.item,create=False)
                        self.perso.element_colli.hud.write(self.item_caught.item)
                        self.item_caught = None
                        return -1

                    elif type(self.perso.element_colli) == Ordi and type(self.item_caught.item).__name__ == 'Instru':
                        self.perso.element_colli.hud.inspect(self.item_caught.item)
                        self.perso.drop(self.item_caught.item,create=False)
                        self.item_caught = None
                        return -1

                    elif type(self.perso.element_colli) == Studio:

                        if type(self.item_caught.item).__name__ == 'Phase' and self.perso.element_colli.hud.phases < 4:
                            self.perso.element_colli.hud.catch(self.item_caught.item)
                            self.perso.drop(self.item_caught.item,create=False)
                            self.item_caught = None
                            return -1
                        elif type(self.item_caught.item).__name__ == 'Instru' and self.perso.element_colli.hud.instru == 0:
                            self.perso.element_colli.hud.catch(self.item_caught.item)
                            self.perso.drop(self.item_caught.item,create=False)
                            self.item_caught = None
                            return -1

                        else:
                            self.item_caught.check_pressed()

                    else:
                        self.item_caught.check_pressed()

                else:
                    self.perso.drop(self.item_caught.item)
                    self.item_caught = None
                    return -1

        else:

            ## on check touu pour vwar si on en catch
            for k in self.uis:
                if self.uis[k] != None:
                    self.uis[k].check_pressed()
                    if self.uis[k].caught:
                        self.item_caught = self.uis[k]
                        return 1
        return 0

    def quick_catch_and_drop(self):

        inventory = False

        if self.perso.element_colli != None and isinstance(self.perso.element_colli,Zone_ACTIV) and self.perso.element_colli.activated:

            if type(self.perso.element_colli) == Lit and type(self.item_caught.item).__name__ == 'Phase':
                self.perso.element_colli.hud.write(self.item_caught.item)
                self.perso.drop(self.item_caught.item,create=False)
                self.item_caught = None

            elif type(self.perso.element_colli) == Ordi and type(self.item_caught.item).__name__ == 'Instru':
                self.perso.element_colli.hud.inspect(self.item_caught.item)
                self.perso.drop(self.item_caught.item,create=False)
                self.item_caught = None

            elif type(self.perso.element_colli) == Studio:

                if type(self.item_caught.item).__name__ == 'Phase' and self.perso.element_colli.hud.phases < 4:
                    self.perso.element_colli.hud.catch(self.item_caught.item)
                    self.perso.drop(self.item_caught.item,create=False)
                    self.item_caught = None

                elif type(self.item_caught.item).__name__ == 'Instru' and self.perso.element_colli.hud.instru == 0:
                    self.perso.element_colli.hud.catch(self.item_caught.item)
                    self.perso.drop(self.item_caught.item,create=False)
                    self.item_caught = None

                else:
                    inventory = True

            else:
                inventory = True

        else:
            inventory = True

        if inventory:
            self.perso.drop(self.item_caught.item,False)
            self.perso.grab(self.item_caught.item,True)
            self.item_caught = None
            return -1


    ## details

    def update_details(self,item=None):

        if item == None:
            for x in ['mid','up','bottom']:
                if self.details[x] != None:
                    g.lman.delete(self.details[x])
                    self.details[x] = None
        else:
            details = item.details()
            keys = ['mid','up','bottom']
            pos = [ (self.box.x+self.box.w/4,self.box.cy),
                    (self.box.x+self.box.w/4,self.box.cy+self.box.h/4),
                    (self.box.x+self.box.w/4,self.box.cy-self.box.h/4)]
            sizes = [20,12,12]

            for i in range(len(keys)):

                #print(i,keys[i],details)

                if self.details[keys[i]] != None and i >= len(details):
                    g.lman.delete(self.details[keys[i]])
                    self.details[keys[i]] = None
                elif self.details[keys[i]] == None and i < len(details):
                    self.details[keys[i]] = g.lman.addLab(details[i],pos[i],anchor = ('center','center'),group='hud21',font_size=sizes[i])
                elif i < len(details):
                    g.lman.set_text(self.details[keys[i]],details[i])


"""'''''''''''''''''''''''''''''''''
'''''''  UI ''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''"""

#------# ui

class Zone_UI(Zone):

    ## HOOVER WITH MOVEMENT OF MOUSE

    def __init__(self,box2,lab_text='UIthg',textid='white',group='ui',makeCol=False,longpress=False,colorlab=c['coral']):
        super(Zone_UI,self).__init__(box2,textid,group,makeCol)
        self.box = box2

        self.lab_text=lab_text

        self.longpress = longpress
        self.visible = True
        self._hoover = False

        #print('LAB')

        # label
        x,y = self.box.cx , self.box.fy + 25
        self.label = g.lman.addLab(lab_text,(x,y),vis=False,anchor = ('center','center'),font_size=20,color=colorlab,group='ui')
        #print(x,y,g.lman.labels[self.label].content_width ,g.lman.labels[self.label].content_height)
        boxbg = box( cx=x,cy=y,w = g.lman.labels[self.label].content_width+20 , h = g.lman.labels[self.label].content_height+4 )
        self.label_bg = g.sman.addCol('black_faded',boxbg,group='ui-1',vis=False)

    def hoover(self):
        g.lman.unhide(self.label)
        g.sman.unhide(self.label_bg)
        self._hoover = True

    def unhoover(self):
        g.lman.unhide(self.label,True)
        g.sman.unhide(self.label_bg,True)
        self._hoover = False

    def activate(self):
        #print(self.lab_text,'activated')
        pass

    def delete(self):

        if hasattr(self,'skin_id'):
            g.sman.delete(self.skin_id)

        g.sman.delete(self.label_bg)
        g.lman.delete(self.label)

    def unhide(self,hide=False):
        # .unhide() affiche machin
        # .unhide(True) cache machin

        if hide:
            self.deload()
            g.lman.unhide(self.label,hide)
            g.sman.unhide(self.label_bg,hide)
        else:
            self.load()
        self.visible = not hide

    ##

    def check_mouse(self,x,y):

        if collisionAX(self.box.realbox,(x,y)):
            self.hoover()
            return True
        else:
            self.unhoover()
            return False

    def check_pressed(self):

        if self._hoover:
            self.activate()

class Button(Zone_UI):

    def __init__(self,box2,funct,param,lab_text='button',textid='delta_blue',vis=False,group='hud22',makeCol=True,longpress=False,colorlab=c['coral']):
        super(Button,self).__init__(box2,lab_text,textid,group,makeCol,longpress,colorlab)

        self.funct = funct
        self.param = param

    def activate(self):
        #print(self.lab_text,'pressed',self.param)
        self.funct(*self.param)

class Toggle(Button):

    def __init__(self,box2,funct,param,lab_text='button',nap_color='delta_purple',act_color='delta_blue',vis=False,group='hud22'):
        super(Toggle,self).__init__(box2,funct,param,lab_text,nap_color,vis,group)
        self.nap_color = nap_color
        self.act_color = act_color

        self.nap = True

    def activate(self):
        super(Toggle,self).activate()
        #self.toggle()

    def toggle(self):

        if self.nap:
            col = self.act_color
        else:
            col = self.nap_color

        self.nap = not self.nap

        if hasattr(self,'skin_id'):
            g.sman.set_col(self.skin_id,col)
        else:
            self.text_id = g.tman.addCol(col)

    def set_nap(self):
        self.nap = True
        if hasattr(self,'skin_id'):
            g.sman.set_col(self.skin_id,self.nap_color)
        else:
            self.text_id = g.tman.addCol(self.nap_color)

    def set_act(self):
        self.nap = False
        if hasattr(self,'skin_id'):
            g.sman.set_col(self.skin_id,self.act_color)
        else:
            self.text_id = g.tman.addCol(self.act_color)

##

class Plume_UI(Zone_UI):

    def __init__(self,box,plume):

        lab_text = plume.owner+'\'s plume '#+convert_quality(plume.quality)

        super(Plume_UI,self).__init__(box,lab_text,group='ui',makeCol=False,colorlab=c[convert_quality(plume.quality)[0]])

        #self.plume = phase

class Life_UI(Zone_UI):

    def __init__(self,box,perso):
        self.perso = perso

        lab_text = 'vie : '+str(perso.life)+'/'+str(perso.max_life)

        super(Life_UI,self).__init__(box,lab_text,group='ui',makeCol=False,colorlab=c['lightred'])

    def update(self):

        g.lman.set_text(self.label,'vie : '+str(self.perso.life)+'/'+str(self.perso.max_life))
        boxbg = box( cx=self.box.cx,cy=self.box.fy + 25,w = g.lman.labels[self.label].content_width+20 , h = g.lman.labels[self.label].content_height+4 )
        g.sman.delete(self.label_bg)
        self.label_bg = g.sman.addCol('delta_blue',boxbg,group='ui-1',vis=self._hoover)

class Cred_UI(Zone_UI):

    def __init__(self,box,perso):
        self.perso = perso

        lab_text = 'cred : '+str(perso.cred)

        super(Cred_UI,self).__init__(box,lab_text,group='ui',makeCol=False,colorlab=c['lightblue'])

    def update(self):
        g.lman.set_text(self.label,'cred : '+str(self.perso.cred))
        boxbg = box( cx=self.box.cx,cy=self.box.fy + 25,w = g.lman.labels[self.label].content_width+20 , h = g.lman.labels[self.label].content_height+4 )
        g.sman.delete(self.label_bg)
        self.label_bg = g.sman.addCol('delta_blue',boxbg,group='ui-1',vis=self._hoover)

#---------# item_ui -> item transportable entre les menus

class Item_UI(Zone_UI):

    def __init__(self,box,lab_text,texture,spr_vis=False,colorlab=c['F'],scale=(0.25,0.25)):

        super(Item_UI,self).__init__(box,lab_text,group='ui',colorlab=colorlab)

        #self.text_id = texture
        self.itemspr = g.sman.addSpr(texture,group='hud21',vis=spr_vis)
        self.scale = scale
        g.sman.modify(self.itemspr,scale=scale)#,opacity=128)

        pos = box.cx - g.sman.spr(self.itemspr).width/2 , box.cy - g.sman.spr(self.itemspr).height/2
        g.sman.modify(self.itemspr,pos)
        #self.itembox = box

        self.caught = False
        self.dropped = False

        self.scale = scale

        self.stacked = 1

    def catch(self):
        self.caught = True
        self.dropped = False
        g.sman.unhide(self.itemspr)
        g.sman.modify(self.itemspr,scale=(self.scale[0]*2,self.scale[1]*2),group='ui')
        if hasattr(self,'stackspr') :
            g.sman.unhide(self.stackspr)
            g.sman.modify(self.stackspr,scale=(self.scale[0]*2,self.scale[1]*2),group='ui')
        self.box = box(self.box.cx - g.sman.spr(self.itemspr).width/2,self.box.cy - g.sman.spr(self.itemspr).height/2,g.sman.spr(self.itemspr).width,g.sman.spr(self.itemspr).height)

        pos = self.box.cx , self.box.fy + 20
        g.lman.modify(self.label,pos)
        pos = self.box.cx - g.lman.labels[self.label].content_width/2 - 5, self.box.fy + 15
        g.sman.modify(self.label_bg,pos)

    def drop(self):
        self.dropped = True
        self.caught = False
        g.sman.modify(self.itemspr,scale=self.scale,group='ui-2')
        g.sman.unhide(self.itemspr,True)

        if hasattr(self,'stackspr') :
            g.sman.modify(self.stackspr,scale=self.scale,group='ui-2')
            g.sman.unhide(self.stackspr,True)

        self.box = box(self.box.cx - g.sman.spr(self.itemspr).width/2,self.box.cy - g.sman.spr(self.itemspr).height/2,g.sman.spr(self.itemspr).width,g.sman.spr(self.itemspr).height)

    def reset(self,hide=False):
        self.dropped = False
        self.caught = False
        g.sman.unhide(self.itemspr,hide)
        g.sman.modify(self.itemspr,scale=self.scale,group='ui-2')
        if hasattr(self,'stackspr') :
            g.sman.unhide(self.stackspr,hide)
            g.sman.modify(self.stackspr,scale=self.scale,group='ui-2')

    def move(self,x,y):
        self.box.xy = x-g.sman.spr(self.itemspr).width/2,y-g.sman.spr(self.itemspr).height/2
        self.update()

    def upbox(self,box):
        self.box = box
        self.update()

    def update(self):

        if self.stacked != self.item.stacked:
            if self.item.stacked == 1 and hasattr(self,'stackspr'):
                g.sman.delete(self.stackspr)
                del self.stackspr
            elif self.item.stacked != 1 and not hasattr(self,'stackspr'):
                self.stackspr = g.sman.addSpr(g.TEXTIDS['nbs'][self.item.stacked],group='hud22',vis=g.sman.spr(self.itemspr).visible)

            elif self.item.stacked != 1:
                g.sman.set_text(self.stackspr,g.TEXTIDS['nbs'][self.item.stacked])
            self.stacked = self.item.stacked

        if self.caught:
            # itemspr
            g.sman.unhide(self.itemspr)
            if hasattr(self,'stackspr'): g.sman.unhide(self.stackspr)
        pos = self.box.cx - g.sman.spr(self.itemspr).width/2 , self.box.cy - g.sman.spr(self.itemspr).height/2
        g.sman.modify(self.itemspr,pos)
        if hasattr(self,'stackspr'): g.sman.modify(self.stackspr,pos)

        # label
        pos = self.box.cx , self.box.fy + 20
        g.lman.modify(self.label,pos)
        # labelbg
        #pos = self.box.cx - g.lman.labels[self.label].content_width/2 - 5, self.box.fy + 15
        boxbg = box( cx=self.box.cx,cy=self.box.fy + 25,w = g.lman.labels[self.label].content_width+20 , h = g.lman.labels[self.label].content_height+4 )
        g.sman.modify(self.label_bg,boxbg.xy)

    def delete(self):
        super(Item_UI,self).delete()
        g.sman.delete(self.itemspr)
        if hasattr(self,'stackspr'):
            g.sman.delete(self.stackspr)
            del self.stackspr

    def activate(self):
        super(Item_UI,self).activate()
        if self.caught:
            self.drop()
        else:
            self.catch()

    def unhide(self,hide=False):

        if hasattr(self,'stackspr'):
            g.sman.unhide(self.stackspr,hide)

        g.sman.unhide(self.itemspr,hide)
        if hide:
            g.lman.unhide(self.label,hide)
            g.sman.unhide(self.label_bg,hide)
        self.visible = not hide

class Writingphase_UI(Item_UI):

    def __init__(self,box,phase):

        lab_text = 'Phase '+convert_quality(phase.quality)+'\n' +phase.them

        super(Writingphase_UI,self).__init__(box,lab_text,g.TEXTIDS['phase'][convert_quality(phase.quality)[0]],colorlab=c[convert_quality(phase.quality)[0]])

        self.phase = phase

class Invent_UI(Item_UI):

    def __init__(self,box,item,spr_vis=False,scale=(0.25,0.25)):
        #print(spr_vis)

        cquecé = type(item).__name__
        col = c['F']

        if isinstance(item,Sound_item):
            lab_text = cquecé +' '+ convert_quality(item.quality)
            col = c[convert_quality(item.quality)[0]]
            text = g.TEXTIDS[cquecé.lower()][convert_quality(item.quality)[0]]

            if cquecé == 'Phase':
                lab_text+='\n'+item.them
        else:
            lab_text = cquecé.lower()
            text = g.TEXTIDS['items'][cquecé.lower()]


        super(Invent_UI,self).__init__(box,lab_text,text,spr_vis=spr_vis,colorlab=col,scale=scale)

        self.item = item

        #self.boxdeta = box_details

    def __lt__(self, other):
         return self.item.quality < other.item.quality
