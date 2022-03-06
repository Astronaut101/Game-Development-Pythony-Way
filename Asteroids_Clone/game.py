#! PYthon 3.9.0 64-bit
import pygame

from utils import load_sprite
from models import Spaceship
from models import Rock
from utils import print_text

# import random

"""
TODO:
Additional Features that are integral in making the game more alive and much more functional:
    1. Fixing the bug wherein when we press K_SPACE, it suddenly crashes. (DONE)
    2. Game Over and Alive State. (adding context)
    3. Adding Multiple Live / Adding Health Bar.
    4. Have the bullets kill the Ship if it accelerates into one.
    5. Add scoring. 
    6. Add a "play again" action. 
    7. Add an "instant replay" feature.
"""

bullets = []
rocks   = []

class AsteroidRun:
    def __init__(self):
        # Initializing PyGame and set the title
        pygame.init()
        pygame.display.set_caption("Asteroid Rocks")
        self.clock             = pygame.time.Clock()
        self.font              = pygame.font.Font(None, 64)
        self.message           = ""
        self.game_active       = True
        
        self.screen     = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)

        # self.bullets = []

        self.ship = Spaceship((400, 300), bullets)
        
        global rocks
        rocks = [
            Rock.create_random(self.screen, self.ship.position) 
            for _ in range(6)
        ]
        # sprite = load_sprite("asteroid")
        # self.rock = GameObject((50, 300), sprite, (0.5, 0))

        # self.collision_count = 0

    def main_loop(self):
        while self.game_active:
            self._handle_input()
            self._game_logic()
            self._draw()

    def _handle_input(self):
        for event in pygame.event.get():
            # Checking if the QUIT functionality is pushed
            if event.type == pygame.QUIT:
                quit()      
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.ship == None:
                        self.ship = Spaceship((400, 300), bullets)
                        self.message = ""
                        
                    self.ship.shoot()

        is_key_pressed = pygame.key.get_pressed()
        if is_key_pressed[pygame.K_ESCAPE] or is_key_pressed[pygame.K_q]:
            quit()
            
        if self.ship is None:  # Game Over Phase
            return self.message
            
        elif is_key_pressed[pygame.K_RIGHT]:
            self.ship.rotate(clockwise=True)
        elif is_key_pressed[pygame.K_LEFT]:
            self.ship.rotate(clockwise=False)
        elif is_key_pressed[pygame.K_UP]:
            self.ship.accelerate()

    # NOTE: Establishing the Start of Game and Game Over States of the Whole Asteroid Game Sequence.
    # def _intro_screen_display(self):
    #     title_surf        = self.font.render(f"Asteroids with PyGame", False, "#e7ffee") 
    #     instructions_surf = self.font.render("Press Spacebar to start shooting asteroids!", False, "#e7ffee")
        
    #     title_rect        = title_surf.get_rect(center=(400, 60)) 
    #     instructions_rect = instructions_surf.get_rect(center=(400, 320))
        
    #     self.screen.blit(title_surf, title_rect) 
    #     self.screen.blit(instructions_surf, instructions_rect)
        
    def _game_over_screen_display(self):
        game_over_instructions_surf   = self.font.render("Press Spacebar to restart!", False, "#e7ffee")
        game_over_instructions_rect   = game_over_instructions_surf.get_rect(center=(400, 200))
        
        self.screen.blit(game_over_instructions_surf, game_over_instructions_rect)
        
    @property
    def game_objects(self):
        global bullets, rocks
        asteroid_game_assets = [*bullets, *rocks]
        
        if self.ship:
            asteroid_game_assets.append(self.ship)
        # return [*self.rocks, *self.bullets, self.ship]

        return asteroid_game_assets
        
    def _game_logic(self):
        global bullets, rocks
        
        for obj in self.game_objects:
            obj.move(self.screen)

        rect = self.screen.get_rect()
        for bullet in bullets[:]:  # copying a list means extra memory has been used
            if not rect.collidepoint(bullet.position):
                bullets.remove(bullet)
                
        for bullet in bullets[:]:
            for rock in rocks[:]:
                if rock.collides_with(bullet):
                    rocks.remove(rock)
                    rock.split()
                    bullets.remove(bullet)
                    break
        
        if self.ship:
            for rock in rocks[:]:
                if rock.collides_with(self.ship):
                    self.ship = None
                    self.message = "You lost!"
                    break
                
        if not rocks and self.ship:
            self.message = "You won!"
        # self.ship.move(self.screen)
        # self.rock.move()

    def _draw(self):
        # Initializing the random movement of the circle wherein the main loop logic is being passed
        # circle_x      = random.randint(10, 790)
        # circle_y      = random.randint(10, 590)
        # circle_radius = random.randint(2, 10)

        # self.screen.fill((135, 206, 235))
        # pygame.draw.circle(
        #     self.screen, (0, 0, 150), (circle_x, circle_y), circle_radius
        # )

        self.screen.blit(self.background, (0, 0))

        for obj in self.game_objects:
            obj.draw(self.screen)

        # self.ship.draw(self.screen)
        # self.rock.draw(self.screen)

        if self.message:
            print_text(self.screen, self.message, self.font)
        
        # Tells the surface buffer to make sure all of the game objects will be displayed all at once.
        pygame.display.flip()

        # if self.ship.collides_with(self.rock):
        #     self.collision_count += 1
        #     print(f"Collision #{self.collision_count}")
        self.clock.tick(60)

