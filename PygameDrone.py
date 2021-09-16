import pygame
from control import Control
import numpy as np


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Pygame Drone")
pygame.display.get_window_size()
bg_image = pygame.image.load(f'images/ceu.jpg')

# fonte = pygame.font.SysFont('arial', 20, False, False)

#set framerate
clock = pygame.time.Clock()
FPS = 500


#define player action variables
moving_weast = False
moving_east = False
moving_north = False
moving_south = False

#define colours
BG = (0, 0, 0)




# def draw_bg():
#     screen.fill(BG)
#     # pygame.draw.circle(screen, (255, 0, 0), (400, 320), 60, 2)
#     # pygame.draw.line(screen, (255, 0, 0), (0, 0), (800, 640))
#     # pygame.draw.line(screen, (255, 0, 0), (800, 0), (0, 640))

class Drone(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.char_type = char_type
        self.speed = speed
        # self.direction = 1
        # self.flip = False
        img = pygame.image.load(f'images/{self.char_type}/drone6.png')
        tam = img.get_rect()
        self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
        self.rect = img.get_rect()
        self.rect.center = (x, y)
        self.original_image = self.image
        # print(tam)

    def update(self, pos_x, pos_y, angle):
        self.rect.move_ip(pos_x, pos_y)

        self.image = pygame.transform.rotate(self.original_image, angle * 180 / np.pi)
        self.rect = self.image.get_rect(center = self.rect.center)


    def move(self, moving_weast, moving_east, moving_north, moving_south):
        #reset movement variables
        dx = 0
        dy = 0

        #assign movement variables if moving left or right
        if moving_weast:
            dx = -self.speed
        if moving_east:
            dx = self.speed
        if moving_north:
            dy = -self.speed
        if moving_south:
            dy = self.speed

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy


    def draw(self):
        screen.blit(self.image, self.rect)



player = Drone('drone', 0, 0, 0.2, 1)
controlSystem = Control()

pos_last_px = np.array([0, 0])


def interpolate(xa, x1, x2, y1, y2):
    return ((xa - x1) / (x2 - x1) * (y2 - y1)) + y1


run = True
while run:
    clock.tick(FPS)

    # draw_bg()

    screen.blit(bg_image, (0, 0))
    player.draw()
    player.move(moving_weast, moving_east, moving_north, moving_south)

    # mensagem = f'Posição: {screen.get_rect()}'
    # texto = fonte.render(mensagem, True, (255, 255, 255))

    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False

        #keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_weast = True
            if event.key == pygame.K_RIGHT:
                moving_east = True
            if event.key == pygame.K_UP:
                moving_north = True
            if event.key == pygame.K_DOWN:
                moving_south = True
            if event.key == pygame.K_ESCAPE:
                run = False

        #keyboard button released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_weast = False
            if event.key == pygame.K_RIGHT:
                moving_east = False
            if event.key == pygame.K_UP:
                moving_north = False
            if event.key == pygame.K_DOWN:
                moving_south = False

    if not controlSystem.is_over():
        pos_abs_m, angle = controlSystem.iterate()

        x_abs_px = interpolate(pos_abs_m[0], -60, 25, 0, SCREEN_WIDTH)
        y_abs_px = interpolate(pos_abs_m[1], -2, 17, 0, SCREEN_HEIGHT)
        y_abs_px = SCREEN_HEIGHT - y_abs_px

        pos_abs_px = np.array([int(x_abs_px), int(y_abs_px)])
        pos_rel_px = pos_abs_px - pos_last_px
        pos_last_px = pos_abs_px

        player.update(pos_rel_px[0], pos_rel_px[1], angle)


    # screen.blit(texto, (0, 0))
    pygame.display.update()

pygame.quit()