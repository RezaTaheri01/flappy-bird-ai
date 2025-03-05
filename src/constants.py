import pygame
import os

pygame.font.init()  # init font

PLAYER_MODE = True

WIN_WIDTH = 550
WIN_HEIGHT = 800

CAPTION = "Flappy Bird"

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(
        os.path.join("assets/imgs", "redbird-downflap.png"))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join("assets/imgs", "redbird-midflap.png"))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join("assets/imgs", "redbird-upflap.png")))
]


PIPE_IMG = pygame.transform.scale2x(pygame.image.load(
    os.path.join("assets/imgs", "pipe-red.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(
    os.path.join("assets/imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(
    os.path.join("assets/imgs", "background-night.png")))

BIRD_X = 200
BIRD_Y = 250
ROTATION_VELOCITY = 20
ANIMATION_TIME = 5
MAX_ROTATION = 25
JUMP_VEL = -9
BIRD_DOWN = 16

PIPE_X = 450
PIPE_GAP = 200
PIPE_GAP_VERTICALLY = 600
BASE_PIPE_VELOCITY = 5
FLOOR = 725

STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

FPS = 30



