import sys

import pygame
from simulation import Simulation
import numpy as np






pygame.init()

clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

BG = (0, 0, 0)

screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption('Pygame Drone')

def draw_bg():
    screen.fill(BG)

class Player(pygame.sprite.Sprite):
    def __init__(self, image_path, width, height):
        super().__init__()

        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (0, 0, 0), ((0, 0), (width, 0), (width, height), (0, height)))
        self.original_image = self.image

        self.rect = self.image.get_rect(center = (0, 0))

    def update(self, pos_x, pos_y, angle):
        self.rect.move_ip(pos_x, pos_y)

        self.image = pygame.transform.rotate(self.original_image, angle * 180 / np.pi)
        self.rect = self.image.get_rect(center = self.rect.center)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


P = Player(f'images/drone/drone5.PNG', 50, 5)
S = Simulation()

pos_last_px = np.array([0, 0])

def interpolate(xa, x1, x2, y1, y2):
    return ((xa - x1) / (x2 - x1) * (y2 - y1)) + y1


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if not S.is_over():
        pos_abs_m, angle = S.iterate()

        x_abs_px = interpolate(pos_abs_m[0], -55, 20, 0, SCREEN_WIDTH)
        y_abs_px = interpolate(pos_abs_m[1], -0.5, 16, 0, SCREEN_HEIGHT)
        y_abs_px = SCREEN_HEIGHT - y_abs_px

        pos_abs_px = np.array([int(x_abs_px), int(y_abs_px)])
        pos_rel_px = pos_abs_px - pos_last_px
        pos_last_px = pos_abs_px

        P.update(pos_rel_px[0], pos_rel_px[1], angle)
    else:
        pygame.quit()
        sys.exit()

    P.draw(screen)

    pygame.display.update()
    clock.tick(60)