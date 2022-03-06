#! Python 3.9.0 64-bit 
"""Entry Point Script for the Asteroids Clone Game"""
from game import AsteroidRun

if __name__ == "__main__":
    space_rocks = AsteroidRun()
    space_rocks.main_loop()