import math
            
class Bullet:
    SPEED = 3
    START_OFFSET = 2
    def __init__(self, angle, display):
        self.display = display
        self.start_position = None # when ship moves bullet needs an anchor point
        self.distance = Bullet.START_OFFSET # from start position
        self.rad = math.radians(angle)#*math.pi/180
        self.hit = False
        self.update()
           
    def update(self):
        self.distance += Bullet.SPEED
        x = int(self.distance * math.sin(self.rad)) + 64
        y = int(-self.distance * math.cos(self.rad)) + 32
        if x <= 0 or x >= 128 or y <= 0 or y >= 64:
            return False
        self.display.pixel(x,y,self.display.white)
        self.position = (x,y)
        return True