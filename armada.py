from alien import Alien

class Armada:
    def __init__(self, game):
        self.rows = 3
        self.columns = 7
        self.aliens = {}

        self.height = ...
        self.width = ...
        self.reference_alien = Alien()
        self.row_gutter = (self.height - self.reference_alien.rect.height * self.rows) / (self.rows - 1)
        self.column_gutter = (self.width - self.reference_alien.rect.width * self.columns) / (self.columns - 1)


