

import pyglet
from pyglet.window import key

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

        #self.size_scr = 1000,800
        #self.window.set_size(self.size_scr[0],self.size_scr[1])

        self.window.set_fullscreen()

        self.window.push_handlers(self)

        ### screens

        """display = pyglet.canvas.get_display()
        self.screens = display.get_screens()
        used_screen = self.get_current_screen()
        """

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

        self.manager = g.MainManager(CURRENT_PATH)
        self.group_manager = g.GroupManager()
        self.graphic = g.GraphManager(self.manager,self.group_manager)
        self.labman = g.LabelManager(self.manager,self.group_manager,self.font[0])
        #self.cmd = graphic.CmdManager((20 , self.size_fullscr[1] - 50))
        #self.specMan = graphic.SpecialManager(self.manager,self.current_size_scr)

        #self.aff_cmd = False

    def init(self):

        ## SPRITES / TEXTURES

        self.textids = {}

        self.textids['persos'] = self.manager.loadImSeq('perso.png',(3,9))


        self.sprids = {}

        ## PERSOS

        self.perso = obj.Rappeur(self.textids['persos'][0],self.graphic)


        ## END

        self.playing = True

        pyglet.clock.schedule_interval(self.gameloop,0.0000001)
        pyglet.app.run()


    ### ONCE FUNCTIONS

    def get_out(self):
        self.playing = False


    ### PYGLET FUNCTIONS

    def on_key_press(self,symbol,modifiers):

        if symbol == key.A:
            self.get_out()

    def on_close(self):

        print('\n\nNumber of lines :',compt(self.path))
        gs.save_files(self.path)



    ### LOOP

    def events(self):

        if self.keys[key.Z]:
            self.perso.move([0,1],self.keys[key.LSHIFT],self.keys[key.SPACE])
        if self.keys[key.S]:
            self.perso.move([0,-1],self.keys[key.LSHIFT],self.keys[key.SPACE])
        if self.keys[key.Q]:
            self.perso.move([-1,0],self.keys[key.LSHIFT],self.keys[key.SPACE])
        if self.keys[key.D]:
            self.perso.move([1,0],self.keys[key.LSHIFT],self.keys[key.SPACE])


    def draw(self):

        self.manager.draw()

    def gameloop(self,dt):


        if self.playing:

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
