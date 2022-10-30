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
        self.wrap_around_screen()

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
        self.has_spawned = False

        # Randomly changes the size of the asteroid
        new_size_value = random.randint(40, 160)
        self.new_size = (new_size_value, new_size_value)
        self.image = pygame.transform.scale(self.image, self.new_size)
        self.original_image = self.image

        # Spawns the asteroid in a random spot offscreen
        starting_pos = self.calculate_starting_pos()
        self.position = vec(starting_pos[0], starting_pos[1])
        self.rect = self.image.get_rect(center=self.position)

        # Moves the asteroid in a straight line based on its starting pos
        starting_vec = self.calculate_trajectory(starting_pos)
        self.vel = vec(starting_vec[0], starting_vec[1])

        # Spins the asteroid
        self.spin_direction = spin_direction
        self.spin_angle = 0
        self.spin_factor = spin_factor

    def update(self):
        self.position += self.vel
        self.rect.center = self.position
        self.spin()
        self.leave_screen()
    
    def calculate_starting_pos(self):
        starting_x_side = "left" if random.randint(0, 1) == 0 else "right"
        if starting_x_side == "left":
            starting_x_value = random.randint(-self.new_size[0], WIDTH/2)
        elif starting_x_side == "right":
            starting_x_value = random.randint(WIDTH/2+1, WIDTH+self.new_size[1])
        if starting_x_value <= 0 or starting_x_value >= WIDTH:
            starting_y_value = random.randint(0, 720)
        else:
            starting_y_cond = "top" if random.randint(0, 1) == 0 else "bottom"
            if starting_y_cond == "top":
                starting_y_value = -self.new_size[0]
            elif starting_y_cond == "bottom":
                starting_y_value = HEIGHT+self.new_size[0]

        starting_pos = (starting_x_value, starting_y_value)
        return starting_pos

    def calculate_trajectory(self, starting_pos):
        starting_x_vec = 0
        starting_y_vec = 0

        # Spawns in top left: start_x < WIDTH/2 and start_y < 0
        if starting_pos[0] < WIDTH/2 and starting_pos[1] < 0:
            starting_x_vec = random.randint(1, 3)
            starting_y_vec = random.randint(1, 3)

        # Spawns in top right: start_x >= WIDTH/2 and start_y < 0
        elif starting_pos[0] >= WIDTH/2 and starting_pos[1] < 0:
            starting_x_vec = random.randint(-3, -1)
            starting_y_vec = random.randint(1, 3)

        # Spawns in bottom left: start_x < WIDTH/2 and start_y > HEIGHT
        elif starting_pos[0] < WIDTH/2 and starting_pos[1] > HEIGHT:
            starting_x_vec = random.randint(1, 3)
            starting_y_vec = random.randint(-3, -1)

        # Spawns in bottom right: start_x >= WIDTH/2 and start_y > HEIGHT
        elif starting_pos[0] >= WIDTH/2 and starting_pos[1] > HEIGHT:
            starting_x_vec = random.randint(-3, -1)
            starting_y_vec = random.randint(-3, -1)

        starting_vec = (starting_x_vec, starting_y_vec)
        return starting_vec

    def spin(self):
        if self.spin_direction == "clockwise":
            self.spin_angle -= 1 - (self.spin_factor/2)
        if self.spin_direction == "counter_clockwise":
            self.spin_angle += 1 + (self.spin_factor/2)
        self.image = pygame.transform.rotate(self.original_image, self.spin_angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def leave_screen(self):
        if self.position.x < WIDTH and self.position.x > 0 and self.position.y < HEIGHT and self.position.y > 0:
            self.has_spawned = True
        if self.has_spawned:
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
    if asteroid_count < 15:
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

    current_sprites = all_sprites.__len__()
    all_sprites.update()
    if all_sprites.__len__() < current_sprites:
            asteroid_count -= 1

    screen.fill((0, 0, 0))

    for star in stars:
        star.draw()
        star.update(-player.vel)

    all_sprites.draw(screen)
    pygame.display.update()
    fps_clock.tick(FPS)
