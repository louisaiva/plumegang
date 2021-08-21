import pyglet


class MyClock(pyglet.clock.Clock):

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
        #print("Set speed", speed)
        self.speed = speed

bertran = MyClock()
# bertran c'est le S
