from machine import Pin,SPI
from Asteroid import Asteroid
from Asteroid import AsteroidStats
from Stars import Stars
from Bullet import Bullet
from Ship import Ship
from Collision import Collision
from Display import Display
import random
import time

class Game:
    def __init__(self):
        self.display = Display()
        self.offTimer = 15
        self.warning = 5
        self.key0 = Pin(15, Pin.IN, Pin.PULL_UP)
        self.key1 = Pin(17, Pin.IN, Pin.PULL_UP)
        self.hc = int(self.display.HALF_WIDTH)
        self.vc = int(self.display.HALF_HEIGHT)
        self.rotSpeed = 10
        self.isContinue = True
        self.anyKey = True
        self.wasOff = False
        self.quitTimer = self.offTimer
        self.angle = 0
        self.direction = 0
        self.bullets = []
        self.asteroids = []
        self.quitCount = False
        self.firedLastFrame = False

    def run(self):
        self.display.fill(self.display.black)
        self.display.show()
        self.display.center("Asteroids", 16, self.display.white )
        time.sleep(.1)
        self.display.center("Ready?", 32, self.display.white )

        while(self.anyKey):
            if self.key0.value() == 0 or self.key1.value() == 0:
                self.display.fill(self.display.black)
                self.display.show()
                self.anyKey = False

        stars = Stars(self.display)
        ship = Ship(self.display)

        while(self.isContinue):
            self.display.fill(self.display.black)
            stars.update()
            self.check_input()
            self.angle += self.direction
            ship.update(self.angle)
            self.update_bullets()
            self.update_asteroids()
            self.check_collisions()
            self.display.show()
            if self.quitCount:
                self.quitTimer = self.offTimer
                if self.wasOff:
                    self.wasOff = False
            self.quitCount = True

    def check_input(self):
        if self.key0.value() == 0 and self.key1.value() == 0:
            if not self.firedLastFrame:
                self.bullets.append(Bullet(self.angle, self.display))
                self.firedLastFrame = True
            else:
                self.firedLastFrame = False
            self.quitTimer-=1
            self.quitCount = False
            if self.quitTimer <= self.warning:
                self.display.fill_rect(0,22,128,20,self.display.white)
                self.display.center("Powering off", 27, self.display.black)
                self.wasOff = True
                if self.quitTimer <= 0:
                    self.isContinue = False   
        elif self.key0.value() == 0:
            self.direction = -self.rotSpeed
        elif self.key1.value() == 0:
            self.direction = self.rotSpeed   
        elif self.key0.value() == 1 and self.key1.value() == 1:
            self.direction = 0

    def update_bullets(self):
        for b in self.bullets:
            if not b.update():
                self.bullets.remove(b)

    def update_asteroids(self):
        if len(self.asteroids) < 4:
            self.asteroids.append(Asteroid(self.display, AsteroidStats.init(random.randint(6, Asteroid.MAX_SIZE))))
        for a in self.asteroids:
            if not a.update():
                self.asteroids.remove(a)

    def check_collisions(self):
        hits = []
        for b in list(self.bullets):
            for a in list(self.asteroids):
                if b.hit:
                    continue
                if a.check_collision(b.position):
                    b.hit = True
                    self.asteroids.remove(a)
                    self.bullets.remove(b)
                    self.asteroids.extend(Collision(a, b).create_fragments())

if __name__=='__main__':
    game = Game()
    game.run()
