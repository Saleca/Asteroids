from Asteroid import Asteroid
from Asteroid import AsteroidStats
from Bullet import Bullet
import math

class Collision:
    def __init__(self, asteroid, bullet):
        self.original_asteroid = asteroid
        self.bullet = bullet

    def create_fragments(self):
        fragments = []
        n_fragments = 2
        if self.original_asteroid.stats.size * .7 > Asteroid.MIN_SIZE:
            size = self.original_asteroid.stats.size * .7
            position = self.original_asteroid.stats.current_position
            #fix the angle and speed creation
            angle_diff = self.bullet.rad - self.original_asteroid.stats.rad
            speed = (self.original_asteroid.stats.speed + Bullet.SPEED / 2) * abs(math.cos(angle_diff))
            angles = [self.bullet.rad + i*(2*math.pi/n_fragments) + angle_diff for i in range(n_fragments)]
            
            for i in range(n_fragments):
                #move position with helpers next position by size/2
                stats = AsteroidStats(size, position, angles[i], speed)
                asteroid = Asteroid(self.original_asteroid.display, stats)
                fragments.append(asteroid)
        return fragments    