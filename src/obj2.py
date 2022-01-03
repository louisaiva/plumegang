"""
CODED by deltasfer
enjoy
"""

import json,os
from src.utils import *
from src import graphic as g
from src import obj as o
from src import perso as p
import random as r

Y = 100,175

# lines

class preStreet(line):

    def __init__(self,name,xd,yd,xf,yf,connex=[]):

        super(preStreet,self).__init__(xd,yd,xf,yf)
        self.name = name

        self.connex = connex

    def add_conn(self,street,x):
        self.connex.append((street.name,x))

## streets

class Street():

    def __init__(self,preStreet,text=(None,None),box=box(0,-50,None)):

        self.text = text

        self.box = box
        self._x,self._y = self.box.xy

        self.name = preStreet.name
        self.line = preStreet.line
        self.pre = preStreet

        self.zones = {}
        self.humans = []
        self.items = []

        self.visible = False

        self.catalog = [] ## ce tableau est un tableau ordonné selon les X contenant tous les éléments et leurs détails:
                            # x y type nom

    def modify(self,x=None,y=None):
        if x != None:
            self.x = x+self.box.xy[0]
        if y != None:
            self.y = y+self.box.xy[1]

    def assign_zones(self,zones):
        for zone in zones:
            self.zones[zone.name] = zone

    def add_item(self,item):
        if type(item) == type([]):
            for ite in item:
                self.items.append(ite)
                if self.visible:
                    ite.load()
        else:
            self.items.append(item)
            if self.visible:
                item.load()

    def del_item(self,item):
        if item in self.items:
            self.items.remove(item)
            if self.visible:
                item.deload()

    def add_hum(self,hum):

        if type(hum) == type([]):
            for h in hum:
                self.humans.append(h)
                if self.visible:
                    h.load()
        else:
            self.humans.append(hum)
            if self.visible:
                hum.load()

    def del_hum(self,hum):
        if hum in self.humans:
            self.humans.remove(hum)
            if self.visible:
                hum.deload()

    def deload(self):
        if hasattr(self,'streetbg'):
            g.sman.delete(self.streetbg)
            del self.streetbg
        if hasattr(self,'streetfg'):
            g.sman.delete(self.streetfg)
            del self.streetfg

        for zone in self.zones:
            self.zones[zone].deload()

        for h in self.humans:
            h.deload()

        for item in self.items:
            item.deload()

        self.visible = False

    def load(self):

        if self.text[0] != None:
            self.streetbg = g.sman.addSpr(self.text[0],self.box.xy,group='mid-1')
        if self.text[1] != None:
            self.streetfg = g.sman.addSpr(self.text[1],self.box.xy,group='midup')

        for zone in self.zones:
            self.zones[zone].load()

        for h in self.humans:
            h.load()

        for item in self.items:
            item.load()

        print(len(list(self.zones)),'zones ---',len(self.humans),'humans ---',len(self.items),'items loaded')

        self.visible = True
        self.update_catalog()

    def update_catalog(self,perso=None):
        self.catalog = []
        for zone in self.zones:
            self.catalog.append( {'x':self.zones[zone].box.cx,'y':self.zones[zone].box.cy,'type':'zone','nom':self.zones[zone].name} )
        for hum in self.humans:
            self.catalog.append( {'x':hum.gex,'y':hum.gey,'type':'hum','nom':hum.name} )
        for item in self.items:
            self.catalog.append( {'x':item.box.cx,'y':item.box.cy,'type':'item','nom':item.name} )
        if perso != None:
            self.catalog.append( {'x':perso.gex,'y':perso.gey,'type':'hum','nom':perso.name} )


        self.catalog.sort(key=lambda x:x.get('x'))

    # bots
    def rand_pos(self):
        x,y = random.randint(0,self.rxf),random.randint(*Y)
        return (x,y)

    def environ_lr(self,xl,xr):
        if xl > xr :
            xr,xl=xl,xr

        il,ir = len(self.catalog)-1,0
        while self.catalog[il].get('x') > xl and il > 0:
            il-=1
        while self.catalog[ir].get('x') < xr and ir > len(self.catalog)-1:
            ir+=1

        elem = []
        for i in range(il,ir+1):
            elem.append(self.catalog[i])
        return elem

    def environ(self,elem):
        #tab = self.environ_lr()
        xl,xr=elem.gex-1000,elem.gex+1000

        il,ir = len(self.catalog)-1,0
        while il > 0 and self.catalog[il-1].get('x') > xl :
            il-=1
        while ir < len(self.catalog)-1 and self.catalog[ir+1].get('x') < xr :
            ir+=1

        elems = []
        for i in range(il,ir+1):
            #if self.catalog[i].get('nom') != elem.name:
            elems.append(self.catalog[i])
        return elems

    ###

    def _x(self):
        return self._x
    def _setx(self,x):
        if hasattr(self,'streetbg'):
            g.sman.spr(self.streetbg).x = x
        if hasattr(self,'streetfg'):
            g.sman.spr(self.streetfg).x = x
        self._x = x

    def _rxf(self):
        if self.box.w == None:
            return None
        else:
            return self._x + self.box.w
    x = property(_x,_setx)
    rxf= property(_rxf)

    def _y(self):
        return self._y
    def _sety(self,y):
        if hasattr(self,'streetbg'):
            g.sman.spr(self.streetbg).y = y
        if hasattr(self,'streetfg'):
            g.sman.spr(self.streetfg).y = y
        self._y = y
    y = property(_y,_sety)

    def _xxf(self):
        if self.box.w == None:
            return (None,None)
        else:
            return (self.box.xy[0],self.box.xy[0]+self.box.w)
    xxf = property(_xxf)

    def _yyf(self):
        return 100,175
    yyf = property(_yyf)

    def _w(self):
        return self.box.w
    w = property(_w)

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

