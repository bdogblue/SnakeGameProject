from pickle import TRUE
import pygame, sys, random

from pygame.locals import *

pygame.font.init()

WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH+120, HEIGHT+120))
pygame.display.set_caption('Snake')

RED = (255, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GREEN = (21, 89, 12)

SCORE_FONT = pygame.font.SysFont('comicsans', 40)
BORDER = pygame.Rect(60, 60, WIDTH, HEIGHT)

FPS = 2
BLOCKSIZE = 20

snake = pygame.Rect(260, 200, BLOCKSIZE, BLOCKSIZE)
meal = pygame.Rect(80, 80, BLOCKSIZE, BLOCKSIZE)

# need a new game over screen with option to start again

def draw_window(tail_parts, TAIL):
    WIN.fill(GREEN)
    pygame.draw.rect(WIN, BLACK, BORDER)
    pygame.draw.rect(WIN, RED, snake)
    pygame.draw.rect(WIN, BLUE, meal)

    score_text = SCORE_FONT.render("Score: " + str(TAIL), 1, BLACK)
    WIN.blit(score_text, (60, 30))

    for tail in tail_parts:
        pygame.draw.rect(WIN, RED, tail)

    pygame.display.update()

def snake_handle_direction(keys_pressed, snake, tail_parts, TAIL, DIR):
    if TAIL <= 0:
        if keys_pressed[pygame.K_LEFT]:  # LEFT
            return 3
        if keys_pressed[pygame.K_RIGHT]:  # RIGHT
            return 1
        if keys_pressed[pygame.K_UP]:  # UP
            return 0
        if keys_pressed[pygame.K_DOWN]:  # DOWN
            return 2
        return DIR
    else:
        if keys_pressed[pygame.K_LEFT] and DIR != 1:  # LEFT
            return 3
        if keys_pressed[pygame.K_RIGHT] and DIR != 3:  # RIGHT
            return 1
        if keys_pressed[pygame.K_UP] and DIR != 2:  # UP
            return 0
        if keys_pressed[pygame.K_DOWN] and DIR != 0:  # DOWN
            return 2
        return DIR

def snake_handle_movement(snake, tail_parts, TAIL, DIR):
    tail_parts = move_tail(tail_parts, snake, TAIL)
    
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

def move_meal(meal, snake, tail_parts):
    find = True

    while find:
        x = random.randrange(60, (WIDTH+60)-meal.width, BLOCKSIZE)
        y = random.randrange(60, (HEIGHT+60)-meal.height, BLOCKSIZE)
        
        if ((x != meal.x and y != meal.y) and
            (is_over_tail(tail_parts, meal.x, meal.y) == False) and
            (x != snake.x and y != snake.y) and 
            (x != snake.x and y != (snake.y - BLOCKSIZE)) and 
            (x != (snake.x + BLOCKSIZE) and y != snake.y) and 
            (x != snake.x and y != (snake.y + BLOCKSIZE)) and 
            (x != (snake.x - BLOCKSIZE) and y != snake.y)):
            
            meal.x = x
            meal.y = y
            find = False

def is_over_tail(tail_parts, x, y):
    found = False
    for tail in tail_parts:
        if tail.x == x and tail.y == y:
            found = True
    return found

def add_tail(tail_parts, snake, TAIL, DIR):
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
        if get_tail_dir(tail_parts, TAIL) == 0:
            newpart = Rect(tail_parts[pos].x, tail_parts[pos].y + tail_parts[pos].height, BLOCKSIZE, BLOCKSIZE)
        if get_tail_dir(tail_parts, TAIL) == 1:
            newpart = Rect(tail_parts[pos].x - tail_parts[pos].width, tail_parts[pos].y, BLOCKSIZE, BLOCKSIZE)
        if get_tail_dir(tail_parts, TAIL) == 2:
            newpart = Rect(tail_parts[pos].x, tail_parts[pos].y - tail_parts[pos].height, BLOCKSIZE, BLOCKSIZE)
        if get_tail_dir(tail_parts, TAIL) == 3:
            newpart = Rect(tail_parts[pos].x + tail_parts[pos].width, tail_parts[pos].y, BLOCKSIZE, BLOCKSIZE)
    
    tail_parts.append(newpart)

def move_tail(tail_parts, snake, TAIL):
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
 
def get_tail_dir(tail_parts, TAIL):
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

    Direction = 1
    Tail = 0

    clock = pygame.time.Clock()

    tail_parts = []

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys_pressed = pygame.key.get_pressed()

        Direction = snake_handle_direction(keys_pressed, snake, tail_parts, Tail, Direction)
        
        snake_handle_movement(snake, tail_parts, Tail, Direction)
        
        if snake.colliderect(meal):
            add_tail(tail_parts, snake, Tail, Direction)
            move_meal(meal, snake, tail_parts)
            Tail += 1

        for tail in tail_parts:
            if snake.x == tail.x and snake.y == tail.y:
                run = False

        # Check if going off screen
        if snake.x < 60 or snake.x > (WIDTH+60)-snake.width or snake.y < 60 or snake.y > (HEIGHT+60)-snake.height:
            break

        draw_window(tail_parts, Tail)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()