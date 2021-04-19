

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

        #super(App, self).__init__()
        self.window = pyglet.window.Window()

        self.size_scr = 1000,800
        self.window.set_size(self.size_scr[0],self.size_scr[1])

        #self.keys = key.KeyStateHandler()
        self.window.push_handlers(self)


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
