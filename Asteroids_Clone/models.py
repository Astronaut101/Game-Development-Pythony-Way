#! Python 3.9.0 64-bit 
import random

from pygame.math import Vector2
from pygame.transform import rotozoom
from utils import load_sprite
from utils import wrap_position
from utils import load_sound

DIRECTION_UP = Vector2(0, -1)

class GameObject:
    def __init__(self, position, sprite, velocity, wraps=True):
        self.position = Vector2(position)
        self.sprite   = sprite
        self.radius   = sprite.get_width() / 2
        self.velocity = Vector2(velocity)
        self.wraps    = wraps
        
    def draw(self, surface):
        position = self.position - Vector2(self.radius)
        surface.blit(self.sprite, position)
        
    def move(self, surface):
        move_to = self.position + self.velocity
        self.position = wrap_position(move_to, surface)
        
        if self.wraps:
            self.position = wrap_position(move_to, surface)
        else:
            self.position = move_to
        
    def collides_with(self, other):
        distance = self.position.distance_to(other.position)
        return distance < self.radius + other.radius
    

class Spaceship(GameObject):
    ROTATION_SPEED = 3
    ACCELERATION   = 0.25
    BULLET_SPEED   = 3
    
    def __init__(self, position, bullet_container):
        self.direction        = Vector2(DIRECTION_UP)
        self.bullet_sound     = load_sound("laser")
        self.bullet_container = bullet_container
        super().__init__(position, load_sprite("spaceship"), Vector2(0))
        
    def rotate(self, clockwise=True):
        sign  = 1 if clockwise else - 1
        angle = self.ROTATION_SPEED * sign 
        self.direction.rotate_ip(angle)  # Handles all trigonometric calculations of a rotating object
        
    def accelerate(self):
        self.velocity += self.direction * self.ACCELERATION
    
    def shoot(self):
        velocity = self.direction * self.BULLET_SPEED + self.velocity
        bullet   = Bullet(self.position, velocity)
        self.bullet_container.append(bullet)
        
        self.bullet_sound.play()
        
        print(f"# bullets:{len(self.bullet_container)}")
    
    def draw(self, surface):
        angle = self.direction.angle_to(DIRECTION_UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
        
        
class Rock(GameObject):
    MIN_START_GAP = 250
    MIN_SPEED = 1
    MAX_SPEED = 3
    
    # Creating a Factory Method
    @classmethod
    def create_random(cls, surface, ship_position):
        # Generate a random position until one is far enough away from ship
        while True:
            position = Vector2(
                random.randrange(surface.get_width()),
                random.randrange(surface.get_height()),
            )
            
            if position.distance_to(ship_position) > cls.MIN_START_GAP:
                break
        
        return Rock(position)
    
    def __init__(self, position, size=3):
        # Generate a random position until one is far enough away from ship
        self.size = size 
        if size == 3:
            scale = 1.0
        elif size == 2:
            scale = 0.5
        else:
            scale = 0.25
        
        sprite = rotozoom(load_sprite("asteroid"), 0, scale)    
        
        # Random Velocity 
        speed = random.randint(self.MIN_SPEED, self.MAX_SPEED)
        angle = random.randint(0, 360)
        velocity = Vector2(speed, 0).rotate(angle)
        
        super().__init__(position, sprite, velocity)
    
    def split(self):
        if self.size > 1:
            from game import rocks 
            
            # Rocks that are going to be split by its scale depending on how large
            # the size of the rocks.  
            rocks.append(Rock(self.position, self.size - 1))
            rocks.append(Rock(self.position, self.size - 1))
        
class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity, False)