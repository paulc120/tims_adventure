import pygame

from src.etc import constants

'''
shadows.py

This file defines the shadow class,
which is an on-screen shadow displayed
under some decorations and entities.
'''


class Shadow:

    def __init__(self, parent):

        # A shadow generates its size based
        # off of its parents dimensions.
        self.parent = parent

        self.width = self.parent.rect.width * 0.8
        self.height = self.width * 0.5

        self.rect = pygame.Rect((parent.rect.x, parent.rect.y+(parent.rect.height*0.85)), (self.width, self.height))

        self.image = pygame.Surface([self.width, self.height])

        self.image.fill(constants.WHITE)
        self.image.set_colorkey(constants.WHITE)

        pygame.draw.ellipse(self.image, constants.BLACK, [0, 0, self.width, self.height])
        self.image.set_alpha(128)

    def update(self):

        self.rect.centerx = self.parent.rect.centerx
        self.rect.y = self.parent.rect.y + (self.parent.rect.height * constants.shadow_offset)

    def draw(self, display):

        display.blit(self.image, (self.rect.x, self.rect.y))
