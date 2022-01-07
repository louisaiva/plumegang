"""
CODED by deltasfer
enjoy
"""

import random as r
import json,time,pyglet
from src.colors import *
from src.utils import *
from src import graphic as g
from src import names as n
from src import obj2 as o2
from src import perso as p

"""""""""""""""""""""""""""""""""""
 INIT
"""""""""""""""""""""""""""""""""""

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

"""""""""""""""""""""""""""""""""""
 USEFUL FUNCTIONS
"""""""""""""""""""""""""""""""""""

def test():

    quality = r.random()
    cred = r.randint(-100,100)

    print(convert_quality(quality),convert_cred(cred))

    plum = Plume('delta',quality,cred)
    print('\n')
    for i in range(20):
        phaz = []
        for i in range(4):
            phaz.append(plum.drop_phase())
        btmker = Btmaker(r.random())
        Son(btmker.drop_instru(),phaz)

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

    return bt.drop_instru()

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

"""""""""""""""""""""""""""""""""""
 BASIK
"""""""""""""""""""""""""""""""""""

#------# plum
class Plume():

    def __init__(self,owner,qua,cred):

        self.quality = qua
        self.cred = cred
        self.owner = owner

        self.level = 0

        # skins
        #self.hud = PlumHUD(self)

    def delete(self):
        return None

    def rplum(self):

        self.quality = r.random()
        self.cred = r.randint(-100,100)

    def drop_phase(self):

        x = 2
        qua = (self.quality*x + r.random())/(x+1)

        x = 3
        cred = (self.cred*x + r.randint(-100,100))/(x+1)

        phase = Phase(qua,cred)
        #print(phase.content)
        #print(convert_quality(qua),convert_cred(cred))

        return phase

    def type(self):
        return 'Plume'

    def __lt__(self, other):
         return self.quality < other.quality

    def __str__(self):
        return 'plume ' + '  ' + trunc(self.quality,5) +' '+convert_quality(self.quality) + '  ' + str(self.cred)

#------# phases
class Phase():

    def __init__(self,quality,cred,):

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

    def __lt__(self, other):
         return self.quality < other.quality

    def __str__(self):
        return 'phase ' + '  ' + trunc(self.quality,5) +' '+convert_quality(self.quality) + '  ' + str(self.cred) + ' || ' + self.content + ' ('+ self.them+')'

    def type(self):
        return 'Phase'

#------# instrus
class Btmaker():

    def __init__(self,qua=0.5,name='Bokusan'):

        self.name = name

        #self.money = 1000

        self.quality = qua

    def drop_instru(self):

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

class Instru():

    def __init__(self,qua,author):

        self.quality = qua
        self.author = author

        self.price = instru_price(self)
        self.owners = []

    def add_owner(self,owner):
        self.owners.append(owner)

    def __lt__(self, other):
         return self.quality < other.quality

    def __str__(self):
        return 'instru' + '  ' + trunc(self.quality,5) +' '+convert_quality(self.quality) + '  ' + self.author.name

    def type(self):
        return 'Instru'

#------# sons
class Son():

    def __init__(self,instru,phases,name='cheh'):

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

    def __lt__(self, other):
         return self.quality < other.quality

    def __str__(self):
        return 'son   ' + '  ' + trunc(self.quality,5) +' '+convert_quality(self.quality) + '  ' + str(self.cred)

    def type(self):
        return 'Son'

"""""""""""""""""""""""""""""""""""
 LABELS
"""""""""""""""""""""""""""""""""""

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

    def release(self,son,perc=1):
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

    def update(self):
        for rapper in self.rappeurs:
            self.caisse[rapper] -= self.daily_abo
            print(rapper.name,':\n\t','daily streams :',self.dailystreams[rapper],'\n\t','caisse :',self.caisse[rapper])
            self.dailystreams[rapper] = 0

distro = Distrokid()


"""""""""""""""""""""""""""""""""""
 ZONES
"""""""""""""""""""""""""""""""""""

class Zone():

    def __init__(self,box,textid='white',group='mid',makeCol=True):

        if makeCol:
            if textid[:4] == 'text':
                self.text_id = textid
            else:
                self.text_id = g.tman.addCol(*box.wh,c[textid])
            self.skin_id = g.sman.addSpr(self.text_id,box.xy,group)
            w,h = g.sman.sprites[self.skin_id].width,g.sman.sprites[self.skin_id].height
            g.sman.modify(self.skin_id,scale=(box.w/w,box.h/h))

        self.gex,self.gey = box.xy
        self.x,self.y = 0,0
        self.w,self.h = box.wh
        self.group = group

        self._hoover = False

    def _realbox(self):
        return self.x,self.y,self.x+self.w,self.y+self.h

    realbox = property(_realbox)

