"""
CODED by deltasfer
enjoy
"""



import pyglet,random,time
from math import *
import src.utils as u
from src import obj as o
from src.colors import *

import pyglet.gl as gl
#gl.glEnable(gl.GL_TEXTURE_2D)
#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)


'''''''''''''''''''''''''''''''''''''''
'''''''PART ONE : GRAPHIC STUFF''''''''
'''''''''''''''''''''''''''''''''''''''


SPR = 32
FPS = 0

class ScreenManager():
    def __init__(self):

        self.display = pyglet.canvas.get_display()
        self.screens = self.display.get_screens()

        self.current_screen = self.screens[0]
        #print(dir(self.current_screen))

    def update_screen(self,window):
        if window.screen in self.screens:
            #print('yeaas screen bien dans screens')
            self.current_screen = window.screen

    def _screen(self):
        return self.current_screen
    screen = property(_screen)

    def _size(self):
        return self.screen.width,self.screen.height
    size = property(_size)

    def _w(self):
        return self.screen.width
    w = property(_w)

    def _h(self):
        return self.screen.height
    h = property(_h)

    def _x(self):
        return self.screen.x
    x = property(_x)

    def _y(self):
        return self.screen.y
    y = property(_y)


    def _cx(self):
        return self.screen.width/2
    cx = property(_cx)

    def _cy(self):
        return self.screen.height/2
    cy = property(_cy)

    def _cxy(self):
        return self.cx,self.cy
    cxy = property(_cxy)


    def _c(self):
        return self.cx,self.cy
    c = property(_c)

scr = ScreenManager()

#manager who rules groups to draw things in the right order u know
class GroupManager():

    def __init__(self):


        self.groups = {} ## give the group with the name

        self.names_wo = {} ## give the name with the order
        self.orders = {} ## give the order with the name

        self.nb_perso_group = 20

        names = ['sky','stars','moon_sun','bg_buildings_loin','bg_buildings_proche','road','buildings','backstreet','backstreet_anim','mid' # good
                            ,'front','perso-1','hud-1','hud','hud1']
        names += ['perso'+str(i) for i in range(self.nb_perso_group-1,-1,-1)]
        names += ['frontstreet','frontstreet_anim','hud2-1','hud2','hud21','hud22','hud3','ui-2','ui-1','ui','up-1','up']
        self.distance_btw = 1

        for i in range(len(names)):
            self.addGroup(names[i],i*self.distance_btw)

        #print(dir(self.groups['sky']))

    def getGroup(self,name):
        if name not in self.groups:
            print('aie le groupe '+name+' n\'existe pas')
            return None
        else:
            return self.groups[name]

    def addGroup(self,name,order):
        if not name in self.groups:
            self.groups[name] = pyglet.graphics.OrderedGroup(order)
            self.orders[name] = order
            self.names_wo[order] = name
            return self.groups[name]
        return self.groups[name] # group was already created

#manager who init images
class TextureManager():

    def __init__(self,path='.'):

        self.textures = {}

        self.path = path

        self.ids = []

        self.batch = pyglet.graphics.Batch()

    def loadImSeq(self,path2,size,scale=None):

        # size décrit le nb de tiles en w et en h

        path3 = '/item/'
        img = pyglet.image.load(self.path+path3+path2)

        textures = pyglet.image.ImageGrid(img, *size)

        ids = []
        for txt in textures:
            id = u.get_id('text')
            self.textures[id] = txt

            self.ids.append(id)
            ids.append(id)
        return ids

    def loadIm(self,path2,scale=None):

        path3 = '/item/'
        id = u.get_id('img')
        img = pyglet.image.load(self.path+path3+path2)

        self.textures[id] = img
        self.ids.append(id)
        return id

    def addText(self,text):
        id = u.get_id('img')
        self.textures[id] = text
        self.ids.append(id)
        return id

    def addCol(self,color='white',w=SPR,h=SPR):

        if color not in TEXTIDS['col']:
            pattern = pyglet.image.SolidColorImagePattern(c[color])
            id = u.get_id('col')
            self.textures[id] = pattern.create_image(w,h)
            self.ids.append(id)
            TEXTIDS['col'][color] = id
            return id
        else:
            return TEXTIDS['col'][color]

    def draw(self):


        gl.glTexParameteri(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_NEAREST)
        self.batch.draw()
        #print(len(sman.sprites))#,'    ',sman.ids)

