"""
CODED by deltasfer
enjoy
"""

import json,os,time
from colors import *

from src.utils import *
from src import graphic as g
from src import obj as o
from src import perso as p
import random as r
from src import cmd

Y = 0,450
Y_BUILD = 250
#maxY = 300
W_BUILD = 1500
W_BACK = 100
H_BUILD = 830
W_SIDE = 800

"""'''''''''''''''''''''''''''''''''
'''''''PART ONE : STREETS'''''''''''
'''''''''''''''''''''''''''''''''"""

class Train():

    def __init__(self,circuit,pos,name='sbahn'):

        # general
        self.name = name
        self.circuit = circuit # ex : ['kamour str','street 1','street 3']
        self.station_x = pos # gex de l'arret pour chaque rue : [10230,28000,6200]

        for street in self.circuit:
            NY.CITY[street].set_station(Station(street,self))

        self.max_speed = 300
        self.realspeed = self.max_speed
        self.stopped_here = False
        self.ready_to_go = False
        self.stop_time = 4
        self.brake_dist = W_BUILD

        # passengers
        self.passengers = []
        self.perso_on_board = False

        #pos
        self.y = Y_BUILD+230
        self.x = 0
        #print(name,'created :',str(circuit))

        #position
        self.gex = self.station_x[-2]
        self.gey = self.y
        self.street = self.circuit[-2]

        #sprite
        self.text = g.TEXTIDS['sbahn'][0]
        self.anim_text = g.TEXTIDS['sbahn'][1:] + [g.TEXTIDS['sbahn'][-1]] + list(reversed(g.TEXTIDS['sbahn']))
        self.anim_time = [ 0.1 for _ in g.TEXTIDS['sbahn'][1:]] + [self.stop_time] + [ 0.1 for _ in list(reversed(g.TEXTIDS['sbahn']))]
        self.anim = None

        #zones

        self.exits = [
                    {'dx':-260,'arrival':'back','y':self.y},
                    {'dx':260,'arrival':'back','y':self.y}
                    ] # par rapport au centre
        self.zones_box = [
                        {'dx':-260},
                        {'dx':260},
                        {'dx':0}
                            ]

        y = self.y
        self.zones = []
        zone_box = box( y=y , w=200 , h=self.y+200 - y )
        self.zones.append(o.TrainStation(self,zone_box))
        zone_box = box( y=y , w=200 , h=self.y+200 - y )
        self.zones.append(o.TrainStation(self,zone_box))
        zone_box = box( y=y , w=600 , h=self.y+200 - y )
        self.zones.append(o.ExitTrain(self,zone_box))

    def update(self,x,y):

        ## bouge le train

        self.move()

        ## verifie si y'a besoin d'afficher le spr ou non:

        self.x = x+self.gex
        if NY.CITY[self.street].visible and (self.x+self.w > -g.SAFE_W and self.x < g.scr.fx+g.SAFE_W):

            if not hasattr(self,'spr'):
                # on load le sprite
                self.spr = g.sman.addSpr(self.text,group='sbahn')
                #time.sleep(2)
                g.Cyc.add_spr((self.spr,0.5))
                if self.anim:
                    self.anim.set_id(self.spr)

            # on le place bieng
            g.sman.modify(self.spr,(self.x,self.y))
        elif hasattr(self,'spr'):
            # on deload
            g.Cyc.del_spr((self.spr,0.5))
            g.sman.delete(self.spr)
            del self.spr

    # movin

    def tp(self,x):
        self.gex = x
        if self.perso_on_board and self.gfx >= NY.CITY[self.street].gfx:
            self.move_street()
        elif self.gex >= NY.CITY[self.street].gfx:
            self.move_street()

    def move(self):

        spd = self.speed
        self.realspeed = spd
        self.gex += spd
        if self.perso_on_board and self.gfx >= NY.CITY[self.street].gfx:
            self.move_street()
        elif self.gex >= NY.CITY[self.street].gfx:
            self.move_street()

    def move_street(self):

        i = self.circuit.index(self.street)

        if i >= len(self.circuit) - 1: i = 0
        else: i+= 1

        self.street = self.circuit[i]
        self.gex = NY.CITY[self.street].box.x
        if not self.perso_on_board:
            self.gex -= self.w
        self.stopped_here = False
        self.ready_to_go = False

        #print(color(self.name+' entering '+self.street,'yellow'))
        cmd.colorsay('cyan',self.name,'entering',self.street)

    # zone

    def activ_zone(self):
        #print(cyan('activin zones'))
        for i in range(len(self.zones)):
            x = self.station_x[self.circuit.index(self.street)]+self.zones_box[i]['dx']
            self.zones[i].move(x,anc='center')
            NY.CITY[self.street].add_zone(self.zones[i])

    def unactiv_zone(self):
        #print(cyan('unactivin zones'))
        for zone in self.zones:
            NY.CITY[self.street].del_zone(zone)

    # takin people
    def add_pass(self,hum):
        if hum not in self.passengers:
            self.passengers.append(hum)
            if type(hum) == p.Perso:
                self.perso_on_board = True

    def del_pass(self,hum):
        if hum in self.passengers:
            self.passengers.remove(hum)
            if type(hum) == p.Perso:
                for perso in self.passengers:
                    if type(perso) == p.Perso:
                        return
                self.perso_on_board = False

    ##
    def _gfx(self):
        return self.gex + self.w
    gfx = property(_gfx)
    def _gcx(self):
        return self.gex + self.w/2
    gcx = property(_gcx)
    def _w(self):
        return g.tman.textures[self.text].width
    w = property(_w)

    def _realbox(self):
        if hasattr(self,'spr'):
            return g.sman.realbox(self.spr)
        else:
            return 0,0,self.text.width,self.text.height
    realbox = property(_realbox)

    def _at_station(self):
        return (self.stopped_here and not self.ready_to_go)
    at_station = property(_at_station)

    def _speed(self):

        s = self.max_speed

        x_arret = self.station_x[self.circuit.index(self.street)]
        if x_arret == None:
            return s

        if abs(self.gcx - x_arret) <= 1:

            if not self.anim and not self.stopped_here:

                self.stopped_here = True
                self.activ_zone()
                #cmd.colorsay('cyan',self.name,'stopped')

                ## On vient d'arriver les portes doivent s'ouvrir
                if not hasattr(self,'spr'):
                    self.anim = g.Anim(None,self.anim_text,self.anim_time)
                else:
                    self.anim = g.Anim(self.spr,self.anim_text,self.anim_time)

            elif self.anim and not self.anim.running and not self.ready_to_go:

                ## les portes sont fermées, on repart
                #del self.anim
                #self.anim = None
                self.unactiv_zone()
                self.ready_to_go = True
                self.anim = None
                return 0.1

            elif self.ready_to_go:
                return 0.1

            return 0
        elif self.gcx < x_arret and self.gcx > x_arret - self.brake_dist:
            d = (x_arret - self.gcx) / self.brake_dist
            #print('avant :',d,self.gcx,x_arret,self.brake_dist)
            return d*s
        elif self.gcx > x_arret and self.gcx < x_arret + self.brake_dist:
            d = (self.gcx - x_arret) / self.brake_dist
            #print('apr :',d)
            return d*s

        return s
    speed = property(_speed)

