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

#graphic

class Human():

    def __init__(self,textids,pos=(400,200),name='John',group='perso-1',street='street1'):
        # general

        self.name = name
        self.speed = 12
        self.yspeed = 5
        self.play = 'play'

        #life
        self.life = 100
        self.max_life = 100
        self.damage = r.randint(10, 110)

        #pos
        self.gex = pos[0] # general x
        self.gey = pos[1] # general y
        self.street = street

        self.money = 1000

        self.element_colli = None

        # track of time
        self.time_last_move = 0

        self.doing = ['nothing']
        self.dir = r.choice(('R','L'))

        # skins
        self.textids = { ('nothing','R',0):textids[0] , ('nothing','R',1):textids[1] , ('nothing','L',0):textids[0+2] , ('nothing','L',1):textids[1+2]
                        , ('move','R',0):textids[2+2] , ('move','R',1):textids[3+2] , ('move','L',0):textids[4+2] , ('move','L',1):textids[5+2]
                        , ('hit','R',0):textids[6+2] , ('hit','R',1):textids[6+2] , ('hit','L',0):textids[7+2] , ('hit','L',1):textids[7+2]
                        , ('write','R',0):textids[10] , ('write','R',1):textids[11] , ('write','L',0):textids[12] , ('write','L',1):textids[13]
                        , ('wait','R',0):textids[0] , ('wait','R',1):textids[0] , ('wait','L',0):textids[0+2] , ('wait','L',1):textids[0+2]
                        , ('die','R',0):textids[14] , ('die','R',1):textids[14] , ('die','L',0):textids[14] , ('die','L',1):textids[14]
                         }
        self.grp = group
        #self.roll_skin = 0
        #self.skin_id = g.sman.addSpr(self.textids[(self.doing[0],self.dir,0)],pos,group=group)

        #self.update_skin()

        ##### HOOOOVER

        self._hoover = False
        self.color = c['coral']

    def update_skin(self,dt=0.4,repeat=True):


        g.sman.set_text(self.skin_id,self.textids[(self.doing[0],self.dir,self.roll_skin)])
        if self.roll_skin:
            self.roll_skin = 0
        else:
            self.roll_skin = 1

        if repeat:
            g.bertran.schedule_once(self.update_skin, 0.4)

    def add_money(self,qté):
        self.money += qté

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

    def move(self,dir,street):

        maxx=street.xxf
        maxy = 100,175
        if 'write' not in self.doing and 'wait' not in self.doing and 'die' not in self.doing:

            moved = False
            if dir == 'R' :
                if (maxx[1] == None or maxx[1] > self.gex+self.speed+g.sman.spr(self.skin_id).width ):
                    self.gex+=self.speed
                    moved = True

            elif dir == 'L' and (maxx[0] == None or maxx[0] < self.gex-self.speed ):
                self.gex-=self.speed
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

                self.time_last_move = time.time()

    def update_lab(self):
        if hasattr(self,'label'):
            # label
            pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 20
            g.lman.modify(self.label,pos)

    def be_hit(self,hitter):
        print(self.name,'hit by',hitter.name)
        g.sman.filter(self.skin_id)
        g.bertran.unschedule(self.un_hit)
        g.bertran.schedule_once(self.un_hit, 0.4)

        self.life -= hitter.damage
        if self.life <= 0:
            self.die()

        s=convert_huge_nb(hitter.damage)
        pos = self.box.cx +r.randint(-10,10),self.box.fy
        g.pman.addLabPart(s,pos,color=c['lightred'],key='icons',anchor=('center','center'),group='up-1',vis=True)

    def un_hit(self,dt):
        if hasattr(self,'skin_id'):
            g.sman.filter(self.skin_id,(255,255,255))

    def die(self):
        self.do('die')
        self.damage = 0
        self.speed = 0
        self.yspeed = 0

        g.bertran.schedule_once(self.delete,4)

    def delete(self,dt=0):

        #self.deload()
        o2.CITY[self.street].del_hum(self)


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
            self.skin_id = g.sman.addSpr(self.textids[(self.doing[0],self.dir,0)],(self.gex,self.gey),group=self.grp)

            self.update_skin()

        if not hasattr(self,'label'):
            pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 20
            self.label = g.lman.addLab(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20,group='mid')

        #print('loaded',self.name)

    def deload(self):
        g.bertran.unschedule(self.update_skin)

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
        return g.sman.box(self.skin_id)
    realbox = property(_realbox)

    def _alive(self):
        if self.life > 0:
            return True
        return False
    alive = property(_alive)

