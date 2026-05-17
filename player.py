import pygame
from pygame import draw


class Player:
    def __init__(self, main_game, image, state, sound=None, volume=1):
        self.main_game = main_game
        self.image = pygame.transform.scale(pygame.image.load(image), (100,100))
        self.active = state
        self.sound = pygame.mixer.Sound(sound)
        self.rect = self.image.get_rect()
        self.volume = volume

    def update(self):
        self.draw()

    def draw(self):
        self.main_game.screen.blit(self.image, self.rect)

    def update_rect(self, width, height, x, y):
        self.rect.width = width
        self.rect.height = height
        self.rect.x = x
        self.rect.y = y