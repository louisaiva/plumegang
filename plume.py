"""
CODED by deltasfer
enjoy
"""


import pyglet,time,random
from pyglet.window import key
import pyglet.gl as gl
import colorama
from colors import red, green, blue
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
FILL_INV = 1
## pour remplir ou non l'inventaire au debut
VSYNC = 1
## utilise la vsync (fps fixé à 60) ou paa

class App():

    ### INIT FUNCTIONS

    def __init__(self):

        self.path = CURRENT_PATH
        self.init_time = time.time()

        ### windows

        self.window = pyglet.window.Window(screen=g.scr.screen,vsync=VSYNC)

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

        # textures/sprites
        if True:

            ##  TEXTURES

            self.create_organise_textures()

            ## Cursor
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
            self.sprids['ground'] = g.sman.addCol('gray',rect,'bg_buildings_proche')
            self.sprids['bg1.1'] = g.sman.addSpr(g.TEXTIDS['bg1'],(self.bgx,self.bgy),'bg_buildings_proche')
            g.sman.modify(self.sprids['bg1.1'],scale=(1.2,1.2))
            self.sprids['bg1.2'] = g.sman.addSpr(g.TEXTIDS['bg1'],(self.bgx+g.sman.spr(self.sprids['bg1.1']).width,self.bgy),'bg_buildings_proche')
            g.sman.modify(self.sprids['bg1.2'],scale=(1.2,1.2))

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

        # streets
        if True:

            o2.create_map()

        # humans
        if True:

            #print(red('OOOOOOOOOOOOOOOOOOOOOOOOOOOO'))
            ## PERSOS
            self.perso = p.Perso('rapper',fill=FILL_INV)
            p.BOTS.append(self.perso)
            #o2.NY.CITY['home'].add_owner(self.perso)

            #print(blue('OOOOOOOOOOOOOOOOOOOOOOOOOOOO'))
            #poto
            p.BOTS.append(p.Fan('perso3',o2.NY.CITY['home'].rand_pos(),street='home'))
            #o2.NY.CITY['home'].add_owner(p.BOTS[-1])
            self.perso.assign_poto(p.BOTS[-1])


            self.lab_doing = g.lman.addLab(self.perso.poto.doing,(1880,1050),font_size=20,anchor=('right','top'))

            ## FANS/RAPPEURS/GUYS

            # add hum to p.BOTS for each street
            for str in o2.NY.CITY:
                street = o2.NY.CITY[str]
                if street.name not in ['home']:
                    n_str = street.get_random_nb_bots()
                    for i in range(n_str):
                        pos = street.rand_pos()
                        if random.random() < 1/8 and len(names.rappeurs) > 0:
                            hum = p.Rappeur('rapper',pos,street=street.name)
                        else:
                            text = random.choice(['perso','perso2','perso3'])
                            hum = p.Fan(text,pos,street=street.name)
                        p.BOTS.append(hum)

            for shop in o2.NY.shops:
                shop.create_guys()

            # adding all hum to their street
            for hum in p.BOTS+p.GUYS:
                street = o2.NY.CITY[hum.street]

                # on donne les clés de chez eux à chaque bot
                if isinstance(street,o2.PrivateHouse):
                    street.add_owner(hum)
                elif random.random()>0.01:
                    # si le gars n'a pas de maison on lui en donne une, sauf s'il est sdf mdr
                    o2.NY.rd_house().add_owner(hum)

                # et on les ajoute à leur street actuelle
                street.add_hum(hum)

            if len(p.BOTS+p.GUYS) < 200:
                print(p.BOTS+p.GUYS)
            print('IN THIS GAME :',len(p.BOTS+p.GUYS),'bots ---',len(o2.NY.CITY),'streets')

        # cycle
        tabcolor = [(self.sprids['bg-1'],1),
                    (self.sprids['bg.1'],0.9),
                    (self.sprids['bg.2'],0.9),
                    (self.sprids['bg1.1'],0.7),
                    (self.sprids['bg1.2'],0.7),
                    (self.sprids['ground'],0.7)]
        g.Cyc.launch(self.perso,tabcolor)

        # zones
        if True:

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
            zones.append(o.Cash(2900,225))
            street = o2.NY.rd_street().name
            o2.NY.CITY[street].assign_zones(zones)
            print('let\'s find the',street,'!')

            # distrokid
            zones = []
            zones.append(o.SimpleReleaser(1670,210,o.distro))
            #o2.NY.CITY['distrokid'].assign_zones(zones)



            o2.NY.CITY[self.perso.street].load()

        # lot of stuff : hud/end/menu/labels/keys/clicks/final
        if True:

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

            self.lab_fps = g.lman.addLab('',(10,1080),group='up',font_name=1,font_size=32,anchor=('left','top'))
            self.lab_day = g.lman.addLab('',(10,1080-32-32),group='up',font_name=1,font_size=32,anchor=('left','top'))
            self.lab_time = g.lman.addLab('',(10,1080-32-32-32),group='up',font_name=1,font_size=20,anchor=('left','top'))
            self.lab_street = g.lman.addLab('',(10,1080-32),group='up',font_name=1,font_size=32,anchor=('left','top'))

            # keys
            g.keys = key.KeyStateHandler()
            self.window.push_handlers(g.keys)
            #g.longpress = {}
            #g.cooldown = 0.5

            #joysticks
            joysticks = pyglet.input.get_joysticks()
            if joysticks:
                g.joystick = joysticks[0]
                g.joystick.open()
                g.joystick.push_handlers(self)


            # clicks
            self.clicks = {'L':False,'R':False,'M':[0,0]}
            self.mouse_speed = 0

            # final
            self.action = "play" # play pause
            self.playing = True

            print(red('LOADIN TIME '+trunc(time.time()-self.init_time)+' sec'))
            pyglet.clock.schedule_interval(self.gameloop,0.0000001)
            pyglet.app.run()

    def create_organise_textures(self):

        ### PERSOS
        if True:

            #

            keys = ['perso','perso2','perso3','guy','rapper']
            for x in keys:
                if x == 'rapper':
                    g.TEXTIDS[x] = g.tman.loadImSeq(x+'.png',(1,60))
                else:
                    g.TEXTIDS[x] = g.tman.loadImSeq(x+'.png',(1,40))
            p.update_textures(keys)

        # items
        if True:
            g.TEXTIDS['_son'] = g.tman.loadImSeq('son.png',(1,6))
            g.TEXTIDS['_phaz'] = g.tman.loadImSeq('phaz.png',(1,6))
            g.TEXTIDS['_instru'] = g.tman.loadImSeq('instru.png',(1,6))
            g.TEXTIDS['_plum'] = g.tman.loadImSeq('plum.png',(1,6))
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

            ## ux
            g.TEXTIDS['ux'] = g.tman.loadImSeq('items.png',(1,40))

            ## nbs
            g.TEXTIDS['nbs'] = g.tman.loadImSeq('nbs.png',(1,100))

            ## items
            g.TEXTIDS['items'] = {}
            g.TEXTIDS['items']['key'] = g.TEXTIDS['ux'][3]
            g.TEXTIDS['items']['bottle'] = g.TEXTIDS['ux'][7]
            g.TEXTIDS['items']['noodle'] = g.TEXTIDS['ux'][6]

        # BG
        if True:
            g.TEXTIDS['bg-1'] = g.tman.loadIm('bg/sky.png')
            g.TEXTIDS['bg'] = g.tman.loadIm('bg/bg'+'.png')
            g.TEXTIDS['bg1'] = g.tman.loadIm('bg/bg1'+'.png')

        # HOME
        if True:
            g.TEXTIDS['home'] = {}
            g.TEXTIDS['home']['back'] = g.tman.loadIm('bg/home/home_back'+'.png',10)
            g.TEXTIDS['home']['front'] = g.tman.loadIm('bg/home/home_front'+'.png')
            g.TEXTIDS['home']['frontanim'] = [g.tman.loadIm('bg/home/home_fanim'+str(i)+'.png') for i in range(1,5)]
            g.TEXTIDS['home']['backanim'] = [g.tman.loadIm('bg/home/home_banim'+str(i)+'.png') for i in range(1,5)]

        # DISTRO
        if True:
            g.TEXTIDS['distrokid'] = {}
            g.TEXTIDS['distrokid']['back'] = g.tman.loadIm('bg/distro/distrokid_shop.png')
            g.TEXTIDS['distrokid']['backanim'] = [g.tman.loadIm('bg/distro/distrokid_anim'+str(i)+'.png') for i in range(1,5)]

        # SHOP
        if True:
            g.TEXTIDS['shop'] = {}
            g.TEXTIDS['shop']['back'] = g.tman.loadIm('bg/shop.png')
            #g.TEXTIDS['shop']['backanim'] = [g.tman.loadIm('bg/distro/shop_anim'+str(i)+'.png') for i in range(1,5)]

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
            g.TEXTIDS['backbuild'] = {}

            nb_build = 4

            #builds : separating front (first 1500x of each build) and back (100x left)
            id = g.tman.loadIm('bg/builds.png')
            img = g.tman.textures[id]

            h = o2.H_BUILD
            w_tot = o2.W_BUILD + o2.W_BACK

            #sides
            for i in range(2):
                txt = ['L','R']
                x = i*(o2.W_SIDE+o2.W_BACK)
                #front
                w = o2.W_SIDE
                text = img.get_region(x, 0, w,h)
                g.TEXTIDS['build'][txt[i]] = g.tman.addText(text)

                #back
                w = o2.W_BACK
                text = img.get_region(x+o2.W_SIDE, 0, w,h)
                g.TEXTIDS['backbuild'][txt[i]] = g.tman.addText(text)

            x = 2*(o2.W_BACK+o2.W_SIDE)
            #builds
            for i in range(nb_build):
                #front
                w = o2.W_BUILD
                text = img.get_region(i*w_tot+x, 0, w,h)
                g.TEXTIDS['build'][i] = g.tman.addText(text)

                #back
                w = o2.W_BACK
                text = img.get_region(i*w_tot+x + o2.W_BUILD, 0, w,h)
                g.TEXTIDS['backbuild'][i] = g.tman.addText(text)

            #o2.builds_key.append(i)

        ## ZONES
        if True:
            g.TEXTIDS['zone'] = {}

            zones = ['distrib']
            ids = g.tman.loadImSeq('zones.png',(1,6))

            for i in range(len(zones)):
                g.TEXTIDS['zone'][zones[i]] = ids[i]

        ## sun moon stars ...
        if True:
            g.TEXTIDS['moon'] = g.tman.loadIm('bg/moon.png')
            g.TEXTIDS['sun'] = g.tman.loadIm('bg/sun.png')
            g.TEXTIDS['stars'] = g.tman.loadIm('bg/stars.png')

            g.TEXTIDS['sbahn'] = g.tman.loadIm('bg/train.png')

        ##
        if True:

            g.TEXTIDS['steam'] = g.tman.addCol('lightgray')
            g.TEXTIDS['steam2'] = g.tman.addCol('gray')

            ## huds
            g.TEXTIDS['studhud'] = g.tman.loadIm('studhud.png')
            g.TEXTIDS['ordhud'] = g.tman.loadIm('ordhud.png')

            ## effects
            g.TEXTIDS['blur'] = g.tman.addCol('black',1,1)

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

        if self.action == "play":

            if symbol == key.ESCAPE:
                self.change_action('pause')
                if not ESK_QUIT:
                    return pyglet.event.EVENT_HANDLED
            #affiche les différents OrderedGroup d'affichage

            elif symbol == key.B:
                print(self.perso.invhud)
                print(self.perso.plume)

            if self.perso.alive:

                if symbol == key.A:
                    self.perso.drop_sel()

                elif symbol == key.SPACE:
                    self.perso.act()

                elif symbol == key.X:
                    self.perso.hud.rollhide()
                    self.perso.lifehud.rollhide()
                    self.perso.selhud.rollhide()
                    self.perso.fedhydhud.rollhide()

                elif symbol == key.E:
                    self.perso.invhud.rollhide()

                elif symbol == key.F:
                    #self.perso.speak()
                    self.perso.rollspeak(g.M)

                elif symbol == key.V:
                    # on assigne le bot le plus proche à être le poto
                    if len(self.perso.hum_env) > 0:
                        bot = self.perso.hum_env[0]
                        self.perso.assign_poto(bot)

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

            elif symbol == key.SPACE:
                self.perso.unact()

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

                # lifeUI
                if self.perso.lifehud.ui.visible and self.this_hud_caught_an_item == None:
                    self.perso.lifehud.ui.check_mouse(x,y)

                #all zones
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
                elif self.this_hud_caught_an_item == self.perso.selhud and self.perso.selhud.item_caught == None:
                    #print('oh yo')
                    self.this_hud_caught_an_item = None

                #print(self.this_hud_caught_an_item)

                # inventUI
                if self.perso.invhud.visible:
                    if self.this_hud_caught_an_item == None:
                        self.perso.invhud.check_hoover(x,y)
                    elif self.this_hud_caught_an_item == self.perso.invhud:
                        self.perso.invhud.item_caught.move(x,y)
                        self.perso.invhud.item_caught.check_mouse(x,y)

                # selUI
                if self.perso.selhud.visible:
                    if self.this_hud_caught_an_item == None:
                        self.perso.selhud.check_hoover(x,y)
                    elif self.this_hud_caught_an_item == self.perso.selhud:
                        self.perso.selhud.item_caught.move(x,y)
                        self.perso.selhud.item_caught.check_mouse(x,y)

                #print(self.this_hud_caught_an_item)

    def on_mouse_press(self,x, y, button, modifiers):

        if self.action == "play":

            butt = ''
            if button == pyglet.window.mouse.LEFT: butt = 'L'
            elif button == pyglet.window.mouse.RIGHT: butt = 'R'

            letsbacktnothingcaught = False

            ## CHECK ALL UI

            #all hud
            for zone in o2.NY.CITY[self.perso.street].zones:
                if o2.NY.CITY[self.perso.street].zones[zone].activated:

                    if zone == 'lit':
                        zone = o2.NY.CITY[self.perso.street].zones['lit']
                        if zone.hud.ui != None :
                            if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == zone.hud) : #check si il peut catch

                                caught_dropped = zone.hud.catch_or_drop(x,y,self.perso,butt)

                                if caught_dropped == 1: # means caught

                                    if not g.keys[key.LSHIFT]:
                                        # signifie qu'on prend le hud
                                        self.this_hud_caught_an_item = zone.hud
                                    else:
                                        # attrapage rapide dans l'inventaire
                                        self.perso.grab(zone.hud.ui.item,True)
                                        o2.NY.CITY[self.perso.street].zones['lit'].hud.delete_phase()
                                        letsbacktnothingcaught = True

                                elif caught_dropped == -1: # means dropped
                                    letsbacktnothingcaught = True

                                self.on_mouse_motion(x,y,0,0)

                    elif zone == 'studio':
                        zone = o2.NY.CITY[self.perso.street].zones['studio']
                        if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == zone.hud) : #check si il peut catch
                            caught_dropped = zone.hud.catch_or_drop(x,y,self.perso,butt)

                            if caught_dropped == 1: # means caught

                                if not g.keys[key.LSHIFT]:
                                    # signifie qu'on prend le hud
                                    self.this_hud_caught_an_item = zone.hud
                                else:
                                    # attrapage rapide dans l'inventaire
                                    self.perso.grab(zone.hud.item_caught.item,True)
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

                            caught_dropped = zone.hud.catch_or_drop(x,y,butt)

                            if caught_dropped == 1: # means caught

                                if not g.keys[key.LSHIFT]:
                                    # signifie qu'on prend le hud
                                    self.this_hud_caught_an_item = zone.hud
                                else:
                                    # attrapage rapide dans l'inventaire
                                    self.perso.grab(zone.hud.item_caught.item,True)
                                    zone.hud.item_caught.delete()
                                    zone.hud.item_caught = None
                                    letsbacktnothingcaught = True
                            elif caught_dropped == -1: # means dropped
                                letsbacktnothingcaught = True

                            self.on_mouse_motion(x,y,0,0)

            # inventUI
            if self.perso.invhud.visible:

                if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == self.perso.invhud) : #check si il peut catch
                    caught_dropped = self.perso.invhud.catch_or_drop(x,y,butt)

                    if caught_dropped == 1: # means caught

                        if not g.keys[key.LSHIFT]:
                            # signifie qu'on prend le hud
                            self.this_hud_caught_an_item = self.perso.invhud
                            self.perso.invhud.item_caught.move(x,y)
                            self.perso.invhud.item_caught.check_mouse(x,y)
                        else:
                            # attrapage rapide dans l'inventaire (fin là en dehors de l'inv)
                            self.perso.invhud.quick_catch_and_drop()
                            letsbacktnothingcaught = True

                    elif caught_dropped == -1: # means dropped
                        letsbacktnothingcaught = True

                    elif caught_dropped == 2: # means continuely caughtin
                        self.perso.invhud.item_caught.move(x,y)
                        self.perso.invhud.item_caught.check_mouse(x,y)

                    ## si on active ça, ça fait que quand on dépose dans le selhud sur un item deja, ça fait de la merde
                    #self.on_mouse_motion(x,y,0,0)

                #self.perso.invhud.check_hoover(x,y)
                self.perso.invhud.check_press_btns(x,y)

            # selUI
            if self.perso.selhud.visible:

                if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == self.perso.selhud) : #check si il peut catch
                    caught_dropped = self.perso.selhud.catch_or_drop(x,y,butt)

                    if caught_dropped == 1: # means caught

                        if not g.keys[key.LSHIFT]:
                            # signifie qu'on prend le hud
                            #print('oh yo')
                            self.this_hud_caught_an_item = self.perso.selhud
                            self.perso.selhud.item_caught.move(x,y)
                            self.perso.selhud.item_caught.check_mouse(x,y)

                            #self.on_mouse_motion(x,y,0,0)
                        else:
                            # attrapage rapide dans l'inventaire (fin là en dehors de l'inv)
                            self.perso.selhud.quick_catch_and_drop()
                            letsbacktnothingcaught = True

                    elif caught_dropped == -1: # means dropped
                        letsbacktnothingcaught = True

                    elif caught_dropped == 2: # 2 means continuely caughtin
                        self.perso.selhud.item_caught.move(x,y)
                        self.perso.selhud.item_caught.check_mouse(x,y)

            if letsbacktnothingcaught:
                self.on_mouse_motion(x,y,0,0)
                self.this_hud_caught_an_item = None

    def on_mouse_release(self,x,y,button,modifiers):
        g.Cur.reset()

    def on_mouse_drag(self,x, y, dx, dy, buttons, modifiers):
        self.on_mouse_motion(x,y,dx,dy)

    def on_mouse_scroll(self,x, y, scroll_x, scroll_y):

        if self.action == "play":
            if scroll_y > 0:
                self.perso.roll_sel('down')
            elif scroll_y < 0:
                self.perso.roll_sel()

    ## JOYSTICK

    def on_joybutton_press(self,joystick, button):
        print('button',button)

        if joystick == g.joystick:
            if self.action == "play" and self.perso.alive:
                if button == 0:
                    self.perso.act()

    def on_joybutton_release(self,joystick, button):

        if joystick == g.joystick:
            if self.action == "play" and self.perso.alive:
                if button == 0:
                    self.perso.unact()

    def on_joyaxis_motion(self,joystick, axis, value):

        if joystick == g.joystick:
            if self.action == "play" and self.perso.alive:

                if axis == 'ry':
                    if value > 0:
                        self.perso.roll_sel('down')
                    elif value < 0:
                        self.perso.roll_sel()
            #print('axis',axis,value)
            pass

    def on_joyhat_motion(self,joystick, hat_x, hat_y):

        if joystick == g.joystick:
            if self.action == "play" and self.perso.alive:
                if hat_y > 0:
                    self.perso.roll_sel('down')
                elif hat_y < 0:
                    self.perso.roll_sel()


    ### LOOP

    def events(self):

        if self.action == "play":

            if not self.gameover:


                speed = self.perso.speed
                if g.keys[key.LSHIFT]:
                    speed = self.perso.runspeed

                ## moving perso
                if g.keys[key.Q]:
                    self.perso.move('L',speed)
                if g.keys[key.D]:
                    self.perso.move('R',speed)
                if g.keys[key.Z]:
                    self.perso.move('up')
                if g.keys[key.S]:
                    self.perso.move('down')

                ## actin
                if g.keys[key.SPACE]:
                    self.perso.act()


                if g.joystick:

                    # do thg with joystik
                    """g.joy_dry = g.joystick.ry - g.joy_ry
                    g.joy_ry = g.joystick.ry
                    print(g.joy_dry)"""


                    ## same with joystick
                    speed = self.perso.speed
                    if g.joystick.z > 0.4:
                        speed = self.perso.runspeed

                    ## moving perso
                    if g.joystick.x < -0.4:
                        self.perso.move('L',speed)
                    elif g.joystick.x > 0.4:
                        self.perso.move('R',speed)
                    if g.joystick.y < -0.4:
                        self.perso.move('up')
                    elif g.joystick.y > 0.4:
                        self.perso.move('down')

                    ## actin
                    #print(g.joystick.buttons)
                    #print(g.joystick.__dict__)
                    if g.joystick.z < -0.4:
                        self.perso.act()

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

            # HOUR LABEL
            g.lman.set_text(self.lab_time,'  '+str(g.Cyc))

            ## anchor / moving sprites

            #print(len(self.sprids),self.sprids)

            perso_street = o2.NY.CITY[self.perso.street]

            # ZONE/ITEMS
            if True:

                #--# zones elem
                for zone in perso_street.zones:
                    zone=perso_street.zones[zone]
                    x_r = zone.gex + g.Cam.X + g.GodCam.X
                    y_r = zone.gey + g.Cam.Y
                    #g.sman.modify(zone.skin_id,(x_r,y_r))
                    zone.move(x_r,y_r)

                    # load/deload
                    if (x_r+zone.w <= -g.SAFE_W or x_r >= g.scr.fx+g.SAFE_W) and zone.loaded:
                        zone.deload()
                    elif (x_r+zone.w > -g.SAFE_W and x_r < g.scr.fx+g.SAFE_W) and not zone.loaded:
                        zone.load(perso_street)

                #--# zones elem item
                for item in perso_street.items:
                    #item=perso_street.items[item]
                    x_r = item.gex + g.Cam.X + g.GodCam.X
                    y_r = item.gey + g.Cam.Y
                    #g.sman.modify(item.skin_id,(x_r,y_r))
                    item.move(x_r,y_r)

                    # load/deload
                    if (x_r+item.w <= -g.SAFE_W or x_r >= g.scr.fx+g.SAFE_W) and item.loaded:
                        item.deload()
                    elif (x_r+item.w > -g.SAFE_W and x_r < g.scr.fx+g.SAFE_W) and not item.loaded:
                        item.load(perso_street)

            # PERSOS
            if True:
                #--# persos
                ## update catalog:
                perso_street.update_catalog()
                for hum in perso_street.humans:
                    x_r = hum.gex + g.Cam.X + g.GodCam.X
                    y_r = hum.gey + g.Cam.Y
                    if hasattr(hum,'skin_id'):
                        g.sman.modify(hum.skin_id,(x_r,y_r))

                    # load/deload
                    if (x_r+p.SIZE_SPR <= -g.SAFE_W or x_r >= g.scr.fx+g.SAFE_W) and hum.loaded:
                        hum.deload()
                    elif (x_r+p.SIZE_SPR > -g.SAFE_W and x_r < g.scr.fx+g.SAFE_W) and not hum.loaded:
                        hum.load()

                    # update
                    hum.update_env()
                    hum.update_lab()
                    hum.update()
                    hum.being_bot()
                    hum.check_do()

            # GUYS
            if True:

                # refresh the guys all over the city
                for guy in p.GUYS:
                    if guy.work_hours != None:
                        hm_begin,hm_end = guy.work_hours
                        if g.Cyc >= hm_begin-g.Hour(1) and g.Cyc < hm_end and not guy.workin:
                            guy.work()
                        elif (g.Cyc < hm_begin or g.Cyc >= hm_end) and guy.workin:
                            guy.stop_work()
                    if guy.street != self.perso.street and o2.NY.CITY[guy.street] not in perso_street.neighbor:
                        guy.lil_check_colli()
                        guy.being_bot()
                        guy.check_do()

            # NEIGHBOR STREETS
            if True:

                for street in perso_street.neighbor:
                    street.update_catalog()
                    for hum in street.humans:
                        hum.update_env()
                        #hum.update_lab()
                        hum.update()
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

            # STREETS
            perso_street.update(g.Cam.X+ g.GodCam.X,g.Cam.Y)

            # BAHN
            for sbahn in o2.NY.BAHN:
                o2.NY.BAHN[sbahn].update(g.Cam.X+ g.GodCam.X,g.Cam.Y)
                #print(o2.NY.BAHN[sbahn].street,o2.NY.BAHN[sbahn].gex,o2.NY.BAHN[sbahn].x)

            # CAM
            if True:

                run = False
                if g.joystick and g.joystick.z > 0.4:
                    run = True
                elif g.keys[key.LSHIFT]:
                    run = True

                g.Cam.update(self.perso.realbox,perso_street,run)

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
                        random.choice(p.BOTS+p.GUYS).stream(self.perso.disco[i])

            if len(p.GUYS) > 0:
                text_lab = (p.GUYS[0].bigdoing['lab'],list(map(lambda x:x['lab'],p.GUYS[0].todo)),p.GUYS[0].doing)
            else:
                text_lab = (self.perso.poto.bigdoing['lab'],list(map(lambda x:x['lab'],self.perso.poto.todo)),self.perso.poto.doing)
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

                self.time_events = g.lman.addLab('',(600,0),group='up',font_size=20,anchor=('left','bottom'))
                self.time_ref = g.lman.addLab('',(800,0),group='up',font_size=20,anchor=('left','bottom'))
                self.time_draw = g.lman.addLab('',(960,0),group='up',font_size=20,anchor=('left','bottom'))
            self.tick += 1


            t = time.time()
            # EVENTS
            self.events()
            g.lman.set_text(self.time_events,'event : '+trunc(time.time()-t,3))

            gl.glClearColor(1/4,1/4,1/4,1)
            # CLR
            self.window.clear()

            gl.glEnable(gl.GL_TEXTURE_2D)
            gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)
            #

            t = time.time()
            # RFRSH
            self.refresh()
            g.lman.set_text(self.time_ref,'ref : '+trunc(time.time()-t,3))

            #
            t = time.time()
            # DRW
            self.draw()
            g.lman.set_text(self.time_draw,'draw : '+trunc(time.time()-t,3))

            #self.window.flip()

        else:
            print('\n\nNumber of lines :',compt(self.path))
            gs.save_files(self.path)

            self.window.close()

def main():

    app = App()
    app.init()

if __name__ == '__main__':
    main()
