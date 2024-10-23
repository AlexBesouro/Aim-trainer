import math
import time
import random
import pygame
from setuptools.config.setupcfg import Target

pygame.init()


WIDTH, HEIGHT = 1000, 800

GAME_WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim trainer")
BG_COLOR = (0 ,25, 50)


TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30
LIVES = 3
BAR_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("comicsans", 24)

def format_time(secs):
    mili = math.floor(int(secs * 1000 % 1000) / 100)
    seconds = int(round(secs % 60, 1))
    minutes = int(secs // 60)
    return f"{minutes:02d}:{seconds:02d}:{mili:02d}"

def top_bar(win, elapsed_time, targets_pressed, misses):
    pygame.draw.rect(surface=win, color="grey", rect=(0, 0, WIDTH, BAR_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")
    win.blit(time_label, (10, 10))

    targets_label = LABEL_FONT.render(f"Targets pressed {targets_pressed}", 1, "black")
    win.blit(targets_label, (150, 10))

    misses_label = LABEL_FONT.render(f"Missed {misses}", 1, "black")
    win.blit(misses_label, (350, 10))


def end_screen(win, elapsed_time, targets_pressed):
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "yellow")
    win.blit(time_label, (300, 300))

    targets_label = LABEL_FONT.render(f"Targets pressed {targets_pressed}", 1, "yellow")
    win.blit(targets_label, (500, 300))
    pygame.display.update()
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def main():
    targets = []
    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    run = True
    while run:
        clock.tick(60)
        click = False
        mouse_pos = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING + BAR_HEIGHT, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + BAR_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for t in targets:
            t.growing()
            if t.size <= 0 :
                targets.remove(t)
                misses += 1

            if click and t.collide(*mouse_pos):
                targets_pressed += 1
                targets.remove(t)

        if misses >= LIVES:
            end_screen(GAME_WINDOW, elapsed_time, targets_pressed)

        draw(GAME_WINDOW,targets)
        top_bar(GAME_WINDOW, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()


class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "yellow"

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def growing(self):
        if self.size + self.GROWTH_RATE >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win): # Step 6
        pygame.draw.circle(surface=win, color=self.COLOR, center=(self.x, self.y), radius=self.size)
        pygame.draw.circle(surface=win, color=self.SECOND_COLOR, center=(self.x, self.y), radius=self.size * 0.8)
        pygame.draw.circle(surface=win, color=self.COLOR, center=(self.x, self.y), radius=self.size * 0.6)
        pygame.draw.circle(surface=win, color=self.SECOND_COLOR, center=(self.x, self.y), radius=self.size * 0.4)

    def collide(self, x, y):
        dis = math.sqrt((self.x - x)**2 + (self.y - y)**2)
        return dis <= self.size


def draw(win, targets):
    win.fill(BG_COLOR)
    for t in targets:
        t.draw(win)


if __name__ == "__main__":
    main()