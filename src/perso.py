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
from src import obj as o
from src import obj2 as o2
from src import voc as v

SIZE_SPR = 256
BOTS = []

#graphic



class Human():

    def __init__(self,textids,pos,name='John',group='perso-1',street='street1'):
        # general

        self.name = name
        self.speed = r.randint(10,25)
        self.yspeed = 5
        self.runspeed = 100
        self.play = 'play'

        #life
        self.life = 100
        self.max_life = 100
        self.damage = r.randint(10, 110)

        #cred
        self.cred = r.randint(-50,50)

        #voc
        self.voc = v.dic
        self.keyids_voc = None
        self.roll = None

        #pos
        self.gex = pos[0] # general x
        self.gey = pos[1] # general y
        self.street = street

        self.money = 1000

        self.element_colli = None
        self.environ = []

        # track of time
        self.time_last_move = 0

        self.doing = ['nothing']
        self.dir = r.choice(('R','L'))

        # skins
        if type(self) in [Human,Fan,Perso]:

            self.textids = {}
            self.textids['nothing'] = {}
            self.textids['nothing']['R'] = [textids[0],textids[1]]
            self.textids['nothing']['L'] = [textids[2],textids[3]]

            self.textids['move'] = {}
            self.textids['move']['R'] = [textids[4],textids[5]]
            self.textids['move']['L'] = [textids[6],textids[7]]

            self.textids['hit'] = {}
            self.textids['hit']['R'] = [textids[8]]
            self.textids['hit']['L'] = [textids[9]]

            self.textids['write'] = {}
            self.textids['write']['R'] = [textids[10],textids[11]]
            self.textids['write']['L'] = [textids[12],textids[13]]

            self.textids['wait'] = {}
            self.textids['wait']['R'] = [textids[0]]
            self.textids['wait']['L'] = [textids[2]]

            self.textids['die'] = {}
            self.textids['die']['R'] = [textids[14]]
            self.textids['die']['L'] = [textids[14]]

        self.grp = group

        ##### HOOOOVER

        self._hoover = False
        self.color = c['coral']
        self.rspeak()

    def update_skin(self,dt=0.4,repeat=True):

        max_roll = len(self.textids[self.doing[0]][self.dir])
        if self.roll_skin >= max_roll:
            self.roll_skin = 0

        g.sman.set_text(self.skin_id,self.textids[self.doing[0]][self.dir][self.roll_skin])
        if g.sman.spr(self.skin_id).width != SIZE_SPR:
            sc = SIZE_SPR//g.sman.spr(self.skin_id).width
            g.sman.modify(self.skin_id,scale=(sc,sc))

        self.roll_skin += 1
        if self.roll_skin >= max_roll:
            self.roll_skin = 0

        if repeat:
            g.bertran.schedule_once(self.update_skin, 0.2)

    def add_money(self,qté):
        self.money += qté

    def update_env(self):
        if self.alive:
            self.environ = o2.NY.CITY[self.street].environ(self)

    ##

    def do(self,action='nothing'):

        if action not in self.doing:

            if action == 'nothing':
                self.doing = ['nothing']

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

            elif action == 'wait':
                self.doing.insert(0, action)
                self.undo()
                self.update_skin(repeat=False)

            elif action == 'die':
                self.doing.insert(0, action)
                self.undo()
                self.update_skin(repeat=False)

    def undo(self,dt=0,action='nothing'):

        if action in self.doing:
            self.doing.remove(action)
            if self.doing == []:
                self.do()

    def check_do(self):

        if 'hit' not in self.doing and 'write' not in self.doing and 'wait' not in self.doing and 'die' not in self.doing:
            if time.time()-self.time_last_move > 0.2:
                self.do()

    def move(self,dir,street,run=False):

        maxx = street.xxf
        maxy = street.yyf

        if run:
            speed = self.runspeed
        else:
            speed = self.speed

        if 'write' not in self.doing and 'wait' not in self.doing and 'die' not in self.doing:

            moved = False
            if dir == 'R' :
                if (maxx[1] == None or maxx[1] > self.gex+speed+g.sman.spr(self.skin_id).width ):
                    self.gex+=speed
                    moved = True

            elif dir == 'L' and (maxx[0] == None or maxx[0] < self.gex-speed ):
                self.gex-=speed
                moved = True

            elif dir == 'up' and maxy[1] > self.gey+self.yspeed:
                self.gey+=self.yspeed
                moved = True

            elif dir == 'down' and maxy[0] < self.gey-self.yspeed :
                self.gey-=self.yspeed
                moved = True

            if moved :
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
            elif run:
                self.move(dir,street)

    def tp(self,x=None,y=None,street=None):

        if x != None:
            oldx = self.box.x
            self.gex = x
            self.update_lab()
            g.Cam.tp(self.gex,oldx)

        if y != None:
            self.gey = y
            self.update_lab()

        if street != None:
            if self.street != street.name:
                self.element_colli = None
                o2.NY.CITY[self.street].deload()
                o2.NY.CITY[street.name].load()
                self.street = street.name
                self.check_colli(street)

        #print('tp : x',x,'y',y,'street',street,'\n')

    def update_lab(self):
        if hasattr(self,'label'):
            # label
            pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 20
            g.lman.modify(self.label,pos)

    def be_hit(self,hitter):

        ## attention faut réécrire dans Perso aussi

        #print(self.name,'hit by',hitter.name)
        self.rsay('aled')
        g.sman.filter(self.skin_id)
        g.bertran.unschedule(self.un_hit)
        g.bertran.schedule_once(self.un_hit, 0.4)

        self.life -= hitter.damage
        hitter.cred += 1
        self.cred += 1

        if (self.life <= 0 or self.cred > 100 or self.cred < -100) and 'die' not in self.doing:
            self.die()

        s=convert_huge_nb(hitter.damage)
        pos = self.box.cx +r.randint(-10,10),self.box.fy
        g.pman.addLabPart(s,pos,color=c['lightred'],key='dmg',font_name=1,anchor=('center','center'),group='up-1',vis=True)

    def un_hit(self,dt):
        if hasattr(self,'skin_id'):
            g.sman.filter(self.skin_id,(255,255,255))

    def die(self):
        self.do('die')
        self.life = 0
        self.damage = 0
        self.speed = 0
        self.yspeed = 0

        g.bertran.schedule_once(self.delete,4)

    def delete(self,dt=0):

        o2.NY.CITY[self.street].del_hum(self)
        BOTS.remove(self)


    ## BOTS

    def being_bot(self):
        if type(self) not in [Rappeur,Perso] and 'die' not in self.doing:

            if r.random() > 0.99995:
                self.rspeak()

            if self.doing == ['nothing'] and r.random()>0.999:
                x,y = self.gex + r.randint(-2000,2000), self.gey + r.randint(-20,20)


                if x > o2.NY.CITY[self.street].rxf :
                    x = o2.NY.CITY[self.street].rxf
                elif x < o2.NY.CITY[self.street].x:
                    x = o2.NY.CITY[self.street].x

                """if type(self) == Perso:
                    print('omg new direction',x,y)"""
                #print(self.name,'moving from',(self.gex,self.gey),'to',objective)
                self.move_until(0,(x,y))

    def move_until(self,dt=0,objective=(0,0)):

        reached = False,False
        x,y = objective

        #x
        if self.gex + self.speed >= x and self.gex <= x:
            reached = True,reached[1]
        elif self.gex > x:
            self.move('L',o2.NY.CITY[self.street])
        elif self.gex < x:
            self.move('R',o2.NY.CITY[self.street])

        #y
        if self.gey + self.speed >= y and self.gey <= y:
            reached = reached[0],True
        elif self.gey > y:
            self.move('down',o2.NY.CITY[self.street])
        elif self.gey < y:
            self.move('up',o2.NY.CITY[self.street])

        if reached != (True,True) and self.alive and not 'nothing' in self.doing:
            g.bertran.schedule_once(self.move_until,0.01,objective)

    ## SPEAKING

    def say(self,exp,duree=20):
        if self.alive:
            if self.keyids_voc:
                g.pman.delete(self.keyids_voc)

            # gaffe faut modifier aussi dans l'update
            x,y = self.box.cx,self.box.fy + 100
            self.keyids_voc = g.pman.addLabPart(exp,(x,y),color=c['yellow'],key='say',anchor=('center','center')\
                                ,group='up-1',vis=True,duree=duree,max_width=20)

    def rsay(self,type,duree=20):
        exp = self.voc.exp(type)
        self.say(exp,duree)

    def update(self):
        if self.keyids_voc:
            x,y = self.box.cx,self.box.fy + 100
            #print(x,y)
            g.pman.modify_single(self.keyids_voc,setx=x,sety=y)
            #self.keyids_voc = g.pman.addLabPart(exp,(x,y),color=c['yellow'],key='say',anchor=('center','center'),group='up-1',vis=True,duree=20)

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

        self.roll = v.Roll_exp(pos,self,self.voc.roll())

    def unroll(self):
        exp = self.roll.admit()
        if exp != None:
            self.say(exp)
        self.roll = None

    def remove_speak_lab(self,dt=0):
        self.keyids_voc = None

    ## hoover

    def hoover(self):
        if hasattr(self,'label'):
            g.lman.unhide(self.label)
            self._hoover = True

    def unhoover(self):
        if hasattr(self,'label'):
            g.lman.unhide(self.label,True)
            self._hoover = False

    ## load deload

    def load(self):
        if not hasattr(self,'skin_id'):
            self.roll_skin = 0
            self.skin_id = g.sman.addSpr(self.textids[self.doing[0]][self.dir][0],(self.gex,self.gey),group=self.grp)

            self.update_skin()

        if not hasattr(self,'label'):
            pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 20
            self.label = g.lman.addLab(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20,group='mid')

        #print('loaded',self.name)

    def deload(self):
        g.bertran.unschedule(self.update_skin)
        g.bertran.unschedule(self.move_until)

        if hasattr(self,'skin_id'):
            g.sman.delete(self.skin_id)
            del self.skin_id
        if hasattr(self,'label'):
            g.lman.delete(self.label)
            del self.label

        #print('deloaded',self.name)

    ##

    def _box(self):
        x,y,xf,yf = self.realbox
        w,h=xf-x,yf-y
        return box(x,y,w,h)
    box = property(_box)

    def _realbox(self):
        if hasattr(self,'skin_id'):
            return g.sman.box(self.skin_id)
        else:
            return 0,0,0,0
    realbox = property(_realbox)

    def _alive(self):
        if self.life > 0:
            return True
        return False
    alive = property(_alive)

