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
import random as r
import plume

CMD_TRY = False
# useful for resolving bug in the functions

# useful
def get_hum(name):

    if name == '@':
        if hasattr(Cmd,'perso'):
            return Cmd.perso
    for h in p.BOTS+p.GUYS:
        if h.name == name or h.id == name:
            return h

def get_street(name,hum=None):
    if name == '@':
        if hasattr(Cmd,'perso'):
            return o2.NY.CITY[Cmd.perso.street]

    if name == '#' and hum:
        return o2.NY.CITY[hum.street]

    if name in o2.NY.CITY:
        return o2.NY.CITY[name]

# dic of cmds
def cmds():

    # tps
    def tp(name,x='None',y='None',street='#'):

        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        if type(x) == type('wesh'):
            if x.isnumeric():
                x = int(x)
            elif x=='None':
                x = None
            else:
                # on essaie de créer trouver un humain pour la destination finale
                ret = tp_to_perso(name,x)
                if not ret:
                    return
                # ça veut dire qu'on a pas réussi à trouver l'humain de destination, estce une street ?
                ret = tp_street(name,x)
                if not ret:
                    return
                else:
                    return 'error : 2nd parameter nor x, nor human, nor street :/'

        if type(y) == type('wesh'):
            if y.isnumeric():
                y = int(y)
            else:
                y = None

        street = get_street(street,hum)
        if not street:
            return 'street not found'

        hum.tp(x,y,street)

    def tp_self(x='None',y='None',street='None'):

        hum = get_hum('@')
        if not hum:
            return 'entity not found'
        return tp(hum.id,x,y,street)

    def tp_street(name,street):
        return tp(name,'None','None',street)

    def tp_to_perso(name,dest_name):

        dest = get_hum(dest_name)
        if not dest:
            return 'destination entity not found'

        gex,gey,street = dest.gex,dest.gey,dest.street
        return tp(name,gex,gey,street)

    # general perso
    def set_streams(name,qté):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        if qté: qté = int(qté)

        hum.nb_streams = qté

    def add_streams(name,qté):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        if qté: qté = int(qté)

        hum.nb_streams += qté

    def set_money(name,qté):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        if qté: qté = int(qté)

        hum.money = qté

    def add_money(name,qté):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        if qté: qté = int(qté)

        hum.add_money(qté)

    def set_fans(name,qté):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        if qté:
            qté = int(qté)

        hum.nb_fans = qté

    # perso godmode, kill toussa toussa
    def wesh():
        hum = get_hum('@')
        if not hum:
            return 'self not found'
        #print('oh yo',hum,hum.name)
        ret = set_fans(hum.name,r.randint(10000,20000))
        if ret:
            return ret

        ret = add_money(hum.name,r.randint(10000000,20000000))
        if ret:
            return ret

        hum.damage = 300
        hum.max_life = 3000
        hum.life = hum.max_life
        hum.confidence = 100

    def esh():
        return wesh()

    def kill(name):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        dmg(name,hum.max_life)

    def stop(name):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        colorsay('orange','a command just immobilized',hum.name)
        hum.immobilised = True

    def free(name):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        colorsay('orange','a command just freed',hum.name)
        hum.immobilised = False

    def dmg(name,qté='20'):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        hitter = get_hum('@')
        if not hitter:
            return '@ not found'

        if qté: qté = int(qté)

        hum.be_hit(hitter,qté)

    def perso(name='@'):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        return '<@> '+ str(hum)

    def poto(name='@'):
        hum = get_hum(name)
        if not hum:
            return 'entity not found'

        perso = get_hum('@')
        if not perso:
            return '@ not found'

        perso.assign_poto(hum)
        return '<@> '+ hum.name + ' assigned to poto'

    # id
    def get_id():
        hum = None
        if hasattr(Cmd,'perso'):
            hum = Cmd.perso
        if not hum:
            return 'self not found'

        if len(hum.hum_env) > 0:
            bot = hum.hum_env[0]
            #colorsay('green',)
            return '<@> target bot is '+bot.name+', id:'+bot.id
        else:
            return '<@> '+hum.name+' is alone, id:'+hum.id

    def street(street=None):

        if street:
            street = get_street(street)
            if street:
                return '<@> '+street.__repr__()
            else:
                return 'street not found'
        else:
            return '<@> '+o2.NY.name+' city : '+str(len(o2.NY.CITY))+' streets'

    #train
    def sbahn_speed(spd='None'):
        if spd == 'None':
            spd = o2.NY.BAHN['sbahn'].max_speed
            return '<@> sbahn speed is '+str(spd)
        else:
            if spd: spd = int(spd)
            o2.NY.BAHN['sbahn'].max_speed = spd

    # time/tick
    def tick(tick=None):

        if tick:
            tick = int(tick)
            g.Cyc.tick_set(tick)
        else:
            tick = g.Cyc.tick
            return '<@> tick is at '+str(tick)

    def time(h=None,m=None):

        if not h and not m:
            return '<@> time is '+str(g.Cyc)

        return '<@> not coded yet ^^*'

        tick = int(tick)
        g.Cyc.tick_set(tick)

    def cheat():
        return '<@> well tried .. but try harder (cheh)'

    # general
    def quit():
        plume.app.get_out()
        return 'error'

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

    def roll_activate(self,window=None,cmd=False):
        if not self.activated:
            self.bg = g.sman.addCol('black_faded',box(w=g.scr.w,h=g.scr.h),group='up-1')

            # Rectangular outline
            pad = 2
            font = self.document.get_font()
            height = font.ascent - font.descent

            self.rect = g.sman.addCol('black_faded',box(x=self.x-2 , y=self.y-3*self.size - 2 , w=3*g.scr.w//4 + 2,h=height + 2),group='up-1')

            self.activated = True
            pyglet.clock.schedule_once(window.set_focus,0.2,self)
            if cmd: self.document.text = '/'
            self.caret.position = len(self.document.text)
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
            self.perso = hum

            txt = self.document.text
            if len(txt) > 0 and txt[0] == '/':

                command = txt[1:]

                par = command.split(' ')
                while '' in par:
                    par.remove('')

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

                    if CMD_TRY:# là on try:
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
                            self.colorsay('red','error in the cmd')
                            return

                    else:# là on try pas

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
            else:
                #self.say('<'+hum.name+'>',self.document.text)
                hum.say(self.document.text)

            if self.document.text in self.input_historic:
                self.input_historic.remove(self.document.text)
            self.input_historic.append(self.document.text)
            self.document.text = ''

    def enter_say(self,thg,hum,color=None):
        if color:
            self.colorsay(color,'<'+hum.name+'>',thg)
        else:
            self.say('<'+hum.name+'>',thg)

    def say(self,*args):

        args = [str(x) for x in args]
        cmd = ' '.join(args)
        print(*args)
        self.historic.append(cmd)
        if self.visible:
            for id in self.ids:
                g.pman.modify_single(id,dy=self.size+2)
            id = g.pman.addLabPart(cmd,self.pos,self.dt,font_name=self.font,font_size=self.size,anchor=('left','center'),key='cmd',vis=self.visible,group='up',use_str_bien=False)
            self.ids.append(id)
            if len(self.ids) >= self.max_length:
                del self.ids[0]

    def colorsay(self,col,*args):

        args = [str(x) for x in args]
        cmd = ' '.join(args)


        self.historic.append(cmd)
        if self.visible:
            for id in self.ids:
                g.pman.modify_single(id,dy=self.size+2)
            id = g.pman.addLabPart(cmd,self.pos,self.dt,font_name=self.font,font_size=self.size,color=c[col],anchor=('left','center'),key='cmd',vis=self.visible,group='up',use_str_bien=False)
            self.ids.append(id)
            if len(self.ids) >= self.max_length:
                del self.ids[0]

        # on le dit aussi dans le print
        if col == 'orange':
            col = 'yellow'
        print(color(cmd,col))

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
            self.caret.position = len(self.document.text)

    def down(self):
        if self.point_input:
            self.point_input += 1
            if self.point_input < 0:
                self.document.text = self.input_historic[self.point_input]
                self.caret.position = len(self.document.text)
            else:
                self.point_input = None
                self.document.text = ''
                self.caret.position = len(self.document.text)

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
def enter_say(*args): Cmd.enter_say(*args)
