import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Professional 2D Platformer Game")

# Clock
clock = pygame.time.Clock()
FPS = 60

# Load images
background_image = pygame.image.load("background.png")  # Add a background image
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

player_image = pygame.image.load("player.png")  # Add a player image
player_image = pygame.transform.scale(player_image, (50, 50))

coin_image = pygame.image.load("coin.png")  # Add a coin image
coin_image = pygame.transform.scale(coin_image, (50, 50))

obstacle_image = pygame.image.load("obstacle.png")  # Add an obstacle image
obstacle_image = pygame.transform.scale(obstacle_image, (70, 70))

# Load sounds
pygame.mixer.init()
jump_sound = pygame.mixer.Sound("jump.wav")  # Add a jump sound file
coin_sound = pygame.mixer.Sound("coin.wav")  # Add a coin sound file
collision_sound = pygame.mixer.Sound("collision.wav")  # Add a collision sound file

# Fonts
font = pygame.font.SysFont("Arial", 30)
button_font = pygame.font.SysFont("Arial", 40)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, screen):
        # Change color if hovered
        if self.hovered:
            pygame.draw.rect(screen, self.hover_color, self.rect, border_radius=10)
        else:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=10)

        # Draw text
        text_surface = button_font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Player properties
player_width = 50
player_height = 50
player_x = 100
player_y = SCREEN_HEIGHT - player_height - 50
player_vel_y = 0
player_jump = False
player_double_jump = False  # Track double jump
player_speed = 5

# Coin properties
coin_width = 30
coin_height = 30
coin_x = random.randint(200, SCREEN_WIDTH - coin_width)
coin_y = random.randint(100, SCREEN_HEIGHT - coin_height - 100)
coin_collected = False

# Obstacle properties
obstacle_width = 70
obstacle_height = 70
obstacle_x = SCREEN_WIDTH
obstacle_y = SCREEN_HEIGHT - obstacle_height - 50
obstacle_speed = 5

# Lives
lives = 3

# Score
score = 0

# Timer
start_time = time.time()

# Game states
game_started = False
game_paused = False

# Buttons
start_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50, 200, 100, "Start", (0, 128, 255), (0, 102, 204))
pause_button = Button(SCREEN_WIDTH - 120, 20, 100, 50, "Pause", (255, 128, 0), (204, 102, 0))

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Draw background
    screen.blit(background_image, (0, 0))

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not game_started and start_button.is_clicked(mouse_pos):
                game_started = True
            if game_started and pause_button.is_clicked(mouse_pos):
                game_paused = not game_paused

    # Check button hover
    mouse_pos = pygame.mouse.get_pos()
    if not game_started:
        start_button.check_hover(mouse_pos)
    pause_button.check_hover(mouse_pos)

    # Draw start button if game hasn't started
    if not game_started:
        start_button.draw(screen)
    else:
        # Draw pause button
        pause_button.draw(screen)

        # Game logic (only if not paused)
        if not game_paused:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= player_speed
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
                player_x += player_speed

            # Jumping mechanics
            if keys[pygame.K_SPACE]:
                if not player_jump:  # First jump
                    player_vel_y = -20  # Increase upward velocity for higher jump
                    player_jump = True
                    jump_sound.play()
                elif player_jump and not player_double_jump:  # Double jump
                    player_vel_y = -20  # Increase upward velocity for double jump
                    player_double_jump = True
                    jump_sound.play()

            # Apply gravity
            player_vel_y += 1
            player_y += player_vel_y

            # Ground collision
            if player_y >= SCREEN_HEIGHT - player_height - 50:
                player_y = SCREEN_HEIGHT - player_height - 50
                player_jump = False
                player_double_jump = False  # Reset double jump when on the ground

            # Draw player
            screen.blit(player_image, (player_x, player_y))

            # Draw coin
            if not coin_collected:
                screen.blit(coin_image, (coin_x, coin_y))

            # Coin collision
            if (player_x < coin_x + coin_width and player_x + player_width > coin_x and
                    player_y < coin_y + coin_height and player_y + player_height > coin_y):
                coin_collected = True
                score += 1
                coin_x = random.randint(200, SCREEN_WIDTH - coin_width)
                coin_y = random.randint(100, SCREEN_HEIGHT - coin_height - 100)
                coin_collected = False
                coin_sound.play()  # Play coin sound

            # Draw obstacle
            screen.blit(obstacle_image, (obstacle_x, obstacle_y))

            # Move obstacle
            obstacle_x -= obstacle_speed
            if obstacle_x < 0:
                obstacle_x = SCREEN_WIDTH
                obstacle_speed += 0.5  # Increase speed over time

            # Obstacle collision
            if (player_x < obstacle_x + obstacle_width and player_x + player_width > obstacle_x and
                    player_y < obstacle_y + obstacle_height and player_y + player_height > obstacle_y):
                lives -= 1
                collision_sound.play()  # Play collision sound
                if lives == 0:
                    running = False
                else:
                    # Reset player and obstacle position after collision
                    player_x = 100
                    player_y = SCREEN_HEIGHT - player_height - 50
                    obstacle_x = SCREEN_WIDTH

            # Display score
            score_text = font.render(f"Score: {score}", True, (255, 255, 255))
            screen.blit(score_text, (10, 10))

            # Display lives
            lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
            screen.blit(lives_text, (10, 50))

            # Display timer
            elapsed_time = int(time.time() - start_time)
            timer_text = font.render(f"Time: {elapsed_time}s", True, (255, 255, 255))
            screen.blit(timer_text, (10, 90))

    # Update display
    pygame.display.update()

# Game over screen
screen.fill((0, 0, 0))
game_over_text = font.render(f"Game Over! Score: {score}", True, (255, 255, 255))
screen.blit(game_over_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 50))
pygame.display.update()
pygame.time.wait(3000)  # Show game over screen for 3 seconds

# Quit Pygame
pygame.quit()