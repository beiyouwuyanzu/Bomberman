import pygame
import sys
import random
import time
from player import Player
from explosion import Explosion
from enemy import Enemy
from algorithm import Algorithm
from spriteManager import  SpriteManager
import pygame_gui
from pygame_gui.elements.ui_text_entry_line import UITextEntryLine
from pygame.rect import Rect
from client import Client
import uuid

TILE_WIDTH = 40
TILE_HEIGHT = 40

WINDOW_WIDTH = 13 * TILE_WIDTH
WINDOW_HEIGHT = 13 * TILE_HEIGHT

BACKGROUND = (177 ,189, 105)


s = None
ui_manager = None
text_input = None
text_show = None

FPS = 60
show_path = True

clock = None

player = None
enemy_list = []
ene_blocks = []
bombs = []
explosions = []

grid = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

grass_img = None
block_img = None
box_img = None
bomb0_img = None
bomb1_img = None
bomb2_img = None
bomb3_img = None
explosion1_img = None
explosion2_img = None
explosion3_img = None

spm = None
bomb_top = None

client = None
bombcache = []

white = (255,255,255)
terrain_images = []
bomb_images = []
explosion_images = []

pygame.font.init()
font = pygame.font.SysFont('Bebas', 30)
TEXT_LOSE = font.render('GAME OVER', False, (0, 0, 0))
TEXT_WIN = font.render('WIN', False, (0, 0, 0))


hello_button = None

def game_init(path, player_alg, en1_alg, en2_alg, en3_alg, scale):

    global TILE_WIDTH
    global TILE_HEIGHT
    TILE_WIDTH = scale
    TILE_HEIGHT = scale

    global bomb_top
    global spm
    spm = SpriteManager(scale)
    # bomb_top = spm.get("bomb_top")

    global font
    font = pygame.font.SysFont('Bebas', scale)

    global show_path
    show_path = path



    global s, ui_manager
    s = pygame.display.set_mode((17 * TILE_WIDTH, 13 * TILE_HEIGHT))
    ui_manager = pygame_gui.UIManager((17 * TILE_WIDTH, 13 * TILE_HEIGHT), './theme.json')
    pygame.display.set_caption('custom_bomb')

    global hello_button
    hello_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((760, 675), (100, 50)),
                                             text='大家好 Say Hello',
                                             manager=ui_manager)
    global text_input
    text_input = UITextEntryLine(relative_rect=Rect(750, 600, 200, 50),  manager=ui_manager)

    global text_show 
    text_show = pygame_gui.elements.ui_text_box.UITextBox(html_text = "消息记录打印",
        relative_rect = Rect(750, 400, 200, 200), manager = ui_manager)

    global client
    client = Client(box = text_show)

    global clock
    clock = pygame.time.Clock()

    global enemy_list
    global ene_blocks
    global player

    enemy_list = []
    ene_blocks = []
    global explosions
    global bombs
    bombs.clear()
    explosions.clear()

    player = Player(W = TILE_WIDTH, H = TILE_HEIGHT)
    player.uid = str(uuid.uuid1())

    if en1_alg is not Algorithm.NONE:
        en1 = Enemy(11, 11, en1_alg)
        en1.load_animations('1', scale)
        enemy_list.append(en1)
        ene_blocks.append(en1)

    if en2_alg is not Algorithm.NONE:
        en2 = Enemy(1, 11, en2_alg)
        en2.load_animations('2', scale)
        enemy_list.append(en2)
        ene_blocks.append(en2)

    if en3_alg is not Algorithm.NONE:
        en3 = Enemy(11, 1, en3_alg)
        en3.load_animations('3', scale)
        enemy_list.append(en3)
        ene_blocks.append(en3)

    if player_alg is Algorithm.PLAYER:
        player.load_animations(scale)
        ene_blocks.append(player)
    elif player_alg is not Algorithm.NONE:
        en0 = Enemy(1, 1, player_alg)
        en0.load_animations('', scale)
        enemy_list.append(en0)
        ene_blocks.append(en0)
        player.life = False
    else:
        player.life = False

    global grass_img
    grass_img = pygame.image.load('images/terrain/stand.png')
    grass_img = pygame.transform.scale(grass_img, (TILE_WIDTH, TILE_HEIGHT))
    global block_img
    block_img = pygame.image.load('images/terrain/wall2.png')
    block_img = pygame.transform.scale(block_img, (TILE_WIDTH, TILE_HEIGHT))
    global box_img
    box_img = pygame.image.load('images/terrain/box1.png')
    box_img = pygame.transform.scale(box_img, (TILE_WIDTH, TILE_HEIGHT))
    global bomb0_img
    bomb0_img = pygame.image.load('images/bomb/bomb12_stand_0_0.png')
    bomb0_img = pygame.transform.scale(bomb0_img, (TILE_WIDTH, TILE_HEIGHT))
    global bomb1_img
    bomb1_img = pygame.image.load('images/bomb/bomb12_stand_0_1.png')
    bomb1_img = pygame.transform.scale(bomb1_img, (TILE_WIDTH, TILE_HEIGHT))
    global bomb2_img
    bomb2_img = pygame.image.load('images/bomb/bomb12_stand_0_2.png')
    bomb2_img = pygame.transform.scale(bomb2_img, (TILE_WIDTH, TILE_HEIGHT))
    global bomb3_img
    bomb3_img = pygame.image.load('images/bomb/bomb12_stand_0_3.png')
    bomb3_img = pygame.transform.scale(bomb3_img, (TILE_WIDTH, TILE_HEIGHT))
    global explosion1_img
    explosion1_img = pygame.image.load('images/explosion/1.png')
    explosion1_img = pygame.transform.scale(explosion1_img, (TILE_WIDTH, TILE_HEIGHT))
    global explosion2_img
    explosion2_img = pygame.image.load('images/explosion/2.png')
    explosion2_img = pygame.transform.scale(explosion2_img, (TILE_WIDTH, TILE_HEIGHT))
    global explosion3_img
    explosion3_img = pygame.image.load('images/explosion/3.png')
    explosion3_img = pygame.transform.scale(explosion3_img, (TILE_WIDTH, TILE_HEIGHT))

    global terrain_images
    terrain_images = [grass_img, block_img, box_img, grass_img]
    global bomb_images
    bomb_images = [bomb0_img, bomb1_img, bomb2_img, bomb3_img]
    global explosion_images
    explosion_images = [explosion1_img, explosion2_img, explosion3_img]

    main()

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def debug(row, info):
    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(info, largeText)
    TextRect.center = (15 * TILE_WIDTH, (row) * TILE_HEIGHT)
    s.blit(TextSurf, TextRect)

