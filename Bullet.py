import pygame
from config import WHITE, screen_height

class Bullet(pygame.sprite.Sprite):
    """
    Player bullet moves upward.
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

class EnemyBullet(pygame.sprite.Sprite):
    """
    Enemy bullet moves downward.
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([4, 10])
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed_y = 5

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height:
            self.kill()
