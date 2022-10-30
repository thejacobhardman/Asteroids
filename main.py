import pygame, random, math

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
        # Slows the ship as time passes
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

#class Bullet(pygame.sprite.Sprite):


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, spin_direction, spin_factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Asteroid Brown.png')
        new_size_value = random.randint(40, 160)
        new_size = (new_size_value, new_size_value)
        self.image = pygame.transform.scale(self.image, new_size)
        self.original_image = self.image
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(random.randint(-2, 2), random.randint(-2, 2))
        self.spin_direction = spin_direction
        self.spin_angle = 0
        self.spin_factor = spin_factor

    def update(self):
        self.position += self.vel
        self.rect.center = self.position
        self.leave_screen()
        self.spin()

    def spin(self):
        if self.spin_direction == "clockwise":
            self.spin_angle -= 1 - (self.spin_factor/2)
        if self.spin_direction == "counter_clockwise":
            self.spin_angle += 1 + (self.spin_factor/2)
        self.image = pygame.transform.rotate(self.original_image, self.spin_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def leave_screen(self):
        if self.position.x > WIDTH:
            all_sprites.remove(self)
        if self.position.x < 0:
            all_sprites.remove(self)
        if self.position.y <= 0:
            all_sprites.remove(self)
        if self.position.y > HEIGHT:
            all_sprites.remove(self)

class Star():
    def __init__(self):
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.2)
        self.angle_speed = 0
        self.angle = 0
        self.color = (255, 255, 255)
        self.radius = 1

    def update(self, vel):
        self.vel = vel
        self.position += vel
        #self.twinkle()
        self.wrap_around_screen()

    def wrap_around_screen(self):
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y <= 0:
            self.position.y = HEIGHT
        if self.position.y > HEIGHT:
            self.position.y = 0

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.position.x, self.position.y), self.radius)

    # def twinkle(self):
    #     twinkle = random.randint(0, 1)
    #     if twinkle == 1:
    #         self.color = (0, 0, 0)
    #     self.color = (255, 255, 255)

# Checks to make sure that no stars are overlapping
def check_intersections(c1, c2):
    dx = c1.position.x - c2.position.x
    dy = c1.position.y - c2.position.y
    distance = math.hypot(dx, dy)
    if distance < c1.radius + c2.radius:
        return True
    return False

all_sprites = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
asteroid_count = 0

# Generates the starfield
stars = []
for i in range(200):
    stars.append(Star())
for i in range(199):
    while check_intersections(stars[i], stars[i+1]):
        stars[i].position.x = random.randint(0, WIDTH)
        stars[i].position.y = random.randint(0, HEIGHT)

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
            if event.key == pygame.K_f: # Handles if the player wants to fullscreen the game
                fullscreen = not fullscreen
                if fullscreen:
                    WIDTH = pygame.display.get_desktop_sizes()[0][0]
                    HEIGHT = pygame.display.get_desktop_sizes()[0][1]
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    WIDTH = 1280
                    HEIGHT = 720
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # Spawns new asteroids
    if asteroid_count < 1:
        # Determines what direction and how fast the asteroid will spin
        spin_generator = random.randint(0, 1)
        spin_factor = random.randint(0, 10)
        spin_direction = ""
        if spin_generator == 0:
            spin_direction = "clockwise"
        if spin_generator == 1:
            spin_direction = "counter_clockwise"
        asteroid = Asteroid(spin_direction, spin_factor)
        all_sprites.add(asteroid)
        asteroid_count += 1

    player.wrap_around_screen()
    all_sprites.update()

    # for sprite in all_sprites:
    #     print(sprite)

    screen.fill((0, 0, 0))

    for star in stars:
        star.draw()
        star.update(-player.vel)

    all_sprites.draw(screen)
    pygame.display.update()
    fps_clock.tick(FPS)
