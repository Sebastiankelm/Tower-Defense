import pygame
import math


class Enemy:
    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(19, 224), (177, 235), (282, 283), (526, 277), (607, 217), (641, 105), (717, 57), (796, 83), (855, 222), (973, 284), (1046, 366), (1022, 458), (894, 492), (740, 504), (580, 542), (148, 541), (10, 442), (-20, 335)]
        self.x = self.path [0] [0]
        self.y = self.path [0] [1]
        self.img = None
        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.imgs = []
        self.flipped = False


    def draw (self, win):
        """
        Draws the enemy with the given images
        :param win: surface
        :return: None
        """
        self.img = self.imgs[self.animation_count]
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):    #
            self.animation_count = 0  #resetowanie animacji

        win.blit(self.img, (self.x, self.y))
        self.move()

    def collide (self, X, Y):
        """
        Returns if position has hit enemy
        :param x: int
        :param y: int
        :return: Bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
                return True
        return False

    def move(self):
        """
        Move enemy
        :return:None
        """
        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len (self.path):
            x2, y2 = (-10, 336)
        else:
            x2, y2 = self.path[self.path_pos+1]
            
        move_dis = math.sqrt ((x2 - x1) ** 2 + (y2 - y1) ** 2)

        dirn = ((x2-x1), (y2-y1))
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length, dirn[1]/length)


        if dirn[0] < 0 and not(self.flipped):
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))
        self.dis += length

        self.x = move_x
        self.y = move_y

        # przejście do kolejnego punktu
        if self.x == x1 and self.y == y2:
            self.dis = 0
            self.path_pos += 1
            if self.path_pos >= len (self.path):
                return False
        return True

    def hit(self):
        """
        Returns if an enemy has died and remove one health
        each call
        :return: Bool
        """
        self.health -= 1
        if self.health <=0:
            return True