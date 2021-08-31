"""
CODED by deltasfer
enjoy
"""

from src.utils import *
from src import graphic as g
from src import obj as o


class Street():

    def __init__(self,name='street1',text=(None,None),box=box(2730,-50,None)):

        self.text = text

        self.box = box
        self._x,self._y = self.box.xy

        self.name = name

        self.zones = {}
        self.humans = []
        self.items = []

        self.visible = False

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

        self.visible = True
    #

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

class House(Street):

    def __init__(self,name='house1',text=(None,None),box=box(-1400,-50,5120)):
        super(House,self).__init__(name,text,box)

        #self.name = owner.name+'\'s House'
        self.owners = []

    def set_owner(self,owner):
        self.owners.append(owner)

    def openable(self,perso):
        return perso in self.owners


CITY = {}
CITY['STREET'] = {}
CITY['HOUSE'] = {}


def generate_map():
    pass

def connect(street1,x1,street2,x2):

    ## crée 2 portes :
    ##      -une à x1 dans la street1 pour passer dans la street2
    ##      -une à x2 dans la street2 pour passer dans la street1

    door1 = o.Porte(street1,box(x1,225,270,400),street2,x2)
    street1.assign_zones([door1])

    door2 = o.Porte(street2,box(x2,225,270,400),street1,x1)
    street2.assign_zones([door2])
