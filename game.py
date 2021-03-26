import pygame
import os
from enemies.scorpion import Scorpion
from enemies.club import Club
from enemies.wizard import Wizard
from towers.archerTower import ArcherTowerLong, ArcherTowerShort
from towers.supportTower import DamageTower, RangeTower
from menu.menu import VerticalMenu
import time
import random
pygame.font.init()

lives_img = pygame.image.load(os.path.join("game_assets", "heart.png"))
star_img = pygame.image.load(os.path.join("game_assets", "star.png"))
side_img = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "side.png")), (120,500))

buy_archer = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_archer.png")), (75,75))
buy_archer_2 = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_archer_2.png")), (75,75))
buy_damage = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_damage.png")), (75,75))
buy_range = pygame.transform.scale(pygame.image.load(os.path.join("game_assets", "buy_range.png")), (75,75))

attack_tower_names = ["archer", "archer2"]
support_tower_names = ["range", "damage"]


class Game:
    def __init__(self):
        self.width = 1350
        self.height = 700
        self.win = pygame.display.set_mode((self.width, self.height))
        self.enemys = []
        self.attack_towers = [ArcherTowerLong(300, 200), ArcherTowerLong(700, 600), ArcherTowerShort(200, 600)]
        self.support_towers = [RangeTower(400,200)]
        self.lives = 10
        self.money = 10000
        self.bg = pygame.image.load(os.path.join("game_assets", "bg.png"))
        self.bg = pygame.transform.scale(self.bg, (self.width, self.height))
        self.timer = time.time()
        self.life_font = pygame.font.SysFont("comicsans", 65)
        self.selected_tower = None
        self.menu = VerticalMenu(self.width - side_img.get_width() + 70, 250, side_img)
        self.menu.add_btn(buy_archer, "buy_archer", 500)
        self.menu.add_btn(buy_archer_2, "buy_archer_2", 750)
        self.menu.add_btn(buy_damage, "buy_damage", 1000)
        self.menu.add_btn(buy_range, "buy_range", 1000)
        self.moving_object = None
        #self.clicks = []



    def run(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            clock.tick(60)
            # Generowanie potworów
            if time.time() - self.timer >= random.randrange(1,5)/2:
                self.timer = time.time()
                self.enemys.append(random.choice([Club(), Scorpion(), Wizard()]))

            pos = pygame.mouse.get_pos()

            # sprawdza czy obiekt sie porusza
            if self.moving_object:
                self.moving_object.move(pos[0], pos[1])

            # główna pętla zdarzeń
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False


                if event.type == pygame.MOUSEBUTTONDOWN:
                    #self.clicks.append(pos)
                    #print(self.clicks)
                    # Jesli prouszasz obiektem i klikniesz
                    if self.moving_object:

                        if self.moving_object.name in attack_tower_names:
                            self.attack_towers.append(self.moving_object)
                        elif self.moving_object.name in support_tower_names:
                            self.support_towers.append(self.moving_object)

                        self.moving_object.moving = False
                        self.moving_object = None


                    else:
                        #klikniecie w menu boczne
                        side_menu_button = self.menu.get_clicked(pos[0], pos[1])
                        if side_menu_button:
                            cost = self.menu.get_item_cost(side_menu_button)
                            if self.money >= cost:
                                self.money -= cost
                                self.add_tower(side_menu_button)



                        # pokazuje zasieg po kliknieciu w wieze atakujaca lub wspierającą
                        btn_clicked = None
                        if self.selected_tower:
                            btn_clicked = self.selected_tower.menu.get_clicked(pos[0], pos[1])
                            if btn_clicked:
                                if btn_clicked == "Upgrade":
                                    cost = self.selected_tower.get_upgrade_cost()
                                    if self.money >= cost:
                                        self.money -= cost
                                        self.selected_tower.upgrade()

                        if not (btn_clicked):
                            for tw in self.attack_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False
                            # pokazuje zasieg po kliknieciu w wieze wspierajaca
                            for tw in self.support_towers:
                                if tw.click(pos[0], pos[1]):
                                    tw.selected = True
                                    self.selected_tower = tw
                                else:
                                    tw.selected = False



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
                self.money +=tw.attack(self.enemys)

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

        #Rysowanie ruchu obiektu
        if self.moving_object:
            self.moving_object.draw(self.win)

        #draw menu
        self.menu.draw(self.win)

        #Rysowanie życ
        text = self.life_font.render(str(self.lives), 1, (255,255,255))
        life = pygame.transform.scale(lives_img, (50,50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 13))
        self.win.blit(life, (start_x, 10))

        #Rysowanie pieniedzy
        text = self.life_font.render(str(self.money), 1, (255,255,255))
        money = pygame.transform.scale(star_img, (50,50))
        start_x = self.width - life.get_width() - 10

        self.win.blit(text, (start_x - text.get_width() - 10, 75))
        self.win.blit(money, (start_x, 65))

        pygame.display.update()

    def add_tower(self, name):
        x, y = pygame.mouse.get_pos()
        name_list = ["buy_archer","buy_archer_2","buy_damage","buy_range" ]
        object_list = [ArcherTowerLong(x,y), ArcherTowerShort(x,y), DamageTower(x,y), RangeTower(x,y)]

        try:
            obj = object_list[name_list.index(name)]
            self.moving_object = obj
            obj.moving = True
        except Exception as e:
            print(str(e) + "Nieprawidłowa nazwa")

g = Game()
g.run()