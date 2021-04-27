
from src import graphic as g

class Street():

    def __init__(self,text,name='street1',pos=(-1400,-50)):

        self.streetbg = g.sman.addSpr(text[0],pos,group='mid-1')
        self.streetfg = g.sman.addSpr(text[1],pos,group='midup')
        self.name = name
        self.pos = pos

    def modify(self,x=None,y=None):
        if x != None:
            self.x = x+self.pos[0]
        if y != None:
            self.y = y+self.pos[1]


    #

    def _x(self):
        return g.sman.spr(self.streetbg).x
    def _setx(self,x):
        g.sman.spr(self.streetbg).x = x
        g.sman.spr(self.streetfg).x = x
    def _xf(self):
        return g.sman.spr(self.streetbg).x + g.sman.spr(self.streetbg).width
    x = property(_x,_setx)
    xf= property(_xf)

    def _y(self):
        return g.sman.spr(self.streetbg).y
    def _sety(self,y):
        g.sman.spr(self.streetbg).y = y
        g.sman.spr(self.streetfg).y = y
    y = property(_y,_sety)

    def _xxf(self):
        return (self.pos[0],self.pos[0]+g.sman.spr(self.streetbg).width)
    xxf = property(_xxf)
