import math

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