# les gens que tu croises dans la rue
class Fan(Human):

    def __init__(self,textids,pos,name=None,street='street1'):

        if name == None:
            name = r.choice(n.names)

        super(Fan,self).__init__(textids,pos,name,group='perso',street=street)


        rge = [ r.randint(-100,100),r.randint(-100,100) ]
        self.cred_range = [ min(rge),max(rge) ]

        self.streams = {}
        self.likes = {}
        self.artists = []

    def like(self,son,direct=True):
        if son.cred >= self.cred_range[0] and son.cred <= self.cred_range[1]:
            if son not in self.likes:
                self.likes[son] = True
                if not self in son.perso.fans:
                    #print(self.name + ' aime ce son !')

                    if direct: son.perso.addfan(self)
                    else: return self
                if not son.perso in self.artists:
                    self.artists.append(son.perso)

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
        #print( list(map( lambda x:x.get('nom'),   list(filter(lambda x:x.get('type')=='hum',self.environ))  )) )
        if self.artists != [] and not self.keyids_voc:
            #print(self.name,'est fan de',list(map(lambda x:x.name,self.artists)))
            for hum in list(filter(lambda x:x.get('type')=='hum',self.environ)):
                #print(hum.get('nom'),list(map(lambda x:x.name,self.artists)))
                if hum.get('nom') in list(map(lambda x:x.name,self.artists)):
                    exp = self.voc.omg_c_delta(hum.get('nom'))
                    print(self.name,':',exp)
                    self.say(exp,60)

    def __str__(self):
        s = '-100 '
        for i in range(-10,11):
            if i*10 >= self.cred_range[0] and i*10 <= self.cred_range[1]:
                s+='#'
            else:
                s+='_'
        s+= ' 100'

        return s + ' ' + self.name

