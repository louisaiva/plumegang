
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
CRED = ['----','---','--'
        ,'-','/','*'
        ,'**','***','****']
CRED_coeff = [-95,-80,-50,-10,10,50,80,95,101]

with open('src/mots.json','r', encoding="utf-8") as f:
    MOTS = json.load(f)

THEMES = ['amour','argent','liberté','révolte','egotrip','ovni','famille','tristesse','notoriété','chill','rap']

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

        self.nb_fans = 0
        #self.fans = []

        self.plume = rplum(self.name)

        self.element_colli = None

        # track of time
        self.time_last_move = 0

        self.doing = ['nothing']
        self.dir = 'R'

        # skins
        self.textids = { ('nothing','R',0):textids[0] , ('nothing','R',1):textids[1] , ('nothing','L',0):textids[0+2] , ('nothing','L',1):textids[1+2]
                        , ('move','R',0):textids[2+2] , ('move','R',1):textids[3+2] , ('move','L',0):textids[4+2] , ('move','L',1):textids[5+2]
                        , ('hit','R',0):textids[6+2] , ('hit','R',1):textids[6+2] , ('hit','L',0):textids[7+2] , ('hit','L',1):textids[7+2]
                        , ('write','R',0):textids[4] , ('write','R',1):textids[5] , ('write','L',0):textids[6] , ('write','L',1):textids[7]
                        , ('wait','R',0):textids[0] , ('wait','R',1):textids[0] , ('wait','L',0):textids[0+2] , ('wait','L',1):textids[0+2]
                         }
        self.roll_skin = 0
        self.skin_id = g.sman.addSpr(self.textids[(self.doing[0],self.dir,0)],pos,'perso')

        # hud
        self.hud = PersoHUD(self)
        self.invhud = InventHUD(self)

        self.update_skin()

    def rplum(self):
        if self.plume != None:
            self.plume.delete()
        self.plume = rplum(self.name)

    def update_skin(self,dt=0.4,repeat=True):

        g.sman.set_text(self.skin_id,self.textids[(self.doing[0],self.dir,self.roll_skin)])
        if self.roll_skin:
            self.roll_skin = 0
        else:
            self.roll_skin = 1

        if repeat :
            pyglet.clock.schedule_once(self.update_skin, 0.4)

    def move(self,dir):

        if 'write' not in self.doing and 'wait' not in self.doing:

            moved = False
            if dir == 'R':
                self.gex+=self.speed

                moved = True
            elif dir == 'L':
                self.gex-=self.speed

                moved = True

            if moved :

                if self.dir != dir:
                    self.dir = dir
                    self.do('move')
                    self.update_skin(repeat=False)
                else:
                    self.do('move')
                self.check_colli()

                self.time_last_move = time.time()

    def check_colli(self):

        colli_elem = None
        for elem in ZONES['ELEM']:
            if collisionAB(self.realbox,ZONES['ELEM'][elem].realbox) :
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

    def drop_plume(self):
        if self.plume != None:
            self.plume = self.plume.delete()

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
                pyglet.clock.schedule_once(self.undo,0.1,'hit')

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

    def undo(self,dt=0,action='nothing'):

        if action in self.doing:
            self.doing.remove(action)
            if self.doing == []:
                self.do()

    def check_do(self):

        if 'hit' not in self.doing and 'write' not in self.doing and 'wait' not in self.doing:
            if time.time()-self.time_last_move > 0.2:
                self.do()


    ##

    def _realbox(self):
        return g.sman.box(self.skin_id)

    realbox = property(_realbox)


class Plume():

    def __init__(self,owner,qua,cred):

        self.quality = qua
        self.cred_power = cred
        self.owner = owner

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

            nb = r.randint(3,4)
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

    def __init__(self,box,textid='white',group='mid',makeCol=True):

        if makeCol:
            if textid[:4] == 'text':
                self.text_id = textid
            else:
                self.text_id = g.tman.addCol(*box.wh,c[textid])
            self.skin_id = g.sman.addSpr(self.text_id,box.xy,group)

        self.gex,self.gey = box.xy

        self._hoover = False

    def _realbox(self):
        return g.sman.box(self.skin_id)

    realbox = property(_realbox)

#------# elements

class Zone_ELEM(Zone):

    ## HOOVER WITH MOVEMENT OF PERSO

    def __init__(self,box,name='thing',textid='white',group='mid',long=False):
        super(Zone_ELEM,self).__init__(box,textid,group)

        self.name = name
        self.longpress = long

        self.box = box

        # label
        pos = box.x + box.w/2 , box.y + box.h + 20
        self.label = g.lman.addLab(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20,group='mid')

        self.color = c['coral']

        self.activated = False

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
        pos = (self.realbox[0] + self.realbox[2])/2 , self.realbox[3] + 20
        g.lman.modify(self.label,pos)

