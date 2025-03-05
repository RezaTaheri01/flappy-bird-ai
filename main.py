import time
import pygame

from src import constants
from src.base import Base
from src.pipe import Pipe
from src.birds import Bird

pygame.init()
pygame.display.set_caption(constants.CAPTION)
WIN = pygame.display.set_mode((constants.WIN_WIDTH, constants.WIN_HEIGHT))

pygame.joystick.init()
joysticks = []

score = 0


def draw_window(bird: Bird, pipes: Pipe, base: Base):
    WIN.blit(constants.BG_IMG, (0, constants.FLOOR - constants.WIN_HEIGHT))

    for pipe in pipes:
        pipe.draw(WIN)

    # score
    score_label = constants.STAT_FONT.render(
        "Score: " + str(score), 1, (255, 255, 255))
    WIN.blit(score_label, ((constants.WIN_WIDTH // 2) -
             (score_label.get_width() // 2), 10))

    base.draw(WIN)

    bird.draw(WIN)
    pygame.display.update()


def main_player():
    reRun = True
    while reRun:
        global score
        score = 0
        bird = Bird(constants.BIRD_X, constants.BIRD_Y)
        base = Base(constants.FLOOR)
        pipes = [Pipe(constants.PIPE_GAP_VERTICALLY)]

        # set the while loop speed
        clock = pygame.time.Clock()

        run = True
        while run:
            clock.tick(constants.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    reRun = False
                elif event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks.append(joy)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                elif event.type == pygame.JOYBUTTONDOWN:
                    print(event.button)
                    if event.button == 0 or event.button == 11:  # press A/X button OR Up
                        bird.jump()

            # region Pipe
            remove = []
            add_pipe = False
            for pipe in pipes:
                if pipe.collide(bird, WIN):
                    run = False
                    break
                if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                    remove.append(pipe)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

                pipe.move()

            if add_pipe:
                score += 1
                pipes.append(Pipe(constants.PIPE_GAP_VERTICALLY))

            for rm in remove:
                pipes.remove(rm)
            # endregion

            if bird.y + bird.img.get_height() >= constants.FLOOR:
                run = False

            bird.move()
            base.move()
            draw_window(bird, pipes, base)
        time.sleep(0.5)
    pygame.quit()
    quit()


if __name__ == "__main__":
    if constants.PLAYER_MODE:
        main_player()
    else:
        pass
