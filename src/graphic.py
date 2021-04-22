



import pyglet
import src.utils as u



#manager who rules groups to draw things in the right order u know
class GroupManager():

    def __init__(self):


        self.groups = {} ## give the group with the name

        self.names_wo = {} ## give the name with the order
        self.orders = {} ## give the order with the name

        names = ['back','back1','mid-1','mid','mid1','front','hud-1','hud','hud1','perso','ui-1','ui','up']
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

        anchor_x,anchor_y= anchor

        if group != None:
            group = gman.getGroup(group)
        self.labels[id] = pyglet.text.Label(contenu,font_name=font_name,font_size=font_size,group=group, \
                        batch=tman.batch,anchor_x= anchor_x,anchor_y= anchor_y,color=color)
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

    def modify(self,lblid,pos=None,scale=None,color=None):

        if scale != None and scale != (self.labels[lblid].scale_x,self.labels[lblid].scale_y):
            self.labels[lblid].update(scale_x = scale[0],scale_y=scale[1])
            #self.labels[lblid].scale_x,self.labels[lblid].scale_y = scale

        if pos != None and pos != (self.labels[lblid].x,self.labels[lblid].y):
            self.labels[lblid].x,self.labels[lblid].y = pos

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

TEXTIDS = {}



#### CAMERA

class Camera():

    def __init__(self):

        self._X,self._Y = 0,0
        self.BGX,self.BGY = 0,0

        self.d = 0.2

        self.speed = 12

    def update(self,persobox):

        scr = (1920,1080)

        if persobox[2] > 4*scr[0]/5:
            self.lessx()
        elif persobox[0] < scr[0]/5:
            self.morex()

        if persobox[3] > 7*scr[1]/8:
            self.lessy()
        elif persobox[1] < scr[1]/8:
            self.morey()

    ##

    def morex(self):
        self._X += self.speed
        self.BGX = self._X*self.d
    def morey(self):
        self._Y += self.speed
        self.BGY = self._Y*self.d
    def lessx(self):
        self._X -= self.speed
        self.BGX = self._X*self.d
    def lessy(self):
        self._Y -= self.speed
        self.BGY = self._Y*self.d


    ##

    def _setX(self,X):
        if X != self._X:
            self._X = X
            self.BGX = self.d*X
    def _X(self):
        return self._X
    def _setY(self,Y):
        if Y != self._Y:
            self._Y = Y
            self.BGY = self.d*Y
    def _Y(self):
        return self._Y
    X = property(_X,_setX)
    Y = property(_Y,_setY)

Cam = Camera()
