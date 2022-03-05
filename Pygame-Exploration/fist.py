# Tackling the Fist Sprite Module

from typing import Callable

import pygame


class Fist(pygame.sprite.Sprite):
    """Moves a clenched fist on the screen, following the mouse"""

    def __init__(self, load_image: Callable):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("fist.png", -1)
        self.fist_offset = (-235, -80)
        self.punching = False

    def update(self):
        """Move the fist based on the mouse position"""
        pos = pygame.mouse.get_pos()
        self.rect.topleft = pos
        self.rect.move_ip(self.fist_offset)
        if self.punching:
            self.rect.move_ip(15, 25)

    def punch(self, target):
        """Returns true if the fist collides with the target"""
        if not self.punching:
            self.punching = True
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        """Called to pull the first back"""
        self.punching = False