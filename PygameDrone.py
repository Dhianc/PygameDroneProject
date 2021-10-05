import pygame
from controler import Controler
import numpy as np
import time


pygame.init()

# Tamanho da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 640

#Definindo janela
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
pygame.display.set_caption("Pygame Drone")
pygame.display.get_window_size()

#Definindo imagem de fundo
bg_image = pygame.image.load(f'images/BG.jpg')


#Configurando a taxa de atualização do jogo
clock = pygame.time.Clock()
FPS = 500
count = 0

start_time = time.time()


#Iniciando variáveis de ação como "false"
esquerda = False
direita = False
cima = False
baixo = False
comandar = False


#Declaração da classe "drone"
class Drone(pygame.sprite.Sprite):
    # Caracteristicas do drone
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

    # Função que atualiza a posição do drone na tela
    def move(self, pos_x, pos_y, angle):
        self.rect.move_ip(pos_x, pos_y)

        self.image = pygame.transform.rotate(self.original_image, angle * 180 / np.pi)
        self.rect = self.image.get_rect(center = self.rect.center)

    # Função que desenha o drone na tela
    def draw(self):
        screen.blit(self.image, self.rect)


#Declara um "drone" de nome "player"
player = Drone('drone', 0, 0, 0.3, 1)

#Define uma posição inicial
pos_ant = np.array([0, 0])

#Função que converte a entrada 'xa' do range x1~x2 para o range y1~y2
def interpolate(xa, x1, x2, y1, y2):
    return ((xa - x1) / (x2 - x1) * (y2 - y1)) + y1


controlSystem = Controler()

#Inicia a variável de controle que dita se o ciclo de execução deve continuar
run = True
while run:

    # Controle de fluidez
    clock.tick(FPS)

    # Atualização temporal para uso no timer
    temp = time.time() - start_time
    # print(temp)

    # Secção que libera o drone para pilotagem manual após ele ter percorrido os waypoints
    if temp >= 30:
        comandar = True

    # Loop que se inicia quando um evento (ação) é detectado
    for event in pygame.event.get():

        #Sai do jogo
        if event.type == pygame.QUIT:
            run = False

        #Define a ação quando teclas do teclado forem pressionadas
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


            #Atualiza o status das variáveis "esquerda, direita, cima ..." para false, quando o botão pressionado for solto
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    esquerda = False
                if event.key == pygame.K_d:
                    direita = False
                if event.key == pygame.K_w:
                    cima = False
                if event.key == pygame.K_s:
                    baixo = False

    # Define a posição do drone, baseado numa lei de controle
    pos, angle = controlSystem.movimenta(esquerda, direita, cima, baixo, comandar)

    # Usa a função de interpolação pra posicionar o drone no esquema de coordenadas cartesiano
    x = interpolate(pos[0], -60, 25, 0, SCREEN_WIDTH)
    y = interpolate(pos[1], -2, 17, 0, SCREEN_HEIGHT)
    y = SCREEN_HEIGHT - y
            
    pos = np.array([int(x), int(y)])
    pos_rel = pos - pos_ant
    pos_ant = pos

    # Atualiza o desenho do drone na tela
    player.move(pos_rel[0], pos_rel[1], angle)

    # Atualização das imagems de fundo e do drone
    screen.blit(bg_image, (0, 0))
    player.draw()

    # Atualiza a tela
    pygame.display.update()

pygame.quit()