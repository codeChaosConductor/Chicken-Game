import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()
pygame.font.init()

# Set up screen
screen_width = 1920
screen_height = 1080
screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Chicken Egg Game")


def imageScaler(filepath, width):
    image = pygame.image.load(filepath)
    image_width = image.get_width()
    image_height = image.get_height()
    height = width/image_width*image_height
    return pygame.transform.scale(image, (width, height))


def eggLaying():
    egg_count = random.randint(5, 9)
    egg_positions = []
    i = 0
    while i < egg_count:
        istaken = False
        pos = random.randint(0, 9)
        for position in egg_positions:
            if position == pos:
                istaken = True
        if istaken != True:
            egg_positions.append(pos)
            i += 1
    return egg_positions


# Load images
chicken_img = imageScaler("assets/chicken.png", 150)
egg_img = imageScaler("assets/egg.png", 60)
pole_img = imageScaler("assets/pole.png", 1920)

# Global Variables

# Clock
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('Comic Sans MS', 30)

# Create a group for eggs
all_eggs = pygame.sprite.Group()

# Flag for falling eggs
eggs_falling = True

# Flag for showing the reset button
show_reset_button = False

# set text
reset_button_text = font.render('Eier legen', False, (0, 0, 0))


def drawScreen():
    screen.fill((255, 255, 255))

    # Update all eggs
    if eggs_falling:
        all_eggs.update()
        all_eggs.draw(screen)

    # Redraw pole
    screen.blit(pole_img, (0, 243))

    # Redraw all chicken
    i = 0
    while i < 10:
        screen.blit(chicken_img, (i*150+10, 50))
        i += 1

# Start new egg laying


def reset_eggs():
    all_eggs.empty()
    egg_positions = eggLaying()
    for position in egg_positions:
        egg = Egg(position*150+110, 170)
        all_eggs.add(egg)
    drawScreen()
    pygame.display.flip()
    global show_reset_button
    global eggs_falling
    show_reset_button = False
    time.sleep(1)
    eggs_falling = True

# Egg class


class Egg(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = egg_img
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        # Move the egg down till y=400
        if self.rect.y <= 400:
            self.rect.y += 5
        else:
            global show_reset_button
            global eggs_falling
            eggs_falling = False
            show_reset_button = True


# initial commands
reset_eggs()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            if 650 < x < 850 and 700 < y < 900 and show_reset_button == True:
                reset_eggs()

    screen.fill((255, 255, 255))

    # Update all eggs
    if eggs_falling:
        all_eggs.update()

    all_eggs.draw(screen)

    # Redraw pole
    screen.blit(pole_img, (0, 243))

    # Redraw all chicken
    i = 0
    while i < 10:
        screen.blit(chicken_img, (i*150+10, 50))
        i += 1

    # Redraw restart Button
    if show_reset_button:
        pygame.draw.rect(screen, (255, 100, 100), (665, 700, 200, 100))
        pygame.draw.rect(screen, (0, 0, 0), (665, 700, 200, 100), 2)
        screen.blit(reset_button_text, (695, 725))

    pygame.display.flip()

    clock.tick(30)

pygame.quit()
sys.exit()
