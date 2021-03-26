import pygame
from menu.menu import Menu
import os

menu_bg = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "menu.png")), (120,70))
upgrade_btn = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "upgrade.png")), (50,50))


class Tower:
    """
    Klasa abstrakcyjna dla wież
    """
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 0
        self.height = 0
        self.sell_price = [0,0,0]
        self.price = [0,0,0]
        self.level = 1
        self.selected = False
        #definiuje menu i przyciski
        self.menu = Menu(self, self.x, self.y, menu_bg, [2000, "MAX"])
        self.menu.add_btn(upgrade_btn, "Upgrade")


        self.tower_imgs = []
        self.damage = 1

    def draw(self, win):
        """
        Rysowanie wieży
        :param win: surface
        :return: None
        """
        img = self.tower_imgs[self.level - 1]
        win.blit (img, (self.x-img.get_width()//2, self.y-img.get_height()//2))

        #rysowanie menu
        if self.selected:
            self.menu.draw(win)

    def draw_radius(self, win):
        if self.selected:
            # rysowanie okręgu zasięgu
            surface = pygame.Surface((self.range*4, self.range*4), pygame.SRCALPHA, 32)
            pygame.draw.circle(surface, (128,128,128, 100), (self.range,self.range), self.range, 0)

            win.blit(surface, (self.x - self.range, self.y - self.range))

    def click(self, X, Y):
        """
        Zwraca gdy kliknięto na wieżę
        i zaznacza wieżę gdy jest kliknięta
        :param x: int
        :param y: int
        :return: bool
        """
        img = self.tower_imgs[self.level - 1]
        if X <= self.x -img.get_width()//2 + self.width and X >= self.x - img.get_width()//2:
            if Y <= self.y + self.height -img.get_height()//2 and Y >= self.y - img.get_height()//2:
                return True
        return False

    def sell(self):
        """
        wezwanie do sprzedazy wiezy, zwraca koszt sprzedaży
        :return:int
        """
        return self.sell_price[self.level-1]

    def upgrade(self):
        """
        ulepsza wieżę za określony koszt
        :return: None
        """
        if self.level + 1 < len(self.tower_imgs):
            self.level += 1
            self.damage += 1

    def get_upgrade_cost(self):
        """
        zwraca koszt ulepszenia, jeśli 0, to nie może  ulepszać
        :return: int
        """
        return self.price[self.level-1]

    def move(self, x, y):
        """
        Przesuwa wieze do podanego x i y
        :param x: int
        :param y: int
        :return: None
        """
        self.x = x
        self.y = y
        self.menu.x = x
        self.menu.y = y
        self.menu.update()