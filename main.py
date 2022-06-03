import pygame_menu
import pygame
import random
import sys
from pygame.locals import *


pygame.init()
pygame.display.set_caption("AirHockey by Grigoryev")

ic_w = 25
ic_h = 32
icon_img = pygame.image.load(f'./images/icon.PNG')
icon = pygame.transform.scale(icon_img, (ic_w, ic_h))
pygame.display.set_icon(icon)

pygame.mixer.music.load(f'./sound/gg.mp3')
pygame.mixer.music.set_volume(0.3)

width = 500
height = 600
size = (width, height)
screen = pygame.display.set_mode(size)

playing_field_images = pygame.image.load(f'./images/bg_playground.png')
playing_field = pygame.transform.scale(playing_field_images, (width, height))
rule_img = pygame.image.load(f'./images/Rule.png')
rule = pygame.transform.scale(rule_img, (width, height))

# Характеристики для первой клюшки
Pl1_width = 50
Pl1_height = 50
Pl1_dx = (width - Pl1_width) / 2
Pl1_dy = 30
Pl1_point = 0

Player1_img = pygame.image.load(f'./images/stick_blue.png')
Player1 = pygame.transform.scale(Player1_img, (Pl1_width, Pl1_height))

# Характеристики для второй клюшки
Pl2_width = 50
Pl2_height = 50
Pl2_dx = (width - Pl2_width) / 2
Pl2_dy = height - Pl2_height - 30
Pl2_point = 0

Player2_img = pygame.image.load(f'./images/stick_red.png')
Player2 = pygame.transform.scale(Player2_img, (Pl2_width, Pl2_height))


# Количество раундов
round = 0
max_round = 5

# Размеры целей
g_dim = (135, width - 135)

# Характеристики шайбы
p_width = 30
p_height = 30
puck_dx = (width - p_width) / 2
puck_dy = (height - p_height) / 2
puck_speed = 1

puck_img = pygame.image.load(f'./images/Puck_grey.png')
puck = pygame.transform.scale(puck_img, (p_width, p_height))

# Шайба будет двигаться в рандомном направлении
dx_dir = puck_speed * [-1, 1][random.randint(0, 1)]
dy_dir = puck_speed * [-1, 1][random.randint(0, 1)]


# Устанавливаем раунды
def set_rounds(_, meaning):
    global max_round
    max_round = meaning


