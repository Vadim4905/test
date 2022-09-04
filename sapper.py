import os
from random import randint
import pygame
from time import time
pygame.init()
FPS = 40
clock = pygame.time.Clock()
window  = pygame.display.set_mode((600, 600))
window.fill((173,216,230))
pygame.display.set_caption('four in row')
class Label():
    def __init__(self,text,font_size,x,y,wieght,hieght,color):
        self.rect = pygame.Rect(x, y, wieght, hieght)
        self.font_size = font_size
        self.text = text
        self.color = color

    def draw_rect(self):
        pygame.draw.rect(window, self.color, self.rect)

    def draw_label(self,x_shift,y_shift):
        self.image = pygame.font.SysFont("verdana", self.font_size,).render(self.text, True, (0,0,0))
        window.blit(self.image, (self.rect.x+x_shift, self.rect.y+y_shift))

    def collidepoint(self, x,y):
        return self.rect.collidepoint(x,y)

class Menu():
    def __init__(self):
        self.label = Label('Выберите уровень сложности:',20,150,50,0,0,(0,0,0))
        self.btns =[Label('легко',20,200,120,200,70,(0,255,0))]
        self.btns.append(Label('нормально',20,200,320,200,70,(255,255,0)))
        self.btns.append(Label('сложно',20,200,500,200,70,(255,0,0)))

    def draw(self):
        [i.draw_rect() for i in self.btns]
        [i.draw_label(50,10) for i in self.btns]
        self.label.draw_label(0,0)

    def presed(self,x,y):
        for i in self.btns:
            if i.collidepoint(x,y):
                if i.text == 'легко':
                    return Game_map(10,10,15,40)
                elif i.text == 'нормально':
                    return Game_map(17,17,50,17)
                else:
                    return Game_map(25,25,100,15)
            else:
                False
class Block():
    def __init__(self,size,x,y,font_size,hide_color,show_color,flag,bomb):
        self.rect = pygame.Rect(x, y, size, size)
        self.name = '0'
        self.image = pygame.font.SysFont("verdana", font_size,).render(self.name, True, (0,0,0))
        self.hide_color = hide_color
        self.show_color = show_color
        self.font_size = font_size
        self.show = False
        self.draw_flag =False
        self.colors = [(0,0,255),(0,255,0),(255,0,0),(75, 0, 130),(255, 140, 0),(0, 191, 255),(255, 20, 147),(0, 0, 0)]
        self.flag = flag
        self.bomb = bomb
        

    def draw_rect(self):
        if self.show:
            self.color = self.show_color
        else:
            self.color = self.hide_color
        pygame.draw.rect(window, self.color, self.rect) 
        try:self.сolor = self.colors[int(self.name)-1]
        except : pass
        self.image = pygame.font.SysFont("verdana", self.font_size,).render(self.name, True, self.сolor)
        if self.show and self.name !=  '0' and self.name !=  'b':
            window.blit(self.image, (self.rect.x+5, self.rect.y))
        if not self.show and self.draw_flag:
            window.blit(self.flag, (self.rect.x, self.rect.y+5))
        if self.show and self.name == 'b':
            window.blit(self.bomb, (self.rect.x, self.rect.y))

    def collidepoint(self, x,y):
        return self.rect.collidepoint(x,y)

