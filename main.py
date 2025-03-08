import os
import pickle
import neat
import neat.population
import pygame

from src import constants
from src.base import Base, Background
from src.pipe import Pipe
from src.birds import Bird

pygame.init()
pygame.display.set_caption(constants.CAPTION)
WIN = pygame.display.set_mode((constants.WIN_WIDTH, constants.WIN_HEIGHT))

pygame.joystick.init()
joysticks = []

score = 0
generation = 0
highest_score = 0

# region score


def show_score():
    global highest_score
    if constants.PLAYER_MODE:
        if score > highest_score:
            save_high_score(score)
            highest_score = score

    score_str = str(score)
    digit_width = constants.SCORE_IMGS[0].get_width()
    count = len(score_str)

    # Calculate starting x position to center the score
    start_x = constants.WIN_WIDTH // 2 - (digit_width * count) // 2

    # Draw each digit in sequence
    for i, char in enumerate(score_str):
        digit = int(char)
        WIN.blit(constants.SCORE_IMGS[digit], (start_x + i * digit_width, 10))


# Load high score from file
def load_high_score():
    if os.path.exists(constants.HIGH_SCORE_FILE):
        with open(constants.HIGH_SCORE_FILE, "r") as file:
            return int(file.read().strip())
    return 0  # Default high score if file doesn't exist


# Save high score to file
def save_high_score(score):
    with open(constants.HIGH_SCORE_FILE, "w") as file:
        file.write(str(score))


# endregion


# region player


def draw_window(bird: Bird, pipes: Pipe, base: Base, bg: Background, refresh=True):
    # WIN.blit(constants.BG_IMG, (0, constants.FLOOR - constants.WIN_HEIGHT))
    bg.draw(WIN)

    # show score(draw before pipe => score display under pipes)
    show_score()

    for pipe in pipes:
        pipe.draw(WIN)

    # highest score
    highest_label = constants.NEAT_FONT.render(
        "Record: " + str(highest_score), 1, (255, 255, 255))
    WIN.blit(highest_label, (10, 10))

    base.draw(WIN)

    bird.draw(WIN)
    if refresh:
        pygame.display.update()


def main_player():
    reRun = True
    while reRun:
        global score
        score = 0
        bird = Bird(constants.BIRD_X, constants.BIRD_Y)
        base = Base(constants.FLOOR)
        background = Background()
        pipes = [Pipe(constants.PIPE_GAP_VERTICALLY)]

        # set the while loop speed
        clock = pygame.time.Clock()

        # Wait for player to press a key to start
        waiting = True
        while waiting:
            clock.tick(constants.FPS)
            WIN.fill((0, 0, 0))  # Clear screen (optional)

            draw_window(bird, pipes, base, background, False)

            start_label = constants.NEAT_FONT.render(
                "Press SPACE to start", 1, (255, 255, 255)
            )
            WIN.blit(start_label, (constants.WIN_WIDTH // 2 -
                     start_label.get_width() // 2, constants.WIN_HEIGHT // 2))
            
            background.move()
            base.move()

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False
                    reRun = False
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        waiting = False
                    elif event.key == pygame.K_ESCAPE:
                        waiting = False
                        reRun = False
                        pygame.quit()
                        return
                if event.type == pygame.JOYBUTTONDOWN:
                    if event.button == 0 or event.button == 11:  # A/X button
                        waiting = False

        run = True
        while run:
            clock.tick(constants.FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    reRun = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                        reRun = False
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                elif event.type == pygame.JOYDEVICEADDED:
                    joy = pygame.joystick.Joystick(event.device_index)
                    joysticks.append(joy)
                elif event.type == pygame.JOYBUTTONDOWN:
                    # print(event.button)
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

            if bird.y + bird.img.get_height() >= constants.FLOOR or bird.y < 0:
                run = False

            bird.move()
            base.move()
            background.move()
            draw_window(bird, pipes, base, background)
        pygame.time.wait(500) # 0.5s
    pygame.quit()
    return

# endregion


# region neat
class ScoreReachedException(Exception):
    pass


def draw_window_ai(birds, pipes, base, bg):
    # WIN.blit(constants.BG_IMG, (0, 0))
    bg.draw(WIN)

    # score
    show_score()

    for pipe in pipes:
        pipe.draw(WIN)

    # generation
    gen_label = constants.NEAT_FONT.render(
        "Gen: " + str(generation), 1, (255, 255, 255))
    WIN.blit(gen_label, (10, 10))

    # alive birds counter
    birds_label = constants.NEAT_FONT.render(
        "Alive: " + str(len(birds)), 1, (255, 255, 255))
    WIN.blit(birds_label, (10, 50))

    base.draw(WIN)

    for bird in birds:
        bird.draw(WIN)

    pygame.display.update()


def eval_genomes(genomes, config):
    global score, generation
    score = 0
    generation += 1

    nets = []
    ge = []
    birds = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(constants.BIRD_X, constants.BIRD_Y))
        g.fitness = 0
        ge.append(g)

    base = Base(constants.FLOOR)
    bg = Background()
    pipes = [Pipe(constants.PIPE_GAP_VERTICALLY_AI)]

    # set the while loop speed
    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(constants.FPS_AI)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                # quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()
                    # quit()
        pipe_ind = 0
        if len(birds) > 0:
            # determine whether to use the first or second
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():
                pipe_ind = 1
        else:
            run = False
            break

        # give each bird a fitness of BONUS_FITNESS for each frame it stays alive
        for x, bird in enumerate(birds):
            ge[x].fitness += constants.BONUS_FITNESS
            bird.move()

            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            # output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            output = nets[x].activate((bird.y, abs(
                bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
            if output[0] > 0.5:
                bird.jump()

        # region Pipe
        remove = []
        add_pipe = False
        for pipe in pipes:
            for i, bird in enumerate(birds):
                if pipe.collide(bird, WIN):
                    ge[i].fitness -= constants.NEGATIVE_FITNESS
                    birds.pop(i)
                    nets.pop(i)
                    ge.pop(i)

                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                remove.append(pipe)

            pipe.move()

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += constants.POSITIVE_FITNESS
            pipes.append(Pipe(constants.PIPE_GAP_VERTICALLY))

        for rm in remove:
            pipes.remove(rm)
        # endregion

        for i, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= constants.FLOOR or bird.y < 0:
                ge[i].fitness -= constants.NEGATIVE_FITNESS
                birds.pop(i)
                nets.pop(i)
                ge.pop(i)

        base.move()
        draw_window_ai(birds, pipes, base, bg)

        # break if score gets large enough
        if score >= constants.SCORE_LIMIT:
            best_genome = max(ge, key=lambda g: g.fitness)
            best_net = neat.nn.FeedForwardNetwork.create(best_genome, config)
            pickle.dump(best_net, open("best.pickle", "wb"))
            raise ScoreReachedException(
                f"Score reached {constants.SCORE_LIMIT} — stopping training!")


def run(config_file):
    """
    runs the NEAT algorithm to train a neural network to play flappy bird.
    :param config_file: location of config file
    :return: None
    """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, constants.MAX_GEN)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

# endregion


if __name__ == "__main__":
    if constants.PLAYER_MODE:
        highest_score = load_high_score()
        main_player()
    else:
        local_dir = os.path.dirname(__file__)
        config_path = os.path.join(local_dir, "config-feedforward.txt")
        run(config_path)
