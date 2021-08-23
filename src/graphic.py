"""
CODED by deltasfer
enjoy
"""



import pyglet
import src.utils as u

"""""""""""""""""""""""""""""""""""
 PART ONE : GRAPHIC STUFF
"""""""""""""""""""""""""""""""""""

class ScreenManager():
    def __init__(self):

        self.display = pyglet.canvas.get_display()
        self.screens = self.display.get_screens()

    def current_screen(self):
        return self.screens[0]

    def size(self):
        return (self.current_screen().width,self.current_screen().height)

scr = ScreenManager()

#manager who rules groups to draw things in the right order u know
class GroupManager():

    def __init__(self):


        self.groups = {} ## give the group with the name

        self.names_wo = {} ## give the name with the order
        self.orders = {} ## give the order with the name

        names = ['back-2','back-1','back','back1','mid-1','mid','mid1','front','perso-1','hud-1','hud','hud1','perso','midup','ui-2','ui-1','ui','up-1','up']
        self.distance_btw = 8

        for i in range(len(names)):
            self.addGroup(names[i],i*self.distance_btw)

    def getGroup(self,name):
        if name not in self.groups:
            print('aie ce groupe n\'existe pas')
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

    def loadImSeq(self,path2,size):

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

    def loadIm(self,path2):

        path3 = '/item/'
        id = u.get_id('img')
        img = pyglet.image.load(self.path+path3+path2)
        self.textures[id] = img
        self.ids.append(id)
        return id

    def addCol(self,w,h,color=(255,255,255,255)):

        pattern = pyglet.image.SolidColorImagePattern(color)
        id = u.get_id('col')
        self.textures[id] = pattern.create_image(w,h)
        self.ids.append(id)
        return id

    def draw(self):
        self.batch.draw()

tman,gman = TextureManager(),GroupManager()

#manager who rules normal sprites
class SpriteManager():

    def __init__(self):

        ## SPRITES

        self.sprites = {}

        self.ids = []

    def addSpr(self,textid,xy_pos=(0,0),group=None,alr_id=-1,vis=True):

        if alr_id == -1:
            id = u.get_id('spr')
            self.ids.append(id)
        else:
            id =alr_id


        self.sprites[id] = pyglet.sprite.Sprite(tman.textures[textid], batch=tman.batch)
        self.sprites[id].position = xy_pos
        self.sprites[id].visible = vis

        if group != None:
            self.addToGroup(id,group)

        return id

    def addCol(self,col=(255,255,255,255),box=u.box(),group=None,alr_id=-1,vis=True):
        text = tman.addCol(*box.wh,col)
        return self.addSpr(text,box.xy,group,alr_id,vis)

    def addToGroup(self,id,group_name='back'):

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

    def modify(self,sprid,pos=None,scale=None,group=None,opacity=None):

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
        self.sprites[sprid].update(x=x,y=y,scale_x = scalex,scale_y=scaley)

    def filter(self,sprid,color=(255,0,0)):
        self.sprites[sprid].color = color

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

    def __init__(self,font=None):

        if font != None:
            self.font = font
        else:
            self.font = 'arial'

        self.labels = {}
        self.ids = []

    def updateman(self,font=None):

        if font != None:
            self.font = font
        else:
            self.font = 'arial'

    def addLab(self,contenu,xy_pos=(0,0),alr_id=-1,vis=True,font_name=None,font_size=30,group='hud',anchor = ('left','bottom'),color=(255,255,255,255)):

        if alr_id == -1:
            id = u.get_id('lbl')
            self.ids.append(id)
        else:
            id =alr_id

        if not font_name:
            font_name = self.font

        if type(contenu) != type('qsd'):
            contenu = str(contenu)

        multi = '\n' in contenu

        anchor_x,anchor_y= anchor

        if multi:
            maxwidth=0
            lines = contenu.split('\n')
            for line in lines:
                lab = pyglet.text.Label(line,font_name=font_name,font_size=font_size, \
                                anchor_x= anchor_x,anchor_y= anchor_y,color=color)
                maxwidth = max(maxwidth,lab.content_width)
                lab.delete()
            width = maxwidth+1

        else:
            width = None


        if group != None:
            group = gman.getGroup(group)
        self.labels[id] = pyglet.text.Label(contenu,font_name=font_name,font_size=font_size,group=group, \
                        batch=tman.batch,anchor_x= anchor_x,anchor_y= anchor_y,color=color,multiline=multi,width=width)



        self.labels[id].x,self.labels[id].y = xy_pos
        self.unhide(id,not vis)
        #self.labels[id].visible = vis


        return id

    def addToGroup(self,id,thg=['back',None],thg2=0,level_to_put_in=0):

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

        if scale != None and scale != (self.labels[lblid].scale_x,self.labels[lblid].scale_y):
            self.labels[lblid].update(scale_x = scale[0],scale_y=scale[1])
            #self.labels[lblid].scale_x,self.labels[lblid].scale_y = scale

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
                ('center','center'),color=(255,255,255,255),key='normal',vis=True):

        id = u.get_id('lab_part')

        if not font_name:
            font_name = lman.font

        if not vis:
            color = [*color[:3],0]

        if type(contenu) != type('qsd'):
            contenu = str(contenu)

        anchor_x,anchor_y= anchor

        if group != None:
            group = gman.getGroup(group)
        self.labels[key][id] = pyglet.text.Label(contenu,font_name=font_name,font_size=font_size,group=group, \
                        batch=tman.batch,anchor_x= anchor_x,anchor_y= anchor_y,color=color)

        self.labels[key][id].x,self.labels[key][id].y = xy_pos

        bertran.schedule_once(self.delay_lab,duree*0.01,id,key)

    def addCol(self,col=(255,255,255,255),box=u.box(),duree=5,group=None,key='normal'):
        text = tman.addCol(*box.wh,col)
        self.addPart(text,box.xy,duree,group,key)

    def delay_spr(self,dt,id,key):

        #print(id)
        self.sprites[key][id].opacity = self.sprites[key][id].opacity-(0.1*255)
        if self.sprites[key][id].opacity <= 0:
            self.sprites[key][id].delete()
            del self.sprites[key][id]
        else:
            bertran.schedule_once(self.delay_spr,dt,id,key)

    def delay_lab(self,dt,id,key):

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