def draw():
    s.fill(BACKGROUND)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            s.blit(terrain_images[grid[i][j]], (i * TILE_WIDTH, j * TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH))

    for x in bombs:
        s.blit(bomb_images[x.frame], (x.posX * TILE_WIDTH, x.posY * TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH))

    for y in explosions:

        for x in y.sectors:
            # s.blit(explosion_images[y.frame], (x[0] * TILE_WIDTH, x[1] * TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH))
            # print(x[0], x[1])
            # print(y.detail)
            s.blit(spm.explore_img(y.detail[x[0]][x[1]], y.frame), (x[0] * TILE_WIDTH, x[1] * TILE_HEIGHT, TILE_HEIGHT, TILE_WIDTH))
    if player.life:
        # print(*player.get_pic_coor())
        s.blit(player.allpic, *player.get_pic_coor())
        pygame.draw.rect(s, (198, 226, 255), [player.posX * TILE_WIDTH, player.posY * TILE_HEIGHT - 24, player.width, player.height], 1 )
        # 给当前任务画框
        pygame.draw.rect(s, (255, 250, 0, 240), [player.tempx * TILE_WIDTH, player.tempy * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT], 1 )
    else:
        # print(player.death_tm, player.posX * TILE_WIDTH, player.posY * TILE_HEIGHT)
        s.blit(spm.get("status", int(player.death_tm  / 300 % 5)), (player.posX * TILE_WIDTH, player.posY * TILE_HEIGHT))
        
    # print(Player)

    # 打印debug文字
    text_x = f"x={round(player.posX, 2)}"
    text_y = f"y={round(player.posY, 2)}"
    
    # debug(1, text_x)
    # debug(2, text_y)
    debug(1, f"fps = {str(int(clock.get_fps()))}")
    debug(3, f"locx  = {player.tempx }")
    debug(4, f"locy  = {player.tempy }")
    # debug(5, f"picx={round(player.posX * 10, 2)}")
    # debug(6, f"picy={round(player.posY * 10, 2)}")

    

    for en in enemy_list:
        if en.life:
            s.blit(en.animation[en.direction][en.frame],
                   (en.posX * (TILE_WIDTH / 4), en.posY * (TILE_HEIGHT / 4), TILE_WIDTH, TILE_HEIGHT))
            if show_path:
                if en.algorithm == Algorithm.DFS:
                    for sek in en.path:
                        pygame.draw.rect(s, (255, 0, 0, 240), [sek[0] * TILE_WIDTH, sek[1] * TILE_HEIGHT, TILE_WIDTH, TILE_WIDTH], 1)
                else:
                    for sek in en.path:
                        pygame.draw.rect(s, (255, 0, 255, 240), [sek[0] * TILE_WIDTH, sek[1] * TILE_HEIGHT, TILE_WIDTH, TILE_WIDTH], 1)

    ui_manager.update(0.02)
    ui_manager.draw_ui(s)
    pygame.display.update()


