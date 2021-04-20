
import random as r
import json
from src.utils import *
#import graphic as g

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
 CLASSES
"""""""""""""""""""""""""""""""""""


#------# phases

class Rappeur():

    def __init__(self,textid,plumtext_id,graph,labman,pos=(200,200),name='Delta'):

        # general

        self.name = name
        self.speed = 50

        self.street_score = 0

        self.money = 1000

        self.nb_fans = 0
        self.fans = []

        self.plume = rplum()

        self.graph = graph
        self.labman = labman
        self.plumtext_id = plumtext_id

        # skins

        self.skin_id = graph.addSpr(textid)
        graph.modify(self.skin_id,pos,(10,10))
        graph.addToGroup(self.skin_id,'up')

        self.plum_id = graph.addSpr(plumtext_id[convert_quality(self.plume.quality)[0]],(1500,40))
        graph.modify(self.plum_id,scale=(0.4,0.4))
        graph.addToGroup(self.skin_id,['up'])

        # labels

        self.label_name_id = labman.addLabel(self.name,(40,40))
        self.label_qua_id = labman.addLabel(convert_quality(self.plume.quality)+' '+trunc(self.plume.quality),(1600,60))
        self.label_cred_id = labman.addLabel(convert_streetcred(self.plume.cred_power)+' '+str(self.plume.cred_power),(1500,10),font_size=20)

    def rplum(self):
        self.plume = rplum()
        self.actualise_skins()


    def actualise_skins(self):

        #self.plum_id = graph.addSpr(plumtext_id[convert_quality(self.plume.quality)[0]],(1500,40))
        self.graph.set_text(self.plum_id,self.plumtext_id[convert_quality(self.plume.quality)[0]])
        self.labman.set_text(self.label_qua_id,convert_quality(self.plume.quality)+' '+trunc(self.plume.quality))
        self.labman.set_text(self.label_cred_id,convert_streetcred(self.plume.cred_power)+' '+str(self.plume.cred_power))


    def move(self,dir):
        x,y = self.graph.spr(self.skin_id).position
        if dir == 'R':
            self.graph.modify(self.skin_id,(x-self.speed,y))
        elif dir == 'L':
            self.graph.modify(self.skin_id,(x+self.speed,y))

class Plume():

    def __init__(self,qua,cred):

        self.quality = qua
        self.cred_power = cred

        self.level = 0

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
