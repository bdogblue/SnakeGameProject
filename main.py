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
    
    tail_parts = move_tail(tail_parts, snake)
    
    move_snake(snake, DIR)

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

    pos = TAIL - 1

    if TAIL <= 0:
        if DIR == 0:
            newpart = Rect(snake.x, snake.y + snake.height, BLOCKSIZE, BLOCKSIZE)
        if DIR == 1:
            newpart = Rect(snake.x - snake.width, snake.y, BLOCKSIZE, BLOCKSIZE)
        if DIR == 2:
            newpart = Rect(snake.x, snake.y - snake.height, BLOCKSIZE, BLOCKSIZE)
        if DIR == 3:
            newpart = Rect(snake.x + snake.width, snake.y, BLOCKSIZE, BLOCKSIZE)
    elif TAIL == 1:
        if DIR == 0:
            newpart = Rect(snake.x, snake.y + snake.height*2, BLOCKSIZE, BLOCKSIZE)
        if DIR == 1:
            newpart = Rect(snake.x - snake.width*2, snake.y, BLOCKSIZE, BLOCKSIZE)
        if DIR == 2:
            newpart = Rect(snake.x, snake.y - snake.height*2, BLOCKSIZE, BLOCKSIZE)
        if DIR == 3:
            newpart = Rect(snake.x + snake.width*2, snake.y, BLOCKSIZE, BLOCKSIZE)
    else:
        if get_tail_dir(tail_parts) == 0:
            newpart = Rect(tail_parts[pos].x, tail_parts[pos].y + tail_parts[pos].height, BLOCKSIZE, BLOCKSIZE)
        if get_tail_dir(tail_parts) == 1:
            newpart = Rect(tail_parts[pos].x - tail_parts[pos].width, tail_parts[pos].y, BLOCKSIZE, BLOCKSIZE)
        if get_tail_dir(tail_parts) == 2:
            newpart = Rect(tail_parts[pos].x, tail_parts[pos].y - tail_parts[pos].height, BLOCKSIZE, BLOCKSIZE)
        if get_tail_dir(tail_parts) == 3:
            newpart = Rect(tail_parts[pos].x + tail_parts[pos].width, tail_parts[pos].y, BLOCKSIZE, BLOCKSIZE)
    
    tail_parts.append(newpart)

def move_tail(tail_parts, snake):
    global TAIL
    
    count = TAIL

    new_parts = tail_parts

    if TAIL > 0:

        if TAIL > 1:
            
            while 0 < count:
                count -= 1
                new_parts[count].x = tail_parts[count-1].x
                new_parts[count].y = tail_parts[count-1].y

        new_parts[0].x = snake.x
        new_parts[0].y = snake.y

    return new_parts
 
def get_tail_dir(tail_parts):
    global TAIL

    pos = TAIL - 1

    if tail_parts[pos].x == tail_parts[pos-1].x and tail_parts[pos].y == (tail_parts[pos-1].y + tail_parts[pos].height):
        return 0
    if tail_parts[pos].x == (tail_parts[pos-1].x - tail_parts[pos].width) and tail_parts[pos].y == tail_parts[pos-1].y:
        return 1
    if tail_parts[pos].x == tail_parts[pos-1].x and tail_parts[pos].y == (tail_parts[pos-1].y - tail_parts[pos].height):
        return 2
    if tail_parts[pos].x == (tail_parts[pos-1].x + tail_parts[pos].width) and tail_parts[pos].y == tail_parts[pos-1].y:
        return 3

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