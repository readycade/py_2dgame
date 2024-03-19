import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 400
FPS = 30  # Adjust frame rate
GRAVITY = 1.0  # Adjust the gravity
JUMP_HEIGHT = 10  # Adjust the jump height
PIPE_WIDTH = 50
PIPE_HEIGHT = 200
PIPE_GAP = 250  # Adjust the gap between pipes

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Load images
bird_image = pygame.image.load("bird.png")
background_image = pygame.image.load("background.png")
pipe_image = pygame.image.load("pipe.png")

# Scale images
bird_image = pygame.transform.scale(bird_image, (30, 30))  # Adjust the bird size
pipe_image = pygame.transform.scale(pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))


# Clock to control the frame rate
clock = pygame.time.Clock()


class Bird:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.width = 30  # Adjust the bird's width
        self.height = 30  # Adjust the bird's height
        self.velocity = 0

    def jump(self):
        self.velocity = -JUMP_HEIGHT  # Adjusted to go upward when jumping

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

        # Keep the bird within the screen bounds
        if self.y < 0:
            self.y = 0
        if self.y > HEIGHT - self.height:
            self.y = HEIGHT - self.height

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))


class Pipe:
    def __init__(self, x):
        self.x = x
        self.gap_top = random.randint(50, HEIGHT - 50 - PIPE_GAP)  # Adjust the gap position

    def update(self):
        self.x -= 5  # Adjust the pipe's movement speed

    def draw(self):
        lower_pipe_top = self.gap_top + PIPE_GAP
        screen.blit(pipe_image, (self.x, lower_pipe_top))


# Create objects
bird = Bird()
pipes = [Pipe(WIDTH + i * 300) for i in range(3)]  # Adjust initial pipe positions

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()

    # Update objects
    bird.update()
    for pipe in pipes:
        pipe.update()

    # Create new pipes
    if pipes[-1].x < WIDTH - 200:
        pipes.append(Pipe(WIDTH))

    # Remove off-screen pipes
    pipes = [pipe for pipe in pipes if pipe.x > -PIPE_WIDTH]

    # Collision detection
    bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
    for pipe in pipes:
        upper_pipe_rect = pygame.Rect(pipe.x, 0, PIPE_WIDTH, pipe.gap_top)
        lower_pipe_rect = pygame.Rect(pipe.x, pipe.gap_top + PIPE_GAP, PIPE_WIDTH, HEIGHT - pipe.gap_top - PIPE_GAP)

        # Check for collision with upper and lower pipes
        if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
            print("Game Over")
            bird = Bird()  # Reset the bird position
            pipes = []  # Reset the pipes
            pygame.time.delay(1000)  # Pause for a moment before restarting

    # Draw background
    screen.fill(WHITE)
    screen.blit(background_image, (0, 0))

    # Draw objects
    bird.draw()
    for pipe in pipes:
        pipe.draw()

    # Update display
    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)