pman = ParticleManager()

TEXTIDS = {}


"""""""""""""""""""""""""""""""""""
 PART TWO : CCCC STUFF
"""""""""""""""""""""""""""""""""""


#### CYCLE -> rules day/night cycle
class Cycle():

    def __init__(self,perso):

        # general

        self.len = 10 # longueur du cycle en secondes
        self.dt = 1 # dt avant chaque update

        self.tick = 0

        self.day = 1 # nb de jour

        self.perso = perso

        # sprites

        """self.sprids = {}
        self.sprids['sun'] ="""



        self.ticked()

    def ticked(self,dt=0):

        self.tick += 1
        #print(self.tick)
        if self.tick*self.dt > self.day*self.len:
            self.day += 1
            #print('wow new day')
            self.perso.add_money(-10)
        day_percentage = (self.tick*self.dt - (self.day-1)*self.len )/self.len
        #print(day_percentage)

        bertran.schedule_once(self.ticked,self.dt)

    def update(self,day_percentage):
        pass

M = [0,0]

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

class Camera():

    def __init__(self):

        self._X,self._Y = 0,0
        #self.BGX,self.BGY = 0,0
        self._dx,self._dy = 0,0

        self.d = 0.2

        self.speed = 12

    def update(self,persobox,street):

        scr = (1920,1080)
        moved = [False,False]

        x,xf = street.xxf
        #print(x,xf)

        #X
        if persobox[2] > 4*scr[0]/5 and (xf == None or street.rxf > scr[0] +self.speed):
            self.lessx()
            moved[0] = True

        elif persobox[0] < scr[0]/5 and (x == None or street.x < -self.speed):
            self.morex()
            moved[0] = True

        if xf != None and street.rxf < scr[0]:
            self.morex()
            moved[0] = True
        elif x != None and street.x > 0:
            self.lessx()
            moved[0] = True

        #print(street.x,street.rxf)

        #Y
        if persobox[3] > 7*scr[1]/8:
            self.lessy()
            moved[1] = True
        elif persobox[1] < scr[1]/8:
            self.morey()
            moved[1] = True

        #moved
        if not moved[0]:
            self._dx = 0
        if not moved[1]:
            self._dy = 0

    ##

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
