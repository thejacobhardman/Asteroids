import pygame, random, math, sys
from itertools import repeat
from pygame import mixer

pygame.init()

vec = pygame.math.Vector2

WIDTH = 1280
HEIGHT = 720
MAX_SPEED = 9
FPS = 60
fps_clock = pygame.time.Clock()
title_font = pygame.font.SysFont(None, 64)
game_font = pygame.font.SysFont(None, 48)

org_screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen = org_screen.copy()
pygame.display.set_caption("Asteroids")
icon = pygame.image.load('Assets/Art/Asteroid Brown.png')
pygame.display.set_icon(icon)

bullet_sound = mixer.Sound("Assets/SFX/laser1.wav")
bullet_sound.set_volume(0.8)
engine_sound = mixer.Sound("Assets/SFX/engine1.wav")
engine_sound.set_volume(0.4)
explosion_sound = mixer.Sound("Assets/SFX/explosion.wav")
explosion_sound.set_volume(0.5)

# Shakes the screen upon player death
offset = repeat((0, 0))
def shake():
    s = -1
    for _ in range(0, 3):
        for x in range(0, 20, 5):
            yield (x*s, 0)
        for x in range(20, 0, 5):
            yield (x*s, 0)
        s *= -1
    while True:
        yield (0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Assets/Art/ship.png')
        self.original_image = self.image
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.rect = self.image.get_rect(center=self.position)
        self.vel = vec(0, 0)
        self.acceleration = vec(0, -0.2)
        self.angle_speed = 0
        self.angle = 0
        self.id = "player"
        self.color = (255, 165, 0)
        self.particles = pygame.sprite.Group()

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
            self.exhaust()
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

    def shoot(self):
        bullet = Bullet(self)
        all_sprites.add(bullet)
        bullets.add(bullet)
        bullet_sound.play()

    def exhaust(self):
        for i in range(5):
            self.color = (255, random.randint(69, 215), 0)
            particle = Particle(self)
            all_sprites.add(particle)
            self.particles.add(particle)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)
        self.color = (255, 0, 0)
        self.position = vec(player.position)
        self.vel = vec(0, 10).rotate(player.angle+180)
        self.angle = player.angle+180
        self.image = pygame.Surface((3, 15), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, -self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.vel
        self.rect.center = self.position
        self.leave_screen()

    def leave_screen(self):
        if self.position.x > WIDTH:
            all_sprites.remove(self)
            bullets.remove(self)
        if self.position.x < 0:
            all_sprites.remove(self)
            bullets.remove(self)
        if self.position.y <= 0:
            all_sprites.remove(self)
            bullets.remove(self)
        if self.position.y > HEIGHT:
            all_sprites.remove(self)
            bullets.remove(self)


class Asteroid(pygame.sprite.Sprite):
    def __init__(self, spin_direction, spin_factor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('Assets/Art/Asteroid Brown.png')
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
                asteroids.remove(self)
            if self.position.x < 0:
                all_sprites.remove(self)
                asteroids.remove(self)
            if self.position.y <= 0:
                all_sprites.remove(self)
                asteroids.remove(self)
            if self.position.y > HEIGHT:
                all_sprites.remove(self)
                asteroids.remove(self)
            
class Explosion():
    def __init__(self, position):
        self.position = position
        self.color = (255, 255, 255)
        self.particles = pygame.sprite.Group()
        self.id = "explosion"

    def explode(self):
        explosion_sound.play()
        for i in range(50):
            self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            particle = Particle(self)
            all_sprites.add(particle)
            self.particles.add(particle)

class Particle(pygame.sprite.Sprite):
    def __init__(self, parent):
        pygame.sprite.Sprite.__init__(self)
        self.parent = parent
        self.color = parent.color
        self.position = vec(parent.position)
        if parent.id == "explosion":
            self.angle = random.randint(0, 360)
            self.vel = vec(0, 10).rotate(self.angle)
        elif parent.id == "player":
            self.vel = vec(0, 10).rotate(parent.angle+random.randint(-5, 5))
            self.angle = parent.angle+random.randint(-5, 5)
        self.image = pygame.Surface((random.randint(1, 4), random.randint(1, 4)), pygame.SRCALPHA)
        self.image.fill(self.color)
        self.original_image = self.image
        self.rect = self.image.get_rect(center=self.position)

    def update(self):
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.vel
        self.rect.center = self.position
        self.leave_screen()

    def leave_screen(self):
        if self.position.x > WIDTH:
            all_sprites.remove(self)
            self.parent.particles.remove(self)
        if self.position.x < 0:
            all_sprites.remove(self)
            self.parent.particles.remove(self)
        if self.position.y <= 0:
            all_sprites.remove(self)
            self.parent.particles.remove(self)
        if self.position.y > HEIGHT:
            all_sprites.remove(self)
            self.parent.particles.remove(self)

class Star():
    def __init__(self):
        self.position = vec(WIDTH / 2, HEIGHT / 2)
        self.color = (255, 255, 255)
        self.radius = 1
        self.max_radius = 2

    def update(self, vel):
        self.position += vel
        self.twinkle()
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

    def twinkle(self):
        twinkle = random.randint(0, 20)
        if twinkle == 1:
            if self.radius >= 1 and self.radius <= self.max_radius:
                self.radius += 1
            else:
                self.radius -= 1

class Collision():
    def __init__(self, is_collision, position):
        self.is_collision = is_collision
        self.position = position

# Checks to make sure that no stars are overlapping
def check_intersections(c1, c2):
    dx = c1.position.x - c2.position.x
    dy = c1.position.y - c2.position.y
    distance = math.hypot(dx, dy)
    if distance < c1.radius + c2.radius:
        return True
    return False

def check_collisions(sprite, group):
    is_collision = False
    if type(sprite) == pygame.sprite.Group:
        for individual_sprite in sprite.sprites():
            is_collision = pygame.sprite.spritecollide(individual_sprite, group, False)
            if is_collision:
                all_sprites.remove(individual_sprite)
                asteroids.remove(individual_sprite)
                collision = Collision(True, individual_sprite.position)
                return collision
    else:
        is_collision = pygame.sprite.spritecollide(sprite, group, True)
        if is_collision:
                all_sprites.remove(sprite)
                collision = Collision(True, sprite.position)
                return collision
    return Collision(False, (WIDTH/2, HEIGHT/2))

def draw_text(text, font, color, surface, x, y):
    text = font.render(text, 1, color)
    text_rect = text.get_rect()
    text_rect.center = (x, y)
    surface.blit(text, text_rect)

all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
player = Player()
asteroid_count = 0

def reset_game():
    all_sprites.empty()
    asteroids.empty()
    bullets.empty()
    player.position = (WIDTH/2, HEIGHT/2)
    player.angle = 0
    player.vel = 0
    all_sprites.add(player)

# Generates the starfield
stars = []
for i in range(200):
    stars.append(Star())
for i in range(199):
    while check_intersections(stars[i], stars[i+1]):
        stars[i].position.x = random.randint(0, WIDTH)
        stars[i].position.y = random.randint(0, HEIGHT)

click = False

def main_menu(all_sprites, asteroids, bullets, player, asteroid_count, offset):
    mixer.music.load("Assets/SFX/MyVeryOwnDeadShip.ogg")
    mixer.music.play(-1)
    click = False

    reset_game()

    while True:
        screen.fill((0, 0, 0))
        for star in stars:
            star.draw()
            star.twinkle()
        draw_text("ASTEROIDS", title_font, (255, 255, 255), screen, WIDTH/2, HEIGHT/2-100)
        mouseX, mouseY = pygame.mouse.get_pos()
        play_button = pygame.Rect(WIDTH/2, HEIGHT/2, 200, 50)
        play_button.center=(WIDTH/2, HEIGHT/2)
        quit_button = pygame.Rect(WIDTH/2, HEIGHT/2+75, 200, 50)
        quit_button.center=(WIDTH/2, HEIGHT/2+75)
        if play_button.collidepoint((mouseX, mouseY)):
            if click:
                game_loop(all_sprites, asteroids, bullets, player, asteroid_count, offset)
        if quit_button.collidepoint((mouseX, mouseY)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(screen, (255, 255, 255), play_button)
        draw_text("PLAY", game_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2)
        pygame.draw.rect(screen, (255, 255, 255), quit_button)
        draw_text("QUIT", game_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2+75)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

def game_loop(all_sprites, asteroids, bullets, player, asteroid_count, offset):
    mixer.music.load("Assets/SFX/through space.ogg")
    mixer.music.play(-1)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()
                if event.key == pygame.K_w:
                    engine_sound.play()

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
            asteroids.add(asteroid)
            asteroid_count += 1

        current_sprites = all_sprites.__len__()
        if current_sprites > 16:
            current_sprites = 16
        all_sprites.update()
        if all_sprites.__len__() < current_sprites:
                asteroid_count -= 1

        did_player_collide = check_collisions(player, asteroids)
        if did_player_collide.is_collision:
            position = did_player_collide.position
            explosion = Explosion(position)
            explosion.explode()
            offset = shake()
            game_over(all_sprites, asteroids, bullets, player, asteroid_count, offset) # <- Need to delay this
        if bullets.__len__() >= 1:
            did_bullet_collide = check_collisions(asteroids, bullets)
            if did_bullet_collide.is_collision:
                position = did_bullet_collide.position
                explosion = Explosion(position)
                explosion.explode()

        org_screen.fill((255, 255, 255))
        screen.fill((0, 0, 0))

        for star in stars:
            star.draw()
            star.update(-player.vel)

        fps_clock.tick(FPS)
        all_sprites.draw(screen)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

def game_over(all_sprites, asteroids, bullets, player, asteroid_count, offset):
    mixer.music.load("Assets/SFX/MyVeryOwnDeadShip.ogg")
    mixer.music.play(-1)
    click = False

    while True:
        screen.fill((0, 0, 0))
        for star in stars:
            star.draw()
            star.twinkle()
        draw_text("GAME OVER", title_font, (255, 255, 255), screen, WIDTH/2, HEIGHT/2-100)
        mouseX, mouseY = pygame.mouse.get_pos()
        menu_button = pygame.Rect(WIDTH/2, HEIGHT/2, 200, 50)
        menu_button.center=(WIDTH/2, HEIGHT/2)
        quit_button= pygame.Rect(WIDTH/2, HEIGHT/2+75, 200, 50)
        quit_button.center=(WIDTH/2, HEIGHT/2+75)
        if menu_button.collidepoint((mouseX, mouseY)):
            if click:
                main_menu(all_sprites, asteroids, bullets, player, asteroid_count, offset)
        if quit_button.collidepoint((mouseX, mouseY)):
            if click:
                pygame.quit()
                sys.exit()
        pygame.draw.rect(screen, (255, 255, 255), menu_button)
        draw_text("MAIN MENU", game_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2)
        pygame.draw.rect(screen, (255, 255, 255), quit_button)
        draw_text("QUIT", game_font, (0, 0, 0), screen, WIDTH/2, HEIGHT/2+75)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        fps_clock.tick(FPS)
        org_screen.blit(screen, next(offset))
        pygame.display.update()

main_menu(all_sprites, asteroids, bullets, player, asteroid_count, offset)
