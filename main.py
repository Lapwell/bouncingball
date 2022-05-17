import pygame
import random
import sys

pygame.init()

BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
WIDTH, HEIGHT = 800, 800
ROOT = pygame.display.set_mode((WIDTH, HEIGHT))
GRAVITY = 0.05
ENERGY_LOSS = 0.95
FPS = 60
FONT = pygame.font.Font(None, 24)  # The font for any text in-game

ball_list = []
clock = pygame.time.Clock()


class BallClass:
    def __init__(self, posx, posy, x_vel, y_vel, SIZE):
        self.posx, self.posy = posx, posy
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.SIZE = SIZE
        self.rect = pygame.Rect(posx, posy, SIZE, SIZE)

    def update_pos(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel

    def collide(self):
        x = list(ball_list)
        x.pop(x.index(self))
        for item in x:
            if self.rect.colliderect(item.rect):
                self.y_vel *= -1
                self.x_vel *= -1
                self.update_pos()


def check_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            spawn_ball(pygame.mouse.get_pos())


def ran_num():
    num = random.randrange(-8, 8)
    while num == 0:
        num = random.randrange(-8, 8)
    return num


def spawn_ball(mouse_pos):
    base = 5
    base = base * round(random.randrange(15, 50)/base)
    ball_list.append(BallClass(mouse_pos[0], mouse_pos[1], ran_num(), ran_num(), base))


def bounce_ball():
    for item in ball_list:
        if item.rect.x >= WIDTH - item.SIZE or item.rect.x <= 0 + item.SIZE:
            item.x_vel = item.x_vel * -1
        if item.rect.colliderect(border):
            item.y_vel = item.y_vel / 2 * -1
        if item.rect.y < -HEIGHT / 2:
            item.y_vel = -item.y_vel * ENERGY_LOSS
        item.y_vel += GRAVITY
        item.update_pos()


def fps_counter():
    count = str(int(clock.get_fps()))
    fps_txt = FONT.render(count, True, WHITE)
    ROOT.blit(fps_txt, (fps_txt.get_width() - fps_txt.get_width()//2, fps_txt.get_height() - fps_txt.get_height()//2))


def update_root():
    ROOT.fill(BLACK)
    for item in ball_list:
        item.collide()
        pygame.draw.circle(ROOT, RED, (item.rect.x + item.SIZE // 2, item.rect.y + item.SIZE // 2), item.SIZE - item.SIZE // 3)
        pygame.draw.rect(ROOT, GREEN, item.rect)
    pygame.draw.rect(ROOT, BLUE, border)
    fps_counter()
    pygame.display.update()


def main():
    check_events()
    bounce_ball()
    update_root()
    clock.tick(FPS)


if __name__ == '__main__':
    border = pygame.Rect(0, HEIGHT - 40, WIDTH, 40)
    while True:
        main()
