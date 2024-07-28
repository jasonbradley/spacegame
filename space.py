import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)

# Score variable
score = 0

# Font for displaying text
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 72)

# Spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self):
        super(Spaceship, self).__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50)
        self.speed = 5
        self.draw_spaceship()

    def draw_spaceship(self):
        pygame.draw.polygon(self.image, WHITE, [(25, 0), (0, 50), (50, 50)])  # Triangle
        pygame.draw.rect(self.image, WHITE, (5, 35, 10, 15))  # Left gun
        pygame.draw.rect(self.image, WHITE, (35, 35, 10, 15))  # Right gun

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_d] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

    def shoot(self):
        laser1 = Laser(self.rect.left + 5, self.rect.top)
        laser2 = Laser(self.rect.right - 15, self.rect.top)
        all_sprites.add(laser1, laser2)
        lasers.add(laser1, laser2)

# Star class
class Star(pygame.sprite.Sprite):
    def __init__(self):
        super(Star, self).__init__()
        self.image = pygame.Surface((5, 5), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH)
        self.rect.y = random.randint(-20, 0)
        self.speed = random.randint(1, 5)
        self.alpha = random.randint(50, 255)  # Random initial transparency
        self.twinkle_speed = random.uniform(0.5, 1.5)  # Random twinkle speed
        self.image.fill(WHITE)
        self.image.set_alpha(self.alpha)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH)
            self.rect.y = random.randint(-20, 0)
            self.speed = random.randint(1, 5)
            self.alpha = random.randint(50, 255)
            self.twinkle_speed = random.uniform(0.5, 1.5)
        
        # Twinkle effect
        self.alpha += int(self.twinkle_speed)
        if self.alpha >= 255 or self.alpha <= 50:
            self.twinkle_speed = -self.twinkle_speed
        self.image.set_alpha(self.alpha)

# Shooting Star class
class ShootingStar(pygame.sprite.Sprite):
    def __init__(self):
        super(ShootingStar, self).__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        self.color = WHITE
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH // 2)
        self.rect.y = random.randint(0, SCREEN_HEIGHT // 2)
        self.speed = 10
        self.alpha = 255
        self.image.fill(WHITE)
        self.image.set_alpha(self.alpha)

    def update(self):
        self.rect.x += self.speed
        self.rect.y += int(self.speed * 0.5)  # Move diagonally
        self.alpha -= 5  # Fade out
        if self.alpha <= 0:
            self.kill()  # Remove the star when fully faded
        else:
            self.image.set_alpha(self.alpha)

# Function to draw gradient
def draw_gradient(surface, color1, color2, rect):
    color1 = pygame.Color(*color1)
    color2 = pygame.Color(*color2)
    steps = rect.height
    for i in range(steps):
        color = (
            color1.r + (color2.r - color1.r) * i // steps,
            color1.g + (color2.g - color1.g) * i // steps,
            color1.b + (color2.b - color1.b) * i // steps,
            color1.a + (color2.a - color1.a) * i // steps
        )
        pygame.draw.line(surface, color, (rect.x, rect.y + i), (rect.x + rect.width, rect.y + i))

# Laser class
class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Laser, self).__init__()
        self.image = pygame.Surface((5, 20), pygame.SRCALPHA)
        draw_gradient(self.image, (0, 0, 255, 255), (0, 255, 255, 255), self.image.get_rect())
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.Surface((50, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.uniform(0.5, 1.5)
        self.draw_enemy()
        self.shoot_timer = random.randint(30, 100)

    def draw_enemy(self):
        pygame.draw.ellipse(self.image, WHITE, [0, 0, 50, 20])  # Flying saucer
        pygame.draw.rect(self.image, RED, [20, 20, 10, 10])  # Red flame

    def update(self):
        self.rect.y += self.speed
        self.speed += 0.005  # Increase speed gradually

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            self.shoot()
            self.shoot_timer = random.randint(30, 100)

    def shoot(self):
        enemy_laser = EnemyLaser(self.rect.centerx, self.rect.bottom)
        all_sprites.add(enemy_laser)
        enemy_lasers.add(enemy_laser)

# Enemy Laser class
class EnemyLaser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(EnemyLaser, self).__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 5

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

# Explosion class
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super(Explosion, self).__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.timer = 10

    def update(self):
        self.timer -= 1
        if self.timer <= 0:
            self.kill()

# Initialize the game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jason's Space Shooter")

# Create sprite groups
all_sprites = pygame.sprite.Group()
stars = pygame.sprite.Group()
shooting_stars = pygame.sprite.Group()
lasers = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemy_lasers = pygame.sprite.Group()

# Create a spaceship
spaceship = Spaceship()
all_sprites.add(spaceship)

# Create stars
for _ in range(50):
    star = Star()
    all_sprites.add(star)
    stars.add(star)

# Game loop
running = True
clock = pygame.time.Clock()
shooting_star_timer = 0
enemy_spawn_timer = 0
game_active = False  # Flag for game state

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not game_active:
                game_active = True
            if event.key == pygame.K_SPACE and game_active:
                spaceship.shoot()

    if game_active:
        # Create a shooting star every 200 frames
        shooting_star_timer += 1
        if shooting_star_timer > 200:
            shooting_star_timer = 0
            shooting_star = ShootingStar()
            all_sprites.add(shooting_star)
            shooting_stars.add(shooting_star)

        # Spawn enemies if there are less than 3 on the screen
        if len(enemies) < 3:
            enemy_spawn_timer += 1
            if enemy_spawn_timer > 100:
                enemy_spawn_timer = 0
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)

        # Update all sprites
        all_sprites.update()

        # Check for collisions between lasers and enemies
        hits = pygame.sprite.groupcollide(enemies, lasers, True, True)
        for hit in hits:
            explosion = Explosion(hit.rect.center)
            all_sprites.add(explosion)
            score += 5

        # Check for collisions between enemy lasers and the spaceship
        hits = pygame.sprite.spritecollide(spaceship, enemy_lasers, True)
        for hit in hits:
            score -= 5
            if score < 0:
                score = 0

        # Clear the screen
        screen.fill(BLACK)

        # Draw all sprites
        all_sprites.draw(screen)

        # Draw the score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # Title screen
        screen.fill(BLACK)
        title_text = title_font.render("Jason's Space Shooter", True, WHITE)
        instructions_text1 = font.render("Use 'a' and 'd' to move.", True, WHITE)
        instructions_text2 = font.render("Press spacebar to shoot.", True, WHITE)
        start_text = font.render("Press enter key to start game.", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
        screen.blit(instructions_text1, (SCREEN_WIDTH // 2 - instructions_text1.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(instructions_text2, (SCREEN_WIDTH // 2 - instructions_text2.get_width() // 2, SCREEN_HEIGHT // 2 + 40))
        screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2 + 80))

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