#------# elements

class Zone_ELEM(Zone):

    ## HOOVER WITH MOVEMENT OF PERSO

    def __init__(self,box,name='thing',textid='white',group='mid',long=False,makeCol=True):
        super(Zone_ELEM,self).__init__(box,textid,group,makeCol)

        self.name = name
        self.longpress = long

        self.box = box

        # label
        pos = box.x + box.w/2 , box.y + box.h + 20
        self.label = g.lman.addLab(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20,group=group)

        self.color = c['coral']

        self.activated = False

    def move(self,x_r,y_r):
        if hasattr(self,'skin_id'):
            g.sman.modify(self.skin_id,(x_r,y_r))
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

        print(perso.name,'just activated',self.name)
        if hasattr(self,'label'):
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
            g.lman.modify(self.label,pos)

    def deload(self):
        if hasattr(self,'skin_id'):
            g.sman.delete(self.skin_id)
            del self.skin_id
        if hasattr(self,'label'):
            g.lman.delete(self.label)
            del self.label

    def load(self):
        if hasattr(self,'text_id') and not hasattr(self,'skin_id') :
            #g.sman.delete(self.skin_id)
            self.skin_id = g.sman.addSpr(self.text_id,self.box.xy,self.group)
            w,h = g.sman.sprites[self.skin_id].width,g.sman.sprites[self.skin_id].height
            g.sman.modify(self.skin_id,scale=(self.box.w/w,self.box.h/h))

        if not hasattr(self,'label'):
            # label
            pos = self.box.x + self.box.w/2 , self.box.y + self.box.h + 20
            self.label = g.lman.addLab(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20,group='mid')

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

    def __init__(self,street,box,destination,xdest,makeCol=True):

        super(Porte,self).__init__(box,destination.name,'grey','mid',makeCol=makeCol)
        self.destination = destination
        self.street = street
        self.xdest = xdest

        self.deload()

    def assign_door_tp(self,door):
        self.porte_tp = door

    def activate(self,perso):
        super(Porte,self).activate(perso)

        if type(self.destination) in [o2.Street] or self.destination.openable(perso):

            #perso.add_money(r.randint(20,230))
            #perso.element_colli = None

            #self.street.deload()
            #self.destination.load()
            perso.tp(x=self.xdest,street=self.destination)
            #perso.check_colli(self.destination)
            return self.destination.name
        else:
            g.pman.alert('you can\'t go here !')
            #print('You can\'t go here !' )

#------# elements item

class Item(Zone_ELEM):

    def __init__(self,item,poscentrale,street,size=100):
        nom = str(item.owner)+'\'s plume'

        pos = poscentrale[0]-size/2,poscentrale[1]

        super(Item,self).__init__(box(*pos,size,size),nom,g.TEXTIDS[item.type().lower()][convert_quality(item.quality)[0]],group='perso')
        o2.NY.CITY[street].add_item(self)
        self.item = item
        self.street = street

    def activate(self,perso):

        print(perso.name,'took',self.name)
        o2.NY.CITY[self.street].del_item(self)
        perso.drop_plume()
        perso.grab_plume(self.item)


#------# active elements

class Zone_ACTIV(Zone_ELEM):

    def __init__(self,box,name='thing',textid='white',group='mid',long=False,makeCol=True):
        super(Zone_ACTIV,self).__init__(box,name,textid,group,long,makeCol)

    def activate(self,perso):
        super(Zone_ACTIV,self).activate(perso)
        self.activated = True

    def close(self,perso):
        self.activated = False
        perso.do()

class Distrib(Zone_ELEM):

    def __init__(self,x,y):
        super(Distrib,self).__init__(box(x,y,100,200),'ez cash','red','mid',makeCol=True)

    def activate(self,perso):
        super(Distrib,self).activate(perso)
        perso.add_money(r.randint(20,230))