class House(Street):

    def __init__(self,name='house1',text=(None,None),box=box(-1400,-50,5120)):
        super(House,self).__init__(name,text,box)

        self.owners = []

    def set_owner(self,owner):
        self.owners.append(owner)

    def openable(self,perso):
        return perso in self.owners

class Shop(House):

    def __init__(self,name='shop1',text=(None,None),box=box(0,-50,5120)):
        super(Shop,self).__init__(name,text,box)

        self.guys = []
        self.guys.append( p.Guy(g.TEXTIDS['guys'],self.rand_pos(),street=self.name) )

    def openable(self,perso):
        return True

    def del_hum(self,hum):
        super(Shop,self).del_hum(hum)
        """if not hum.alive:
            self.guys.remove(hum)"""

    def update_catalog(self,perso=None):
        for guy in self.guys:
            if not guy.alive:
                print('wtf alphonse mort')
                exp = guy.name + ' est mort wtf'
                g.pman.alert(exp)
                self.guys.remove(guy)
                #self.guys.append(p.Human_to_Guy(self))
        super(Shop,self).update_catalog(perso)

## CITY

class CITY():

    def __init__(self):
        self.width = 0
        self.CITY = {}

        self.Ghost = Street(preStreet('ghost',1,1,2,1),box=box(0,-50,50))

    def add_streets(self,street):
        if type(street) == []:
            for stree in street:
                self.add_streets(stee)
        else:
            self.CITY[street.name] = street
            self.width += street.w

    def percentage(self,street):
        return street.w / self.w

    def rand_street(self):

        k = r.random()
        d = 0

        for street in list(self.CITY.values()):
            if type(street) != House and k > d and k <= d+self.percentage(street):
                return street
            d+=self.percentage(street)
        return list(self.CITY.values())[0]


    #

    def _w(self):
        return self.width
    w = property(_w)

NY = CITY()

LINES = []

LOAD = 1
# permet de conserver une map si y'en a une bien (1) ou d'en recreer une à chaque fois (0)
MAP_NAME = 'ny'
# key à transmettre à la fonction de chargement pour selectionner une map créée

#-------------------------------#
#-------------------------------#

k = 20

MAP = k,k
nb_lines = k

def generate_map():

    global LINES

    lines = []
    connexions = []

    ## street longueur 1 => 10k => de 0 à 10000
    ## longueur 2 => 20k
    ## ...

    if LOAD == 1:
        lines,connexions = load_lines(MAP_NAME)
    else:
        a=0
        while len(lines) == 0:
            a+=1
            #print(a,'try')
            lines,connexions = create_rect_lines()

    ### TRANSFORMATION LINES IN STREETS

    line_home = r.choice(lines)
    line_distro = r.choice(lines)

    width_between_streets = 5000

    # we create streets + home
    for line in lines:
        NY.add_streets(Street(line,box=box(-100,-50,(line.w+1)*width_between_streets+100)))

        if line == line_home:
            prestr = preStreet('home',line.x,line.y,line.x,line.y)
            NY.add_streets(House(prestr,(g.TEXTIDS['bgmid'],g.TEXTIDS['bgup'])))
            connect(NY.CITY['home'],3200,NY.CITY[line.name],500,(False,True))
            LINES.append(prestr)

            #elif line == line_distro:
            prestr = preStreet('distrokid',line.x,line.y,line.x,line.y)
            NY.add_streets(Shop(prestr,(g.TEXTIDS['distrokid']['mid'],None)))
            connect(NY.CITY['distrokid'],4215,NY.CITY[line.name],1500,(False,True))
            LINES.append(prestr)

            prestr = preStreet('maison de drake',line.x,line.y,line.x,line.y)
            NY.add_streets(House(prestr,(g.TEXTIDS['bgmid'],None)))
            connect(NY.CITY['maison de drake'],3200,NY.CITY[line.name],2500,(False,True))
            LINES.append(prestr)


    # we make connexions -> creations of doors
    for conn in connexions:
        line1,x1,line2,x2 = conn
        connect(NY.CITY[line1],x1*width_between_streets,NY.CITY[line2],x2*width_between_streets)

    LINES += lines[:]

    # we draw the whole NY.CITY
    #draw_lines()

