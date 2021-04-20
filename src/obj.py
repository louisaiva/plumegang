
import random as r
import json
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

    def __init__(self,textid,pos=(200,200),name='Delta'):

        # general

        self.name = name
        self.speed = 50

        #self.street_score = 0

        #self.money = 1000

        #self.nb_fans = 0
        #self.fans = []

        self.plume = rplum()

        self.element_colli = None

        # skins
        self.skin_id = g.sman.addSpr(textid)
        g.sman.modify(self.skin_id,pos,(10,10),'up')

        # labels
        self.label_name_id = g.lman.addLabel(self.name,(40,40))

    def rplum(self):
        self.plume.rplum()

    def update_skin(self):

        if self.plume != None:
            self.plume.update_skin()

    def move(self,dir):

        moved = False
        x,y = g.sman.spr(self.skin_id).position
        if dir == 'R':
            g.sman.modify(self.skin_id,(x-self.speed,y))
            moved = True
        elif dir == 'L':
            g.sman.modify(self.skin_id,(x+self.speed,y))
            moved = True

        if moved :
            self.check_colli()

    def check_colli(self):

        boxper = g.sman.box(self.skin_id)
        colli_elem = None
        for elem in ZONES['ELEM']:
            if collision(boxper,ZONES['ELEM'][elem].box()) :
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

    def hit(self):
        print(self.name,'hits the void')


class Plume():

    def __init__(self,qua,cred):

        self.quality = qua
        self.cred_power = cred

        self.level = 0

        # skins
        self.skin_id = g.sman.addSpr(g.TEXTIDS['plume'][convert_quality(self.quality)[0]],(1500,40),'up')
        g.sman.modify(self.skin_id,scale=(0.4,0.4))

        # labels
        self.lbl_qua_id = g.lman.addLabel(convert_quality(self.quality)+' '+trunc(self.quality),(1600,60))
        self.lbl_cred_id = g.lman.addLabel(convert_streetcred(self.cred_power)+' '+str(self.cred_power),(1500,10),font_size=20)

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

    def box(self):
        return g.sman.box(self.skin_id)

#------# ui

class Zone_UI(Zone):

    ## HOOVER WITH MOVEMENT OF MOUSE

    def __init__(self,box,name='thing',textid='white',group='mid'):
        super(Zone_UI,self).__init__(box,textid,group)

        self.name = name

        # label
        pos = box.x + box.w/2 , box.y + box.h + 20
        self.label = g.lman.addLabel(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20,color=c['darkkhaki'])

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
        self.label = g.lman.addLabel(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20)

    def hoover(self):
        g.lman.unhide(self.label)

    def unhoover(self):
        g.lman.unhide(self.label,True)

    def activate(self):
        print(self.name,'activated')

class Market(Zone_ELEM):

    def __init__(self,box,perso):
        super(Market,self).__init__(box,'market','pink','mid',long=True)

        self.perso = perso

    def activate(self):
        print(self.name,'activated')
        self.perso.rplum()


ZONES = {}
ZONES['UI'] = {}
ZONES['ELEM'] = {}
# use ZONES['UI'] for gui
# use ZONES['ELEM'] for graphic element


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
