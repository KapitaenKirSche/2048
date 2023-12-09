# Import the pygame module
import pygame
from aufgabe1.test import test1

# Initialize the pygame module
pygame.init()

# Set up some constants
WIDTH = 800  # Width of the window
HEIGHT = 600  # Height of the window
FPS = 60  # Frames per second

# Create the screen object
# The size is a tuple containing the width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Game loop
running = True
while running:
    # Event processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Game logic here

    # Clear the screen
    screen.fill((190, 190, 190))

    # Draw everything
    test1(screen)

    # Flip the display
    pygame.display.flip()

    # Ensure the program maintains a rate of 60 frames per second
    pygame.time.Clock().tick(FPS)

# Quit the game
pygame.quit()
