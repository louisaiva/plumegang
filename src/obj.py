
import random as r
import json

######################## INIT

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

CRED = ['pire merde de la terre','sous-merde','merde'
        ,'victime','neutre','thug'
        ,'gangster','gros ganster','ennemi number one']
CRED_coeff = [-95,-80,-50,-10,10,50,80,95,101]

with open('../item/mots.json','r') as f:
    MOTS = json.load(f)


######################## CLASSES

class Rappeur():

    def __init__(self,name='Delta'):

        self.name = name


        self.street_score = 0

        self.money = 1000

        self.nb_fans = 0
        self.fans = []

        self.plume = None

    def get_Plume(plume):

        self.plume = plume

class Plume():

    def __init__(self,quality,cred_power):

        self.quality = quality
        self.cred_power = cred_power

        self.level = 0

    def drop_phase(self):

        x = 2
        qua = (self.quality*x + r.random())/(x+1)

        x = 2
        cred = (self.cred_power*x + r.randint(-100,100))/(x+1)

        phase = Phase(qua,cred)
        print(phase.content)

class Phase():

        def __init__(self,quality,cred,):

            self.quality = quality
            self.cred = cred

            self.content = self.generate_content()

        def generate_content(self):

            nb = r.randint(3,6)
            s = r.choice(MOTS)
            for i in range(nb-1):
                s += ' ' + r.choice(MOTS)
            return s


#################### USEFUL FUNCTIONS

def create_random_Plume():

    quality = r.random()
    cred_power = r.randint(-100,100)

    print(convert_quality(quality),convert_streetcred(cred_power))

    plum = Plume(quality,cred_power)
    print('\n')
    for i in range(20):
        plum.drop_phase()

    #return Plume(quality,cred_power)

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
