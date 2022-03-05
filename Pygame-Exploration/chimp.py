# Chimp Sprite Class

from typing import Callable

import pygame

class Chimp(pygame.sprite.Sprite):
    """Moves a monkey critter across the screen. It can spin the
    monkey when it is punched."""

    def __init__(self, load_image: Callable):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("chimp.png", -1, 4)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.topleft = 10, 90
        self.move = 18
        self.dizzy = False
    
    def update(self):
        """Walk or spin, depending on the monkeys state"""
        if self.dizzy:
            self._spin()
        else:
            self._walk()
    
    def _walk(self):
        """Move the monkey across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
        
        if not self.area.contains(newpos):
            if self.rect.left < self.area.left or self.rect.right > self.area.right:
                self.move = -self.move
                newpos = self.rect.move((self.move, 0))
                self.image = pygame.transform.flip(self.image, True, False)
        
        self.rect = newpos

    def _spin(self):
        """Spin the Monkey Image"""
        center = self.rect.center
        self.dizzy = self.dizzy + 12
        if self.dizzy >= 360:
            self.dizzy = False
            self.image = self.original
        else:
            rotate = pygame.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def punched(self):
        """This will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = True
            self.original = self.image