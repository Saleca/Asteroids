import random
import math
import Helpers
from Display import Display

class Asteroid:
    MIN_SIZE = 4
    MAX_SIZE = 15
    
    def __init__(self, display, stats):
        self.display = display
        self.stats = stats
        self.asteroid = []
        
        variation = int(self.stats.size*.3)
        full_circle = 2*math.pi
        arcLength = full_circle/self.stats.size #make sure there is no remaining
        for rad in Helpers.float_range(0, full_circle, arcLength):
            x = int((-self.stats.size + random.randint(-variation,variation)) * math.sin(rad))
            y = int((self.stats.size + random.randint(-variation,variation)) * math.cos(rad))
            self.asteroid.append((x,y))
            
        self.draw()
            
    def update(self):
        self.stats.distance += self.stats.speed
        x, y = Helpers.next_position(self.stats.distance, self.stats.rad, self.stats.start_position)
        if Helpers.outside_bounds(x, 0, Display.WIDTH) or \
        Helpers.outside_bounds(y, 0, Display.HEIGHT):
            return False
        self.stats.current_position = (x,y)
        self.draw()
        return True
    
    def draw(self):
        first = True
        for point in self.asteroid:
            x, y = point
            x += self.stats.current_position[0]
            y += self.stats.current_position[1]
            if not first:
                x1, y1 = lastPoint
                x2, y2 = x, y
                self.display.line(int(x1), int(y1), int(x2), int(y2), self.display.white)
            else:
                first = False
            lastPoint = x, y
        x1, y1 = lastPoint
        x2 = self.asteroid[0][0] + self.stats.current_position[0]
        y2 = self.asteroid[0][1] + self.stats.current_position[1]
        self.display.line(int(x1), int(y1), int(x2), int(y2), self.display.white)
    
    def check_collision(self, position):
        if self.stats.current_position[0] + self.stats.size > position[0] and self.stats.current_position[0] - self.stats.size < position[0]:
            if self.stats.current_position[1] + self.stats.size > position[1] and self.stats.current_position[1] - self.stats.size < position[1]:
                return True
        else:
            return False
        
class AsteroidStats:    
    def __init__(self, size, position, rad, speed):
        self.size = size
        self.start_position = position
        self.rad = rad
        self.speed = speed
        self.distance = size/2
        self.current_position = Helpers.next_position(self.distance, self.rad, position)
        
    @classmethod
    def init(cls, size):
        #get random position arround the edges
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            position = random.randint(0, Display.WIDTH), 0
        elif edge == 'bottom':
            position = random.randint(0, Display.WIDTH), Display.HEIGHT
        elif edge == 'left':
            position = 0, random.randint(0, Display.HEIGHT)
        else: # 'right'
            position = Display.WIDTH, random.randint(0, Display.HEIGHT)
        
        #get an angle for the direction
        direction_x = Display.HALF_WIDTH - position[0]
        direction_y = Display.HALF_HEIGHT - position[1]
        rad = math.atan2(direction_y, direction_x)
        half_pi = math.pi / 2
        rad += random.uniform(-half_pi, half_pi)
        
        #initialize the remaining variables
        speed = random.randint(1,2)
        
        return cls(size, position, rad, speed)