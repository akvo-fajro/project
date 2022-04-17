import pygame
import random
import time

# define constant
FPS = 60
WINDOWS_WIDTH = 400
WHINDOWS_HEIGHT = 600
GIRD_WIDTH = 10
GRID_LEFT = 100
GRID_TOP = 100


# initial
pygame.init()
pygame.display.set_caption('Tetris_With_Pygame')
windows = pygame.display.set_mode((WINDOWS_WIDTH,WHINDOWS_HEIGHT))
clock = pygame.time.Clock()
running = True
random.seed(int(time.time()))

# grid
grid = [0 for _ in range(200)]

# tetromino
# itetromino sky blue
itetromino = [
    [GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH+2,GIRD_WIDTH+3],
    [2,GIRD_WIDTH+2,GIRD_WIDTH*2+2,GIRD_WIDTH*3+2],
    [GIRD_WIDTH*2,GIRD_WIDTH*2+1,GIRD_WIDTH*2+2,GIRD_WIDTH*2+3],
    [1,GIRD_WIDTH+1,GIRD_WIDTH*2+1,GIRD_WIDTH*3+1]
]
itetromino_color = (37,252,255)
# jtetromino blue
jtetromino = [
    [0,GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH+2],
    [1,2,GIRD_WIDTH+1,GIRD_WIDTH*2+1],
    [GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH+2,GIRD_WIDTH*2+2],
    [1,GIRD_WIDTH+1,GIRD_WIDTH*2,GIRD_WIDTH*2+1]
]
jtetromino_color = (37,50,255)
# ltetromino orange
ltetromino = [
    [2,GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH+2],
    [1,GIRD_WIDTH+1,GIRD_WIDTH*2+1,GIRD_WIDTH*2+2],
    [GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH+2,GIRD_WIDTH*2],
    [0,1,GIRD_WIDTH+1,GIRD_WIDTH*2+1]
]
ltetromino_color = (255,173,37)
# otetromino yellow
otetromino = [
    [1,2,GIRD_WIDTH+1,GIRD_WIDTH+2],
    [1,2,GIRD_WIDTH+1,GIRD_WIDTH+2],
    [1,2,GIRD_WIDTH+1,GIRD_WIDTH+2],
    [1,2,GIRD_WIDTH+1,GIRD_WIDTH+2]
]
otetromino_color = (255,248,37)
# stetromino green
stetromino = [
    [1,2,GIRD_WIDTH,GIRD_WIDTH+1],
    [1,GIRD_WIDTH+1,GIRD_WIDTH+2,GIRD_WIDTH*2+2],
    [GIRD_WIDTH+1,GIRD_WIDTH+2,GIRD_WIDTH*2,GIRD_WIDTH*2+1],
    [0,GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH*2+1]
]
stetromino_color = (71,255,37)
# ttetromino purple
ttetromino = [
    [1,GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH+2],
    [1,GIRD_WIDTH+1,GIRD_WIDTH+2,GIRD_WIDTH*2+1],
    [GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH+2,GIRD_WIDTH*2+1],
    [1,GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH*2+1]
]
ttetromino_color = (221,37,255)
# ztetromino red
ztetromino = [
    [0,1,GIRD_WIDTH+1,GIRD_WIDTH+2],
    [2,GIRD_WIDTH+1,GIRD_WIDTH+2,GIRD_WIDTH*2+1],
    [GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH*2+1,GIRD_WIDTH*2+2],
    [1,GIRD_WIDTH,GIRD_WIDTH+1,GIRD_WIDTH*2]
]
ztetromino_color = (255,37,37)
tetromino = {
    'i':itetromino,
    'j':jtetromino,
    'l':ltetromino,
    'o':otetromino,
    's':stetromino,
    't':ttetromino,
    'z':ztetromino
}
tetromino_color = {
    'i':itetromino_color,
    'j':jtetromino_color,
    'l':ltetromino_color,
    'o':otetromino_color,
    's':stetromino_color,
    't':ttetromino_color,
    'z':ztetromino_color
}
all_tetromino_type = ['i','j','l','o','s','t','z']
all_tetromino_type_weights = [2,4,4,3,5,4,5]

