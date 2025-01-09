import pygame
import random
from utils import load_image

class Enemy(pygame.sprite.Sprite):
    """
    Represents an enemy on the screen.
    """
    def __init__(self, speed=1):
        super().__init__()
        self.IMAGE = load_image('space_invaders_sprite_sheet.jpg')
        
        # Possible animation frames (pairs for toggling)
        self.frames = [
            ((6, 198, 25, 16), (35, 198, 25, 16)),
            ((65, 198, 25, 16), (94, 198, 25, 16)),
            ((130, 198, 25, 16), (157, 198, 25, 16))
        ]

        # Pick one of the frame pairs at random
        self.initial_frame, self.intermediate_frame = random.choice(self.frames)
        self.image = self.get_frame_at(*self.initial_frame)
        self.rect = self.image.get_rect()

        # Animation timing
        self.switch_time = pygame.time.get_ticks() + 1000
        self.state = 'initial'
        self.speed = speed

    def update(self, direction):
        # Handle sprite toggles every 1 second
        current_time = pygame.time.get_ticks()
        if self.state == 'initial' and current_time >= self.switch_time:
            self.image = self.get_frame_at(*self.intermediate_frame)
            self.state = 'intermediate'
            self.switch_time = current_time + 1000
        elif self.state == 'intermediate' and current_time >= self.switch_time:
            self.image = self.get_frame_at(*self.initial_frame)
            self.state = 'initial'
            self.switch_time = current_time + 1000

        # Move horizontally based on direction
        self.rect.x += direction * self.speed

    def get_frame_at(self, x, y, width, height):
        """
        Crops the sprite from the loaded IMAGE.
        """
        frame_rect = pygame.Rect(x, y, width, height)
        return self.IMAGE.subsurface(frame_rect)
