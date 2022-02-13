"""
CODED by deltasfer
enjoy
"""

from src import perso as p
from src import graphic as g
from src import obj2 as o2
import pyglet,time
from colors import *
from src.colors import *
from src.utils import *

def cmds():

    def tp(name,x='None',y='None',street='None'):

        hum = None
        for h in p.BOTS+p.GUYS:
            if h.name == name:
                hum = h
                break
        if not hum:
            return 'entity not found'

        if x != 'None':
            x = int(x)
        else:
            x = None

        if y != 'None':
            y = int(y)
        else:
            y = None

        if street == 'None':
            street = None
        else:
            street = o2.NY.CITY[street]

        hum.tp(x,y,street)

    def tp_street(name,street):
        hum = None
        for h in p.BOTS+p.GUYS:
            if h.name == name:
                hum = h
                break
        if not hum:
            return 'entity not found'

        hum.tp(street=o2.NY.CITY[street])

    def set_streams(name,qté):
        hum = None
        for h in p.BOTS+p.GUYS:
            if h.name == name:
                hum = h
                break
        if not hum:
            return 'entity not found'

        if qté: qté = int(qté)

        hum.nb_streams = qté

    def kill(name):
        hum = None
        for h in p.BOTS+p.GUYS:
            if h.name == name:
                hum = h
                break
        if not hum:
            return 'entity not found'

        hum.die()

    def tick_set(tick):

        tick = int(tick)
        g.Cyc.tick_set(tick)

    def time_set(h='None',m='None'):

        tick = int(tick)
        g.Cyc.tick_set(tick)

    return locals()

commands = cmds()

##### CONSOLE

class Console():

    def __init__(self):

        self.window = None

        self.historic = []
        self.ids = []
        self.x,self.y = 10,300
        self.dt = 128
        self.size = 16
        self.max_length = 25
        self.visible = True

        self.font = 'Consolas'
        self.activated = False

        ## PARTIE DOCUMENT
        self.document = pyglet.text.document.UnformattedDocument()
        self.document.set_style(0, len(self.document.text), dict(font_name =self.font, font_size = self.size, color =(255, 255, 255, 255)))

        #self.document.font_name = self.font
        font = self.document.get_font()
        height = font.ascent - font.descent

        self.layout = pyglet.text.layout.IncrementalTextLayout(self.document, 3*g.scr.w//4, height, batch=g.tman.batch,group=g.gman.getGroup('up'))
        self.layout.position = self.x,self.y-3*self.size
        self.caret = pyglet.text.caret.Caret(self.layout,batch=g.tman.batch, color =(255, 255, 255))
        self.caret.set_style({'font_name':self.font,'font_size':self.size,'color':(255,255,255)})

        self.input_historic = []
        self.point_input = None

    def roll_activate(self,window=None):
        if not self.activated:
            self.bg = g.sman.addCol('black_faded',box(w=g.scr.w,h=g.scr.h),group='up-1')

            # Rectangular outline
            pad = 2
            font = self.document.get_font()
            height = font.ascent - font.descent

            self.rect = g.sman.addCol('black_faded',box(x=self.x-2 , y=self.y-3*self.size - 2 , w=3*g.scr.w//4 + 2,h=height + 2),group='up-1')

            self.activated = True
            g.bertran.schedule_once(window.set_focus,0.2,self)
            #window.focus = self
        else:
            # on delete le bg
            if hasattr(self,'bg'):
                g.sman.delete([self.bg,self.rect])
                del self.bg
                del self.rect
            self.activated = False
            window.focus = None
            self.document.text = ''
        self.window = window

    def enter(self,hum):
        if self.activated:

            txt = self.document.text
            if len(txt) > 0 and txt[0] == '/':

                command = txt[1:]

                par = command.split(' ')

                ## adjustment
                todel = []
                par_add = []
                i_add = []

                for i in range(len(par)):
                    if i < len(par)-1 and (par[i][0] == '<' and par[i+1][-1] == '>'):
                        i_add.append(i)
                        s = par[i][1:] + ' ' + par[i+1][:-1]
                        par_add.append(s)
                        todel.append([par[i],par[i+1]])

                    if par[i][0] == '<' and par[i][-1] == '>':
                        par[i] = par[i][1:-1]

                for i in range(len(todel)):
                    if type(todel[i]) == type([]):
                        for x in todel[i]:
                            par.remove(x)
                    else:
                        par.remove(todel[i])
                    par.insert(i_add[i],par_add[i])

                ## lezgo cmd
                if par[0] not in commands:
                    self.colorsay('red','command not found')
                    return
                else:
                    try:
                        result = commands[par[0]]( *par[1:] )
                        if result == None:
                            self.colorsay('green','command sucessful !')
                            if self.document.text in self.input_historic:
                                self.input_historic.remove(self.document.text)
                            self.input_historic.append(self.document.text)
                            self.roll_activate(self.window)
                            return
                        else:
                            self.colorsay('orange',result)
                    except:
                        self.colorsay('red','error in the parameters')
                        return

            else:
                self.say('<'+hum.name+'>',self.document.text)

            if self.document.text in self.input_historic:
                self.input_historic.remove(self.document.text)
            self.input_historic.append(self.document.text)
            self.document.text = ''

    def say(self,*args):

        print(*args)
        args = [str(x) for x in args]
        cmd = ' '.join(args)

        self.historic.append(cmd)
        for id in self.ids:
            g.pman.modify_single(id,dy=self.size+2)
        id = g.pman.addLabPart(cmd,self.pos,self.dt,font_name=self.font,font_size=self.size,anchor=('left','center'),key='cmd',vis=self.visible,group='up',use_str_bien=False)
        self.ids.append(id)
        if len(self.ids) >= self.max_length:
            del self.ids[0]

    def colorsay(self,col,*args):

        args = [str(x) for x in args]
        cmd = ' '.join(args)
        print(color(cmd,col))

        self.historic.append(cmd)
        for id in self.ids:
            g.pman.modify_single(id,dy=self.size+2)
        id = g.pman.addLabPart(cmd,self.pos,self.dt,font_name=self.font,font_size=self.size,color=c[col],anchor=('left','center'),key='cmd',vis=self.visible,group='up',use_str_bien=False)
        self.ids.append(id)
        if len(self.ids) >= self.max_length:
            del self.ids[0]

    def rollhide(self):
        g.pman.unhide('cmd',self.visible)
        if hasattr(self,'bg'): g.sman.unhide([self.bg,self.rect],self.visible)
        self.visible = not self.visible

    def up(self):
        if not self.point_input:
            self.point_input = 0
        if len(self.input_historic) >= abs(self.point_input - 1):
            self.point_input -= 1
            self.document.text = self.input_historic[self.point_input]

    def down(self):
        if self.point_input:
            self.point_input += 1
            if self.point_input < 0:
                self.document.text = self.input_historic[self.point_input]
            else:
                self.point_input = None
                self.document.text = ''

    #
    def pos():
        def fget(self):
            return self.x,self.y
        def fset(self, value):
            self.x,self.y = value
        return locals()
    pos = property(**pos())

Cmd = Console()

def colorsay(*args): Cmd.colorsay(*args)
def say(*args): Cmd.say(*args)
def rollhide(*args): Cmd.rollhide(*args)
def enter(*args): Cmd.enter(*args)
def roll_activate(*args): Cmd.roll_activate(*args)
