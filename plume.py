

import pyglet,time
from pyglet.window import key
import pyglet.gl as gl

from src.utils import *
import src.getsave as gs
from src import obj
from src import graphic as g

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) # fopatouché
if ' ' in CURRENT_PATH:
    print('Le chemin d\'acces contient un espace. Le programme va BUGUER SA MERE.')
    print('Changez le programme de place pour un path sans espace svp.')



class App():

    ### INIT FUNCTIONS

    def __init__(self):

        self.path = CURRENT_PATH

        ### windows

        self.window = pyglet.window.Window()

        self.window.set_fullscreen()

        self.window.push_handlers(self)

        ### loading fonts
        font_path = 'item/fonts/'
        self.fonts = ['RaubFont']
        self.font = ['RaubFont']
        for ft in self.fonts:
            try:
                pyglet.resource.add_font(font_path+ft+'.otf')
            except:
                try:
                    pyglet.resource.add_font(font_path+ft+'.ttf')
                except :
                    pyglet.resource.add_font('arial.ttf')

        ### managers

        #g.init_managers(CURRENT_PATH,self.font)

        g.lman.updateman(self.font[0])

        #self.cmd = graphic.CmdManager((20 , self.size_fullscr[1] - 50))
        #self.specMan = graphic.SpecialManager(g.tman,self.current_size_scr)

        #self.aff_cmd = False

    def init(self):

        ## SPRITES / TEXTURES

        self.textids = {}

        self.textids['persos'] = g.tman.loadImSeq('perso.png',(3,9))
        self.textids['son'] = g.tman.loadImSeq('son.png',(1,6))
        self.textids['phaz'] = g.tman.loadImSeq('phaz.png',(1,6))
        self.textids['instru'] = g.tman.loadImSeq('instru.png',(1,6))
        self.textids['plum'] = g.tman.loadImSeq('plum.png',(1,6))

        qua = ['F','D','C','B','A','S']
        self.textids['plume'] = {}
        for i in range(len(self.textids['plum'])):
            self.textids['plume'][qua[i]] = self.textids['plum'][i]
        del self.textids['plum']

        self.textids['gui'] = g.tman.loadImSeq('gui.png',(2,2))
        self.textids['bg'] = g.tman.loadIm('bg/bg'+str(random.randint(1,8))+'.png')


        self.sprids = {}
        self.sprids['bg'] = g.sman.addSpr(self.textids['bg'],(0,250))
        g.sman.modify(self.sprids['bg'],scale=(1.5,1.5))
        g.sman.addToGroup(self.sprids['bg'],'back')

        ## PERSOS

        self.perso = obj.Rappeur(self.textids['persos'][0],self.textids['plume'])
        #self.sprids['cred_bar'] =


        ## END

        # keys
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        self.longpress = {}
        self.cooldown = 0.5

        # clicks
        self.clicks = {'L':False,'R':False,'M':[0,0]}
        self.mouse_speed = 0


        self.playing = True

        pyglet.clock.schedule_interval(self.gameloop,0.0000001)
        pyglet.app.run()


    ### ONCE FUNCTIONS

    def get_out(self):
        self.playing = False


    ### PYGLET FUNCTIONS

    def on_key_press(self,symbol,modifiers):

        self.longpress[symbol] = time.time()

        if symbol == key.ESCAPE:
            print('wesh')

        #affiche les différents OrderedGroup d'affichage
        elif symbol == key.G:

            print('\nYOU ASKED TO PRINT GROUPS AND THEIR ORGANISATION:')
            print('  will be displayed in descending order like that : order,name\n')

            tab = []
            orders_sorted = sorted(g.gman.names_wo,reverse=True)

            for order in orders_sorted:
                say = str(order)
                say += (6-len(say))*' '
                say +=g.gman.names_wo[order]
                print(say)
            print('')

    def on_key_release(self,symbol,modifiers):

        if symbol in self.longpress:
            del self.longpress[symbol]

    def on_close(self):

        print('\n\nNumber of lines :',compt(self.path))
        gs.save_files(self.path)

    ### LOOP

    def events(self):

        if self.keys[key.Q]:
            self.perso.move('R')
        if self.keys[key.D]:
            self.perso.move('L')

        if self.keys[key.E]:
            if time.time() - self.longpress[key.E] > self.cooldown:
                self.longpress[key.E] = time.time()
                self.perso.rplum()

    def draw(self):

        g.tman.draw()

    def gameloop(self,dt):

        if self.playing:

            # EVENTS
            self.events()

            gl.glClearColor(1/4,1/4,1/4,1)
            # CLR
            self.window.clear()

            # RFRSH

            # DRW
            self.draw()

        else:
            print('\n\nNumber of lines :',compt(self.path))
            gs.save_files(self.path)

            self.window.close()


def main():

    app = App()
    app.init()

if __name__ == '__main__':
    main()
