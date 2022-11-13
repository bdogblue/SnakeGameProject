from pickle import TRUE
import pygame, sys, random

from pygame.locals import *

WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake')

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

FPS = 2
DIR = 1

BLOCKSIZE = 20
TAIL = 0

BORDER = pygame.Rect(WIDTH, 0, 10, HEIGHT)

snake = pygame.Rect(260, 200, BLOCKSIZE, BLOCKSIZE)
meal = pygame.Rect(80, 80, BLOCKSIZE, BLOCKSIZE)
 
# add a new section when snake head eats a meal
# 
# if snake head runs into tale then game over

# also a new meal needs to not spawn in the tale

# need a new game over screen

def draw_window(tail_parts):
    WIN.fill(BLACK)
    pygame.draw.rect(WIN, RED, snake)
    pygame.draw.rect(WIN, BLUE, meal)

    for tail in tail_parts:
        pygame.draw.rect(WIN, RED, tail)

    pygame.display.update()

def snake_handle_movement(keys_pressed, snake, tail_parts):
    global DIR
    if keys_pressed[pygame.K_LEFT]:  # LEFT
        DIR = 3
    if keys_pressed[pygame.K_RIGHT]:  # RIGHT
        DIR = 1
    if keys_pressed[pygame.K_UP]:  # UP
        DIR = 0
    if keys_pressed[pygame.K_DOWN]:  # DOWN
        DIR = 2
    
    current_x = snake.x
    current_y = snake.y

    move_snake(snake, DIR)

    tail_parts = move_tail(tail_parts, current_x, current_y)

def move_snake(snake, direction):
    if direction == 0:
        snake.y -= snake.height
    if direction == 1:
        snake.x += snake.width
    if direction == 2:
        snake.y += snake.height
    if direction == 3:
        snake.x -= snake.width

def move_meal(meal, snake):
    
    if snake.x-(snake.width*3) <= meal.width: 
        meal.x = random.randrange(snake.x+(snake.width*4), WIDTH-meal.width, BLOCKSIZE)
    elif snake.x+(snake.width*4) >= WIDTH-meal.width:
        meal.x = random.randrange(0, snake.x-(snake.width*3), BLOCKSIZE)
    else:
        meal.x = random.choice([random.randrange(0, snake.x-(snake.width*3), BLOCKSIZE), random.randrange(snake.x+(snake.width*4), WIDTH-meal.width, BLOCKSIZE)])

    if snake.y-(snake.height*3) <= meal.height: 
        meal.y = random.randrange(snake.y+(snake.height*4), HEIGHT-meal.height, BLOCKSIZE)
    elif snake.y+(snake.height*4) >= HEIGHT-meal.height:
        meal.y = random.randrange(0, snake.y-(snake.height*3), BLOCKSIZE)
    else:
        meal.y = random.choice([random.randrange(0, snake.y-(snake.height*3), BLOCKSIZE), random.randrange(snake.y+(snake.height*4), HEIGHT-meal.height, BLOCKSIZE)])

def add_tail(tail_parts, snake):
    global TAIL, DIR

    if TAIL <= 0:
        if DIR == 0:
            newpart = Rect(snake.x, snake.y + snake.height, BLOCKSIZE, BLOCKSIZE)
        if DIR == 1:
            newpart = Rect(snake.x - snake.width, snake.y, BLOCKSIZE, BLOCKSIZE)
        if DIR == 2:
            newpart = Rect(snake.x, snake.y - snake.height, BLOCKSIZE, BLOCKSIZE)
        if DIR == 3:
            newpart = Rect(snake.x + snake.width, snake.y, BLOCKSIZE, BLOCKSIZE)
        tail_parts.append(newpart)

def move_tail(tail_parts, pre_snake_x, pre_snake_y):
    global TAIL

    new_parts = tail_parts
    
    for part in new_parts:
        count =+ 1

    if TAIL > 0:
        new_parts[0].x = pre_snake_x
        new_parts[0].y = pre_snake_y

    for tail in tail_parts:
        if TAIL != 0 and TAIL+1 < len(new_parts):
            new_parts[tail+1].x = tail_parts[tail_parts].x
            new_parts[tail+1].y = tail_parts[tail_parts].y
    
    return new_parts
    
def main():

    global TAIL

    clock = pygame.time.Clock()

    tail_parts = []

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        snake_handle_movement(keys_pressed, snake, tail_parts)

        if snake.colliderect(meal):
            add_tail(tail_parts, snake)
            move_meal(meal, snake)
            TAIL += 1

        # Check if going off screen
        if snake.x < 0 or snake.x > WIDTH-snake.width or snake.y < 0 or snake.y > HEIGHT-snake.height:
            break

        draw_window(tail_parts)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()