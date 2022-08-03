import pygame as pg
from game import Game

def main():

    running = True
    playing = True

    pg.init()
    pg.mixer.init()

    monitorSize = [pg.display.Info().current_w, pg.display.Info().current_h]
    screen = pg.display.set_mode((1000,700), pg.RESIZABLE)
    clock = pg.time.Clock()

    game = Game(clock, screen, monitorSize)
    
    while running:

        #menu.run()
            
        while playing:

            # game loop
            game.run()



if __name__ == "__main__":
    main()