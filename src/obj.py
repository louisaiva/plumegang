
import random as r
import json,time,pyglet
from src.colors import *
from src.utils import *
from src import graphic as g

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
CRED_coeff = [-95,-80,-50,-10,10,50,80,95,101]

with open('src/mots.json','r') as f:
    MOTS = json.load(f)

THEMES = ['amour','argent','liberté','révolte','egotrip','ovni','famille','mort + dévastation','notoriété','chill','rap']

"""""""""""""""""""""""""""""""""""
 CLASSES BASIK
"""""""""""""""""""""""""""""""""""


#------# phases

class Rappeur():

    def __init__(self,textids,pos=(400,200),name='Delta'):

        # general

        self.name = name
        self.speed = 12

        self.gex = pos[0] # general x
        self.gey = pos[1] # general y

        #self.street_score = 0

        self.money = 10000

        #self.nb_fans = 0
        #self.fans = []

        self.plume = rplum()

        self.element_colli = None

        # track of time
        self.time_last_move = 0

        self.doing = 'nothing'
        self.dir = 'R'

        # skins
        self.textids = { ('nothing','R',0):textids[0] , ('nothing','R',1):textids[1]
                        , ('nothing','L',0):textids[0+2] , ('nothing','L',1):textids[1+2]
                        , ('moving','R',0):textids[2+2]
                        , ('moving','R',1):textids[3+2] , ('moving','L',0):textids[4+2] , ('moving','L',1):textids[5+2]
                        , ('hitting','R',0):textids[6+2] , ('hitting','R',1):textids[6+2] , ('hitting','L',0):textids[7+2] , ('hitting','L',1):textids[7+2] }
        self.roll_skin = 0
        self.skin_id = g.sman.addSpr(self.textids[(self.doing,self.dir,0)],pos,'up')

        # hud
        self.hud = PersoHUD(self)

        #print(self.hud)

        self.update_skin()

    def rplum(self):
        if self.plume != None:
            self.plume.delete()
        self.plume = rplum()

    def update_skin(self,dt=0.4,repeat=True):

        g.sman.set_text(self.skin_id,self.textids[(self.doing,self.dir,self.roll_skin)])
        if self.roll_skin:
            self.roll_skin = 0
        else:
            self.roll_skin = 1

        if repeat :
            pyglet.clock.schedule_once(self.update_skin, 0.4)

    def move(self,dir):

        moved = False
        #x,y = g.sman.spr(self.skin_id).position
        if dir == 'R':
            self.gex+=self.speed
            #g.sman.modify(self.skin_id,(x+self.speed,y))
            moved = True
        elif dir == 'L':
            self.gex-=self.speed
            #g.sman.modify(self.skin_id,(x-self.speed,y))
            moved = True

        if moved :
            if self.doing != 'hitting':
                if (self.doing != 'moving' or self.dir != dir):
                    self.doing = 'moving'
                    self.dir = dir
                    self.update_skin(repeat=False)
                self.doing = 'moving'
                self.dir = dir
            self.check_colli()

            self.time_last_move = time.time()

    def check_colli(self):

        colli_elem = None
        for elem in ZONES['ELEM']:
            if collision(self.box,ZONES['ELEM'][elem].box) :
                    colli_elem = ZONES['ELEM'][elem]

        if self.element_colli != None:
            if colli_elem != None:
                if colli_elem != self.element_colli :
                    self.element_colli.unhoover()
                    self.element_colli = colli_elem
                    self.element_colli.hoover()
            else:
                self.element_colli.unhoover()
                self.element_colli = None
        else:
            if colli_elem != None:
                self.element_colli = colli_elem
                self.element_colli.hoover()

        #print(self.element_colli)

    def check_ani(self):

        if time.time()-self.time_last_move > 0.2 and self.doing != 'hitting':
            self.doing = 'nothing'

    def hit(self,dt=0):

        if self.doing != 'hitting':
            self.doing = 'hitting'
            self.update_skin(repeat=False)
            #print(self.name,'hits the void')
            pyglet.clock.schedule_once(self.hit,0.2)
        else:
            self.doing = 'nothing'

    def drop_plume(self):
        if self.plume != None:
            self.plume = self.plume.delete()

    def add_money(self,qté):
        self.money += qté

    ##

    def _realbox(self):
        return g.sman.box(self.skin_id)

    box = property(_realbox)
    """
    def _plum(self):
        if self._plume != None
        return self._plume"""

class Plume():

    def __init__(self,qua,cred):

        self.quality = qua
        self.cred_power = cred

        self.level = 0

        # skins
        self.hud = PlumHUD(self)

    def delete(self):

        self.hud.delete()
        return None

    def rplum(self):

        self.quality = r.random()
        self.cred_power = r.randint(-100,100)
        self.update_skin()

    def update_skin(self):

        g.sman.set_text(self.skin_id,g.TEXTIDS['plume'][convert_quality(self.quality)[0]])
        g.lman.set_text(self.lbl_qua_id,convert_quality(self.quality)+' '+trunc(self.quality))
        g.lman.set_text(self.lbl_cred_id,convert_streetcred(self.cred_power)+' '+str(self.cred_power))

    def drop_phase(self):

        x = 2
        qua = (self.quality*x + r.random())/(x+1)

        x = 3
        cred = (self.cred_power*x + r.randint(-100,100))/(x+1)

        phase = Phase(qua,cred)
        #print(phase.content)
        #print(convert_quality(qua),convert_streetcred(cred))

        return phase

