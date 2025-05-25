import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Game settings
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 7
ALIEN_SPEED = 1
ALIEN_DROP = 30

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders Clone")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.lives = 3
        
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -PLAYER_SPEED
        if keystate[pygame.K_RIGHT]:
            self.speed_x = PLAYER_SPEED
        self.rect.x += self.speed_x
        
        # Keep player on the screen
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed_x = ALIEN_SPEED
        self.direction = 1
        
    def update(self):
        self.rect.x += self.speed_x * self.direction

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -BULLET_SPEED
        
    def update(self):
        self.rect.y += self.speed_y
        # Kill the bullet if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
aliens = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Create the aliens
for row in range(5):
    for column in range(10):
        alien = Alien(column * 70 + 50, row * 50 + 50)
        all_sprites.add(alien)
        aliens.add(alien)

# Game variables
score = 0
game_over = False

# Game loop
running = True
while running:
    # Keep the loop running at the right speed
    clock.tick(FPS)
    
    # Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()
    
    # Update
    if not game_over:
        all_sprites.update()
        
        # Check if any alien has reached the edge
        move_down = False
        for alien in aliens:
            if alien.rect.right >= SCREEN_WIDTH or alien.rect.left <= 0:
                move_down = True
                break
        
        if move_down:
            for alien in aliens:
                alien.direction *= -1
                alien.rect.y += ALIEN_DROP
        
        # Check for bullet-alien collisions
        hits = pygame.sprite.groupcollide(bullets, aliens, True, True)
        for hit in hits:
            score += 10
        
        # Check if any alien has reached the bottom
        for alien in aliens:
            if alien.rect.bottom >= SCREEN_HEIGHT - 50:
                game_over = True
        
        # Check if all aliens are destroyed
        if len(aliens) == 0:
            game_over = True
    
    # Draw / render
    screen.fill(BLACK)
    all_sprites.draw(screen)
    
    # Draw the score
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))
    
    # Draw the lives
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
    
    # Draw game over message
    if game_over:
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
    
    # Flip the display
    pygame.display.flip()

# Quit the game
pygame.quit()
sys.exit()