class Ordi(Zone_ACTIV):

    def __init__(self,x,y,perso):
        super(Ordi,self).__init__(box(x,y,230,260),'ordi','red','mid',makeCol=False,long=True)

        self.hud = MarketHUD(perso)

    def activate(self,perso):
        super(Ordi,self).activate(perso)

        g.lman.modify(self.hud.labids['market'],color=self.color)

        if self.hud.visible:
            perso.do('write')
            perso.undo(0,'wait')

        else:
            perso.do('wait')
            self.hud.unhide()
            perso.invhud.eff_detail()
            perso.invhud.autorize_deta = False

    def deactivate(self,dt):
        super(Ordi,self).deactivate(0)
        if self.activated:
            g.lman.modify(self.hud.labids['market'],color=c['white'])
        else:
            g.lman.modify(self.hud.labids['market'],color=(255,255,255,0))

    def close(self,perso):
        super(Ordi,self).close(perso)
        self.hud.unhide(True)
        perso.invhud.autorize_deta = True

class Studio(Zone_ACTIV):

    def __init__(self,x,y):
        super(Studio,self).__init__(box(x,y,50,200),'studio','blue','mid',makeCol=False,long=True)

        self.hud = StudHUD()

    def activate(self,perso):
        super(Studio,self).activate(perso)

        g.lman.modify(self.hud.labids['stud'],color=self.color)

        if self.hud.visible:
            perso.do('write')
            perso.undo(0,'wait')
            self.hud.assemble(perso)
        else:
            perso.do('wait')
            perso.invhud.unhide()
            self.hud.unhide()
            perso.invhud.eff_detail()
            perso.invhud.autorize_deta = False

    def deactivate(self,dt):
        super(Studio,self).deactivate(0)
        if self.activated:
            g.lman.modify(self.hud.labids['stud'],color=c['white'])
        else:
            g.lman.modify(self.hud.labids['stud'],color=(255,255,255,0))

    def close(self,perso):
        super(Studio,self).close(perso)
        self.hud.unhide(True)
        perso.invhud.autorize_deta = True

    def assemble(self,perso):

        son = perso.creer_son()
        if son != None:
            perso.invhud.catch(son)
        else:
            print('Frerooooo t\'as besoin d\'une instru et de 4 phases pour faire un son tu vas ou commas ?')

class Lit(Zone_ACTIV):

    def __init__(self,x,y):
        super(Lit,self).__init__(box(x,y,300,150),'lit','darkgreen','mid',long=True)

        self.hud = WriteHUD()

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
            perso.invhud.eff_detail()
            perso.invhud.autorize_deta = False

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
        perso.invhud.autorize_deta = True
        #perso.invhud.unhide(True)

    def write(self,perso):

        if perso.plume != None:
            phase = perso.plume.drop_phase()
            #aff_phase(phase)
            self.hud.write(phase)


