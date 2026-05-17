import pygame
from constants import SCREEN_HEIGHT


class Obstacle:
    def __init__(self, main_game, image, x, y=None):
        self.main_game = main_game
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        if y is not None:
            self.rect.y = y
        else:
            self.rect.bottom = SCREEN_HEIGHT - self.rect.height

    def move(self,amount):
        self.rect.x -= amount

    def draw(self):
        self.main_game.screen.blit(self.image, self.rect)

    def check_collision(self, game):
        return self.rect.colliderect(game.player_rect)