import pygame
from random import choice
from sys import exit

run = True
clock = pygame.time.Clock()

class window():
    def __init__(self, width, height, title):
        self.count = 0
        self.width = width
        self.height = height
        self.title = title
        self.door_rects = []
        self.select = False
        self.luck = choice([1,2,3])
        self.show = False
        self.door1 = 'closed'
        self.door2 = 'closed'
        self.door3 = 'closed'

        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        self.font = pygame.font.Font('files/Pixeltype.ttf',45)
        selected = pygame.image.load('files/door_selected.png').convert_alpha()
        closed = pygame.image.load('files/door_closed.png').convert_alpha()
        empty = pygame.image.load('files/door_opened_empty.png').convert_alpha()
        item = pygame.image.load('files/door_opened_item.png').convert_alpha()
        self.yes = pygame.image.load('files/yes.png').convert_alpha()
        self.no = pygame.image.load('files/no.png').convert_alpha()

        self.images = [closed,selected,empty,item]
        count = 0
        for image in self.images:
            scale = 0.5
            width = image.get_width()
            height = image.get_height()
            self.images[count] = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
            count+=1
        door1 = self.images[0]
        door2 = self.images[0]
        door3 = self.images[0]
        self.doors = [door1,door2,door3]
        
        for door in self.doors:
            self.door_rects.append(door.get_rect())
        self.door_rects[0].topleft = ((0-10,0+10))
        self.door_rects[1].topleft = ((200-10,0+10))
        self.door_rects[2].topleft = ((400-10,0+10))
        self.screen.fill((148,188,233))
        self.draw()

    def screen(self):
        return self.screen

    def draw(self,doors=['closed','closed','closed'],text="Select a door",buttons=False):
        count = 0
        count2 = 0
        self.screen.fill((148,188,233))
        for door in doors:
            if door == 'closed': self.doors[count2] = self.images[0]
            elif door == 'selected': self.doors[count2] = self.images[1]
            elif door == 'empty': self.doors[count2] = self.images[2]
            else: self.doors[count2] = self.images[3]
            count2+=1

        for door in self.doors:
            self.screen.blit(door,(self.door_rects[count].x,self.door_rects[count].y))
            count+=1
        self.draw_text(text)
        if buttons:
            self.draw_buttons()      

        pygame.display.update()

    def draw_text(self,thing):
        text = self.font.render(thing,False,(0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (int(self.width*1/2),int(self.height*3/5))
        self.screen.blit(text,(text_rect.x,text_rect.y))

    def draw_buttons(self):
        self.yes = pygame.transform.scale(self.yes,(int(150*0.7),int(100*0.7)))
        self.no = pygame.transform.scale(self.no,(int(150*0.7),int(100*0.7)))
        yes = self.yes.get_rect()
        yes.center = (int(self.width*4/10),int(self.height*4/6)+45)
        no = self.no.get_rect()
        no.center = (int(self.width*6/10),int(self.height*4/6)+45)
        self.screen.blit(self.yes,(yes.x,yes.y))
        self.screen.blit(self.no,(no.x,no.y))
        self.clicked = False
        pos = pygame.mouse.get_pos()
        if not self.clicked:
            if yes.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.clicked = True
                    self.swicth = True
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

            elif no.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1:
                    self.clicked = True
                    self.swicth = False
                if pygame.mouse.get_pressed()[0] == 0:
                    self.clicked = False

    def check_click(self):
        self.action = False
        clicked = False
        pos = pygame.mouse.get_pos()
        count = 0
        for rect in self.door_rects:
            if count == 3: count = 0
            count+=1
            if rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0] == 1 and not clicked:
                    clicked = True
                    self.action = True                 
                    return count
                if pygame.mouse.get_pressed()[0] == 0:
                    clicked = False               

    def game(self):
        check = self.check_click()
        if check == None:
            check = 0
        if check == 1 and self.select == False:
            self.door1 = 'selected'            
            self.select = True
            self.sel = 1
        elif check == 2 and self.select == False:
            self.door2 = 'selected'
            self.select = True
            self.sel = 2
        elif check == 3 and self.select == False:
            self.door3 = 'selected'
            self.select = True
            self.sel = 3
        
        if self.select and not self.show and check != 0:
            self.show2 = 0
            if self.luck != 1 and self.sel != 1:
                self.door1 = 'empty'
                self.show = True
                self.show2 = 1 
            elif self.luck != 2 and self.sel != 2:
                self.door2 = 'empty'
                self.show = True
                self.show2 = 2
            elif self.luck != 3 and self.sel != 3:
                self.door3 = 'empty'
                self.show = True
                self.show2 = 3
            self.draw([self.door1,self.door2,self.door3],"Swicth?",True)
        if self.show:
            if not self.clicked:
                self.draw([self.door1,self.door2,self.door3],"Swicth?",True)
            if self.clicked:
                self.end = False
                if self.swicth and not self.end:
                    if self.sel == 1: self.door1 = 'closed'
                    elif self.sel == 2: self.door2 = 'closed'
                    elif self.sel == 3: self.door3 = 'closed'
                    if self.show2 != 1 and self.sel != 1:
                        self.door1 = 'selected'
                        self.sel = 1
                    elif self.show2 != 2 and self.sel != 2:
                        self.door2 = 'selected'
                        self.sel = 2
                    elif self.show2 != 3 and self.sel != 3:
                        self.door3 = 'selected'
                        self.sel = 3
                    
                    self.draw([self.door1,self.door2,self.door3],"Swicthed",False)
                    self.swicth = False
                elif not self.swicth and self.end:
                    self.draw([self.door1,self.door2,self.door3],"Not swicthed",False)

                if self.sel or self.show2 != 1:
                    self.door1 = 'item'
                elif self.sel or self.show2 != 2:
                    self.door2 = 'item'
                elif self.sel or self.show2 != 3:
                    self.door3 = 'item'

                self.end = True
                if self.end == True:
                    if self.sel == self.luck:
                        self.draw([self.door1,self.door2,self.door3],"Winner",False)
                    else:
                        self.draw([self.door1,self.door2,self.door3],"Loser",False)

window_1 = window(600,400,"Three Doors Paradox")
while run:   
    window_1.game()
    events = pygame.event.get()
    for event in events:
        if(event.type == pygame.QUIT):
            run = False
    clock.tick(30)
pygame.quit()
exit()