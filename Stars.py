import random

class Stars:
    def __init__(self, display):
        self.display = display
        self.stars = []
        for x in range(30):
            self.stars.append((random.randint(0,128), random.randint(0,64)))
            
    def update(self):
        for star in self.stars:
            self.display.pixel(star[0],star[1], self.display.white)
