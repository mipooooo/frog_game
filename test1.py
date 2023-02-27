import random
import sys
import pygame
from pygame.locals import *


size = width, height = 600, 499
elev = height * 0.8
imgs = {}
fps = 32
kuv = 'kubch.png'
liana = 'liana.png'
bg = 'back.jpeg'
frog = 'rob.png'
fg = 'water.png'



def flappygame():
    score = 0
    x = width // 5
    y = width // 2
    ground = 0
    my_height = 100
    pipeUP = Pipe()
    pipeDown = Pipe(1)
    pipeUP2 = Pipe()
    pipeDown2 = Pipe(1)
    pipe_up1 = {'x': width + 300 - my_height, 'y':pipeUP['y']}
    pipe_up2 = {'x': width + 200 - my_height + (width//2), 'y':pipeUP2['y']}
    pipe_down1 = {'x': width + 300 - my_height, 'y':pipeDown['y']}
    pipe_down2 = {'x': width + 300 - my_height+(width//2), 'y':pipeDown2['y']}
    pipeup = [pipe_up1, pipe_up2]
    pipedown = [pipe_down1, pipe_down2]
    
    pipe_speed_x = -2
    f_speed_y = -6
    f_sp_mn_y = -5
    f_sp_mx_y = 5
    f_acc_y = 1

    f_speed_flap = -8
    f_flapped = False
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                if y > 0:
                    f_speed_y = f_speed_flap
                    f_flapped = True
        player = x + imgs['flappy'].get_width() // 2
        for pipe in pipeup:
            pipe_pos1 = pipe_up1['x'] + imgs['pipe'][0].get_width()
            if pipe_pos1 < player < pipe_pos1 + 4:
                score += 1

        game_over =  GameOver(x, y, pipeup, pipedown)
        if game_over:
            print(f'Игра окончена. Ваш счет: {score}')
            return
        if f_speed_y < f_sp_mx_y and not f_flapped:
            f_speed_y += f_acc_y

        if f_flapped:
            f_flapped = False
        player_h = imgs['flappy'].get_height()
        y += min(f_speed_y, elev - y - player_h)

        for upperPipe, lowerPipe in zip(pipeup, pipedown):
            upperPipe['x'] += pipe_speed_x
            lowerPipe['x'] += pipe_speed_x

        if 0 < pipeup[0]['x'] < 5:
            newpipe_up = Pipe()
            newpipe_down = Pipe(1)
            pipeup.append(newpipe_up)
            pipedown.append(newpipe_down)

        if pipeup[0]['x'] < -imgs['pipe'][0].get_width():
            pipeup.pop(0)
            pipedown.pop(0)

        screen.blit(imgs['back'], (0, 0))
        for upperPipe, lowerPipe in zip(pipeup, pipedown):
            screen.blit(imgs['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(imgs['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
        screen.blit(imgs['fg'], (ground, elev))
        screen.blit(imgs['flappy'], (x, y))

        numbers = [int(x) for x in list(str(score))]
        width2 = 0
        for num in numbers:
            width2 += imgs['score'][num].get_width()
        Xa = (width - width2)//1.1
        for num in numbers:
            screen.blit(imgs['score'][num],(Xa, width*0.02))
            Xa += imgs['score'][num].get_width()
        pygame.display.update()
        fps_clock.tick(fps)


def GameOver(x, y, pipeup, pipedown):
    if y > elev - 50 or y < 0:
        return True
    for pipe in pipeup:
        pipe_height = imgs['pipe'][0].get_height()
        if (y < pipe_height + pipe['y'] and abs(x - pipe['x']) < imgs['pipe'][0].get_width()):
            return True
    for pipe1 in pipedown:
        if (y + imgs['flappy'].get_height() > pipe1['y']) and abs(x - pipe['x']) < imgs['pipe'][0].get_width():
            return True
    return False

def Pipe(k=0):
    a = height/3
    pipeHeight = imgs['pipe'][0].get_height()
    y2 = a + random.randrange(0, int(height - imgs['fg'].get_height() - 1.2 * a))
    pipeX = width + 10
    y1 = pipeHeight - y2 + a
    pipe_up = {'x': pipeX, 'y': -y1}
    pipe_down = {'x': pipeX, 'y': y2}
    if k == 1:
        return pipe_down
    return pipe_up

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((size))
    fps_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Frog')

    imgs['score'] = (
		pygame.image.load('0.png'),
		pygame.image.load('1.png'),
		pygame.image.load('2.png'),
		pygame.image.load('3.png'),
		pygame.image.load('4.png'),
		pygame.image.load('5.png'),
		pygame.image.load('6.png'),
		pygame.image.load('7.png'),
		pygame.image.load('8.png'),
		pygame.image.load('9.png')
	)
    imgs['flappy'] = pygame.transform.scale(pygame.image.load(frog).convert_alpha(), (50, 40))
    imgs['fg'] = pygame.transform.scale(pygame.image.load(fg).convert_alpha(), (600, 100))
    imgs['back'] = pygame.image.load(bg).convert_alpha()
    imgs['pipe'] = pygame.transform.scale(pygame.image.load(liana).convert_alpha(), (52, 300)), pygame.transform.scale(pygame.image.load(kuv).convert_alpha(), (80, 300))
    print('Для того, чтобы начать игру, нажмите пробел')
    print('Для того, чтобы поднять жабу вверх нажимайте пробел')
    print('При столкновении с лианами, водой, верхней границей и кувшинками игра завершится')
    while True:
        x = height // 5
        y = height - imgs['flappy'].get_height()
        ground = 0
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif  event.type == KEYDOWN and event.key == K_SPACE:
                    flappygame()
                else:
                    screen.blit(imgs['back'], (0, 0))
                    screen.blit(imgs['flappy'],(x, y))
                    screen.blit(imgs['fg'], (ground, elev))
                    pygame.display.update()
                    fps_clock.tick(fps)



