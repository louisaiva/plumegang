

import pyglet,time,random
from pyglet.window import key
import pyglet.gl as gl

from src.utils import *
from src.colors import *
import src.getsave as gs
from src import obj as o
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

        ##  TEXTURES

        self.create_organise_textures()

        ## SPRITES

        self.bgx,self.bgy = 0,250

        self.sprids = {}
        self.sprids['bg'] = g.sman.addSpr(g.TEXTIDS['bg'],(self.bgx,self.bgy),'back')
        g.sman.modify(self.sprids['bg'],scale=(1.5,1.5),group='back')

        ## PERSOS

        self.perso = o.Rappeur(g.TEXTIDS['persos'])
        #self.sprids['cred_bar'] =
        self.lab_doing = g.lman.addLab(self.perso.doing,(1880,1050),font_size=20,anchor=('right','top'))

        ## ZONES

        o.ZONES['ELEM']['ordi'] = o.Ordi(1400,225)
        o.ZONES['ELEM']['studio'] = o.Studio(-100,225)
        o.ZONES['ELEM']['plume'] = o.Market(600,225)
        o.ZONES['ELEM']['lit'] = o.Lit(900,225)


        ## items
        self.this_hud_caught_an_item = None

        ## ANCHOR

        #self.X,self.Y = 0,0

        ## END

        self.nb = 0
        self.gameover = False

        # labels

        self.fps = g.lman.addLab('FPS : 0',(20,1060),group='up',font_size=32,anchor=('left','top'))




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

    def create_organise_textures(self):

        g.TEXTIDS['persos'] = g.tman.loadImSeq('perso.png',(4,6))
        g.TEXTIDS['_son'] = g.tman.loadImSeq('son.png',(1,6))
        g.TEXTIDS['_phaz'] = g.tman.loadImSeq('phaz.png',(1,6))
        g.TEXTIDS['_instru'] = g.tman.loadImSeq('instru.png',(1,6))
        g.TEXTIDS['_plum'] = g.tman.loadImSeq('plum.png',(1,6))
        g.TEXTIDS['item'] = g.tman.loadImSeq('item.png',(6,6))

        qua = ['F','D','C','B','A','S']
        g.TEXTIDS['plume'] = {}
        for i in range(len(g.TEXTIDS['_plum'])):
            g.TEXTIDS['plume'][qua[i]] = g.TEXTIDS['_plum'][i]
        del g.TEXTIDS['_plum']

        g.TEXTIDS['phase'] = {}
        for i in range(len(g.TEXTIDS['_phaz'])):
            g.TEXTIDS['phase'][qua[i]] = g.TEXTIDS['_phaz'][i]
        del g.TEXTIDS['_phaz']

        g.TEXTIDS['instru'] = {}
        for i in range(len(g.TEXTIDS['_instru'])):
            g.TEXTIDS['instru'][qua[i]] = g.TEXTIDS['_instru'][i]
        del g.TEXTIDS['_instru']

        g.TEXTIDS['son'] = {}
        for i in range(len(g.TEXTIDS['_son'])):
            g.TEXTIDS['son'][qua[i]] = g.TEXTIDS['_son'][i]
        del g.TEXTIDS['_son']

        g.TEXTIDS['gui'] = g.tman.loadImSeq('gui.png',(2,2))
        g.TEXTIDS['bg'] = g.tman.loadIm('bg/bg'+str(random.randint(1,8))+'.png')



    ### ONCE FUNCTIONS

    def game_over(self):

        self.label_gameover = g.lman.addLab('GAME OVER',(1920/2,1080/2),anchor=('center','center'),font_size=200,color=c['darkkhaki'],group='up')
        self.label_gameover2 = g.lman.addLab('GAME OVER',(1920/2,1080/2),anchor=('center','center'),font_size=210,color=c['black'],group='up')

    def get_out(self):
        self.playing = False


    ### PYGLET FUNCTIONS

    def on_key_press(self,symbol,modifiers):

        self.longpress[symbol] = time.time()

        if symbol == key.ESCAPE:
            if self.perso.element_colli != None and self.perso.element_colli.activated:
                self.perso.element_colli.close(self.perso)
                return pyglet.event.EVENT_HANDLED

        elif symbol == key.A:
            self.perso.drop_plume()

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

        elif symbol == key.E:
            if self.perso.element_colli != None:
                if not self.perso.element_colli.longpress:
                    self.perso.element_colli.activate(self.perso)
                    self.perso.do('hit')
            else:
                self.perso.do('hit')

        elif symbol == key.X:
            self.perso.hud.rollhide()

        elif symbol == key.B:
            print(self.perso.invhud)
            print(self.perso.plume)

        elif symbol == key.I:
            self.perso.invhud.rollhide()

    def on_key_release(self,symbol,modifiers):

        if symbol in self.longpress:
            del self.longpress[symbol]

    def on_close(self):

        print('\n\nNumber of lines :',compt(self.path))
        gs.save_files(self.path)

    def on_mouse_motion(self,x,y,dx,dy):

        ## CHECK ALL UI

        # plumUI
        if self.perso.plume != None and self.perso.plume.hud.ui.visible and self.this_hud_caught_an_item == None:
            self.perso.plume.hud.ui.check_mouse(x,y)

        #phaseUI

        for zone in o.ZONES['ELEM']:
            if o.ZONES['ELEM'][zone].activated:

                if zone == 'lit':
                    if o.ZONES['ELEM']['lit'].hud.ui != None :
                        if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == o.ZONES['ELEM']['lit'].hud) : #check si il a caught

                            o.ZONES['ELEM']['lit'].hud.ui.check_mouse(x,y)
                            if o.ZONES['ELEM']['lit'].hud.ui.caught:
                                    o.ZONES['ELEM']['lit'].hud.ui.move(x,y)

        if self.this_hud_caught_an_item == self.perso.invhud and self.perso.invhud.item_caught == None:
            self.this_hud_caught_an_item = None

        # inventUI
        if self.perso.invhud.visible:
            if self.this_hud_caught_an_item == None:
                self.perso.invhud.check_hoover(x,y)
            elif self.this_hud_caught_an_item == self.perso.invhud:
                for uitype in self.perso.invhud.inventory:
                    for ui in self.perso.invhud.inventory[uitype]:
                        if ui.caught:
                            ui.move(x,y)
                            ui.check_mouse(x,y)

    def on_mouse_press(self,x, y, button, modifiers):

        letsbacktnothingcaught = False

        ## CHECK ALL UI

        # plumUI
        if self.perso.plume != None and self.perso.plume.hud.ui.visible and self.this_hud_caught_an_item == None:
            self.perso.plume.hud.ui.check_pressed()

        #phaseUI

        for zone in o.ZONES['ELEM']:
            if o.ZONES['ELEM'][zone].activated:

                if zone == 'lit':
                    if o.ZONES['ELEM']['lit'].hud.ui != None :
                        if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == o.ZONES['ELEM']['lit'].hud) : #check si il peut catch

                            caught_dropped = o.ZONES['ELEM']['lit'].hud.catch_or_drop(x,y,self.perso)

                            if caught_dropped == 1: # means caught
                                self.this_hud_caught_an_item = o.ZONES['ELEM']['lit'].hud
                            elif caught_dropped == -1: # means dropped
                                letsbacktnothingcaught = True

                            self.on_mouse_motion(x,y,0,0)

        # inventUI
        if self.perso.invhud.visible:

            if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == self.perso.invhud) : #check si il peut catch

                caught_dropped = self.perso.invhud.catch_or_drop(x,y)

                if caught_dropped == 1: # means caught
                    self.this_hud_caught_an_item = self.perso.invhud
                elif caught_dropped == -1: # means dropped
                    self.this_hud_caught_an_item = None

                self.on_mouse_motion(x,y,0,0)

        if letsbacktnothingcaught:
            self.this_hud_caught_an_item = None

    ### LOOP

    def events(self):

        if not self.gameover:

            if self.keys[key.Q]:
                self.perso.move('L')
            if self.keys[key.D]:
                self.perso.move('R')

            if self.keys[key.E]:
                if self.perso.element_colli != None:
                    if self.perso.element_colli.longpress:
                        if time.time() - self.longpress[key.E] > self.cooldown:
                            self.longpress[key.E] = time.time()
                            self.perso.element_colli.activate(self.perso)
                            self.perso.do('hit')

        if self.keys[key.LEFT]:
            g.Cam.morex()

        if self.keys[key.RIGHT]:
            g.Cam.lessx()

    def draw(self):

        g.tman.draw()

    def refresh(self):

        ## labels

        g.lman.set_text(self.fps,'FPS : '+str(int(pyglet.clock.get_fps())))

        ## anchor / moving sprites

        for zone in o.ZONES['ELEM']:
            zone=o.ZONES['ELEM'][zone]
            x_r = zone.gex + g.Cam.X
            y_r = zone.gey + g.Cam.Y
            g.sman.modify(zone.skin_id,(x_r,y_r))
            zone.update()

        x_r = self.perso.gex + g.Cam.X
        y_r = self.perso.gey + g.Cam.Y
        g.sman.modify(self.perso.skin_id,(x_r,y_r))

        x_bg,y_bg = self.bgx+g.Cam.BGX,g.Cam.BGY+self.bgy
        g.sman.modify(self.sprids['bg'],(x_bg,y_bg))

        g.Cam.update(self.perso.realbox)


        ## perso

        self.perso.check_do()
        g.lman.set_text(self.lab_doing,self.perso.doing)
        self.perso.hud.update()

        if self.perso.money <= 0:
            #print('game over')
            self.gameover = True
            self.game_over()
        else:
            self.perso.add_money(-1)
            self.perso.nb_fans += random.randint(1*(self.perso.money//1000),10*(self.perso.money//1000))

    def gameloop(self,dt):

        if self.playing:
            if self.nb == 0:



                self.nb += 1

            # EVENTS
            self.events()

            gl.glClearColor(1/4,1/4,1/4,1)
            # CLR
            self.window.clear()

            # RFRSH
            self.refresh()

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
