import pygame
import os

pygame.font.init()  # init font

PLAYER_MODE = True

WIN_WIDTH = 550
WIN_HEIGHT = 800

# File to store high score
HIGH_SCORE_FILE = os.path.join("assets", f"highscore.txt")

CAPTION = "Flappy Bird"

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(
        os.path.join("assets/imgs", "redbird-downflap.png"))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join("assets/imgs", "redbird-midflap.png"))),
    pygame.transform.scale2x(pygame.image.load(
        os.path.join("assets/imgs", "redbird-upflap.png")))
]

SCORE_IMGS = [pygame.transform.scale_by(pygame.image.load(os.path.join(
    "assets/imgs", f"{i}.png")), 1.5) for i in range(10)]

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(
    os.path.join("assets/imgs", "pipe-red.png")))
BASE_IMG = pygame.transform.scale2x(pygame.image.load(
    os.path.join("assets/imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(
    os.path.join("assets/imgs", "background-night.png")))

BIRD_X = 200
BIRD_Y = 250
ROTATION_VELOCITY = 15
ANIMATION_TIME = 5
MAX_ROTATION = 20
JUMP_VEL = -9
GRAVITY = 1.1  # Added gravity constant
TERMINAL_VEL = 16  # Added terminal velocity

PIPE_X = 450
PIPE_GAP = 200
PIPE_GAP_VERTICALLY = 600
FLOOR = 725

# Speed of each layer
PIPE_VELOCITY = 5
BASE_VELOCITY = 6
BG_VELOCITY = 3

STAT_FONT = pygame.font.SysFont("comicsans", 50)
END_FONT = pygame.font.SysFont("comicsans", 70)
DRAW_LINES = False

FPS = 30


# NEAT
FPS_AI = 60 # set it to Zero for max speed
NEAT_FONT = pygame.font.SysFont("comicsans", 25)
PIPE_GAP_VERTICALLY_AI = 570
PIPE_GAP_AI = 135
NEGATIVE_FITNESS = -1
POSITIVE_FITNESS = 3
BONUS_FITNESS = 0.1

JUMP_VEL_AI = -9
TERMINAL_VEL_AI = 16  # Added terminal velocity

SCORE_LIMIT = 75

MAX_GEN = 50