class Phase():

        def __init__(self,quality,cred,):

            self.quality = quality
            self.cred = cred

            self.content = self.generate_content()

            self.them = r.choice(THEMES)

        def generate_content(self):

            nb = r.randint(3,6)
            s = r.choice(MOTS)
            for i in range(nb-1):
                s += ' ' + r.choice(MOTS)
            return s

        def str(self):

            s= '\n'
            s += self.content + '\t:' + convert_quality(self.quality) + '  ' + convert_streetcred(self.cred) + '\n'
            s+= str(self.them)
            s+= '\n'

            return s

#------# instrus

class Btmaker():

    def __init__(self,qua=0.5,name='Bokusan'):

        self.name = name

        #self.money = 1000

        self.quality = qua

    def drop_instru(self):

        x = 2
        qua = (self.quality*x + r.random())/(x+1)

        instru = Instru(qua,self.name)
        #print('instru '+convert_quality(qua))
        return instru

class Instru():

    def __init__(self,qua,author):

        self.quality = qua
        self.author = author

#------# sons

class Son():

    def __init__(self,instru,phases,name='cheh'):

        self.name = name

        self.instru = instru
        self.phases = phases

        self.quality = self.global_qua()
        self.cred = max([ x.cred for x in self.phases])

        print(convert_quality(self.quality),convert_streetcred(self.cred))

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


"""""""""""""""""""""""""""""""""""
 CLASSES GRAFIK
"""""""""""""""""""""""""""""""""""

class Zone():

    def __init__(self,box,textid='white',group='mid'):

        if textid[:4] == 'text':
            self.text_id = textid
        else:
            self.text_id = g.tman.addCol(*box.wh,c[textid])
        self.skin_id = g.sman.addSpr(self.text_id,box.xy,group)

        self.gex,self.gey = box.xy

        self._hoover = False

    def _realbox(self):
        return g.sman.box(self.skin_id)

    box = property(_realbox)

#------# ui

class Zone_UI(Zone):

    ## HOOVER WITH MOVEMENT OF MOUSE

    def __init__(self,box,name='thing',textid='white',group='mid'):
        super(Zone_UI,self).__init__(box,textid,group)

        self.name = name

        # label
        pos = box.x + box.w/2 , box.y + box.h + 20
        self.label = g.lman.addLab(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20,color=c['darkkhaki'])

    def hoover(self):
        g.lman.unhide(self.label)

    def unhoover(self):
        g.lman.unhide(self.label,True)

    def activate(self):
        print(self.skin_id,'activated')

#------# elements

class Zone_ELEM(Zone):

    ## HOOVER WITH MOVEMENT OF PERSO

    def __init__(self,box,name='thing',textid='white',group='mid',long=False):
        super(Zone_ELEM,self).__init__(box,textid,group)

        self.name = name
        self.longpress = long

        # label
        pos = box.x + box.w/2 , box.y + box.h + 20
        self.label = g.lman.addLab(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20)

        self.color = c['coral']

    def hoover(self):
        g.lman.unhide(self.label)
        self._hoover = True

    def unhoover(self):
        g.lman.unhide(self.label,True)
        self._hoover = False

    def activate(self,perso):
        #print(perso.name,'just activated',self.name)
        g.lman.modify(self.label,color=self.color)

        pyglet.clock.schedule_once(self.deactivate,0.5)

    def deactivate(self,dt):
        if self._hoover:
            g.lman.modify(self.label,color=c['white'])
        else:
            g.lman.modify(self.label,color=(255,255,255,0))

    def update(self):
        # label
        pos = (self.box[0] + self.box[2])/2 , self.box[3] + 20
        g.lman.modify(self.label,pos)

class Market(Zone_ELEM):

    def __init__(self,x,y):
        super(Market,self).__init__(box(x,y,200,200),'market','pink','mid',long=True)

    def activate(self,perso):
        super(Market,self).activate(perso)
        perso.rplum()

class Ordi(Zone_ELEM):

    def __init__(self,x,y):
        super(Ordi,self).__init__(box(x,y,150,200),'ordi','red','mid')

    def activate(self,perso):
        super(Ordi,self).activate(perso)
        perso.add_money(10000)

class Studio(Zone_ELEM):

    def __init__(self,x,y):
        super(Studio,self).__init__(box(x,y,50,200),'studio','blue','mid')

class Lit(Zone_ELEM):

    def __init__(self,x,y):
        super(Lit,self).__init__(box(x,y,300,150),'lit','darkgreen','mid',long=True)

    def activate(self,perso):
        super(Lit,self).activate(perso)
        if perso.plume != None:
            phase =perso.plume.drop_phase()
            print(phase.str())


ZONES = {}
ZONES['UI'] = {}
ZONES['ELEM'] = {}
# use ZONES['UI'] for gui
# use ZONES['ELEM'] for graphic element


