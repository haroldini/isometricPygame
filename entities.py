import pygame as pg
import numpy.random as rnd
import random


class Entities:
    def __init__(self, screen):
        self.screen = screen
        self.pos = 0
        self.direction = "right"
        self.particles = []
        pass

    def update(self, dt):
        self.particles.append([[250, 250], [random.randint(0, 20) / 10 - 1, 5], random.randint(2, 4)])
        self.dt = dt

        if self.pos > self.screen.get_size()[0]-100:
            self.direction = "left"
        elif self.pos < 0:
            self.direction = "right"
        
        if self.direction == "right":
            self.pos += 3*dt
        else:
            self.pos -= 3*dt

        self.r=pg.Rect(self.pos, 200, 100, 100)


    def draw(self):

        for particle in self.particles:
            particle[0][0] += particle[1][0]
            particle[0][1] += particle[1][1]
            particle[2] -= 0.01
            particle[1][1] -= 0.05
            pg.draw.circle(self.screen, (255,255,255), particle[0], particle[2])
            if particle[2] <= 0:
                self.particles.remove(particle)

        pg.draw.rect(self.screen, (255, 255, 255), self.r)
        

