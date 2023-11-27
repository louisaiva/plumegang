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
from src import obj as o
from src import perso as p
from collections import OrderedDict
from src import cmd

"""THIS OBJ FILE IS ABOUT ITEMs && ZONEs"""


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

    k = int(gey/o2.GRP_DY)
    if k >= g.gman.nb_perso_group:
        grp = 'persoup'
    elif k < 0:
        grp = 'persodown'
    else:
        k = str(k)
        if len(k) == 1:
            k = '0'+k
        grp = 'perso'+k

    return grp

def bullet_run(dt,keyid,wp):
    bullet = wp.bullets[keyid]
    dir = bullet['dir']

    key,id = keyid
    x = g.pman.part[key][id]['x']

    if dir == 1:
        if x + wp.launch_spd > bullet['x'] + dir*wp.area:
            g.pman.delete(keyid)
        else:
            g.pman.modify_single(keyid,dx=dir*wp.launch_spd)
            env = o2.NY.CITY[bullet['street']].environ_lr(x,x + wp.launch_spd)
            touched = list(filter(lambda x: x['type'] == 'hum' and abs(x['elem'].gey - bullet['y']) < wp.y_area,env))
            #print(touched)
            for hum in list(map(lambda x:x['elem'],touched)):
                if hum != bullet['hitter']:
                    hum.be_hit(bullet['hitter'],wp.dmg)
                    g.pman.delete(keyid)
                    return
            g.bertran.schedule_once(bullet_run,0.0001,keyid,wp)

    elif dir == -1:
        if x - wp.launch_spd < bullet['x'] + dir*wp.area:
            g.pman.delete(keyid)
        else:
            g.pman.modify_single(keyid,dx=dir*wp.launch_spd)
            env = o2.NY.CITY[bullet['street']].environ_lr(x - wp.launch_spd,x)
            touched = list(filter(lambda x:x['type'] == 'hum' and abs(x['elem'].gey - bullet['y']) < wp.y_area,env))
            for hum in list(map(lambda x:x['elem'],touched)):
                if hum != bullet['hitter']:
                    hum.be_hit(bullet['hitter'],wp.dmg)
                    g.pman.delete(keyid)
                    return
            g.bertran.schedule_once(bullet_run,0.0001,keyid,wp)

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

        if type(street) == type('wesh'):
            street = o2.NY.CITY[street]
        self.target = street
        self.cat = 'key'

    def __str__(self):
        return 'key for '+self.target.name

    def details(self):
        return self.target.name.split('-')

#FOOD
class Food_item(Item):

    def __init__(self):
        super(Food_item,self).__init__()
        self.cat = 'food'
        self.single_act = True

