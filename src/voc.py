

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

    def bienouquoi(self,perc):
        if perc > 0.8:
            return self.exp('cavabien')
        elif perc < 0.2:
            return self.exp('cavapabien')
        else:
            return self.exp('cavaboarf')

    # understanding
    def extract_meaning(self,exp):
        for meaning in self.voc:
            if exp.lower() == meaning or exp in self.voc[meaning]:
                return meaning


voc = {}
voc['oui'] = [   'c\'est cela meme','vous avez bien raison','affirmatif','en effet','oui','yes','euh yep','ouai','oe','oe y\'a quoi'   ]
voc['non'] = [   'c\'est ma foi faux','vous avez tort','négatif','non','euh nope','nop','no','nn','nik','non frr'   ]
voc['tu bosses?'] = [   'tu fais quoi ?','tu fous quoi ici','tu fais quoi ?','tu bosses ici','vous faites quoi ici ?'   ]
voc['bien?'] = [   'bien ou quoi frr','comment ça va ?','sku ?','ça baigne ?','bien le reuf ?','ça dit quoi','u good ?','quoi de neuf ?','bien ?','\'sup ?'   ]
voc['aled'] = [   'aleeeed','wsh tape moi pas','mdr t ki degage','tu fais quoi la','arrhrh je fuis','deso frero mé tape paas','pas bien la violence'
                    ,'t essaie de mourir frr ?','A L AIDE APPELEZ LA POLICE !'   ]
voc['bonjour'] = [   'mes plus sincères salutations','enchanté','bonjour','salut','plop','coucou','wesh','wesh la zone','wsh t ki','t ki','yo'
                        ,'wsh le gang',   ]
voc['merci'] = [   'merci','merce','thx','merci beaucoup','mercee','tu régales','ça fait zizir','oh merce','merci le zin','tu fais plaaiz','thanks broo'   ]
voc['trop cool'] = [   'ohh trop cool','trop cool','incroyable','ça fait zizir','ptain trop bienn','trop dla bouule','je suis joie','oh yaaay','lezgooo','lezgongue','ouuh yeaah'   ]

voc['cavabien'] = ['yaas on é là','trop bien le reuf','yeeep de ouf','carrément bien poto','grave jsuis a donf là','ptain ouai de ouf hein jsuis alaiz']
voc['cavapabien'] = ['arh bof jsuis en train de crever','arh non jmeurs','euh bof c\'est plutot la mort là','bah on est sur un niveau de mort qwa'
                ,'bof tavu mon sang qui coule là ?','mal','très mal','à peu près le néant bien']
voc['cavaboarf'] = ['boarf on é là hein','j\'y travaille','mouais'
                ,'bof on sfait chier quoi','comme un lundi','ca va','on é là hein','ça paasse']

voc['au revoir'] = [   'que votre voyage continue agréablement','à une prochaine fois','au revoir','salut','à toute','la bise','bye','a+','ouai degage ouai'   ]
voc['omgcdelta'] = [   'omg tema c est delta','whaaa delta stp fais moi l amour','oh ptn je t aime delta'
                        ,'oh wow le rappeur le plus fort de france !','trop cools tes sons le reuf'
                        ,'delta fais moi des gosses stp','delta le s t bo', 'oh wow delta je suis joie',
                        'oh god file un autographe stp','oh chut regarde c est delta','ptainnn delta jtm']
voc['veut thune'] = [   'file ma thune','file ta thune','enculé file moi mes sous','tu mdois du flouz gars','t\'as ma thune ?' ]
voc['parle seul'] = [   'ptdr je parle tout seul','pk jparle frr ya personne','mdrr je parle on dirait c\'est pas moi qui parle j\'ai juré'
                            ,'jparle vraiment tout seul là ? mdrr jsuis fou','ah merde mdr jsuis tout seul','j aime le silence' ]
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
        size = 20
        #acts
        for i in range(len(self.acts)):
            exp = self.acts[i]['exp']
            pt = self.pts[i]

            self.labids.append(g.lman.addLab(exp,pt,color=(255,100,100,150),font_size=size,anchor = ('center','center'),group='ui',use_str_bien=True))
        j = len(self.acts)
        #exps
        for i in range(len(self.exps)):
            exp = self.exps[i]
            pt = self.pts[i+j]

            self.labids.append(g.lman.addLab(exp,pt,color=(255,255,100,150),font_size=size,anchor = ('center','center'),group='ui',use_str_bien=True))

        # create bg circle
        self.bg = g.sman.addCircle(pos,self.ray*1.5,(80,80,120,180),group='ui-1')

    def update(self):

        """if len(self.acts+self.exps) != len(self.labids):
            self.recreate()"""

        if distance(g.M,self.pos) < 20:
            self.cur = None
            for i in range(len(self.labids)):
                if i >= len(self.acts):
                    g.lman.modify(self.labids[i],color=(255,255,100,180))
                else:
                    g.lman.modify(self.labids[i],color=(255,100,100,180))
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
                        g.lman.modify(self.labids[i],color=(255,255,100,180))
                else:
                    if self.cur == i:
                        g.lman.modify(self.labids[i],color=(255,0,0,255))
                    else:
                        g.lman.modify(self.labids[i],color=(255,100,100,180))

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

        # ACT : { 't':float  ,  'giver':hum  ,  'exp':str  ,  'fct':funct  ,  'param':[]  ,  'answer':str ,'id': str}

        act = self.acts[self.cur]

        act['fct'](*act['param'])

        self.perso.del_act(act['id'],recreate=False)

        return self.perso.voc.exp(act['answer'])

    def get_exps(self):

        dials = sorted(self.perso.dials,key= lambda x:x.get('imp'),reverse=True)
        #print(dials,self.perso.dials)
        exps = []
        for dial in dials:
            exps.append(self.perso.voc.exp(dial['meaning']))

        ## toujours un truc random
        exps.append('~')

        return exps

    def recreate(self):

        self.delete()

        self.exps = self.get_exps()
        self.acts = self.perso.acts

        self.cur = None

        # calcul pos
        self.ray = 200
        self.pts,self.angs = points_on_circle(self.pos,self.ray,len(self.acts+self.exps))

        # create labels
        self.labids = []
        size = 20
        #acts
        for i in range(len(self.acts)):
            exp = self.acts[i]['exp']
            pt = self.pts[i]

            self.labids.append(g.lman.addLab(exp,pt,color=(255,100,100,150),font_size=size,anchor = ('center','center'),group='ui',use_str_bien=True))
        j = len(self.acts)
        #exps
        for i in range(len(self.exps)):
            exp = self.exps[i]
            pt = self.pts[i+j]

            self.labids.append(g.lman.addLab(exp,pt,color=(255,255,100,150),font_size=size,anchor = ('center','center'),group='ui',use_str_bien=True))

        # create bg circle
        self.bg = g.sman.addCircle(self.pos,self.ray*1.5,(80,80,120,180),group='ui-1')