class Market(Zone_ELEM):

    def __init__(self,x,y):
        super(Market,self).__init__(box(x,y,200,200),'market','pink','mid',long=True)

    def activate(self,perso):
        super(Market,self).activate(perso)
        perso.rplum()

#------# active elements

class Zone_ACTIV(Zone_ELEM):

    def __init__(self,box,name='thing',textid='white',group='mid',long=False):
        super(Zone_ACTIV,self).__init__(box,name,textid,group,long)

    def activate(self,perso):
        super(Zone_ACTIV,self).activate(perso)
        self.activated = True

    def close(self,perso):
        self.activated = False
        perso.do()

class Ordi(Zone_ELEM):

    def __init__(self,x,y):
        super(Ordi,self).__init__(box(x,y,150,200),'ordi','red','mid')

    def activate(self,perso):
        super(Ordi,self).activate(perso)
        perso.add_money(10000)

class Studio(Zone_ELEM):

    def __init__(self,x,y):
        super(Studio,self).__init__(box(x,y,50,200),'studio','blue','mid')

class Lit(Zone_ACTIV):

    def __init__(self,x,y):
        super(Lit,self).__init__(box(x,y,300,150),'lit','darkgreen','mid',long=True)

        self.hud = WriteHUD()

    def activate(self,perso):
        super(Lit,self).activate(perso)
        g.lman.modify(self.hud.labids['lit'],color=self.color)

        if self.hud.visible:
            perso.do('write')
            perso.undo(0,'wait')
            self.write(perso)
        else:
            perso.do('wait')
            self.hud.unhide()

    def deactivate(self,dt):
        super(Lit,self).deactivate(0)
        if self.activated:
            g.lman.modify(self.hud.labids['lit'],color=c['white'])
        else:
            g.lman.modify(self.hud.labids['lit'],color=(255,255,255,0))

    def close(self,perso):
        super(Lit,self).close(perso)
        self.hud.delete_phase()
        self.hud.unhide(True)
        perso.invhud.unhide(True) 

    def write(self,perso):

        if perso.plume != None:
            phase = perso.plume.drop_phase()
            #aff_phase(phase)
            self.hud.write(phase)

#------# ui

class Zone_UI(Zone):

    ## HOOVER WITH MOVEMENT OF MOUSE

    def __init__(self,box2,name='UIthg',textid='white',group='ui',makeCol=False,longpress=False):
        super(Zone_UI,self).__init__(box2,textid,group,makeCol)

        self.name = name
        self.box = box2

        self.longpress = longpress
        self.visible = True
        self._hoover = False

        # label
        pos = self.box.x + self.box.w/2 , self.box.y + self.box.h + 20
        self.label = g.lman.addLab(self.name,pos,vis=False,anchor = ('center','bottom'),font_size=20,color=c['coral'],group=group)
        boxbg = box( self.box.x + self.box.w/2 - g.lman.labels[self.label].content_width/2 - 5, self.box.y + self.box.h + 15, g.lman.labels[self.label].content_width+10 , g.lman.labels[self.label].content_height+10 )
        self.label_bg = g.sman.addCol((120,120,120,int(0.75*255)),boxbg,group=group+'-1',vis=False)

    def hoover(self):
        g.lman.unhide(self.label)
        g.sman.unhide(self.label_bg)
        self._hoover = True

    def unhoover(self):
        g.lman.unhide(self.label,True)
        g.sman.unhide(self.label_bg,True)
        self._hoover = False

    def activate(self):
        #print(self.name,'activated')
        pass

    def delete(self):

        if hasattr(self,'skin_id'):
            g.sman.delete(self.skin_id)

        g.sman.delete(self.label_bg)
        g.lman.delete(self.label)

    ##

    def check_mouse(self,x,y):

        if collisionAX(self.box.realbox,(x,y)):
            self.hoover()
            return True
        else:
            self.unhoover()
            return False

    def check_pressed(self):

        if self._hoover:
            self.activate()

class Plume_UI(Zone_UI):

    def __init__(self,box,plume):

        name = plume.owner+'\'s plume '#+convert_quality(plume.quality)

        super(Plume_UI,self).__init__(box,name,group='ui',makeCol=False)

        #self.plume = phase

    def update(self):
        pass

