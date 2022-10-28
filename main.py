import pygame

pygame.init()

screen = pygame.display.set_mode((1280, 720))

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.quit():
            game_running = False
