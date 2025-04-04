from . import constants
import pygame
import random


class Pipe:
    GAP = constants.PIPE_GAP if constants.PLAYER_MODE else constants.PIPE_GAP_AI
    VEL = constants.PIPE_VELOCITY
    PIPE_IMG = constants.PIPE_IMG

    def __init__(self, x, gap=GAP):
        self.x = x
        self.height = 0
        self.gap = gap

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pygame.transform.flip(self.PIPE_IMG, False, True)
        self.PIPE_BOTTOM = self.PIPE_IMG
        
        self.passed = False
        self.set_height()
        
    
    def set_height(self):
        """
        set the height of the pipe, from the top of the screen
        :return: None
        """
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap
        
    def move(self):
        """
         move pipe based on vel
        :return: None
        """
        self.x -= self.VEL

    def draw(self, win):
        """
         draw both the top and bottom of the pipe
        :param win: pygame window/surface
        :return: None
        """
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))
        
        
    def collide(self, bird, win):
        """
         returns if a point is colliding with the pipe
        :param bird: Bird object
        :return: Bool
        """
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False