class Item_UI(Zone_UI):

    def __init__(self,box,name,texture):

        super(Item_UI,self).__init__(box,name,group='ui',makeCol=False)

        #self.text_id = texture
        self.itemspr = g.sman.addSpr(texture,group='ui',vis=False)
        g.sman.modify(self.itemspr,scale=(0.5,0.5))

        pos = box.cx - g.sman.spr(self.itemspr).width/2 , box.cy - g.sman.spr(self.itemspr).height/2
        g.sman.modify(self.itemspr,pos)

        self.caught = False

    def catch(self):
        self.caught = True
        g.sman.unhide(self.itemspr)
        self.box = box(self.box.cx - g.sman.spr(self.itemspr).width/2,self.box.cy - g.sman.spr(self.itemspr).height/2,g.sman.spr(self.itemspr).width,g.sman.spr(self.itemspr).height)

        pos = self.box.cx , self.box.fy + 20
        g.lman.modify(self.label,pos)
        pos = self.box.cx - g.lman.labels[self.label].content_width/2 - 5, self.box.fy + 15
        g.sman.modify(self.label_bg,pos)

    def drop(self):
        self.caught = False
        g.sman.unhide(self.itemspr,True)

    def move(self,x,y):
        self.box.xy = x-g.sman.spr(self.itemspr).width/2,y-g.sman.spr(self.itemspr).width/2
        self.update()

    def update(self):

        if self.caught:

            # itemspr
            g.sman.unhide(self.itemspr)
            pos = self.box.cx - g.sman.spr(self.itemspr).width/2 , self.box.cy - g.sman.spr(self.itemspr).height/2
            g.sman.modify(self.itemspr,pos)

            # label
            pos = self.box.cx , self.box.fy + 20
            g.lman.modify(self.label,pos)
            # labelbg
            pos = self.box.cx - g.lman.labels[self.label].content_width/2 - 5, self.box.fy + 15
            g.sman.modify(self.label_bg,pos)

    def delete(self):
        super(Item_UI,self).delete()
        g.sman.delete(self.itemspr)

    def activate(self):
        super(Item_UI,self).activate()
        if self.caught:
            self.drop()
        else:
            self.catch()

class Phase_UI(Item_UI):

    def __init__(self,box,phase):

        name = 'Phase '+convert_quality(phase.quality)

        super(Phase_UI,self).__init__(box,name,g.TEXTIDS['phase'][convert_quality(phase.quality)[0]])

        self.phase = phase

ZONES = {}
#ZONES['UI'] = {} # use ZONES['UI'] for ui
#ZONES['Item'] = {} # use ZONES['UI'] for item ui
ZONES['ELEM'] = {} # use ZONES['ELEM'] for in-game graph element


#------# hud

class HUD():

    def __init__(self,group='hud1',name='main',vis=True):

        self.name = name
        self.group = group

        #---#

        self.sprids = {}
        self.labids = {}

        #---#

        self.visible = vis

    def addSpr(self,key,textid,xy_pos=(0,0),group=None):

        if key in self.sprids:
            g.sman.delete(self.sprids[key])

        if group == None:
            group = self.group

        self.sprids[key] = g.sman.addSpr(textid,xy_pos,group,vis=self.visible)

    def addCol(self,key,box,color=c['delta_purple'],group=None):

        if group == None:
            group = self.group

        if type(color) == type(()):
            textid = g.tman.addCol(*box.wh,color)
        else:
            textid = g.tman.addCol(*box.wh,c[color])
        self.addSpr(key,textid,box.xy,group=group)

    def addLab(self,key,contenu,xy_pos=(0,0),group=None,font_size=30,anchor=('left','bottom'),color=(255,255,255,255)):

        if key in self.labids:
            g.lman.delete(self.labids[key])

        if group == None:
            group = self.group

        self.labids[key] = g.lman.addLab(str(contenu),xy_pos,group=group,font_size=font_size,anchor=anchor,color=color,vis=self.visible)

        #print(xy_pos)

    def modifySpr(self,key,pos=None,scale=None):
        g.sman.modify(self.sprids[key],pos,scale)

    def unhide(self,hide=False):

        g.sman.unhide(self.sprids,hide)
        g.lman.unhide(self.labids,hide)
        self.visible = not hide

    def rollhide(self):
        self.unhide(self.visible)

    def delete(self):
        g.lman.delete(self.labids)
        g.sman.delete(self.sprids)

    ## oeoe

    def spr(self,key):
        return g.sman.spr(self.sprids[key])

    def lab(self,key):
        return g.lman.labels[self.labids[key]]

