"""
CODED by deltasfer
enjoy
"""

import random as r
import json,time,pyglet
from src.colors import *
from colors import red, green, blue
from src.utils import *
from src import graphic as g
from src import names as n
from src import obj2 as o2
from src import obj3 as o3
from src import perso as p
from collections import OrderedDict
from src import cmd

"""THIS OBJ FILE IS ABOUT HUD && UIs"""



"""'''''''''''''''''''''''''''''''''
'''''''HUD  ''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''"""

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

    def addSpr(self,key,textid,xy_pos=(0,0),group=None,wh=None,anchor=None):

        if key in self.sprids:
            g.sman.delete(self.sprids[key])

        if group == None:
            group = self.group

        self.sprids[key] = g.sman.addSpr(textid,xy_pos,group,vis=self.visible,wh=wh,anchor=anchor,key='hud_'+self.name)

        #if wh and (g.sman.spr(self.sprids[key]).width != wh[0] or g.sman.spr(self.sprids[key]).height != wh[1]):
        #    g.sman.modify(self.sprids[key],size=wh)

    def addCol(self,key,box,color='delta_purple',group=None):

        if key in self.sprids:
            g.sman.delete(self.sprids[key])

        if group == None:
            group = self.group

        self.sprids[key] = g.sman.addCol(color,box,group,vis=self.visible)

    def addLab(self,key,contenu,xy_pos=(0,0),group=None,font_name=0,font_size=30,anchor=('left','bottom'),color=(255,255,255,255),replace=True):

        if replace:
            if key in self.labids:
                g.lman.delete(self.labids[key])

            if group == None:
                group = self.group

            self.labids[key] = g.lman.addLab(str(contenu),xy_pos,group=group,font_name=font_name,font_size=font_size,anchor=anchor,color=color,vis=self.visible)

        elif key not in self.labids:
            if group == None:
                group = self.group

            self.labids[key] = g.lman.addLab(str(contenu),xy_pos,group=group,font_name=font_name,font_size=font_size,anchor=anchor,color=color,vis=self.visible)

    def delLab(self,key):
        if key in self.labids:
            g.lman.delete(self.labids[key])
            self.labids.pop(key)

    def delSpr(self,key):
        if key in self.sprids:
            g.sman.delete(self.sprids[key])
            self.sprids.pop(key)

    def modifySpr(self,key,pos=None,scale=None):
        g.sman.modify(self.sprids[key],pos,scale)

    def modifyLab(self,key,pos=None,col=None):
        g.lman.modify(self.labids[key],pos,color=col)

    def set_text(self,key,text,wh=None):
        if key in self.labids:
            g.lman.set_text(self.labids[key],text)
        elif key in self.sprids:
            g.sman.set_text(self.sprids[key],text)
            if wh and (g.sman.spr(self.sprids[key]).width != wh[0] or g.sman.spr(self.sprids[key]).height != wh[1]):
                g.sman.modify(self.sprids[key],size=wh)

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

