"""
CODED by deltasfer
enjoy
"""

import random as r
import json,time,pyglet
from pyglet.window import key
from src.colors import *
from src.utils import *
from src import graphic as g
from src import names as n
from src import obj as o
from src import obj2 as o2
from src import voc as v
import pyglet.gl as gl

SIZE_SPR = 256
BOTS = []
CHEAT = False


"""'''''''''''''''''''''''''''''''''
'''''''TEXTURES TAB'''''''''''''''''
'''''''''''''''''''''''''''''''''"""

persos_skins = []
textures = {}
def update_textures(keys):
    global textures,persos_skins

    for x in keys:
        textids = g.TEXTIDS[x]
        persos_skins.append(x)
        textures[x] = {}

        if x != 'rapper': # NORMAL
            textures[x]['nothing'] = {}
            textures[x]['nothing']['R'] = [textids[0],textids[1]]
            textures[x]['nothing']['L'] = [textids[2],textids[3]]

            textures[x]['move'] = {}
            textures[x]['move']['R'] = [textids[4],textids[5]]
            textures[x]['move']['L'] = [textids[6],textids[7]]

            textures[x]['hit'] = {}
            textures[x]['hit']['R'] = [textids[8]]
            textures[x]['hit']['L'] = [textids[9]]

            textures[x]['write'] = {}
            textures[x]['write']['R'] = [textids[10],textids[11]]
            textures[x]['write']['L'] = [textids[12],textids[13]]

            textures[x]['wait'] = {}
            textures[x]['wait']['R'] = [textids[0]]
            textures[x]['wait']['L'] = [textids[2]]

            textures[x]['die'] = {}
            textures[x]['die']['R'] = [textids[14]]
            textures[x]['die']['L'] = [textids[14]]

            textures[x]['heal'] = {}
            textures[x]['heal']['R'] = [textids[15],textids[16]]
            textures[x]['heal']['L'] = [textids[15],textids[16]]

            textures[x]['door'] = {}
            textures[x]['door']['R'] = [textids[17],textids[18],textids[19],textids[20],textids[21]]
            textures[x]['door']['L'] = [textids[17],textids[18],textids[19],textids[20],textids[21]]

            textures[x]['act'] = {}
            textures[x]['act']['R'] = [textids[17+5],textids[18+5],textids[19+5],textids[20+5],textids[21+5]]
            textures[x]['act']['L'] = [textids[17+5],textids[18+5],textids[19+5],textids[20+5],textids[21+5]]

            textures[x]['stairs'] = {}
            textures[x]['stairs']['R'] = [textids[17],textids[18],textids[19],textids[20],textids[21]]
            textures[x]['stairs']['L'] = [textids[17],textids[18],textids[19],textids[20],textids[21]]
        else: # RAPPER
            textures[x]['nothing'] = {}
            textures[x]['nothing']['R'] = [textids[0],textids[1],textids[2]]
            textures[x]['nothing']['L'] = [textids[3],textids[4],textids[5]]

            textures[x]['move'] = {}
            textures[x]['move']['R'] = [textids[6],textids[7]]
            textures[x]['move']['L'] = [textids[8],textids[9]]

            textures[x]['hit'] = {}
            textures[x]['hit']['R'] = [textids[10]]
            textures[x]['hit']['L'] = [textids[11]]

            textures[x]['write'] = {}
            textures[x]['write']['R'] = [textids[10+2],textids[11+2]]
            textures[x]['write']['L'] = [textids[12+2],textids[13+2]]

            textures[x]['wait'] = {}
            textures[x]['wait']['R'] = [textids[0]]
            textures[x]['wait']['L'] = [textids[3]]

            textures[x]['die'] = {}
            textures[x]['die']['R'] = [textids[14+2]]
            textures[x]['die']['L'] = [textids[14+2]]

            textures[x]['heal'] = {}
            textures[x]['heal']['R'] = [textids[15+2],textids[16+2]]
            textures[x]['heal']['L'] = [textids[15+2],textids[16+2]]

            textures[x]['door'] = {}
            textures[x]['door']['R'] = [textids[19],textids[20],textids[21],textids[22],textids[23]]
            textures[x]['door']['L'] = [textids[19],textids[20],textids[21],textids[22],textids[23]]

            textures[x]['act'] = {}
            textures[x]['act']['R'] = [textids[19+5],textids[20+5],textids[21+5],textids[22+5],textids[23+5]]
            textures[x]['act']['L'] = [textids[19+5],textids[20+5],textids[21+5],textids[22+5],textids[23+5]]

            textures[x]['stairs'] = {}
            textures[x]['stairs']['R'] = [textids[19+10],textids[20+10],textids[21+10],textids[22+10]]
            textures[x]['stairs']['L'] = [textids[19+10],textids[20+10],textids[21+10],textids[22+10]]


"""""""""""""""""""""""""""""""""""
 METIERS
"""""""""""""""""""""""""""""""""""


class Metier():
    def __init__(self,perso,name='chomeur'):
        self.perso = perso
        self.meanings = ['veut thune']
        self.name = name

        self.dials = {}
        self.acts = {}

    def answer(self,voice):
        meaning = voice['meaning']
        if meaning == 'veut thune':
            return 'jsuis au chomdu'

    def add_arrival_dials(self,hum):
        pass

    def del_arrival_dials(self,hum):
        pass

class Distroguy(Metier):
    def __init__(self,perso):
        super(Distroguy,self).__init__(perso,'distroguy')

        self.meanings.append('veut thune')
        self.meanings.append('tu bosses?')

        self.dials['distroguy_dial_thune'] = { 't':0 , 'delay':None , 'meaning':'veut thune' , 'imp':81 , 'id':'distroguy_dial_thune' }
        self.dials['distroguy_dial_sign'] = { 't':0 , 'delay':None , 'meaning':'tu bosses?' , 'imp':80 , 'id':'distroguy_dial_sign' }

        self.acts['distroguy_act_thune'] = { 't':0 , 'delay':10 , 'giver':self.perso  , 'exp':'prendre'
                                , 'fct':o.distro.cashback , 'param':[] , 'answer':'merci' , 'id':'distroguy_act_thune'}

        self.acts['distroguy_act_sign'] = { 't':0 , 'delay':10 , 'giver':self.perso , 'exp':'signer chez distro (1$/jour)'
                                , 'fct':o.distro.sign , 'param':[] , 'answer':'trop cool' , 'id':'distroguy_act_sign'}

    def answer(self,voice):
        meaning = voice['meaning']
        hum = voice['h']
        if meaning == 'veut thune':
            #print(hum,'veut thune')
            if isinstance(hum, Rappeur) and hum in o.distro.rappeurs:
                if o.distro.caisse[hum] > 0:
                    exp = 'tu as ' + str(int(o.distro.caisse[hum])) + ' $ de côté, tu les veux ?'
                    self.act_cashback(hum,o.distro.caisse[hum])
                elif o.distro.caisse[hum] < 0:
                    exp = 'mdr non tu nous dois '+str(int(-o.distro.caisse[hum]))+ ' balles batard'
                else:
                    exp = 'fais de la thune d\'abord mdr'
                return exp

        elif meaning == 'tu bosses?':
            if isinstance(hum, Rappeur) and hum not in o.distro.rappeurs:
                exps = ['oue je fais de la thune en signant des rappeurs chez distrokid, ça pourrait t\'interesser !',
                        'ici on accueille des rappeurs qui veulent poster des sons sur le web, ça t\'intéresse ?',
                        'on signe des ptis rappeurs ici ! ça coûte pas cher pour poster tes sons, ça te dit ?',
                        'oh mais t\'es rappeur ! ici on signe des artistes pour qu\'ils puissent être sur spotify etc ! ça te dit ?']

                exp = r.choice(exps)

                act = self.acts['distroguy_act_sign']
                act['param'] = [hum]
                act['t'] = time.time()

                hum.del_dial('distroguy_dial_sign')
                dial = self.dials['distroguy_dial_thune']
                dial['t'] = time.time()
                hum.add_dial(dial)
                hum.add_act(act)
            else:
                exp = 'boarf je glande, pas bcp de taf ici'
            return exp

    def add_arrival_dials(self,hum):

        if isinstance(hum, Rappeur) and hum in o.distro.rappeurs:
            dial = self.dials['distroguy_dial_thune']
            dial['t'] = time.time()
            hum.add_dial(dial)

        dial = self.dials['distroguy_dial_sign']
        dial['t'] = time.time()
        hum.add_dial(dial)

    def del_arrival_dials(self,hum):
        for dialid in self.dials:
            hum.del_dial(dialid)

    ## distro

    def act_cashback(self,rapper,qté):

        rapper.del_dial('distroguy_dial_thune')
        act = self.acts['distroguy_act_thune']
        act['exp'] = 'prendre ('+trunc(qté,2)+'$)'
        act['param'] = [rapper]
        act['t'] = time.time()
        rapper.add_act(act)