class Game_map():
    def __init__(self,row,col,bombs_am,font_size):
        self.bombs_am = bombs_am
        self.font_size = font_size
        self.matrix = []
        self.start_x = 50
        self.start_y = 50
        self.end_x = 550
        self.end_y = 550
        self.lost = False
        self.first_click = True
        self.block_size = min((self.end_x-self.start_x)//col, (self.end_y-self.start_y)//row)
        self.locations=[lambda i, j:(i,j-1),
                        lambda i, j:(i,j+1),
                        lambda i, j:(i-1,j),
                        lambda i, j:(i+1,j),
                        lambda i, j:(i-1,j-1),
                        lambda i, j:(i+1,j+1),
                        lambda i, j:(i+1,j-1),
                        lambda i, j:(i-1,j+1)]    

        filename = os.path.join(os.path.abspath(__file__+'/..'),'images','flag.png')
        flag = pygame.image.load(filename)
        flag.set_colorkey((255,255,255))
        flag = pygame.transform.scale(flag,(self.block_size-7,self.block_size-7))
        filename = os.path.join(os.path.abspath(__file__+'/..'),'images','bomb.png')
        bomb = pygame.image.load(filename)
        bomb.set_colorkey((255,255,255))
        bomb = pygame.transform.scale(bomb,(self.block_size,self.block_size))
           
        for i in range(row):
            l = []
            for j in range(col):
                if i%2 == j%2: # чтобы цвет сделать в шахмотном порядке мы проверяем четность координат
                    h_color,sh_color = (0,255,0),(192, 192, 192)
                else:
                    h_color,sh_color = (50,205,50),(220, 220, 220)
                x = (self.block_size*j)+self.start_x
                y = (self.block_size*i)+self.start_y
                block = Block(self.block_size,x,y,font_size,h_color,sh_color,flag,bomb)
                l.append(block)
            self.matrix.append(l)
        
    def draw_map(self):
        [ [j.draw_rect() for j in i] for i in self.matrix]
        pygame.display.update()

    def check_right_click(self,x,y):
        for i in self.matrix:
            for j in i:
                if j.collidepoint(x,y):
                    if not j.show:
                        if j.draw_flag:
                            j.draw_flag = False
                        else:   
                            j.draw_flag = True
                        j.draw_rect()
                        pygame.display.update()

    def get_nearest(self,i,j):
        nearest = []
        for f in self.locations:
            try:
                x,y = f(i,j)
                if x >= 0 and y >=0:
                    nearest.append(self.matrix[x][y])
            except IndexError:
                pass 
        return nearest

    def generate_map(self,i,j):
        while self.bombs_am > 0:
            for x in range(len(self.matrix)):
                for y in range(len(self.matrix[x])):
                    if randint(1,10) == 10 and self.matrix[x][y].name  == '0' and  not( (x,y)  in [f(i,j) for f in self.locations]+[(i,j)]):
                        if self.bombs_am <= 0:
                            break
                        self.matrix[x][y].name = 'b'
                        self.bombs_am -= 1
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j].name == '0':
                    bombs = 0
                    for place in self.get_nearest(i,j):
                        if place.name == 'b':
                            bombs +=1
                    self.matrix[i][j].name = str(bombs)

    def get_index(self,place):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if  self.matrix[i][j] == place:
                    return i,j 

    def open_bomb(self):
        for i in self.matrix:
            for j in i:
                if j.name == 'b':
                    delay(4)
                    j.show = True
                    j.draw_rect()
                    pygame.display.update()
        self.lost = True            
        
    def open(self,i,j):
        self.matrix[i][j].show = True
        self.matrix[i][j].draw_rect()
        if self.matrix[i][j].name == 'b':
            self.open_bomb()
        if self.matrix[i][j].name == '0':
            for place in self.get_nearest(i,j):
                if not place.show:
                    self.open(*self.get_index(place))

    def check_left_click(self,x,y):
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j].collidepoint(x,y):
                    if self.first_click:
                        self.generate_map(i,j)
                        self.first_click = False
                    self.open(i,j)

    def check_win(self):
        for i in self.matrix:
            for j in i:
                if not j.show  and j.name !='b':
                    return False
        return True

    def res_anim(self,name,color):
        window.fill((255,255,255))
        image = pygame.font.SysFont("verdana", 70).render(name, True, color)
        window.blit(image, (200, 200))
        delay(40)

def start_game(game_map):
    while True:
        window.fill((173,216,230))
        game_map.draw_map()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                game_map.check_right_click(*event.pos)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                game_map.check_left_click(*event.pos)
        if game_map.check_win():
            game_map.res_anim('You win',(0,255,0))
            print('you win')
            return
        if game_map.lost:
            game_map.res_anim('You lost',(255,0,0))
            print('you lost')
            return
        pygame.display.update()
        clock.tick(FPS)


def delay (ammaunt):
    while ammaunt != 0:
        ammaunt -= 1
        clock.tick(FPS)
        pygame.display.update()


def main():
    menu = Menu()
    while True:
        start =time()
        window.fill((173,216,230))
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                my_map = menu.presed(*event.pos)
                if my_map:
                    start_game(my_map)
        pygame.display.update()
        clock.tick(FPS)
main()