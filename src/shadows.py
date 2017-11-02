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

        self.width = self.parent.rect.width * 0.75
        self.height = self.width * 0.5

        self.rect = pygame.Rect((parent.rect.x, parent.rect.y), (self.width, self.height))

        self.image = pygame.Surface([self.width, self.height])
        pygame.draw.ellipse(self.image, constants.BLACK, self.rect)