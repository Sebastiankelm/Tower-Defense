import pygame
import os
from enemies.scorpion import Scorpion
from enemies.club import Club
from enemies.wizard import Wizard
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import DamageTower, RangeTower
import time
import random
pygame.font.init()

lives_img = pygame.image.load(os.path.join("game_assets", "heart.png"))
star_img = pygame.image.load(os.path.join("game_assets", "star.png"))


class Game:
    def __init__(self):
        self.width = 1200
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = [Wizard()]
        self.attack_towers = [ArcherTowerLong(300, 200), ArcherTowerLong(700, 600), ArcherTowerShort(200, 600)]
        self.support_towers = [RangeTower(200,100)]
        self.lives = 10
        self.money = 100
        self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans", 70)



    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            if time.time() - self.timer >= random.randrange(1,5)/2:
                self.timer = time.time()
                self.enemys.append(random.choice([Club(), Scorpion(), Wizard()]))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                pos = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

            # petla przez przeciwnikow
            to_del = []
            for en in self.enemys:
                if en.x < -15:
                    to_del.append(en)

            # usuniecie wszystkich wrogów z ekranu
            for d in to_del:
                self.lives -= 1
                self.enemys.remove(d)

            # pętla przez wieże atakujące
            for tw in self.attack_towers:
                tw.attack(self.enemys)

            # pętla przez wieże wspierające
            for tw in self.support_towers:
                tw.support(self.attack_towers)

            #jesli przegrasz
            if self.lives <=0:
                print("Przegrana")
                run = False

            self.draw()

        pygame.quit()

    def draw (self):
        self.win.blit(self.bg, (0,0))

        #Rysowanie wież atakujących
        for tw in self.attack_towers:
            tw.draw(self.win)

        # Rysowanie wież wspierających
        for tw in self.support_towers:
            tw.draw(self.win)

        # Rysowanie przeciwników
        for en in self.enemys:
            en.draw(self.win)

        #Rysowanie życ
        text = self.life_font.render(str(self.lives), 1, (255,255,255))
        life = pygame.transform.scale(lives_img, (50,50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 13))
        self.win.blit(life, (start_x, 10))

        pygame.display.update()

    def draw_menu(self):
        pass

g = Game()
g.run()