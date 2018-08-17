import pygame
import random
from point import Point

W = 800
H = 600

ROW = 30
COL = 40

head = Point(row=int(ROW / 2), col=int(COL / 2))

bg_color = (255,255,200)

snake_color = (200,200,200)

head_color = (0,128,128)

food_color = (255,128,255)


#生成食物
def gen_food(snakes):
    '''
    :param snakes:蛇身所在位置组成的列表
    :return: 食物的坐标
    '''
    while 1:
        pos = Point(row=random.randint(0,ROW - 1), col=random.randint(0,COL - 1))

        #
        is_coll=False

        #是否跟蛇碰上了
        if head.row == pos.row and head.col == pos.col:
            is_coll = True

        #蛇身子
        for snake in snakes:
            if snake.row == pos.row and snake.col == pos.col:
                is_coll = True
                break

        if not is_coll:
            break

    return pos

#将点在图上渲染出来
def rect(window, point, color):
    cell_width = W/COL
    cell_height = H/ROW

    left = point.col*cell_width
    top = point.row*cell_height

    pygame.draw.rect(
        window, color,
        (left, top, cell_width, cell_height)
    )

def game(init_scores=0, direct='left', speed=20):
    '''初始方向为left
       蛇的长度为3
    '''
    # 初始化
    pygame.init()

    size = (W, H)

    window = pygame.display.set_mode(size)
    pygame.display.set_caption('贪吃蛇O(∩_∩)O')
    #游戏循环
    scores = init_scores
    snakes = [
        Point(row=head.row, col=head.col + 1),
        Point(row=head.row, col=head.col + 2),
        Point(row=head.row, col=head.col + 3)
    ]
    food = gen_food(snakes=snakes)
    quit = True
    clock = pygame.time.Clock()
    while quit:
      #处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = False
            elif event.type == pygame.KEYDOWN:
                if event.key == 273 or event.key == 119:
                    if direct == 'left' or direct == 'right':
                        direct = 'up'
                elif event.key == 274 or event.key == 115:
                    if direct == 'left' or direct == 'right':
                        direct = 'down'
                elif event.key == 276 or event.key == 97:
                    if direct == 'up' or direct == 'down':
                        direct = 'left'
                elif event.key == 275 or event.key == 100:
                    if direct == 'up' or direct == 'down':
                        direct = 'right'
                # print(event)

        #吃东西
        eat = (head.row == food.row and head.col == food.col)

        #重新产生食物
        if eat:
            print("分数+1")
            scores += 1
            if scores % 20  == 0:
                speed += 2          # 每20分为一个分界点,越来越快
            food = gen_food(snakes=snakes)

        #处理身子
        #1.把原来的头，插入到snakes的头上
        snakes.insert(0, head.copy())
        #2.把snakes的最后一个删掉
        if not eat:
            snakes.pop()

        #移动
        if direct == 'left':
            head.col -= 1
        elif direct == 'right':
            head.col += 1
        elif direct == 'up':
            head.row -= 1
        elif direct == 'down':
            head.row += 1

        #检测
        dead=False
        #撞墙会死
        # if head.col<0 or head.row<0 or head.col>=COL or head.row>=ROW:
        #     dead=True
        #撞墙不死
        if head.col<0:
            head.col = COL - 1
        if head.row<0:
            head.row = ROW - 1
        if head.col >= COL:
            head.col = 0
        if head.row >= ROW:
            head.row = 0


        #2.撞自己
        for snake in snakes:
            if head.col == snake.col and head.row == snake.row:
                dead = True
                break

        if dead:
            print('死了')
            quit = False
            print("您的最终分数为{}分".format(scores))

        #渲染——画出来
        #背景
        pygame.draw.rect(window, bg_color, (0,0,W,H))

        #蛇身，蛇头，食物
        for snake in snakes:
            rect(window, snake, snake_color)
        rect(window, head, head_color)
        rect(window, food, food_color)

        #将选然后的界面显示出来
        pygame.display.flip()

        #设置帧频

        clock.tick(speed)
    pygame.quit()
    return scores

if __name__ == '__main__':
    while True:
        game()
        input("回车开始新一局游戏")