class Station():

    def __init__(self,street,train):

        self.street = street
        self.train = train
        self.name = street

        # times
        self.moy_dt = 0
        self.rec_times = []
        #self.lab =

    def update(self):

        if self.train.street == self.street and self.train.at_station:
            #
            if self.rec_times == [] or time.time() - 2*self.train.stop_time > self.rec_times[-1]:
                 self.rec_times.append(time.time())

        self.rec_dt = []
        for i in range(len(self.rec_times) - 2):
            self.rec_dt.append(self.rec_times[i+1]-self.rec_times[i])
        if len(self.rec_dt) > 0 :
            self.moy_dt = sum(self.rec_dt)/len(self.rec_dt)

            dt = self.rec_times[-1] + self.moy_dt - time.time()


# lines

class preStreet(line):

    def __init__(self,name,xd=0,yd=0,xf=0,yf=0,connex=[]):

        super(preStreet,self).__init__(xd,yd,xf,yf)
        self.name = name

        self.connex = connex

    def add_conn(self,street,x):
        self.connex.append((street.name,x))

class preRue(line):

    def __init__(self,nom,x,y,long=0,vert=False):

        if vert:
            super(preRue,self).__init__(x,y,x,y+long)
        else:
            super(preRue,self).__init__(x,y,x+long,y)

        self.name = nom
        self.long = long
        self.cont = [0 for i in range(self.long)]
        self.connex = []

    def empl_rd_door(self):

        i = r.randint(1,self.long-2)
        while self.cont[i] != 0:
            i = r.randint(1,self.long-2)

        return i

    def place_door(self,x,nom):
        self.cont[x] = nom
        self.connex.append((nom,x))

    def place_door_rd(self,nom):

        x = self.empl_rd_door()
        self.place_door(x,nom)
        return x

    def get_pos(self,n):

        # n le numéro du batiment de la rue
        if self.long == 0:
            return self.x,self.y
        else:
            if self.vert:
                return self.x,self.y + n
            else:
                return self.x+n,self.y

    def __repr__(self):

        s = self.name + red(' -> ')

        for x in self.cont:
            if x == 0:
                s += '. '
            else:
                s+=x+ ' '

        return s+'\n'

    def _nb_voisins(self):

        n = 0
        for x in self.cont:
            if x != 0:
                n+=1
        return n
    nb_voisins = property(_nb_voisins)

## streets

