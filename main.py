import pygame

pygame.init()

vec = pygame.math.Vector2

WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 9
FPS = 60
fps_clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Asteroids")
icon = pygame.image.load('Asteroid Brown.png')
pygame.display.set_icon(icon)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ship.png')
        self.original_image = self.image
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.2)
        self.angle_speed = 0
        self.angle = 0

    def update(self):
        if self.vel != 0:
            self.vel -= self.vel*0.02

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.angle_speed = -4.5
            player.rotate()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.angle_speed = 4.5
            player.rotate()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.vel += self.acceleration
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.vel -= self.acceleration

        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)

        self.position += self.vel
        self.rect.center = self.position

    def rotate(self):
        self.acceleration.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        elif self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def wrap_around_screen(self):
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y <= 0:
            self.position.y = HEIGHT
        if self.position.y > HEIGHT:
            self.position.y = 0

class Asteroid(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Asteroid Brown.png')
        self.original_image = self.image
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)

    def update(self):
        self.position += self.vel
        self.rect.center = self.position
        self.leave_screen()

    def leave_screen(self):
        if self.position.x > WIDTH:
            all_sprites.remove(self)
        if self.position.x < 0:
            all_sprites.remove(self)
        if self.position.y <= 0:
            all_sprites.remove(self)
        if self.position.y > HEIGHT:
            all_sprites.remove(self)

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
asteroid_count = 0
fullscreen = False

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        if event.type == pygame.VIDEORESIZE:
            if not fullscreen:
                WIDTH = event.w
                HEIGHT = event.h
                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                fullscreen = not fullscreen
                if fullscreen:
                    WIDTH = pygame.display.get_desktop_sizes()[0][0]
                    HEIGHT = pygame.display.get_desktop_sizes()[0][1]
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    WIDTH = 1280
                    HEIGHT = 720
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    if asteroid_count <= 1:
        asteroid = Asteroid()
        all_sprites.add(asteroid)
        asteroid_count += 1

    player.wrap_around_screen()
    all_sprites.update()

    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    pygame.display.update()
    fps_clock.tick(FPS)
