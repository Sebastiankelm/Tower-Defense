import pygame
import os


class Button:
    def __init__(self, x, y, img, name):
        self.name = name
        self.img = img
        self.x =x
        self.y = y
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def click(self,X ,Y):
        """
        Zwraca gdy pozycja ma kolizje z menu
        :param x: int
        :param y: int
        :return: bool
        """
        if X <= self.x + self.width and X >- self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))


class Menu:

    """
    menu dla przechowywanych przedmiotow
    """
    def __init__(self, x, y, img):

        self.x = x
        self.y = y
        self.width = img.get_width()
        self.height = img.get_height()
        self.item_names = []
        self.buttons = []
        self.items = 0
        self.bg = img

    def add_btn(self, img, name):
        """
        dodawanie przyciskó do menu
        :param img: surface
        :param name: str
        :return: none
        """
        self.items += 1
        inc_x = self.width/self.items/2
        btn_x = self.x - self.bg.get_width()/2 + 10
        btn_y = self.y - 120 + 10
        self.buttons.append(Button(btn_x, btn_y, img, name))

    def draw(self, win):
        """
        rysowanie przycisków i tła menu
        :param win: surface
        :return: None
        """
        win.blit(self.bg, (self.x - self.bg.get_width()/2, self.y-120))
        for item in self.buttons:
            item.draw(win)

    def get_clicked(self, X, Y):
        """
        zwraca klikniety item z menu
        :param X: int
        :param Y: int
        :return: str
        """
        for btn in self.buttons:
            if btn.click(X, Y):
                return btn.name
