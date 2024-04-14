from machine import Pin,SPI
import Asteroids
import Display
import random
import math
import time
import gc

class Game:
    def __init__(self):
        self.s = Display.Screen()
        self.offTimer = 15
        self.warning = 5
        self.key0 = Pin(15, Pin.IN, Pin.PULL_UP)
        self.key1 = Pin(17, Pin.IN, Pin.PULL_UP)
        self.hc = int(self.s.width/2)
        self.vc = int(self.s.height/2)
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
        self.s.fill(self.s.black)
        self.s.show()
        self.s.center("Asteroids", 16, self.s.white )
        time.sleep(.1)
        self.s.center("Ready?", 32, self.s.white )

        while(self.anyKey):
            if self.key0.value() == 0 or self.key1.value() == 0:
                self.s.fill(self.s.black)
                self.s.show()
                self.anyKey = False

        stars = Asteroids.Stars(self.s)
        ship = Asteroids.Ship(self.s)

        while(self.isContinue):
            self.s.fill(self.s.black)
            stars.update()
            self.check_input()
            self.angle += self.direction
            ship.update(self.angle)
            self.update_bullets()
            self.update_asteroids()
            self.check_collisions()
            self.s.show()
            if self.quitCount:
                self.quitTimer = self.offTimer
                if self.wasOff:
                    self.wasOff = False
            self.quitCount = True
            gc.collect()

    def check_input(self):
        if self.key0.value() == 0 and self.key1.value() == 0:
            if not self.firedLastFrame:
                self.bullets.append(Asteroids.Bullet(self.angle, self.s))
                self.firedLastFrame = True
            else:
                self.firedLastFrame = False
            self.quitTimer-=1
            self.quitCount = False
            if self.quitTimer <= self.warning:
                self.s.fill_rect(0,22,128,20,self.s.white)
                self.s.center("Powering off", 27, self.s.black)
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
            self.asteroids.append(Asteroids.Asteroid(self.s, 6))
        for a in self.asteroids:
            if not a.update():
                self.asteroids.remove(a)

    def check_collisions(self):
        hits = []
        for b in list(self.bullets):
            for a in list(self.asteroids):
                if b.hit:
                    continue
                if a.checkColision(b.pos):
                    b.hit = True
                    self.asteroids.remove(a)
                    self.bullets.remove(b)
                    for i in range(2):
                        self.asteroids.append(Asteroids.Asteroid(self.s, 4, True, b.pos))            

if __name__=='__main__':
    game = Game()
    game.run()