class Bottle(Food_item):

    def __init__(self,stacked=1,liq='water',qt=None):
        super(Bottle,self).__init__()

        self.liquid = liq

        self.stacked = stacked

        self.max_qt = 1000*stacked
        if not qt:
            self.qt = self.max_qt #qté en mL
        else:
            self.qt = qt #qté en mL
        # 1 litre d'eau recharge toute une "vie d'eau"
        self.single_act = False

    def act(self,perso):

        qté = 4
        if self.qt >= qté and perso.hyd <= 100-qté/10:
            perso.drink(qté)
            self.qt -= qté

            if (self.qt//self.max_qt)+1 != self.stacked:
                self.stacked = (self.qt//self.max_qt)+1

        else:
            perso.actin = 'done'
            g.bertran.schedule_once(perso.undo,0.2,'drink')

    def __str__(self):
        return 'bottle of '+convert_huge_nb(self.qt,[' mL',' L',' kL'])+' of water'

    def details(self):
        return [self.liquid,convert_huge_nb(self.qt,[' mL',' L',' kL'])]

    def stackable(self,other):

        ## return 0 if unstackable
        ## return 1 if stackable

        if self.liquid == other.liquid and self.stacked + other.stacked  < MAX_STACK:
            return 1
        return 0

    def stack(self,other=None):

        if other == None:
            other=Bottle()

        self.stacked += other.stacked
        self.qt += other.qt

    def unstack(self,other=None):

        if other == None:
            other=Bottle()

        self.stacked -= other.stacked

        if other.qt > self.qt:
            other.qt = self.qt

        self.qt -= other.qt
        return other

class Apple(Food_item):

    def __init__(self,stacked=1):
        super(Apple,self).__init__()

        self.stacked = stacked
        self.effect = None
        self.cal = 4
        # donne 4 calories -> un humain lambda doit manger 1 kcal pr régénerer sa bouffe

    def act(self,perso):

        if perso.fed <= 100-self.cal/10:
            perso.eat(self.cal)
            g.bertran.schedule_once(perso.undo,0.2,'drink')

            if self.stacked > 1:
                self.stacked -= 1
            else:
                perso.drop(self,False)

    def __str__(self):
        return 'apple. simple apple. apple simple'

    def details(self):
        return ['The','only','apple']

    def stackable(self,other):

        ## return 0 if unstackable
        ## return 1 if stackable

        if self.stacked + other.stacked  < MAX_STACK:
            return 1
        return 0

    def stack(self,other=None):

        if other == None:
            other=Apple()

        self.stacked += other.stacked

    def unstack(self,other=None):

        if other == None:
            other=Apple()

        self.stacked -= other.stacked
        return other


#WEAPONS
class Fire_weapon(Item):

    def __init__(self):
        super(Fire_weapon,self).__init__()
        self.cat = 'weapon'
        self.dmg = 10
        self.area = 1000
        self.y_area = 30
        self.launch_spd = 200
        # damage per ball
        self.automatic = False
        # u need to click to launch a ball

        self.bullets = {}

    def hit(self,perso):

        dir = perso.dir
        gex,gey = perso.pos_bullet
        if dir == 'R':
            dir = 1
            gex += r.randint(0,self.launch_spd)
        elif dir == 'L':
            dir = -1
            gex -= r.randint(0,self.launch_spd)
        gey += r.randint(-2,2)

        keyid = g.pman.addCol(col='black',box=box(x=gex,y=gey,w=5,h=2),duree=None,group=perso.group,key='bullet')
        self.bullets[keyid] = {'x':gex,'y':perso.gey,'dir':dir,'street':perso.street,'hitter':perso}
        g.bertran.schedule_once(bullet_run,0.000001,keyid,self)

    def _single_act(self):
        return not self.automatic
    single_act = property(_single_act)

class M16(Fire_weapon):

    def __init__(self):
        super(M16,self).__init__()
        self.dmg = 1
        self.automatic = True
        self.y_area = 15

# permet de donner les bons paramètres pour afficher droit l'item sur le perso
catalog_items = {   'm16':{'elem':M16,'param':None,'rota':45,'size':(128,128),'bullet_pos':(64,0)},
                    'water_bottle':{'elem':Bottle,'param':[1]},
                    'bottle':{'elem':Bottle,'param':[1]},
                    'apple':{'elem':Apple,'param':[1]},
                    'secretapple':{'elem':Apple,'param':[1]},
                    'key':{'elem':Key,'param':['home']}
                }


'''''''''SOUND'''''''''


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
        self.author = perso
        self.release_date = day
        self.label = label
        self.label.release(self)
        self._released = True
        
        print(self.name,'released by',perso.name,'on',day)

    def stream(self):
        self.streams+=1
        self.author.addstream()
        self.label.stream(self)

    def __str__(self):
        return 'son   ' + '  ' + trunc(self.quality,5) +' '+convert_quality(self.quality) + '  ' + str(self.cred)

SPOTIFY = {}
# contient tous les sons publiés à ce jour
def target_spot(hum):
    # renvoie une musique en fonction des goûts de l'humain
    pass
    # aléatoire : si on a trop écouté cte zik on peu être saoulé
def explore_spot(hum):
    # renvoie une musique pas habituelle pour voir si l'humain kiffe
    pass
    # aléatoire pour si l'humain kiffe : change ses goûts un chouilla



"""'''''''''''''''''''''''''''''''''
'''''''LABELS'''''''''''''''''''''''
'''''''''''''''''''''''''''''''''"""

class Label():

    def __init__(self,nom='DefJam'):

        self.name = nom  #name of the label
        SPOTIFY[self.name] = []

        self.rappeurs = [] #each rapper workin with this label

        self.caisse = {}
        self.sons = {}
        self.streams = {}
        self.dailystreams = {}

        self.thune = 0
        self.promo = 100

        ## argent gagné par stream :
        ## caisse = nb_streams * prix_stream * pourcentage_pour_artiste
        self.stream_price = 1 # prix du stream

    def sign(self,rapper):
        self.rappeurs.append(rapper)
        self.caisse[rapper] = 0
        self.streams[rapper] = {}
        self.sons[rapper] = {}
        self.dailystreams[rapper] = 0
        rapper.LABEL = self

        print(rapper.name,'a signé chez',self.name,'!')
        exp = rapper.name+' a signé chez '+self.name+' !'
        g.pman.alert(exp)

    def release(self,son,perc=0.5):
        if not son._released:
            rapper = son.author
            self.sons[rapper][son] = perc
            self.streams[rapper][son] = 0

            score = self.promo*perc
            sd = {'son':son , 'promo':score }

            SPOTIFY[self.name].append(sd)

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
            rapper.day_streams = self.dailystreams[rapper]
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

        if textid not in c:
            self.text_id = textid
        elif makeCol:
            self.text_id = g.tman.addCol(textid)
        self.loaded = False

        if vis: self.load()

        self.box = box
        self.x,self.y = 0,0
        self.group = group

        self._hoover = False

    def load(self):

        if hasattr(self,'text_id') and not hasattr(self,'skin_id') :
            x = self.gex + g.Cam.X + g.GodCam.X
            y = self.gey + g.Cam.Y
            self.skin_id = g.sman.addSpr(self.text_id,(x,y),self.group,key=self.name)
            w,h = g.sman.sprites[self.skin_id].width,g.sman.sprites[self.skin_id].height
            g.sman.modify(self.skin_id,scale=(self.box.w/w,self.box.h/h))
            #print(self.name,'spr loaded',g.sman.spr(self.skin_id).x)

        self.loaded = True

    def deload(self):

        if hasattr(self,'skin_id'):
            g.sman.delete(self.skin_id)
            del self.skin_id

        self.loaded = False


    ##
    def _gex(self):
        return self.box.x
    def _setgex(self,x):
        self.box.x = x
    gex = property(_gex,_setgex)

    def _gey(self):
        return self.box.y
    def _setgey(self,y):
        self.box.y = y
    gey = property(_gey,_setgey)

    def _w(self):
        return self.box.w
    w = property(_w)
    def _h(self):
        return self.box.h
    h = property(_h)


    def _realbox(self):
        return self.x,self.y,self.x+self.w,self.y+self.h
    realbox = property(_realbox)
    def _gebox(self):
        return self.gex,self.gey,self.gex+self.w,self.gey+self.h
    gebox = property(_gebox)

#------# elements

catalog_zones = {}

class Zone_ELEM(Zone):

    ## SIMPLE ELEMNT in the street (borne,machins)

    def __init__(self,box,street,name='thing',textid='white',makeCol=True):
        super(Zone_ELEM,self).__init__(box,textid,None,makeCol)

        self.name = name
        self.group = get_perso_grp(self.gey)
        self.street = street

    def move(self,x=None,y=None,anc='left'):

        if anc != 'left' and x:
            if anc == 'right':
                x = x-self.w
            elif anc == 'center':
                x = x-self.w/2
        if x:
            self.gex = x
        if y:
            self.gey = y

    def update(self,x,y):

        self.x,self.y = x,y

        if hasattr(self,'skin_id'):

            grp = get_perso_grp(self.gey+o2.GRP_DY)
            grp += '_arm'

            g.sman.modify(self.skin_id,(x,y),group=grp)

    def load(self):
        super(Zone_ELEM,self).load()
        if hasattr(self,'skin_id') and self.street.outside:
            g.Cyc.add_spr((self.skin_id,0.3))

    def deload(self):
        if hasattr(self,'skin_id'):
            g.Cyc.del_spr((self.skin_id,0.3))
        super(Zone_ELEM,self).deload()

    def _collbox(self):
        return self.gebox
    collbox = property(_collbox)

class Zone_HOOV(Zone_ELEM):

    ## HOOVER WITH MOVEMENT OF PERSO

    def __init__(self,box,street,name='thing',textid='white',long=False,makeCol=True,position='back'):
        super(Zone_HOOV,self).__init__(box,street,name,textid,makeCol)

        ## la position est différente que la pos !! (louis du futur stp trouve un autre nom là cé éclaté)
        #   elle régule la position de la zone PAR RAPPORT au perso afin de l'activer correctement
        #   3 positions : 'back','front','mid' :
        # si 'back', le perso doit monter (Z) pour activer la zone
        # si 'front', le perso doit descendre (S) pour activer la zone
        # si 'mid', inactivable (prendre avec E)

        self.position = position
        self.perso_anim = 'act'

        self.cooldown = 0.5


        self.labtext = name
        self.longpress = long


        ## TARGETS : un humain en voiture ne peut activer une porte
        self.targets = [p.Human]


        self.color = c['coral']

        self.activated = False

    def hoover(self):
        if hasattr(self,'label'):
            g.lman.unhide(self.label)
            self._hoover = True

    def unhoover(self):
        if hasattr(self,'label'):
            g.lman.unhide(self.label,True)
            self._hoover = False

    def activate(self,perso):

        #print(perso.name,'just activated',self.labtext)
        cmd.say(perso.name,'just activated',self.labtext)
        if hasattr(self,'label') and isinstance(perso,p.Perso):
            g.lman.modify(self.label,color=self.color)

            g.bertran.schedule_once(self.deactivate,0.5)

    def deactivate(self,dt):
        if hasattr(self,'label'):
            if self._hoover:
                g.lman.modify(self.label,color=c['white'])
            else:
                g.lman.modify(self.label,color=(255,255,255,0))

    def update(self,x,y):

        super(Zone_HOOV,self).update(x,y)

        if hasattr(self,'label'):
            # label
            pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 20
            g.lman.modify(self.label,pos,group=get_perso_grp(self.gey))

    def deload(self):
        super(Zone_HOOV,self).deload()
        if hasattr(self,'label'):
            g.lman.delete(self.label)
            del self.label

    def load(self):
        super(Zone_HOOV,self).load()

        if not hasattr(self,'label'):
            # label
            pos = self.box.x + self.box.w/2 , self.box.y + self.box.h + 20
            self.label = g.lman.addLab(self.labtext,pos,vis=False,anchor = ('center','bottom'),font_size=20,group='mid')

    def activable(self,thg):

        if isinstance(thg,p.Human) and not thg.vehicle:
            for target in self.targets:
                if isinstance(thg,target):
                    return True
        elif isinstance(thg,p.Human):
            for target in self.targets:
                if isinstance(thg.vehicle,target):
                    return True

        return False

class Market(Zone_HOOV):

    def __init__(self,x,y,street):
        super(Market,self).__init__(box(x,y,300,320),street,'plumoir','pink',True,False)

    def activate(self,perso):
        super(Market,self).activate(perso)
        perso.rplum()

class SimpleReleaser(Zone_HOOV):

    def __init__(self,x,y,label,street):
        super(SimpleReleaser,self).__init__(box(x,y,300,320),street,'releaser','pink',True,False)
        self.LABEL = label

    def activate(self,perso):
        super(SimpleReleaser,self).activate(perso)
        if perso in self.LABEL.rappeurs:
            perso.auto_release(self.LABEL)

class Porte(Zone_HOOV):

    def __init__(self,street,box,destination,xdest,makeCol=False,text=None,anim='door'):

        super(Porte,self).__init__(box,street,get_id(destination.name),'grey',makeCol=makeCol)
        self.destination = destination
        #self.street = street
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
            perso.tp(x=x,y=self.destination.Y_AVERAGE,street=self.destination,arrival='back')
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

class Cash(Zone_HOOV):

    def __init__(self,x,y,street,w=100,h=200,make_col=True):
        super(Cash,self).__init__(box(x,y,w,h),street,'ez cash','red',makeCol=make_col)

    def activate(self,perso):
        super(Cash,self).activate(perso)
        perso.add_money(r.randint(20,230))

class Distrib(Zone_HOOV):

    def __init__(self,x,y,street):

        text = g.TEXTIDS['zone']['distrib']
        w,h = g.tman.textures[text].width,g.tman.textures[text].height
        super(Distrib,self).__init__(box(x,y,w,h),street,get_id('distrib'),text)
        self.labtext = 'distrib'

    def activate(self,perso):
        super(Distrib,self).activate(perso)

        prob = {
                'bottle':1,
                'apple':0.1,
                'm16':0.01,
        }

        item = r.choices(list(prob.keys()),list(prob.values()))[0]
        perso.grab(catalog_items[item]['elem']())

#trains
class TrainStation(Zone_HOOV):

    def __init__(self,train,box):
        self.train = train
        name = train.name

        super(TrainStation,self).__init__(box,self.train.street,get_id(name),'pink',False,False)
        self.labtext = name
        self.perso_anim = 'door'

    def activate(self,perso):
        super(TrainStation,self).activate(perso)
        #self.train.embarq(perso)
        perso.embarq(self.train)

class ExitTrain(Zone_HOOV):

    def __init__(self,train,box):
        self.train = train
        name = 'exit '+train.name

        super(ExitTrain,self).__init__(box,self.train.street,get_id(name),'pink',False,False,position='front')
        self.labtext = name
        self.targets = [o2.Train]
        self.perso_anim = 'door'

    def activate(self,perso):
        super(ExitTrain,self).activate(perso)
        perso.debarq()

#------# elements item -> item posable au sol dans une street

class Item_ELEM(Zone_HOOV):

    def __init__(self,item,poscentrale,street,size=64):
        nom = str(item)

        pos = poscentrale[0]-size/2,poscentrale[1]

        text = 'white'
        if isinstance(item,Sound_item):
            text = g.TEXTIDS[type(item).__name__.lower()][convert_quality(item.quality)[0]]
        else:
            text = g.TEXTIDS['items'][type(item).__name__.lower()]

        super(Item_ELEM,self).__init__(box(*pos,size,size),street,nom,text,makeCol=False)
        self.labtext = type(item).__name__.lower()
        o2.NY.CITY[street].add_item(self)
        self.item = item
        self.street = o2.NY.CITY[street]

    def activate(self,perso):

        self.street.del_item(self)
        perso.grab(self.item)

        print(perso.name,'took',self.name)


#------# active elements

class Zone_ACTIV(Zone_HOOV):

    def __init__(self,box,street,name='thing',textid='white',long=False,makeCol=True,position='back',hud=None):
        super(Zone_ACTIV,self).__init__(box,street,name,textid,long,makeCol,position)

        self.activate_inv = True
        self.inv_already_vis = False

        if hud:
            self.hud = hud
        else:
            self.hud = o.HUD()

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

    def __init__(self,x,y,perso,street):
        super(Ordi,self).__init__(box(x,y,230,150),street,'ordi','red',makeCol=False,long=True,position='front',hud=o.MarketHUD(perso))

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

    def __init__(self,x,y,street):
        super(Studio,self).__init__(box(x,y,50,150),street,'studio','blue',makeCol=False,long=True,hud=o.StudHUD())

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

    def __init__(self,x,y,street):
        super(Lit,self).__init__(box(x,y,300,150),street,'lit','darkgreen',long=True,hud=o.WriteHUD())

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

#------# lights

catalog_zones['lamps'] = {'linilop': {'text':'lamp',
                                    'light_text':'bigdouche',
                                    'collbox':(90,0,110,30)
                                    }
                        }

class Lamp(Zone_ELEM):

    def __init__(self,x,y,street):

        self.lamp = catalog_zones['lamps']['linilop']
        key = get_id('linilop')

        text = g.TEXTIDS['zone'][self.lamp['text']]
        w,h = g.tman.textures[text].width,g.tman.textures[text].height
        super(Lamp,self).__init__(box(x,y,w,h),street,key,text)

        self.light_text = g.TEXTIDS['lights'][self.lamp['light_text']]
        self.lums = [(60,700),(130,700)]
        self.lum_ids = []
        self.ancs = [('center','top')]*2

        self.on = False

    def switch_on(self):

        if not self.on:
            self.on = True
            #cmd.say(self.name,'switched on')

            # on crée la light
            if self.loaded: self.load_lums()

    def switch_off(self):

        if self.on:
            self.on = False
            #cmd.say(self.name,'switched off')

            if self.loaded: self.deload_lums()

    def update(self,x,y):
        super(Lamp,self).update(x,y)

        for i in range(len(self.lum_ids)):

            x = self.x+self.lums[i][0]
            y = self.y+self.lums[i][1]
            #cmd.say('up lamp',x,y)

            grp = get_perso_grp(self.gey)
            g.sman.modify(self.lum_ids[i],(x,y),group=grp,anchor=self.ancs[i])

    def load(self):
        super(Lamp,self).load()
        if self.on:
            self.load_lums()

    def deload(self):
        self.deload_lums()
        super(Lamp,self).deload()

    def load_lums(self):

        for i in range(len(self.lums)):
            x,y = self.lums[i]
            if len(self.lum_ids) <= i:

                x = g.sman.spr(self.skin_id).x + x
                y = g.sman.spr(self.skin_id).y + y
                #cmd.say('new lamp',x,y)

                id = g.sman.addSpr(self.light_text,(x,y),self.group,key=self.name+'_lum',anchor=self.ancs[i])
                self.lum_ids.append(id)

                if self.street.outside:
                    g.Cyc.add_spr((id,0.3))

    def deload_lums(self):
        for i in range(len(self.lum_ids)):
            g.Cyc.del_spr((self.lum_ids[i],0.3))
            g.sman.delete(self.lum_ids[i])
        self.lum_ids = []

    def _collbox(self):
        x,y,fx,fy = self.lamp['collbox']
        return self.gex+x,self.gey+y,self.gex+fx,self.gey+fy
    collbox = property(_collbox)

class HourLamp(Lamp):

    def __init__(self,x,y,street):

        super(HourLamp,self).__init__(x,y,street)

        self.hm_begin,self.hm_end = g.Hour(18,0),g.Hour(6,30)
        self.activated = True

    def update(self,x,y):

        super(HourLamp,self).update(x,y)

        #hours
        if (g.Cyc >= self.hm_begin or g.Cyc < self.hm_end) and not self.on:
            self.switch_on()
        elif (g.Cyc < self.hm_begin and g.Cyc >= self.hm_end) and self.on:
            self.switch_off()

    def _hours(self):
        return self.hm_begin,self.hm_end
    hours = property(_hours)