tman,gman = TextureManager(),GroupManager()

#manager who rules normal sprites
class SpriteManager():

    def __init__(self):

        ## SPRITES

        self.sprites = {}

        self.ids = []

        self.filters = {}

    def addSpr(self,textid,xy_pos=(0,0),group=None,alr_id=-1,vis=True):


        if alr_id == -1:
            id = u.get_id('spr')
            self.ids.append(id)
        else:
            id =alr_id
        #print(id)



        self.sprites[id] = pyglet.sprite.Sprite(tman.textures[textid], batch=tman.batch)
        self.sprites[id].position = xy_pos
        self.sprites[id].visible = vis

        if group != None:
            self.addToGroup(id,group)

        return id

    def addCol(self,col='white',box=u.box(),group=None,alr_id=-1,vis=True):
        if col in TEXTIDS['col']:
            id = self.addSpr(TEXTIDS['col'][col],box.xy,group,alr_id,vis)

            scy = box.w/self.sprites[id].width
            scx = box.h/self.sprites[id].height

            self.modify(id,scale=(scy,scx))
            return id
        else:
            tman.addCol(col)
            return self.addCol(col,box,group,alr_id,vis)

    def addCircle(self,pos,ray,col=(255,255,255,255),group=None,alr_id=-1,vis=True):

        if alr_id == -1:
            id = u.get_id('spr')
            self.ids.append(id)
        else:
            id =alr_id

        if group != None:
            group = gman.getGroup(group)

        x,y = pos
        opac = col[3]
        col = col[0],col[1],col[2]
        self.sprites[id] = pyglet.shapes.Circle(x,y,ray,color=col,batch=tman.batch,group=group)
        self.sprites[id].opacity = opac
        self.sprites[id].visible = vis

        return id

    def addToGroup(self,id,group_name='bg_buildings_loin'):

        group = gman.getGroup(group_name)
        self.sprites[id].group = group

        #self.detect()

    def unhide(self,tabids,hide=False):
        ## unhide(machin) AFFICHE machin
        ## unhide(machin,True) N'AFFICHE PAS machin

        if type(tabids) == type([]):
            for id in tabids:
                if self.sprites[id].visible != (not hide):
                    self.sprites[id].visible = (not hide)

        elif type(tabids) == type({}):
            for id in tabids:
                self.unhide(tabids[id],hide)

        else:
            if self.sprites[tabids].visible != (not hide):
                self.sprites[tabids].visible = (not hide)

    def set_text(self,sprid,textid):

        if self.sprites[sprid].image != tman.textures[textid]:
            self.sprites[sprid].image = tman.textures[textid]

    def modify(self,sprid,pos=None,scale=None,group=None,opacity=None,anchor=None):

        # position
        x,y = None,None
        if pos != None and pos != (self.sprites[sprid].x,self.sprites[sprid].y):
            x,y = pos

        # scale
        scalex,scaley = None,None
        if scale != None and scale != (self.sprites[sprid].scale_x,self.sprites[sprid].scale_y):
            scalex,scaley = scale

        # updating group
        if group != None:
            group = gman.getGroup(group)
            if group != self.sprites[sprid].group:
                self.sprites[sprid].group = group


        # updating opacity
        if opacity != None:
            if opacity != self.sprites[sprid].opacity:
                self.sprites[sprid].opacity = opacity

        # final updating positon and scale
        #
        self.sprites[sprid].update(x=x,y=y,scale_x = scalex,scale_y=scaley)

        if anchor:
            if anchor == 'center':
                x,y = self.sprites[sprid].position
                x -= self.sprites[sprid].width/2
                y -= self.sprites[sprid].width/2
                self.sprites[sprid].update(x=x,y=y)

    def set_col(self,sprid,col):
        if col in TEXTIDS['col']:
            w,h = self.sprites[sprid].width,self.sprites[sprid].height
            self.set_text(sprid,TEXTIDS['col'][col])
            self.modify(sprid,scale=(1,1))
            sc = w/self.sprites[sprid].width,h/self.sprites[sprid].height
            self.modify(sprid,scale=sc)
        else:
            tman.addCol(col)
            self.set_col(sprid,col)

    #filter
    def filter(self,sprid,color=(255,0,0)):

        if type(sprid) == type([]):
            for id in sprid:
                self.filter(id,color)

        elif type(sprid) == type({}):
            for id in sprid:
                self.filter(sprid[id],color)
        else:
            self.sprites[sprid].color = color

    def update_filter(self,sprid):

        if sprid in self.filters and len(self.filters[sprid]) != 0:

            #print('debut :',self.filters[sprid])
            r,g,b = 0,0,0
            tot_st = 0

            for filterid in self.filters[sprid]:
                col,st = self.filters[sprid][filterid]
                r+=col[0]*st
                g+=col[1]*st
                b+=col[2]*st
                tot_st += st

            moy_st = tot_st/len(self.filters[sprid])
            r/=tot_st
            g/=tot_st
            b/=tot_st

            final_color = (255-r*moy_st,255-g*moy_st,255-b*moy_st)
            #print('fin :',final_color)
            self.filter(sprid,final_color)

    def add_filter(self,sprid,color=(0,255,255),strengh=1,filterid='hit'):

        ### ATTENTION !! POUR LES FILTRES IL FAUT ENVOYER LA COULEUR INVERSE
        ## on veut du rouge à l'écran ? add_filter( (0,255,255) )

        if sprid not in self.filters:
            self.filters[sprid] = {}
        self.filters[sprid][filterid] = (color,strengh)
        self.update_filter(sprid)

    def del_filter(self,sprid,filterid='hit'):
        if sprid in self.filters and filterid in self.filters[sprid]:
            del self.filters[sprid][filterid]
            if len(self.filters[sprid]) == 0:
                del self.filters[sprid]
            else:
                self.update_filter(sprid)
        self.filter(sprid,(255,255,255))

    def spr(self,id):
        if id in self.sprites:
            return self.sprites[id]
        return None

    def box(self,id):
        spr = self.sprites[id]
        return [spr.x,spr.y,spr.x+spr.width,spr.y+spr.height]

    def delete(self,tabids='all'):

        if tabids == 'all': # on delete tous les sprites affichés ingame
            for id in self.sprites:
                self.sprites[id].delete()
            self.sprites = {}
            #print('sprites deleted')

        elif type(tabids) == type('aa'): # on delete un seul sprite precis
            if tabids in self.sprites:
                self.sprites[tabids].delete()
                del self.sprites[tabids]
                #print(tabids,'deleted')

        elif type(tabids) == type([]): # on delete un tableau de sprite
            #print('deleting',tabids)
            for id in tabids:
                self.delete(id)

        elif type(tabids) == type({}): # on delete un dico de sprite
            #print('deleting',tabids)
            for lab in tabids:
                self.delete(tabids[lab])

