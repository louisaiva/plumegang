
def a(qua):

    basis = (qua)*10
    bonus = 0

    if qua > 0.6:
        bonus += (qua-0.6)*15
    if qua > 0.8:
        bonus += (qua-0.8)*50
    if qua > 0.92:
        bonus += (qua-0.92)*200
    if qua > 0.98:
        bonus += (qua-0.98)*800
    if qua > 0.995:
        bonus += (qua-0.995)*8400

    return int((basis + bonus)*10)

def test2():

    for i in range(20):

        qua = i/20

        b = a(qua)
        print(qua,b)
        #x = (qua-self.qua_score) * self.nb_fans

    for i in range(90,99,2):

        qua = i/100

        b = a(qua)
        print(qua,b)

    for i in range(990,1001,1):

        qua = i/1000

        b = a(qua)
        print(qua,b)

import src.obj as o
o.test3()