class Street():

    def __init__(self,preStreet,textures={},buildings=None,box=box(0,-50,None)):

        self.textures = textures
        self.build_list = buildings

        # self.textures['back'] = img/None
        # self.textures['front'] = img/None
        # self.textures['frontanim'] = img/None
        # self.textures['backanim'] = img/None
        # self.textures['road'] = img/None

        self.outside = True
        self.free_access = True


        self.cursor_anim = 0

        self.box = box
        self._x,self._y = self.box.xy

        self.name = preStreet.name
        self.line = preStreet.line
        self.pre = preStreet

        self.zones = {}
        self.humans = []
        self.items = []


        self.neighbor = {}
        self.neighbors_street = {}

        self.visible = False

        self.catalog = [] ## ce tableau est un tableau ordonné selon les X contenant tous les éléments et leurs détails:
                            # x y type nom

        self.Y = Y
        self.Y_AVERAGE = Y_BUILD # y où vont arriver les bots qui se tp ici

    def update(self,x,y):

        self.y = y+self.box.y
        self.x = x+self.box.x

        if hasattr(self,'station'):
            self.station.update()

        #zones/items
        if True:
            #zones
            for zone in self.zones:
                zone=self.zones[zone]
                x_r = zone.gex + x
                y_r = zone.gey + y
                zone.update(x_r,y_r)

                # load/deload
                if (x_r+zone.w <= -g.SAFE_W or x_r >= g.scr.fx+g.SAFE_W) and zone.loaded:
                    zone.deload()
                elif (x_r+zone.w > -g.SAFE_W and x_r < g.scr.fx+g.SAFE_W) and not zone.loaded:
                    zone.load(self)

            #items
            for item in self.items:
                x_r = item.gex + x
                y_r = item.gey + y
                item.update(x_r,y_r)

                # load/deload
                if (x_r+item.w <= -g.SAFE_W or x_r >= g.scr.fx+g.SAFE_W) and item.loaded:
                    item.deload()
                elif (x_r+item.w > -g.SAFE_W and x_r < g.scr.fx+g.SAFE_W) and not item.loaded:
                    item.load(self)

        # bg
        if True:
            if hasattr(self,'streetbg'):
                g.sman.spr(self.streetbg).x = self.x
            if hasattr(self,'streetfg'):
                g.sman.spr(self.streetfg).x = self.x
            if hasattr(self,'streetanimfg'):
                g.sman.spr(self.streetanimfg).x = self.x
            if hasattr(self,'streetanimbg'):
                g.sman.spr(self.streetanimbg).x = self.x

        # builds + sides
        if True:
            if hasattr(self,'builds'):

                # check chaque batiment pour voir s'il est dans l'écran safe afin de le load/deload en fonction
                for i in range(len(self.builds)):

                    x_r = self.x+W_SIDE+i*W_BUILD
                    w_r = W_BUILD+W_BACK

                    # load/deload
                    if (x_r+w_r <= -g.SAFE_W or x_r >= g.scr.fx+g.SAFE_W) and (self.builds[i] != None):
                        self.deload_build(i)
                    elif (x_r+w_r > -g.SAFE_W and x_r < g.scr.fx+g.SAFE_W) and (self.builds[i] == None):
                        self.load_build(i)
                    elif self.builds[i] != None:
                        g.sman.spr(self.builds[i]).x = x_r
                        g.sman.spr(self.backbuilds[i]).x = x_r+W_BUILD

            if hasattr(self,'side'):

                ## side L
                x_r = self.x
                w_r = W_SIDE+W_BACK

                if (x_r+w_r <= -g.SAFE_W or x_r >= g.scr.fx+g.SAFE_W) and (self.side['L'] != None):
                    self.deload_build('L')
                elif (x_r+w_r > -g.SAFE_W and x_r < g.scr.fx+g.SAFE_W) and (self.side['L'] == None):
                    self.load_build('L')
                elif self.side['L'] != None:
                    g.sman.spr(self.side['L']).x = x_r
                    g.sman.spr(self.backside['L']).x = x_r+W_SIDE

                ## side R
                x_r = self.x+W_SIDE+self.pre.long*W_BUILD
                w_r = W_SIDE+W_BACK

                if (x_r+w_r <= -g.SAFE_W or x_r >= g.scr.fx+g.SAFE_W) and (self.side['R'] != None):
                    self.deload_build('R')
                elif (x_r+w_r > -g.SAFE_W and x_r < g.scr.fx+g.SAFE_W) and (self.side['R'] == None):
                    self.load_build('R')
                elif self.side['R'] != None:
                    g.sman.spr(self.side['R']).x = x_r
                    g.sman.spr(self.backside['R']).x = x_r+W_SIDE

        # road
        if hasattr(self,'road1') and hasattr(self,'road2'):
            self.verify_endless_road()

    def collision(self,thg=0,dir=0,spd=0,light=False,return_box=False,thg_box=None):

        ## vérifie si une box entre en collision avec les boxs des éléments de la street
        #if type(thg) == p.Perso : cmd.say(self.Y)

        if not thg_box:

            ## vérifie les bords de la street
            if dir == 'L' and thg.gx - spd < self.box.x:
                if not return_box: return True
            elif dir == 'R' and thg.gfx + spd > self.box.fx:
                if not return_box: return True
            elif dir == 'up' and thg.gey + spd > self.Y[1]:
                if not return_box: return True
            elif dir == 'down' and thg.gey - spd < self.Y[0]:
                if not return_box: return True

            if light:
                if not return_box: return False


            thg_box = thg.collbox
            #thg_old_box = thg.collbox

            if dir == 'R':
                thg_box[0] += spd
                thg_box[2] += spd
            elif dir == 'L':
                thg_box[0] -= spd
                thg_box[2] -= spd
            if dir == 'up':
                thg_box[1] += spd
                thg_box[3] += spd
            elif dir == 'down':
                thg_box[1] -= spd
                thg_box[3] -= spd

        ## vérifie les zones_elems
        for zone in self.zones.values():
            if zone.loaded and collisionAB(zone.gebox,thg_box):
                if return_box:return zone.gebox
                return True

        ## vérifie les zones des builds où on est
        if self.build_list:
            build = self.get_build_x(thg_box[0])
            dx = 0
            if type(build) != type('aa'):
                dx += build*W_BUILD+W_SIDE
                build = self.build_list[int(build)]
            elif build == 'R':
                dx += self.pre.w*W_BUILD+W_SIDE
            #if type(thg) == p.Perso : cmd.say(build)
            for gbox in coll_boxs[build]:
                rbox = gbox.realbox
                rbox[0]+= dx
                rbox[2]+= dx
                if collisionAB(rbox,thg_box):
                    if return_box:return rbox
                    return True

            if build != self.get_build_x(thg_box[2]):
                # on vérifie les box de la fin du spr
                if build == 'L':
                    dx += W_SIDE
                else:
                    dx += W_BUILD

                build = self.get_build_x(thg_box[2])
                if type(build) != type('aa'):
                    build = self.build_list[int(build)]

                for gbox in coll_boxs[build]:
                    rbox = gbox.realbox
                    rbox[0]+= dx
                    rbox[2]+= dx
                    if collisionAB(rbox,thg_box):
                        if return_box:return rbox
                        return True

        if return_box: return None
        return False


    def assign_zones(self,zones):
        for zone in zones:
            self.add_zone(zone)

    def add_zone(self,zone):
        self.zones[zone.name] = zone
        #print('added zone',zone.name,zone.gex,zone.gey)

        if isinstance(zone,o.Porte) and zone.destination not in self.neighbor:
            self.neighbor[zone.destination] = {'door':zone}
            if type(zone.destination) == Street:
                self.neighbors_street[zone.destination] = {'door':zone}

    def del_zone(self,zone):
        if zone.name in self.zones and zone == self.zones[zone.name]:
            if zone.loaded:
                zone.deload()
            del self.zones[zone.name]

    def add_item(self,item):
        if type(item) == type([]):
            for ite in item:
                self.items.append(ite)
                #if self.visible:
                #    ite.load(self)
        else:
            self.items.append(item)
            #if self.visible:
            #    item.load(self)

    def del_item(self,item):
        if item in self.items:
            self.items.remove(item)
            if item.loaded:
                item.deload()

    def add_hum(self,hum):

        if type(hum) == type([]):
            for h in hum:
                self.humans.append(h)
                #if self.visible:
                #    h.load()
        else:
            self.humans.append(hum)
            #if self.visible:
            #    hum.load()

    def del_hum(self,hum):
        if hum in self.humans:
            self.humans.remove(hum)
            if hum.loaded:
                hum.deload()

    def set_station(self,station):
        self.station = station

    # loadin/update

    def deload(self):

        g.bertran.unschedule(self.anim)
        g.Cyc.empty_plus()

        ## road
        if hasattr(self,'road1') and hasattr(self,'road2'):
            g.sman.delete(self.road1)
            del self.road1
            g.sman.delete(self.road2)
            del self.road2
        ## build
        if hasattr(self,'builds'):
            for i in range(len(self.builds)):
                self.deload_build(i)
        ## side
        if hasattr(self,'side'):
            self.deload_build('L')
            self.deload_build('R')


        ## back front /back front anim
        if hasattr(self,'streetbg'):
            g.sman.delete(self.streetbg)
            del self.streetbg
        if hasattr(self,'streetfg'):
            g.sman.delete(self.streetfg)
            del self.streetfg
        if hasattr(self,'streetanimbg'):
            g.sman.delete(self.streetanimbg)
            del self.streetanimbg
        if hasattr(self,'streetanimfg'):
            g.sman.delete(self.streetanimfg)
            del self.streetanimfg

        ## elements
        for zone in self.zones:
            self.zones[zone].deload()

        for h in self.humans:
            h.deload()

        for item in self.items:
            item.deload()

        self.visible = False

    def load(self):

        ## road
        if 'road' in self.textures:
            self.road1 = g.sman.addSpr(self.textures['road'],self.box.xy,group='road')
            w = g.sman.spr(self.road1).width
            self.road2 = g.sman.addSpr(self.textures['road'],(self.x+w,self.y),group='road')
            self.roaddx = 0

            g.Cyc.add_spr((self.road1,0.3))
            g.Cyc.add_spr((self.road2,0.3))

        ## buildings
        if self.build_list:

            #avant/back
            self.builds = [None for _ in self.build_list]
            self.backbuilds = [None for _ in self.build_list]

            self.side = {'L':None,'R':None}
            self.backside = {'L':None,'R':None}

        ## back front /back front anim
        if 'back' in self.textures:
            self.streetbg = g.sman.addSpr(self.textures['back'],self.box.xy,group='backstreet')
        if 'front' in self.textures:
            self.streetfg = g.sman.addSpr(self.textures['front'],self.box.xy,group='frontstreet')
        if 'backanim' in self.textures:
            self.streetanimbg = g.sman.addSpr(self.textures['backanim'][0],self.box.xy,group='backstreet_anim')
        if 'frontanim' in self.textures:
            self.streetanimfg = g.sman.addSpr(self.textures['frontanim'][0],self.box.xy,group='frontstreet_anim')

        if 'backanim' in self.textures or 'frontanim' in self.textures:
            g.bertran.schedule_interval_soft(self.anim,0.1)

        nbh = len(self.humans)
        for street in self.neighbor:
            nbh += len(street.humans)

        print(green(self.name),blue('('+str(self.long)+' blocks)'),green(':  '+str(len(list(self.zones))) + ' zones --- ' + str(len(self.humans)) + ' humans --- ' + str(len(self.items)) + ' items loaded'),blue('('+str(nbh)+' humans)'))
        #print([x.name for x in self.neighbor])


        self.visible = True
        self.update_catalog()

    def load_build(self,i):

        # 'L' load la side gauche
        # i load le bat i
        # 'R' load la side droite

        ## buildings
        if self.build_list:

            x,y = self.x,Y_BUILD

            if i == 'L':
                self.side['L'] = g.sman.addSpr(g.TEXTIDS['build']['L'],(x,y),group='buildings')
                self.backside['L'] = g.sman.addSpr(g.TEXTIDS['backbuild']['L'],(x+W_SIDE,y),group='road')
                g.Cyc.add_spr((self.side['L'],0.3))
                g.Cyc.add_spr((self.backside['L'],0.3))
                #print('oh ya')

            elif i == 'R':
                x += W_SIDE+self.pre.long*W_BUILD
                self.side['R'] = g.sman.addSpr(g.TEXTIDS['build']['R'],(x,y),group='buildings')
                self.backside['R'] = g.sman.addSpr(g.TEXTIDS['backbuild']['R'],(x+W_SIDE,y),group='road')
                g.Cyc.add_spr((self.side['R'],0.3))
                g.Cyc.add_spr((self.backside['R'],0.3))

            elif i >= 0 and i < len(self.build_list):

                x += W_SIDE+i*W_BUILD
                w = W_BUILD

                build = self.build_list[i]
                id = g.sman.addSpr(g.TEXTIDS['build'][builds[build]['text']],(x,y),group='buildings')
                backid = g.sman.addSpr(g.TEXTIDS['backbuild'][builds[build]['text']],(x+w,y),group='road')
                self.builds[i] = id
                self.backbuilds[i] = backid
                g.Cyc.add_spr((id,0.3))
                g.Cyc.add_spr((backid,0.3))

    def deload_build(self,i):

        # 'L' deload la side gauche
        # i deload le bat i
        # 'R' deload la side droite

        if hasattr(self,'builds'):

            if i == 'L':
                #print('oh yo')
                if self.side['L'] != None:
                    g.Cyc.del_spr((self.side['L'],0.3))
                    g.sman.delete(self.side['L'])
                    self.side['L'] = None
                    g.Cyc.del_spr((self.backside['L'],0.3))
                    g.sman.delete(self.backside['L'])
                    self.backside['L'] = None
            elif i == 'R':
                if self.side['R'] != None:
                    g.Cyc.del_spr((self.side['R'],0.3))
                    g.sman.delete(self.side['R'])
                    self.side['R'] = None
                    g.Cyc.del_spr((self.backside['R'],0.3))
                    g.sman.delete(self.backside['R'])
                    self.backside['R'] = None
            elif i >= 0 and i < len(self.build_list) and self.builds[i] != None:
                g.Cyc.del_spr((self.builds[i],0.3))
                g.Cyc.del_spr((self.backbuilds[i],0.3))
                g.sman.delete(self.builds[i])
                self.builds[i] = None
                g.sman.delete(self.backbuilds[i])
                self.backbuilds[i] = None

    def update_catalog(self):
        self.catalog = []
        for zone in self.zones:
            self.catalog.append( {'x':self.zones[zone].box.cx,'y':self.zones[zone].box.cy,'type':'zone','nom':self.zones[zone].name,'elem':self.zones[zone]} )
        for hum in self.humans:
            self.catalog.append( {'x':hum.gex,'y':hum.gey,'type':'hum','nom':hum.name,'elem':hum} )
        for item in self.items:
            self.catalog.append( {'x':item.box.cx,'y':item.box.cy,'type':'item','nom':item.name,'elem':item} )

        self.catalog.sort(key=lambda x:x.get('x'))
        #print(self.catalog)


    # bots
    def rand_pos(self):
        x,y = random.randint(int(self.gex),int(self.gfx)-p.SIZE_SPR-1),random.randint(self.Y[0],self.Y_AVERAGE)
        return (x,y)

    def get_pos(self,hum):
        if hum in self.humans:
            #print(self.box.x)
            #gex = (hum.gex+p.SIZE_SPR/2) # position centrale du perso
            return (hum.gex-self.gex)/(self.box.w)

    def environ_lr(self,xl,xr):
        #print(xl,xr)
        if xl > xr :
            xr,xl=xl,xr

        il,ir = len(self.catalog)-1,0
        while il > 0 and self.catalog[il-1].get('x') > xl :
            il-=1
        while ir < len(self.catalog)-1 and self.catalog[ir+1].get('x') < xr :
            ir+=1

        #print(il,ir+1)

        elem = []
        for i in range(il,ir+1):
            elem.append(self.catalog[i])
        return elem

    def environ(self,elem,dx=1000):
        xl,xr=elem.gex-dx,elem.gex+dx

        il,ir = len(self.catalog)-1,0
        while il > 0 and self.catalog[il-1].get('x') > xl :
            il-=1
        while ir < len(self.catalog)-1 and self.catalog[ir+1].get('x') < xr :
            ir+=1

        elems = []
        for i in range(il,ir+1):
            if self.catalog[i].get('nom') != elem.name:
                elems.append(self.catalog[i])
        return elems

    def get_lil_colli(self,hum):

        ## donne juste les collisions des doors

        if hum in self.humans:
            collis = []
            for door in list(filter(lambda x:isinstance(x,o.Porte),list(self.zones.values()))):
                #print(door.name)
                if collisionAB(hum.gebox,door.gebox):
                    collis.append(door)
            return collis
        return []

    def get_random_nb_bots(self):
        return r.randint(self.long//8,self.long//4)

    def get_rd_neighbor(self):
        return r.choice([x for x in self.neighbor])

    def get_neighbor_door(self,street):
        if street in self.neighbor:
            return self.neighbor[street]['door']

    # anim
    def anim(self,dt):

        self.cursor_anim += 1
        if ('backanim' in self.textures and self.cursor_anim >= len(self.textures['backanim'])) or \
                ('frontanim' in self.textures and self.cursor_anim >= len(self.textures['frontanim'])):
            self.cursor_anim = 0

        if 'backanim' in self.textures:
            g.sman.set_text(self.streetanimbg,self.textures['backanim'][self.cursor_anim])
        if 'frontanim' in self.textures:
            g.sman.set_text(self.streetanimfg,self.textures['frontanim'][self.cursor_anim])

    # endless road and buildings
    def verify_endless_road(self):

        w = g.sman.spr(self.road1).width

        road1x = self.x + self.roaddx
        road2x = self.x + self.roaddx + w

        if road1x >= 0:
            self.roaddx -= w
        elif road2x + w <= g.scr.w:
            self.roaddx += w

        g.sman.modify(self.road1,(road1x,None))
        g.sman.modify(self.road2,(road2x,None))

    ## prerue
    def get_build_x(self,x):
        if self.build_list:
            #cmd.say(x,self.box.fx,self.box.fx-W_SIDE)
            if x < self.box.x + W_SIDE:
                return 'L'
            elif x >= self.box.fx - W_SIDE:
                return 'R'
            else:
                return (x-W_SIDE)//W_BUILD

    def get_build(self,x):
        if self.build_list:

            i = self.get_build_x(x)
            if i and i not in ['R','L']:
                print(i)
                i = self.build_list[int(i)]

            return i

    ###

    def _x(self):
        return self._x
    def _setx(self,x):
        self._x = x
    x = property(_x,_setx)

    def _rxf(self):
        if self.box.w == None:
            return None
        else:
            return self._x + self.box.w
    rxf= property(_rxf)

    def _y(self):
        return self._y
    def _sety(self,y):
        if hasattr(self,'streetbg'):
            g.sman.spr(self.streetbg).y = y
        if hasattr(self,'streetfg'):
            g.sman.spr(self.streetfg).y = y
        if hasattr(self,'streetanimfg'):
            g.sman.spr(self.streetanimfg).y = y
        if hasattr(self,'streetanimbg'):
            g.sman.spr(self.streetanimbg).y = y
        if hasattr(self,'road1'):
            g.sman.spr(self.road1).y = y
        if hasattr(self,'road2'):
            g.sman.spr(self.road2).y = y
        self._y = y
    y = property(_y,_sety)

    def _gex(self):
        return self.box.x
    gex = property(_gex)

    def _gfx(self):
        return self.box.x+self.box.w
    gfx = property(_gfx)

    def _xxf(self):
        if self.box.w == None:
            return (None,None)
        else:
            return (self.box.x,self.box.x+self.box.w)
    xxf = property(_xxf)

    def _yyf(self):
        return self.Y
    yyf = property(_yyf)

    def YY(self,gex):
        # return the actual Y at the gex pos
        if not self.build_list:
            return self.Y

        build = self.get_build(gex)
        maxY = builds[build]['maxY']
        if maxY:
            return self.Y[0],self.Y_AVERAGE+maxY
        else:
            return self.Y

    def _w(self):
        return self.box.w
    w = property(_w)

    def _long(self):
        if type(self.pre) == preStreet:
            return self.pre.w
        elif type(self.pre) == preRue:
            return self.pre.long
    long = property(_long)

    def _has_station(self):
        return (self.build_list and 'sbahn' in self.build_list)
    has_station = property(_has_station)


    ##

    def _range(self):
        if self.w:
            return self.x,self.x+self.w
        else:
            return self.x,infini
    range = property(_range)

    def __str__(self):

        s = '\n\n'+'\n\n'+'\n ---'+self.name+'---' +   str(self.line)   + '\n'
        s+= 'range : '+str(self.range)+'\n\n'

        s+='-zones\n'
        for zone in self.zones:
            zone = self.zones[zone]
            s+= '        '+zone.name+' : '+str((zone.box.x,zone.box.fx))+'\n'

        s+='-humains\n'
        for hum in self.humans:
            s+= '        '+hum.name+' : '+str((hum.box.x,hum.box.fx))+'\n'

        s+='-items\n'
        for item in self.items:
            s+= '        '+item.name+' : '+str((item.box.x,item.box.fx))+'\n'

        s+='\n'+ str(len(list(self.zones))) + ' zones ---'+str(len(self.humans)) + ' humans ---' + str(len(self.items)) + ' items'

        return s

    def __repr__(self):

        nbh = len(self.humans)
        for street in self.neighbor:
            nbh += len(street.humans)

        s = self.name + ' (' +str(self.long)+' blocks) :  '+str(len(list(self.zones)))
        s +=' zones --- ' + str(len(self.humans)) + ' humans --- ' + str(len(self.items))
        s +=' items ('+str(nbh)+' humans)'
        print(s)
        return s

class Building(Street):

    def __init__(self,name='bat1',textures={},box=box(0,-50,5120)):
        super(Building,self).__init__(name,textures,box=box)

        self.Y = (50,200)
        self.Y_AVERAGE = self.Y[1]
        self.houses = []

        self.outside = False
        self.free_access = False

    def add_house(self,house):
        self.houses.append(house)
        house.set_building(self)

    def get_random_nb_bots(self):
        return r.randint(0,2)

class House(Street):

    def __init__(self,name='house1',textures={},box=box(-1400,-50,5120)):
        super(House,self).__init__(name,textures,box=box)

        self.owners = []
        self.Y = (50,200)
        self.Y_AVERAGE = self.Y[1]


        self.outside = False
        self.free_access = False

        self.building = None

    def add_owner(self,owner):
        self.owners.append(owner)
        owner.grab(o.Key(self))

    def get_random_nb_bots(self):
        return r.randint(0,2)

    def set_building(self,build):
        self.building = build

class PrivateHouse(House):
    pass

class SpecialHouse(House):
    pass

class Shop(House):

    def __init__(self,name='shop1',textures={},box=box(0,-50,5120)):
        super(Shop,self).__init__(name,textures,box=box)

        self.guys = []
        self.Y = (50,150)
        self.Y_AVERAGE = self.Y[1]

        self.outside = False
        self.free_access = True

    def create_guys(self):
        text = random.choice(['perso','perso2','perso3'])
        self.add_guy(p.Guy(text,workplace=self.name))

    def add_guy(self,guy):
        if guy not in self.guys:
            self.guys.append(guy)
            if self.visible:
                guy.load()

    def del_guy(self,guy):
        if guy in self.guys:
            self.guys.remove(guy)
            if self.visible:
                guy.deload()

    def update_catalog(self):
        for guy in self.guys:
            if not guy.alive:
                print('wtf alphonse mort')
                exp = guy.name + ' est mort wtf'
                g.pman.alert(exp)
                self.guys.remove(guy)
        super(Shop,self).update_catalog()

    def get_random_nb_bots(self):
        return r.randint(1,3)

class Distrokid(Shop):

    def __init__(self,x,y):

        super(Distrokid,self).__init__(preRue('distrokid',x,y),g.TEXTIDS['distrokid'],box=box(0,-50,5120))

    def create_guys(self):
        text = random.choice(['perso','perso2','perso3'])
        self.add_guy(p.Guy(text,workplace=self.name,metier=p.Distroguy))

class MiniMarket(Shop):

    def __init__(self,x,y):
        super(MiniMarket,self).__init__(preRue('shop',x,y),g.TEXTIDS['shop'],box=box(0,-50,6400))

    def get_random_nb_bots(self):
        return r.randint(2,5)

    def create_guys(self):
        text = random.choice(['perso','perso2','perso3'])
        self.add_guy(p.Guy(text,workplace=self.name,metier=p.Shopguy))


"""'''''''''''''''''''''''''''''''''
'''''''PART TWO : CITY '''''''''''''
'''''''''''''''''''''''''''''''''"""

class CITY():

    def __init__(self):
        self.width = 0
        self.CITY = {}
        self.name = 'New York bitch'

        self.BAHN = {}
        #self.Ghost = Street(preStreet('ghost',1,1,2,1),box=box(0,-50,50))

    def add_streets(self,street):
        if type(street) == []:
            for stree in street:
                self.add_streets(stee)
        else:
            self.CITY[street.name] = street
            self.width += street.w

    def percentage(self,street):
        return street.w / self.w

    def rd_street(self):
        #print(list(self.CITY.values()))
        street = r.choice( list(self.CITY.values()))
        return street

    def rd_house(self):

        house = r.choice( list(filter( lambda x:isinstance(x,PrivateHouse),self.CITY.values())) )
        return house

    def rd_avnue(self):
        return r.choice(self.avnues)

    ## dij

    def create_node_graph(self):

        self.node_graph = {}

        for st in self.avnues:
            doors = list(map(lambda x:x['door'],list(st.neighbors_street.values())))
            doors = sorted(doors,key=lambda x:x.gex)
            for i in range(len(doors)):

                #print(doors[i].node)
                if doors[i].node not in self.node_graph:
                    self.node_graph[doors[i].node] = {}

                if i > 0:
                    self.node_graph[doors[i].node][doors[i-1].node] = doors[i].gex - doors[i-1].gex
                if i < len(doors)-1:
                    self.node_graph[doors[i].node][doors[i+1].node] = doors[i+1].gex - doors[i].gex

        if False:
            for node in self.node_graph:
                print(node)
                for noode in self.node_graph[node]:
                    print('   ',noode, '      ',self.node_graph[node][noode])

    def shortest_path(self,dep,dest):

        #print('lookin for shortest path :',dep.name,'->',dest.name)

        ## 1e étape : on crée le graph des rues
        self.create_node_graph()
        graph = self.node_graph

        ## 2e étape : on prend la rue de départ et la rue d'arrivée (si dep et dest != Street)
        begin = [dep.name]
        if type(dep) != Street:
            if isinstance(dep,PrivateHouse):
                if dep.building != None:
                    begin.append(dep.building.name)
                    dep = dep.building
                else:
                    print('DIJ error : la privatehouse de dep n a pas de building')
                    return []
            if isinstance(dep,Shop):
                if dep.building != None:
                    begin.append(dep.building.name)
                    dep = dep.building
                else:
                    if len(dep.neighbors_street.keys()) != 0:
                        begin.append(list(dep.neighbors_street.keys())[0].name)
                        dep = list(dep.neighbors_street.keys())[0]
            if isinstance(dep,Building):
                if len(dep.neighbors_street.keys()) != 0:
                    begin.append(list(dep.neighbors_street.keys())[0].name)
                    dep = list(dep.neighbors_street.keys())[0]
                else:
                    print('DIJ error : le building de dep n est pas connectée à une rue')
                    return []
        end = []
        if type(dest) != Street:
            if isinstance(dest,PrivateHouse):
                if dest.building != None:
                    end.append(dest.name)
                    dest = dest.building
                else:
                    print('DIJ error : la privatehouse de dest n a pas de building')
                    return []
            if isinstance(dest,Shop):
                if dest.building != None:
                    end.append(dest.name)
                    dest = dest.building
                else:
                    if len(dest.neighbors_street.keys()) != 0:
                        end.append(dest.name)
                        dest = list(dest.neighbors_street.keys())[0]
            if isinstance(dest,Building):
                if len(dest.neighbors_street.keys()) != 0:
                    end.append(dest.name)
                    dest = list(dest.neighbors_street.keys())[0]
                else:
                    print('DIJ error : le building de dest n est pas connectée à une rue')
                    return []
            end.reverse()

        if dep == dest:
            print('mm rue')
            return begin + end
        elif dest in dep.neighbors_street:
            print('voisine rue')
            return begin +[dest.name]+ end

        #print(begin,'->',end)
        #print(dep.name,dest.name)

        ## 3e étape : on trouve les nodes de départ et d'arrivée les plus proches
        dep_node = list(map(lambda x:x['door'],list(dep.neighbors_street.values())))[0].node
        dest_node = list(map(lambda x:x['door'],list(dest.neighbors_street.values())))[0].node

        ## 4e étape : applique dij
        nodes = dij(self.node_graph,dep_node,dest_node)

        ## 5e étape : on récupère les rues depuis les nodes
        mid = []
        st = dep.name
        for i in range(len(nodes)):
            if i < len(nodes)-1:
                rues = nodes[i].split(' -<->- ')
                if st in rues and st not in nodes[i+1].split(' -<->- '):
                    mid.append(st)
                    rues.remove(st)
                    st = rues[0]
            else:
                mid.append(st)
                if st != dest.name:
                    rues = nodes[i].split(' -<->- ')
                    rues.remove(st)
                    mid.append(rues[0])


        try: mid.remove(dep.name)
        except: print('error -',mid)
        print('shortest path :',dep.name,'->',dest.name,begin + mid + end)

        ## e étape : on concatene et on retourne
        return begin + mid + end

    # trains

    def add_train(self,train):

        self.BAHN[train.name] = train

    #

    def _shops(self):
        return list(filter(lambda x:isinstance(x,Shop), self.CITY.values()))
    shops = property(_shops)

    def _avnues(self):
        return list(filter(lambda x:type(x) == Street, self.CITY.values()))
    avnues = property(_avnues)

    def __len__(self):
        x=0
        for name in self.CITY:
            if type(self.CITY[name]) == Street:
                x+=1
        return x

    def _w(self):
        return self.width
    w = property(_w)

NY = CITY()

LINES = []

#LOAD = 3
# permet de conserver une map si y'en a une bien (1) ou d'en recreer une à chaque fois (0) ou de faire une map short (2) (plus d'actualité)
MAP_NAME = 'ny'
# key à transmettre à la fonction de chargement pour selectionner une map créée

"""'''''''''''''''''''''''''''''''''
'''''''PART 3 : BUILDINGS ''''''''''
'''''''''''''''''''''''''''''''''"""

builds = {
        'empty':{'text':0 , 'door':None ,'distrib':None,'maxY':None},
        'stand':{'text':1 , 'door':box(400,50,fx=800,h=370), 'door2':box(890,50,400,370) ,'distrib':(0,0),'maxY':100},
        'bat':{'text':2 , 'door':box(300,110,fx=570,h=400) ,'distrib':None,'maxY':110},
        'stairs':{'text':3 , 'door':box(310,100,fx=940,h=420) ,'distrib':(0,0),'maxY':90},
        'L':{'text':'side', 'door':None,'distrib':None,'maxY':100},
        'R':{'text':'side', 'door':None,'distrib':None,'maxY':50},
        'sbahn':{'text':4 , 'arret':750 ,'distrib':None,'maxY':None},
}

coll_boxs = {

        'L' : [
                box(x=0,y=50+Y_BUILD,fx=750,fy=800+Y_BUILD),
                box(x=750,y=70+Y_BUILD,fx=780,fy=800+Y_BUILD),
                box(x=780,y=100+Y_BUILD,fx=800,fy=800+Y_BUILD),
                ],
        'R' : [
                box(x=0,y=50+Y_BUILD,fx=750,fy=800+Y_BUILD),
                box(x=610,y=0+Y_BUILD,fx=800,fy=800+Y_BUILD),
                ],
        'empty' : [
                box(x=0,y=100+Y_BUILD,fx=160,fy=800+Y_BUILD),
                box(x=40,y=80+Y_BUILD,fx=130,fy=800+Y_BUILD),
                box(x=160,fx=190,y=120+Y_BUILD,fy=800+Y_BUILD),
                box(x=1410,fx=1500,y=200+Y_BUILD,fy=800+Y_BUILD),
                ],
        'stand' : [
                box(x=220,fx=280,y=80+Y_BUILD,fy=800+Y_BUILD),
                box(x=280,fx=360,y=60+Y_BUILD,fy=800+Y_BUILD),
                box(x=360,fx=800,y=40+Y_BUILD,fy=800+Y_BUILD),
                box(x=800,fx=880,y=80+Y_BUILD,fy=800+Y_BUILD),
                box(x=880,fx=1320,y=40+Y_BUILD,fy=800+Y_BUILD),
                box(x=1320,fx=1440,y=80+Y_BUILD,fy=800+Y_BUILD),
                box(x=1440,fx=1500,y=100+Y_BUILD,fy=800+Y_BUILD),
        ],
        'bat' : [
                box(x=0,fx=750,y=100+Y_BUILD,fy=800+Y_BUILD),
                box(x=210,fx=240,y=80+Y_BUILD,fy=800+Y_BUILD),
                box(x=590,fx=660,y=80+Y_BUILD,fy=800+Y_BUILD),
                box(x=760,fx=1500,y=110+Y_BUILD,fy=800+Y_BUILD),
        ],
        'stairs' : [
                box(x=0,fx=280,y=50+Y_BUILD,fy=800+Y_BUILD),
                box(x=280,fx=950,y=80+Y_BUILD,fy=800+Y_BUILD),
                box(x=950,fx=1220,y=50+Y_BUILD,fy=800+Y_BUILD),
                box(x=1220,fx=1270,y=70+Y_BUILD,fy=800+Y_BUILD),
                box(x=1270,fx=1500,y=90+Y_BUILD,fy=800+Y_BUILD),
                ],
        'sbahn' : [
                box(x=1310,fx=1330,y=130+Y_BUILD,fy=160+Y_BUILD),
        ],

            }

builds_key = ['empty','stand','bat'] # va être donné aléatoirement si ce n'est pas un build spécial


"""'''''''''''''''''''''''''''''''''
'''''''PART 4 : GENERATION '''''''''
'''''''''''''''''''''''''''''''''"""

nb_iterations = 4
rue_princ = 'kamour str.'


def create_map():

    ## la map part d'une rue simple et unique et puis s'étend de celle là
    #  chaque rue peut avoir un maximum que 4 rues voisines sinon ça va être le sbeul

    #-> à la fin on se retrouve avec 2**3 = 8 rues
    n = 1

    #pos_doors = {} # stocke les positions des portes de chaque rue (pour pas avoir deux rues au même endroit tsé)

    ## RUES
    lon = r.randint(5*(nb_iterations+1), 10*(nb_iterations+1))
    if nb_iterations > 5:
            lon = r.randint(5*4, 10*4)


    rues = [ preRue(rue_princ,0,0,lon) ]

    for i in range(nb_iterations):
        newrues = []
        for rue in rues:
            if rue.nb_voisins < 5:

                #general
                nom = 'rue '+str(n)
                n+=1
                lon = r.randint(5*(nb_iterations-i), 10*(nb_iterations-i))
                if nb_iterations-i > 4:
                    lon = r.randint(5*4, 10*4)
                vert = not rue.vert

                # on prend au hasard les pos des portes
                x_new = r.randint(1,lon-2)
                x_old = rue.place_door_rd(nom)

                # on calcule la position de départ de la nouvelle rue:
                if vert:
                    x,y = rue.x + x_old , rue.y - x_new
                else:
                    x,y = rue.x - x_new , rue.y + x_old

                #print(rue.x,rue.y,x_new,x_old,red(' -> '),x,y)

                # on crée la rue
                newrue = preRue(nom,x,y,lon,vert)

                # on place la nouvelle porte
                newrue.place_door(x_new,rue.name)
                newrues.append(newrue)
        rues += newrues

    x_distro = rues[0].place_door_rd('distro')
    x_shop = rues[0].place_door_rd('shop')
    rues[0].place_door(0,'home')

    # TRAIN
    circ_sbahn = [rue_princ]

    try:
        nb = 3
        for i in range(nb):
            chosen = r.choice(rues)
            #print(i,chosen.name)
            while chosen.name in circ_sbahn:
                chosen = r.choice(rues)
            circ_sbahn.append(chosen.name)
    except:print('warn : le sbahn ne circule que dans la rue princ')

    x_arrets = [] # stocke les gex de l'arret
    x_stations = [] # stocke les builds concernés
    for rue in circ_sbahn:
        i = list(map(lambda x:x.name,rues)).index(rue)
        i = rues[i].place_door_rd('sbahn')
        x_arrets.append( W_SIDE + i*W_BUILD + builds['sbahn']['arret'] )
        x_stations.append( i )

    #print(rues)
    ## TRANSFORMATION RUES EN STREETS

    connexions = []

    for rue in rues:

        nom = rue.name

        build_list = []
        #print(len(rue.cont),rue.long)

        ## on organise build_list
        for i in range(rue.long):
            if rue.cont[i] == 0:
                #print(builds_key)
                key = r.choice(list(filter(lambda x:x not in [3],builds_key)))
                build_list.append(key)
            else:
                build_list.append('stairs')

        # on place les différents shops
        if nom == rue_princ:
            build_list[0] = 'bat'
            build_list[x_distro] = 'bat'
            build_list[x_shop] = 'stand'

        # on place les stations de sbahn
        if nom in circ_sbahn:
            i = circ_sbahn.index(nom)
            build_list[x_stations[i]] = 'sbahn'

        ## on créé la street
        w = rue.long*W_BUILD+2*W_SIDE
        NY.add_streets(Street(rue,g.TEXTIDS['street'],build_list,box=box(0,-50,w)))

        if nom == rue_princ:

            ## HOME
            name = 'kedulov gang'

            # inside building
            zone_box = builds['bat']['door'].pop()
            zone_box.x += W_SIDE
            zone_box.y += Y_BUILD
            x,y = rue.get_pos( NY.CITY[nom].get_build_x(zone_box.x) )
            NY.add_streets(Building(preRue(name,x,y),g.TEXTIDS['inside']))
            connect(NY.CITY[name],box(600,Y_BUILD,400,400),NY.CITY[nom],zone_box,(False,False))

            #home + porte
            NY.add_streets(PrivateHouse(preRue('home',x,y),g.TEXTIDS['home']))
            connect(NY.CITY['home'],3200,NY.CITY[name],box(1500,Y_BUILD,300,400),(False,False))
            NY.CITY[name].add_house(NY.CITY['home'])

            #maison du voisin
            NY.add_streets(PrivateHouse(preRue('voisin',x,y),g.TEXTIDS['home']))
            connect(NY.CITY['voisin'],3200,NY.CITY[name],box(2500,Y_BUILD,300,400),(False,False))
            NY.CITY[name].add_house(NY.CITY['voisin'])

            ## 2 autres voisins
            for j in range(2,4):
                labtext = (None,'1'+chr(65+j))
                house_name = '1'+chr(65+j) +'-' + name
                NY.add_streets(PrivateHouse(preRue(house_name,x,y),g.TEXTIDS['home']))
                connect(NY.CITY[house_name],3200,NY.CITY[name],box(1500+1000*j,Y_BUILD,300,400),(False,False),labtext)
                NY.CITY[name].add_house(NY.CITY[house_name])

            ## DISTROKID

            #distrokid + porte
            zone_box = builds['bat']['door'].pop()
            zone_box.y += Y_BUILD
            zone_box.x += x_distro*W_BUILD+W_SIDE
            x,y = rue.get_pos( NY.CITY[nom].get_build_x(zone_box.x) )
            NY.add_streets(Distrokid(x,y))
            connect(NY.CITY['distrokid'],4215,NY.CITY[nom],zone_box,(False,False))

            ## SHOP
            zone_box = builds['stand']['door'].pop()
            zone_box.y += Y_BUILD
            zone_box.x += x_shop*W_BUILD+W_SIDE
            zone_box2 = builds['stand']['door2'].pop()
            zone_box2.y += Y_BUILD
            zone_box2.x += x_shop*W_BUILD+W_SIDE
            x,y = rue.get_pos( NY.CITY[nom].get_build_x(zone_box.x) )
            NY.add_streets(MiniMarket(x,y))
            connect(NY.CITY['shop'],1160,NY.CITY[nom],zone_box,(False,False))
            connect(NY.CITY['shop'],4960,NY.CITY[nom],zone_box2,(False,False))

        for i in range(rue.long):

            if builds[build_list[i]]['distrib'] and r.random() > 0.75:
                # on crée un distrib
                x,y = i*W_BUILD+W_SIDE,Y_BUILD
                y += builds[build_list[i]]['distrib'][1]
                x += builds[build_list[i]]['distrib'][0]
                distrib = o.Distrib(x,y)
                NY.CITY[nom].assign_zones([distrib])

            ## On créé un BUILDING
            if rue.cont[i] == 0 and builds[build_list[i]]['door']:

                zone_box = builds[build_list[i]]['door'].pop()
                zone_box.y += Y_BUILD
                zone_box.x += i*W_BUILD+W_SIDE

                x,y = rue.get_pos( NY.CITY[nom].get_build_x(zone_box.x) )

                name = str(i) + '- ' +nom

                # inside building
                NY.add_streets(Building(preRue(name,x,y),g.TEXTIDS['inside']))
                connect(NY.CITY[name],box(600,Y_BUILD,400,400),NY.CITY[nom],zone_box,(False,False))

                ## CHAQUE APPART DANS CHAQUE BUILDING
                for j in range(4):
                    labtext = (None,'1'+chr(65+j))
                    house_name = '1'+chr(65+j) +'-' + str(i) + ' '+nom
                    NY.add_streets(PrivateHouse(preRue(house_name,x,y),g.TEXTIDS['home']))
                    connect(NY.CITY[house_name],3200,NY.CITY[name],box(1500+1000*j,Y_BUILD,300,400),(False,False),labtext)
                    NY.CITY[name].add_house(NY.CITY[house_name])

            elif rue.cont[i] != 0 and rue.cont[i] not in ['distro','home','shop','sbahn']:
                ## On connecte les rues
                #print(build_list[i])
                zone_box = builds[build_list[i]]['door'].pop()
                dx = zone_box.x
                zone_box.y += Y_BUILD
                zone_box.x += i*W_BUILD+W_SIDE
                x2 = list(filter(lambda x:x.name == rue.cont[i],rues))[0].cont.index(nom)*W_BUILD+dx+W_SIDE
                connexions.append( [nom,zone_box,rue.cont[i],x2] )

    for st1,zonebox,st2,x2 in connexions:

        connect_solo(NY.CITY[st1],zonebox,NY.CITY[st2],x2,anim='stairs')


    ## TRAIN

    sbahn = Train(circ_sbahn,x_arrets)
    NY.add_train(sbahn)

"""'''''''''''''''''''''''''''''''''
'''''''PART 5 : USEFUL FONCTIONS''''
'''''''''''''''''''''''''''''''''"""

def connect(street1,box1,street2,box2,col=(False,False),labs=(None,None)):

    ## crée 2 portes :
    ##      -une à x1 dans la street1 pour passer dans la street2
    ##      -une à x2 dans la street2 pour passer dans la street1

    if type(box1) != box:
        box1 = box(box1,Y_BUILD,270,400)
    if type(box2) != box:
        box2 = box(box2,Y_BUILD,270,400)

    door1 = o.Porte(street1,box1,street2,box2.x,makeCol=col[0],text=labs[0])
    street1.assign_zones([door1])

    door2 = o.Porte(street2,box2,street1,box1.x,makeCol=col[1],text=labs[1])
    street2.assign_zones([door2])

def connect_solo(street1,box1,street2,x2,col=False,labs=None,anim='door'):

    ## crée 1 porte :
    ##      -à x1 dans la street1 pour passer dans la street2

    if type(box1) != box:
        box1 = box(box1,Y_BUILD,270,400)

    door = o.Porte(street1,box1,street2,x2,makeCol=col,text=labs,anim=anim)
    street1.assign_zones([door])

def save_lines(tab):

    # on transforme les prestr et les connexions en str
    prestr,connex = tab
    lines = []
    for str in prestr:
        lines.append((str.name,str.x,str.y,str.xf,str.yf))

    tab = lines,connex

    # on dump
    if not 'maps' in os.listdir():
        os.makedirs('maps')

    with open('maps/map','w') as f:
        json.dump(tab,f)

def load_lines(name='map'):

    # on load
    with open('maps/'+name,'r') as f:
        tab = json.load(f)

    # on transforme les str en prestr
    lines,connex = tab
    prestr = []
    for line in lines:
        name,xd,yd,xf,yf = line
        prestr.append(preStreet(name,xd,yd,xf,yf))

    return prestr,connex
