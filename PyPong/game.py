# Python 3.10.1 64-bit

import os

import pygame

from utils import print_text

class PongRun(object):

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("PyPong")

        main_path = os.path.split(os.path.abspath(__file__))[0]
        font_path = os.path.join(main_path, 'font.ttf')

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(font_path, 64)
        self.title_font = pygame.font.Font(font_path, 85)
        self.game_active = True

        self.game_title_screen = "PyPong"
        self.one_player_score = "0"
        self.second_player_score = "0"

        self.screen = pygame.display.set_mode((1200, 800))
        self.background = pygame.Surface(self.screen.get_size())
        self.background.convert().fill((0, 0, 0))

    def main_loop(self):
        while self.game_active:
            self._handle_input()
            self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
    
    def _game_logic(self):
        pass

    def _score_display(self):
        """Responsible for displaying the scores of 1P and 2P"""
        # TODO: Make the score display to dynamically change for every
        # point won by the player.
        print_text(
            self.screen, self.one_player_score, self.font, 
            pos_x_divisor=4, pos_y=200
        )
        print_text(
            self.screen, self.second_player_score, self.font, 
            pos_x_divisor=1.3498, pos_y=200
        )
  
    def _pong_board_style(self):
        """Style of the Pong Board"""
        # TODO: Crooked line possible solutions
        # https://codereview.stackexchange.com/questions/70143/drawing-a-dashed-line-with-pygame

        print_text(
            self.screen, self.game_title_screen, self.title_font, 
            pos_x_divisor=2, pos_y=30
        )

    def _draw(self):

        self.screen.blit(self.background, (0, 0))
        
        self._pong_board_style()
        if self.one_player_score or self.second_player_score:
            self._score_display()

        # Tells the surface buffer to make sure all of the game objects will be displayed all at once
        pygame.display.flip()

        # Retaining the FPS of the display at stable 60FPS
        self.clock.tick(60)