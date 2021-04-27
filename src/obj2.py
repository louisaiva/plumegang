
from src import graphic as g

class Street():

    def __init__(self,text=(None,None),name='street1',pos=(-1400,-50)):

        self.text = text
        if self.text != (None,None):
            self.streetbg = g.sman.addSpr(text[0],pos,group='mid-1')
            self.streetfg = g.sman.addSpr(text[1],pos,group='midup')


        if hasattr(self,'streetbg'):
            self._w = g.sman.spr(self.streetbg).width
        else:
            self._w = None
        self._x,self._y = pos

        self.name = name
        self.pos = pos

        self.zones = {}

    def modify(self,x=None,y=None):
        if x != None:
            self.x = x+self.pos[0]
        if y != None:
            self.y = y+self.pos[1]

    def assign_zones(self,zones):

        for zone in zones:
            self.zones[zone.name] = zone

    def delete(self):
        if hasattr(self,'streetbg'):
            g.sman.delete([self.streetbg,self.streetfg])
            del self.streetbg
            del self.streetfg

        for zone in self.zones:
            self.zones[zone].delete()

    def load(self):
        if self.text != (None,None):
            self.streetbg = g.sman.addSpr(text[0],pos,group='mid-1')
            self.streetfg = g.sman.addSpr(text[1],pos,group='midup')
    #

    def _x(self):
        if hasattr(self,'streetbg'):
            return g.sman.spr(self.streetbg).x
        else:
            return self._x

    def _setx(self,x):
        if hasattr(self,'streetbg'):
            g.sman.spr(self.streetbg).x = x
            g.sman.spr(self.streetfg).x = x
        else:
            self._x = x

    def _xf(self):
        if hasattr(self,'streetbg'):
            return g.sman.spr(self.streetbg).x + g.sman.spr(self.streetbg).width
        else:
            if self._w == None:
                return None
            else:
                return self._x + self._w
    x = property(_x,_setx)
    xf= property(_xf)

    def _y(self):
        if hasattr(self,'streetbg'):
            return g.sman.spr(self.streetbg).y
        else:
            self._y = y
    def _sety(self,y):
        if hasattr(self,'streetbg'):
            g.sman.spr(self.streetbg).y = y
            g.sman.spr(self.streetfg).y = y
        else:
            self._y = y
    y = property(_y,_sety)

    def _xxf(self):
        if hasattr(self,'streetbg'):
            return (self.pos[0],self.pos[0]+g.sman.spr(self.streetbg).width)
        else:
            if self._w == None:
                return (None,None)
            else:
                return (self.pos[0],self.pos[0]+self._w)
    xxf = property(_xxf)


CITY = {}
