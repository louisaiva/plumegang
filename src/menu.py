"""
CODED by deltasfer
enjoy
"""

from src import graphic as g
from src.colors import *
from collections import OrderedDict

class Menu:

    def __init__(self):

        self.arb = OrderedDict()

        self.arb['play']='play'
        param = OrderedDict()
        param['go home']='go home','play','reset'
        param['nuits colorées'] = 'roll_color','play','reset'
        param['écran'] = OrderedDict()
        for i in range(len(g.scr.screens)):
            scr = g.scr.screens[i]
            nom = scr.get_device_name()
            param['écran'][nom] = 'scr'+str(i)

        self.arb['...'] = param
        self.arb['quit'] = 'quit'

        self.max_len = 4

        """
            play

            param
                cheh
                lezgo

            quit
        """


        self.point = '' ## exemple : "param,screen,opac"
        self.cursor = 0


        ## labels

        self.labids = {}
        (w,h) = g.scr.size
        padding = 100
        self.size = 30
        x = w/2
        y = h/2 + (self.max_len*self.size + (self.max_len-1)*padding)/2
        for i in range(self.max_len):
            y = y-padding
            self.labids[i] = g.lman.addLab('',(x,y),font_size=self.size,group='up',vis=False,anchor=('center','center'))

        self.actualise()

    def actualise(self):

        cont = list(self.get_dic().keys())

        vis = g.lman.labels[self.labids[0]].color[3]
        #print(list(c["yellow"])[:3],vis)

        g.lman.unhide(self.labids,True)
        for i in range(len(cont)):
            g.lman.set_text(self.labids[i],cont[i])
            if self.cursor == i:
                g.lman.modify(self.labids[i],size=50,color=list(c["yellow"])[:3]+[vis])
            else:
                g.lman.modify(self.labids[i],size=self.size,color=list(c["white"])[:3]+[vis])

    def reset(self):
        self.point = ''
        self.cursor = 0
        self.actualise()

    ##

    def click(self):

        if type(list(self.get_dic().values())[self.cursor]) == type(self.arb):
            name_dic = list(self.get_dic().keys())[self.cursor]
            if self.point == '':
                self.point = name_dic
            else:
                self.point = self.point+','+name_dic
            self.cursor = 0
            #print('waoouh',name_dic,self.point,self.cursor)
            self.actualise()
            return name_dic
        else:
            return list(self.get_dic().values())[self.cursor]

    def unclick(self):
        if self.point == '':
            return 'play'
        else:
            self.point = ','.join(self.point.split(',')[:-1])
            print(self.point)
            self.cursor = 0
            self.actualise()

    def up(self):
        self.cursor -= 1
        if self.cursor < 0:
            self.cursor = self.get_current_maxcurs()-1
        self.actualise()

    def down(self):
        self.cursor += 1
        if self.cursor >= self.get_current_maxcurs():
            self.cursor = 0
        self.actualise()

    ##

    def get_dic(self):
        depth = 0
        if self.point != '':
            path = self.point.split(',')
            depth = len(path)

        dic = self.arb
        for i in range(depth):
            dic = dic[path[i]]
        return dic

    def get_current_maxcurs(self):
        return len(self.get_dic())

    def unhide(self,hide=False):
        ## unhide() AFFICHE le menu
        ## unhide(True) N'AFFICHE PAS le menu

        g.lman.unhide(self.labids,hide)
