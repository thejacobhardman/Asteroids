import pygame, random

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Asteroids")
icon = pygame.image.load('Asteroid Brown.png')
pygame.display.set_icon(icon)

player_image = pygame.image.load('ship.png')
playerX = 640
playerY = 360
playerX_change = 0
playerY_change = 0

def player(x, y):
    screen.blit(player_image, (x, y))

class asteroid:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 80
        self.image = pygame.image.load('Asteroid Brown.png')
        self.x_change = 0
        self.y_change = 0

    def asteroid(self):
        screen.blit(self.image, (self.x, self.y))

    # def update_location(self):


asteroid_count = 0
game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -0.3
            if event.key == pygame.K_DOWN:
                playerY_change = 0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                playerX_change = 0

    screen.fill((0, 0, 0))

    playerX += playerX_change
    playerY += playerY_change
    if playerX <= 0:
        playerX = 1235
    if playerX > 1235:
        playerX = 0
    if playerY < 0:
        playerY = 689
    if playerY > 689:
        playerY = 0

    player(playerX, playerY)

    pygame.display.update()