class Rappeur(Human):

    def __init__(self,textids,pos=(2000,175),name='Freeze Corleone',street='street1'):

        super(Rappeur,self).__init__(textids,pos,name,group='perso',street=street)

        self.cred_score = 0
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
            self.plume = self.plume.delete()

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

    ##

    def update_scores(self):

        sons = self.disco[-2:]
        qua_score = sum([ i.quality for i in sons])/len(sons)
        self.cred_score = max([ i.cred for i in sons])

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

class Perso(Rappeur):

    def __init__(self,textids,pos=(400,175),name='Delta',street='street1'):

        super(Perso,self).__init__(textids,pos,name,street=street)

        self.max_life = 800
        self.life = self.max_life
        self.speed = g.SPEED

        # hud
        self.hud = o.PersoHUD(self)
        self.lifehud = o.LifeHUD(self)
        self.plumhud = o.PlumHUD(self.plume)
        self.invhud = o.InventHUD(self)
        self.sonhud = o.SonHUD(self)

        self.load()

    # huds

    def rplum(self):
        if self.plume != None:
            self.plumhud.delete()
        super(Perso,self).rplum()
        self.plumhud = o.PlumHUD(self.plume)

    def drop_plume(self):
        if self.plume != None:
            self.plumhud.delete()
        super(Perso,self).drop_plume()

    def be_hit(self,hitter):
        print(self.name,'hit by',hitter.name)
        g.sman.filter(self.skin_id)
        g.bertran.unschedule(self.un_hit)
        g.bertran.schedule_once(self.un_hit, 0.4)

        self.life -= hitter.damage

        if self.life <= 0:
            self.life = 0
        self.lifehud.update()

        if self.life <= 0:
            self.die()

        s=convert_huge_nb(hitter.damage)
        pos = self.box.cx +r.randint(-10,10),self.box.fy
        g.pman.addLabPart(s,pos,color=c['lightred'],key='icons',anchor=('center','center'),group='up-1',vis=True)

    ## particles

    def addfan(self,fan):
        super(Perso,self).addfan(fan)
        s = '+1'
        pos = g.lman.labels[self.hud.labids['fan_lab']].x +r.randint(-2,2) ,g.lman.labels[self.hud.labids['fan_lab']].y+20
        g.pman.addLabPart(s,pos,color=c['lightgreen'],key='icons',anchor=('right','center'),group='up',vis=self.hud.visible)

    def addfans(self,fans):
        super(Perso,self).addfans(fans)
        s = '+'+str(len(fans))
        pos = g.lman.labels[self.hud.labids['fan_lab']].x +r.randint(-2,2) ,g.lman.labels[self.hud.labids['fan_lab']].y+20
        g.pman.addLabPart(s,pos,color=c['lightgreen'],key='icons',anchor=('right','center'),group='up',vis=self.hud.visible)

    def addstream(self):
        super(Perso,self).addstream()
        s = '+1'
        pos = g.lman.labels[self.hud.labids['stream_lab']].x +r.randint(-2,2) ,g.lman.labels[self.hud.labids['stream_lab']].y+20
        g.pman.addLabPart(s,pos,color=c['lightblue'],key='icons',anchor=('right','center'),group='up',vis=self.hud.visible)

    def add_money(self,qté):
        super(Perso,self).add_money(qté)
        if qté < 0:
            s= convert_huge_nb(qté)
        else:
            s='+' + convert_huge_nb(qté)
        pos = g.lman.labels[self.hud.labids['coin_lab']].x +r.randint(-2,2),g.lman.labels[self.hud.labids['coin_lab']].y+20
        g.pman.addLabPart(s,pos,color=c['yellow'],key='icons',anchor=('right','center'),group='up',vis=self.hud.visible)

    ## colli hoover

    def move(self,dir,street):
        super(Perso,self).move(dir,street)
        self.check_colli(street)

    def check_colli(self,street):

        colli_elem = None

        for hum in street.humans:
            if collisionAB(self.realbox,hum.realbox) :
                    colli_elem = hum

        for elem in street.zones:
            if collisionAB(self.realbox,street.zones[elem].realbox) :
                    colli_elem = street.zones[elem]

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