def rule_game():

    while 1:

        screen.blit(rule_img, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
               if event.type == QUIT:
                      sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            break


# Начало работы приложения
def start_game():
    menu.disable()


menu = pygame_menu.Menu('Аэрохоккей', width, height, theme=pygame_menu.themes.THEME_ORANGE)
menu.add.selector('Выберите кол. раундов', [('3', 3), ('5', 5), ('10', 10)], onchange=set_rounds)
menu.add.button('Играть', start_game)
menu.add.button('Правила игры', rule_game)
menu.add.button('Выйти', pygame_menu.events.EXIT)

menu.mainloop(screen)


# Прорисовка очков
def draw_point():
    font = pygame.font.Font('freesansbold.ttf', 100)
    Pl1_text = font.render(str(Pl1_point), False, (200, 200, 200))
    Pl2_text = font.render(str(Pl2_point), False, (200, 200, 200))
    screen.blit(Pl1_text, ((width - Pl1_text.get_size()[0]) / 2, height / 2 - Pl1_text.get_size()[1] - 70))
    screen.blit(Pl2_text, ((width - Pl2_text.get_size()[0]) / 2, height / 2 + 80))


# Прорисовка победителя
def draw_winner(winner_text):
    overlap = pygame.Surface((width, height), pygame.SRCALPHA)
    overlap.fill((0, 0, 0, 150))
    screen.blit(overlap, (0, 0))
    font = pygame.font.Font('freesansbold.ttf', 50)
    text = font.render(winner_text, False, (200, 200, 200))
    screen.blit(text, ((width - text.get_size()[0]) / 2, (height - text.get_size()[1]) / 2))


# Перезагрузка игры
def reset_game():
    global puck_dx, puck_dy, Pl1_dx, Pl1_dy, Pl2_dx, Pl2_dy, dx_dir, dy_dir, puck_speed, round
    puck_dx = (width - 30) / 2
    puck_dy = (height - 30) / 2
    Pl1_dx = (width - 50) / 2
    Pl1_dy = 30
    Pl2_dx = (width - 50) / 2
    Pl2_dy = height - 50 - 30
    puck_speed = 1
    dx_dir = puck_speed * [-1, 1][random.randint(0, 1)]
    dy_dir = puck_speed * [-1, 1][random.randint(0, 1)]
    round += 1


# Начать заново игру
def restart_game():
    global Pl1_point, Pl2_point, puck_speed, round
    Pl1_point = 0
    Pl2_point = 0
    reset_game()
    round = 0


# ИГРА
run_game = True
timer = pygame.time.Clock()

pygame.mixer.music.play(-1)

while run_game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run_game = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and Pl1_dx >= 15:
        Pl1_dx += -5
    if keys[pygame.K_RIGHT] and Pl1_dx + Pl1_width <= width - 15:
        Pl1_dx += 5
    if keys[pygame.K_UP] and Pl1_dy >= 10:
        Pl1_dy += -5
    if keys[pygame.K_DOWN] and Pl1_dy + Pl1_height <= height / 2:
        Pl1_dy += 5
    if keys[pygame.K_a] and Pl2_dx >= 15:
        Pl2_dx += -5
    if keys[pygame.K_d] and Pl2_dx + Pl2_width <= width - 15:
        Pl2_dx += 5
    if keys[pygame.K_w] and Pl2_dy >= height / 2:
        Pl2_dy += -5
    if keys[pygame.K_s] and Pl2_dy + Pl2_height <= height - 10:
        Pl2_dy += 5

    # Столкновение шайбы с левой частью экрана
    if puck_dx <= 15:
        dx_dir = puck_speed

    # Столкновение шайбы с правой частью экрана
    if puck_dx + p_width >= width - 15:
        dx_dir = -puck_speed

    # Столкновение шайбы с верхней частью экрана
    if puck_dy <= 10:
        dy_dir = puck_speed

    # Столкновение шайбы с нижней частью экрана
    if puck_dy + p_width >= height - 10:
        dy_dir = -puck_speed

    # Столкновение с нижней частью экрана 1-го игрока
    if puck_dy <= Pl1_dy + Pl1_height <= puck_dy + p_height and Pl1_dx - p_width <= puck_dx <= Pl1_dx + Pl1_width:
        dy_dir = puck_speed
        puck_speed += 0.01

    # Столкновение с верхней частью экрана 1-го игрока
    if puck_dy <= Pl1_dy <= puck_dy + p_height and Pl1_dx - p_width <= puck_dx <= Pl1_dx + Pl1_width:
        dy_dir = -puck_speed
        puck_speed += 0.01

    # Столкновение с правой частью экрана 1-го игрока
    if puck_dx <= Pl1_dx + Pl1_width <= puck_dx + p_width and Pl1_dx - p_height <= puck_dy <= Pl1_dy + Pl1_height:
        dx_dir = puck_speed
        puck_speed += 0.01

    # Столкновение с левой частью экрана 1-го игрока
    if puck_dx <= Pl1_dx <= puck_dx + p_width and Pl1_dy - p_height <= puck_dy <= Pl1_dy + Pl1_height:
        dx_dir = -puck_speed
        puck_speed += 0.01

    # Столкновение с нижней частью экрана 2-го игрока
    if puck_dy <= Pl2_dy + Pl2_height <= puck_dy + p_height and Pl2_dx - p_width <= puck_dx <= Pl2_dx + Pl2_width:
        dy_dir = puck_speed
        puck_speed += 0.01

    # Столкновение с верхней частью экрана 2-го игрока
    if puck_dy <= Pl2_dy <= puck_dy + p_height and Pl2_dx - p_width <= puck_dx <= Pl2_dx + Pl2_width:
        dy_dir = -puck_speed
        puck_speed += 0.01

    # Столкновение с правой частью экрана 2-го игрока
    if puck_dx <= Pl2_dx + Pl2_width <= puck_dx + p_width and Pl2_dy - p_height <= puck_dy <= Pl2_dy + Pl2_height:
        dx_dir = puck_speed
        puck_speed += 0.01

    # Столкновение с левой частью экрана 2-го игрока
    if puck_dx <= Pl2_dx <= puck_dx + p_width and Pl2_dy - p_height <= puck_dy <= Pl2_dy + Pl2_height:
        dx_dir = -puck_speed
        puck_speed += 0.01

    # Игрок 1 забил
    if puck_dy <= 10 and g_dim[0] <= puck_dx <= g_dim[1]:
        Pl2_point += 1
        reset_game()

    # Игрок 2 забил
    if puck_dy + p_height >= height - 10 and g_dim[0] <= puck_dx <= g_dim[1]:
        Pl1_point += 1
        reset_game()

    puck_dx += dx_dir
    puck_dy += dy_dir

    screen.fill((0, 0, 0))
    screen.blit(playing_field, (0, 0))
    draw_point()
    screen.blit(Player1, (Pl1_dx, Pl1_dy))
    screen.blit(Player2, (Pl2_dx, Pl2_dy))
    screen.blit(puck, (puck_dx, puck_dy))

    # Процедура определения победителя
    if round == max_round:
        if Pl1_point > Pl2_point:
            draw_winner('Игрок 1 выиграл')
        elif Pl2_point > Pl1_point:
            draw_winner('Игрок 2 выиграл')
        else:
            draw_winner('Ничья')
        pygame.display.flip()
        pygame.time.wait(3000)
        restart_game()

    # Обновляет всю поверхность дисплея
    pygame.display.flip()

    timer.tick(60)

pygame.quit()

