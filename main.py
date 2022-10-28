import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Asteroids")
icon = pygame.image.load('Asteroid Brown.png')
pygame.display.set_icon(icon)

player_image = pygame.image.load('ship.png')
playerX = 640
playerY = 360

def player():
    screen.blit(player_image, (playerX, playerY))

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    screen.fill((0, 0, 0))
    player()

    pygame.display.update()
