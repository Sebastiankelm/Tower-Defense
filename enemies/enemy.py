import pygame
import math



class Enemy:
    def __init__(self):
        self.width = 64
        self.height = 64
        self.animation_count = 0
        self.health = 1
        self.vel = 3
        self.path = [(-10, 224),(53, 221), (186, 226), (249, 258), (630, 275), (703, 190), (724, 97), (828, 49), (922, 100), (965, 233), (1052, 276), (1137, 291), (1174, 353), (1176, 440), (1102, 491), (958, 495), (832, 515), (745, 555), (150, 542), (94, 421), (56, 348), (8, 332), (-20, 335)]
        self.x = self.path [0] [0]
        self.y = self.path [0] [1]
        self.img = None
        self.dis = 0
        self.path_pos = 0
        self.move_count = 0
        self.move_dis = 0
        self.imgs = []
        self.flipped = False
        self.max_health = 0


    def draw (self, win):
        """
        Rysuje wroga za pomocą podanych obrazów
        :param win: surface
        :return: None
        """
        self.img = self.imgs[self.animation_count]
        self.animation_count += 1
        if self.animation_count >= len(self.imgs):    #
            self.animation_count = 0  #resetowanie animacji

        #for dot in self.path:
            #pygame.draw.circle(win, (255,0,0), dot, 10, 0)

        win.blit(self.img, (self.x - self.img.get_width()/2, self.y - self.img.get_height()/2 -35))
        self.draw_health_bar(win)
        self.move()

    def draw_health_bar(self, win):
        """
        Rysowanie paska życia nad przeciwnikami
        :param win: surface
        :return:None
        """
        length = 50
        move_by = round(length / self.max_health)
        health_bar = move_by * self.health

        pygame.draw.rect(win, (255,0,0), (self.x-30, self.y-75, length, 10), 0)
        pygame.draw.rect(win, (0, 255, 0), (self.x-30, self.y - 75, health_bar, 10), 0)

    def collide (self, X, Y):
        """
        Zwraca, gdy trafiono wroga
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
        Ruch przeciwnikow
        :return:None
        """
        x1, y1 = self.path[self.path_pos]
        if self.path_pos + 1 >= len (self.path):
            x2, y2 = (-10, 355)
        else:
            x2, y2 = self.path[self.path_pos+1]


        dirn = ((x2-x1)*2, (y2-y1)*2)
        length = math.sqrt((dirn[0])**2 + (dirn[1])**2)
        dirn = (dirn[0]/length, dirn[1]/length)


        if dirn[0] < 0 and not(self.flipped):
            self.flipped = True
            for x, img in enumerate(self.imgs):
                self.imgs[x] = pygame.transform.flip(img, True, False)

        move_x, move_y = ((self.x + dirn[0]), (self.y + dirn[1]))

        self.x = move_x
        self.y = move_y

        # przejście do kolejnego punktu
        if dirn[0] >= 0: # ruch w prawo
            if dirn[1] >= 0: # ruch w dol
                if self.x >= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x >= x2 and self.y <= y2:
                    self.path_pos += 1

        else: # ruch w lewo
            if dirn[1] >= 0: # ruch w dol
                if self.x <= x2 and self.y >= y2:
                    self.path_pos += 1
            else:
                if self.x < x2 and self.y >= y2:
                    self.path_pos += 1


    def hit(self, damage):
        """
        Returns if an enemy has died and remove one health
        each call
        :return: Bool
        """
        self.health -= damage
        if self.health <= 0:
            return True
        return False