class InventHUD(HUD):

    def __init__(self,perso):

        super(InventHUD, self).__init__(group='hud1',name='inv',vis=False)

        self.perso = perso

        self.inventory = {}
        self.inventory['phase'] = []
        self.inventory['instru'] = []
        self.inventory['son'] = []

        self.box = box(20,200,320,800)
        self.padding = 64
        self.padding2 = 20
        self.lilpadding = 12

        self.addCol('bg',self.box,group='hud-1')

        self.box2 = box(self.box.x+self.padding2,self.box.y+self.padding2,self.box.w-2*self.padding2,self.box.h-self.padding2-100)

        self.addCol('bg2',self.box2,color=c['delta_blue'],group='hud')

        print(self.box2.wh)

        ## inv
        self.addLab('inv_lab','inventory',(self.box.cx,self.box.fy-50),anchor=('center','center'))

    def catch(self,item):

        if type(item) == Phase:
            self.inventory['phase'].append(item)
        elif type(item) == Instru:
            self.inventory['instru'].append(item)
        elif type(item) == Son:
            self.inventory['son'].append(item)

        print(self.inventory)

class PersoHUD(HUD):

    def __init__(self,perso):

        super(PersoHUD, self).__init__(group='hud1',name='perso')

        self.perso = perso

        self.box = box(1700,460+150,200,400)
        self.padding = 64

        self.addCol('bg',self.box,group='hud-1')

        ## name
        self.addLab('name',self.perso.name,(self.box.cx,self.box.y+self.box.h-50),anchor=('center','center'))

        ## coin

        xcoin = self.box.cx
        ycoin = self.lab('name').y  - self.padding

        self.addSpr('coin_spr',g.TEXTIDS['item'][0],(xcoin,ycoin - g.tman.textures[g.TEXTIDS['item'][0]].height/2))
        self.addLab('coin_lab',convert_huge_nb(self.perso.money),(xcoin ,ycoin),font_size=20,color=c['yellow'],anchor=('right','center'))

        ## fans

        xfan = self.box.cx
        yfan = self.lab('coin_lab').y - self.padding

        self.addSpr('fan_spr',g.TEXTIDS['item'][1],(xfan,yfan - g.tman.textures[g.TEXTIDS['item'][1]].height/2))
        self.addLab('fan_lab',convert_huge_nb(self.perso.nb_fans),(xfan ,yfan),font_size=20,color=c['green'],anchor=('right','center'))


        ## pressX
        self.addLab('pressX','X to hide',(self.box.cx,self.box.y+20),font_size=10,color=c['black'],anchor=('center','center'))

    def update(self):

        g.lman.set_text(self.labids['coin_lab'],convert_huge_nb(self.perso.money))
        g.lman.set_text(self.labids['fan_lab'],convert_huge_nb(self.perso.nb_fans))

class PlumHUD(HUD):

    def __init__(self,plum):

        super(PlumHUD, self).__init__(group='hud1',name='plum')

        self.plum = plum


        self.box = box(1650,20,250,150)
        self.padding = 50

        self.addCol('bg',self.box,group='hud-1')

        self.addLab('quality',convert_quality(self.plum.quality),(self.box.x+self.box.w-self.padding,self.box.cy),anchor=('center','center'))

        self.addSpr('plum_spr',g.TEXTIDS['plume'][convert_quality(self.plum.quality)[0]])
        g.sman.modify(self.sprids['plum_spr'],scale=(0.4,0.4))

        xplum = self.lab('quality').x - self.padding - self.spr('plum_spr').width/2
        yplum = self.box.cy - self.spr('plum_spr').height/2

        g.sman.modify(self.sprids['plum_spr'],pos=(xplum,yplum))


        x = (xplum +  (self.box.x) )/2

        self.addLab('cred',convert_streetcred(self.plum.cred_power),(x ,self.box.cy),font_size=20,anchor=('center','center'))


        ### UI
        self.ui = Plume_UI(box(xplum,yplum,self.spr('plum_spr').width,self.spr('plum_spr').height),plum)

    def delete(self):
        super(PlumHUD,self).delete()
        self.ui.delete()

