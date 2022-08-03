import pygame as pg

class Camera:

    def __init__(self):
        self.scroll = pg.Vector2(0, 0)
        self.scrollSpeed = 25
        self.drag = False
    

    def update(self, event):

        if event.type == pg.MOUSEBUTTONDOWN:        
            if event.button == 1:
                self.MR=None
                self.MD = pg.mouse.get_pos()        #mouse down position
                self.drag = True                    #permits dragging mouse motion event below
 
        if event.type==pg.MOUSEMOTION:
            if self.drag == True:
                self.MR = event.rel                 #gets mouse position relative to mouse down position // start of scrolling
                self.scroll.x += self.MR[0]         #update scroll x
                self.scroll.y += self.MR[1]         #update scroll y
        
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                self.drag = False                   #prevents dragging mouse motion event