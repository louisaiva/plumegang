

## Chaque phrase (expression) a plusieurs particularités qui vont définir si/quand/pourquoi un bot la prononce :

##  1. Un registre de langage (wsh la zone != mes sincères salutations) (de -100 hyper poli à 100 vulgaire)
##  2. Une signification (bonjour != bonsoir)

"""
def Exp():

    def __init__(self,exp,reg=0):

        self.cont = exp
        self.reg=reg
"""

import random as r
from src import graphic as g
from src import obj as o
from src import perso as p
from src.utils import *

class Dico():
    def __init__(self,voc):
        self.voc = voc
        self.roll_exp = ['oui','non','yo','~','file ta thune']

    def exp(self,sign='oui',cred=0):
        return r.choice(self.voc[sign])

    def omg_c_delta(self,nom='delta'):
        text = r.choice(self.voc['omgcdelta'])
        if 'delta' in text:
            return text.replace('delta',nom)
        return text

    def random(self):
        return r.choice(self.voc['random'])

    def roll(self):
        return self.roll_exp

    # understanding
    def extract_meaning(self,exp):
        for meaning in self.voc:
            if exp.lower() == meaning or exp in self.voc[meaning]:
                return meaning

    def answer(self,voice):

        meaning = voice['meaning']
        if meaning == 'bonjour':
            return self.exp(meaning)
        elif meaning == 'au revoir':
            return self.exp(meaning)
        elif meaning == 'veut thune':
            return self.exp('non')
        elif meaning == 'random':
            if r.random() > 0.5:
                return self.exp('oui')
            else:
                return self.exp('non')


voc = {}
voc['oui'] = [   'c\'est cela meme','vous avez\nbien raison','affirmatif','en effet','oui','yes','euh yep','ouai','oe','oe y\'a quoi'   ]
voc['non'] = [   'c\'est ma\nfoi faux','vous avez tort','négatif','non','euh nope','nop','no','nn','nik','non frr'   ]
voc['aled'] = [   'aleeeed','wsh tape moi pas','mdr t ki\ndegage','tu fais quoi la','arrhrh je fuis','deso frero\nmé tape paas','pas bien la violence'
                    ,'t essaie de\nmourir frr ?','A L AIDE APPELEZ\nLA POLICE !'   ]
voc['bonjour'] = [   'mes plus sincères\nsalutations','enchanté','bonjour','salut','plop','coucou','wesh','wesh la zone','wsh t ki','t ki','yo'
                        ,'wsh il fait\nbeau la',   ]
voc['merci'] = [   'merci','merce','thx','merci beaucoup','mercee','tu régales','ça fait zizir','oh merce','merci le zin','tu fais plaaiz','thanks broo'   ]
voc['au revoir'] = [   'que votre voyage\ncontinue agréablement','à une prochaine fois','au revoir','salut','à toute','la bise','bye','a+','ouai degage ouai'   ]
voc['omgcdelta'] = [   'omg tema\nc est delta','whaaa delta stp\nfais moi l amour','oh ptn je\nt aime delta'
                        ,'oh wow le rappeur\nle plus fort de france !','trop cools tes\nsons le reuf','delta fais moi\ndes gosses stp','delta le s t bo', 'oh wow delta\nje suis joie',
                        'oh god file un\nautographe stp','oh chut regarde\nc est delta','ptainnn delta jtm']
voc['veut thune'] = [   'file ma thune','file ta thune','enculé file\nmoi mes sous','tu mdois du\nflouz gars','t\'as ma thune ?' ]
voc['parle seul'] = [   'ptdr je parle\ntout seul','pk jparle frr\nya personne','mdrr je parle\non dirait c\'est pas\nmoi qui parle j\'ai juré'
                            ,'jparle vraiment\ntout seul là ? mdrr\njsuis fou','ah merde mdr\njsuis tout seul','j aime le silence' ]
voc['random'] = [
                'wow le developpeur est si beau c\'est incroyable',
                'humm le createur est si séduisant tu trouves pas ?',
                'wsh il fait beau la',
                'aaah j\'ai faim sa mère',
                'ptn j\'ai le seum j\'ai encore perdu ma confiance en moi',
                'casse couille de pas percer là',
                'je hais les rappeurs',
                'j\'adore jouer à la pétanque',
                'bon antoine daniel cquand tu fais clyde vanilla 2 ?',
                'aaa',
                'trop d\'la boule j\'débarque comme roucool',
                'sku',
                'ç\'cu',
                'ptain envie d\'caner',
                '*scof scof*',
                'nan mé wesh drake d\'où tu refuses mon feat',
                ]