# travaille dans un shop ou autre
class Guy(Fan):

    def __init__(self,textids,pos,name='Alphonse',street='street1'):

        super(Guy,self).__init__(textids,pos,name,street=street)

        # skins
        self.textids = {}
        self.textids['nothing'] = {}
        self.textids['nothing']['R'] = [textids[0]]
        self.textids['nothing']['L'] = [textids[0]]

        self.textids['move'] = {}
        self.textids['move']['R'] = [textids[0]]
        self.textids['move']['L'] = [textids[0]]

        self.textids['hit'] = {}
        self.textids['hit']['R'] = [textids[0]]
        self.textids['hit']['L'] = [textids[0]]

        self.textids['write'] = {}
        self.textids['write']['R'] = [textids[0]]
        self.textids['write']['L'] = [textids[0]]

        self.textids['wait'] = {}
        self.textids['wait']['R'] = [textids[0]]
        self.textids['wait']['L'] = [textids[0]]

        self.textids['die'] = {}
        self.textids['die']['R'] = [textids[0]]
        self.textids['die']['L'] = [textids[0]]

        ## check if in BOTS (souvent les guys sont ajoutés directement depuis leur shop)
        if self not in BOTS:
            BOTS.append(self)

# les rappeurs
class Rappeur(Fan):

    def __init__(self,textids,pos,name=None,street='street1'):

        if name == None:
            name = r.choice(n.rappeurs)
            n.rappeurs.remove(name)

        super(Rappeur,self).__init__(textids,pos,name,street=street)

        if type(self) != Perso:
            # skins
            self.textids = {}
            self.textids['nothing'] = {}
            self.textids['nothing']['R'] = [textids[0],textids[1],textids[2],textids[3]]
            self.textids['nothing']['L'] = [textids[0],textids[1],textids[2],textids[3]]

            self.textids['move'] = {}
            self.textids['move']['R'] = [textids[0]]
            self.textids['move']['L'] = [textids[0]]

            self.textids['hit'] = {}
            self.textids['hit']['R'] = [textids[0],textids[1],textids[2],textids[3]]
            self.textids['hit']['L'] = [textids[0],textids[1],textids[2],textids[3]]

            self.textids['write'] = {}
            self.textids['write']['R'] = [textids[0],textids[1],textids[2],textids[3]]
            self.textids['write']['L'] = [textids[0],textids[1],textids[2],textids[3]]

            self.textids['wait'] = {}
            self.textids['wait']['R'] = [textids[0]]
            self.textids['wait']['L'] = [textids[0]]

            self.textids['die'] = {}
            self.textids['die']['R'] = [textids[0]]
            self.textids['die']['L'] = [textids[0]]

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

    def drop_plume(self):
        if self.plume != None:
            w,h = self.box.wh
            x,y = self.gex,self.gey
            dx = 0
            if self.dir == 'R':
                dx += 150
            else:
                dx -= 150
            o.Item(self.plume,(x+w/2+dx,y),self.street)
            self.plume = self.plume.delete()

    def grab_plume(self,plume):
        if self.plume != None:
            self.plume.delete()
        self.plume = plume

    def release_son(self,son,fans,day):
        self.disco.append(son)
        son.release(self,day)

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
        self.drop_plume()
        super(Rappeur,self).die()

    ##

    def load(self):
        super(Rappeur,self).load()
        if not hasattr(self,'label_plume') and self.plume != None:
            x = g.lman.labels[self.label].x
            y = g.lman.labels[self.label].y

            self.label_plume = g.sman.addSpr(g.TEXTIDS[self.plume.type().lower()][o.convert_quality(self.plume.quality)[0]],(x,y),group=self.grp,vis=False)

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

        elif self.plume != None:
            x = g.lman.labels[self.label].x
            y = g.lman.labels[self.label].y

            self.label_plume = g.sman.addSpr(g.TEXTIDS[self.plume.type().lower()][o.convert_quality(self.plume.quality)[0]],(x,y),group=self.grp,vis=False)

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