def generate_map():

    for i in range(1, len(grid) - 1):
        for j in range(1, len(grid[i]) - 1):
            if grid[i][j] != 0:
                continue
            elif (i < 3 or i > len(grid) - 4) and (j < 3 or j > len(grid[i]) - 4):
                continue
            if random.randint(0, 9) < 7:
                grid[i][j] = 2

    return


def main():
    # pygame.key.set_repeat(1,1)
    # print("get_setting", pygame.key.get_repeat())
    generate_map()
    last_send_tm = 0
    while player.life or player.death_tm < 100000:
        dt = clock.tick(FPS)
        if not player.life:
            player.death_tm += dt
        for en in enemy_list:
            en.make_move(grid, bombs, explosions, ene_blocks)
        keys = pygame.key.get_pressed()
        # print(time.time() ,keys)
        temp = player.direction
        movement = False

        

        if keys[pygame.K_DOWN]:
            # print(time.time(), "down")
            temp = 0
            player.move(0, 1, grid, ene_blocks)
            movement = True
        elif keys[pygame.K_RIGHT]:
            # print(time.time(), "r")
            temp = 1
            player.move(1, 0, grid, ene_blocks)
            movement = True
        elif keys[pygame.K_UP]:
            # print(time.time(), "up")
            temp = 2
            player.move(0, -1, grid, ene_blocks)
            movement = True
        elif keys[pygame.K_LEFT]:
            # print(time.time(), "left")
            temp = 3
            player.move(-1, 0, grid, ene_blocks)
            movement = True
        if temp != player.direction:
            player.frame = 0
            player.direction = temp
        if movement:
            player.frame = (player.frame + 0.1) % 4

        draw()
        for e in pygame.event.get():

            if e.type == pygame_gui.UI_BUTTON_PRESSED:
              if e.ui_element == hello_button:
                  print('Hello World!')


            if e.type == pygame.USEREVENT:
                if e.user_type == pygame_gui.UI_TEXT_ENTRY_FINISHED:
                    if e.ui_element == text_input:
                        
                        entered_text = e.text
                        print("input_text", entered_text)
                        client.send({"chat":entered_text })
                        text_input.set_text("")

            if e.type == pygame.QUIT:
                sys.exit(0)
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_SPACE:
                    if player.bomb_limit == 0:
                        continue
                    temp_bomb = player.plant_bomb(grid)
                    bombs.append(temp_bomb)
                    grid[temp_bomb.posX][temp_bomb.posY] = 3
                    player.bomb_limit -= 1

                    global bombcache
                    bombcache.append([temp_bomb.posX, temp_bomb.posY])

            ui_manager.process_events(e)
        update_bombs(dt)

        # 更新发送数据
        last_send_tm += dt
        if last_send_tm > 2000:
            data = get_update_info(movement)
            client.send(data)
            last_send_tm %= 2000


    game_over()

def get_update_info(movement):
    data = {}
    data["protocol"] = "player_status"
    data["pos"] = [player.posX, player.posY]
    data["movement"] = movement
    data["direction"] = player.direction
    data["uuid"] = player.uid
    global bombcache 
    data["bombs"] = bombcache[:]
    bombcache.clear()

    return data

def update_bombs(dt):
    for b in bombs:
        b.update(dt)
        if b.time < 1:
            b.bomber.bomb_limit += 1
            grid[b.posX][b.posY] = 0
            exp_temp = Explosion(b.posX, b.posY, b.range)
            exp_temp.explode(grid, bombs, b)
            exp_temp.clear_sectors(grid)
            explosions.append(exp_temp)
    if player not in enemy_list:
        player.check_death(explosions)
    for en in enemy_list:
        en.check_death(explosions)
    for e in explosions:
        e.update(dt)
        if e.time < 1:
            explosions.remove(e)


def game_over():

    while True:
        dt = clock.tick(15)
        update_bombs(dt)
        count = 0
        winner = ""
        for en in enemy_list:
            en.make_move(grid, bombs, explosions, ene_blocks)
            if en.life:
                count += 1
                winner = en.algorithm.name
        if count == 1:
            draw()
            textsurface = font.render(winner + " wins", False, (0, 0, 0))
            font_w = textsurface.get_width()
            font_h = textsurface.get_height()
            s.blit(textsurface, (s.get_width() // 2 - font_w//2,  s.get_height() // 2 - font_h//2))
            pygame.display.update()
            time.sleep(2)
            break
        if count == 0:
            draw()
            textsurface = font.render("Draw", False, (0, 0, 0))
            font_w = textsurface.get_width()
            font_h = textsurface.get_height()
            s.blit(textsurface, (s.get_width() // 2 - font_w//2, s.get_height() // 2 - font_h//2))
            pygame.display.update()
            time.sleep(2)
            break
        draw()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit(0)
    explosions.clear()
    enemy_list.clear()
    ene_blocks.clear()
    client.close()
