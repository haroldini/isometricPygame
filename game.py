import pygame as pg
import time
from sys import exit
from camera import Camera
from world import World
from utils import drawText, guiEvents



class Game:

    def __init__(self, clock, screen, monitor):
        self.clock = clock
        self.screen = screen
        self.width, self.height = self.screen.get_size()
        self.monitorSize = monitor
        self.fullscreen = False
        self.camera = Camera()
        self.world = World(self.screen, self.camera)
        self.f3 = False

        #self.entities = Entities(screen)
        

        #game settings
        self.FPS = 60
        self.lastTime = time.time()


    def run(self):

        self.playing = True
        while self.playing:
            self.clock.tick(self.FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):

        for event in pg.event.get():
            guiEvents(self, event)

            self.camera.update(event)
            self.world.events(event)
            
            
    def update(self):

        self.dt = time.time() - self.lastTime
        self.dt *= 60
        self.lastTime = time.time()


        self.world.update(self.screen)

        #self.entities.update(self.dt)
        

    def draw(self):
        self.world.draw()
        #self.entities.draw()

        if self.f3:
            drawText(
                self.screen,
                "fps = {}".format(round(self.clock.get_fps())),
                25, (255, 255, 255), (10, 10)
            )
        pg.display.update()
        self.screen.fill(self.world.colors["colorBlack"])
        