class WriteHUD(HUD):

    def __init__(self):

        super(WriteHUD, self).__init__(group='hud1',name='write',vis=False)

        ##

        self.ui = None

        self.box = box(400,300,1000,600)
        self.padding = 50

        self.addCol('bg',self.box,group='hud-1')

        self.box2 = box(self.box.x+self.padding,self.box.y+2*self.padding,self.box.w-2*self.padding,self.box.h-3*self.padding)

        self.addCol('bg2',self.box2,color=c['delta_blue'],group='hud')

        #self.addLab('quality',convert_quality(self.plum.quality),(self.box.x+self.box.w-self.padding,self.box.cy),anchor=('center','center'))
        self.addLab('pressE','E to write --- ESC to leave',(self.box.cx,self.box.y+self.padding),font_size=20,anchor=('center','center'))
        self.addLab('lit','LIT - zone d\'ecriture',(self.box.cx,self.box.y+self.box.h+self.padding),font_size=20,anchor=('center','center'))

    def delete_phase(self,ui=True):

        if 'phaz_spr' in self.sprids:
            g.sman.delete(self.sprids['phaz_spr'])
            del self.sprids['phaz_spr']

        if 'phaz_content' in self.labids:
            g.lman.delete(self.labids['phaz_content'])
            del self.labids['phaz_content']

        if 'phaz_qua' in self.labids:
            g.lman.delete(self.labids['phaz_qua'])
            del self.labids['phaz_qua']

        if 'phaz_cred' in self.labids:
            g.lman.delete(self.labids['phaz_cred'])
            del self.labids['phaz_cred']

        if 'phaz_them' in self.labids:
            g.lman.delete(self.labids['phaz_them'])
            del self.labids['phaz_them']

        if self.ui != None and ui:
            self.ui.delete()
            self.ui = None

    def write(self,phase):

        text = g.TEXTIDS['phase'][convert_quality(phase.quality)[0]]

        self.addSpr('phaz_spr',text)
        #g.sman.modify(self.sprids['phaz_spr'],scale=(0.8,0.8))
        g.sman.modify(self.sprids['phaz_spr'],pos=(self.box2.cx - self.spr('phaz_spr').width/2,self.box2.cy - self.spr('phaz_spr').height/2))

        y = (( self.box2.cy + self.spr('phaz_spr').height/2 )  +  (self.box2.y + self.box2.h) )/2
        self.addLab('phaz_content',phase.content,(self.box2.cx,y),anchor=('center','center'),color=c['black'])

        x = (self.box2.cx + self.spr('phaz_spr').width/2  +  (self.box2.x + self.box2.w) )/2
        self.addLab('phaz_qua',convert_quality(phase.quality),(x,self.box2.cy),anchor=('center','center'),color=c['black'],font_size=100)

        x = (self.box2.cx - self.spr('phaz_spr').width/2  +  (self.box2.x) )/2
        self.addLab('phaz_cred',convert_streetcred(phase.cred),(x,self.box2.cy),anchor=('center','center'),color=c['black'],font_size=100)

        #y = (( self.box2.cy - self.spr('phaz_spr').height/2 )  +  (self.box2.y) )/2
        y = ( self.box2.cy - self.spr('phaz_spr').height/2 ) - 30
        self.addLab('phaz_them','thème : '+phase.them,(self.box2.cx,y),anchor=('center','center'),font_size=20)

        x,y,w,h = self.box2.cx - self.spr('phaz_spr').width/2 , self.box2.cy - self.spr('phaz_spr').height/2 , self.spr('phaz_spr').width , self.spr('phaz_spr').height

        if self.ui != None:
            self.ui.delete()
        self.ui = Phase_UI(box(x,y,w,h),phase)

    def catch_phase(self,x,y,perso):

        self.ui.check_pressed()
        if self.ui.caught:
            perso.invhud.unhide()
            self.delete_phase(False)
        elif collisionAX(self.box.realbox,(x,y)):
            self.write(self.ui.phase)
        elif perso.invhud.visible and collisionAX(perso.invhud.box.realbox,(x,y)):
            perso.invhud.catch(self.ui.phase)
            self.delete_phase()
        else:
            self.delete_phase()



"""""""""""""""""""""""""""""""""""
 USEFUL FUNCTIONS
"""""""""""""""""""""""""""""""""""

def test():

    quality = r.random()
    cred_power = r.randint(-100,100)

    print(convert_quality(quality),convert_streetcred(cred_power))

    plum = Plume('delta',quality,cred_power)
    print('\n')
    for i in range(20):
        phaz = []
        for i in range(4):
            phaz.append(plum.drop_phase())
        btmker = Btmaker(r.random())
        Son(btmker.drop_instru(),phaz)

    #return Plume(quality,cred_power)

def rplum(owner):

    quality = r.random()
    cred_power = r.randint(-100,100)

    #print(convert_quality(quality),convert_streetcred(cred_power))

    return Plume(owner,quality,cred_power)

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

def aff_phase(phase):

    print(phase.str())
