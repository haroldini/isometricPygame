import pygame as pg
import numpy.random as rnd

class World:

    def __init__(self, screen, camera):

        #default zoom settings
        self.TILESIZE = 64
        self.MAXZOOM = 4
        self.MINZOOM = 128
        self.zoomOffset = 0, 0

        #default world settings
        self.GRIDSIZE = [25, 25]
        self.grid = self.createGrid()

        #initialising features
        self.screen = screen
        self.camera = camera
        self.colors = {"colorBlack":"#262626", "colorWhite":"#e3e3e3"}
        self.tileTextures = self.initTerrainAssets()
        self.tileTexturesVar = self.tileTextures
        self.animations = self.loadAnimations()
        
        
        #default mouse states
        self.clickUp = False
        self.dragTime = 0
        
        
    def events(self, event):

        GRIDSIZE = self.GRIDSIZE
        mousePos = pg.mouse.get_pos()
        gridPosX, gridPosY = self.mouseToGrid(mousePos[0], mousePos[1])

        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.MD = pg.mouse.get_pos()
                gridPosX, gridPosY = self.mouseToGrid(self.MD[0], self.MD[1])
                
                if -GRIDSIZE[0] <= gridPosX < 0 and -GRIDSIZE[1] <= gridPosY < 0:
                    pass           #area within grid (cell) clicked
                else:
                    pass                        #area outside of grid clicked
        
        
                
        if event.type == pg.MOUSEMOTION:
            if self.camera.drag == True:
                self.dragTime += 1

        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if self.dragTime < 10:          #click is registered if dragtime is small
                    if -GRIDSIZE[0] <= gridPosX < 0 and -GRIDSIZE[1] <= gridPosY < 0:
                        self.clickUp = True
                    self.MU = pg.mouse.get_pos()
                self.dragTime = 0

        if event.type == pg.MOUSEBUTTONDOWN:    #zoom in
            if event.button == 4:
                if self.TILESIZE < self.screen.get_size()[0]/self.MAXZOOM:
                    self.zoomRender(4)

        if event.type == pg.MOUSEBUTTONDOWN:    #zoom out
            if event.button == 5:
                if self.TILESIZE > self.screen.get_size()[0]/self.MINZOOM:
                    self.zoomRender(5)


    def update(self, screen):
        self.screen = screen
        GRIDSIZE = self.GRIDSIZE

        #hover effect
        mousePos = pg.mouse.get_pos()
        gridPosX, gridPosY = self.mouseToGrid(mousePos[0], mousePos[1])

        #if mouse on cell
        if -GRIDSIZE[0] <= gridPosX < 0:
            if -GRIDSIZE[1] <= gridPosY <0:
                self.grid[gridPosX][gridPosY]["cellHover"] = True
                #update celltype on click
                if self.clickUp == True:
                    self.grid[gridPosX][gridPosY]["cellClick"] = True
                    if self.grid[gridPosX][gridPosY]["cellType"] != 1:
                        self.grid[gridPosX][gridPosY]["cellType"] = 1
                    elif self.grid[gridPosX][gridPosY]["cellType"] == 1:
                        self.grid[gridPosX][gridPosY]["cellType"] = 0
                self.clickUp = False
                
        

    def draw(self): 

        WIDTH, HEIGHT = self.screen.get_size()
        GRIDSIZE = self.GRIDSIZE
        cameraOffsetX, cameraOffsetY = self.camera.scroll
        
        #total offset for drawing objects
        self.DRAWtotalOffsetX = cameraOffsetX + WIDTH/2 - self.drawOffset[0] - self.zoomOffset[0]
        self.DRAWtotalOffsetY = cameraOffsetY + HEIGHT/2 - self.drawOffset[1] - self.zoomOffset[1]

        for y in range(GRIDSIZE[0]):                       
            for x in range(GRIDSIZE[1]):
                cell = self.grid[y][x]      

                #getting cell positition and cell poly position
                cellPoly = [(x + self.DRAWtotalOffsetX, y + self.DRAWtotalOffsetY) for x, y in cell["cellPoly"]] 
                cellPos = cell["cellPos"][0] + self.DRAWtotalOffsetX,  cell["cellPos"][1] + self.DRAWtotalOffsetY
                
                #checking texture
                cellType = cell["cellType"]
                if cellType == 0:           image = self.tileTextures["none"]
                elif cellType == 1:     
                    cellSE = self.grid[y+1][x]
                    cellS = self.grid[y+1][x+1]
                    cellN = self.grid[y-1][x-1]
                    cellNW = self.grid[y-1][x]
                    cellNE = self.grid[y][x-1]
                    cellSW = self.grid[y][x+1]
                    cellW = self.grid[y-1][x+1]
                    cellE = self.grid[y+1][x-1]
                    
                    image = self.tileTextures["cell_out"]

                    if cellNE["cellType"] != 0 or cellE["cellType"] != 0:
                        image = self.tileTextures["cell_right"]

                    if cellNW["cellType"] != 0 and (cellNE["cellType"] == 0 or cellE["cellType"] == 0) or \
                        (cellW["cellType"] != 0 and (cellNE["cellType"] == 0 or cellE["cellType"] == 0)):
                        image = self.tileTextures["cell_left"]

                    if ((cellE["cellType"] != 0 or cellNE["cellType"] != 0) and (cellW["cellType"] != 0 or \
                        cellNW["cellType"] != 0)) or ((cellW["cellType"] != 0 or cellNW["cellType"] != 0) and \
                        (cellE["cellType"] != 0 or cellNE["cellType"] != 0)):
                        image = self.tileTextures["cell_in"]


                        


                if cellType != 0:
                    image = pg.transform.scale(image, (self.TILESIZE*2, self.TILESIZE*2))

                #checking hover
                image.set_alpha(255)
                if cell["cellHover"] == True:   
                    image.set_alpha(200)
                
                #drawing the textures 
                self.screen.blit(image, (cellPos))

                #getting additional textures for cell:
                if cellType == 2:
                    image2 = self.tileTextures["rising_circles"]
                    image2 = pg.transform.scale(image2, (self.TILESIZE*2, self.TILESIZE*2))
                    self.screen.blit(image2, (cellPos[0], cellPos[1]-self.TILESIZE))


                #drawing the hovering polygon
                if cell["cellHover"] == True:
                    pg.draw.polygon(self.screen, self.colors["colorWhite"], cellPoly, 4)
                cell["cellHover"] = False
                
        
        

    def createGrid(self):

        TILESIZE = self.TILESIZE
        GRIDSIZE = self.GRIDSIZE
        grid = []                               # grid dictionary                           
        
        for x in range(GRIDSIZE[0]):
            grid.append([])
            for y in range(GRIDSIZE[1]):

                #calculating cell dict values
                cellCoords = x,y                                                # grid coordinates
                cellType = 0                 #rnd.randint(2, size=1)[0]                            # terrain type / insert get_terrain_type function here later
                cellRect = [(x * TILESIZE, y * TILESIZE),
                            (x * TILESIZE + TILESIZE, y * TILESIZE),
                            (x * TILESIZE + TILESIZE, y * TILESIZE + TILESIZE),
                            (x * TILESIZE, y * TILESIZE + TILESIZE)]
                
                cellPoly = [self.cartToIso(x, y) for x, y in cellRect]       
                cellPosX = min([x for x, y in cellPoly])
                cellPosY = min([y for x, y in cellPoly])
                cellPos = [cellPosX, cellPosY]
                
                #generating cell dictionary
                cell = {}
                cell = {"cellCoords":cellCoords, "cellType":cellType, "cellRect":cellRect, 
                        "cellPoly":cellPoly, "cellPos":cellPos ,"cellHover": False, "cellClick": False, "frame":0}
                grid[x].append(cell)

        return grid


    def zoomRender(self, direction):

        TILESIZE = self.TILESIZE
        GRIDSIZE = self.GRIDSIZE
        MZoom = pg.mouse.get_pos()           

        #cellPos before zoom
        x, y = self.mouseToGrid(MZoom[0], MZoom[1])
        x, y = x+1, y   
        cellPos1 = self.simZoom(self.MTGtotalOffsetX, self.MTGtotalOffsetY, x, y, TILESIZE)

        #applying zoom factor
        if direction == 4:
            self.TILESIZE *= 5/4
        elif direction == 5:
            self.TILESIZE *= 4/5
        TILESIZE = self.TILESIZE
        self.drawOffset = (GRIDSIZE[0] - GRIDSIZE[1])*TILESIZE/2,\
                          (GRIDSIZE[0] + GRIDSIZE[1])*TILESIZE/4 

        #cellPos after zoom
        hypotheticalOffsetX=self.camera.scroll[0] + self.screen.get_size()[0]/2 + self.drawOffset[0]
        hypotheticalOffsetY=self.camera.scroll[1] + self.screen.get_size()[1]/2 + self.drawOffset[1]
        cellPos2 = self.simZoom(hypotheticalOffsetX, hypotheticalOffsetY, x, y, TILESIZE)

        #finding difference between before and after
        dPosX = cellPos2[0] - cellPos1[0]
        dPosY = cellPos2[1] - cellPos1[1]
        self.zoomOffset = dPosX + self.zoomOffset[0], dPosY + self.zoomOffset[1]

        #apply new tilesize to cell dict
        for x in range(GRIDSIZE[0]):
            for y in range(GRIDSIZE[1]):
                cell = self.grid[x][y]
                cellRect = [
                    (x * TILESIZE, y * TILESIZE),
                    (x * TILESIZE + TILESIZE, y * TILESIZE),
                    (x * TILESIZE + TILESIZE, y * TILESIZE + TILESIZE),
                    (x * TILESIZE, y * TILESIZE + TILESIZE)
                ]
                cellPoly = [self.cartToIso(x, y) for x, y in cellRect]       
                cellPosX = min([x for x, y in cellPoly])
                cellPosY = min([y for x, y in cellPoly])
                cellPos = [cellPosX, cellPosY]

                cell["cellRect"], cell["cellPoly"], cell["cellPos"] = cellRect, cellPoly, cellPos


    def simZoom(self, offsetX, offsetY, x, y, TILESIZE):   

        cellRect1 = [(x * TILESIZE, y * TILESIZE),
                     (x * TILESIZE + TILESIZE, y * TILESIZE),
                     (x * TILESIZE + TILESIZE, y * TILESIZE + TILESIZE),
                     (x * TILESIZE, y * TILESIZE + TILESIZE)]
            
        cellPoly1 = [self.cartToIso(x, y) for x, y in cellRect1]       
        cellPosX1 = min([x for x, y in cellPoly1])
        cellPosY1 = min([y for x, y in cellPoly1])

        return [cellPosX1+offsetX, cellPosY1+offsetY]       #self.MTGtotalOffsetY


    def cartToIso(self, x, y):
        isoX = x - y
        isoY = (x + y) / 2
        return isoX, isoY


    def mouseToGrid(self, x, y):

        TILESIZE = self.TILESIZE
        GRIDSIZE = self.GRIDSIZE
        
        #calculating offset
        self.drawOffset = (GRIDSIZE[0] - GRIDSIZE[1])*TILESIZE/2,\
                          (GRIDSIZE[0] + GRIDSIZE[1])*TILESIZE/4
        self.MTGtotalOffsetX = self.camera.scroll[0] + self.screen.get_size()[0]/2 + self.drawOffset[0]
        self.MTGtotalOffsetY = self.camera.scroll[1] + self.screen.get_size()[1]/2 + self.drawOffset[1]

        #transform to world position (remove camera scroll and offset)
        worldX = x - self.MTGtotalOffsetX + self.zoomOffset[0]
        worldY = y - self.MTGtotalOffsetY + self.zoomOffset[1]
        #transform to cart (inverse of cart to iso)
        cartY = (2*worldY - worldX)/2
        cartX = cartY + worldX
        #transform to grid coordinates
        gridX = int(cartX // TILESIZE)
        gridY = int(cartY // TILESIZE)

        return gridX, gridY


    def initTerrainAssets(self):
        TILESIZE = self.TILESIZE
        none = pg.image.load('assets/cellNone.png').convert_alpha()

        cell_in = pg.image.load('assets/cell/cell_in.png').convert_alpha()
        cell_out = pg.image.load('assets/cell/cell_out.png').convert_alpha()
        cell_left = pg.image.load('assets/cell/cell_left.png').convert_alpha()
        cell_right = pg.image.load('assets/cell/cell_right.png').convert_alpha()

        none = pg.transform.scale(none, (TILESIZE*2, TILESIZE*2))
        cell_in = pg.transform.scale(cell_in, (TILESIZE*2, TILESIZE*2))
        cell_out = pg.transform.scale(cell_out, (TILESIZE*2, TILESIZE*2))
        cell_left = pg.transform.scale(cell_left, (TILESIZE*2, TILESIZE*2))
        cell_right = pg.transform.scale(cell_right, (TILESIZE*2, TILESIZE*2))

        return {"none":none, "cell_in":cell_in, "cell_out":cell_out, "cell_left":cell_left, "cell_right":cell_right}
    
        
    def changeAnimation(self, actionVar, frame, newValue):
        if actionVar != newValue:
            actionVar = newValue
            frame = 0
        
        return actionVar, frame


    def loadAnimations(self):
        
        animationDatabase = {}
        # animationDatabase["triangle_replicator"] = self.loadAnimation('assets/triangle_replicator', [4, 4, 4, 4, 4])

        return animationDatabase


    def loadAnimation(self, path, frameDurations):
        self.animationFrames = {}
        animationName = path.split("/")[-1]
        animationFrameData = []
        n = 0

        for frame in frameDurations:
            animationFrameID = animationName + "_" + str(n)
            imgLoc = path + "/" + animationFrameID + ".png"
            animationImage = pg.image.load(imgLoc).convert_alpha()
            self.animationFrames[animationFrameID] = animationImage.copy()
            for i in range(frame):
                animationFrameData.append(animationFrameID)
            n += 1

        return animationFrameData

    


