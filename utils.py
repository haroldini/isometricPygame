import pygame as pg


def drawText(screen, text, size, color, pos):

    font = pg.font.SysFont(None, size)
    textSurface = font.render(text, True, color)
    textRect = textSurface.get_rect(topleft = pos)
    screen.blit(textSurface, textRect)


def guiEvents(self, event):

    if event.type==pg.QUIT:
        pg.quit()
        exit()
    if event.type==pg.KEYDOWN:
        if event.key==pg.K_ESCAPE:
            pg.quit()
            exit()
        
    if event.type==pg.KEYDOWN:        
        if event.key==pg.K_F11:
            self.fullscreen = not self.fullscreen
            if self.fullscreen:
                self.screen = pg.display.set_mode(self.monitorSize, pg.FULLSCREEN)
                print("fullscreened")
            else:
                self.screen = pg.display.set_mode((1000,700), pg.RESIZABLE)
                print("unfullscreened")

    elif event.type == pg.VIDEORESIZE and self.fullscreen == False:
        self.screen = pg.display.set_mode((event.w, event.h), pg.RESIZABLE)


    if event.type==pg.KEYDOWN:
        if event.key == pg.K_F3:
            self.f3 = not self.f3

    if event.type==pg.KEYDOWN:
        if event.key == pg.K_e:
            if self.FPS ==120:
                self.FPS = 10
            else:
                self.FPS = 120