#manager who rules normal labels
class LabelManager():

    def __init__(self,fonts=None):

        if fonts != None:
            self.fonts = fonts
            self.font = fonts[0]
        else:
            self.fonts = ['arial']
            self.font = 'arial'
        ## RaubFont

        self.labels = {}
        self.ids = []

    def updateman(self,fonts=None):

        if fonts != None:
            self.fonts = fonts
            self.font = fonts[0]
        else:
            self.fonts = ['arial']
            self.font = 'arial'

    def addLab(self,contenu,xy_pos=(0,0),alr_id=-1,vis=True,font_name=None,font_size=30,group='hud'
                ,anchor = ('left','bottom'),color=(255,255,255,255),use_str_bien=False,w=20):

        if alr_id == -1:
            id = u.get_id('lbl')
            self.ids.append(id)
        else:
            id =alr_id

        if font_name == None:
            font_name = self.font
        elif type(font_name) == int:
            font_name = self.fonts[font_name]

        if type(contenu) != type('qsd'):
            contenu = str(contenu)

        if use_str_bien:
            contenu = u.str_bien(contenu,w)

        multi = '\n' in contenu

        anchor_x,anchor_y= anchor

        if multi:
            width = 4000
            anchor_x = 'center'
        else:
            width = None

        if group != None:
            group = gman.getGroup(group)
        self.labels[id] = pyglet.text.Label(contenu,font_name=font_name,font_size=font_size,group=group, \
                        batch=tman.batch,anchor_x= anchor_x,anchor_y= anchor_y,color=color,multiline=multi,width=width,align='center')



        self.labels[id].x,self.labels[id].y = xy_pos
        self.unhide(id,not vis)
        #self.labels[id].visible = vis


        return id

    def addToGroup(self,id,thg=['bg_buildings_loin',None],thg2=0,level_to_put_in=0):

        group = gman.createGroup(thg,thg2,level_to_put_in)
        #print('GROUP IS',group)
        self.labels[id]._init_groups(group)
        self.labels[id]._update()

    def unhide(self,tabids,hide=False):
        ## unhide(machin) AFFICHE machin
        ## unhide(machin,True) N'AFFICHE PAS machin

        if type(tabids) == type([]):
            for id in tabids:
                self.unhide(id,hide)
        elif type(tabids) == type({}):
            for id in tabids:
                self.unhide(tabids[id],hide)
        else:
            if hide == False and self.labels[tabids].color[3] == 0:
                self.labels[tabids].color = [*self.labels[tabids].color[:3],255]
            elif hide == True and self.labels[tabids].color[3] != 0:
                self.labels[tabids].color = [*self.labels[tabids].color[:3],0]

    def set_text(self,lblid,contenu):

        if type(contenu) != type('qsdd'):
            contenu = str(contenu)

        if self.labels[lblid].text != contenu:
            self.labels[lblid].text = contenu

    def printGroup(self,lblid):
        print('\ttopgroup :',self.labels[lblid].top_group)
        print('\tbackgroup :',self.labels[lblid].background_group)
        print('\tforegroup :',self.labels[lblid].foreground_group)
        print('\tforegroupdeco :',self.labels[lblid].foreground_decoration_group)

    def modify(self,lblid,pos=None,size=None,scale=None,color=None):

        if scale != None :
            newsize = self.labels[lblid].font_size*scale
            self.labels[lblid].font_size = int(newsize)

        if size != None:
            self.labels[lblid].font_size = size

        if pos != None:
            if pos[0] != None and pos[0] != self.labels[lblid].x:
                self.labels[lblid].x = pos[0]
            if pos[1] != None and pos[1] != self.labels[lblid].y:
                self.labels[lblid].y = pos[1]

        if color != None and color != self.labels[lblid].color:
            self.labels[lblid].color = color

    def delete(self,tabids='all'):

        if tabids == 'all': # on delete tous les labels affichés ingame
            for id in self.labels:
                self.labels[id].delete()
            self.labels = {}
            #print('labels deleted')

        elif type(tabids) == type('aa'): # on delete un seul label precis
            self.labels[tabids].delete()
            del self.labels[tabids]
            #print(tabids,'deleted')

        elif type(tabids) == type([]): # on delete un tableau de label
            #print('deleting',tabids)
            for id in tabids:
                self.delete(id)

        elif type(tabids) == type({}): # on delete un dico de label
            #print('deleting',tabids)
            for lab in tabids:
                self.delete(tabids[lab])

