import pygame
import sys

# Initialize Pygame
pygame.init()

# Set window dimensions
WIDTH, HEIGHT = 800, 600

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3AINT")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Main game loop
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Close window when pressing Escape key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    # Fill the background with white
    screen.fill(BLACK)

    # Update the display
    pygame.display.flip()

