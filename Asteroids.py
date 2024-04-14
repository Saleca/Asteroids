import random
import math

class Stars:
    def __init__(self, display):
        self.display = display
        self.stars = []
        for x in range(30):
            self.stars.append((random.randint(0,128), random.randint(0,64)))
            
    def update(self):
        for star in self.stars:
            self.display.pixel(star[0],star[1], self.display.white)
            
class Bullet:
    def __init__(self, angle, display):
        self.display = display
        self.dist = 5
        self.angle = angle
        self.hit = False
        self.update()
           
    def update(self):
        rad = self.angle*math.pi/180
        x = int(self.dist * math.sin(rad)) + 64
        y = int(-self.dist * math.cos(rad)) + 32
        if x <= 0 or x >= 128:
            return False
        if y <= 0 or y >= 64:
            return False
        self.display.pixel(x,y,self.display.white)
        self.dist += 3
        self.pos = (x,y)
        return True
        
class Asteroid:
    def __init__(self, display, startDist, fragment = False, startPos = (0,0)):
        self.display = display
        self.startDist = startDist
        self.asteroid = []
        for angle in range(0,360, 45 if fragment else 36):
            rad = angle*math.pi/180
            variation = random.randint(0,3) if fragment else random.randint(-3,3)
            x = int((-self.startDist+variation) * math.sin(rad))
            y = int((self.startDist+variation) * math.cos(rad))
            self.asteroid.append((x,y))
        if fragment:
            while True:
                self.speed = (random.randint(-1,1), random.randint(-1,1))
                if self.speed != (0, 0):
                    break
            self.x, self.y = startPos
        else:
            self.speed, self.x, self.y = self.calculate_speed()
        self.draw()

    def calculate_speed(self):
        side = random.randint(0,3)
        if side == 0:
            return (1,random.randint(-1,1)), 10, random.randint(10,54)
        elif side == 1:
            return (random.randint(-1,1),1), random.randint(10,118), 10
        elif side == 2:
            return (-1,random.randint(-1,1)), 118, random.randint(10,54)
        elif side == 3:
            return (random.randint(-1,1),-1), random.randint(10,118), 54
            
    def update(self):
        if self.x <= 0 or self.x >= 128:
            return False
        if self.y <= 0 or self.y >= 64:
            return False
        self.draw()
        self.x += self.speed[0]
        self.y += self.speed[1]
        return True
    
    def draw(self):
        first = True
        for point in self.asteroid:
            x, y = point
            x += self.x
            y += self.y
            if not first:
                x1, y1 = lastPoint
                x2, y2 = x, y
                self.display.line(x1, y1, x2, y2, self.display.white)
            else:
                first = False
            lastPoint = x, y
        x1, y1 = lastPoint
        x2, y2 = self.asteroid[0][0] + self.x, self.asteroid[0][1] + self.y
        self.display.line(x1, y1, x2, y2, self.display.white)

    
    def checkColision(self, pos):
        if self.x + self.startDist > pos[0] and self.x - self.startDist < pos[0]:
            if self.y + self.startDist > pos[1] and self.y - self.startDist < pos[1]:
                return True
        else:
            return False
        
class Ship:
    def __init__(self, display):
        self.display = display
        self.ship = [ #(0,y1,x2,y2)
            (-4, 3, 4),
            (-4, -3, 4),
            (2, 3, 3),
            (2, -3, 3)]
    
    def update(self, angle):
        rad = angle*math.pi/180;
        for coord in self.ship:                
            x1 = -coord[0] * math.sin(rad) + 64
            y1 = coord[0] * math.cos(rad) + 32
            x2 = (coord[1] * math.cos(rad) - coord[2] * math.sin(rad)) + 64
            y2 = (coord[2] * math.cos(rad) + coord[1] * math.sin(rad)) + 32
            self.display.line(int(x1), int(y1), int(x2), int(y2), self.display.white)