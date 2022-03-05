# Main Smack-a-Chimp game loop

import os

import pygame

from fist import Fist
from chimp import Chimp

# TODO: 
# Possibly to properly contain it inside of a calss

# To give appropriate warnings if our font and sound assets are disabled
if not pygame.font:
    print("Warning, fonts disabled")
if not pygame.mixer:
    print("Warning, sound disabled")

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "game-assets")

def load_image(name, colorKey=None, scale=1) -> tuple:
    """
    params name: image to be loaded
    params colorKey: Used in graphics to represent 
    a color of the image that is transparent.
    params scale: scaling the image to the desired size
    """

    fullname = os.path.join(data_dir, name)
    image = pygame.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pygame.transform.scale(image, size)

    image = image.convert()
    if colorKey is not None:
        if colorKey == -1:
            colorKey = image.get_at((0, 0))
        image.set_colorkey(colorKey, pygame.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    # This will check if the pygame.mixer has been imported properly
    # If not, it returns a small class instance that has a dummy play method.
    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)
    sound = pygame.mixer.Sound(fullname)

    return sound


def main() -> None:

    pygame.init()
    screen = pygame.display.set_mode((1280, 480), pygame.SCALED)
    pygame.display.set_caption("Smack-a-Monkey")
    pygame.mouse.set_visible(False)

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))

    if pygame.font:
        font = pygame.font.Font(os.path.join(data_dir, 'font.ttf'), 64)
        text = font.render("Pummel The Chimp, and win $$$", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)
    
    screen.blit(background, (0, 0))
    pygame.display.flip()

    whiff_sound = load_sound("whiff.wav")
    punch_sound = load_sound("punch.wav")
    chimp = Chimp(load_image)
    fist = Fist(load_image)
    allsprites = pygame.sprite.RenderPlain((chimp, fist))
    clock = pygame.time.Clock()

    going = True
    while going:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                going = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                going = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if fist.punch(chimp):
                    punch_sound.play()  # punch
                    chimp.punched()
                else:
                    whiff_sound.play()  # miss
            elif event.type == pygame.MOUSEBUTTONUP:
                fist.unpunch()
    
        allsprites.update()

        screen.blit(background, (0,0))
        allsprites.draw(screen)
        pygame.display.flip()

    pygame.quit()  # Game Over


if __name__ == "__main__":
    raise SystemExit(main())