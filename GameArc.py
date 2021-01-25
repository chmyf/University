import pygame
from random import randrange as rnd

WIDTH, HEIGHT = 1200, 800
FPS = 60
POINTS = 0
BONUS_SPEED_BOOST = rnd(29, 39)

# платформа
paddle_H = 35
paddle_w = 330
paddle_s = 15
paddle = pygame.Rect(WIDTH // 2 - paddle_w // 2, HEIGHT - paddle_H - 10, paddle_w, paddle_H)
#ball
ball_rad = 20
ball_s = 4
ball_rect = int(ball_rad * 2 ** 0.5)
ball = pygame.Rect(rnd(ball_rect, WIDTH - ball_rect), HEIGHT//2, ball_rect, ball_rect)
dx, dy = 1, -1
# blocks settings
block_list = [pygame.Rect(10 + 120 * i, 10 + 70 * j, 100, 50) for i in range(10) for j in range(4)]
color_list = [(rnd(30, 256), rnd(30, 256), rnd(30, 256)) for i in range(10) for j in range(4)]

pygame.init()
sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# backgound
img = pygame.image.load('1.jpg').convert()

def detect_collis(dx, dy, ball, rect):
    if dx > 0:
        delta_x = ball.right - rect.left
    else:
        delta_x = rect.right - ball.left
    if dy > 0:
        delta_y = ball.bottom - rect.top
    else:
        delta_y = rect.bottom - ball.top

    if abs(delta_x - delta_y) < 10:
        dx, dy = -dx, -dy
    elif delta_x > delta_y:
        dy = -dy
    elif delta_y > delta_x:
        dx = -dx
    return dx, dy

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    sc.blit(img, (0,0))
    # print points
    # map
    [pygame.draw.rect(sc, color_list[color], block) for color, block in enumerate(block_list)]
    pygame.draw.rect(sc, pygame.Color('yellow'), paddle)
    pygame.draw.circle(sc, pygame.Color('white'), ball.center, ball_rad)

    # moove ball
    ball.x += ball_s * dx
    ball.y += ball_s * dy
    # колизия с боками
    if ball.centerx < ball_rad or ball.centerx > WIDTH - ball_rad:
        dx = -dx
    # collis top
    if ball.centery < ball_rad:
        dy = -dy
    # соприкосновение с платформой
    if ball.colliderect(paddle) and dy > 0:
        dx, dy = detect_collis(dx, dy, ball, paddle)
    #collis blocks
    hit_index = ball.collidelist(block_list)
    if hit_index != -1:
        if hit_index == BONUS_SPEED_BOOST:
            FPS *= 2
            hit_rect.inflate_ip(ball.width * 3, ball.height * 3)
            pygame.draw.rect(sc, hit_color, hit_rect)
        POINTS += 100
        hit_rect = block_list.pop(hit_index)
        hit_color = color_list.pop(hit_index)
        dx, dy = detect_collis(dx, dy, ball, hit_rect)
        # увеличение скорости
        FPS += 3
    # game end
    if ball.bottom > HEIGHT:
        print('GAME OVER')
        exit()
    elif not len(block_list):
        print('WIN')
        exit()
    # управление платформой
    key = pygame.key.get_pressed()
    if key[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= paddle_s
    if key[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.right += paddle_s
    # update scrin
    pygame.display.flip()
    clock.tick(FPS)