sman,lman = SpriteManager(),LabelManager()

class ParticleManager():

    def __init__(self):
        self.sprites = {}
        self.sprites['normal'] = {}
        self.sprites['steam'] = {}
        self.sprites['steam2'] = {}

        self.labels = {}
        self.labels['normal'] = {}
        self.labels['icons'] = {}
        self.labels['dmg'] = {}
        self.labels['say'] = {}

    def addPart(self,textid,xy_pos=(0,0),duree=5,group=None,key='normal',opac=255,vis=True):

        id = u.get_id('spr_part')
        #self.ids.append(id)

        self.sprites[key][id] = pyglet.sprite.Sprite(tman.textures[textid], batch=tman.batch,visible=vis)
        self.sprites[key][id].position = xy_pos
        self.sprites[key][id].opacity = opac

        if group != None:
            group = gman.getGroup(group)
            self.sprites[key][id].group = group

        bertran.schedule_once(self.delay_spr,duree*0.01,id,key)

    def addLabPart(self,contenu,xy_pos=(0,0),duree=5,font_name=None,font_size=20,group=None,anchor = \
                ('center','center'),color=(255,255,255,255),key='normal',vis=True,use_str_bien=True,w=20):

        id = u.get_id('lab_part')

        if font_name == None:
            font_name = lman.font
        elif type(font_name) == int:
            font_name = lman.fonts[font_name]

        if not vis:
            color = [*color[:3],0]

        if type(contenu) != type('qsd'):
            contenu = str(contenu)

        if use_str_bien:
            contenu = u.str_bien(contenu,w)

        multi = '\n' in contenu

        anchor_x,anchor_y= anchor

        if multi:
            width = 2000
            anchor_x = 'center'
        else:
            width = None


        if group != None:
            group = gman.getGroup(group)
        self.labels[key][id] = pyglet.text.Label(contenu,font_name=font_name,font_size=font_size,group=group, \
                        batch=tman.batch,anchor_x= anchor_x,anchor_y= anchor_y,color=color,multiline=multi,align='center',width=width)

        self.labels[key][id].x,self.labels[key][id].y = xy_pos

        bertran.schedule_once(self.delay_lab,duree*0.01,id,key)
        return key,id

    def alert(self,contenu):
        xy_pos = scr.cx,3*scr.cy/2
        color = (255,20,20,255)
        duree = 10
        size = 40
        self.addLabPart(contenu,xy_pos,duree,font_size=size,color=color,group='ui',use_str_bien=False)

    def addCol(self,col=(255,255,255,255),box=u.box(),duree=5,group=None,key='normal'):
        pass
        ## not optimized so plz correct it
        """text = tman.addCol(col)
        self.addPart(text,box.xy,duree,group,key)"""

    def delay_spr(self,dt,id,key):

        #print(id)
        self.sprites[key][id].opacity = self.sprites[key][id].opacity-(0.1*255)
        if self.sprites[key][id].opacity <= 0:
            self.sprites[key][id].delete()
            del self.sprites[key][id]
        else:
            bertran.schedule_once(self.delay_spr,dt,id,key)

    def delay_lab(self,dt,id,key):

        if key in self.labels and id in self.labels[key]:
            self.labels[key][id].color = (*self.labels[key][id].color[:3]  , int(self.labels[key][id].color[3]-(0.1*255)))
            if self.labels[key][id].color[3] <= 0:
                self.labels[key][id].delete()
                del self.labels[key][id]
            else:
                bertran.schedule_once(self.delay_lab,dt,id,key)

    def modify(self,key,dx=0,dy=0,setx=None,sety=None):
        if key in self.sprites:
            for id in self.sprites[key]:
                if setx == None:
                    self.sprites[key][id].x += dx
                else:
                    self.sprites[key][id].x = setx
                if sety == None:
                    self.sprites[key][id].y += dy
                else:
                    self.sprites[key][id].y = sety
        else:
            for id in self.labels[key]:
                if setx == None:
                    self.labels[key][id].x += dx
                else:
                    self.labels[key][id].x = setx
                if sety == None:
                    self.labels[key][id].y += dy
                else:
                    self.labels[key][id].y = sety

    def modify_single(self,keyid,dx=0,dy=0,setx=None,sety=None):
        key,id = keyid
        if key in self.labels and id in self.labels[key]:
            if setx == None:
                self.labels[key][id].x += dx
            else:
                self.labels[key][id].x = setx
            if sety == None:
                self.labels[key][id].y += dy
            else:
                self.labels[key][id].y = sety

        elif key in self.sprites and id in self.sprites[key]:
            if setx == None:
                self.sprites[key][id].x += dx
            else:
                self.sprites[key][id].x = setx
            if sety == None:
                self.sprites[key][id].y += dy
            else:
                self.sprites[key][id].y = sety

    def unhide(self,key,hide=False):
        if key in self.sprites:
            for id in self.sprites[key]:
                if self.sprites[key][id].visible != (not hide):
                    self.sprites[key][id].visible = (not hide)
        else:
            for id in self.labels[key]:
                if hide == False and self.labels[key][id].color[3] == 0:
                    self.labels[key][id].color = [*self.labels[key][id].color[:3],255]
                elif hide == True and self.labels[key][id].color[3] != 0:
                    self.labels[key][id].color = [*self.labels[key][id].color[:3],0]

    def unhide_single(self,keyid,hide=False):
        key,id = keyid
        if key in self.sprites and id in self.sprites[key]:
            if self.sprites[key][id].visible != (not hide):
                self.sprites[key][id].visible = (not hide)

        elif key in self.labels and id in self.labels[key]:
            if hide == False and self.labels[key][id].color[3] == 0:
                self.labels[key][id].color = [*self.labels[key][id].color[:3],255]
            elif hide == True and self.labels[key][id].color[3] != 0:
                self.labels[key][id].color = [*self.labels[key][id].color[:3],0]

    def delete(self,keyid):
        key,id = keyid
        if key in self.labels and id in self.labels[key]:
            self.labels[key][id].delete()
            del self.labels[key][id]

        elif key in self.sprites and id in self.sprites[key]:
            self.sprites[key][id].delete()
            del self.sprites[key][id]