#toa
class Perso(Rappeur):

    def __init__(self,textids,pos=(400,175),name='Delta',street='home',fill=True):

        super(Perso,self).__init__(textids,pos,name,street=street)

        self.max_life = 4800
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

        self.load()

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

    # huds

    def rplum(self):
        if self.plume != None:
            self.plumhud.delete()
        super(Perso,self).rplum()
        self.plumhud = o.PlumHUD(self.plume)

    def grab_plume(self,plume):
        if self.plume != None:
            self.plumhud.delete()
        super(Perso,self).grab_plume(plume)
        self.plumhud = o.PlumHUD(self.plume)

    def drop_plume(self):
        if self.plume != None:
            self.plumhud.delete()
        super(Perso,self).drop_plume()

    def be_hit(self,hitter):
        #print(self.name,'hit by',hitter.name)
        g.sman.filter(self.skin_id)
        g.bertran.unschedule(self.un_hit)
        g.bertran.schedule_once(self.un_hit, 0.4)

        self.life -= hitter.damage
        hitter.cred += 1
        self.cred += 1
        self.credhud.update()

        if self.life <= 0:
            self.life = 0
        self.lifehud.update()

        if (self.life <= 0 or self.cred > 100 or self.cred < -100) and 'die' not in self.doing:
            self.die()

        s=convert_huge_nb(hitter.damage)
        pos = self.box.cx +r.randint(-10,10),self.box.fy
        g.pman.addLabPart(s,pos,color=c['lightred'],key='dmg',font_name=1,anchor=('center','center'),group='up-1',vis=True)

    def release_son(self,son,fans,day):
        super(Perso,self).release_son(son,fans,day)
        self.credhud.update()

    def auto_release(self):

        choiced_son = None
        for son in self.invhud.inventory['son']:
            if not son.item._released:
                choiced_son = son.item
                break
        if choiced_son != None:
            self.release_son(choiced_son,BOTS,g.Cyc.day)

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

    def add_money(self,qté):
        super(Perso,self).add_money(qté)
        if qté < 0:
            s= convert_huge_nb(qté)
        else:
            s='+' + convert_huge_nb(qté)
        pos = g.lman.labels[self.hud.labids['coin_lab']].x +r.randint(-2,2),g.lman.labels[self.hud.labids['coin_lab']].y+20
        g.pman.addLabPart(s,pos,color=c['yellow'],key='icons',font_name=1,anchor=('right','center'),group='up-1',vis=self.hud.visible)

    ## colli hoover

    def move(self,dir,street,run=False):
        super(Perso,self).move(dir,street,run)
        self.check_colli(street)

    def check_colli(self,street):

        collis = []

        for hum in street.humans:
            if collisionAB(self.realbox,hum.realbox) :
                collis.append(hum)

        for elem in street.zones:
            if collisionAB(self.realbox,street.zones[elem].realbox) :
                collis.append(street.zones[elem])

        for item in street.items:
            if collisionAB(self.realbox,item.realbox) :
                collis.append(item)

        if len(collis) > 0:
            collis.sort(key=lambda x:x.gey)
            #print(list(map(lambda x:x.name,collis)))

            y,yf = street.yyf
            d = yf-y
            yranges = [y]
            for i in range(len(collis)):
                yranges.append(y+(i+1)*(d/len(collis)))
            #print(yranges)

            k=0
            for i in range(len(collis)):
                if self.gey >= yranges[i] and self.gey <= yranges[i+1]:
                    k=i
            colli_elem = collis[k]

        else:
            colli_elem = None


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
