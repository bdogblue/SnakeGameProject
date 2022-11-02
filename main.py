from pickle import TRUE
import pygame, sys

from pygame.locals import *

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

FPS = 2
DIR = 1

BORDER = pygame.Rect(WIDTH, 0, 10, HEIGHT)

snake = pygame.Rect(260, 200, 20, 20)
meal = pygame.Rect(80, 80, 20, 20)

def draw_window():
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, RED, snake)
    pygame.draw.rect(WIN, BLUE, meal)
    pygame.display.update()

def snake_handle_movement(keys_pressed, snake):
    global DIR
    if keys_pressed[pygame.K_LEFT]:  # LEFT
        DIR = 3
    if keys_pressed[pygame.K_RIGHT]:  # RIGHT
        DIR = 1
    if keys_pressed[pygame.K_UP]:  # UP
        DIR = 0
    if keys_pressed[pygame.K_DOWN]:  # DOWN
        DIR = 2
    move_snake(snake, DIR)

def move_snake(snake, direction):
    if direction == 0:
        snake.y -= 20
    if direction == 1:
        snake.x += 20
    if direction == 2:
        snake.y += 20
    if direction == 3:
        snake.x -= 20

def main():

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        
        snake_handle_movement(keys_pressed, snake)

        # Check if going off screen
        if snake.x < 0 or snake.x > WIDTH-20 or snake.y < 0 or snake.y > HEIGHT-20:
            break

        draw_window()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()