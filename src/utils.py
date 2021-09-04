"""
CODED by deltasfer
enjoy
"""



import random,os,ctypes,time
#from __future__ import division

from math import *
#from win32gui import GetWindowRect, GetForegroundWindow, GetWindowText
if os.name == 'nt':
    from ctypes import windll, Structure, c_long, byref
    class POINT(Structure):
        _fields_ = [("x", c_long), ("y", c_long)]

class box():

    def __init__(self,x=0,y=0,w=30,h=30):

        self.w = w
        self.h = h
        self.x = x
        self.y = y

    def _wh(self):
        return self.w,self.h

    def _xy(self):
        return self.x,self.y

    def _setxy(self,xy):
        self.x,self.y = xy

    def _xywh(self):
        return self.x,self.y,self.w,self.h

    wh = property(_wh)
    xy = property(_xy,_setxy)
    xywh = property(_xywh)


    def _centerx(self):
        return self.x + self.w/2

    def _centery(self):
        return self.y + self.h/2

    def _center(self):
        return self.centerx,self.centery

    cx = property(_centerx)
    cy = property(_centery)
    cxy = property(_center)

    def _fx(self):
        return self.x+self.w

    def _fy(self):
        return self.y+self.h

    def _realbox(self):
        return self.x,self.y,self.fx,self.fy

    fx = property(_fx)
    fy = property(_fy)
    realbox = property(_realbox)

class line():

    def __init__(self,x=0,y=0,xf=0,yf=0):

        self.x = x
        self.y = y

        self.vert = x == xf

        if self.vert:
            self.w = yf-y
        else:
            self.w = xf-x

    def _xf(self):
        if self.vert:
            return self.x
        return self.x + self.w
    def _yf(self):
        if self.vert:
            return self.y + self.w
        return self.y
    def _vert(self):
        return self.x == self.xf

    def _xy(self):
        return self.x,self.y
    def _setxy(self,xy):
        self.x,self.y = xy
    def _line(self):
        return ( (self.x,self.y) , (self.xf,self.yf) )

    #w = property(_w)
    #vert = property(_vert)
    xf = property(_xf)
    yf = property(_yf)

    xy = property(_xy,_setxy)
    line = property(_line)


    def _centerx(self):
        if self.vert:
            return self.x
        return self.x + self.w/2

    def _centery(self):
        if self.vert:
            return self.y + self.w/2
        return self.y

    def _center(self):
        return self.cx,self.cy

    cx = property(_centerx)
    cy = property(_centery)
    cxy = property(_center)

## partie SCREEN

def get_screen_size():
    user32 = ctypes.windll.user32
    return user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)


## partie random

def choice(thg):

    if type(thg) == type({}):
        return choice(list(thg.keys()))
        #print(thg.keys())
    else:
        return random.choice(thg)

def randmultint(n,a,b=None): #returns n differents numbers between a and b-1

    if b == None:
        return randmultint(n,0,a-1)
    else:
        t = []
        while len(t) < n:
            new = random.randint(a,b-1)
            while new in t:
                new = random.randint(a,b-1)
            t.append(new)
        return t


def get_key_from_value(d,v,s=[]): # v valeur seule, d dic ou tab

    if type(d) == type({}):
        for key,val in d.items():
            if type(val) != type({}) and type(val) != type([]):
                if v == val:
                    return s+[key]
            else:
                ns = get_key_from_value(val,v,s+[key])
                if ns != None:
                    return ns

    elif type(d) == type([]):
        for key in range(len(d)):
            val = d[key]
            if type(val) != type({}) and type(val) != type([]):
                #print(val)
                if v == val:
                    return s+[key]
            else:
                ns = get_key_from_value(val,v,s+[key])
                if ns != None:
                    return ns

    return None

def getMousePos():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt.x,pt.y

def module(x,y):
    return sqrt(x**2+y**2)

def int_rd(dec):
    if dec < int(dec)+0.5:
        return int(dec)
    else:
        return ceil(dec)

def sign(n):
    if n==0:
        return 0
    else:
        return n//abs(n)

def rangef(a,b,d=1):

    res = []
    if b > a:
        while b>a:
            res.append(a)
            a+=d
    else:
        while abs(b-a)>0:
            res.append(a)
            a+=d

    return res

def convert_huge_nb(n,letters = True):

    if letters:

        if n <= 0:
            return str(n)

        tab = ['',' K',' M',' T']

        for i in range(4,0,-1):
            f = n/(1000**(i-1))
            if f > 1:
                if f >= 10:
                    return str(int(f))+tab[i-1]
                else:
                    if tab[i-1] == '':
                        return str(int(f))
                    return trunc(f,1)+tab[i-1]
            elif f == 1:
                if tab[i-1] == '':
                    return str(int(f))
                return trunc(f,1)+tab[i-1]



# partie ids

ids = 1112

def get_id(key):

    global ids

    id = ''+key
    id+=str(ids)
    ids+=1
    return id

def mycopy(thg):

    if type(thg) == type([]):

        res = []

        for i in thg:
            res.append(mycopy(i))

        return res

    else:

        return thg

def trunc(f, n=3):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

### PARTIE AUTO-SAUVEGARDE
def compt(bigpath,path = ['/.','/src']):

    long = 0

    for chem in path:
        for file in os.listdir('.'+chem):
            if file[-3:] == '.py':
                with open('.'+chem+'/'+file,'r', encoding="utf8") as f:
                    long += len(f.readlines())

    return long


# collision
def collisionAB(a,b):
    if (a[0] > b[2]) or (a[2] < b[0]) or (a[1] > b[3]) or (a[3] < b[1]):
        return False #  oklm c'est bon ca collisionne PAS
    else:
        return True # aoutch ca collisionne

def collisionAX(a,pos):

    if pos[0] > a[2]:
        return False #  oklm c'est bon ca collisionne PAS
    if pos[0] < a[0]:
        return False #  oklm c'est bon ca collisionne PAS
    if pos[1] > a[3]:
        return False #  oklm c'est bon ca collisionne PAS
    if pos[1] < a[1]:
        return False #  oklm c'est bon ca collisionne PAS
    return True # aoutch ca collisionne

def line_intersection(line1, line2):

    ## line 1 : [ (xdep,zdep) , (xfinal,zfinal) ]
    ## line 2 : [ (xdep,zdep) , (xfinal,zfinal) ]
    ## sortie : (xinter,zinter)

    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div == 0:
       return None,None

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return int(x), int(y)


def util_line(line):
    A = (line[0][1] - line[1][1])
    B = (line[1][0] - line[0][0])
    C = (line[0][0]*line[1][1] - line[1][0]*line[0][1])
    return A, B, -C

def line_intersection2(line1, line2):

    L1 = util_line(line1)
    L2 = util_line(line2)

    D  = L1[0] * L2[1] - L1[1] * L2[0]
    Dx = L1[2] * L2[1] - L1[1] * L2[2]
    Dy = L1[0] * L2[2] - L1[2] * L2[0]
    if D != 0:
        x = Dx / D
        y = Dy / D
        if point_in_segment((x,y),line1) and point_in_segment((x,y),line2):
            return x,y

    return False

def point_in_segment(C,line):
    A,B = line
    AB = B[0]-A[0],B[1]-A[1]
    AC = C[0]-A[0],C[1]-A[1]

    Kac = AB[0]*AC[0] + AB[1]*AC[1]
    Kab = AB[0]*AB[0] + AB[1]*AB[1]

    if Kac >= 0 and Kac <= Kab:
        return True
    return False
