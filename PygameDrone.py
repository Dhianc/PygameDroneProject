import pygame
from control import Control
import numpy as np
import time


pygame.init()

# Definição da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Pygame Drone")
pygame.display.get_window_size()

#background
bg_image = pygame.image.load(f'images/BG.jpg')


#set framerate
clock = pygame.time.Clock()
FPS = 500
count = 0

start_time = time.time()


#define player action variables
esquerda = False
direita = False
cima = False
baixo = False
comandar = False



class Drone(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        # self.direction = 1
        # self.flip = False
        img = pygame.image.load(f'images/drone.png')
        tam = img.get_rect()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = img.get_rect()
        self.rect.center = (x, y)
        self.original_image = self.image

    def move(self, pos_x, pos_y, angle):
        self.rect.move_ip(pos_x, pos_y)

        self.image = pygame.transform.rotate(self.original_image, angle * 180 / np.pi)
        self.rect = self.image.get_rect(center = self.rect.center)


    # def move(self, esquerda, direita, cima, baixo):
    #     #reset movement variables
    #     dx = 0
    #     dy = 0
    #
    #     #assign movement variables if moving left or right
    #     if esquerda:
    #         dx = -self.speed
    #     if direita:
    #         dx = self.speed
    #     if cima:
    #         dy = -self.speed
    #     if baixo:
    #         dy = self.speed
    #
    #     #update rectangle position
    #     self.rect.x += dx
    #     self.rect.y += dy


    def draw(self):
        screen.blit(self.image, self.rect)



player = Drone('drone', 0, 0, 0.3, 1)


pos_last_px = np.array([0, 0])


def interpolate(xa, x1, x2, y1, y2):
    return ((xa - x1) / (x2 - x1) * (y2 - y1)) + y1



controlSystem = Control()


run = True
while run:
    
    clock.tick(FPS)

   
    screen.blit(bg_image, (0, 0))
    player.draw()

    temp = time.time() - start_time
    # print(temp)

    if temp >= 26:  #tempo total dos waypoints
        comandar = True

    for event in pygame.event.get():

        #quit game
        if event.type == pygame.QUIT:
            run = False

        #keyboard presses
        if comandar == True:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    esquerda = True
                if event.key == pygame.K_d:
                    direita = True
                if event.key == pygame.K_w:
                    cima = True
                if event.key == pygame.K_s:
                    baixo = True
                if event.key == pygame.K_ESCAPE:
                    run = False


            #keyboard button released
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    esquerda = False
                if event.key == pygame.K_d:
                    direita = False
                if event.key == pygame.K_w:
                    cima = False
                if event.key == pygame.K_s:
                    baixo = False


    # if not controlSystem.is_over():
    pos_abs_m, angle = controlSystem.movimenta(esquerda, direita, cima, baixo, comandar)
    x_abs_px = interpolate(pos_abs_m[0], -60, 25, 0, SCREEN_WIDTH)
    y_abs_px = interpolate(pos_abs_m[1], -2, 17, 0, SCREEN_HEIGHT)
    y_abs_px = SCREEN_HEIGHT - y_abs_px
            
    pos_abs_px = np.array([int(x_abs_px), int(y_abs_px)])
    pos_rel_px = pos_abs_px - pos_last_px
    pos_last_px = pos_abs_px

    player.move(pos_rel_px[0], pos_rel_px[1], angle)
        

    pygame.display.update()

pygame.quit()