"""""""""""""""""""""""""""""""""""
 HUMAINS
"""""""""""""""""""""""""""""""""""

class Human():

    def __init__(self,key_skin,pos,name='John',group='perso0',street='street1'):
        # general

        self.name = name
        self.money = 1000
        self.speed = r.randint(10,25)
        self.yspeed = 5
        self.runspeed = 100
        self.id = get_id('hum')

        self.cheat = False

        #life
        self.life = 100
        self.max_life = 100
        self.damage = r.randint(10, 15)

        #items
        self.keys = []

        #états
        self.cred = r.randint(-50,50)
        self.confidence = 100 #compris entre 0 et 100 -> décrit la peur (0) et la confidence (100)

        #combat
        self.hits_in_row = 0
        self.last_hit = 0

        # relations
        self.relations = {}
        self.mood = None

        #voc
        self.voc = v.dic
        self.keyids_voc = None
        self.roll = None

        #listener
        self.ear = []
        self.selfear = []
        self.delay_earin = 1
        self.acts = []
        self.dials = []

        #pos
        self.gex = pos[0] # general x
        self.gey = pos[1] # general y
        self.street = street

        #environ
        self.element_colli = None
        self.collis = []
        self.environ = []
        self.hum_env = []

        # track of time
        self.time_last_move = 0

        #do
        self.doing = ['nothing']
        self.dir = r.choice(('R','L'))
        self.todo = [] ## 'fuir' 'attack' 'move' 'talkin' 'followin'
        self.bigdoing = {'lab':None,'funct':None,'param':None,'imp':-10000}

        # skins
        self.textids = textures[key_skin]

        self.grp = group

        ##### HOOOOVER

        self._hoover = False
        self.color = c['coral']
        self.rspeak()
        self.loaded = False

    ### GENERAL

    def add_money(self,qté):
        self.money += qté

    def die(self):
        self.do('die')
        self.life = 0
        self.damage = 0
        self.speed = 0
        self.yspeed = 0

        for key in self.keys:
            self.drop(o.Key(key))

        if hasattr(self,'label_life'):
            g.sman.delete(self.label_life)
            del self.label_life
            g.sman.delete(self.label_conf)
            del self.label_conf

        g.bertran.schedule_once(self.delete,4)

    def delete(self,dt=0):

        o2.NY.CITY[self.street].del_hum(self)
        BOTS.remove(self)

    def add_key(self,street):
        if street not in self.keys:
            self.keys.append(street)

    # relations
    def relup(self,hum,qté,cat='hate/like'):
        if hum in self.relations:
            self.relations[hum][cat] += qté
            if self.relations[hum][cat] > 100:
                self.relations[hum][cat] = 100
            elif self.relations[hum][cat] < -100:
                self.relations[hum][cat] = -100

    def get_feel(self,hum):

        if hum in self.relations:
            #print(self.relations[hum]['hate/like'])
            return self.relations[hum]['hate/like']


    ### UPDATES

    def update_skin(self,dt=0.4,repeat=True):
        if hasattr(self,'skin_id'):

            ## change the right group compared to y pos

            k = int(g.gman.nb_perso_group*self.gey/o2.maxY)
            #print(k)
            g.sman.modify(self.skin_id,group='perso'+str(k))

            ## roll the animation
            max_roll = len(self.textids[self.doing[0]][self.dir])
            if self.roll_skin >= max_roll:
                self.roll_skin = 0

            g.sman.set_text(self.skin_id,self.textids[self.doing[0]][self.dir][self.roll_skin])
            if g.sman.spr(self.skin_id).width != SIZE_SPR:
                sc = SIZE_SPR//g.sman.spr(self.skin_id).width
                gl.glEnable(gl.GL_TEXTURE_2D)

                g.sman.modify(self.skin_id,scale=(sc,sc))

            self.roll_skin += 1
            if self.roll_skin >= max_roll:
                self.roll_skin = 0

            if repeat:
                g.bertran.schedule_once(self.update_skin, 0.2)

    def update_env(self):
        if self.alive:
            self.old_env = self.environ
            self.environ = o2.NY.CITY[self.street].environ(self)

            self.hum_oldenv = self.hum_env
            self.hum_env = list(filter(lambda x:x.get('type')=='hum',self.environ))
            self.hum_env = list(map(lambda x:x.get('elem'),self.hum_env))
            self.new_hum = list(filter(lambda x:x not in self.hum_oldenv,self.hum_env))

            nb_hum_env = len(self.hum_env)
            nb_hum_oldenv = len(self.hum_oldenv)

            for hum in self.hum_env:
                if hum not in self.relations:
                    self.relations[hum] = {'t':1,'last':-1,'hate/like':r.randint(-100,100),'peur/rassure':0}

                if self.relations[hum]['hate/like'] < -50:
                    imp = -self.relations[hum]['hate/like']-20
                    dial = { 't':time.time() , 'delay':None , 'meaning':'free insult' , 'imp':imp ,'id':'dial_insuult'}
                    self.add_dial(dial)

            if not True in list(map(lambda x:self.relations[x]['hate/like'] < -50,self.relations)):
                self.del_dial('dial_insuult')

            if nb_hum_oldenv > nb_hum_env:
                # si y'a des gens qui partent
                if nb_hum_env == 0:
                    # si on vient d'etre seul
                    self.empty_dial()

                    dial = { 't':time.time() , 'delay':10 , 'meaning':'parle seul' , 'imp':30 ,'id':'dial_parle_seul'}
                    self.add_dial(dial)

                t = time.time()
                for hum in self.hum_oldenv:
                    if hum not in self.hum_env:
                        self.relations[hum]['last'] = t

            elif nb_hum_env > 0 and nb_hum_env > nb_hum_oldenv:
                # si y'a des nouveaux gens qui arrivent
                self.del_dial('dial_parle_seul')
                dial = { 't':time.time() , 'delay':None , 'meaning':'bonjour' , 'imp':30 ,'id':'dial_bjr'}
                self.add_dial(dial)
                dial = { 't':time.time() , 'delay':None , 'meaning':'bien?' , 'imp':25 ,'id':'dial_uoka'}
                self.add_dial(dial)
                #dial = { 't':time.time() , 'delay':None , 'meaning':'au revoir' , 'imp':20 ,'id':'dial_bye'}
                #self.add_dial(dial)

        self.check_colli()

    def check_colli(self):

        street = o2.NY.CITY[self.street]

        ## CHANGER DANS PERSO
        self.collis = []

        for elem in list(map(lambda x:x.get('elem'),self.environ)):
            if collisionAB(self.gebox,elem.gebox) :
                self.collis.append(elem)

        if len(self.collis) > 0:
            self.collis.sort(key=lambda x:x.gey)
            #print(list(map(lambda x:x.name,self.collis)))

            y,yf = street.yyf
            d = yf-y
            yranges = [y]
            for i in range(len(self.collis)):
                yranges.append(y+(i+1)*(d/len(self.collis)))
            #print(yranges)

            k=0
            for i in range(len(self.collis)):
                if self.gey >= yranges[i] and self.gey <= yranges[i+1]:
                    k=i
            colli_elem = self.collis[k]
        else:
            colli_elem = None

        if type(self) == Perso:

            if self.element_colli != None:
                if colli_elem != None:
                    if colli_elem != self.element_colli :
                        self.element_colli.unhoover()
                        self.element_colli = colli_elem
                        self.element_colli.hoover()

                        ## on reinitialise les keys d'activation (ZS activaiton)
                        if key.Z in g.longpress:
                            del g.longpress[key.Z]
                        if key.S in g.longpress:
                            del g.longpress[key.S]

                else:
                    self.element_colli.unhoover()
                    self.element_colli = None

                    ## on reinitialise les keys d'activation (ZS activaiton)
                    if key.Z in g.longpress:
                        del g.longpress[key.Z]
                    if key.S in g.longpress:
                        del g.longpress[key.S]

            else:
                if colli_elem != None:
                    self.element_colli = colli_elem
                    self.element_colli.hoover()
        else:
            self.element_colli = colli_elem

    def update(self):

        t = time.time()

        #life
        if self.life < self.max_life and not 'heal' in list(map(lambda x:x['lab'],self.todo)):
            self.add_todo('heal',self.heal,20)

        #speaking
        if self.keyids_voc and self.loaded:
            x,y = self.box.cx,self.box.fy + 150
            #print(x,y)
            g.pman.modify_single(self.keyids_voc,setx=x,sety=y)
            #self.keyids_voc = g.pman.addLabPart(exp,(x,y),color=c['yellow'],key='say',anchor=('center','center'),group='up-1',vis=True,duree=20)

        #listening
        todel = []
        for voice in self.ear:
            if t-voice['t'] > self.delay_earin:
                todel.append(voice)
        for voice in todel:
            self.ear.remove(voice)
        todel = []
        for voice in self.selfear:
            if t-voice['t'] > 5*self.delay_earin:
                todel.append(voice)
        for voice in todel:
            self.selfear.remove(voice)

        #act/dial
        deleted_acts_dials = False
        todel = []
        for act in self.acts:
            if t-act['t'] > act['delay']:
                todel.append(act)
                deleted_acts_dials = True
        for act in todel:
            self.acts.remove(act)
        todel = []
        for dial in self.dials:
            if dial['delay'] != None and t-dial['t'] > dial['delay']:
                todel.append(dial)
                deleted_acts_dials = True
        for dial in todel:
            self.dials.remove(dial)
        if deleted_acts_dials and self.roll != None:
            self.roll.recreate()

        #combatting
        if (self.in_combat or True in list(map(lambda x:x.in_combat,self.hum_env))) :
            if t-self.last_hit > 5:
                self.hits_in_row = 0
                self.last_hit = 0
        else:

            ## confidence

            gens_effrayants = 0
            amis_rassurants = 0

            for hum in self.hum_env:
                if self.relations[hum]['peur/rassure'] < 0:
                    gens_effrayants += self.relations[hum]['peur/rassure']
                elif self.relations[hum]['peur/rassure'] > 0:
                    amis_rassurants += self.relations[hum]['peur/rassure']

            confidence = 100*self.life/self.max_life + gens_effrayants + amis_rassurants

            if confidence > 100:
                confidence = 100
            elif confidence < 0:
                confidence = 0

            if int(confidence) != int(self.confidence):
                if self.confidence > confidence:
                    self.confidence -= 1
                else:
                    self.confidence += 1

        #relations
        for hum in self.relations:
            if hum in self.hum_env:
                self.relations[hum]['t'] += 1
            else:
                self.relations[hum]['t'] -= 0.1

        if self.name == 'Delta':
            pass
            #print()

    def force_anim(self,perc,action='act',dir='L'):

        if hasattr(self,'skin_id'):
            n = len(self.textids[action][dir])
            # il faut au moins que y'en ai 2 sinon ça beug

            if perc > 0.95:
                g.sman.set_text(self.skin_id,self.textids[action][dir][n-1])
                return 0

            dp = 0.8/(n-1)
            for i in range(n-1):
                if perc > 0.2 + i*dp and perc <= 0.2 + (i+1)*dp:
                    g.sman.set_text(self.skin_id,self.textids[action][dir][i])


    ## DOIN

    def do(self,action='nothing'):

        if action not in self.doing:
            if action == 'die':
                self.doing.insert(0, action)
                self.undo()
                self.update_skin(repeat=False)
            elif self.alive:
                if action == 'nothing':
                    self.doing = ['nothing']
                    #print(self.name,'do notjing')

                elif action == 'hit':
                    self.doing.insert(0, action)
                    self.undo()
                    self.update_skin(repeat=False)
                    g.bertran.schedule_once(self.undo,0.1,'hit')

                elif action == 'write':
                    self.doing.insert(0, action)
                    self.undo()

                elif action == 'move':
                    self.doing.append(action)
                    self.undo()

                elif action == 'heal':
                    self.doing.append(action)
                    self.undo()
                    self.update_skin(repeat=False)

                elif action == 'wait':
                    self.doing.insert(0, action)
                    self.undo()
                    self.update_skin(repeat=False)

    def undo(self,dt=0,action='nothing'):

        if action in self.doing:
            self.doing.remove(action)
            if self.doing == []:
                self.do()

    def check_do(self):

        if time.time()-self.time_last_move > 0.2:
            if 'hit' not in self.doing and 'write' not in self.doing and 'wait' not in self.doing and 'die' not in self.doing and 'heal' not in self.doing:
                self.do()
            else:
                self.undo(0,'move')

    ## ACTION

    def movedt(self,dt,dir,speed=None,again=4):
        self.move(dir,speed)
        if again > 0:
            g.bertran.schedule_once(self.movedt,0.001,dir,again=again-1)

    def move(self,dir,speed=None):

        if self.alive :

            street = o2.NY.CITY[self.street]

            maxx = street.xxf
            maxy = street.yyf

            if not speed:
                speed = self.speed

            moved = False
            activated_smthg = False

            #R/L
            if 'write' not in self.doing and 'wait' not in self.doing:

                if dir == 'R' :
                    if (maxx[1] == None or maxx[1] > self.gex+speed+SIZE_SPR ):
                        self.gex+=speed
                        moved = True

                elif dir == 'L' and (maxx[0] == None or maxx[0] < self.gex-speed ):
                    self.gex-=speed
                    moved = True

            # up/down
            if dir == 'up':
                if maxy[1] > self.gey+self.yspeed:
                    self.gey+=self.yspeed
                    moved = True
            elif dir == 'down':
                if maxy[0] < self.gey-self.yspeed :
                    self.gey-=self.yspeed
                    moved = True

            ## check activations
            if type(self) == Perso:
                if dir == 'up':
                    if isinstance(self.element_colli, o.Zone_ACTIV) and self.element_colli.position == 'front':
                        self.element_colli.close(self)
                    if maxy[1] <= self.gey+self.yspeed and isinstance(self.element_colli, o.Zone_ELEM) and self.element_colli.position == 'back':

                        #we are moving -> stop heal and ...
                        moved = True

                        # launch longpress
                        if key.Z not in g.longpress:
                            g.longpress[key.Z] = time.time()

                        #get cooldown percentage + anim
                        perc = g.cooldown_one(key.Z,self.element_colli)
                        self.force_anim(perc,self.element_colli.perso_anim)

                        #activating
                        if perc > 1:
                            self.element_colli.activate(self)

                elif dir == 'down':
                    if isinstance(self.element_colli, o.Zone_ACTIV) and self.element_colli.position == 'back':
                        self.element_colli.close(self)
                    if maxy[0] >= self.gey-self.yspeed and isinstance(self.element_colli, o.Zone_ELEM) and self.element_colli.position == 'front':

                        #we are moving -> stop heal and ...
                        moved = True

                        # launch longpress
                        if key.S not in g.longpress:
                            g.longpress[key.S] = time.time()

                        #get cooldown percentage + anim
                        perc = g.cooldown_one(key.S,self.element_colli)
                        self.force_anim(perc,self.element_colli.perso_anim)

                        #activating
                        if perc > 1:
                            self.element_colli.activate(self)
            else:
                if dir == 'up':
                    #print(self.name,'up')
                    if maxy[1] <= self.gey+self.yspeed and isinstance(self.element_colli, o.Porte) and self.element_colli.position == 'back':

                        #we are moving -> stop heal and ...
                        moved = True

                        # launch longpress
                        if (self,'Z') not in g.longpress:
                            g.longpress[(self,'Z')] = time.time()

                        #get cooldown percentage + anim
                        perc = g.cooldown_one((self,'Z'),self.element_colli)
                        self.force_anim(perc,self.element_colli.perso_anim)

                        #activating
                        if perc > 1:
                            del g.longpress[(self,'Z')]
                            self.element_colli.activate(self)

                if dir == 'down':
                    if maxy[0] >= self.gey-self.yspeed and isinstance(self.element_colli, o.Porte) and self.element_colli.position == 'front':

                        #we are moving -> stop heal and ...
                        moved = True

                        # launch longpress
                        if (self,'S') not in g.longpress:
                            g.longpress[(self,'S')] = time.time()

                        #get cooldown percentage + anim
                        perc = g.cooldown_one((self,'S'),self.element_colli)
                        self.force_anim(perc,self.element_colli.perso_anim)

                        #activating
                        if perc > 1:
                            del g.longpress[(self,'S')]
                            self.element_colli.activate(self)

            ## checking thg
            if moved :
                if 'heal' in self.doing:
                    self.done_todo()

                if dir in ['R','L']:
                    if self.dir != dir:
                        self.dir = dir
                        self.do('move')
                        self.update_skin(repeat=False)
                    else:
                        self.do('move')
                else:
                    self.do('move')
                self.update_lab()
                self.update()

                self.time_last_move = time.time()
                self.check_colli()
            elif not activated_smthg and speed > self.speed:
                self.move(dir)

    def tp(self,x=None,y=None,street=None,arrival='back'):

        if x != None:
            oldx = self.box.x
            self.gex = x
            self.update_lab()
            if type(self) == Perso:
                g.Cam.tp(self.gex,oldx)

        if y != None:
            self.gey = y
            self.update_lab()

        if street != None:
            if self.street != street.name:
                self.element_colli = None
                if type(self) == Perso:
                    o2.NY.CITY[self.street].deload()

                o2.NY.CITY[self.street].del_hum(self)
                o2.NY.CITY[street.name].add_hum(self)
                self.street = street.name

                if type(self) == Perso:
                    o2.NY.CITY[self.street].load()

                if arrival == 'back':
                    self.tp(y=o2.NY.CITY[self.street].yyf[1])
                    self.gey+=4*self.yspeed
                    g.bertran.schedule_once(self.movedt,0.1,'down')
                elif arrival == 'front':
                    self.tp(y=o2.NY.CITY[self.street].yyf[0]-self.yspeed)
                    self.gey-=4*self.yspeed
                    g.bertran.schedule_once(self.movedt,0.1,'up')

                self.check_colli()

    def hit(self,dt=0):
        if self.alive:

            # on arrête le heal vu qu'on bouge
            if 'heal' in self.doing:
                self.done_todo()

            # et on bouge
            self.time_last_move = time.time()
            self.do('hit')

            # puis on vérifie si on touche qqchose
            if self.element_colli != None:

                if isinstance(self.element_colli,Human):
                    # là c'est un humain
                    self.last_hit = time.time()
                    self.relup(self.element_colli,self.damage,'peur/rassure')
                    self.element_colli.be_hit(self)

                elif isinstance(self.element_colli,o.Item):
                    # là c'est un item
                    self.element_colli.activate(self)

    def be_hit(self,hitter):

        if self.bigdoing['lab'] == 'heal':
            self.done_todo()

        ## skin
        if hasattr(self,'skin_id'):
            g.sman.add_filter(self.skin_id)
            g.bertran.unschedule(self.un_hit)
            g.bertran.schedule_once(self.un_hit, 0.4)

        dmg = hitter.damage + r.randint(-5,5)

        ## on affiche le label que si on se situe dans la bonne street évidemment
        if self.loaded:
            ## label +57
            s=convert_huge_nb(dmg)
            pos = self.box.cx +r.randint(-10,10),self.box.fy
            g.pman.addLabPart(s,pos,color=c['lightred'],key='dmg',font_name=1,anchor=('center','center'),group='up-1',vis=o2.NY.CITY[self.street].visible)

        ## dmging
        self.life -= dmg
        self.hits_in_row += 1
        hitter.cred += 1
        self.relup(hitter,-dmg)
        self.relup(hitter,-dmg,'peur/rassure')



        if (self.life <= 0) and 'die' not in self.doing:
            print(red(hitter.name + ' killed ' + self.name))
            self.die()

        if self.alive and type(self) != Perso:

            ## feelings
            #peur
            if dmg > self.life:
                # je suis oneshot j'ai PEUR => minimum
                self.confidence = 0
            else :
                self.confidence -= self.confidence/(self.life/dmg)


            if not self.in_combat:
                # 3 cas de figure : soit on est très confiant et on réplique direct
                # soit on est pas confiant et on dit calmos et on attend de se faire taper un peu plus
                # soit on est une tafiole et on fuit

                if self.confidence > 80:
                    self.add_todo('atak_'+hitter.id,self.attack_hum,80,[hitter])
                    #self.attack_hum(0,hitter)
                elif self.confidence > 40 and self.hits_in_row > 1:
                    self.add_todo('atak_'+hitter.id,self.attack_hum,80,[hitter])

            if self.confidence > 80:
                self.rsay('tveux mourir?')
            elif self.confidence > 40:
                self.rsay('stop taper')
            elif self.confidence > 20:
                g.bertran.unschedule(self.hit)
                g.bertran.unschedule(self.attack_hum)
                self.add_todo('fuir_'+hitter.id,self.fuir,100,[hitter,1000])
                self.add_todo('heal',self.heal,90)
                self.rsay('moi fuir')
            else:
                g.bertran.unschedule(self.hit)
                g.bertran.unschedule(self.attack_hum)
                self.add_todo('fuir_'+hitter.id,self.fuir,100,[hitter])
                self.add_todo('heal',self.heal,90)
                self.rsay('aled')


        self.last_hit = time.time()

    def un_hit(self,dt):
        if hasattr(self,'skin_id'):
            g.sman.del_filter(self.skin_id)

    def drop(self,thg):

        droppin = False
        if type(thg) == o.Key:
            if thg.target in self.keys:
                droppin = True
                self.keys.remove(thg.target)

        elif type(thg) == o.Plume and isinstance(self,Rappeur) and self.plume == thg:
            droppin = True
            if isinstance(self,Perso) : self.plumhud.delete()
            self.plume = None

        if droppin:
            w,h = self.box.wh
            x,y = self.gex,self.gey
            dx = 0
            if self.dir == 'R':
                dx += 150
            else:
                dx -= 150
            o.Item(thg,(x+w/2+dx,y),self.street)

    def grab(self,thg):

        if type(thg) == o.Plume and isinstance(self,Rappeur):
            if isinstance(self,Perso):
                if self.plume != None : self.plumhud.delete()
                self.plumhud = o.PlumHUD(thg)
            self.plume = thg
        elif type(thg) == o.Key:
            if thg.target not in self.keys:
                self.keys.append(thg.target)


    ## BOTS

    def being_bot(self):
        if 'die' not in self.doing:

            if type(self) not in [Perso]:

                #move
                choice = r.random()
                if choice>0.999:
                    x,y = o2.NY.CITY[self.street].rand_pos()

                    #self.move_until(0,(x,y))
                    self.add_todo('move_'+str(x)+'_'+str(y),self.move_until,param=[(x,y)])
                elif choice < 0.001: # change street
                    dest = o2.NY.CITY[self.street].get_rd_neighbor()
                    self.add_todo('go_street_'+dest.name,self.go_to_street,imp=10,param=[dest])

                #say the dial
                if True :
                    #acting/dialing
                    exp = None
                    chosen_dial = None
                    imp = 0
                    p = r.random()
                    if p < 0.2:
                        exp = self.voc.random()
                        imp = 20
                    else:
                        ptot = sum(list(map(lambda x:x.get('imp'),self.dials)))
                        if ptot < 100:
                            ptot = 100
                        for dial in self.dials:
                            prob = 0.1 + dial.get('imp')*0.8/ptot
                            if p < prob:
                                chosen_dial = dial
                                exp = self.voc.exp(dial['meaning'])
                                imp = dial.get('imp')
                                break

                    p = r.random()
                    if p < imp/20000:
                        if chosen_dial:
                            self.del_dial(chosen_dial['id'])
                        self.say(exp)

            ##todo
            if len(self.todo) > 0 and self.bigdoing != self.todo[0]:

                g.bertran.unschedule(self.bigdoing['funct'])
                self.bigdoing = self.todo[0]
                self.todo[0]['funct'](0,*self.todo[0]['param'])

    def done_todo(self):

        if len(self.todo) > 0:
            if self.bigdoing == self.todo[0]:
                del self.todo[0]
                g.bertran.unschedule(self.bigdoing['funct'])
                if self.bigdoing['lab'] == 'heal':
                    self.undo(0,'heal')

        if len(self.todo) == 0:
            self.bigdoing = {'lab':None,'funct':None,'param':None,'imp':-10000}

    def add_todo(self,lab,funct,imp=0,param=[]):

        # nouveau todo
        newtodo = {'lab':lab,'funct':funct,'imp':imp,'param':param}


        # on vérifie qu'il y est pas déjà et on supprim si jamai
        if funct == self.fuir:
            for todo in list(filter(lambda x:x['funct'] == self.attack_hum,self.todo)):
                if todo['param'][0] == param[0]:
                    self.todo.remove(todo)

        if newtodo not in self.todo:

            # on remplace si y'a meme lab
            self.del_todo(lab)

            # on ajoute le nouveau et on reclasse
            self.todo.append(newtodo)
            self.todo.sort(key=lambda x:x.get('imp'),reverse=True)

    def del_todo(self,lab):

        if type(lab) == type(''):
            # on delete suivant un lab précis
            for todo in list(filter(lambda x:x['lab'] == lab,self.todo)):
                self.todo.remove(todo)
        else:
            # on delete suivant une fonction
            for todo in list(filter(lambda x:x['funct'] == lab,self.todo)):
                self.todo.remove(todo)


    ## TO DO

    def move_until(self,dt=0,objective=(0,0)):

        reached = False,False
        x,y = objective

        #x
        if self.gex + self.speed >= x and self.gex <= x:
            reached = True,reached[1]
        elif self.gex > x:
            self.move('L')
        elif self.gex < x:
            self.move('R')

        #y
        if self.gey + self.speed >= y and self.gey <= y:
            reached = reached[0],True
        elif self.gey > y:
            self.move('down')
        elif self.gey < y:
            self.move('up')

        if reached != (True,True) and self.alive and not 'nothing' in self.doing:
            g.bertran.schedule_once(self.move_until,0.01,objective)
        else:
            self.done_todo()

    def go_to_street(self,dt,street):

        reached = False
        door = o2.NY.CITY[self.street].get_neighbor_door(street)
        if door != None and door.openable(self):
            x = door.box.x

            #x
            if self.gex + self.speed >= x and self.gex <= x:
                reached = True
            elif self.gex > x:
                self.move('L')
            elif self.gex < x:
                self.move('R')

            if reached:

                # on est au bon x
                #-> on doit bouger en y jusqu'à traverser la porte

                position = door.position

                #y
                if position == 'back':
                    self.move('up')
                elif position == 'front':
                    self.move('down')

            if self.street == street.name:
                #print('finii')
                self.del_todo(self.move_until)
                self.del_todo(self.go_to_street)
                self.done_todo()
            elif self.alive:
                g.bertran.schedule_once(self.go_to_street,0.01,street)
        else:
            self.done_todo()

    def attack_hum(self,dt,target):

        if self.alive and target.alive:

            if target.street != self.street:
                dest = o2.NY.CITY[target.street]
                self.add_todo('go_street_'+dest.name,self.go_to_street,imp=self.bigdoing['imp']+1,param=[dest])
            else:

                x,y = target.gex,target.gey
                speed = self.speed

                #x
                if target == self.element_colli:
                    dt = r.randint(1,2)/10
                    g.bertran.schedule_once(self.hit,dt)
                    g.bertran.schedule_once(self.attack_hum,r.randint(2,5)/10,target)
                else:
                    if target in self.collis:
                        #y
                        if self.gey > y:
                            self.move('down')
                        elif self.gey < y:
                            self.move('up')

                    if self.gex > x:
                        self.move('L',speed)
                    elif self.gex < x:
                        self.move('R',speed)

                    if self.alive and not 'nothing' in self.doing:
                        g.bertran.schedule_once(self.attack_hum,0.01,target)
                    else:
                        self.done_todo()
        elif not target.alive:
            self.done_todo()

    def fuir(self,dt,target,safety_distance=1000):

        if self.alive and target.alive:
            x = target.gex
            speed = self.speed

            if self.gex > x:
                self.move('R',speed)
            else:
                self.move('L',speed)

            if self.alive and abs(self.gex-x) < safety_distance and not 'nothing' in self.doing:
                g.bertran.schedule_once(self.fuir,0.01,target)
            else:
                #self.undo('move')
                self.done_todo()
        elif not target.alive:
            self.done_todo()

    def heal(self,dt=0):

        if self.alive and self.life <= self.max_life:
            if not (self.in_combat or True in list(map(lambda x:x.in_combat,self.hum_env))) and time.time()-self.time_last_move > 1:
                self.do('heal')
                heal = self.max_life//100
                self.life += heal
                if self.life > self.max_life:
                    self.life = self.max_life
                    self.done_todo()
                else:
                    g.bertran.schedule_once(self.heal,0.1)
            else:
                g.bertran.schedule_once(self.heal,0.1)


    ## SPEAKING

    def say(self,exp):
        if self.alive:

            ## on affiche le label que si on se situe dans la bonne street évidemment
            #if o2.NY.CITY[self.street].visible:

            duree = 20
            if len(exp) > duree:
                duree = len(exp)

            w=20
            if len(exp)>60:
                w=(len(exp)//3) + 1

            if self.keyids_voc:
                g.pman.delete(self.keyids_voc)

            # gaffe faut modifier aussi dans l'update
            x,y = self.box.cx,self.box.fy + 150
            self.keyids_voc = g.pman.addLabPart(exp,(x,y),color=c['yellow'],key='say',anchor=('center','center')\
                                    ,group='frontstreet',vis=o2.NY.CITY[self.street].visible,duree=duree,w=w)

            ## on dit un truc -> l'environnement l'entend
            #print(list(filter( lambda x:x.get('type') == 'hum' , self.environ)))
            for hum in list(filter( lambda x:x.get('type') == 'hum' , self.environ)):
                hum = hum.get('elem')
                hum.listen(self,exp)
            self.listen(self,exp)

    def rsay(self,type):
        exp = self.voc.exp(type)
        self.say(exp)

    def rspeak(self,dt=0):
        if hasattr(self,'skin_id') and 'die' not in self.doing:
            exp = self.voc.random()
            self.say(exp)
        #g.bertran.schedule_once(self.rspeak, r.randint(30,100))
        #print(self.name,'said',exp)

    def speak(self,dt=0):
        if hasattr(self,'skin_id'):
            exp = self.voc.random()
            self.say(exp)

    def rollspeak(self,pos):
        if self.roll != None:
            self.roll.delete()

        self.roll = v.Roll_exp(pos,self)

    def unroll(self):
        exp = self.roll.admit()
        if exp != None:
            self.say(exp)
        self.roll = None

    def remove_speak_lab(self,dt=0):
        self.keyids_voc = None


    ## LISTENING

    def listen(self,hum,exp):

        ## voice : ( time , perso , exp )
        voice = {'t':time.time(),'h':hum,'exp':exp}

        if hum != self:
            self.ear.append( voice )
            #print(self.name,'heard',hum.name)

            #self.understand(voice)
            g.bertran.schedule_once(self.understand, r.randint(3,6)/10,voice)
        else:
            voice['meaning'] = self.voc.extract_meaning(exp)
            self.selfear.append( voice )

    def understand(self,dt,voice):
        t,h,exp = voice.values()
        meaning = self.voc.extract_meaning(exp)

        if meaning and meaning not in list(map( lambda x:x.get('meaning') , self.selfear )):
            voice = {'t':t,'h':h,'exp':exp,'meaning':meaning}
            self.answer(voice)

    def answer(self,voice):

        ## ATTENTION CHANGER DANS GUY asussi (PEUT ETRE ~~~~)

        if type(self) != Perso:
            meaning = voice['meaning']

            exp = None
            if meaning == 'bonjour':
                exp = self.voc.exp(meaning)
            elif meaning == 'au revoir':
                exp = self.voc.exp(meaning)
            elif meaning == 'bien?':
                exp = self.voc.bienouquoi(self.life/self.max_life)
            elif meaning == 'veut thune':
                exp = self.voc.exp('non')
            elif meaning == 'random':
                if r.random() > 0.5:
                    exp = self.voc.exp('oui')
                else:
                    exp = self.voc.exp('non')

            elif meaning == 'free insult':
                hum = voice['h']
                if hum not in self.relations:
                    self.relations[hum] = {'t':1,'last':-1,'hate/like':r.randint(-100,100),'peur/rassure':0}
                    if self.relations[hum]['hate/like'] < -50:
                        imp = -self.relations[hum]['hate/like']-20
                        dial = { 't':time.time() , 'delay':None , 'meaning':'free insult' , 'imp':imp ,'id':'dial_insuult'}
                        self.add_dial(dial)

                prob_tapé = self.confidence*(-self.relations[hum]['hate/like'])/10000
                self.relup(hum,-10)

                #print(prob_tapé)
                p = r.random()
                if p < prob_tapé/2:
                    self.add_todo('atak_'+hum.id,self.attack_hum,80,[hum])
                if p < prob_tapé:
                    exp = self.voc.exp('free insult')

            if exp:
                self.say(exp)


    ## ACTS / DIALS

    def add_act(self,act):
        # ACT : { 't':float  ,  'delay':float/((((((None))))))  ,  'giver':hum  ,
        #   'exp':str  ,  'fct':funct  ,  'param':[]  ,  'answer':str ,'id': unique str}
        if not act['id'] in list(map(lambda x:x.get('id'),self.acts)):
            self.acts.append(act)
            if self.roll != None:
                self.roll.recreate()

    def del_act(self,actid,recreate=True):
        if actid in list(map(lambda x:x.get('id'),self.acts)):
            act = list(filter(lambda x:x.get('id') == actid,self.acts))[0]
            self.acts.remove(act)
            if recreate and self.roll != None:
                self.roll.recreate()

    def add_dial(self,dial):

        # DIAL : { 't':float  ,  'delay':float/None  ,   'meaning':str  , 'imp':int ,'id': unique str}
        # (imp -> importance : plus c'est eleve plus ça va etre haut dans la roue -> concerne les warnings et les dialogues de situation)

        # 100 : warning
        #  80 : situation
        #  50 : insulte
        #  10 : banal

        if not dial['id'] in list(map(lambda x:x.get('id'),self.dials)):
            self.dials.append(dial)
            if self.roll != None:
                self.roll.recreate()

    def del_dial(self,dialid):

        if dialid in list(map(lambda x:x.get('id'),self.dials)):
            self.dials.remove(list(filter(lambda x:x.get('id')==dialid,self.dials))[0])
            if self.roll != None:
                self.roll.recreate()

    def empty_dial(self):
        self.dials = []


    ## SPR/LABELS

    def load(self):

        if True:

            if not hasattr(self,'skin_id'):
                self.roll_skin = 0
                self.skin_id = g.sman.addSpr(self.textids[self.doing[0]][self.dir][0],(self.gex,self.gey),group=self.grp)

                self.update_skin()
                if self.outside:
                    g.Cyc.add_spr((self.skin_id,0.3))

            if not hasattr(self,'label'):
                #label
                pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 30
                self.label = g.lman.addLab(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20,group=self.grp)

            if not hasattr(self,'label_life') and self.alive:
                # spr life
                size_lifebar = 100
                size_fill = (self.life*size_lifebar)/self.max_life
                x,y = self.box.cx-size_lifebar/2 , self.box.fy +2

                self.label_life = g.sman.addSpr(g.TEXTIDS['utils'][5],(x,y),group=self.grp,vis=False)
                g.sman.modify(self.label_life,scale=(size_fill/32,5/32))

                # spr confidence
                size_lifebar = 150
                size_fill = (self.confidence*size_lifebar)/100
                x,y = self.box.cx-size_lifebar/2 , self.box.fy + 7

                self.label_conf = g.sman.addSpr(g.TEXTIDS['utils'][6],(x,y),group=self.grp,vis=False)
                g.sman.modify(self.label_conf,(x,y),scale=(size_fill/32,5/32))

        #speaking
        if self.keyids_voc:
            g.pman.unhide_single(self.keyids_voc)

        self.loaded = True

    def deload(self):
        g.bertran.unschedule(self.update_skin)
        g.bertran.unschedule(self.hit)
        g.bertran.unschedule(self.be_hit)
        g.bertran.unschedule(self.bigdoing['funct'])
        self.bigdoing = {'lab':None,'funct':None,'param':None,'imp':-10000}


        if hasattr(self,'skin_id'):
            g.Cyc.del_spr((self.skin_id,0.3))
            g.sman.delete(self.skin_id)
            del self.skin_id
        if hasattr(self,'label'):
            g.lman.delete(self.label)
            del self.label
        if hasattr(self,'label_life'):
            g.sman.delete(self.label_life)
            del self.label_life
            g.sman.delete(self.label_conf)
            del self.label_conf

        #speaking
        if self.keyids_voc:
            g.pman.unhide_single(self.keyids_voc,True)

        self.loaded = False

    def update_lab(self):
        if hasattr(self,'label'):
            # label
            pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 30
            g.lman.modify(self.label,pos)

        if hasattr(self,'label_life'):
            # spr life
            size_lifebar = 150
            size_fill = (self.life*size_lifebar)/self.max_life
            x,y = self.box.cx-size_lifebar/2 , self.box.fy + 2
            g.sman.modify(self.label_life,(x,y),scale=(size_fill/32,None))
            # spr confidence
            size_lifebar = 150
            size_fill = (self.confidence*size_lifebar)/100
            x,y = self.box.cx-size_lifebar/2 , self.box.fy + 7
            g.sman.modify(self.label_conf,(x,y),scale=(size_fill/32,None))

    def hoover(self):
        if hasattr(self,'label'):
            g.lman.unhide(self.label)
        if hasattr(self,'label_life'):
            g.sman.unhide(self.label_life)
            g.sman.unhide(self.label_conf)
            self._hoover = True

    def unhoover(self):
        if hasattr(self,'label'):
            g.lman.unhide(self.label,True)
        if hasattr(self,'label_life'):
            g.sman.unhide(self.label_life,True)
            g.sman.unhide(self.label_conf,True)
            self._hoover = False
    ##


    def __repr__(self):
        s = self.name +' ('+red(self.type) + ')'+' ['+ blue(self.street)+'] '
        return s

    def _type(self):
        return 'HUMAN'
    type = property(_type)
    def _outside(self):
        return o2.NY.CITY[self.street].outside
    outside = property(_outside)
    def _box(self):
        x,y,xf,yf = self.realbox
        w,h=xf-x,yf-y
        return box(x,y,w,h)
    box = property(_box)
    def _realbox(self):
        if hasattr(self,'skin_id'):
            return g.sman.box(self.skin_id)
        else:
            return 0,0,SIZE_SPR,SIZE_SPR
    realbox = property(_realbox)
    def _gebox(self):
        return self.gex,self.gey,self.gex+SIZE_SPR,self.gey+SIZE_SPR
    gebox = property(_gebox)
    def _in_combat(self):

        in_c = False
        if (time.time()-self.last_hit < 5):
            in_c = True
        if self.attack_hum == self.bigdoing['funct']:
            in_c = True

        if not in_c:
            self.last_hit = 0
            self.hits_in_row = 0

        return in_c
    in_combat = property(_in_combat)
    def _alive(self):
        if self.life > 0:
            return True
        return False
    alive = property(_alive)

# les gens que tu croises dans la rue
class Fan(Human):

    def __init__(self,key_skin,pos,name=None,street='street1'):

        if name == None:
            name = r.choice(n.names)

        super(Fan,self).__init__(key_skin,pos,name,group='perso0',street=street)


        rge = [ r.randint(-100,100),r.randint(-100,100) ]
        self.cred_range = [ min(rge),max(rge) ]

        self.streams = {}
        self.likes = {}
        self.artists = []

    def like(self,son,direct=True):
        if son.cred >= self.cred_range[0] and son.cred <= self.cred_range[1]:
            if son not in self.likes:
                self.likes[son] = True
                if not self in son.author.fans:
                    #print(self.name + ' aime ce son !')

                    if direct: son.author.addfan(self)
                    else: return self
                if not son.author in self.artists:
                    self.artists.append(son.author)

                else:
                    #print(self.name + ' aime deja un autre son !')
                    pass
            else:
                #print(self.name + ' aime deja ce son !')
                pass
        else:
            #print(self.name + ' cheh')
            pass
        return None

    def stream(self,son):
        son.stream()
        if son not in self.streams:
            self.streams[son] = 0
        self.streams[son] += 1
        if self.streams[son] > 1:
            self.like(son)

    def update_env(self):
        super(Fan,self).update_env()

        if self.artists != [] and not self.keyids_voc:
            for hum in self.hum_env:
                if hum.name in list(map(lambda x:x.name,self.artists)):
                    exp = self.voc.omg_c_delta(hum.name)
                    print(self.name,':',exp)
                    self.say(exp)

    def __str__(self):
        s = '-100 '
        for i in range(-10,11):
            if i*10 >= self.cred_range[0] and i*10 <= self.cred_range[1]:
                s+='#'
            else:
                s+='_'
        s+= ' 100'

        return s + ' ' + self.name

    def _type(self):
        return 'FAN'
    type = property(_type)

# travaille dans un shop ou autre
class Guy(Fan):

    def __init__(self,key_skin,pos,name='Alphonse',metier=Metier,street='street1'):

        super(Guy,self).__init__(key_skin,pos,name,street=street)

        ## check if in BOTS (souvent les guys sont ajoutés directement depuis leur shop)
        if self not in BOTS:
            BOTS.append(self)

        ## crée son metier:
        self.metier = metier(self)

    def update_env(self):
        super(Guy,self).update_env()

        ## RAJOUTE LES DIALS DU METIER AUX nouveaux VENUS
        for hum in self.hum_env:
            if hum not in self.hum_oldenv:
                if hum != self:
                    self.metier.add_arrival_dials(hum)

        ## ENLEVE LES DIALS DU METIER A CEUX QUI SONT PARTI
        for hum in self.hum_oldenv:
            if hum not in self.hum_env:
                self.metier.del_arrival_dials(hum)

    def answer(self,voice):

        meaning = voice['meaning']
        #print(meaning)
        exp = None

        # on check si le metier donne un comportement metier
        if meaning in self.metier.meanings:
            exp = self.metier.answer(voice)

        if exp:
            self.say(exp)
        else:
            # sinon on fait un comportement d'humain
            super(Guy,self).answer(voice)

    ### label
    def load(self):
        super(Guy,self).load()
        if not hasattr(self,'label_work'):
            pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 8
            self.label_work = g.lman.addLab('-'+self.metier.name+'-',pos,anchor = ('center','bottom'),font_size=15,group=self.grp,vis=False,color=c['white'])

    def deload(self):
        super(Guy,self).deload()
        if hasattr(self,'label_work'):
            g.lman.delete(self.label_work)
            del self.label_work

    def update_lab(self):
        super(Guy,self).update_lab()
        if hasattr(self,'label_work'):
            pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 8
            g.lman.modify(self.label_work,pos)

    def hoover(self):
        super(Guy,self).hoover()
        if hasattr(self,'label_work'):
            g.lman.unhide(self.label_work)

    def unhoover(self):
        super(Guy,self).unhoover()
        if hasattr(self,'label_work'):
            g.lman.unhide(self.label_work,True)

    def _type(self):
        return 'GUY'
    type = property(_type)

# les rappeurs
class Rappeur(Fan):

    def __init__(self,key_skin,pos,name=None,street='street1'):

        if name == None:
            name = r.choice(n.rappeurs)
            n.rappeurs.remove(name)

        super(Rappeur,self).__init__(key_skin,pos,name,street=street)

        #self.textids = text_rap

        self.qua_score = 0

        self.disco = []

        self.nb_streams = 0
        self.nb_fans = 0
        self.fans = []

        self.plume = o.rplum(self.name)

    def rplum(self):
        if self.plume != None:
            self.plume.delete()
        self.plume = o.rplum(self.name)

    def release_son(self,son,fans,day,label):
        self.disco.append(son)
        son.release(self,day,label)

        aa = o.a(son.quality)
        x = (son.quality-self.qua_score) * self.nb_fans

        print(son,'a='+str(int(aa)),'x='+str(int(x)))

        ii = [ r.randint(0,len(fans)-1) for _ in range(int(aa)+int(x))]

        newfans = []
        for ind in ii:
            fan = fans[ind]
            liked = fan.like(son,False)
            if liked != None:
                newfans.append(liked)
        self.addfans(newfans)

        self.update_scores()

    def die(self):
        self.drop(self.plume)
        super(Rappeur,self).die()

    # env
    def update_env(self):

        super(Rappeur,self).update_env()

        for hum in self.hum_env:
            if hum not in self.hum_oldenv:
                if hum != self and hum in self.fans:
                    dial = { 't':time.time() , 'delay':None , 'meaning':'omgcdelta' , 'imp':60 ,'id':'dial_omgcdelta'}
                    hum.add_dial(dial)

        for hum in self.hum_oldenv:
            if hum not in self.hum_env:
                if hum in self.fans:
                    hum.del_dial('dial_omgcdelta')

    ##

    def load(self):
        super(Rappeur,self).load()
        if False:
            if not hasattr(self,'label_plume') and self.plume != None:
                x = g.lman.labels[self.label].x
                y = g.lman.labels[self.label].y

                self.label_plume = g.sman.addSpr(g.TEXTIDS[type(self.plume).__name__.lower()][o.convert_quality(self.plume.quality)[0]],(x,y),group=self.grp,vis=False)

                sc = g.lman.labels[self.label].content_height
                w,h = g.sman.sprites[self.label_plume].width,g.sman.sprites[self.label_plume].height
                g.sman.modify(self.label_plume,scale=(sc/w,sc/h))

        #print('loaded',self.name)

    def deload(self):
        super(Rappeur,self).deload()
        if hasattr(self,'label_plume'):
            g.sman.delete(self.label_plume)
            del self.label_plume

        #print('deloaded',self.name)

    def update_lab(self):
        super(Rappeur,self).update_lab()
        if hasattr(self,'label_plume'):
            if self.plume != None:
                x = g.lman.labels[self.label].x+g.lman.labels[self.label].content_width/2+5
                y = g.lman.labels[self.label].y
                g.sman.modify(self.label_plume,(x,y))
            else:
                g.sman.delete(self.label_plume)
                del self.label_plume

        elif self.plume != None and hasattr(self,'label'):
            x = g.lman.labels[self.label].x
            y = g.lman.labels[self.label].y

            self.label_plume = g.sman.addSpr(g.TEXTIDS[type(self.plume).__name__.lower()][o.convert_quality(self.plume.quality)[0]],(x,y),group=self.grp,vis=False)

            sc = g.lman.labels[self.label].content_height
            w,h = g.sman.sprites[self.label_plume].width,g.sman.sprites[self.label_plume].height
            g.sman.modify(self.label_plume,scale=(sc/w,sc/h))

    def hoover(self):
        super(Rappeur,self).hoover()
        if hasattr(self,'label_plume'):
            g.sman.unhide(self.label_plume)

    def unhoover(self):
        super(Rappeur,self).unhoover()
        if hasattr(self,'label_plume'):
            g.sman.unhide(self.label_plume,True)

    ##

    def update_scores(self):

        sons = self.disco[-2:]
        qua_score = sum([ i.quality for i in sons])/len(sons)
        #self.cred = max([ i.cred for i in sons])

        self.qua_score = qua_score

    def addfan(self,fan):
        self.nb_fans+=1

    def addfans(self,fans):
        for fan in fans:
            self.fans.append(fan)
        self.nb_fans+=len(fans)

    def addstream(self):
        self.nb_streams += 1

    def add_money(self,qté):
        self.money += qté

    def _type(self):
        return 'RAPPER'
    type = property(_type)

#toa
class Perso(Rappeur):

    def __init__(self,key_skin,pos=(400,175),name='Delta',street='home',fill=True):

        super(Perso,self).__init__(key_skin,pos,name,street=street)

        self.max_life = 500
        self.damage = 40
        self.life = self.max_life
        self.speed = g.SPEED
        self.runspeed = g.RSPEED

        # hud
        self.hud = o.PersoHUD(self)
        self.lifehud = o.LifeHUD(self)
        self.credhud = o.CredHUD(self)
        self.plumhud = o.PlumHUD(self.plume)
        self.invhud = o.InventHUD(self,fill)
        self.sonhud = o.SonHUD(self)

        self.bigmap = o.Map(self)
        self.relhud = o.RelHUD(self)
        self.minirelhud = o.MiniRelHUD(self)

        self.cheat = CHEAT

        #self.load()

    # cheat
    def cheat(self):
        self.life = self.max_life
        self.cred = 0
        self.lifehud.update()
        self.credhud.update()

    def cheat_plumson(self):
        if self.plume != None:
            self.plumhud.delete()
        self.plume = o.splum(self.name)
        self.plumhud = o.PlumHUD(self.plume)

        self.invhud.catch(o.sson(self.name))

    def add_dial(self,dial):
        super(Perso,self).add_dial(dial)
        #print(list(map(lambda x:x.get('meaning'),self.dials)))

    # huds

    def rplum(self):
        if self.plume != None:
            self.plumhud.delete()
        super(Perso,self).rplum()
        self.plumhud = o.PlumHUD(self.plume)

    def be_hit(self,hitter):
        super(Perso,self).be_hit(hitter)
        self.credhud.update()
        self.lifehud.update()

    def heal(self,dt=0):
        super(Perso,self).heal(dt)
        self.credhud.update()
        self.lifehud.update()

    def release_son(self,son,fans,day,label):
        super(Perso,self).release_son(son,fans,day,label)
        self.credhud.update()

    def auto_release(self,label):

        choiced_son = None
        for son in self.invhud.inventory['son']:
            if not son.item._released:
                choiced_son = son.item
                break
        if choiced_son != None:
            self.release_son(choiced_son,BOTS,g.Cyc.day,label)

    ## particles

    def addfan(self,fan):
        super(Perso,self).addfan(fan)
        s = '+1'
        pos = g.lman.labels[self.hud.labids['fan_lab']].x +r.randint(-2,2) ,g.lman.labels[self.hud.labids['fan_lab']].y+20
        g.pman.addLabPart(s,pos,color=c['lightgreen'],key='icons',font_name=1,anchor=('right','center'),group='up-1',vis=self.hud.visible)

    def addfans(self,fans):
        super(Perso,self).addfans(fans)
        s = '+'+str(len(fans))
        pos = g.lman.labels[self.hud.labids['fan_lab']].x +r.randint(-2,2) ,g.lman.labels[self.hud.labids['fan_lab']].y+20
        g.pman.addLabPart(s,pos,color=c['lightgreen'],key='icons',font_name=1,anchor=('right','center'),group='up-1',vis=self.hud.visible)

    def addstream(self):
        super(Perso,self).addstream()
        s = '+1'
        pos = g.lman.labels[self.hud.labids['stream_lab']].x +r.randint(-2,2) ,g.lman.labels[self.hud.labids['stream_lab']].y+20
        g.pman.addLabPart(s,pos,color=c['lightblue'],key='icons',font_name=1,anchor=('right','center'),group='up-1',vis=self.hud.visible)

    def addstreams(self,nb):
        super(Perso,self).addstream()
        s = '+'+str(nb)
        pos = g.lman.labels[self.hud.labids['stream_lab']].x +r.randint(-2,2) ,g.lman.labels[self.hud.labids['stream_lab']].y+20
        g.pman.addLabPart(s,pos,color=c['lightgreen'],key='icons',font_name=1,anchor=('right','center'),group='up-1',vis=self.hud.visible)

    def add_money(self,qté):
        super(Perso,self).add_money(qté)
        if qté < 0:
            s= convert_huge_nb(qté)
        else:
            s='+' + convert_huge_nb(qté)
        pos = g.lman.labels[self.hud.labids['coin_lab']].x +r.randint(-2,2),g.lman.labels[self.hud.labids['coin_lab']].y+20
        g.pman.addLabPart(s,pos,color=c['yellow'],key='icons',font_name=1,anchor=('right','center'),group='up-1',vis=self.hud.visible)

    def update(self):

        super(Perso,self).update()
        self.relhud.update()
        self.minirelhud.update()

    def assign_poto(self,hum):
        self.poto = hum
        print(hum.name,'assigned to potooooo')
        self.minirelhud.assign_target(self.poto)


    ## colli hoover

    def _in_combat(self):
        return (time.time()-self.last_hit < 5)
    in_combat = property(_in_combat)

    def _type(self):
        return 'PERSO'
    type = property(_type)
