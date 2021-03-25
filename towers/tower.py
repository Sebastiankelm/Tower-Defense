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
        self. selected = False
        self.menu = None
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

    def click(self, X, Y):
        """
        Zwraca gdy kliknięto na wieżę
        i zaznacza wieżę gdy jest kliknięta
        :param x: int
        :param y: int
        :return: bool
        """
        if X <= self.x + self.width and X >= self.x:
            if Y <= self.y + self.height and Y >= self.y:
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
        self.level += 1
        self.damage += 1

    def get_upgrade_cost(self):
        """
        zwraca koszt ulepszenia, jeśli 0, to nie może  ulepszać
        :return: int
        """
        return self.price(self.level-1)

    def move(self, x, y):
        self.x = x
        self.y = y