def create_rand_lines():

    lines = []
    connexions = []

    ## CREATION OF LINES

    for i in range(nb_lines):

        line = rand_line(i)

        for j in range(len(lines)):
            R = line_intersection2(line.line,lines[j].line)
            #print(R)
            if R:
                X,Z = R
                if line.vert :
                    x1 = Z-line.line[0][1]
                    x2 = X-lines[j].line[0][0]

                else:
                    x1 = X-line.line[0][0]
                    x2 = Z-lines[j].line[0][1]

                connexions.append((line.name,x1,lines[j].name,x2))
                line.add_conn(lines[j],x1)
                lines[j].add_conn(line,x2)

        lines.append(line)


    ## WE DELETE ALONE LINES

    todel = []
    for line in lines:
        if len(line.connex) == 0:
            todel.append(line)
    for line in todel:
        lines.remove(line)

    save_lines((lines,connexions))
    return lines,connexions

def create_rect_lines():

    lines = []
    connexions = []

    ## CREATION OF LINES

    print( [*range(0,k,2)] )

    # verticales
    for i in range(0,k,2):

        ## x reste le meme
        xdep = i
        ydep = 0
        xfin = i
        yfin = MAP[1]
        line = preStreet('street'+str(i),xdep,ydep,xfin,yfin)

        for j in range(len(lines)):
            R = line_intersection2(line.line,lines[j].line)
            #print(R)
            if R:
                X,Z = R
                if line.vert :
                    x1 = Z-line.line[0][1]
                    x2 = X-lines[j].line[0][0]

                else:
                    x1 = X-line.line[0][0]
                    x2 = Z-lines[j].line[0][1]

                connexions.append((line.name,x1,lines[j].name,x2))
                line.add_conn(lines[j],x1)
                lines[j].add_conn(line,x2)

        lines.append(line)

    # horiz
    for i in range(0,k,2):

        ## y reste le meme
        xdep = 0
        ydep = i
        xfin = MAP[1]
        yfin = i
        line = preStreet('street'+str(i+1),xdep,ydep,xfin,yfin)

        for j in range(len(lines)):
            R = line_intersection2(line.line,lines[j].line)
            #print(R)
            if R:
                X,Z = R
                if line.vert :
                    x1 = Z-line.line[0][1]
                    x2 = X-lines[j].line[0][0]

                else:
                    x1 = X-line.line[0][0]
                    x2 = Z-lines[j].line[0][1]

                connexions.append((line.name,x1,lines[j].name,x2))
                line.add_conn(lines[j],x1)
                lines[j].add_conn(line,x2)

        lines.append(line)

    save_lines((lines,connexions))
    return lines,connexions

def rand_line(i):

    vert = r.choice([True,False])

    if vert:
        ## x reste le meme
        xdep = r.randint(0, MAP[0])
        ydep = r.randint(0, MAP[1]-1)
        xfin = xdep
        yfin = r.randint(ydep+1,MAP[1])

    else:
        ## y reste le meme
        xdep = r.randint(0, MAP[0]-1)
        ydep = r.randint(0, MAP[1])
        xfin = r.randint(xdep+1,MAP[1])
        yfin = ydep

    return preStreet('street'+str(i),xdep,ydep,xfin,yfin)

def connect(street1,x1,street2,x2,col=(True,True)):

    ## crée 2 portes :
    ##      -une à x1 dans la street1 pour passer dans la street2
    ##      -une à x2 dans la street2 pour passer dans la street1

    door1 = o.Porte(street1,box(x1,225,270,400),street2,x2,makeCol=col[0])
    street1.assign_zones([door1])

    door2 = o.Porte(street2,box(x2,225,270,400),street1,x1,makeCol=col[1])
    street2.assign_zones([door2])

def draw_lines():

    map = [[ ' ' for i in range(MAP[0]+1)] for i in range(MAP[1]+1)]

    xhome,yhome = 0,0
    for street in LINES:
        if street.name == 'home':
            xhome,yhome = street.x,street.y
        else:
            if street.vert:
                street=street.line
                # same x
                x = street[0][0]
                for y in range(street[0][1],street[1][1]):
                    map[y][x] = '|'

            else:
                street=street.line
                # same y
                y = street[0][1]
                for x in range(street[0][0],street[1][0]):
                    map[y][x] = '='

    map[yhome][xhome] = 'X'


    s=' '

    for x in range(len(map[0])):
        s+=' '+str(x)
    s+='\n'

    for y in range(len(map)):
        s+=str(y)+' '
        for x in range(len(map[y])):
            s+=map[y][x]+' '
        s+='\n'

    print('map'+'\n\n'+s)

def print_lines():
    for street in NY.CITY:
        print(NY.CITY[street])

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