pman = ParticleManager()

TEXTIDS = {}
TEXTIDS['col'] = {}



"""'''''''''''''''''''''''''''''''''
'''''''PART TWO : CCCC STUFF''''''''
'''''''''''''''''''''''''''''''''"""

#### KEYS ->  Not graphic nor C but t'as capté ya un K ça passe

keys = []
longpress = {}

#cooldown = 0.5

def cooldown_one(key,obj):
    cooldown = obj.cooldown
    if key in longpress:
        perc = (time.time()-longpress[key])/cooldown
        if perc > 1:
            longpress[key] = time.time()
        return perc

    return 0


#### CYCLE -> rules day/night cycle

MODE_COLOR = 1 ## 1 pour avoir des couleurs wtf et 0 pour la "réalité"

class Cycle():

    def __init__(self):

        # general

        self.len = 20 # longueur du cycle en secondes
        self.dt = 0.05 # dt avant chaque update

        self.tick = 0

        self.day = 1 # nb de jour

        self.plus_sprids = []

    def launch(self,perso,bg):

        self.perso = perso

        # sprites

        self.ext_sprids = bg # tableau contenant les ids des sprites à colorer et le pourcentage d'effectif que le cycle a sur lui
        # (plus ce pourcentage se rapporche de 1 plus ça va devenir noir)

        #self.plus_sprids = [] # pareil mais en bonus (ce tableau là va être modifié souvent)

        self.sprids = {} # en plus on crée un dic qui va contenir les spr controlés directement par le cycle : type soleil, lune, etoile et meme weather ?
        self.sprids['sun'] = sman.addSpr(TEXTIDS['sun'],(scr.w/2,0),'moon_sun')
        sman.modify(self.sprids['sun'],scale=(0.75,0.75))
        self.sprids['moon'] = sman.addSpr(TEXTIDS['moon'],(scr.w/4,0),'moon_sun')
        sman.modify(self.sprids['moon'],scale=(0.75,0.75))
        self.sprids['stars'] = sman.addSpr(TEXTIDS['stars'],(0,0),'stars')
        sman.modify(self.sprids['stars'],scale=(0.75,0.75),opacity=0)

        #COLORS
        self.newteinte()

        self.ticked()

    def ticked(self,dt=0):

        self.tick += 1
        #print(self.tick)
        if self.tick*self.dt > self.day*self.len:
            self.day_update()
        day_percentage = (self.tick*self.dt - (self.day-1)*self.len )/self.len
        #print(day_percentage)
        self.update(day_percentage)

        bertran.schedule_once(self.ticked,self.dt)

    def update(self,day_percentage):
        ## color
        p=day_percentage
        r,g,b = self.R(p),self.G(p),self.B(p)

        ## bg
        for id,prc in self.ext_sprids+self.plus_sprids:
            sman.add_filter(id,[255*r,255*g,255*b],prc,'env')

        ## sun
        ysun = p*4*scr.h-0.6*scr.h
        sman.modify(self.sprids['sun'],pos=(None,ysun))
        sman.add_filter(self.sprids['sun'],[255*r,255*g,255*b],1,'env')

        ## moon
        pm = p-0.5
        if pm < 0:
            pm = 1+pm
        ymoon = pm*4*scr.h-1.2*scr.h
        sman.modify(self.sprids['moon'],pos=(None,ymoon))
        sman.add_filter(self.sprids['moon'],[255*r,255*g,255*b],0.5,'env')

        ## stars
        if p >= 0.8:
            ps = (p-0.8)*5
            sman.modify(self.sprids['stars'],opacity=ps*255)
        elif p < 0.2:
            ps = (1-p-0.8)*5
            sman.modify(self.sprids['stars'],opacity=ps*255)
        else:
            sman.modify(self.sprids['stars'],opacity=0)

    def add_spr(self,spr):
        self.plus_sprids.append(spr)

    def del_spr(self,spr):
        if spr in self.plus_sprids:
            self.plus_sprids.remove(spr)

    def empty_plus(self):
        self.plus_sprids = []

    def day_update(self):

        #general
        self.day += 1
        self.perso.add_money(-10)
        o.distro.update()

        #teinte
        self.newteinte()

    def newteinte(self):

        self.rr = (random.random()-0.5)
        self.gg = (random.random()-0.5)
        self.bb = (random.random()-0.5)

        if not MODE_COLOR:
            self.rr*=0.1
            self.gg*=0.1
            self.bb*=0.1

        #print('nouvelle teinte :',(self.rr,self.gg,self.bb))

    def roll_mode(self):
        global MODE_COLOR
        MODE_COLOR = not MODE_COLOR
        self.newteinte()

    #rgb
    def R(self,dayperc):
        p = (dayperc*2-1)**2
        p=p+self.rr
        if p <0:
            return 0
        return p
    def G(self,dayperc):
        p = 1-sin(dayperc*pi)
        p=p+self.gg
        if p <0:
            return 0
        return p
    def B(self,dayperc):
        if dayperc < 0.5:
            p=1-dayperc*2
        else:
            p=(dayperc-0.5)*2
        p=p+self.bb
        if p <0:
            return 0
        return p

    def __str__(self):
        # retourne l'heure actuelle
        p = (self.tick*self.dt - (self.day-1)*self.len )/self.len
        hm = int(p*24*60)
        h = hm//60
        m = (hm%60)

        strh = str(h)
        if len(strh) < 2:
            strh = '0' + strh
        strm = str(m)
        if len(strm) < 2:
            strm = '0' + strm

        return strh+' : '+strm

