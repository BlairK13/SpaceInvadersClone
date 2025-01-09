import pygame
from config import screen_width, screen_height
from utils import load_image

class Player(pygame.sprite.Sprite):
    """
    Represents the player. 
    Movement is managed in the main loop, but this class can still have an update method if needed.
    """
    def __init__(self):
        super().__init__()
        self.IMAGE = load_image('space_invaders_sprite_sheet.jpg')
        self.image = self.get_frame_at(240, 200, 30, 15)
        self.rect = self.image.get_rect()

    def update(self, direction=None):
        # Currently doesn't move on its own; main loop handles movement.
        pass

    def get_frame_at(self, x, y, width, height):
        frame_rect = pygame.Rect(x, y, width, height)
        return self.IMAGE.subsurface(frame_rect)
