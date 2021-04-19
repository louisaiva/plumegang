

import pyglet
from pyglet.window import key

from src.utils import *
import src.getsave as gs

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

        display = pyglet.canvas.get_display()
        self.screens = display.get_screens()
        used_screen = self.get_current_screen()

        ### managers

        self.manager = graphic.MainManager(CURRENT_PATH)
        self.group_manager = graphic.GroupManager()
        self.graphic = graphic.GraphManager(self.manager,self.group_manager)
        self.labman = graphic.LabelManager(self.manager,self.group_manager,self.font[0])
        #self.cmd = graphic.CmdManager((20 , self.size_fullscr[1] - 50))
        #self.specMan = graphic.SpecialManager(self.manager,self.current_size_scr)

        #self.aff_cmd = False

    def init(self):

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

    def draw(self):
        pass

    def gameloop(self,dt):


        if self.playing:

            self.window.clear()
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
