"""
CODED by deltasfer
enjoy
"""


import pyglet,time,random
from pyglet.window import key
import pyglet.gl as gl
import colorama
from colors import *
colorama.init()

from src.utils import *
from src.colors import *
import src.names as names
import src.getsave as gs
from src import obj as o
from src import perso as p
from src import obj2 as o2
from src import obj3 as o3
from src import graphic as g
from src import menu as m
from src import cmd


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
            self.sprids['bg-1'] = g.sman.addSpr(g.TEXTIDS['bg-1'],(self.bgx,self.bgy),'sky',key='sky')
            g.sman.modify(self.sprids['bg-1'],scale=(0.75,0.75))
            self.sprids['bg.1'] = g.sman.addSpr(g.TEXTIDS['bg'],(self.bgx,self.bgy),'bg_buildings_loin',key='landscape_far_')
            g.sman.modify(self.sprids['bg.1'],scale=(0.75,0.75))
            self.sprids['bg.2'] = g.sman.addSpr(g.TEXTIDS['bg'],(self.bgx+g.sman.spr(self.sprids['bg.1']).width,self.bgy),'bg_buildings_loin',key='landscape_far_')
            g.sman.modify(self.sprids['bg.2'],scale=(0.75,0.75))

            rect = box(0,0,g.scr.w,250)
            self.sprids['ground'] = g.sman.addCol('gray',rect,'bg_buildings_proche',key='sol')
            self.sprids['bg1.1'] = g.sman.addSpr(g.TEXTIDS['bg1'],(self.bgx,self.bgy),'bg_buildings_proche',key='landscape_proche_')
            g.sman.modify(self.sprids['bg1.1'],scale=(1.2,1.2))
            self.sprids['bg1.2'] = g.sman.addSpr(g.TEXTIDS['bg1'],(self.bgx+g.sman.spr(self.sprids['bg1.1']).width,self.bgy),'bg_buildings_proche',key='landscape_proche_')
            g.sman.modify(self.sprids['bg1.2'],scale=(1.2,1.2))

            ## sprites effects

            self.sprids['effects'] = {}
            sizes = []
            for scr in g.scr.screens:
                if (scr.width,scr.height) not in sizes:
                    sizes.append((scr.width,scr.height))

            for size in sizes:
                self.sprids['effects'][size] = g.sman.addSpr(g.TEXTIDS['blur'],group='up-1',vis=False,key='blur')
                g.sman.modify(self.sprids['effects'][size],scale=size,opacity=150)

            #print(self.sprids['effects'])

        # streets
        if True:

            o2.create_map()

        # humans
        if True:

            ## PERSOS
            self.perso = p.Perso('rapper',fill=FILL_INV,street='home')
            g.Cam.follow(self.perso)
            p.BOTS.append(self.perso)
            # o3.distro.sign(self.perso)

            #poto
            p.BOTS.append(p.Fan('perso3',o2.NY.CITY['home'].rand_pos(),street='home'))
            self.perso.assign_poto(self.perso)


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
            zones.append(o3.Ordi(1990,260,self.perso,o2.NY.CITY['home']))
            zones.append(o3.Studio(2640,225+50,o2.NY.CITY['home']))
            zones.append(o3.Market(450,210,o2.NY.CITY['home']))
            zones.append(o3.Lit(-600,225,o2.NY.CITY['home']))
            o2.NY.CITY['home'].assign_zones(zones)

            # ez cash
            street = o2.NY.rd_street().name
            zones = []
            zones.append(o3.Cash(2900,225,o2.NY.CITY[street]))
            o2.NY.CITY[street].assign_zones(zones)
            print('let\'s find the',street,'!')

            # distrokid
            zones = []
            zones.append(o3.SimpleReleaser(1670,210,o3.distro,o2.NY.CITY['distrokid']))
            o2.NY.CITY['distrokid'].assign_zones(zones)

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

            self.fps_times = {'event':[],'ref':[],'draw':[]}
            self.fps_labs = {}
            self.fps_labs['event'] = g.lman.addLab('',(600,0),group='up',font_size=20,anchor=('left','bottom'))
            self.fps_labs['ref'] = g.lman.addLab('',(800,0),group='up',font_size=20,anchor=('left','bottom'))
            self.fps_labs['draw'] = g.lman.addLab('',(960,0),group='up',font_size=20,anchor=('left','bottom'))

            # keys
            g.keys = key.KeyStateHandler()
            self.window.push_handlers(g.keys)

            self.focus = None
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
            g.TEXTIDS['items']['m16'] = g.TEXTIDS['ux'][8]
            g.TEXTIDS['items']['micro'] = g.TEXTIDS['ux'][9]
            g.TEXTIDS['items']['apple'] = g.TEXTIDS['ux'][10]
            g.TEXTIDS['items']['secretapple'] = g.TEXTIDS['ux'][11]

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

            nb_build = 5

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

            zones = [('distrib',(320,400)),
                    ('lamp',(200,700))
                    ]

            id = g.tman.loadIm('zones.png')
            img = g.tman.textures[id]

            x=0
            for name,wh in zones:
                w,h = wh
                text = img.get_region(x,0,w,h)
                id = g.tman.addText(text)
                g.TEXTIDS['zone'][name] = id
                #cmd.say(name,'texture created id',id)
                x+=w

        ## TRAINS
        if True:

            ids = g.tman.loadImSeq('bg/train.png',(5,1))
            ids.reverse()
            g.TEXTIDS['sbahn'] = ids

        ## sun moon stars ...
        if True:
            g.TEXTIDS['moon'] = g.tman.loadIm('bg/moon.png')
            g.TEXTIDS['sun'] = g.tman.loadIm('bg/sun.png')
            g.TEXTIDS['stars'] = g.tman.loadIm('bg/stars.png')

        ##
        if True:

            g.TEXTIDS['steam'] = g.tman.addCol('lightgray')
            g.TEXTIDS['steam2'] = g.tman.addCol('gray')

            ## huds
            g.TEXTIDS['studhud'] = g.tman.loadIm('studhud.png')
            g.TEXTIDS['ordhud'] = g.tman.loadIm('ordhud.png')

            ## effects
            g.TEXTIDS['blur'] = g.tman.addCol('black',1,1)
            g.TEXTIDS['lights'] = {}

            lux=['doucheXL','doucheL','douche','bigdouche']

            g.TEXTIDS['lights'] = {}
            ids = g.tman.loadImSeq('lum.png',(1,20))
            for i in range(len(lux)):
                g.TEXTIDS['lights'][lux[i]] = ids[i]

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

        if not self.focus:

            #print(symbol,key.SLASH,key.BACKSLASH)
            #print(key.__dict__)

            ## real keys
            if symbol == key.F1:
                self.screen_capture()

            elif symbol == key.G:
                g.print_groups()

            elif symbol == key.T:
                cmd.roll_activate(self)
            elif symbol == key.COLON:
                cmd.roll_activate(self,True)

            elif symbol == key.Y:
                cmd.rollhide()

            if self.action == "play":

                if symbol == key.ESCAPE:
                    self.change_action('pause')
                    if not ESK_QUIT:
                        return pyglet.event.EVENT_HANDLED

                elif symbol == key.B:
                    print(self.perso.invhud)
                    print(self.perso.plume)

                if self.perso.alive:

                    if symbol == key.A:
                        self.perso.drop_sel()

                    elif symbol == key.SPACE:
                        if self.perso.MODE == 'peace':
                            self.perso.act()
                        elif self.perso.MODE == 'fight':
                            self.perso.act()

                    elif symbol == key.X:
                        self.perso.hud.rollhide()
                        self.perso.lifehud.rollhide()
                        self.perso.selhud.rollhide()
                        self.perso.fedhydhud.rollhide()

                    elif symbol == key.E:
                        self.perso.invhud.rollhide()

                    elif symbol == key.F:
                        self.perso.roll_mode(['fight','peace'])

                    elif symbol == key.V:

                        # on assigne le bot le plus proche à être le poto
                        if self.perso.nearest_bot():
                            self.perso.assign_poto(self.perso.nearest_bot())
                        else:
                            self.perso.assign_poto(self.perso)

                    elif symbol == key.M:
                        self.perso.bigmap.rollhide()

                    elif symbol == key.TAB:
                        self.perso.relhud.unhide()

                    elif symbol == key.K:
                        self.perso.minirelhud.rollhide()
                        #self.perso.poto.attack_hum(0,self.perso)

                    elif symbol == key.L:
                        self.perso.chartshud.rollhide()

                    elif symbol in [key._1,key._2,key._3,key._4]:
                        self.perso.selected = symbol - key._1
                        #cmd.colorsay('orange','<@>',symbol)

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

        else:
            if symbol == key.ESCAPE:
                cmd.roll_activate(self)
                return pyglet.event.EVENT_HANDLED

    def on_key_release(self,symbol,modifiers):

        if symbol in g.longpress:
            del g.longpress[symbol]

        if self.action == "play" and self.perso.alive:

            if symbol == key.TAB:
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
            activated_smthg = False

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
                                        activated_smthg = True

                                elif caught_dropped == -1: # means dropped
                                    letsbacktnothingcaught = True
                                    activated_smthg = True

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
                                    activated_smthg = True

                            elif caught_dropped == -1: # means dropped
                                letsbacktnothingcaught = True
                                activated_smthg = True

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
                                    activated_smthg = True
                            elif caught_dropped == -1: # means dropped
                                letsbacktnothingcaught = True
                                activated_smthg = True
                            elif caught_dropped == 2: # means smthg actived
                                activated_smthg = True

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
                            activated_smthg = True

                    elif caught_dropped == -1: # means dropped
                        letsbacktnothingcaught = True

                    elif caught_dropped == 2: # means continuely caughtin
                        self.perso.invhud.item_caught.move(x,y)
                        self.perso.invhud.item_caught.check_mouse(x,y)

                    ## si on active ça, ça fait que quand on dépose dans le selhud sur un item deja, ça fait de la merde
                    #self.on_mouse_motion(x,y,0,0)

                #self.perso.invhud.check_hoover(x,y)
                if self.perso.invhud.check_press_btns(x,y):
                    activated_smthg = True

            # selUI
            if self.perso.selhud.visible:

                if (self.this_hud_caught_an_item == None or self.this_hud_caught_an_item == self.perso.selhud) : #check si il peut catch
                    caught_dropped = self.perso.selhud.catch_or_drop(x,y,butt)

                    if caught_dropped == 1: # means caught

                        if not g.keys[key.LSHIFT]:
                            # signifie qu'on prend le hud
                            self.this_hud_caught_an_item = self.perso.selhud
                            self.perso.selhud.item_caught.move(x,y)
                            self.perso.selhud.item_caught.check_mouse(x,y)

                            #self.on_mouse_motion(x,y,0,0)
                        else:
                            # attrapage rapide dans l'inventaire (fin là en dehors de l'inv)
                            self.perso.selhud.quick_catch_and_drop()
                            letsbacktnothingcaught = True
                            activated_smthg = True

                    elif caught_dropped == -1: # means dropped
                        letsbacktnothingcaught = True

                    elif caught_dropped == 2: # 2 means continuely caughtin
                        self.perso.selhud.item_caught.move(x,y)
                        self.perso.selhud.item_caught.check_mouse(x,y)

            ## ON LANCE LA ROLL de dialogue
            if not self.this_hud_caught_an_item and self.perso.alive and not activated_smthg:
                self.perso.rollspeak(g.M)

            if letsbacktnothingcaught:
                self.on_mouse_motion(x,y,0,0)
                self.this_hud_caught_an_item = None

    def on_mouse_release(self,x,y,button,modifiers):
        g.Cur.reset()
        if self.perso.roll != None and self.action == "play" and self.perso.alive:
            self.perso.unroll()

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

    ## WRITING

    def set_focus(self,dt,focus):
        if self.focus != focus:
            self.focus = focus

    def on_text(self,text):
        if self.focus:
            #print([text])
            if text == '\r':
                self.focus.enter(self.perso)
            else:
                self.focus.caret.on_text(text)
                self.focus.point_input = None

    def on_text_motion(self, motion):
        #print(motion)
        #print(key.UP)
        if self.focus:
            if motion == key.UP:
                self.focus.up()
            elif motion == key.DOWN:
                self.focus.down()
            else:
                self.focus.caret.on_text_motion(motion)

    def on_text_motion_select(self, motion):
        if self.focus:
            self.focus.caret.on_text_motion_select(motion)

    ### LOOP
    def events(self):

        if self.action == "play" and not self.focus:

            if not self.gameover:

                ## moving perso
                if g.keys[key.Q]:
                    self.perso.move('L',run=g.keys[key.LSHIFT])
                if g.keys[key.D]:
                    self.perso.move('R',run=g.keys[key.LSHIFT])
                if g.keys[key.Z]:
                    self.perso.move('up',run=g.keys[key.LSHIFT])
                if g.keys[key.S]:
                    self.perso.move('down',run=g.keys[key.LSHIFT])

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
        if dt > 0:
            self.lab_fps1.append(int(1/dt))
        if len(self.lab_fps1) > 0:
            if len(self.lab_fps1) > 10:
                del self.lab_fps1[0]
            moyfps = int(sum(self.lab_fps1)/len(self.lab_fps1))
            g.FPS = moyfps
            g.lman.set_text(self.lab_fps,'FPS : '+str(moyfps))

        ## TIMES
        for key in self.fps_times:
            if len(self.fps_times[key]) > 0:
                if len(self.fps_times[key]) > 30:
                    del self.fps_times[key][0]
                moyfps = sum(self.fps_times[key])/len(self.fps_times[key])
                g.lman.set_text(self.fps_labs[key],key+' : '+trunc(moyfps,3))

        ## PLAYIN
        if self.action == "play":

            # LABELS
            if True:
                # STREETS LABEL
                g.lman.set_text(self.lab_street,self.perso.street)

                # DAYS LABEL
                g.lman.set_text(self.lab_day,'DAY : '+str(g.Cyc.day))

                # HOUR LABEL
                g.lman.set_text(self.lab_time,'  '+str(g.Cyc))

            perso_street = o2.NY.CITY[self.perso.street]
            # STREETS
            perso_street.update(g.Cam.X+ g.GodCam.X,g.Cam.Y)

            # PERSOS
            if True:
                #--# persos
                ## update catalog:
                perso_street.update_catalog()
                for hum in perso_street.humans:
                    # update
                    hum.update(perso_street.name,g.Cam.X + g.GodCam.X,g.Cam.Y)
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
                        hum.update(perso_street.name,g.Cam.X + g.GodCam.X,g.Cam.Y)
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

            # BAHN
            for sbahn in o2.NY.BAHN:
                o2.NY.BAHN[sbahn].update(g.Cam.X+ g.GodCam.X,g.Cam.Y)
                for street in o2.NY.BAHN[sbahn].circuit:
                    o2.NY.CITY[street].station.update()

            # CAM
            if True:
                g.Cam.update(perso_street)

            # if not pause, go streamin and particles
            if g.bertran.speed > 0:

                ## particles
                g.pman.modify('icons',dy=0.1)
                g.pman.modify('dmg',dy=0.1,ux=g.Cam.X+ g.GodCam.X)
                g.pman.modify('bullet',ux=g.Cam.X+ g.GodCam.X)
                #g.pman.modify('bullet',dx=1)

                ## fans are streaming
                for i in range(len(self.perso.disco)):
                    chance = random.randint(0,int(60*g.FPS))
                    malus = 1-i*0.2
                    if chance < self.perso.nb_fans*malus:
                        random.choice(p.BOTS+p.GUYS).stream(self.perso.disco[i])

                ## updates charts
                #p.update_charts()

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

            self.tick += 1

            # EVENTS
            t = time.time()
            self.events()
            self.fps_times['event'].append(time.time()-t)

            # CLR
            gl.glClearColor(1/4,1/4,1/4,1)
            self.window.clear()

            #gl.glEnable(gl.GL_TEXTURE_2D)
            #gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_NEAREST)

            # RFRSH
            t = time.time()
            self.refresh()
            self.fps_times['ref'].append(time.time()-t)

            # DRW
            t = time.time()
            self.draw()
            self.fps_times['draw'].append(time.time()-t)

        else:
            print('\n\nNumber of lines :',compt(self.path))
            gs.save_files(self.path)

            self.window.close()

def main():

    app = App()
    app.init()

if __name__ == '__main__':
    main()