Cyc = Cycle()

#### CLOCK

class Clock(pyglet.clock.Clock):

    def __init__(self):
        self.__time = 0
        self.speed = 1.0
        pyglet.clock.Clock.__init__(self, time_function=self.get_time)
        pyglet.clock.schedule(self.advance)

    def advance(self, time):
        self.__time += time * self.speed
        self.tick()

    def get_time(self):
        return self.__time

    def set_speed(self, dt=0, speed=1.0):
        self.speed = speed

bertran = Clock() # bertran c'est le S


#### CURSOR

M = [0,0]

class Cursor():

    def __init__(self):

        self.long_time = 0.5 #en secondes

        ##
        self.longbox = None
        self.start_time = None
        self.func = None

    def init(self,window,textures):

        self.window = window
        self.text = textures

        cursor = pyglet.window.ImageMouseCursor(tman.textures[self.text[1]],16,16)
        self.window.set_mouse_cursor(cursor)

    def start_long_press(self,box,func):

        if u.collisionAX(box.realbox,M) and self.start_time == None:

            self.longbox = box
            self.start_time = bertran.get_time()
            self.func = func

            #self.check_long_press(0,xy)
            bertran.schedule(self.check_long_press)

    def check_long_press(self,dt=0):

        #check si on a quitté le box:
        if not u.collisionAX(self.longbox.realbox,M):
            self.reset()
            return 0

        percentage = (bertran.get_time()-self.start_time)/self.long_time
        self.change_skin(percentage)
        #print(percentage)

        if percentage >= 1:
            print('applying',self.func.__name__)
            self.func() # on clique
            self.reset()

    def reset(self):
        bertran.unschedule(self.check_long_press)
        cursor = pyglet.window.ImageMouseCursor(tman.textures[self.text[1]],16,16)
        self.window.set_mouse_cursor(cursor)
        self.longbox = None
        self.start_time = None
        self.func = None

    def change_skin(self,per):
        nb = int(per*8)
        cursor = pyglet.window.ImageMouseCursor(tman.textures[self.text[nb+8]],16,16)
        self.window.set_mouse_cursor(cursor)

