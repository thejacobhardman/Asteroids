import pygame, random

pygame.init()

screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Asteroids")
icon = pygame.image.load('Asteroid Brown.png')
pygame.display.set_icon(icon)

player_image = pygame.image.load('ship.png')
player_image.set_colorkey((0, 0, 0))
playerX = 640
playerY = 360
playerX_change = 0
playerY_change = 0
player_angle_change = 0
angle = 0

def player(x, y, angle):
    image_copy = pygame.transform.rotate(player_image, angle)
    screen.blit(pygame.transform.rotate(player_image, angle), (x - int(image_copy.get_width()/2), y - int(image_copy.get_height()/2)))

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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            playerY_change = -0.3
        if keys[pygame.K_DOWN]:
            playerY_change = 0.3
        if keys[pygame.K_RIGHT]:
            player_angle_change = -0.2
        if keys[pygame.K_LEFT]:
            player_angle_change = 0.2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                player_angle_change = 0

    screen.fill((0, 0, 0))

    playerX += playerX_change
    playerY += playerY_change

    # Keeps angle between 0 and 360 so it can be used for velocity calculations
    angle += player_angle_change
    if angle > 360:
        angle = 0
    if angle < 0:
        angle = 360

    if playerX <= 0:
        playerX = 1235
    if playerX > 1235:
        playerX = 0
    if playerY < 0:
        playerY = 689
    if playerY > 689:
        playerY = 0

    player(playerX, playerY, angle)

    print(angle)

    pygame.display.update()
