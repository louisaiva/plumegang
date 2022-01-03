

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
        return self.voc['roll']

voc = {}
voc['roll'] = ['oui','non','nik','yo','t ki ?','file ma thune']
voc['oui'] = [   'c\'est cela meme','vous avez bien raison','affirmatif','en effet','oui','yes','euh yep','ouai','oe','oe y\'a quoi'   ]
voc['non'] = [   'c\'est ma foi faux','vous avez tort','négatif','non','euh nope','nop','no','nn','non frr'   ]
voc['aled'] = [   'aleeeed','wsh tape moi pas','mdr t ki degage','tu fais quoi la','arrhrh je fuis','deso frero mé tape paas','pas bien la violence'
                    ,'t essaie de mourir frr ?','A L AIDE APPELEZ LA POLICE !'   ]
voc['bonjour'] = [   'mes plus sincères salutations','enchanté','bonjour','salut','plop','coucou','wesh','wesh la zone','wsh t ki'   ]
voc['au revoir'] = [   'que votre voyage continue agréablement','à une prochaine fois','au revoir','salut','à toute','la bise','bye','a+','ouai degage ouai'   ]
voc['omgcdelta'] = [   'omg tema c est delta','whaaa delta stp fais moi l amour','oh ptn je t aime delta'
                        ,'oh wow le rappeur le plus fort de france !','trop cools tes sons le reuf','delta fais moi des gosses stp','delta le s t bo', 'oh wow delta je suis joie',
                        'oh god file un autographe stp','oh chut regarde c est delta','ptainnn delta jtm']
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





###
# TEST GRAPHIQUE
###

class Roll_exp():

    def __init__(self,pos,perso,exps):

        self.exps = exps
        self.perso = perso

        self.pos = pos

        self.cur = None

        # calcul pos
        self.ray = 200
        self.pts,self.angs = points_on_circle(pos,self.ray,len(self.exps))

        # create labels
        self.labids = []
        for i in range(len(self.exps)):
            exp = self.exps[i]
            pt = self.pts[i]
            size = 20

            self.labids.append(g.lman.addLab(exp,pt,color=(255,255,200,255),font_size=size,anchor = ('center','center'),group='hud1'))

        # create bg circle
        self.bg = g.sman.addCircle(pos,self.ray*1.5,(80,80,120,160),group='hud-1')

    def update(self):

        if distance(g.M,self.pos) < 20:
            self.cur = None
            for i in range(len(self.labids)):
                g.lman.modify(self.labids[i],color=(255,255,200,255))
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
                if self.cur == i:
                    g.lman.modify(self.labids[i],color=(255,255,0,255))
                else:
                    g.lman.modify(self.labids[i],color=(255,255,200,255))

    def admit(self):
        self.delete()
        #print(self.cur)
        if self.cur != None:
            return self.exps[self.cur]
        return None

    def delete(self):
        g.lman.delete(self.labids)
        g.sman.delete(self.bg)
