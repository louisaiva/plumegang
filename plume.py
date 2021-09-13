"""
CODED by deltasfer
enjoy
"""


import pyglet,time,random
from pyglet.window import key
import pyglet.gl as gl

from src.utils import *
from src.colors import *
import src.names as names
import src.getsave as gs
from src import obj as o
from src import perso as p
from src import obj2 as o2
from src import graphic as g
from src import menu as m

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__)) # fopatouché
if ' ' in CURRENT_PATH:
    print('Le chemin d\'acces contient un espace. Le programme va BUGUER SA MERE.')
    print('Changez le programme de place pour un path sans espace svp.')

ESK_QUIT = 0
## pour éviter d'avoir à passer par le menu
FILL_INV = 1
## pour remplir ou non l'inventaire au debut

class App():

    ### INIT FUNCTIONS

    def __init__(self):

        self.path = CURRENT_PATH

        ### windows

        self.window = pyglet.window.Window(screen=g.scr.screen)

        self.window.set_fullscreen()

        self.window.push_handlers(self)
        #self.window.screen = self.get_current_screen()

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

        #pyglet.clock.set_fps_limit(None)

        ### managers

        #g.init_managers(CURRENT_PATH,self.font)

        g.lman.updateman(self.font[0])

        #self.cmd = graphic.CmdManager((20 , self.size_fullscr[1] - 50))
        #self.specMan = graphic.SpecialManager(g.tman,self.current_size_scr)

        #self.aff_cmd = False

    def init(self):

        ##  TEXTURES

        self.create_organise_textures()

        ## Cursor
        #image = pyglet.image.load('cursor.png')
        g.Cur.init(self.window,g.TEXTIDS['utils'])

        ## SPRITES

        self.bgx,self.bgy = 0,250
        self.bg1dx = 0
        self.bgdx = 0

        self.sprids = {}
        self.sprids['bg-1'] = g.sman.addSpr(g.TEXTIDS['bg-1'],(self.bgx,self.bgy),'back-1')
        g.sman.modify(self.sprids['bg-1'],scale=(0.75,0.75))
        self.sprids['bg.1'] = g.sman.addSpr(g.TEXTIDS['bg'],(self.bgx,self.bgy),'back')
        g.sman.modify(self.sprids['bg.1'],scale=(0.75,0.75))
        self.sprids['bg.2'] = g.sman.addSpr(g.TEXTIDS['bg'],(self.bgx+g.sman.spr(self.sprids['bg.1']).width,self.bgy),'back')
        g.sman.modify(self.sprids['bg.2'],scale=(0.75,0.75))

        self.sprids['bg1.1'] = g.sman.addSpr(g.TEXTIDS['bg1'],(self.bgx,self.bgy),'back1')
        g.sman.modify(self.sprids['bg1.1'],scale=(1.2,1.2))
        self.sprids['bg1.2'] = g.sman.addSpr(g.TEXTIDS['bg1'],(self.bgx+g.sman.spr(self.sprids['bg1.1']).width,self.bgy),'back1')
        g.sman.modify(self.sprids['bg1.2'],scale=(1.2,1.2))
        #self.sprids['bgmid'] = g.sman.addSpr(g.TEXTIDS['bgmid'],(-1000,-50),'mid-1')
        #g.sman.modify(self.sprids['bg1.2'],scale=(1.2,1.2))

        ## sprites effects

        self.sprids['effects'] = {}
        sizes = []
        for scr in g.scr.screens:
            if (scr.width,scr.height) not in sizes:
                sizes.append((scr.width,scr.height))

        for size in sizes:
            self.sprids['effects'][size] = g.sman.addSpr(g.TEXTIDS['blur'],group='up-1',vis=False)
            g.sman.modify(self.sprids['effects'][size],scale=size,opacity=150)

        print(self.sprids['effects'])


        ## STREETS
        o2.generate_map()

        ## PERSOS

        self.perso = p.Perso(g.TEXTIDS['persos'],fill=FILL_INV)
        o2.NY.CITY['home'].set_owner(self.perso)
        #self.sprids['cred_bar'] =
        self.lab_doing = g.lman.addLab(self.perso.doing,(1880,1050),font_size=20,anchor=('right','top'))

        #p.BOTS = []
        n = 30*len(o2.NY.CITY)
        print(n,'bots in this game !')
        for i in range(n):
            street = o2.NY.rand_street()
            pos = (random.randint(0,street.rxf),random.randint(105,175))

            if random.random() < 1/8 and len(names.rappeurs) > 0:
                p.BOTS.append(p.Rappeur(g.TEXTIDS['persos'],pos,street=street.name))
            else:
                p.BOTS.append(p.Fan(g.TEXTIDS['persos'],pos,street=street.name))

        for hum in p.BOTS:
            if hum.street != 'ghost':
                o2.NY.CITY[hum.street].add_hum(hum)
            else:
                o2.NY.Ghost.add_hum(hum)

        ## cycle

        self.cycle = g.Cycle(self.perso)

        ## ZONES

        zones = []
        zones.append(o.Ordi(1990,150,self.perso))
        zones.append(o.Studio(2640,225))
        zones.append(o.Market(450,210))
        zones.append(o.Lit(-600,225))
        o2.NY.CITY['home'].assign_zones(zones)

        zones = []
        zones.append(o.Distrib(2900,225))
        street = o2.NY.rand_street().name
        o2.NY.CITY[street].assign_zones(zones)
        print('let\'s find the',street,'!')

        o2.NY.CITY[self.perso.street].load()


        ## items
        self.this_hud_caught_an_item = None

        ## END

        self.tick = 0
        self.day = 0
        self.duree_day = 60 # en secondes
        self.gameover = False

        # menu
        self.create_menu()

        # labels

        self.lab_fps = g.lman.addLab('FPS : 0',(20,1060),group='up',font_size=32,anchor=('left','top'))
        self.lab_day = g.lman.addLab('DAY : 0',(20,1060-50),group='up',font_size=32,anchor=('left','top'))
        self.lab_street = g.lman.addLab('home',(20,1060-50-32),group='up',font_size=20,anchor=('left','top'))




        # keys
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)
        self.longpress = {}
        self.cooldown = 0.5

        # clicks
        self.clicks = {'L':False,'R':False,'M':[0,0]}
        self.mouse_speed = 0

        # final
        self.action = "play" # play pause
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
        g.TEXTIDS['utils'] = g.tman.loadImSeq('utils.png',(8,8))
        #g.TEXTIDS['gui'] = g.tman.loadImSeq('gui.png',(8,8))

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
        g.TEXTIDS['bg-1'] = g.tman.loadIm('bg/bg-1'+'.png')
        g.TEXTIDS['bg'] = g.tman.loadIm('bg/bg'+'.png')
        g.TEXTIDS['bg1'] = g.tman.loadIm('bg/bg1'+'.png')
        g.TEXTIDS['bgmid'] = g.tman.loadIm('bg/bg2'+'.png')
        g.TEXTIDS['bgup'] = g.tman.loadIm('bg/bg3'+'.png')
        g.TEXTIDS['street1_bg'] = g.tman.loadIm('bg/street1_bg'+'.png')

        ##

        g.TEXTIDS['steam'] = g.tman.addCol(20,20,c['lightgrey'])
        g.TEXTIDS['steam2'] = g.tman.addCol(50,50,c['grey'])

        ## huds
        g.TEXTIDS['studhud'] = g.tman.loadIm('studhud.png')
        g.TEXTIDS['ordhud'] = g.tman.loadIm('ordhud.png')

        ## effects
        g.TEXTIDS['blur'] = g.tman.addCol(1,1,c['black'])

    def get_current_screen(self):

        x,y = self.window.get_location()
        for i in range(len(self.screens)):
            scr = self.screens[i]
            if (x >= scr.x and x <= scr.x + scr.width) and (y >= scr.y and y <= scr.y + scr.height):
                return scr
        return self.screens[0]

    def create_menu(self):

        self.menu = m.Menu()
        self.menu_fonct = {'play':self.change_action,'quit':self.get_out,'go home':self.perso.tp}
        self.menu_args = {'play':['play'],'go home':[0,None,o2.NY.CITY['home']]}

    def apply_menu(self,res):

        if res:
            if type(res) == type((0,1)):
                for thg in res:
                    self.apply_menu(thg)
            else:
                if res in self.menu_fonct and res in self.menu_args:
                    self.menu_fonct[res](*self.menu_args[res])
                elif res in self.menu_fonct:
                    self.menu_fonct[res]()
                else:
                    print('click',res)


    ### ONCE FUNCTIONS

    def game_over(self):

        self.label_gameover = g.lman.addLab('GAME OVER',(1920/2,1080/2),anchor=('center','center'),font_size=200,color=c['darkkhaki'],group='up')
        self.label_gameover2 = g.lman.addLab('GAME OVER',(1920/2,1080/2),anchor=('center','center'),font_size=210,color=c['black'],group='up')

        g.bertran.set_speed(0,0)

    def get_out(self):
        self.playing = False

    def change_action(self,act='play'):

        size_scr = (self.window.screen.width,self.window.screen.height)
        if act == "pause":
            g.sman.unhide(self.sprids['effects'][size_scr])
            self.menu.unhide()
            g.bertran.set_speed(0,0)
        else:
            g.sman.unhide(self.sprids['effects'][size_scr],True)
            self.menu.unhide(True)
            g.bertran.set_speed(0,1)

        self.action = act
        #print('go',act)

        #self.perso.pause(act)


    ### PYGLET FUNCTIONS

    def on_key_press(self,symbol,modifiers):

        if self.action == "play":

            self.longpress[symbol] = time.time()

            if symbol == key.ESCAPE:
                if self.perso.element_colli != None and type(self.perso.element_colli) not in [p.Human,p.Fan,p.Rappeur,p.Perso] and self.perso.element_colli.activated:
                    self.perso.element_colli.close(self.perso)
                    return pyglet.event.EVENT_HANDLED
                else:
                    self.change_action('pause')
                    if not ESK_QUIT:
                        return pyglet.event.EVENT_HANDLED
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

            elif symbol == key.B:
                print(self.perso.invhud)
                print(self.perso.plume)

            if self.perso.alive:

                if symbol == key.A:
                    self.perso.drop_plume()

                elif symbol == key.E:
                    if self.perso.element_colli != None:

                        if type(self.perso.element_colli) in [p.Human,p.Fan,p.Rappeur,p.Perso]:
                            if self.perso.element_colli.alive:
                                self.perso.element_colli.do('hit')
                                self.perso.be_hit(self.perso.element_colli)
                            self.perso.do('hit')
                            self.perso.element_colli.be_hit(self.perso)
                        else:
                            if not self.perso.element_colli.longpress:
                                if type(self.perso.element_colli) == o.Porte:
                                    self.perso.element_colli.activate(self.perso)
                                else:
                                    self.perso.element_colli.activate(self.perso)
                                self.perso.do('hit')
                    else:
                        self.perso.do('hit')

                elif symbol == key.X:
                    self.perso.hud.rollhide()

                elif symbol == key.I:
                    self.perso.invhud.rollhide()

                elif symbol == key.F:

                    choiced_son = None
                    for son in self.perso.invhud.inventory['son']:
                        if not son.item._released:
                            choiced_son = son.item
                            break
                    if choiced_son != None:
                        self.perso.release_son(choiced_son,p.BOTS,self.cycle.day)


                elif symbol == key.M:
                    self.perso.bigmap.rollhide()

                elif symbol == key.K:
                    self.perso.speak()


        elif self.action == 'pause':

            if symbol == key.ESCAPE:
                res = self.menu.unclick()
                self.apply_menu(res)
                if not ESK_QUIT:
                    return pyglet.event.EVENT_HANDLED

            elif symbol == key.BACKSPACE:
                res = self.menu.unclick()
                self.apply_menu(res)
                return pyglet.event.EVENT_HANDLED

            elif symbol == key.ENTER:
                res = self.menu.click()
                self.apply_menu(res)

            elif symbol == key.UP:
                self.menu.up()

            elif symbol == key.DOWN:
                self.menu.down()

    def on_key_release(self,symbol,modifiers):

        if symbol in self.longpress:
            del self.longpress[symbol]

    def on_close(self):

        print('\n\nNumber of lines :',compt(self.path))
        gs.save_files(self.path)

    def on_mouse_motion(self,x,y,dx,dy):
        g.M = [x,y]

        if self.action == "play":
            ## CHECK ALL UI
            #print(self.this_hud_caught_an_item)

            # plumUI
            if self.perso.plume != None and self.perso.plumhud.ui.visible and self.this_hud_caught_an_item == None:
                self.perso.plumhud.ui.check_mouse(x,y)

            # lifeUI
            if self.perso.lifehud.ui.visible and self.this_hud_caught_an_item == None:
                self.perso.lifehud.ui.check_mouse(x,y)

            # credUI
            if self.perso.credhud.ui.visible and self.this_hud_caught_an_item == None:
                self.perso.credhud.ui.check_mouse(x,y)

            #phaseUI

            for zone in o2.NY.CITY[self.perso.street].zones:

                if zone == 'studio' and self.this_hud_caught_an_item == o2.NY.CITY[self.perso.street].zones['studio'].hud and o2.NY.CITY[self.perso.street].zones['studio'].hud.item_caught == None:
                    self.this_hud_caught_an_item = None

                if zone == 'ordi' and self.this_hud_caught_an_item == o2.NY.CITY[self.perso.street].zones['ordi'].hud and o2.NY.CITY[self.perso.street].zones['ordi'].hud.item_caught == None:
                    self.this_hud_caught_an_item = None

                if o2.NY.CITY[self.perso.street].zones[zone].activated:

                    if zone == 'lit':
                        if o2.NY.CITY[self.perso.street].zones['lit'].hud.ui != None :
                            if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == o2.NY.CITY[self.perso.street].zones['lit'].hud) : #check si il a caught

                                o2.NY.CITY[self.perso.street].zones['lit'].hud.ui.check_mouse(x,y)
                                if o2.NY.CITY[self.perso.street].zones['lit'].hud.ui.caught:
                                        o2.NY.CITY[self.perso.street].zones['lit'].hud.ui.move(x,y)

                    if zone == 'studio':
                        if self.this_hud_caught_an_item == None:
                            for lab in o2.NY.CITY[self.perso.street].zones['studio'].hud.uis:
                                ui = o2.NY.CITY[self.perso.street].zones['studio'].hud.uis[lab]
                                if ui != None :
                                    ui.check_mouse(x,y)

                        elif self.this_hud_caught_an_item == o2.NY.CITY[self.perso.street].zones['studio'].hud: #check si il a caught
                            if o2.NY.CITY[self.perso.street].zones['studio'].hud.item_caught != None:
                                ui = o2.NY.CITY[self.perso.street].zones['studio'].hud.item_caught
                                ui.check_mouse(x,y)
                                if ui.caught:
                                        ui.move(x,y)

                    if zone == 'ordi':
                        if self.this_hud_caught_an_item == None:
                            for lab in o2.NY.CITY[self.perso.street].zones['ordi'].hud.uis:
                                ui = o2.NY.CITY[self.perso.street].zones['ordi'].hud.uis[lab]
                                if ui != None :
                                    ui.check_mouse(x,y)

                        elif self.this_hud_caught_an_item == o2.NY.CITY[self.perso.street].zones['ordi'].hud: #check si il a caught
                            if o2.NY.CITY[self.perso.street].zones['ordi'].hud.item_caught != None:
                                ui = o2.NY.CITY[self.perso.street].zones['ordi'].hud.item_caught
                                ui.check_mouse(x,y)
                                if ui.caught:
                                        ui.move(x,y)

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

            #print(self.this_hud_caught_an_item)

    def on_mouse_press(self,x, y, button, modifiers):

        if self.action == "play":
            letsbacktnothingcaught = False

            ## CHECK ALL UI

            # plumUI
            if self.perso.plume != None and self.perso.plumhud.ui.visible and self.this_hud_caught_an_item == None:
                self.perso.plumhud.ui.check_pressed()

            #phaseUI
            for zone in o2.NY.CITY[self.perso.street].zones:
                if o2.NY.CITY[self.perso.street].zones[zone].activated:

                    if zone == 'lit':
                        if o2.NY.CITY[self.perso.street].zones['lit'].hud.ui != None :
                            if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == o2.NY.CITY[self.perso.street].zones['lit'].hud) : #check si il peut catch

                                caught_dropped = o2.NY.CITY[self.perso.street].zones['lit'].hud.catch_or_drop(x,y,self.perso)

                                if caught_dropped == 1: # means caught
                                    self.this_hud_caught_an_item = o2.NY.CITY[self.perso.street].zones['lit'].hud
                                elif caught_dropped == -1: # means dropped
                                    letsbacktnothingcaught = True

                                self.on_mouse_motion(x,y,0,0)

                    elif zone == 'studio':
                        if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == o2.NY.CITY[self.perso.street].zones['studio'].hud) : #check si il peut catch
                            caught_dropped = o2.NY.CITY[self.perso.street].zones['studio'].hud.catch_or_drop(x,y,self.perso)

                            if caught_dropped == 1: # means caught
                                self.this_hud_caught_an_item = o2.NY.CITY[self.perso.street].zones['studio'].hud
                            elif caught_dropped == -1: # means dropped
                                letsbacktnothingcaught = True

                            #self.on_mouse_motion(x,y,0,0)

                    elif zone == 'ordi':
                        if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == o2.NY.CITY[self.perso.street].zones['ordi'].hud) : #check si il peut catch

                            if o2.NY.CITY[self.perso.street].zones['ordi'].hud.uis['main'] != None and self.perso not in o2.NY.CITY[self.perso.street].zones['ordi'].hud.uis['main'].item.owners:
                                g.Cur.start_long_press(o2.NY.CITY[self.perso.street].zones['ordi'].hud.uis['main'].box,o2.NY.CITY[self.perso.street].zones['ordi'].hud.buy_instru)


                            caught_dropped = o2.NY.CITY[self.perso.street].zones['ordi'].hud.catch_or_drop(x,y)

                            if caught_dropped == 1: # means caught
                                self.this_hud_caught_an_item = o2.NY.CITY[self.perso.street].zones['ordi'].hud
                            elif caught_dropped == -1: # means dropped
                                letsbacktnothingcaught = True

                            #self.on_mouse_motion(x,y,0,0)

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

    def on_mouse_release(self,x,y,button,modifiers):
        g.Cur.reset()

    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        self.on_mouse_motion(x,y,dx,dy)


    ### LOOP

    def events(self):

        if self.action == "play":

            if not self.gameover:

                run = False
                if self.keys[key.LSHIFT]:
                    run = True

                ## moving perso
                if self.keys[key.Q]:
                    self.perso.move('L',o2.NY.CITY[self.perso.street],run)
                if self.keys[key.D]:
                    self.perso.move('R',o2.NY.CITY[self.perso.street],run)

                if self.keys[key.Z]:
                    self.perso.move('up',o2.NY.CITY[self.perso.street])
                if self.keys[key.S]:
                    self.perso.move('down',o2.NY.CITY[self.perso.street])

                ## moving freeze Corleone
                if self.perso.street == p.BOTS[0].street:
                    if self.keys[key.K]:
                        p.BOTS[0].move('L',o2.NY.CITY[self.perso.street])
                    if self.keys[key.M]:
                        p.BOTS[0].move('R',o2.NY.CITY[self.perso.street])

                if self.keys[key.E]:
                    if self.perso.element_colli != None and type(self.perso.element_colli) not in [p.Human,p.Fan,p.Rappeur,p.Perso]:
                        if self.perso.element_colli.longpress:
                            if time.time() - self.longpress[key.E] > self.cooldown:
                                self.longpress[key.E] = time.time()
                                self.perso.element_colli.activate(self.perso)
                                self.perso.do('hit')

            if self.keys[key.LEFT] or self.keys[key.RIGHT]:
                if self.keys[key.RIGHT]:
                    g.GodCam.activate('R')
                else:
                    g.GodCam.activate()
            else:
                g.GodCam.unactivate(self.perso)

    def draw(self):

        g.tman.draw()

    def refresh(self):

        #print(g.Cam.X)


        ## FPS
        dt = time.time() - self.lab_fps_time
        self.lab_fps_time = time.time()
        try:
            self.lab_fps1.append(int(1/dt))

            if len(self.lab_fps1) > 10:
                del self.lab_fps1[0]dqdqd
            moyfps = int(sum(self.lab_fps1)/len(self.lab_fps1))
            g.lman.set_text(self.lab_fps,'FPS : '+str(moyfps))
        except : pass

        if self.action == "play":

            # STREETS
            g.lman.set_text(self.lab_street,self.perso.street)

            # DAYS
            g.lman.set_text(self.lab_day,'DAY : '+str(self.cycle.day))


            ## anchor / moving sprites

            if True:

                #--# zones elem
                for zone in o2.NY.CITY[self.perso.street].zones:
                    zone=o2.NY.CITY[self.perso.street].zones[zone]
                    x_r = zone.gex + g.Cam.X + g.GodCam.X
                    y_r = zone.gey + g.Cam.Y
                    #g.sman.modify(zone.skin_id,(x_r,y_r))
                    zone.move(x_r,y_r)

                #--# zones elem item
                for item in o2.NY.CITY[self.perso.street].items:
                    #item=o2.NY.CITY[self.perso.street].items[item]
                    x_r = item.gex + g.Cam.X + g.GodCam.X
                    y_r = item.gey + g.Cam.Y
                    #g.sman.modify(item.skin_id,(x_r,y_r))
                    item.move(x_r,y_r)

                #--# persos
                for hum in o2.NY.CITY[self.perso.street].humans + [self.perso]:
                    x_r = hum.gex + g.Cam.X + g.GodCam.X
                    y_r = hum.gey + g.Cam.Y
                    g.sman.modify(hum.skin_id,(x_r,y_r))
                    hum.update_lab()
                    hum.update()
                self.perso.check_colli(o2.NY.CITY[self.perso.street])


                #--# bg
                w = g.sman.spr(self.sprids['bg.1']).width
                x_bg1,y_bg1 = self.bgx+g.Cam.X*0.2 +self.bgdx + g.GodCam.X,g.Cam.Y*0.2 +self.bgy
                x_bg2,y_bg2 = self.bgx+g.Cam.X*0.2 +w +self.bgdx+ g.GodCam.X,g.Cam.Y*0.2 +self.bgy

                if x_bg1 >= 0:
                    self.bgdx -= w
                elif x_bg2 + w <= 1920:
                    self.bgdx += w

                g.sman.modify(self.sprids['bg.1'],(x_bg1,y_bg1))
                g.sman.modify(self.sprids['bg.2'],(x_bg2,y_bg2))

                #bg1
                w = g.sman.spr(self.sprids['bg1.1']).width
                x_bg1,y_bg1 = self.bgx+g.Cam.X*0.4 +self.bg1dx + g.GodCam.X,g.Cam.Y*0.4 +self.bgy
                x_bg2,y_bg2 = self.bgx+g.Cam.X*0.4 +w +self.bg1dx+ g.GodCam.X,g.Cam.Y*0.4 +self.bgy

                if x_bg1 >= 0:
                    self.bg1dx -= w
                elif x_bg2 + w <= 1920:
                    self.bg1dx += w

                g.sman.modify(self.sprids['bg1.1'],(x_bg1,y_bg1))
                g.sman.modify(self.sprids['bg1.2'],(x_bg2,y_bg2))
                o2.NY.CITY[self.perso.street].modify(g.Cam.X+ g.GodCam.X,g.Cam.Y)
                #g.sman.modify(self.sprids['bgmid'],(g.Cam.X-1000,-50+g.Cam.Y))

                g.Cam.update(self.perso.realbox,o2.NY.CITY[self.perso.street],self.keys[key.LSHIFT])

            if g.bertran.speed > 0:

                ## particles
                g.pman.modify('icons',dy=0.1)
                g.pman.modify('dmg',dy=0.1,dx=g.Cam.dx + g.GodCam.X)

                ## fans are streaming
                for i in range(len(self.perso.disco)):
                    chance = random.randint(0,int(60*moyfps))
                    malus = 1-i*0.2
                    if chance < self.perso.nb_fans*malus:
                        random.choice(p.BOTS).stream(self.perso.disco[i])


            ## perso

            for hum in o2.NY.CITY[self.perso.street].humans + [self.perso]:
                hum.check_do()
                #hum.update()
            g.lman.set_text(self.lab_doing,self.perso.doing)
            self.perso.hud.update()
            self.perso.bigmap.update()
            #print(self.perso.gex,self.perso.gey)

            if self.perso.money <= 0 or not self.perso.alive:
                #print('game over')
                self.gameover = True
                self.game_over()

    def gameloop(self,dt):

        if self.playing:
            if self.tick == 0:

                self.lab_fps_time = time.time()
                self.lab_fps1 = []

            self.tick += 1
            #print(self.tick)

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
