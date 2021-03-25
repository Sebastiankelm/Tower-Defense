import pygame
from .tower import Tower
import os

class ArcherTowerLong(Tower)
    def __init__(self, x ,y):
        super(). __init__(self, x, y)
        self.tower_imgs = []
        self.archer_imgs = []
        self.archer_count = 0

        #Wczytuje zdjęcie wiezy łuczniczej
        for x in range(7,10):
                self.tower_imgs.append(pygame.transform.scale(
                    pygame.image.load(os.path.join("game_assets/archer_towers/archer_1", str(x) + ".png")),
                    (64, 64)))

        for x in range(7,10):
                self.tower_imgs.append(pygame.transform.scale(
                    pygame.image.load(os.path.join("game_assets/archer_towers/archer_1", str(x) + ".png")),
                    (64, 64)))

    def draw(self, win):
        super().draw(win)

    def attack(self, enemies):
        """
        atakuje wroga z listy wrogów, modyfikuje listę
        :param enemies: lista wrogów
        :return: None
        """