class Map(HUD):

    def __init__(self,perso):

        #w_map = 100000

        super(Map, self).__init__(group='hud2',name='map',vis=False)

        self.perso = perso

        scrw,scrh=g.scr.size
        area = box(scrw//2-2*scrh//6,scrh//6,2*scrh//3,2*scrh//3)

        self.pad = 25
        self.box = box(area.x+self.pad,area.y+self.pad,area.w-2*self.pad,area.h-2*self.pad)

        self.larg_cube = 18
        self.larg_street = 6
        self.larg_house = 12
        #w = self.larg_cube*3*w_map
        #self.box = box(scrw/2-w/2,scrh/2-w/2,w,w)

        self.ax,self.ay = self.box.cxy

        self.addCol('bg',area,group='hud2-1',color='delta_blue_faded')
        self.addCol('bg2',area,group='hud2-1',color='delta_blue_faded')

        ## name
        self.addLab('name','MAP OF NY CITY',(area.cx,area.fy-self.pad),font_name=1,anchor=('center','center'),group='hud2')

    def load(self):
        self.create_map()

    def deload(self):
        for street in o2.NY.CITY:
            self.delSpr(o2.NY.CITY[street].name)

    def unhide(self,hide=False):
        super(Map,self).unhide(hide)
        if hide:
            self.deload()
        else:
            self.load()

    def create_map(self):

        for street in o2.NY.CITY:
            #print(street.name)
            street = o2.NY.CITY[street]

            if type(street) == o2.Street:

                vert = street.pre.vert

                if not vert:
                    x = self.ax + street.pre.x*self.larg_cube
                    y = self.ay + self.larg_cube/2 -self.larg_street/2 + street.pre.y*self.larg_cube
                else:
                    x = self.ax + self.larg_cube/2 -self.larg_street/2 + street.pre.x*self.larg_cube
                    y = self.ay + street.pre.y*self.larg_cube

                if vert:
                    w,h=self.larg_street,street.pre.w*self.larg_cube
                else:
                    h,w=self.larg_street,street.pre.w*self.larg_cube

                self.addCol(street.name,box(x,y,w,h),color='delta_purple',group='hud2')

                if street.has_station:
                    i = street.build_list.index('sbahn')
                    w,h=self.larg_house,self.larg_house
                    if not vert:
                        x = self.ax + (street.pre.x+i)*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                        y = self.ay + street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    else:
                        x = self.ax + street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                        y = self.ay + (street.pre.y+i)*self.larg_cube + self.larg_cube/2 -self.larg_house/2

                    self.addCol(street.name+' station',box(x,y,w,h),color='green',group='hud21')

            elif street.name == 'home':
                w,h=self.larg_house,self.larg_house

                x = self.ax + street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                y = self.ay + street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                self.addCol(street.name,box(x,y,w,h),color='red',group='hud21')

            elif isinstance(street,o2.Shop) or isinstance(street,o2.SpecialHouse):
                w,h=self.larg_house,self.larg_house

                x = self.ax + street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                y = self.ay + street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                self.addCol(street.name,box(x,y,w,h),color='blue',group='hud21')

    def update(self):

        if self.visible :
            perso_street = o2.NY.CITY[self.perso.street]

            # get pos
            if type(perso_street) == o2.Street: # si le perso se trouve dans une rue

                perc = perso_street.get_pos(self.perso)

                vert = perso_street.pre.vert
                if vert:
                    px = g.sman.spr(self.sprids[perso_street.name]).x - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                    py = g.sman.spr(self.sprids[perso_street.name]).y + perc*g.sman.spr(self.sprids[perso_street.name]).height
                else:
                    py = g.sman.spr(self.sprids[perso_street.name]).y - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                    px = g.sman.spr(self.sprids[perso_street.name]).x + perc*g.sman.spr(self.sprids[perso_street.name]).width
            else: #perso_street.name == 'home': # si le perso se trouve dans une maison
                px = self.ax + perso_street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                py = self.ay + perso_street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                px += self.larg_cube/2
                py += self.larg_cube/2


            # update anchor
            self.ax += self.box.cx-px
            self.ay += self.box.cy-py

            # update all streets
            for street in o2.NY.CITY:
                street = o2.NY.CITY[street]

                if type(street) == o2.Street:

                    vert = street.pre.vert

                    if not vert:
                        x = self.ax + street.pre.x*self.larg_cube
                        y = self.ay + self.larg_cube/2 -self.larg_street/2 + street.pre.y*self.larg_cube
                    else:
                        x = self.ax + self.larg_cube/2 -self.larg_street/2 + street.pre.x*self.larg_cube
                        y = self.ay + street.pre.y*self.larg_cube

                    g.sman.modify(self.sprids[street.name],(x,y))

                    if street.has_station:
                        i = street.build_list.index('sbahn')
                        if not vert:
                            x = self.ax + (street.pre.x+i)*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                            y = self.ay + street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                        else:
                            x = self.ax + street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                            y = self.ay + (street.pre.y+i)*self.larg_cube + self.larg_cube/2 -self.larg_house/2

                        g.sman.modify(self.sprids[street.name+' station'],(x,y))

                elif street.name == 'home':
                    x = self.ax + street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    y = self.ay + street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    g.sman.modify(self.sprids[street.name],(x,y))

                elif isinstance(street,o2.Shop) or isinstance(street,o2.SpecialHouse):
                    x = self.ax + street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    y = self.ay + street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    g.sman.modify(self.sprids[street.name],(x,y))

            # update all guys
            for guy in p.GUYS:

                guy_street = o2.NY.CITY[guy.street]

                # get pos
                if type(guy_street) == o2.Street: # si le perso se trouve dans une rue

                    perc = guy_street.get_pos(guy)

                    vert = guy_street.pre.vert
                    if vert:
                        px = g.sman.spr(self.sprids[guy_street.name]).x - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                        py = g.sman.spr(self.sprids[guy_street.name]).y + perc*g.sman.spr(self.sprids[guy_street.name]).height
                    else:
                        py = g.sman.spr(self.sprids[guy_street.name]).y - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                        px = g.sman.spr(self.sprids[guy_street.name]).x + perc*g.sman.spr(self.sprids[guy_street.name]).width
                else: #guy_street.name == 'home': # si le perso se trouve dans une maison
                    px = self.ax + guy_street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    py = self.ay + guy_street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                    px += self.larg_cube/2
                    py += self.larg_cube/2

                if not 'perso_'+guy.name in self.sprids:
                    self.addSpr('perso_'+guy.name,guy.textids['nothing']['R'][0],(px,py), group='hud22')
                    scale = self.pad/g.sman.spr(self.sprids['perso_'+guy.name]).width
                    g.sman.modify(self.sprids['perso_'+guy.name],scale=(scale,scale),anchor='center')
                else:
                    g.sman.modify(self.sprids['perso_'+guy.name],pos=(px,py),anchor='center')

            # get pos
            if type(perso_street) == o2.Street: # si le perso se trouve dans une rue

                perc = perso_street.get_pos(self.perso)

                vert = perso_street.pre.vert
                if vert:
                    px = g.sman.spr(self.sprids[perso_street.name]).x - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                    py = g.sman.spr(self.sprids[perso_street.name]).y + perc*g.sman.spr(self.sprids[perso_street.name]).height
                else:
                    py = g.sman.spr(self.sprids[perso_street.name]).y - self.larg_cube/2 +self.larg_street/2 + self.larg_cube/2
                    px = g.sman.spr(self.sprids[perso_street.name]).x + perc*g.sman.spr(self.sprids[perso_street.name]).width
            else: #perso_street.name == 'home': # si le perso se trouve dans une maison
                px = self.ax + perso_street.pre.x*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                py = self.ay + perso_street.pre.y*self.larg_cube + self.larg_cube/2 -self.larg_house/2
                px += self.larg_cube/2
                py += self.larg_cube/2

            # create and or change pos
            if not 'perso_spr' in self.sprids:
                self.addSpr('perso_spr',self.perso.textids['nothing']['R'][0],(px,py), group='hud22')
                scale = self.pad/g.sman.spr(self.sprids['perso_spr']).width
                g.sman.modify(self.sprids['perso_spr'],scale=(scale,scale),anchor='center')
            else:
                g.sman.modify(self.sprids['perso_spr'],pos=(px,py),anchor='center')

class PersoHUD(HUD):

    def __init__(self,perso):

        super(PersoHUD, self).__init__(group='ui',name='perso')

        self.perso = perso

        self.box = box(1700,460+150,200,400)
        self.padding = 64

        #self.addCol('bg',self.box,group='ui-1')
        self.texts = {'fight':g.tman.addCol('red_fight'),'peace':g.tman.addCol('delta_purple'),'sneak':g.tman.addCol('black_faded')}
        self.addSpr('bg',self.texts[perso.MODE],self.box.xy,group='ui-1',wh=self.box.wh)
        #g.sman.modify(self.sprids['bg'],size=self.box.wh)
        self.MODE = perso.MODE

        ## name
        self.addLab('name',self.perso.name,(self.box.cx,self.box.y+self.box.h-50),anchor=('center','center'))

        ## coin

        xcoin = self.box.cx
        ycoin = self.lab('name').y  - self.padding

        self.addSpr('coin_spr',g.TEXTIDS['ux'][0],(xcoin,ycoin),wh=(64,64),anchor=('left','center'))
        self.addLab('coin_lab',convert_huge_nb(self.perso.money),(xcoin ,ycoin),font_name=1,font_size=20,color=c['yellow'],anchor=('right','center'))

        ## fans

        xfan = self.box.cx
        yfan = self.lab('coin_lab').y - self.padding

        self.addSpr('fan_spr',g.TEXTIDS['ux'][1],(xfan,yfan),wh=(64,64),anchor=('left','center'))
        self.addLab('fan_lab',convert_huge_nb(self.perso.nb_fans),(xfan ,yfan),font_name=1,font_size=20,color=c['lightgreen'],anchor=('right','center'))

        ## fans

        xstream = self.box.cx
        ystream = self.lab('fan_lab').y - self.padding

        self.addSpr('stream_spr',g.TEXTIDS['ux'][2],(xstream,ystream),wh=(64,64),anchor=('left','center'))
        self.addLab('stream_lab',convert_huge_nb(self.perso.nb_streams),(xstream ,ystream),font_name=1,font_size=20,color=c['lightblue'],anchor=('right','center'))


        ## pressX
        self.addLab('pressX','X to hide',(self.box.cx,self.box.y+20),font_name=1,font_size=10,color=c['black'],anchor=('center','center'))

    def update(self):

        if self.MODE != self.perso.MODE:
            self.set_text('bg',self.texts[self.perso.MODE],wh=self.box.wh)
            # resize si jamais la taille est différente de celle de la box
            #g.sman.modify(self.sprids['bg'],size=self.box.wh)
            self.MODE = self.perso.MODE

        g.lman.set_text(self.labids['coin_lab'],convert_huge_nb(self.perso.money))
        g.lman.set_text(self.labids['fan_lab'],convert_huge_nb(self.perso.nb_fans))
        g.lman.set_text(self.labids['stream_lab'],convert_huge_nb(self.perso.nb_streams))

    def unhide(self,hide=False):

        g.sman.unhide(self.sprids,hide)
        g.lman.unhide(self.labids,hide)
        g.pman.unhide('icons',hide)
        self.visible = not hide

class LifeHUD(HUD):

    def __init__(self,perso):

        super(LifeHUD, self).__init__(group='hud2',name='life')
        #print(self.group)

        self.perso = perso

        #self.box = box(1700,460+150,200,400)
        self.anc = (20,20)

        size_lifebar = 400
        size_fill = (self.perso.life*size_lifebar)/self.perso.max_life


        self.addSpr('l',g.TEXTIDS['utils'][4],self.anc,group='hud2')
        self.addSpr('r',g.TEXTIDS['utils'][4],(self.anc[0]+size_lifebar,self.anc[1]),group='hud2')
        self.addSpr('mid',g.TEXTIDS['utils'][3],self.anc,group='hud2')
        g.sman.modify(self.sprids['mid'],scale=(size_lifebar/32,1))

        self.addSpr('fill',g.TEXTIDS['utils'][5],self.anc,group='hud2-1')
        g.sman.modify(self.sprids['fill'],scale=(size_fill/32,1))

        ### UI
        self.ui = Life_UI(box(*self.anc,self.spr('fill').width,self.spr('fill').height),self.perso)

    def update(self):

        size_lifebar = 400
        size_fill = (self.perso.life*size_lifebar)/self.perso.max_life
        g.sman.modify(self.sprids['r'],(self.anc[0]+size_lifebar,self.anc[1]))
        g.sman.modify(self.sprids['mid'],scale=(size_lifebar/32,1))
        g.sman.modify(self.sprids['fill'],scale=(size_fill/32,1))
        self.ui.update()

    def delete(self):
        super(LifeHUD,self).delete()
        self.ui.delete()

class CredHUD(HUD):

    def __init__(self,perso):

        super(CredHUD, self).__init__(group='hud2',name='cred')
        #print(self.group)

        self.perso = perso

        self.anc = (20,20+40)

        size_lifebar = 400
        size_fill = (abs(self.perso.cred)*size_lifebar/2)/100

        if self.perso.cred >=0:
            ancmid = self.anc[0]+size_lifebar/2,self.anc[1]
        else:
            ancmid = self.anc[0]+size_lifebar/2-size_fill,self.anc[1]

        self.addSpr('l',g.TEXTIDS['utils'][4],self.anc,group='hud2')
        self.addSpr('r',g.TEXTIDS['utils'][4],(self.anc[0]+size_lifebar,self.anc[1]),group='hud2')
        self.addSpr('mid',g.TEXTIDS['utils'][3],self.anc,group='hud2')
        g.sman.modify(self.sprids['mid'],scale=(size_lifebar/32,1))


        self.addSpr('fill',g.TEXTIDS['utils'][6],ancmid,group='hud2-1')
        g.sman.modify(self.sprids['fill'],scale=(size_fill/32,1))

        ### UI
        self.ui = Cred_UI(box(*self.anc,self.spr('mid').width,self.spr('mid').height),self.perso)

    def update(self):

        size_lifebar = 400
        size_fill = (abs(self.perso.cred)*size_lifebar/2)/100

        if self.perso.cred >=0:
            ancmid = self.anc[0]+size_lifebar/2,self.anc[1]
        else:
            ancmid = self.anc[0]+size_lifebar/2-size_fill,self.anc[1]

        g.sman.modify(self.sprids['r'],(self.anc[0]+size_lifebar,self.anc[1]))
        g.sman.modify(self.sprids['mid'],scale=(size_lifebar/32,1))
        g.sman.modify(self.sprids['fill'],pos=ancmid,scale=(size_fill/32,1))
        self.ui.update()

    def delete(self):
        super(CredHUD,self).delete()
        self.ui.delete()

class FedHydHUD(HUD):

    def __init__(self,perso):

        super(FedHydHUD, self).__init__(group='hud2',name='life')

        self.perso = perso
        self.anc = (20,60)
        dx = g.SPR + 10
        sy = g.SPR/3
        dy = g.SPR/2 - sy/2

        size_lifebar = 300
        size_fed = (self.perso.fed*size_lifebar)/100
        size_hyd = (self.perso.hyd*size_lifebar)/100

        #self.addSpr('l',g.TEXTIDS['utils'][4],self.anc,group='hud2')
        #self.addSpr('r',g.TEXTIDS['utils'][4],(self.anc[0]+size_lifebar,self.anc[1]),group='hud2')
        #self.addSpr('mid',g.TEXTIDS['utils'][3],self.anc,group='hud2')
        #g.sman.modify(self.sprids['mid'],scale=(size_lifebar/32,1))

        x,y = self.anc

        self.addSpr('water',g.TEXTIDS['items']['bottle'],(x,y),group='hud2-1',wh=(32,32))#,anchor='center')
        #g.sman.modify(self.sprids['water'],scale=(0.5,0.5))
        self.addSpr('hyd',g.tman.addCol(color='clearwater'),(x+dx,y+dy),group='hud2-1')
        g.sman.modify(self.sprids['hyd'],scale=(size_hyd/g.SPR,sy/g.SPR))

        y += g.SPR + 5

        self.addSpr('food',g.TEXTIDS['items']['noodle'],(x,y),group='hud2-1',wh=(32,32))#,anchor='center')
        #g.sman.modify(self.sprids['food'],scale=(0.5,0.5))
        self.addSpr('fed',g.tman.addCol(color='noodle'),(x+dx,y+dy),group='hud2-1')
        g.sman.modify(self.sprids['fed'],scale=(size_fed/g.SPR,sy/g.SPR))


        ### UI
        #self.ui = Life_UI(box(*self.anc,self.spr('fill').width,self.spr('fill').height),self.perso)

    def update(self):
        sy = g.SPR/3

        size_lifebar = 300
        size_fed = (self.perso.fed*size_lifebar)/100
        g.sman.modify(self.sprids['fed'],scale=(size_fed/g.SPR,sy/g.SPR))

        size_hyd = (self.perso.hyd*size_lifebar)/100
        g.sman.modify(self.sprids['hyd'],scale=(size_hyd/g.SPR,sy/g.SPR))

        #self.ui.update()

    def delete(self):
        super(FedHydHUD,self).delete()
        #self.ui.delete()

class RelHUD(HUD):

    def __init__(self,hum):

        super(RelHUD, self).__init__(group='hud2',name='relhud',vis=False)

        self.hum = hum

        cx,cy=g.scr.c
        self.box = box(cx-300,cy-450,600,900)

        self.pad = 25
        self.padding = 50

        #col = (*c['delta_blue'][:3],170)
        self.addCol('bg',self.box,color='delta_blue_faded',group='hud2-1')
        self.addLab('title','relations of '+self.hum.name,(self.box.cx,self.box.fy+self.padding),font_name=1,font_size=20,anchor=('center','center'))

    def update(self):

        if self.visible:

            max_aff = 10

            aff = 0
            y = self.box.fy-(3/4)*self.padding
            xname = self.box.cx - self.box.w/4
            xthg = self.box.cx + self.box.w/4

            size_max_bar = self.box.w/2

            ## EN 1er on affiche les humains dans l'environnement
            for hum in self.hum.hum_env:
                if aff <= max_aff:
                    if hum.id not in self.labids :
                        self.addLab(hum.id,hum.name,(xname,y),font_size=20,anchor=('center','center'),replace=False)
                        self.addLab(hum.id+'o','o',(xthg,y),anchor=('center','center'),replace=False,color=c['green'])

                        y -= self.pad

                        feel = self.hum.get_feel(hum)
                        size_fill = (abs(feel)*size_max_bar/2)/100
                        if feel >=0:
                            xfeel = self.box.cx
                        else:
                            xfeel = self.box.cx-size_fill

                        self.addSpr(hum.id+'hate/like',g.TEXTIDS['utils'][6],(xfeel,y))
                        self.modifySpr(hum.id+'hate/like',scale=(size_fill/32,5/32))
                    else:
                        self.modifyLab(hum.id,(xname,y),(255,255,255,255))
                        self.modifyLab(hum.id+'o',(xthg,y),c['green'])
                        y -= self.pad

                        feel = self.hum.get_feel(hum)
                        size_fill = (abs(feel)*size_max_bar/2)/100
                        if feel >=0:
                            xfeel = self.box.cx
                        else:
                            xfeel = self.box.cx-size_fill

                        self.modifySpr(hum.id+'hate/like',(xfeel,y),scale=(size_fill/32,None))


                    y -= self.padding
                    aff +=1

                elif hum.id in self.labids :
                    self.delLab(hum.id)
                    self.delLab(hum.id+'o')
                    self.delSpr(hum.id+'hate/like')


            # on laisse une ptite place vide pour bien voir
            if len(self.hum.hum_env) > 0:
                y -= self.padding+self.pad
            else:
                max_aff+=1

            col = (255,255,255,170)
            colred = (*c['red'][:3],170)

            ## ENsuite ceux qui n'y sont pas en faded
            #od = OrderedDict(self.hum.relations.items())
            #print(self.hum.relations.items())
            od = OrderedDict(sorted(self.hum.relations.items(), key=lambda t: t[1]['last'],reverse=True))
            for hum in od:
                if hum not in self.hum.hum_env:
                    if aff <= max_aff:
                        #name + time elapsed
                        if hum.id not in self.labids :
                            self.addLab(hum.id,hum.name,(xname,y),font_size=20,anchor=('center','center'),replace=False,color=col)
                            self.addLab(hum.id+'o','o',(xthg,y),anchor=('center','center'),replace=False,color=colred)

                            y -= self.pad

                            feel = self.hum.get_feel(hum)
                            size_fill = (abs(feel)*size_max_bar/2)/100
                            if feel >=0:
                                xfeel = self.box.cx
                            else:
                                xfeel = self.box.cx-size_fill

                            self.addSpr(hum.id+'hate/like',g.TEXTIDS['utils'][6],(xfeel,y))
                            self.modifySpr(hum.id+'hate/like',scale=(size_fill/32,5/32))
                        else:
                            self.modifyLab(hum.id,(xname,y),col)
                            self.modifyLab(hum.id+'o',(xthg,y),colred)
                            y -= self.pad

                            feel = self.hum.get_feel(hum)
                            size_fill = (abs(feel)*size_max_bar/2)/100
                            if feel >=0:
                                xfeel = self.box.cx
                            else:
                                xfeel = self.box.cx-size_fill

                            self.modifySpr(hum.id+'hate/like',(xfeel,y),scale=(size_fill/32,None))

                        y -= self.padding
                        aff +=1

                    elif hum.id in self.labids :
                        self.delLab(hum.id)
                        self.delLab(hum.id+'o')
                        self.delSpr(hum.id+'hate/like')

class MiniRelHUD(HUD):

    def __init__(self,hum):

        super(MiniRelHUD, self).__init__(group='hud2',name='minirelhud',vis=False)

        self.hum = hum
        self.target=None

        x,y = 20,100
        w,h = 300,80
        self.box = box(x,y,w,h)

        self.pad = 25
        self.padding = 50

        #col = (*c['delta_blue'][:3],170)
        self.addCol('bg',self.box,color='delta_blue_faded',group='hud2-1')

    def assign_target(self,hum):
        self.target = hum
        self.addLab('title','relations of '+self.target.name,(self.box.cx,self.box.fy+self.pad),font_name=1,font_size=20,anchor=('center','center'))

    def update(self):

        if self.visible and self.target!=None:

            y = self.box.fy-(3/4)*self.padding
            xname = self.box.cx - self.box.w/4
            xthg = self.box.cx + self.box.w/4

            size_max_bar = self.box.w/2

            hum = self.hum
            if hum in self.target.relations:

                feel = self.target.get_feel(hum)
                size_fill = (abs(feel)*size_max_bar/2)/100
                if feel >=0:
                    xfeel = self.box.cx
                else:
                    xfeel = self.box.cx-size_fill

                if hum in self.target.hum_env:
                    if hum.id not in self.labids :
                        self.addLab(hum.id,hum.name,(xname,y),font_size=20,anchor=('center','center'),replace=False)
                        self.addLab(hum.id+'o','o',(xthg,y),anchor=('center','center'),replace=False,color=c['green'])
                        y -= self.pad
                        self.addSpr(hum.id+'hate/like',g.TEXTIDS['utils'][6],(xfeel,y))
                        self.modifySpr(hum.id+'hate/like',scale=(size_fill/32,5/32))
                    else:
                        self.modifyLab(hum.id,(xname,y),(255,255,255,255))
                        self.modifyLab(hum.id+'o',(xthg,y),c['green'])
                        y -= self.pad
                        self.modifySpr(hum.id+'hate/like',(xfeel,y),scale=(size_fill/32,None))
                else:
                    col = (255,255,255,170)
                    colred = (*c['red'][:3],170)
                    if hum.id not in self.labids :
                        self.addLab(hum.id,hum.name,(xname,y),font_size=20,anchor=('center','center'),replace=False,color=col)
                        self.addLab(hum.id+'o','o',(xthg,y),anchor=('center','center'),replace=False,color=colred)
                        y -= self.pad
                        self.addSpr(hum.id+'hate/like',g.TEXTIDS['utils'][6],(xfeel,y))
                        self.modifySpr(hum.id+'hate/like',scale=(size_fill/32,5/32))
                    else:
                        self.modifyLab(hum.id,(xname,y),col)
                        self.modifyLab(hum.id+'o',(xthg,y),colred)
                        y -= self.pad
                        self.modifySpr(hum.id+'hate/like',(xfeel,y),scale=(size_fill/32,None))

class SonHUD(HUD):

    def __init__(self,perso):

        super(SonHUD, self).__init__(group='ui',name='son')
        #print(self.group)

        self.perso = perso

        self.box = box(1650-820,20,800,64)
        self.padding = 20

        #self.addCol('bg',self.box,group='ui-1')


    def update(self):

        for son in self.perso.invhud.inventory['son']:
            if son._released:
                pass

        """g.lman.set_text(self.labids['coin_lab'],convert_huge_nb(self.perso.money))
        g.lman.set_text(self.labids['fan_lab'],convert_huge_nb(self.perso.nb_fans))
        g.lman.set_text(self.labids['stream_lab'],convert_huge_nb(self.perso.nb_streams))"""
        pass

    def unhide(self,hide=False):

        """g.sman.unhide(self.sprids,hide)
        g.lman.unhide(self.labids,hide)
        g.pman.unhide('icons',hide)"""
        self.visible = not hide

class WriteHUD(HUD):

    def __init__(self):

        super(WriteHUD, self).__init__(group='hud1',name='write',vis=False)

        ##

        self.ui = None

        self.box = box(500,300,1000,600)
        self.padding = 50

        self.addCol('bg',self.box,group='hud-1')

        self.box2 = box(self.box.x+self.padding,self.box.y+2*self.padding,self.box.w-2*self.padding,self.box.h-3*self.padding)

        self.addCol('bg2',self.box2,color='delta_blue',group='hud')

        #self.addLab('quality',o3.convert_quality(self.plum.quality),(self.box.x+self.box.w-self.padding,self.box.cy),anchor=('center','center'))
        self.addLab('pressE','E to write --- ESC to leave',(self.box.cx,self.box.y+self.padding),font_name=1,font_size=20,anchor=('center','center'))
        self.addLab('lit','LIT - zone d\'ecriture',(self.box.cx,self.box.y+self.box.h+self.padding),font_name=1,font_size=20,anchor=('center','center'))

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

        text = g.TEXTIDS['phase'][o3.convert_quality(phase.quality)[0]]

        self.addSpr('phaz_spr',text)
        #g.sman.modify(self.sprids['phaz_spr'],scale=(0.8,0.8))
        g.sman.modify(self.sprids['phaz_spr'],pos=(self.box2.cx - self.spr('phaz_spr').width/2,self.box2.cy - self.spr('phaz_spr').height/2))

        y = (( self.box2.cy + self.spr('phaz_spr').height/2 )  +  (self.box2.y + self.box2.h) )/2
        self.addLab('phaz_content',phase.content,(self.box2.cx,y),anchor=('center','center'),color=c['black'])

        x = (self.box2.cx + self.spr('phaz_spr').width/2  +  (self.box2.x + self.box2.w) )/2
        self.addLab('phaz_qua',o3.convert_quality(phase.quality),(x,self.box2.cy),anchor=('center','center'),color=c['black'],font_name=1,font_size=100)

        x = (self.box2.cx - self.spr('phaz_spr').width/2  +  (self.box2.x) )/2
        self.addLab('phaz_cred',o3.convert_cred(phase.cred),(x,self.box2.cy),anchor=('center','center'),color=c['black'],font_name=1,font_size=100)

        #y = (( self.box2.cy - self.spr('phaz_spr').height/2 )  +  (self.box2.y) )/2
        y = ( self.box2.cy - self.spr('phaz_spr').height/2 ) - 30
        self.addLab('phaz_them','thème : '+phase.them,(self.box2.cx,y),anchor=('center','center'),font_size=20)

        x,y,w,h = self.box2.cx - self.spr('phaz_spr').width/2 , self.box2.cy - self.spr('phaz_spr').height/2 , self.spr('phaz_spr').width , self.spr('phaz_spr').height

        if self.ui != None:
            self.ui.delete()
        self.ui = Writingphase_UI(box(x,y,w,h),phase)

    def catch_or_drop(self,x,y,perso,butt='L'):

        self.ui.check_pressed()
        if self.ui.caught:
            perso.invhud.unhide()
            self.delete_phase(False)
            return 1
        elif self.ui.dropped:
            if self.collision(x,y):
                self.write(self.ui.item)
            elif perso.invhud.visible and perso.invhud.collision(x,y):
                perso.grab(self.ui.item,True)
                self.delete_phase()
            elif perso.selhud.visible and perso.selhud.collision(x,y):
                perso.grab(self.ui.item)
                self.delete_phase()
            else:
                self.delete_phase()
            return -1
        return 0

    ## catch drop self
    def catchable(self,item):
        if type(item).__name__ == 'Phase':
            return True
        return False
    def catch_item(self,item):
        if type(item).__name__ == 'Phase':
            self.write(item)
            return 1
        return 0
    def drop_item(self,item,perso):
        perso.drop(item,False)
    def collision(self,x,y):
        if collisionAX(self.box.realbox,(x,y)):
            return True
        return False

class StudHUD(HUD):

    def __init__(self):

        super(StudHUD, self).__init__(group='hud1',name='stud',vis=False)

        ##

        #self.ui = None

        self.box = box(500,300,1200,650)
        self.padding = 50

        self.item_caught = None

        self.uis = {}
        self.uis['instru'] = None
        self.uis['phase0'] = None
        self.uis['phase1'] = None
        self.uis['phase2'] = None
        self.uis['phase3'] = None
        self.uis['son'] = None

        sz=128
        self.boxs = {}
        self.boxs['instru'] = box( self.box.x+75+11,self.box.y+275+11,sz,sz )
        self.boxs['phase0'] = box( self.box.x+325+11,self.box.y+440+11,sz,sz )
        self.boxs['phase1'] = box( self.box.x+675+11,self.box.y+440+11,sz,sz )
        self.boxs['phase2'] = box( self.box.x+325+11,self.box.y+110+11,sz,sz )
        self.boxs['phase3'] = box( self.box.x+675+11,self.box.y+110+11,sz,sz )
        self.boxs['son'] = box( self.box.x+950+11,self.box.y+275+11,sz,sz )

        self.addSpr('bg',g.TEXTIDS['studhud'],self.box.xy,'hud')

        #self.addLab('quality',o3.convert_quality(self.plum.quality),(self.box.x+self.box.w-self.padding,self.box.cy),anchor=('center','center'))
        self.addLab('pressE','E to assemble a song --- ESC to leave',(400+462.5,self.box.y+self.padding),font_name=1,font_size=20,anchor=('center','center'))
        self.addLab('stud','STUD - zone d\'enregistrement',(self.box.cx,self.box.y+self.box.h+self.padding),font_name=1,font_size=20,anchor=('center','center'))

        self.instru = 0
        self.phases = 0
        self.son = 0

    def assemble(self,perso):

        if self.phases == 4 and self.instru == 1 and self.son == 0: # on peut assembler

            instru = self.uis['instru'].item
            ph = []
            for i in range(4):
                ph.append(self.uis['phase'+str(i)].item)

            son = o3.Son(instru,ph,perso.name)

            self.delete_ui('instru')
            for i in range(4):
                self.delete_ui('phase'+str(i))

            self.uis['son'] = Invent_UI(self.boxs['son'],son,self.visible,scale=(0.4,0.4))
            self.son = 1
        else:
            print('fréro ta r capté')

    def delete_ui(self,lab):

        self.uis[lab].delete()
        self.uis[lab] = None
        if lab[:3] == 'ins':
            self.instru = 0
        elif lab[:3] == 'pha':
            self.phases -= 1
        elif lab[:3] == 'son':
            self.son = 0

    def catch_or_drop(self,x,y,perso,butt='L'):

        if self.item_caught != None:
            ## on check kelui pour vwar si on l'drop

            if self.collision(x,y):
                if type(self.item_caught.item).__name__ != 'Son':
                    self.catch(self.item_caught.item)
                    self.item_caught.delete()
                    self.item_caught = None
                else:
                    return 0

            elif perso.invhud.visible and perso.invhud.collision(x,y):
                perso.grab(self.item_caught.item,True)
                self.item_caught.delete()
                self.item_caught = None

            elif perso.selhud.visible and perso.selhud.collision(x,y):
                perso.grab(self.item_caught.item)
                self.item_caught.delete()
                self.item_caught = None

            else:
                self.item_caught.delete()
                self.item_caught = None
            return -1
        else:
            ## on check touu pour vwar si on en catch

            for lab in self.uis:
                ui = self.uis[lab]
                if ui != None:
                    ui.check_pressed()
                    if ui.caught:
                        self.item_caught = Invent_UI(self.boxs[lab],ui.item,self.visible)
                        self.item_caught.press()
                        self.delete_ui(lab)

                        return 1
        return 0

    def catch(self,thg):

        if type(thg).__name__ == 'Phase' and self.phases < 4:
            for lab in self.uis:
                if lab[:3] == 'pha' and self.uis[lab] == None:
                    self.uis[lab] = Invent_UI(self.boxs[lab],thg,self.visible,scale=(0.4,0.4))
                    self.phases+=1
                    break

        elif type(thg).__name__ == 'Instru' and self.instru == 0:
            self.uis['instru'] = Invent_UI(self.boxs['instru'],thg,self.visible,scale=(0.4,0.4))
            self.instru = 1
        else:
            print('u cant drop this here cheh')

    def unhide(self,hide=False):
        super(StudHUD,self).unhide(hide)

        if hide and self.item_caught != None:
            self.catch(self.item_caught.item)
            self.item_caught.delete()
            self.item_caught = None

        for lab in self.uis:
            ui = self.uis[lab]
            if ui != None:
                ui.unhide(hide)

    ## catch drop self
    def catchable(self,item):
        if type(item).__name__ == 'Phase' and self.phases < 4:
            return True
        elif type(item).__name__ == 'Instru' and self.instru == 0:
            return True
        return False
    def catch_item(self,item):
        if type(item).__name__ == 'Phase' and self.phases < 4:
            self.catch(item)
            return 1
        elif type(item).__name__ == 'Instru' and self.instru == 0:
            self.catch(item)
            return 1
        return 0
    def drop_item(self,item,perso):
        perso.drop(item,False)
    def collision(self,x,y):
        if collisionAX(self.box.realbox,(x,y)):
            return True
        return False

class MarketHUD(HUD):

    def __init__(self,perso):

        super(MarketHUD, self).__init__(group='hud1',name='market',vis=False)

        ##

        self.ui = None

        self.box = box(500,300,1000,650)
        self.padding = 50

        self.item_caught = None

        self.uis = {}
        self.uis['main'] = None
        self.uis['instru0'] = None
        self.uis['instru1'] = None
        self.uis['instru2'] = None
        self.uis['instru3'] = None

        self.old_main_pos = None

        sz = 128

        self.boxs = {}
        self.boxs['main'] = box( self.box.x+230,self.box.y+222,2*sz,2*sz )
        self.boxs['instru0'] = box( self.box.x+820+1,self.box.y+476+11,sz,sz )
        self.boxs['instru1'] = box( self.box.x+820+1,self.box.y+342+11,sz,sz )
        self.boxs['instru2'] = box( self.box.x+820+1,self.box.y+208+11,sz,sz )
        self.boxs['instru3'] = box( self.box.x+820+1,self.box.y+74+11,sz,sz )

        self.addSpr('bg',g.TEXTIDS['ordhud'],self.box.xy,'hud')

        #self.addLab('quality',o3.convert_quality(self.plum.quality),(self.box.x+self.box.w-self.padding,self.box.cy),anchor=('center','center'))
        self.addLab('longclick','longclick on an instru to buy --- ESC to leave',(self.box.cx,self.box.y+self.padding),font_name=1,font_size=20,anchor=('center','center'))
        self.addLab('market','Ordi - achat d\'instrus',(self.box.cx,self.box.y+self.box.h+self.padding),font_name=1,font_size=20,anchor=('center','center'))

        self.instru = 0
        self.perso = perso
        self.add_instru(0)

    def delete_ui(self,lab):

        self.uis[lab].delete()
        self.uis[lab] = None
        if lab[:3] == 'ins':
            self.instru -= 1
        elif lab == 'main':
            for lab2 in ['qua','bt','price','status']:
                g.lman.delete(self.labids[lab+'_'+lab2])
                del self.labids[lab+'_'+lab2]

            g.sman.delete(self.sprids[lab+'_price'])
            del self.sprids[lab+'_price']

    def catch_or_drop(self,x,y,butt='L'):

        #print("wesh")

        if self.item_caught != None:
            ## on check kelui pour vwar si on l'drop

            if self.collision(x,y):
                self.inspect(self.item_caught.item)

            elif self.perso.invhud.visible and self.perso.invhud.collision(x,y):
                self.perso.grab(self.item_caught.item,True)

            elif self.perso.selhud.visible and self.perso.selhud.collision(x,y):
                self.perso.grab(self.item_caught.item)

            self.item_caught.delete()
            self.item_caught = None
            return -1
        else:
            ## on check touu pour vwar si on en catch

            for lab in self.uis:
                ui = self.uis[lab]

                if ui != None and lab != 'main':
                    ui.check_pressed()
                    if ui.caught:
                        self.inspect(ui.item,int(lab[-1]))
                        self.delete_ui(lab)
                        return 2

                elif ui != None: # on est dans le main
                    if self.perso in ui.item.owners:
                        ui.check_pressed()
                        if ui.caught:
                            self.item_caught = Invent_UI(self.boxs[lab],ui.item,self.visible)
                            self.item_caught.press()
                            self.delete_ui(lab)

                            return 1
                    if ui._hoover:
                        return 2

        return 0

    def inspect(self,ins,pos=None):

        if self.uis['main'] != None:

            if self.perso in self.uis['main'].item.owners:
                self.perso.grab(self.uis['main'].item)
            elif self.old_main_pos != None and self.old_main_pos <= 3:
                self.uis['instru'+str(self.old_main_pos)] = Invent_UI(self.boxs['instru'+str(self.old_main_pos)],self.uis['main'].item,self.visible,(0.4,0.4))
            self.delete_ui('main')

        self.old_main_pos = pos

        self.uis['main'] = Invent_UI(self.boxs['main'],ins,self.visible,(0.8,0.8))
        padding = 150

        # creating new details
        self.addLab('main_qua',o3.convert_quality(ins.quality),(self.boxs['main'].cx,self.boxs['main'].cy+padding),font_name=1,anchor=('center','center'),color=c['white'],font_size=50)
        self.addLab('main_bt',ins.author.name,(self.boxs['main'].cx,self.boxs['main'].cy-padding),anchor=('center','center'),color=c['white'],font_size=30)
        self.addLab('main_price',convert_huge_nb(ins.price),(self.box.x+129,self.boxs['main'].cy),font_name=1,anchor=('right','center'),color=c['yellow'],font_size=30)
        self.addSpr('main_price',g.TEXTIDS['ux'][0],(self.box.x+129,self.boxs['main'].cy),wh=(64,64),anchor=('left','center'))

        if self.perso in ins.owners:
            status,color = "purchased",c['green']
        else:
            status,color = "on sale",c['red']

        self.addLab('main_status',status,(self.box.x+609,self.boxs['main'].cy),anchor=('center','center'),color=color,font_size=30)

    def add_instru(self,dt):

        ins = o3.rinstru()

        # deleting last instru
        if self.uis['instru3'] != None:
            self.delete_ui('instru3')

        # moving each instru and details to next box
        for i in range(2,-1,-1):

            # each instru
            self.uis['instru'+str(i+1)] = self.uis['instru'+str(i)]
            if self.uis['instru'+str(i+1)] != None:
                self.uis['instru'+str(i+1)].upbox(self.boxs['instru'+str(i+1)])
        if self.old_main_pos != None:
            self.old_main_pos += 1

        # replacing the first box with the new instru
        self.uis['instru0'] = Invent_UI(self.boxs['instru0'],ins,self.visible,(0.4,0.4))
        self.instru += 1
        # recalling this function
        t = r.randint(2,10)
        #print('wow new instru :',ins,'next in',t,'secondes')
        g.bertran.schedule_once(self.add_instru,t)

    def actualise(self):

        if self.uis['main'] != None:
            ins = self.uis['main'].item

            padding = 150

            # creating new details
            self.addLab('main_qua',o3.convert_quality(ins.quality),(self.boxs['main'].cx,self.boxs['main'].cy+padding),anchor=('center','center'),color=c['white'],font_name=1,font_size=50)
            self.addLab('main_bt',ins.author.name,(self.boxs['main'].cx,self.boxs['main'].cy-padding),anchor=('center','center'),color=c['white'],font_size=30)
            self.addLab('main_price',convert_huge_nb(ins.price),(self.box.x+129,self.boxs['main'].cy),anchor=('right','center'),color=c['yellow'],font_name=1,font_size=30)
            self.addSpr('main_price',g.TEXTIDS['ux'][0],(self.box.x+129,self.boxs['main'].cy),wh=(64,64),anchor=('left','center'))

            if self.perso in ins.owners:
                status,color = "purchased",c['green']
            else:
                status,color = "on sale",c['red']

            self.addLab('main_status',status,(self.box.x+609,self.boxs['main'].cy),anchor=('center','center'),color=color,font_size=30)

    def buy_instru(self):

        if self.uis['main'] != None and self.perso.money >= self.uis['main'].item.price:
            self.perso.add_money(-self.uis['main'].item.price)
            self.uis['main'].item.add_owner(self.perso)
            self.actualise()

        #print('u wanna buy instru n*'+str(k), 'it will cost'+convert_huge_nb(self.uis['instru'+str(k)].item.price),'$')

    def unhide(self,hide=False):
        super(MarketHUD,self).unhide(hide)

        if hide and self.item_caught != None:
            perso.grab(self.item_caught.item)
            self.item_caught.delete()
            self.item_caught = None

        for lab in self.uis:
            ui = self.uis[lab]
            if ui != None:
                ui.unhide(hide)

    ## catch drop self
    def catchable(self,item):
        if type(item).__name__ == 'Instru':
            return True
        return False
    def catch_item(self,item):
        if type(item).__name__ == 'Instru':
            self.inspect(item)
            return 1
        return 0
    def drop_item(self,item,perso):
        perso.drop(item,False)
    def collision(self,x,y):
        if collisionAX(self.box.realbox,(x,y)):
            return True
        return False

class ChartsHUD(HUD):

    def __init__(self,hum):

        super(ChartsHUD, self).__init__(group='hud2',name='charts',vis=False)

        self.hum = hum

        cx,cy=g.scr.c
        self.box = box(cx-300,cy-450,600,900)

        self.pad = 40
        self.padding = 50

        self.addCol('bg',self.box,color='black_faded',group='hud2-1')
        self.addLab('title','top 20 charts artists',font_name=1,font_size=20,anchor=('center','center'))

    def update(self):

        if self.visible:

            y = self.box.fy-(3/4)*self.padding
            x_classman = self.box.x + self.padding
            x_name = self.box.x + 2*self.padding
            x_streams = self.box.fx - 3*self.padding

            for k in range(len(p.top_20_artists)):
                ast = p.top_20_artists[k] #ast = artist

                coltop = 'red'
                col = 'white'
                if ast == self.hum :
                    coltop = 'yellow'
                    col = 'yellow'

                if ast.id not in self.labids :
                    self.addLab(ast.id+'__top__',str(k+1),(x_classman,y),font_size=20,anchor=('center','center'),color=c[coltop])
                    self.addLab(ast.id,ast.name,(x_name,y),font_size=20,anchor=('left','center'),color=c[col])
                    self.addLab(ast.id+'__streams__',convert_huge_nb(ast.nb_streams),(x_streams,y),font_size=20,anchor=('left','center'),color=c['lightblue'])
                else:
                    #self.addLab(ast.id+'__top__',str(k+1),(x_classman,y),anchor=('center','center'),color=c[coltop])
                    self.modifyLab(ast.id,(x_name,y))
                    self.modifyLab(ast.id+'__top__',(x_classman,y))
                    self.set_text(ast.id+'__top__',str(k+1))
                    self.modifyLab(ast.id+'__streams__',(x_streams,y))
                    self.set_text(ast.id+'__streams__',convert_huge_nb(ast.nb_streams))

                y -= self.pad

            if self.hum not in p.top_20_artists:
                classman = p.charts['artists'].index(self.hum)
                if self.hum.id not in self.labids :
                    self.addLab(self.hum.id+'__top__',str(classman+1),(x_classman,y),anchor=('center','center'),color=c['yellow'])
                    self.addLab(self.hum.id,self.hum.name,(x_name,y),font_size=20,anchor=('left','center'),color=c['yellow'])
                    self.addLab(self.hum.id+'__streams__',convert_huge_nb(self.hum.nb_streams),(x_streams,y),anchor=('left','center'),color=c['lightblue'])
                else:
                    #self.addLab(self.hum.id+'__top__',str(classman+1),(x_classman,y),anchor=('center','center'),color=c['yellow'])
                    self.modifyLab(self.hum.id+'__top__',(x_classman,y))
                    self.set_text(self.hum.id+'__top__',str(classman+1))
                    self.modifyLab(self.hum.id,(x_name,y))
                    self.modifyLab(self.hum.id+'__streams__',(x_streams,y))
                    self.set_text(self.hum.id+'__streams__',convert_huge_nb(self.hum.nb_streams))

            ids = [x.id for x in p.top_20_artists]
            todel = []
            for lab in self.labids:
                if not '__top__' in lab and not '__streams__' in lab and lab != self.hum.id:
                    if lab not in ids:
                        todel.append(lab)

            for lab in todel:
                self.delLab(lab)
                self.delLab(lab+'__top__')
                self.delSpr(lab+'__streams__')

#---# hud spéciaux inventaire/selecteur

class InventHUD(HUD):

    def __init__(self,perso,fill=True):

        super(InventHUD, self).__init__(group='hud21',name='inv',vis=False)

        self.perso = perso

        self.item_caught = None

        # inventory
        self.uis = {}
        self.uis['phase'] = []
        self.uis['instru'] = []
        self.uis['son'] = []
        self.uis['general'] = []
        self.uis['plume'] = []

        ### GENERAL

        self.box = box(20,200,338,800)
        self.padding = 64
        self.padding2 = 20
        self.lilpadding = 12
        self.lilpadding2 = 6


        ### COLORS

        self.addCol('bg',self.box,group='hud2-1')

        self.box2 = box(self.box.x+self.padding2,self.box.y+self.padding2,self.box.w-2*self.padding2,self.box.h-self.padding2-100)

        self.addCol('bg2',self.box2,color='delta_blue',group='hud2')

        ### MENUS

        self.menus = ['general','sound']
        self.menu = 'general'
        self.btns = {}

        self.menus_cont = {}
        self.menus_cont['general'] = ['general']
        self.menus_cont['sound'] = ['plume','son','instru','phase']

        h = 90
        for i in range(len(self.menus)):
            zone_box = box(self.box2.fx,self.box2.y+i*h,h,h)
            x,y = zone_box.cxy
            x -= 32
            y -= 32
            self.addSpr('menu_'+self.menus[i],g.TEXTIDS['ux'][4+i],(x,y),group='hud3',wh=(64,64))
            self.btns[self.menus[i]] = Toggle(zone_box,self.roll_menu,[self.menus[i]],self.menus[i],vis=self.visible)

        self.btns[self.menu].toggle()

        ### PARTIE DETAILS

        self.autorize_deta = True
        self.deta_visible = False
        self.detaids = {}
        self.detaids['spr'] = {}
        self.detaids['bg'] = {}
        self.detaids['lab'] = {}

        height_detail = self.box.h-len(self.menus)*h-self.padding2
        width_detail = 180

        self.box3 = box(self.box.fx,self.box.fy-int(height_detail),width_detail,int(height_detail))
        self.addCol('bgdeta',self.box3,group='hud2-1',detail=True)

        self.box4 = box(self.box.fx,self.box.y,h,len(self.menus)*h+2*self.padding2)
        self.addCol('bg4',self.box4,group='hud2-1')



        ### LABEL inv
        self.addLab('inv_lab','inventory',(self.box.cx,self.box.fy-50),font_name=1,anchor=('center','center'))

        if fill and False:

            ## /WARNING\ Ne peut fonctionner car grab / drop doit se situer APRES
            ## initialistion de selhud et invhud

            #self.update()
            for i in range(r.randint(2,10)):
                ins = Instru(r.random(),r.choice(btmakers))
                ins.add_owner(self.perso)
                self.perso.grab(ins)
            for i in range(r.randint(2,10)):
                ph = []
                for i in range(4):
                    ph.append(Phase(rqua(),rcred()))
                instru = Instru(r.random(),r.choice(btmakers))

                self.perso.grab(Son(instru,ph))

    # add/del/update

    def add_ui(self,item):

        vis = True
        if not self.visible:
            vis = False
        if isinstance(item,o3.Sound_item) and self.menu == 'general':
            vis = False
        if not isinstance(item,o3.Sound_item) and self.menu == 'sound':
            vis = False

        # on stocke l'ui
        if isinstance(item,o3.Sound_item):
            self.uis[type(item).__name__.lower()].append(Invent_UI(box(w=self.padding,h=self.padding),item,vis))
        else:
            self.uis['general'].append(Invent_UI(box(w=self.padding,h=self.padding),item,vis))

        self.update()

        #print(self.uis)

    def del_ui(self,item,up=True):

        #print(self.uis,item)
        #print(list(map(lambda x:x.item,self.uis['general'])))

        if type(item) == type([]):
            for subitem in item:
                self.del_ui(subitem,False)
        elif item != None:
            if isinstance(item,o3.Sound_item):
                ui = list(filter(lambda x:x.item == item,self.uis[type(item).__name__.lower()]))[0]
                ui.delete()
                self.uis[type(item).__name__.lower()].remove(ui)
            else:
                ui = list(filter(lambda x:x.item == item,self.uis['general']))[0]
                #print(self.uis['general'])
                ui.delete()
                self.uis['general'].remove(ui)

        if up:
            self.update()

    def del_caught_ui(self):
        if self.item_caught != None:
            tab = []
            for cquecé in self.uis:
                for x in self.uis[cquecé]:
                    tab.append(x)
            if self.item_caught not in tab:
                self.item_caught.delete()
            self.item_caught = None
            self.update()

    def update(self):

        #self.create_uis()

        if self.menu == 'sound':
            yf = self.box2.fy

            for cquecé in self.menus_cont[self.menu]:
                tab = self.uis[cquecé]
                if tab != []:
                    #cquecé = type(tab[0].item).__name__.lower()
                    self.addLab(cquecé+'s_lab',cquecé+'s',(self.box.cx,yf-self.padding2),font_name=1,color=c['black'],font_size=20,anchor=('center','center'))
                    yf -= self.padding2*2

                    self.uis[cquecé].sort(reverse=True)

                    for i in range(len(self.uis[cquecé])):

                        x = self.box2.x + self.padding/2 + self.lilpadding + (self.padding + self.lilpadding2)*(i%4)
                        y = yf + self.padding/2 - (self.padding + self.lilpadding2)*(i//4 + 1)

                        self.uis[cquecé][i].move(x,y)
                    yf -= (self.padding + self.lilpadding2)*((len(self.uis[cquecé])-1)//4 + 1) + self.lilpadding - self.lilpadding2
                else:
                    if (cquecé+'s_lab') in self.labids:
                        g.lman.delete(self.labids[cquecé+'s_lab'])
                        del self.labids[cquecé+'s_lab']

        elif self.menu == 'general':
            yf = self.box2.fy

            for cquecé in self.menus_cont[self.menu]:
                tab = self.uis[cquecé]
                if tab != []:
                    #self.uis[cquecé].sort(reverse=True)
                    for i in range(len(self.uis[cquecé])):

                        x = self.box2.x + self.padding/2 + self.lilpadding + (self.padding + self.lilpadding2)*(i%4)
                        y = yf + self.padding/2 - (self.padding + self.lilpadding2)*(i//4 + 1)

                        self.uis[cquecé][i].update()
                        self.uis[cquecé][i].move(x,y)
                    yf -= (self.padding + self.lilpadding2)*((len(self.uis[cquecé])-1)//4 + 1) + self.lilpadding - self.lilpadding2


    # general

    def unhide(self,hide=False):
        super(InventHUD,self).unhide(hide)

        if hide and self.item_caught != None:
            item = self.item_caught.item
            self.del_caught_ui()
            self.drop_item(item,self.perso)
            self.catch_item(item)
            self.update()

        for cquecé in self.menus_cont[self.menu]:
            for ui in self.uis[cquecé]:
                ui.unhide(hide)

        for menu in self.btns:
            if not hide:
                if menu == self.menu:
                    self.btns[menu].set_act()
                else:
                    self.btns[menu].set_nap()

            self.btns[menu].unhide(hide)

        if (not hide) and (not self.deta_visible):
            self.eff_detail()
        elif hide and self.deta_visible:
            self.eff_detail()

    def catch_or_drop(self,x,y,butt='L'):

        if self.item_caught :
            ## on check kelui pour vwar si on l'drop

            self.item_caught.check_pressed()

            if self.item_caught.dropped:
                item = self.item_caught.item

                hud = None

                # choix du hud
                if self.collision(x,y):
                    hud = self
                elif self.perso.selhud.visible and self.perso.selhud.collision(x,y):
                    hud = self.perso.selhud
                elif self.perso.zone_colli != None and isinstance(self.perso.zone_colli,o3.Zone_ACTIV) and self.perso.zone_colli.activated and self.perso.zone_colli.hud.collision(x,y):
                    hud = self.perso.zone_colli.hud

                # on vérifie si c'est R on drop un seul item
                unstacked = False
                if butt == 'R' and item.stacked > 1:
                    item = item.unstack()
                    if hud == None or hud.catchable(item):
                        unstacked = True
                    else:
                        # ici le hud existe mais ne l'a pas accepté
                        self.item_caught.item.stack(item)
                        item = self.item_caught.item

                    self.item_caught.update()

                if hud:
                    # si on a un hud on essaie de le catch
                    if hud.catchable(item):
                        if not unstacked: self.del_caught_ui()
                        self.drop_item(item,self.perso)
                        hud.catch_item(item)
                        if not unstacked: return -1
                    else:
                        self.item_caught.check_pressed()
                else:
                    # si on a pas de hud on tej juste l'item
                    if not unstacked: self.del_caught_ui()
                    self.perso.drop(item)
                    if not unstacked: return -1

                if unstacked:
                    # on rattrape l'item caught sans
                    self.item_caught.catch()
                    return 2

        else:
            ## on check touu pour vwar si on en catch

            if self.menu == 'sound':
                for x in self.menus_cont[self.menu]:
                    tab = self.uis[x]
                    for ui in tab:

                        # ici pas besoin de tester les stack vu qu'on ne peut stacker les sound_item
                        # /WARNING\ ça peut changer !

                        ui.check_pressed()
                        if ui.caught:
                            self.item_caught = ui
                            return 1

            elif self.menu == 'general':
                for ui in self.uis['general']:

                    if butt == 'L':
                        ui.check_pressed()
                        if ui.caught:
                            self.item_caught = ui
                            return 1
                    elif butt == 'R':
                        # ici on prend un seul item si on clik sur un truc
                        if ui._hoover:
                            # ça veut dire qu'on catch cet ui

                            # on vérifie cb de stack il a
                            if ui.item.stacked == 1:
                                ui.catch()
                                self.item_caught = ui
                                return 1
                            elif ui.item.stacked > 1:
                                item = ui.item.unstack()
                                ui = Invent_UI(box(),item,self.visible)
                                self.item_caught = ui
                                ui.catch()
                                self.update()
                                return 1

        return 0

    def quick_catch_and_drop(self):

        selector = False
        item = self.item_caught.item

        if self.perso.zone_colli != None and isinstance(self.perso.zone_colli,o3.Zone_ACTIV) and self.perso.zone_colli.activated:

            if type(self.perso.zone_colli) == Lit and type(item).__name__ == 'Phase':
                self.del_caught_ui()
                self.perso.drop(item,create=False)
                self.perso.zone_colli.hud.write(item)

            elif type(self.perso.zone_colli) == Ordi and type(item).__name__ == 'Instru':
                self.del_caught_ui()
                self.perso.drop(item,create=False)
                self.perso.zone_colli.hud.inspect(item)

            elif type(self.perso.zone_colli) == Studio:

                if type(item).__name__ == 'Phase' and self.perso.zone_colli.hud.phases < 4:
                    self.del_caught_ui()
                    self.perso.drop(item,create=False)
                    self.perso.zone_colli.hud.catch(item)

                elif type(item).__name__ == 'Instru' and self.perso.zone_colli.hud.instru == 0:
                    self.del_caught_ui()
                    self.perso.drop(item,create=False)
                    self.perso.zone_colli.hud.catch(item)

                else:
                    selector = True

            else:
                selector = True

        else:
            selector = True

        if selector:
            self.del_caught_ui()
            self.perso.drop(item,False)
            self.perso.grab(item)
            return -1

    def check_hoover(self,x,y):

        # inventory
        something_to_aff = False

        for cquecé in self.menus_cont[self.menu]:
            for ui in self.uis[cquecé]:
                ui.check_mouse(x,y)
                if ui._hoover:
                    something_to_aff = True
                    self.aff_detail(ui)

        if not something_to_aff:
            self.eff_detail()

        # menus
        for menu in self.btns:
            self.btns[menu].check_mouse(x,y)


    ## catch drop self
    def catchable(self,item):
        return True
    def catch_item(self,item):
        self.perso.grab(item,True)
        return 1
    def drop_item(self,item,perso):
        perso.drop(item,False)
    def collision(self,x,y):
        if collisionAX(self.box.realbox,(x,y)):
            return True
        if collisionAX(self.box4.realbox,(x,y)):
            return True
        return False

    ## de base

    def addSpr(self,key,textid,xy_pos=(0,0),group=None,detail=False,wh=None,anc=None):
        super(InventHUD,self).addSpr(key,textid,xy_pos,group,wh,anc)
        if detail:
            self.detaids['spr'][key]=self.sprids[key]
            del self.sprids[key]

    def addCol(self,key,box,color='delta_purple',group=None,detail=False):
        super(InventHUD,self).addCol(key,box,color,group)
        if detail:
            self.detaids['bg'][key]=self.sprids[key]
            del self.sprids[key]

    def addLab(self,key,contenu,xy_pos=(0,0),group=None,font_name=1,font_size=30,anchor=('left','bottom'),color=(255,255,255,255),detail=False):
        super(InventHUD,self).addLab(key,contenu,xy_pos,group,font_name,font_size,anchor,color)
        if detail:
            self.detaids['lab'][key]=self.labids[key]
            del self.labids[key]

        #print(xy_pos)


    ## print

    def __str__(self):
        s = ''
        #print('waw')
        for item in self.uis['son']+self.uis['instru']+self.uis['phase']:
            s+=str(item.item)+'\n'
        return s

    ## details

    def aff_detail(self,ui):

        if self.autorize_deta:

            for fam in self.detaids:
                if fam == 'lab':
                    g.lman.delete(self.detaids[fam])
                elif fam == 'spr':
                    g.sman.delete(self.detaids[fam])
            self.detaids['spr'] = {}
            self.detaids['lab'] = {}

            if isinstance(ui.item,o3.Sound_item):
                #skin
                self.addSpr('detail_spr',g.TEXTIDS[type(ui.item).__name__.lower()][o3.convert_quality(ui.item.quality)[0]],detail=True)
                #self.detaids.append(self.sprids['detail_spr'])
                g.sman.modify(self.detaids['spr']['detail_spr'],scale=(0.5,0.5))
                g.sman.modify(self.detaids['spr']['detail_spr'],( self.box3.cx - g.sman.spr(self.detaids['spr']['detail_spr']).width/2 , self.box3.fy - 80 - g.sman.spr(self.detaids['spr']['detail_spr']).height/2 ))
                y = g.sman.spr(self.detaids['spr']['detail_spr']).y

                #qua
                self.addLab('detail_qua',o3.convert_quality(ui.item.quality), ( self.box3.cx , y - 2*self.padding2 ), anchor = ('center','center'),detail=True)
                #self.detaids.append(self.detaids['lab']['detail_qua'])
                y = g.lman.labels[self.detaids['lab']['detail_qua']].y

                #cred / author
                if type(ui.item).__name__ != 'Instru':

                    self.addLab('detail_cred',o3.convert_cred(ui.item.cred), ( self.box3.cx , y - self.padding ), anchor = ('center','center'),detail=True)
                    #    self.detaids.append(self.detaids['lab']['detail_cred'])
                    y = g.lman.labels[self.detaids['lab']['detail_cred']].y

                else:
                    self.addLab('detail_aut',ui.item.author.name, ( self.box3.cx , y - self.padding ),font_name=0, anchor = ('center','center'),font_size = 20,detail=True)
                    #    self.detaids.append(self.detaids['lab']['detail_aut'])
                    y = g.lman.labels[self.detaids['lab']['detail_aut']].y

                # phase
                if type(ui.item).__name__ == 'Phase':

                    tab = ui.item.content.split(' ')
                    #content = tab[0] + ' ' + tab[1] + '\n' + ' '.join(tab[2:])

                    self.addLab('detail_cont','\n'.join(tab), ( self.box3.cx , y - self.padding ),font_name=0, anchor = ('center','center'),font_size = 15,detail=True,color=c['black'])
                    #    self.detaids.append(self.detaids['lab']['detail_aut'])
                    y = g.lman.labels[self.detaids['lab']['detail_cont']].y

            else:
                self.addSpr('detail_spr',g.TEXTIDS['items'][type(ui.item).__name__.lower()],detail=True)
                g.sman.modify(self.detaids['spr']['detail_spr'],scale=(0.5,0.5))
                g.sman.modify(self.detaids['spr']['detail_spr'],( self.box3.cx - g.sman.spr(self.detaids['spr']['detail_spr']).width/2 , self.box3.fy - 80 - g.sman.spr(self.detaids['spr']['detail_spr']).height/2 ))

                if type(ui.item).__name__ == 'Key':
                    y = g.sman.spr(self.detaids['spr']['detail_spr']).y
                    self.addLab('detail_street',ui.item.target.name, ( self.box3.cx , y - 2*self.padding2 )\
                                    ,font_name=0, anchor = ('center','center'),font_size = 15,detail=True)

                elif type(ui.item).__name__ == 'Bottle':
                    y = g.sman.spr(self.detaids['spr']['detail_spr']).y
                    self.addLab('detail_liquid',ui.item.liquid, ( self.box3.cx , y - 2*self.padding2 )\
                                    ,font_name=0, anchor = ('center','center'),font_size = 15,detail=True)
                    y -= 2*self.padding2
                    self.addLab('detail_qté',str(ui.item.qt) +' mL', ( self.box3.cx , y - 2*self.padding2 )\
                                    ,font_name=0, anchor = ('center','center'),font_size = 15,detail=True)



            ## FINISH

            self.deta_visible = True
            for fam in self.detaids:
                if fam == 'lab':
                    g.lman.unhide(self.detaids[fam])
                else:
                    g.sman.unhide(self.detaids[fam])

    def eff_detail(self):
        self.deta_visible = False
        for fam in self.detaids:
            if fam == 'lab':
                g.lman.unhide(self.detaids[fam],True)
            else:
                g.sman.unhide(self.detaids[fam],True)

    ## menus

    def check_press_btns(self,x,y):

        for menu in self.btns:
            ui = self.btns[menu]
            if ui.check_pressed():
                return True

    def roll_menu(self,menu='general'):

        if self.menu != menu:

            for lab in self.btns:
                if lab == menu:
                    self.btns[lab].set_act()
                else:
                    self.btns[lab].set_nap()

            if self.menu == 'sound':
                if 'sons_lab' in self.labids:
                    g.lman.delete(self.labids['sons_lab'])
                    del self.labids['sons_lab']
                if 'instrus_lab' in self.labids:
                    g.lman.delete(self.labids['instrus_lab'])
                    del self.labids['instrus_lab']
                if 'phases_lab' in self.labids:
                    g.lman.delete(self.labids['phases_lab'])
                    del self.labids['phases_lab']
                if 'plumes_lab' in self.labids:
                    g.lman.delete(self.labids['plumes_lab'])
                    del self.labids['plumes_lab']

            for cquecé in self.menus_cont[self.menu]:
                for ui in self.uis[cquecé]:
                    ui.unhide(True)
            self.menu = menu
            for cquecé in self.menus_cont[self.menu]:
                for ui in self.uis[cquecé]:
                    ui.unhide()

            self.update()

class SelectHUD(HUD):

    def __init__(self,perso):

        super(SelectHUD, self).__init__(group='hud2',name='selecter')

        self.perso = perso

        self.item_caught = None

        self.biggitem_w = 3*g.SPR
        self.smallitem_w = g.SPR
        self.padding = self.smallitem_w*1.8
        self.pad = 100


        # general : boxin
        self.box = box(1650,20,250,150)
        self.box2 = self.box.pop()
        self.box2.y += self.box.h
        self.box2.x = self.box.fx-self.padding
        self.box2.w = self.padding
        self.box2.h = (len(self.perso.selecter)-1)*self.padding

        self.texts = {'fight':g.tman.addCol('red_fight'),'peace':g.tman.addCol('delta_purple'),'sneak':g.tman.addCol('black')}
        self.faded_texts = {'fight':g.tman.addCol('red_fight_faded'),'peace':g.tman.addCol('delta_blue_faded'),'sneak':g.tman.addCol('black_faded')}
        self.MODE = self.perso.MODE

        self.addSpr('bg',self.texts[self.MODE],self.box.xy,group='hud2-1',wh=self.box.wh)
        self.addSpr('bg2',self.faded_texts[self.MODE],self.box2.xy,group='hud2-1',wh=self.box2.wh)

        # inventory
        self.uis = {}
        for i in range(len(self.perso.selecter)):
            self.uis[i] = None

        # details
        self.details = {}
        self.details['up'] = None
        self.details['mid'] = None
        self.details['bottom'] = None

        self.update()

    def update(self):

        # modes
        if self.MODE != self.perso.MODE:
            self.set_text('bg',self.texts[self.perso.MODE],wh=self.box.wh)
            self.set_text('bg2',self.faded_texts[self.perso.MODE],wh=self.box2.wh)
            self.MODE = self.perso.MODE


        # on check les items dans le selecter du perso et on les mets à la bonne place

        # verif lequel est selected
        sel = []
        for i in range(len(self.uis)):
            x = self.perso.selected+i
            if x >= len(self.uis):
                x -= len(self.uis)
            sel.append(x)

        for k in range(len(sel)):
            i = sel[k]
            item = self.perso.selecter[i]

            if not self.item_caught or (self.item_caught and not self.uis[i] == self.item_caught):
                if item != None:

                    x,y = self.box2.cx,self.box2.y + (k-1)*(self.padding) + self.padding/2
                    w = self.smallitem_w

                    # si c'est l'element selectionné on met bien
                    if k == 0:
                        w = self.biggitem_w
                        x,y = self.box.fx-3*w/4,self.box.cy

                    # on crée si jamais
                    if self.uis[i] == None:
                        self.uis[i] = Invent_UI(box(x-w/2,y-w/2,w,w),item,spr_vis=self.visible)

                    # on scale et on place
                    if g.sman.spr(self.uis[i].itemspr).width != w:
                        self.uis[i].modify(size=(w,w))

                    self.uis[i].upbox(box(x-w/2,y-w/2,w,w))

                else:
                    if self.uis[i] != None:
                        self.uis[i].delete()
                        self.uis[i] = None

            if k == 0:
                # on update les details
                self.update_details(item)

    def del_caught_ui(self):
        #print('ohahahh')
        if self.item_caught != None :
            if self.item_caught not in list(self.uis.values()):
                self.item_caught.delete()
            self.item_caught = None
            self.update()

    # hoover catch drop ...

    def check_hoover(self,x,y):
        for cquecé in self.uis:
            if self.uis[cquecé] != None:
                self.uis[cquecé].check_mouse(x,y)

    def catch_or_drop(self,x,y,butt='L'):

        if self.item_caught :
            ## on check kelui pour vwar si on l'drop
            self.item_caught.check_pressed()

            if self.item_caught.dropped:
                item = self.item_caught.item

                hud = None

                # choix du hud
                if self.collision(x,y):
                    hud = self
                elif self.perso.invhud.visible and self.perso.invhud.collision(x,y):
                    hud = self.perso.invhud
                elif self.perso.zone_colli != None and isinstance(self.perso.zone_colli,o3.Zone_ACTIV) and self.perso.zone_colli.activated and self.perso.zone_colli.hud.collision(x,y):
                    hud = self.perso.zone_colli.hud

                # on vérifie si c'est R on drop un seul item

                unstacked = False

                if butt == 'R' and item.stacked > 1:
                    item = item.unstack()
                    if hud == None or hud.catchable(item):
                        unstacked = True
                    else:
                        # ici le hud existe mais ne l'a pas accepté
                        self.item_caught.item.stack(item)
                        item = self.item_caught.item

                    self.item_caught.update()

                if hud:
                    # si on a un hud on essaie de le catch
                    if hud.catchable(item):
                        if not unstacked: self.del_caught_ui()
                        self.drop_item(item,self.perso)
                        hud.catch_item(item)
                        if not unstacked: return -1
                    else:
                        self.item_caught.check_pressed()
                else:
                    # si on a pas de hud on tej juste l'item
                    if not unstacked: self.del_caught_ui()
                    self.perso.drop(item)
                    if not unstacked: return -1

                if unstacked:
                    # on rattrape l'item caught sans
                    self.item_caught.catch()
                    return 2
        else:
            ## on check touu pour vwar si on en catch
            for k in self.uis:
                if self.uis[k] != None:
                    if butt == 'L':
                        self.uis[k].check_pressed()
                        if self.uis[k].caught:
                            self.item_caught = self.uis[k]
                            return 1
                    elif butt == 'R':
                        # ici on prend un seul item si on clik sur un truc
                        if self.uis[k]._hoover:
                            # ça veut dire qu'on catch cet self.uis[k]
                            # on vérifie cb de stack il a
                            if self.uis[k].item.stacked == 1:
                                self.uis[k].catch()
                                self.item_caught = self.uis[k]
                                return 1
                            elif self.uis[k].item.stacked > 1:
                                item = self.uis[k].item.unstack()
                                ui = Invent_UI(box(),item,self.visible)
                                ui.catch()
                                self.item_caught = ui
                                return 1

        return 0

    def quick_catch_and_drop(self):

        inventory = False
        item = self.item_caught.item

        if self.perso.zone_colli != None and isinstance(self.perso.zone_colli,o3.Zone_ACTIV) and self.perso.zone_colli.activated:

            if type(self.perso.zone_colli) == Lit and type(item).__name__ == 'Phase':
                self.del_caught_ui()
                self.perso.drop(item,create=False)
                self.perso.zone_colli.hud.write(item)

            elif type(self.perso.zone_colli) == Ordi and type(item).__name__ == 'Instru':
                self.del_caught_ui()
                self.perso.drop(item,create=False)
                self.perso.zone_colli.hud.inspect(item)

            elif type(self.perso.zone_colli) == Studio:

                if type(item).__name__ == 'Phase' and self.perso.zone_colli.hud.phases < 4:
                    self.del_caught_ui()
                    self.perso.drop(item,create=False)
                    self.perso.zone_colli.hud.catch(item)

                elif type(item).__name__ == 'Instru' and self.perso.zone_colli.hud.instru == 0:
                    self.del_caught_ui()
                    self.perso.drop(item,create=False)
                    self.perso.zone_colli.hud.catch(item)

                else:
                    inventory = True

            else:
                inventory = True

        else:
            inventory = True

        if inventory:
            self.del_caught_ui()
            self.perso.drop(item,False)
            self.perso.grab(item,True)
            return -1


    ## catch drop self
    def catchable(self,item):
        return True
    def catch_item(self,item):
        self.perso.grab(item)
        return 1
    def drop_item(self,item,perso):
        perso.drop(item,False)
    def collision(self,x,y):
        if collisionAX(self.box.realbox,(x,y)):
            return True
        if collisionAX(self.box2.realbox,(x,y)):
            return True
        return False

    ## details

    def update_details(self,item=None):

        if item == None:
            for x in ['mid','up','bottom']:
                if self.details[x] != None:
                    g.lman.delete(self.details[x])
                    self.details[x] = None
        else:
            details = item.details()
            keys = ['mid','up','bottom']
            pos = [ (self.box.x+self.box.w/4,self.box.cy),
                    (self.box.x+self.box.w/4,self.box.cy+self.box.h/4),
                    (self.box.x+self.box.w/4,self.box.cy-self.box.h/4)]
            sizes = [20,12,12]

            for i in range(len(keys)):

                #print(i,keys[i],details)

                if self.details[keys[i]] != None and i >= len(details):
                    g.lman.delete(self.details[keys[i]])
                    self.details[keys[i]] = None
                elif self.details[keys[i]] == None and i < len(details):
                    self.details[keys[i]] = g.lman.addLab(details[i],pos[i],anchor = ('center','center'),group='hud21',font_size=sizes[i])
                elif i < len(details):
                    g.lman.set_text(self.details[keys[i]],details[i])


"""'''''''''''''''''''''''''''''''''
'''''''  UI ''''''''''''''''''''''''
'''''''''''''''''''''''''''''''''"""

#------# ui

class UI():

    ## HOOVER WITH MOVEMENT OF MOUSE

    def __init__(self,box2,lab_text='UIthg',textid='white',group='ui',makeCol=False,colorlab=c['coral']):

        if textid[:4] == 'text':
            self.text_id = textid
        elif makeCol:
            self.text_id = g.tman.addCol(textid)
        self.loaded = False

        self.box = box2
        self.group = group


        self.lab_text=lab_text
        self.visible = True
        self._hoover = False

        #print('LAB')

        # label
        x,y = self.box.cx , self.box.fy + 25
        self.label = g.lman.addLab(lab_text,(x,y),vis=False,anchor = ('center','center'),font_size=20,color=colorlab,group='ui')
        #print(x,y,g.lman.labels[self.label].content_width ,g.lman.labels[self.label].content_height)
        boxbg = box( cx=x,cy=y,w = g.lman.labels[self.label].content_width+20 , h = g.lman.labels[self.label].content_height+4 )
        self.label_bg = g.sman.addCol('black_faded',boxbg,group='ui-1',vis=False)

    def hoover(self):
        g.lman.unhide(self.label)
        g.sman.unhide(self.label_bg)
        self._hoover = True

    def unhoover(self):
        g.lman.unhide(self.label,True)
        g.sman.unhide(self.label_bg,True)
        self._hoover = False

    def delete(self):

        if hasattr(self,'skin_id'):
            g.sman.delete(self.skin_id)

        g.sman.delete(self.label_bg)
        g.lman.delete(self.label)

    def unhide(self,hide=False):
        # .unhide() affiche machin
        # .unhide(True) cache machin

        if hide:
            self.deload()
            g.lman.unhide(self.label,hide)
            g.sman.unhide(self.label_bg,hide)
        else:
            self.load()
        self.visible = not hide

    def load(self):

        if hasattr(self,'text_id') and not hasattr(self,'skin_id') :
            self.skin_id = g.sman.addSpr(self.text_id,self.box.xy,self.group,key='ui'+self.lab_text)
            w,h = g.sman.sprites[self.skin_id].width,g.sman.sprites[self.skin_id].height
            g.sman.modify(self.skin_id,scale=(self.box.w/w,self.box.h/h))

        self.loaded = True

    def deload(self):

        if hasattr(self,'skin_id'):
            g.sman.delete(self.skin_id)
            del self.skin_id

        self.loaded = False

    ##

    def check_mouse(self,x,y):

        if collisionAX(self.box.realbox,(x,y)):
            self.hoover()
            return True
        else:
            self.unhoover()
            return False

class Plume_UI(UI):

    def __init__(self,box,plume):

        lab_text = plume.owner+'\'s plume '#+o3.convert_quality(plume.quality)

        super(Plume_UI,self).__init__(box,lab_text,group='ui',makeCol=False,colorlab=c[o3.convert_quality(plume.quality)[0]])

        #self.plume = phase

class Life_UI(UI):

    def __init__(self,box,perso):
        self.perso = perso

        lab_text = 'vie : '+str(perso.life)+'/'+str(perso.max_life)

        super(Life_UI,self).__init__(box,lab_text,group='ui',makeCol=False,colorlab=c['lightred'])

    def update(self):

        g.lman.set_text(self.label,'vie : '+str(self.perso.life)+'/'+str(self.perso.max_life))
        boxbg = box( cx=self.box.cx,cy=self.box.fy + 25,w = g.lman.labels[self.label].content_width+20 , h = g.lman.labels[self.label].content_height+4 )
        g.sman.delete(self.label_bg)
        self.label_bg = g.sman.addCol('delta_blue',boxbg,group='ui-1',vis=self._hoover)

class Cred_UI(UI):

    def __init__(self,box,perso):
        self.perso = perso

        lab_text = 'cred : '+str(perso.cred)

        super(Cred_UI,self).__init__(box,lab_text,group='ui',makeCol=False,colorlab=c['lightblue'])

    def update(self):
        g.lman.set_text(self.label,'cred : '+str(self.perso.cred))
        boxbg = box( cx=self.box.cx,cy=self.box.fy + 25,w = g.lman.labels[self.label].content_width+20 , h = g.lman.labels[self.label].content_height+4 )
        g.sman.delete(self.label_bg)
        self.label_bg = g.sman.addCol('delta_blue',boxbg,group='ui-1',vis=self._hoover)

##

class Press_UI(UI):

    def __init__(self,box2,lab_text='UIthg',textid='white',group='ui',makeCol=False,longpress=False,colorlab=c['coral']):
        super(Press_UI,self).__init__(box2,lab_text,textid,group,makeCol,colorlab)
        self.longpress = longpress

    def check_pressed(self):

        if self._hoover:
            self.press()
            return True

    def press(self):
        pass

class Button(Press_UI):

    def __init__(self,box2,funct,param,lab_text='button',textid='delta_blue',vis=False,group='hud22',makeCol=True,longpress=False,colorlab=c['coral']):
        super(Button,self).__init__(box2,lab_text,textid,group,makeCol,longpress,colorlab)

        self.funct = funct
        self.param = param

    def press(self):
        #print(self.lab_text,'pressed',self.param)
        self.funct(*self.param)

class Toggle(Button):

    def __init__(self,box2,funct,param,lab_text='button',nap_color='delta_purple',act_color='delta_blue',vis=False,group='hud22'):
        super(Toggle,self).__init__(box2,funct,param,lab_text,nap_color,vis,group)
        self.nap_color = nap_color
        self.act_color = act_color

        self.nap = True

    def press(self):
        super(Toggle,self).press()
        #self.toggle()

    def toggle(self):

        if self.nap:
            col = self.act_color
        else:
            col = self.nap_color

        self.nap = not self.nap

        if hasattr(self,'skin_id'):
            g.sman.set_col(self.skin_id,col)
        else:
            self.text_id = g.tman.addCol(col)

    def set_nap(self):
        self.nap = True
        if hasattr(self,'skin_id'):
            g.sman.set_col(self.skin_id,self.nap_color)
        else:
            self.text_id = g.tman.addCol(self.nap_color)

    def set_act(self):
        self.nap = False
        if hasattr(self,'skin_id'):
            g.sman.set_col(self.skin_id,self.act_color)
        else:
            self.text_id = g.tman.addCol(self.act_color)


#---------# item_ui -> item transportable entre les menus

class Item_UI(Press_UI):

    def __init__(self,item,box,lab_text,texture,spr_vis=False,colorlab=c['F'],scale=(0.25,0.25)):

        super(Item_UI,self).__init__(box,lab_text,group='ui',colorlab=colorlab)

        self.item = item
        self.item_group = 'hud21'

        self.itemspr = g.sman.addSpr(texture,group=self.item_group,vis=spr_vis,key='uiitem_'+self.lab_text)
        self.scale = scale
        g.sman.modify(self.itemspr,scale=scale)

        pos = box.cx - g.sman.spr(self.itemspr).width/2 , box.cy - g.sman.spr(self.itemspr).height/2
        g.sman.modify(self.itemspr,pos)

        self.caught = False
        self.dropped = False

        self.scale = scale

        self.stacked = 1

    def modify(self,sc=None,group=None,size=None):

        if sc == None:
            sc = self.scale

        if size == None or g.sman.spr(self.itemspr).width == size[0]:
            size=None

        g.sman.modify(self.itemspr,scale=sc,group=group,size=size)

        if hasattr(self,'stackspr') :
            g.sman.modify(self.stackspr,scale=sc,group=group,size=size)

        self.box = g.sman.box(self.itemspr)

    def catch(self):
        self.caught = True
        self.dropped = False
        self.modify((self.scale[0]*2,self.scale[1]*2),'ui-1')

        pos = self.box.cx , self.box.fy + 20
        g.lman.modify(self.label,pos)
        pos = self.box.cx - g.lman.labels[self.label].content_width/2 - 5, self.box.fy + 15
        g.sman.modify(self.label_bg,pos)

        self.update()

    def drop(self):
        self.dropped = True
        self.caught = False
        self.modify(group=self.item_group)

    def move(self,x,y):
        self.box.xy = x-g.sman.spr(self.itemspr).width/2,y-g.sman.spr(self.itemspr).height/2
        self.update()

    def upbox(self,box):
        self.box = box
        self.update()

    def update(self):

        if self.stacked != self.item.stacked:
            if self.item.stacked == 1 and hasattr(self,'stackspr'):
                g.sman.delete(self.stackspr)
                del self.stackspr
            elif self.item.stacked != 1 and not hasattr(self,'stackspr'):
                self.stackspr = g.sman.addSpr(g.TEXTIDS['nbs'][self.item.stacked],group='hud22',vis=g.sman.spr(self.itemspr).visible,key='uiitem_stack_'+self.lab_text)

            elif self.item.stacked != 1:
                g.sman.set_text(self.stackspr,g.TEXTIDS['nbs'][self.item.stacked])
            self.stacked = self.item.stacked

        if hasattr(self,'stackspr'):
            g.sman.modify(self.stackspr,size=(g.sman.spr(self.itemspr).width,g.sman.spr(self.itemspr).width))

        if self.caught:
            # itemspr
            g.sman.unhide(self.itemspr)
            if hasattr(self,'stackspr'): g.sman.unhide(self.stackspr)

        g.sman.modify(self.itemspr,self.box.cxy,anchor='center')
        if hasattr(self,'stackspr'): g.sman.modify(self.stackspr,self.box.cxy,anchor='center')

        # label
        pos = self.box.cx , self.box.fy + 20
        g.lman.modify(self.label,pos)
        # labelbg
        boxbg = box( cx=self.box.cx,cy=self.box.fy + 25,w = g.lman.labels[self.label].content_width+20 , h = g.lman.labels[self.label].content_height+4 )
        g.sman.modify(self.label_bg,boxbg.xy)

    def delete(self):
        super(Item_UI,self).delete()
        g.sman.delete(self.itemspr)
        if hasattr(self,'stackspr'):
            g.sman.delete(self.stackspr)
            del self.stackspr

    def press(self):
        if self.caught:
            self.drop()
        else:
            self.catch()

    def unhide(self,hide=False):

        if hasattr(self,'stackspr'):
            g.sman.unhide(self.stackspr,hide)

        g.sman.unhide(self.itemspr,hide)
        if hide:
            g.lman.unhide(self.label,hide)
            g.sman.unhide(self.label_bg,hide)
        self.visible = not hide

class Writingphase_UI(Item_UI):

    def __init__(self,box,phase):

        lab_text = 'Phase '+o3.convert_quality(phase.quality)+'\n' +phase.them

        super(Writingphase_UI,self).__init__(phase,box,lab_text,g.TEXTIDS['phase'][o3.convert_quality(phase.quality)[0]],colorlab=c[o3.convert_quality(phase.quality)[0]])

class Invent_UI(Item_UI):

    def __init__(self,box,item,spr_vis=False,scale=None):
        #print(spr_vis)

        cquecé = type(item).__name__
        col = c['F']

        if isinstance(item,o3.Sound_item):
            lab_text = cquecé +' '+ o3.convert_quality(item.quality)
            col = c[o3.convert_quality(item.quality)[0]]
            text = g.TEXTIDS[cquecé.lower()][o3.convert_quality(item.quality)[0]]
            if not scale : scale = (0.25,0.25)

            if cquecé == 'Phase':
                lab_text+='\n'+item.them
        else:
            lab_text = cquecé.lower()
            text = g.TEXTIDS['items'][cquecé.lower()]
            if not scale : scale = (0.25,0.25)

        super(Invent_UI,self).__init__(item,box,lab_text,text,spr_vis=spr_vis,colorlab=col,scale=scale)


        #self.boxdeta = box_details

    def __lt__(self, other):
         return self.item.quality < other.item.quality