def draw_grid(surf,grid):
    for i in range(200):
        if grid[i] == 0:
            pygame.draw.rect(surf,(255,255,255),((i%GIRD_WIDTH)*20 + GRID_LEFT,(i//GIRD_WIDTH)*20 + GRID_TOP,20,20),0)
            continue
        pygame.draw.rect(surf,tetromino_color[grid[i]],((i%GIRD_WIDTH)*20 + GRID_LEFT,(i//GIRD_WIDTH)*20 + GRID_TOP,20,20),0)

def draw_block(surf,blocktype,blockposition,blockrotate):
    for i in tetromino[blocktype][blockrotate]:
        pygame.draw.rect(surf,tetromino_color[blocktype],(((i + blockposition)%GIRD_WIDTH)*20 + GRID_LEFT,((i + blockposition)//GIRD_WIDTH)*20 + GRID_TOP,20,20),0)

def check_block_in(blocktype,blockposition,blockrotate,grid):
    for i in tetromino[blocktype][blockrotate]:
        if (i + blockposition) >= 200:
            return False
        if grid[i + blockposition] != 0:
            return False
    return True

def check_can_right(blocktype,blockposition,blockrotate,grid):
    for i in tetromino[blocktype][blockrotate]:
        if (i + blockposition) % GIRD_WIDTH == 9:
            return False
    return check_block_in(blocktype,blockposition + 1,blockrotate,grid)

def check_can_left(blocktype,blockposition,blockrotate,grid):
    for i in tetromino[blocktype][blockrotate]:
        if (i + blockposition) % GIRD_WIDTH == 0:
            return False
    return check_block_in(blocktype,blockposition - 1,blockrotate,grid)

def check_can_rotate(blocktype,blockposition,blockrotate,grid):
    for i in tetromino[blocktype][(blockrotate + 1)%4]:
        if (i%GIRD_WIDTH + blockposition%GIRD_WIDTH) >= GIRD_WIDTH:
            return False
    return check_block_in(blocktype,blockposition,(blockrotate+1)%4,grid)

def check_line_in_grid(grid):
    delete_line = []
    for i in range(20):
        check = True
        for j in range(10):
            if grid[i*10+j] == 0:
                check = False
                break
        if check == True:
            delete_line.append(i)
    delete_line.sort()
    for i in delete_line:
        if i == 0:
            for j in range(10):
                grid[j] = 0
            continue
        for j in range(i-1,-1,-1):
            for k in range(10):
                grid[(j+1)*10 + k] = grid[j*10 + k]
        for j in range(10):
            grid[j] = 0
    return grid


def update_game(blocktype,blockposition,blockrotate,grid,count,running):
    if count == 31:
        count = 0
        if check_block_in(blocktype,blockposition + 10,blockrotate,grid):
            blockposition += 10
        else:
            for i in tetromino[blocktype][blockrotate]:
                grid[i+blockposition] = blocktype
            grid = check_line_in_grid(grid)
            blocktype = random.choices(all_tetromino_type,weights=all_tetromino_type_weights,k=1)[0]
            blockposition = 3
            blockrotate = 0
            running = check_block_in(blocktype,blockposition,blockrotate,grid)
            return (blocktype,blockposition,blockrotate,grid,count,running)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if (event.key == pygame.K_RIGHT) and (check_can_right(blocktype,blockposition,blockrotate,grid)):
                blockposition += 1
            if (event.key == pygame.K_LEFT) and (check_can_left(blocktype,blockposition,blockrotate,grid)):
                blockposition -= 1
            if (event.key == pygame.K_UP) and (check_can_rotate(blocktype,blockposition,blockrotate,grid)):
                blockrotate = (blockrotate + 1) % 4
                pass
            if event.key == pygame.K_SPACE:
                for i in range(20):
                    if not check_block_in(blocktype,blockposition + i*10,blockrotate,grid):
                        blockposition += (i - 1)*10
                        break
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_DOWN]:
        if check_block_in(blocktype,blockposition + 10,blockrotate,grid):
            blockposition += 10
        else:
            for i in tetromino[blocktype][blockrotate]:
                grid[i+blockposition] = blocktype
            grid = check_line_in_grid(grid)
            blocktype = random.choices(all_tetromino_type,weights=all_tetromino_type_weights,k=1)[0]
            blockposition = 3
            blockrotate = 0
            running = check_block_in(blocktype,blockposition,blockrotate,grid)
            return (blocktype,blockposition,blockrotate,grid,count,running)
    return (blocktype,blockposition,blockrotate,grid,count,running)

# game loop
count = 0
tetromino_position = 3
tetromino_rotate = 0
tetromino_type = random.choices(all_tetromino_type,weights=all_tetromino_type_weights,k=1)[0]
while running:
    clock.tick(FPS)
    count += 1

    # update game
    (tetromino_type,tetromino_position,tetromino_rotate,grid,count,running) = update_game(tetromino_type,tetromino_position,tetromino_rotate,grid,count,running)

    # display interface
    pygame.display.update()
    draw_grid(windows,grid)
    draw_block(windows,tetromino_type,tetromino_position,tetromino_rotate)


pygame.quit()
