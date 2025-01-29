import pygame

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('walls/wall.png')
        self.rect = self.image.get_rect(topleft=(x, y))