"""""""""""""""""""""""""""""""""""
 HUD
"""""""""""""""""""""""""""""""""""

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

    def addCol(self,key,box,color=c['delta_purple'],group=None):

        if group == None:
            group = self.group

        if type(color) == type(()):
            textid = g.tman.addCol(*box.wh,color)
        else:
            textid = g.tman.addCol(*box.wh,c[color])
        self.addSpr(key,textid,box.xy,group=group)

    def addLab(self,key,contenu,xy_pos=(0,0),group=None,font_name=0,font_size=30,anchor=('left','bottom'),color=(255,255,255,255)):

        if key in self.labids:
            g.lman.delete(self.labids[key])

        if group == None:
            group = self.group

        self.labids[key] = g.lman.addLab(str(contenu),xy_pos,group=group,font_name=font_name,font_size=font_size,anchor=anchor,color=color,vis=self.visible)

        #print(xy_pos)

    def modifySpr(self,key,pos=None,scale=None):
        g.sman.modify(self.sprids[key],pos,scale)

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

        super(Map, self).__init__(group='hud2',name='map',vis=False)

        self.perso = perso

        scrw,scrh=g.scr.size
        area = box(scrw//2-2*scrh//6,scrh//6,2*scrh//3,2*scrh//3)

        self.pad = 25
        self.box = box(area.x+self.pad,area.y+self.pad,area.w-2*self.pad,area.h-2*self.pad)

        self.larg_street = int((self.box.w/3)/o2.MAP[0])
        w = self.larg_street*3*o2.MAP[0]
        self.box = box(scrw/2-w/2,scrh/2-w/2,w,w)

        #print(area.xywh,self.larg_street)

        col = (*c['delta_blue'][:3],170)
        #print(col)
        self.addCol('bg',area,group='hud2-1',color=col)
        self.addCol('bg2',area,group='hud2-1',color=col)

        ## name
        self.addLab('name','MAP OF NY CITY',(area.cx,area.fy-self.pad),font_name=1,anchor=('center','center'),group='hud2')
        self.create_map()

    def create_map(self):

        for street in o2.NY.CITY:
            street = o2.NY.CITY[street]

            if type(street) == o2.Street:

                vert = street.pre.vert

                if vert:
                    x = self.box.x + street.line[0][0]*3*self.larg_street+self.larg_street
                    y = self.box.fy - street.line[1][1]*3*self.larg_street
                else:
                    x = self.box.x + street.line[0][0]*3*self.larg_street
                    y = self.box.fy - street.line[0][1]*3*self.larg_street-self.larg_street

                if vert:
                    w,h=self.larg_street,street.pre.w*3*self.larg_street+self.larg_street
                else:
                    h,w=self.larg_street,street.pre.w*3*self.larg_street+self.larg_street
                #print(street.name)
                self.addCol(street.name,box(x,y,w,h),color=c['delta_purple'],group='hud2')

            else:
                w,h=self.larg_street,self.larg_street

                x=self.box.x + street.line[0][0]*3*self.larg_street
                y = self.box.fy - street.line[1][1]*3*self.larg_street
                self.addCol(street.name,box(x,y,w,h),color=c['red'],group='hud2')

    def update(self):

        street = o2.NY.CITY[self.perso.street]

        # get pos
        if type(street) == o2.Street: # si le perso se trouve dans une rue

            perc = self.perso.gex/street.xxf[1]

            vert = street.pre.vert
            if vert:
                x = g.sman.spr(self.sprids[street.name]).x + self.larg_street/2
                y = g.sman.spr(self.sprids[street.name]).y + g.sman.spr(self.sprids[street.name]).height + self.larg_street/2 - perc*g.sman.spr(self.sprids[street.name]).height
            else:
                y = g.sman.spr(self.sprids[street.name]).y + self.larg_street/2
                x = g.sman.spr(self.sprids[street.name]).x + perc*g.sman.spr(self.sprids[street.name]).width

        else: # si le perso se trouve dans une maison
            x,y = g.sman.spr(self.sprids[street.name]).position
            x += self.larg_street/2
            y += self.larg_street/2

        # create and or change pos
        if not 'perso_spr' in self.sprids:
            self.addSpr('perso_spr',self.perso.textids['nothing']['R'][0],(x,y), group='hud21')
            scale = self.pad/g.sman.spr(self.sprids['perso_spr']).width
            g.sman.modify(self.sprids['perso_spr'],scale=(scale,scale),anchor='center')
        else:
            g.sman.modify(self.sprids['perso_spr'],pos=(x,y),anchor='center')

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

        self.addSpr('coin_spr',g.TEXTIDS['item'][0],(xcoin,ycoin - g.tman.textures[g.TEXTIDS['item'][0]].height/2))
        self.addLab('coin_lab',convert_huge_nb(self.perso.money),(xcoin ,ycoin),font_name=1,font_size=20,color=c['yellow'],anchor=('right','center'))

        ## fans

        xfan = self.box.cx
        yfan = self.lab('coin_lab').y - self.padding

        self.addSpr('fan_spr',g.TEXTIDS['item'][1],(xfan,yfan - g.tman.textures[g.TEXTIDS['item'][1]].height/2))
        self.addLab('fan_lab',convert_huge_nb(self.perso.nb_fans),(xfan ,yfan),font_name=1,font_size=20,color=c['lightgreen'],anchor=('right','center'))

        ## fans

        xstream = self.box.cx
        ystream = self.lab('fan_lab').y - self.padding

        self.addSpr('stream_spr',g.TEXTIDS['item'][2],(xstream,ystream - g.tman.textures[g.TEXTIDS['item'][2]].height/2))
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

class PlumHUD(HUD):

    def __init__(self,plum):

        super(PlumHUD, self).__init__(group='hud2',name='plum')

        self.plum = plum


        self.box = box(1650,20,250,150)
        self.padding = 50

        self.addCol('bg',self.box,group='hud2-1')

        self.addLab('quality',convert_quality(self.plum.quality),(self.box.x+self.box.w-self.padding,self.box.cy),font_name=1,anchor=('center','center'))

        self.addSpr('plum_spr',g.TEXTIDS['plume'][convert_quality(self.plum.quality)[0]])
        g.sman.modify(self.sprids['plum_spr'],scale=(0.4,0.4))

        xplum = self.lab('quality').x - self.padding - self.spr('plum_spr').width/2
        yplum = self.box.cy - self.spr('plum_spr').height/2

        g.sman.modify(self.sprids['plum_spr'],pos=(xplum,yplum))


        x = (xplum +  (self.box.x) )/2

        self.addLab('cred',convert_cred(self.plum.cred),(x ,self.box.cy),font_name=1,font_size=20,anchor=('center','center'))


        ### UI
        self.ui = Plume_UI(box(xplum,yplum,self.spr('plum_spr').width,self.spr('plum_spr').height),plum)

    def delete(self):

        super(PlumHUD,self).delete()
        self.ui.delete()

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

        self.addCol('bg2',self.box2,color=c['delta_blue'],group='hud')

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
                perso.invhud.catch(self.ui.phase)
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
                if self.item_caught.item.type() != 'Son':
                    self.catch(self.item_caught.item)
                    self.item_caught.delete()
                    self.item_caught = None
                else:
                    return 0

            elif perso.invhud.visible and collisionAX(perso.invhud.box.realbox,(x,y)):
                perso.invhud.catch(self.item_caught.item)
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

        if thg.type() == 'Phase' and self.phases < 4:
            for lab in self.uis:
                if lab[:3] == 'pha' and self.uis[lab] == None:
                    self.uis[lab] = Invent_UI(self.boxs[lab],thg,self.visible,scale=(0.4,0.4))
                    self.phases+=1
                    break

        elif thg.type() == 'Instru' and self.instru == 0:
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
                self.perso.invhud.catch(self.item_caught.item)
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
                self.perso.invhud.catch(self.uis['main'].item)
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
        self.addSpr('main_price',g.TEXTIDS['item'][0],(self.box.x+129,self.boxs['main'].cy - g.tman.textures[g.TEXTIDS['item'][0]].height/2))

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
            self.addSpr('main_price',g.TEXTIDS['item'][0],(self.box.x+129,self.boxs['main'].cy - g.tman.textures[g.TEXTIDS['item'][0]].height/2))

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
            perso.invhud.catch(self.item_caught.item)
            self.item_caught.delete()
            self.item_caught = None

        for lab in self.uis:
            ui = self.uis[lab]
            if ui != None:
                ui.unhide(hide)

class InventHUD(HUD):

    def __init__(self,perso,fill=True):

        super(InventHUD, self).__init__(group='hud1',name='inv',vis=False)

        self.perso = perso

        self.item_caught = None

        # inventory
        self.inventory = {}
        self.inventory['phase'] = []
        self.inventory['instru'] = []
        self.inventory['son'] = []

        ### GENERAL

        self.box = box(20,200,338,800)
        self.padding = 64
        self.padding2 = 20
        self.lilpadding = 12
        self.lilpadding2 = 6

        ### COLORS

        self.addCol('bg',self.box,group='hud-1')

        self.box2 = box(self.box.x+self.padding2,self.box.y+self.padding2,self.box.w-2*self.padding2,self.box.h-self.padding2-100)

        self.addCol('bg2',self.box2,color=c['delta_blue'],group='hud')


        ### PARTIE DETAILS

        self.autorize_deta = True
        self.deta_visible = False
        self.detaids = {}
        self.detaids['spr'] = {}
        self.detaids['bg'] = {}
        self.detaids['lab'] = {}

        height_detail = 2*self.box.h/3
        width_detail = 180

        self.box3 = box(self.box.fx,self.box.cy-height_detail/2,width_detail,int(height_detail))
        #print(not self.deta_visible)
        self.addCol('bgdeta',self.box3,group='hud-1',detail=True)
        #g.sman.unhide(self.sprids['bgdeta'],not self.deta_visible)
        #self.detaids.append(self.sprids['bgdeta'])


        ### LABEL inv
        self.addLab('inv_lab','inventory',(self.box.cx,self.box.fy-50),font_name=1,anchor=('center','center'))

        if fill:
            #self.update()
            for i in range(r.randint(2,10)):
                ins = Instru(r.random(),r.choice(btmakers))
                ins.add_owner(self.perso)
                self.catch(ins)
            for i in range(r.randint(2,10)):
                ph = []
                for i in range(4):
                    ph.append(Phase(rqua(),rcred()))
                instru = Instru(r.random(),r.choice(btmakers))

                self.catch(Son(instru,ph))

    def catch(self,item):

        ui = Invent_UI(box(w=self.padding,h=self.padding),item,self.visible)
        self.inventory[item.type().lower()].append(ui)

        self.update()

        #print(self.inventory)

    def update(self):

        yf = self.box2.fy

        #sons
        if self.inventory['son'] != []:
            self.addLab('sons_lab','sons',(self.box.cx,yf-self.padding2),font_name=1,color=c['black'],font_size=20,anchor=('center','center'))
            yf -= self.padding2*2

            self.inventory['son'].sort(reverse=True)

            for i in range(len(self.inventory['son'])):

                x = self.box2.x + self.padding/2 + self.lilpadding + (self.padding + self.lilpadding2)*(i%4)
                y = yf + self.padding/2 - (self.padding + self.lilpadding2)*(i//4 + 1)

                self.inventory['son'][i].move(x,y)
            yf -= (self.padding + self.lilpadding2)*((len(self.inventory['son'])-1)//4 + 1) + self.lilpadding - self.lilpadding2
        else:
            if 'sons_lab' in self.labids:
                g.lman.delete(self.labids['sons_lab'])
                del self.labids['sons_lab']

        #instrus
        if self.inventory['instru'] != []:
            self.addLab('instrus_lab','instrus',(self.box.cx,yf-self.padding2),font_name=1,color=c['black'],font_size=20,anchor=('center','center'))
            yf -= self.padding2*2

            self.inventory['instru'].sort(reverse=True)

            for i in range(len(self.inventory['instru'])):

                x = self.box2.x + self.padding/2 + self.lilpadding + (self.padding + self.lilpadding2)*(i%4)
                y = yf + self.padding/2 - (self.padding + self.lilpadding2)*(i//4 + 1)

                self.inventory['instru'][i].move(x,y)
            yf -= (self.padding + self.lilpadding2)*((len(self.inventory['instru'])-1)//4 + 1) + self.lilpadding - self.lilpadding2
        else:
            if 'instrus_lab' in self.labids:
                g.lman.delete(self.labids['instrus_lab'])
                del self.labids['instrus_lab']

        #phases
        if self.inventory['phase'] != []:
            self.addLab('phases_lab','phases',(self.box.cx,yf-self.padding2),font_name=1,color=c['black'],font_size=20,anchor=('center','center'))
            yf -= self.padding2*2

            self.inventory['phase'].sort(reverse=True)

            for i in range(len(self.inventory['phase'])):

                x = self.box2.x + self.padding/2 + self.lilpadding + (self.padding + self.lilpadding2)*(i%4)
                y = yf + self.padding/2 - (self.padding + self.lilpadding2 )*(i//4 + 1)

                self.inventory['phase'][i].move(x,y)
            yf -= (self.padding + self.lilpadding2)*((len(self.inventory['phase'])-1)//4 + 1) + self.lilpadding - self.lilpadding2
        else:
            if 'phases_lab' in self.labids:
                g.lman.delete(self.labids['phases_lab'])
                del self.labids['phases_lab']

    def unhide(self,hide=False):
        super(InventHUD,self).unhide(hide)

        if hide and self.item_caught != None:
            self.item_caught.drop()
            self.item_caught.reset()
            self.item_caught = None
            self.update()
        for ui in self.inventory['phase']+self.inventory['son']+self.inventory['instru']:
            ui.unhide(hide)

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
                    self.update()
                    self.item_caught = None
                    return -1

                elif self.perso.element_colli != None and self.perso.element_colli.activated and collisionAX(self.perso.element_colli.hud.box.realbox,(x,y)): # and hasattr(self.perso.element_colli,'hud'):

                    if type(self.perso.element_colli) == Lit and self.item_caught.item.type() == 'Phase':
                        self.perso.element_colli.hud.write(self.item_caught.item)
                        self.remove(self.item_caught)
                        self.item_caught = None
                        return -1

                    elif type(self.perso.element_colli) == Ordi and self.item_caught.item.type() == 'Instru':
                        self.perso.element_colli.hud.inspect(self.item_caught.item)
                        self.remove(self.item_caught)
                        self.item_caught = None
                        return -1

                    elif type(self.perso.element_colli) == Studio:

                        if self.item_caught.item.type() == 'Phase' and self.perso.element_colli.hud.phases < 4:
                            self.perso.element_colli.hud.catch(self.item_caught.item)
                            self.remove(self.item_caught)
                            self.item_caught = None
                            return -1
                        elif self.item_caught.item.type() == 'Instru' and self.perso.element_colli.hud.instru == 0:
                            self.perso.element_colli.hud.catch(self.item_caught.item)
                            self.remove(self.item_caught)
                            self.item_caught = None
                            return -1

                        else:
                            self.item_caught.check_pressed()

                    else:
                        self.item_caught.check_pressed()

                else:
                    self.remove(self.item_caught)
                    self.item_caught = None
                    return -1

        else:
            ## on check touu pour vwar si on en catch

            for ui in self.inventory['phase']+self.inventory['son']+self.inventory['instru']:

                ui.check_pressed()
                if ui.caught:
                    self.item_caught = ui
                    return 1
        return 0

    def remove(self,item,up=True):

        if type(item) == type([]):
            for subitem in item:
                self.remove(subitem,False)
        elif item != None:
            item.delete()
            self.inventory[item.item.type().lower()].remove(item)

        if up:
            self.update()

    def check_hoover(self,x,y):

        something_to_aff = False

        for uitype in self.inventory:
            for ui in self.inventory[uitype]:
                ui.check_mouse(x,y)
                if ui._hoover:
                    something_to_aff = True
                    self.aff_detail(ui)

        if not something_to_aff:
            self.eff_detail()

    ## de base

    def addSpr(self,key,textid,xy_pos=(0,0),group=None,detail=False):
        super(InventHUD,self).addSpr(key,textid,xy_pos,group)
        if detail:
            self.detaids['spr'][key]=self.sprids[key]
            del self.sprids[key]

    def addCol(self,key,box,color=c['delta_purple'],group=None,detail=False):
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
        for item in self.inventory['son']+self.inventory['instru']+self.inventory['phase']:
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

            #skin
            self.addSpr('detail_spr',g.TEXTIDS[ui.item.type().lower()][convert_quality(ui.item.quality)[0]],detail=True)
            #self.detaids.append(self.sprids['detail_spr'])
            g.sman.modify(self.detaids['spr']['detail_spr'],scale=(0.5,0.5))
            g.sman.modify(self.detaids['spr']['detail_spr'],( self.box3.cx - g.sman.spr(self.detaids['spr']['detail_spr']).width/2 , self.box3.fy - 80 - g.sman.spr(self.detaids['spr']['detail_spr']).height/2 ))
            y = g.sman.spr(self.detaids['spr']['detail_spr']).y

            #qua
            self.addLab('detail_qua',convert_quality(ui.item.quality), ( self.box3.cx , y - 2*self.padding2 ), anchor = ('center','center'),detail=True)
            #self.detaids.append(self.detaids['lab']['detail_qua'])
            y = g.lman.labels[self.detaids['lab']['detail_qua']].y

            #cred / author
            if ui.item.type() != 'Instru':

                self.addLab('detail_cred',convert_cred(ui.item.cred), ( self.box3.cx , y - self.padding ), anchor = ('center','center'),detail=True)
                #    self.detaids.append(self.detaids['lab']['detail_cred'])
                y = g.lman.labels[self.detaids['lab']['detail_cred']].y

            else:
                self.addLab('detail_aut',ui.item.author.name, ( self.box3.cx , y - self.padding ),font_name=0, anchor = ('center','center'),font_size = 20,detail=True)
                #    self.detaids.append(self.detaids['lab']['detail_aut'])
                y = g.lman.labels[self.detaids['lab']['detail_aut']].y

            # phase
            if ui.item.type() == 'Phase':

                tab = ui.item.content.split(' ')
                #content = tab[0] + ' ' + tab[1] + '\n' + ' '.join(tab[2:])

                self.addLab('detail_cont','\n'.join(tab), ( self.box3.cx , y - self.padding ),font_name=0, anchor = ('center','center'),font_size = 15,detail=True,color=c['black'])
                #    self.detaids.append(self.detaids['lab']['detail_aut'])
                y = g.lman.labels[self.detaids['lab']['detail_cont']].y


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


"""""""""""""""""""""""""""""""""""
 UI
"""""""""""""""""""""""""""""""""""

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

        # label
        pos = self.box.x + self.box.w/2 , self.box.y + self.box.h + 20
        self.label = g.lman.addLab(lab_text,pos,vis=False,anchor = ('center','bottom'),font_size=20,color=colorlab,group=group)
        boxbg = box( self.box.x + self.box.w/2 - g.lman.labels[self.label].content_width/2 - 5, self.box.y + self.box.h + 15, g.lman.labels[self.label].content_width+10 , g.lman.labels[self.label].content_height+10 )
        self.label_bg = g.sman.addCol((120,120,120,255),boxbg,group=group+'-1',vis=False)

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

class Plume_UI(Zone_UI):

    def __init__(self,box,plume):

        lab_text = plume.owner+'\'s plume '#+convert_quality(plume.quality)

        super(Plume_UI,self).__init__(box,lab_text,group='ui',makeCol=False,colorlab=c[convert_quality(plume.quality)[0]])

        #self.plume = phase

    def update(self):
        pass

class Life_UI(Zone_UI):

    def __init__(self,box,perso):
        self.perso = perso

        lab_text = 'vie : '+str(perso.life)+'/'+str(perso.max_life)

        super(Life_UI,self).__init__(box,lab_text,group='ui',makeCol=False,colorlab=c['lightred'])

    def update(self):
        g.lman.set_text(self.label,'vie : '+str(self.perso.life)+'/'+str(self.perso.max_life))
        boxbg = box( self.box.x + self.box.w/2 - g.lman.labels[self.label].content_width/2 - 5, self.box.y + self.box.h + 15, g.lman.labels[self.label].content_width+10 , g.lman.labels[self.label].content_height+10 )
        g.sman.delete(self.label_bg)
        self.label_bg = g.sman.addCol((120,120,120,255),boxbg,group='ui-1',vis=self._hoover)

class Cred_UI(Zone_UI):

    def __init__(self,box,perso):
        self.perso = perso

        lab_text = 'cred : '+str(perso.cred)

        super(Cred_UI,self).__init__(box,lab_text,group='ui',makeCol=False,colorlab=c['lightblue'])

    def update(self):
        g.lman.set_text(self.label,'cred : '+str(self.perso.cred))
        boxbg = box( self.box.x + self.box.w/2 - g.lman.labels[self.label].content_width/2 - 5, self.box.y + self.box.h + 15, g.lman.labels[self.label].content_width+10 , g.lman.labels[self.label].content_height+10 )
        g.sman.delete(self.label_bg)
        self.label_bg = g.sman.addCol((120,120,120,255),boxbg,group='ui-1',vis=self._hoover)

class Item_UI(Zone_UI):

    def __init__(self,box,lab_text,texture,spr_vis=False,colorlab=c['F'],scale=(0.25,0.25)):

        super(Item_UI,self).__init__(box,lab_text,group='ui',colorlab=colorlab)

        #self.text_id = texture
        self.itemspr = g.sman.addSpr(texture,group='ui-2',vis=spr_vis)
        self.scale = scale
        g.sman.modify(self.itemspr,scale=scale)#,opacity=128)

        pos = box.cx - g.sman.spr(self.itemspr).width/2 , box.cy - g.sman.spr(self.itemspr).height/2
        g.sman.modify(self.itemspr,pos)

        self.caught = False
        self.dropped = False

    def catch(self):
        self.caught = True
        self.dropped = False
        g.sman.unhide(self.itemspr)
        g.sman.modify(self.itemspr,scale=(0.5,0.5),group='ui')
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
        self.box = box(self.box.cx - g.sman.spr(self.itemspr).width/2,self.box.cy - g.sman.spr(self.itemspr).height/2,g.sman.spr(self.itemspr).width,g.sman.spr(self.itemspr).height)

    def reset(self,hide=False):
        self.dropped = False
        self.caught = False
        g.sman.unhide(self.itemspr,hide)
        g.sman.modify(self.itemspr,scale=self.scale,group='ui-2')

    def move(self,x,y):
        self.box.xy = x-g.sman.spr(self.itemspr).width/2,y-g.sman.spr(self.itemspr).height/2
        self.update()

    def upbox(self,box):
        self.box = box
        self.update()

    def update(self):

        if self.caught:

            # itemspr
            g.sman.unhide(self.itemspr)
        pos = self.box.cx - g.sman.spr(self.itemspr).width/2 , self.box.cy - g.sman.spr(self.itemspr).height/2
        g.sman.modify(self.itemspr,pos)

        # label
        pos = self.box.cx , self.box.fy + 20
        g.lman.modify(self.label,pos)
        # labelbg
        pos = self.box.cx - g.lman.labels[self.label].content_width/2 - 5, self.box.fy + 15
        g.sman.modify(self.label_bg,pos)

    def delete(self):
        super(Item_UI,self).delete()
        g.sman.delete(self.itemspr)

    def activate(self):
        super(Item_UI,self).activate()
        if self.caught:
            self.drop()
        else:
            self.catch()

    def unhide(self,hide=False):

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

        cquecé = item.type()

        lab_text = cquecé +' '+ convert_quality(item.quality)
        col = c[convert_quality(item.quality)[0]]

        if cquecé == 'Phase':
            lab_text+='\n'+item.them

        super(Invent_UI,self).__init__(box,lab_text,g.TEXTIDS[cquecé.lower()][convert_quality(item.quality)[0]],spr_vis=spr_vis,colorlab=col,scale=scale)

        self.item = item

        #self.boxdeta = box_details

    def __lt__(self, other):
         return self.item.quality < other.item.quality
