"""
CODED by deltasfer
enjoy
"""


import pyglet,time,random
from pyglet.window import key
import pyglet.gl as gl
import colorama
colorama.init()

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
FILL_INV = 0
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
        self.fonts = ['RaubFont','Bitter-Bold']
        self.font = ['Bitter','RaubFont']
        for ft in self.fonts:
            try:
                pyglet.resource.add_font(font_path+ft+'.otf')
            except:
                try:
                    pyglet.resource.add_font(font_path+ft+'.ttf')
                except :
                    pass

        ### managers
        g.lman.updateman(self.font)

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
        self.sprids['bg-1'] = g.sman.addSpr(g.TEXTIDS['bg-1'],(self.bgx,self.bgy),'sky')
        g.sman.modify(self.sprids['bg-1'],scale=(0.75,0.75))
        self.sprids['bg.1'] = g.sman.addSpr(g.TEXTIDS['bg'],(self.bgx,self.bgy),'bg_buildings_loin')
        g.sman.modify(self.sprids['bg.1'],scale=(0.75,0.75))
        self.sprids['bg.2'] = g.sman.addSpr(g.TEXTIDS['bg'],(self.bgx+g.sman.spr(self.sprids['bg.1']).width,self.bgy),'bg_buildings_loin')
        g.sman.modify(self.sprids['bg.2'],scale=(0.75,0.75))

        rect = box(0,0,g.scr.w,250)
        self.sprids['ground'] = g.sman.addCol(c['grey'],rect,'bg_buildings_proche')
        self.sprids['bg1.1'] = g.sman.addSpr(g.TEXTIDS['bg1'],(self.bgx,self.bgy),'bg_buildings_proche')
        g.sman.modify(self.sprids['bg1.1'],scale=(1.2,1.2))
        self.sprids['bg1.2'] = g.sman.addSpr(g.TEXTIDS['bg1'],(self.bgx+g.sman.spr(self.sprids['bg1.1']).width,self.bgy),'bg_buildings_proche')
        g.sman.modify(self.sprids['bg1.2'],scale=(1.2,1.2))
        #self.sprids['bgmid'] = g.sman.addSpr(g.TEXTIDS['bgmid'],(-1000,-50),'mid-1')
        #g.sman.modify(self.sprids['bg1.2'],scale=(1.2,1.2))

        #self.circle = g.sman.addCircle(g.scr.c,100,group='up')
        #cir = pyglet.shapes.Circle(g.scr.cx,g.scr.cy,100,batch=g.tman.batch)

        ## sprites effects

        self.sprids['effects'] = {}
        sizes = []
        for scr in g.scr.screens:
            if (scr.width,scr.height) not in sizes:
                sizes.append((scr.width,scr.height))

        for size in sizes:
            self.sprids['effects'][size] = g.sman.addSpr(g.TEXTIDS['blur'],group='up-1',vis=False)
            g.sman.modify(self.sprids['effects'][size],scale=size,opacity=150)

        #print(self.sprids['effects'])

        ## STREETS
        if o2.LOAD != 2:
            o2.generate_map()
        else:
            o2.generate_short_map()

        ## PERSOS

        self.perso = p.Perso(g.TEXTIDS['rap'],fill=FILL_INV)
        o2.NY.CITY['home'].set_owner(self.perso)

        #poto
        p.BOTS.append(p.Fan(g.TEXTIDS['perso3'],o2.NY.CITY['voisin'].rand_pos(),street='voisin'))
        o2.NY.CITY['voisin'].set_owner(p.BOTS[-1])
        self.perso.assign_poto(p.BOTS[-1])


        self.lab_doing = g.lman.addLab(self.perso.doing,(1880,1050),font_size=20,anchor=('right','top'))

        ## FANS/RAPPEURS

        # add hum to p.BOTS for each street
        for str in o2.NY.CITY:
            street = o2.NY.CITY[str]
            if street.name not in ['home','voisin']:
                n_str = street.get_random_nb_bots()
                for i in range(n_str):
                    pos = street.rand_pos()
                    if random.random() < 1/8 and len(names.rappeurs) > 0:
                        hum = p.Rappeur(g.TEXTIDS['rap'],pos,street=street.name)
                    else:
                        text = random.choice(['persos','perso2','perso3'])
                        hum = p.Fan(g.TEXTIDS[text],pos,street=street.name)
                    p.BOTS.append(hum)

        # adding all hum to their street
        for hum in p.BOTS:
            o2.NY.CITY[hum.street].add_hum(hum)

        print(len(p.BOTS),'bots in this game !')

        ## cycle

        tabcolor = [(self.sprids['bg-1'],1),
                    (self.sprids['bg.1'],0.9),
                    (self.sprids['bg.2'],0.9),
                    (self.sprids['bg1.1'],0.7),
                    (self.sprids['bg1.2'],0.7),
                    (self.sprids['ground'],0.7)]

        #g.Cyc = g.Cycle(self.perso,tabcolor)
        g.Cyc.launch(self.perso,tabcolor)

        ## ZONES

        # à la maison
        zones = []
        zones.append(o.Ordi(1990,0,self.perso))
        zones.append(o.Studio(2640,225))
        zones.append(o.Market(450,210))
        zones.append(o.Lit(-600,225))
        o2.NY.CITY['home'].assign_zones(zones)

        # ez cash
        zones = []
        zones.append(o.Distrib(2900,225))
        street = o2.NY.rand_street().name
        o2.NY.CITY[street].assign_zones(zones)
        print('let\'s find the',street,'!')

        # distrokid
        zones = []
        zones.append(o.SimpleReleaser(1670,210,o.distro))
        o2.NY.CITY['distrokid'].assign_zones(zones)


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

        self.lab_fps = g.lman.addLab('FPS : 0',(20,1060),group='up',font_name=1,font_size=32,anchor=('left','top'))
        self.lab_day = g.lman.addLab('DAY : 0',(20,1060-50),group='up',font_name=1,font_size=32,anchor=('left','top'))
        self.lab_street = g.lman.addLab('home',(20,1060-50-32),group='up',font_name=1,font_size=20,anchor=('left','top'))

        # keys
        g.keys = key.KeyStateHandler()
        self.window.push_handlers(g.keys)
        #g.longpress = {}
        #g.cooldown = 0.5

        # clicks
        self.clicks = {'L':False,'R':False,'M':[0,0]}
        self.mouse_speed = 0

        # final
        self.action = "play" # play pause
        self.playing = True

        pyglet.clock.schedule_interval(self.gameloop,0.0000001)
        pyglet.app.run()

    def create_organise_textures(self):

        ### PERSOS
        if True:
            g.TEXTIDS['persos'] = g.tman.loadImSeq('perso.png',(1,30))
            g.TEXTIDS['perso2'] = g.tman.loadImSeq('perso_2.png',(1,30))
            g.TEXTIDS['perso3'] = g.tman.loadImSeq('perso_3.png',(1,30))
            g.TEXTIDS['guys'] = g.tman.loadImSeq('guy.png',(1,30))
            g.TEXTIDS['rap'] = g.tman.loadImSeq('perso2.png',(1,40))

        # items
        if True:
            g.TEXTIDS['_son'] = g.tman.loadImSeq('son.png',(1,6))
            g.TEXTIDS['_phaz'] = g.tman.loadImSeq('phaz.png',(1,6))
            g.TEXTIDS['_instru'] = g.tman.loadImSeq('instru.png',(1,6))
            g.TEXTIDS['_plum'] = g.tman.loadImSeq('plum.png',(1,6))
            g.TEXTIDS['item'] = g.tman.loadImSeq('item.png',(6,6))
            g.TEXTIDS['utils'] = g.tman.loadImSeq('utils.png',(8,8))

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

        # BG
        if True:
            g.TEXTIDS['bg-1'] = g.tman.loadIm('bg/sky.png')
            g.TEXTIDS['bg'] = g.tman.loadIm('bg/bg'+'.png')
            g.TEXTIDS['bg1'] = g.tman.loadIm('bg/bg1'+'.png')

        # HOME
        if True:
            g.TEXTIDS['home'] = {}
            g.TEXTIDS['home']['back'] = g.tman.loadIm('bg/home/home_back'+'.png')
            g.TEXTIDS['home']['front'] = g.tman.loadIm('bg/home/home_front'+'.png')
            g.TEXTIDS['home']['frontanim'] = [g.tman.loadIm('bg/home/home_fanim'+str(i)+'.png') for i in range(1,5)]
            g.TEXTIDS['home']['backanim'] = [g.tman.loadIm('bg/home/home_banim'+str(i)+'.png') for i in range(1,5)]

        # DISTRO
        if True:
            g.TEXTIDS['distrokid'] = {}
            g.TEXTIDS['distrokid']['back'] = g.tman.loadIm('bg/distro/distrokid_shop.png')
            g.TEXTIDS['distrokid']['backanim'] = [g.tman.loadIm('bg/distro/distrokid_anim'+str(i)+'.png') for i in range(1,5)]

        # STREET
        if True:
            g.TEXTIDS['street'] = {}
            g.TEXTIDS['street']['road'] = g.tman.loadIm('bg/street_back.png')
            #g.TEXTIDS['street']['buildings'] = g.tman.loadIm('bg/building1.png')

        # INSIDE BUILDING
        if True:
            g.TEXTIDS['inside'] = {}
            g.TEXTIDS['inside']['back'] = g.tman.loadIm('bg/inside_building.png')


        ## BUILDINGS
        if True:
            g.TEXTIDS['build'] = {}

            #builds lambda
            b = g.tman.loadImSeq('bg/builds.png',(1,3))
            for i in range(len(b)):
                g.TEXTIDS['build'][i] = b[i]
                o2.builds_key.append(i)


        ## sun moon stars
        if True:
            g.TEXTIDS['moon'] = g.tman.loadIm('bg/moon.png')
            g.TEXTIDS['sun'] = g.tman.loadIm('bg/sun.png')
            g.TEXTIDS['stars'] = g.tman.loadIm('bg/stars.png')

        ##
        if True:

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
        self.menu_fonct = {'play':self.change_action
                        ,'quit':self.get_out
                        ,'go home':self.perso.tp
                        ,'scr0':self.change_screen
                        ,'scr1':self.change_screen
                        ,'reset':self.menu.reset
                        ,'cheat':self.perso.cheat
                        ,'splum':self.perso.cheat_plumson
                        ,'roll_color':g.Cyc.roll_mode}
        self.menu_args = {'play':['play'],'go home':[0,None,o2.NY.CITY['home']],'scr0':[0],'scr1':[1]}

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


    ### ONCE FUNCTIONS

    def game_over(self):

        self.label_gameover = g.lman.addLab('GAME OVER',(1920/2,1080/2),anchor=('center','center'),font_name=1,font_size=200,color=c['darkkhaki'],group='up')
        self.label_gameover2 = g.lman.addLab('GAME OVER',(1920/2,1080/2),anchor=('center','center'),font_name=1,font_size=210,color=c['black'],group='up')

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

    def change_screen(self,screen_nb):

        screens = g.scr.screens
        screen = screens[screen_nb]

        # on recrée
        newwin = pyglet.window.Window(screen=screen)
        newwin.set_fullscreen()
        newwin.push_handlers(self)
        newwin.push_handlers(g.keys)

        # on supprime l'ancienne window
        self.window.close()
        self.window = newwin

        #on update g.scr
        g.scr.update_screen(self.window)

    def screen_capture(self):

        capture_screen((g.scr.x, g.scr.y, g.scr.w, g.scr.h))
        g.pman.alert('screen capture copied to clipboard !')

    ### PYGLET FUNCTIONS

    def on_key_press(self,symbol,modifiers):

        ## real keys
        if symbol == key.F1:
            self.screen_capture()

        if self.action == "play":

            if symbol == key.ESCAPE:
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
                    self.perso.hit()

                elif symbol == key.X:
                    self.perso.hud.rollhide()
                    self.perso.lifehud.rollhide()
                    self.perso.credhud.rollhide()
                    if self.perso.plume != None:
                        self.perso.plumhud.rollhide()

                elif symbol == key.I:
                    self.perso.invhud.rollhide()

                elif symbol == key.F:
                    #self.perso.speak()
                    self.perso.rollspeak(g.M)

                elif symbol == key.M:
                    self.perso.bigmap.rollhide()

                elif symbol == key.TAB:
                    self.perso.relhud.unhide()

                elif symbol == key.K:
                    self.perso.minirelhud.rollhide()
                    #self.perso.poto.attack_hum(0,self.perso)

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

        if symbol in g.longpress:
            del g.longpress[symbol]

        if self.action == "play" and self.perso.alive:

            if symbol == key.F and self.perso.roll != None:
                self.perso.unroll()

            elif symbol == key.TAB:
                self.perso.relhud.unhide(True)

    def on_close(self):

        print('\n\nNumber of lines :',compt(self.path))
        gs.save_files(self.path)

    def on_mouse_motion(self,x,y,dx,dy):
        g.M = [x,y]

        if self.action == "play":

            ## CHECK ROLL
            if self.perso.roll != None:
                self.perso.roll.update()
            else:
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
                        zone = o2.NY.CITY[self.perso.street].zones['lit']
                        if zone.hud.ui != None :
                            if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == zone.hud) : #check si il peut catch

                                caught_dropped = zone.hud.catch_or_drop(x,y,self.perso)

                                if caught_dropped == 1: # means caught

                                    if not g.keys[key.LSHIFT]:
                                        # signifie qu'on prend le hud
                                        self.this_hud_caught_an_item = zone.hud
                                    else:
                                        # attrapage rapide dans l'inventaire
                                        self.perso.invhud.catch(zone.hud.ui.phase)
                                        o2.NY.CITY[self.perso.street].zones['lit'].hud.delete_phase()
                                        letsbacktnothingcaught = True

                                elif caught_dropped == -1: # means dropped
                                    letsbacktnothingcaught = True

                                self.on_mouse_motion(x,y,0,0)

                    elif zone == 'studio':
                        zone = o2.NY.CITY[self.perso.street].zones['studio']
                        if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == zone.hud) : #check si il peut catch
                            caught_dropped = zone.hud.catch_or_drop(x,y,self.perso)

                            if caught_dropped == 1: # means caught

                                if not g.keys[key.LSHIFT]:
                                    # signifie qu'on prend le hud
                                    self.this_hud_caught_an_item = zone.hud
                                else:
                                    # attrapage rapide dans l'inventaire
                                    self.perso.invhud.catch(zone.hud.item_caught.item)
                                    zone.hud.item_caught.delete()
                                    zone.hud.item_caught = None
                                    letsbacktnothingcaught = True

                            elif caught_dropped == -1: # means dropped
                                letsbacktnothingcaught = True

                            self.on_mouse_motion(x,y,0,0)

                    elif zone == 'ordi':
                        zone = o2.NY.CITY[self.perso.street].zones['ordi']
                        if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == zone.hud) : #check si il peut catch

                            if zone.hud.uis['main'] != None and self.perso not in zone.hud.uis['main'].item.owners:
                                g.Cur.start_long_press(zone.hud.uis['main'].box,zone.hud.buy_instru)

                            caught_dropped = zone.hud.catch_or_drop(x,y)

                            if caught_dropped == 1: # means caught

                                if not g.keys[key.LSHIFT]:
                                    # signifie qu'on prend le hud
                                    self.this_hud_caught_an_item = zone.hud
                                else:
                                    # attrapage rapide dans l'inventaire
                                    self.perso.invhud.catch(zone.hud.item_caught.item)
                                    zone.hud.item_caught.delete()
                                    zone.hud.item_caught = None
                                    letsbacktnothingcaught = True
                            elif caught_dropped == -1: # means dropped
                                letsbacktnothingcaught = True

                            self.on_mouse_motion(x,y,0,0)

            # inventUI
            if self.perso.invhud.visible:

                if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == self.perso.invhud) : #check si il peut catch
                    caught_dropped = self.perso.invhud.catch_or_drop(x,y)

                    if caught_dropped == 1: # means caught

                        if not g.keys[key.LSHIFT]:
                            # signifie qu'on prend le hud
                            self.this_hud_caught_an_item = self.perso.invhud
                        else:
                            # attrapage rapide dans l'inventaire (fin là en dehors de l'inv)
                            self.perso.invhud.quick_catch_and_drop(self.perso.invhud.item_caught.item)
                            letsbacktnothingcaught = True

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

                speed = self.perso.speed
                if g.keys[key.LSHIFT]:
                    speed = self.perso.runspeed

                ## moving perso
                if g.keys[key.Q]:
                    self.perso.move('L',o2.NY.CITY[self.perso.street],speed)
                if g.keys[key.D]:
                    self.perso.move('R',o2.NY.CITY[self.perso.street],speed)
                if g.keys[key.Z]:
                    self.perso.move('up',o2.NY.CITY[self.perso.street])
                if g.keys[key.S]:
                    self.perso.move('down',o2.NY.CITY[self.perso.street])

            if g.keys[key.LEFT] or g.keys[key.RIGHT]:
                if g.keys[key.RIGHT]:
                    g.GodCam.activate('R')
                if g.keys[key.LEFT]:
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
                del self.lab_fps1[0]
            moyfps = int(sum(self.lab_fps1)/len(self.lab_fps1))
            g.FPS = moyfps
            g.lman.set_text(self.lab_fps,'FPS : '+str(moyfps))
        except : pass

        if self.action == "play":

            # STREETS LABEL
            g.lman.set_text(self.lab_street,self.perso.street)

            # DAYS LABEL
            g.lman.set_text(self.lab_day,'DAY : '+str(g.Cyc.day))

            ## anchor / moving sprites

            # ZONE/ITEMS
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

            # PERSOS
            if True:
                #--# persos
                ## update catalog:
                o2.NY.CITY[self.perso.street].update_catalog(self.perso)
                #print(self.perso.street)
                for hum in o2.NY.CITY[self.perso.street].humans:
                    #print(hum)
                    x_r = hum.gex + g.Cam.X + g.GodCam.X
                    y_r = hum.gey + g.Cam.Y
                    g.sman.modify(hum.skin_id,(x_r,y_r))
                    hum.update_env()
                    hum.update_lab()
                    hum.update()

                for hum in o2.NY.CITY[self.perso.street].humans:
                    hum.being_bot()
                    hum.check_do()

            # BG
            if True:

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

            # CAM
            if True:
                o2.NY.CITY[self.perso.street].modify(g.Cam.X+ g.GodCam.X,g.Cam.Y)

                g.Cam.update(self.perso.realbox,o2.NY.CITY[self.perso.street],g.keys[key.LSHIFT])

            # if not pause, go streamin and particles
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

            text_lab = (self.perso.bigdoing['lab'],list(map(lambda x:x['lab'],self.perso.todo)),self.perso.doing)
            g.lman.set_text(self.lab_doing,text_lab)
            self.perso.hud.update()
            self.perso.bigmap.update()

            if self.perso.money <= 0 or not self.perso.alive:
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