dic = Dico(voc)



''''''' ROLL '''''''''''''''''''''''''''

###
# TEST GRAPHIQUE
###

class Roll_exp():

    def __init__(self,pos,perso):

        self.perso = perso

        self.exps = self.get_exps()
        self.acts = perso.acts

        self.pos = pos

        self.cur = None

        # calcul pos
        self.ray = 200
        self.pts,self.angs = points_on_circle(pos,self.ray,len(self.acts+self.exps))

        # create labels
        self.labids = []
        #acts
        for i in range(len(self.acts)):
            exp = self.acts[i]['exp']
            pt = self.pts[i]
            size = 20

            self.labids.append(g.lman.addLab(exp,pt,color=(255,100,100,150),font_size=size,anchor = ('center','center'),group='ui',max_width=20))
        j = len(self.acts)
        #exps
        for i in range(len(self.exps)):
            exp = self.exps[i]
            pt = self.pts[i+j]
            size = 20

            self.labids.append(g.lman.addLab(exp,pt,color=(255,255,100,150),font_size=size,anchor = ('center','center'),group='ui'))

        # create bg circle
        self.bg = g.sman.addCircle(pos,self.ray*1.5,(80,80,120,160),group='ui-1')

    def update(self):

        if distance(g.M,self.pos) < 20:
            self.cur = None
            for i in range(len(self.labids)):
                if i >= len(self.acts):
                    g.lman.modify(self.labids[i],color=(255,255,100,150))
                else:
                    g.lman.modify(self.labids[i],color=(255,100,100,150))
        elif len(self.labids) == 1:
            self.cur = 0
            g.lman.modify(self.labids[self.cur],color=(255,255,0,255))
        else:
            ang = ang_from_pos(g.M,self.pos)
            for i in range(len(self.angs)):
                if i==0:
                    if ang <= self.angs[i+1] or ang >= self.angs[0]:
                        self.cur = 0
                        break
                elif i != len(self.angs)-1:
                    if ang >= self.angs[i] and ang <= self.angs[i+1]:
                        self.cur = i
                        break
                else:
                    if ang >= self.angs[i] and ang <= self.angs[0]:
                        self.cur = i
                        break

            for i in range(len(self.labids)):
                if i >= len(self.acts):
                    if self.cur == i:
                        g.lman.modify(self.labids[i],color=(255,255,0,255))
                    else:
                        g.lman.modify(self.labids[i],color=(255,255,100,150))
                else:
                    if self.cur == i:
                        g.lman.modify(self.labids[i],color=(255,0,0,255))
                    else:
                        g.lman.modify(self.labids[i],color=(255,100,100,150))

    def admit(self):
        self.delete()
        #print(self.cur)
        if self.cur != None:

            if self.cur >= len(self.acts):
                ## on est dans les exps
                if self.exps[self.cur-len(self.acts)] == '~':
                    return self.perso.voc.random()
                else:
                    return self.exps[self.cur-len(self.acts)]
            else:
                ## on est dans les acts
                return self.act()

        return None

    def delete(self):
        g.lman.delete(self.labids)
        g.sman.delete(self.bg)

    def act(self):

        ## si on est là c'est que le joueur a reçu une proposition à répondre (accepter ou autre)
        ## et qu'il la suit

        ## le rôle de la roll est de faire cette action puis de renvoyer un msg (ou r) que le perso va dire

        # ACT : { 't':float  ,  'giver':hum  ,  'recever':hum  ,  'exp':str  ,  'fct':funct  ,  'param':[]  ,  'answer':str }

        act = self.acts[self.cur]

        act['fct'](*act['param'])

        self.perso.del_act(act)

        return self.perso.voc.exp(act['answer'])

    def get_exps(self):

        dials = sorted(self.perso.dials,key= lambda x:x.get('imp'),reverse=True)
        print(dials,self.perso.dials)
        exps = []
        for dial in dials:
            exps.append(self.perso.voc.exp(dial['meaning']))

        ## toujours un truc random
        exps.append('~')

        return exps
