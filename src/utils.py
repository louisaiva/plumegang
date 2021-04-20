



import random,os,ctypes,time
from ctypes import windll, Structure, c_long, byref
from math import *
#from win32gui import GetWindowRect, GetForegroundWindow, GetWindowText


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

    def _xywh(self):
        return self.x,self.y,self.w,self.h

    wh = property(_wh)
    xy = property(_xy)
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
        try:
            for file in os.listdir(bigpath+chem):
                if file[-3:] == '.py':
                    with open(bigpath+chem+'/'+file,'r') as f:
                        long += len(f.readlines())
        except :
            jsghd=0
            #print('no path',bigpath+chem,':',os.listdir(bigpath+chem))

    return long


# collision
def collision(a,b):
    if (a[0] > b[2]) or (a[2] < b[0]) or (a[1] > b[3]) or (a[3] < b[1]):
        return False #  oklm c'est bon ca collisionne PAS
    else:
        return True # aoutch ca collisionne
