from . import constants
import pygame


class Bird:
    IMGS = constants.BIRD_IMGS
    ROTATION_VELOCITY = constants.ROTATION_VELOCITY
    ANIMATION_TIME = constants.ANIMATION_TIME
    MAX_ROTATION = constants.MAX_ROTATION
    JUMP_VEL = constants.JUMP_VEL

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 0
        self.tilt = 0  # !
        self.img_count = 0  # change image base on Animation Time
        self.tick_count = 0  # !
        self.height = self.y
        self.img = self.IMGS[0]

    def jump(self):
        # Top Left: (0, 0) so move up should be negative
        self.vel = self.JUMP_VEL
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1

        d = self.vel * self.tick_count + 1.5 * self.tick_count ** 2

        if d >= constants.BIRD_DOWN:  # more than 15 pixels
            d = constants.BIRD_DOWN

        if d < 0:
            d -= 2

        self.y += d

        if d < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        elif self.tilt > -90:
            self.tilt -= self.ROTATION_VELOCITY

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

        if self.img_count < self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME * 4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME * 2

        # tilt the bird
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