#------# hud

class HUD():

    def __init__(self,group='hud',name='main'):

        self.name = name
        self.group = group

        #---#

        self.sprids = {}
        self.labids = {}

        #---#

        self.visible = True

    def addSpr(self,key,textid,xy_pos=(0,0),group=None):

        if group == None:
            group = self.group

        self.sprids[key] = g.sman.addSpr(textid,xy_pos,group)

    def addCol(self,key,box,color=(102, 102, 153,255),group=None):

        if group == None:
            group = self.group

        if type(color) == type(()):
            textid = g.tman.addCol(*box.wh,color)
        else:
            textid = g.tman.addCol(*box.wh,c[color])
        self.addSpr(key,textid,box.xy,group=group)

    def addLab(self,key,contenu,xy_pos=(0,0),group=None,font_size=30,anchor=('left','bottom'),color=(255,255,255,255)):

        if group == None:
            group = self.group

        self.labids[key] = g.lman.addLab(str(contenu),xy_pos,group=group,font_size=font_size,anchor=anchor,color=color)

        #print(xy_pos)

    def modifySpr(self,key,pos=None,scale=None):
        g.sman.modify(self.sprids[key],pos,scale)

    def unhide(self,hide=False):
        #print(self.labids)
        g.sman.unhide(self.sprids,hide)
        g.lman.unhide(self.labids,hide)

    def rollhide(self):
        self.unhide(self.visible)
        self.visible = not self.visible
        #print(self.visible)

    def delete(self):
        g.lman.delete(self.labids)
        g.sman.delete(self.sprids)

    ## oeoe

    def spr(self,key):
        return g.sman.spr(self.sprids[key])

    def lab(self,key):
        return g.lman.labels[self.labids[key]]

class PersoHUD(HUD):

    def __init__(self,perso):

        super(PersoHUD, self).__init__(group='hud',name='perso')

        self.perso = perso

        self.box = box(1700,460+150,200,400)
        self.padding = 50

        self.addCol('bg',self.box,group='mid')

        self.addLab('name',self.perso.name,(self.box.cx,self.box.y+self.box.h-self.padding),anchor=('center','center'))

        xcoin = self.box.cx
        ycoin = self.lab('name').y  - self.padding

        self.addSpr('coin_spr',g.TEXTIDS['item'][0],(xcoin,ycoin - g.tman.textures[g.TEXTIDS['item'][0]].height/2))
        self.addLab('coin_lab',convert_huge_nb(self.perso.money),(xcoin ,ycoin),font_size=20,color=c['yellow'],anchor=('right','center'))

    def update(self):

        g.lman.set_text(self.labids['coin_lab'],convert_huge_nb(self.perso.money))

class PlumHUD(HUD):

    def __init__(self,plum):

        super(PlumHUD, self).__init__(group='hud',name='plum')

        self.plum = plum

        self.box = box(1600,20,300,150)
        self.padding = 50

        self.addCol('bg',self.box,group='mid')

        self.addLab('quality',convert_quality(self.plum.quality),(self.box.x+self.box.w-self.padding,self.box.cy),anchor=('center','center'))

        xplum = self.lab('quality').x - self.padding
        yplum = self.box.cy

        self.addSpr('plum_spr',g.TEXTIDS['plume'][convert_quality(self.plum.quality)[0]])
        g.sman.modify(self.sprids['plum_spr'],scale=(0.4,0.4))
        g.sman.modify(self.sprids['plum_spr'],pos=(xplum - self.spr('plum_spr').width/2,yplum - self.spr('plum_spr').height/2))
        self.addLab('cred',convert_streetcred(self.plum.cred_power),(xplum - self.padding -10 ,yplum),font_size=20,anchor=('right','center'))



"""""""""""""""""""""""""""""""""""
 USEFUL FUNCTIONS
"""""""""""""""""""""""""""""""""""

def test():

    quality = r.random()
    cred_power = r.randint(-100,100)

    print(convert_quality(quality),convert_streetcred(cred_power))

    plum = Plume(quality,cred_power)
    print('\n')
    for i in range(20):
        phaz = []
        for i in range(4):
            phaz.append(plum.drop_phase())
        btmker = Btmaker(r.random())
        Son(btmker.drop_instru(),phaz)

    #return Plume(quality,cred_power)

def rplum():

    quality = r.random()
    cred_power = r.randint(-100,100)

    #print(convert_quality(quality),convert_streetcred(cred_power))

    return Plume(quality,cred_power)

def convert_quality(qua,test=(QUALITIES,QUALITIES_coeff)):


    if qua < test[1][0]:
        return test[0][0]
    else:
        return convert_quality(qua,(test[0][1:],test[1][1:]))

def convert_streetcred(cred,test=(CRED,CRED_coeff)):

    if cred < test[1][0]:
        return test[0][0]
    else:
        return convert_streetcred(cred,(test[0][1:],test[1][1:]))

def upgrade_qua(qua,bonus=True):

    if bonus:
        return qua + QUALITIES_up[convert_quality(qua)]
    else:
        return qua + QUALITIES_dwn[convert_quality(qua)]
