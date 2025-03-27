from . import constants
import pygame


class Bird:
    IMGS = constants.BIRD_IMGS
    ROTATION_VELOCITY = constants.ROTATION_VELOCITY
    ANIMATION_TIME = constants.ANIMATION_TIME
    MAX_ROTATION = constants.MAX_ROTATION
    JUMP_VEL = constants.JUMP_VEL if constants.PLAYER_MODE else constants.JUMP_VEL_AI
    GRAVITY = constants.GRAVITY # Added gravity constant
    TERMINAL_VEL = constants.TERMINAL_VEL  # Added terminal velocity

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.tilt = 0
        self.img_count = 0
        self.tick_count = 0
        self.height = self.y
        self.img = self.IMGS[0]

    def jump(self):
        self.vel = self.JUMP_VEL
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        # Apply gravity with smoothing
        self.vel += self.GRAVITY
        if self.vel > self.TERMINAL_VEL:
            self.vel = self.TERMINAL_VEL
            
        d = self.vel

        if constants.PLAYER_MODE:
            if d >= constants.TERMINAL_VEL:
                d = constants.TERMINAL_VEL
        else:
            if d >= constants.TERMINAL_VEL_AI:
                d = constants.TERMINAL_VEL_AI

        self.y += d

        # Smoother tilt transitions
        target_tilt = 0
        if d < 0 or self.y < self.height + 50:
            target_tilt = self.MAX_ROTATION
        else:
            target_tilt = min(-30, -self.vel * 2)  # Tilt based on velocity

        # Smooth tilt interpolation
        if self.tilt < target_tilt:
            self.tilt += min(self.ROTATION_VELOCITY, target_tilt - self.tilt)
        elif self.tilt > target_tilt:
            self.tilt -= min(self.ROTATION_VELOCITY, self.tilt - target_tilt)

    def draw(self, win):
        def blitRotateCenter(surf, image, topleft, angle):
            """
            Rotate a surface and blit it to the window
            :param surf: the surface to blit to
            :param image: the image surface to rotate
            :param topLeft: the top left position of the image
            :param angle: a float value for angle
            :return: None
            """
            rotated_image = pygame.transform.rotate(image, angle)
            new_rect = rotated_image.get_rect(
                center=image.get_rect(topleft=topleft).center)

            surf.blit(rotated_image, new_rect.topleft)

        self.img_count += 1

        # Smoother animation transitions
        cycle = self.ANIMATION_TIME * 4
        frame = (self.img_count % cycle) // self.ANIMATION_TIME
        
        if frame == 0:
            self.img = self.IMGS[0]
        elif frame == 1:
            self.img = self.IMGS[1]
        elif frame == 2:
            self.img = self.IMGS[2]
        elif frame == 3:
            self.img = self.IMGS[1]

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