Cur = Cursor()

#### CAMERA

SPEED = 20
RSPEED = 100

MOVE_Y = False

class Camera():

    def __init__(self):

        self._X,self._Y = 0,0
        #self.BGX,self.BGY = 0,0
        self._dx,self._dy = 0,0

        self.d = 0.2

        self.speed = SPEED
        self.runspeed = RSPEED

        self.activate = True

    def update(self,persobox,street,run=False):

        if self.activate:
            #scr = (1920,1080)
            #scr = scr.size
            moved = [False,False]

            x,xf = street.xxf
            #print(x,xf)

            if run:
                speed = self.runspeed
            else:
                speed = self.speed

            #X
            if persobox[2] > 4*scr.size[0]/5 and (xf == None or street.rxf > scr.size[0] +speed):
                if run:
                    self.rlessx()
                else:
                    self.lessx()
                moved[0] = True

            elif persobox[0] < scr.size[0]/5 and (x == None or street.x < -speed):
                if run:
                    self.rmorex()
                else:
                    self.morex()
                moved[0] = True

            if xf != None and street.rxf < scr.size[0]:
                if street.rxf < scr.size[0] - self.runspeed:
                    self.rmorex()
                else:
                    self.morex()
                moved[0] = True
            elif x != None and street.x > 0:
                if street.x > self.runspeed:
                    self.rlessx()
                else:
                    self.lessx()
                moved[0] = True


            #Y
            if MOVE_Y:
                if persobox[3] > 19*scr.size[1]/20:
                    self.lessy()
                    moved[1] = True
                elif persobox[1] < scr.size[1]/20:
                    self.morey()
                    moved[1] = True

            ### applyin movement to sprites
            if not moved[1]:
                self._dy = 0
            if not moved[0]:
                if run:
                    self.update(persobox,street)
                else:
                    self._dx = 0

    def tp(self,ge_x,real_x):

        ## ge_x -> position générale du perso après passage par la porte
        ## real_x -> position réelle à l'écran du perso AVANT passage par la porte

        self._X = - ge_x + real_x

    ##

    # if perso walks
    def morex(self):
        self._X += self.speed
        self._dx = self.speed
        #self.BGX = self._X*self.d
    def morey(self):
        self._Y += self.speed
        self._dy = self.speed
        #self.BGY = self._Y*self.d
    def lessx(self):
        self._X -= self.speed
        self._dx = -self.speed
        #self.BGX = self._X*self.d
    def lessy(self):
        self._Y -= self.speed
        self._dy = -self.speed
        #self.BGY = self._Y*self.d

    # if perso runs
    def rmorex(self):
        self._X += self.runspeed
        self._dx = self.runspeed
        #self.BGX = self._X*self.d
    def rlessx(self):
        self._X -= self.runspeed
        self._dx = -self.runspeed
        #self.BGX = self._X*self.d


    ##

    def _setX(self,X):
        if X != self._X:
            self._dx = self._X-X
            self._X = X
            #self.BGX = self.d*X
    def _X(self):
        return self._X
    def _setY(self,Y):
        if Y != self._Y:
            self._dy = self._Y-Y
            self._Y = Y
            #self.BGY = self.d*Y
    def _Y(self):
        return self._Y
    X = property(_X,_setX)
    Y = property(_Y,_setY)

    def _dx(self):
        return self._dx
    def _dy(self):
        return self._dy
    dx = property(_dx)
    dy = property(_dy)

Cam = Camera()

class GodCamera():

    def __init__(self):

        self._X,self._Y = 0,0
        self._dx,self._dy = 0,0

        #self.d = 0.2

        self.speed = 30

    def activate(self,dir='L'):

        if dir == 'L':
            self.X += self.speed
        else:
            self.X -= self.speed

        Cam.activate = False

    def unactivate(self,perso):

        if not Cam.activate:
            self.X,self.Y = 0,0
            Cam.tp(perso.gex,scr.w/2)
            Cam.activate = True

    ###

    def _setX(self,X):
        if X != self._X:
            self._dx = self._X-X
            self._X = X
            #self.BGX = self.d*X
    def _X(self):
        return self._X
    def _setY(self,Y):
        if Y != self._Y:
            self._dy = self._Y-Y
            self._Y = Y
            #self.BGY = self.d*Y
    def _Y(self):
        return self._Y
    X = property(_X,_setX)
    Y = property(_Y,_setY)

    def _dx(self):
        return self._dx
    def _dy(self):
        return self._dy
    dx = property(_dx)
    dy = property(_dy)

GodCam = GodCamera()
