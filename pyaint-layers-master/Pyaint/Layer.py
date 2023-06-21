import pygame.sprite

from utils.button import Button
from utils.settings import *


class Layer():

    def __init__(self, x, y, layer_id):
        self.id = layer_id
        self.layer_button = Button(
            x, y, 40, 40, WHITE, "L" + str(layer_id), BLACK, name=str(self.id))

        self.selection_button = Button(
            x + 45, y + 10, 20, 20, WHITE, name="L" + str(self.id))

        self.visible_grid = self.init_grid(ROWS, COLS, BG_COLOR)
        self.grid = self.visible_grid

    def get_button(self):
        return self.layer_button

    def __eq__(self, other):
        return self.id == other.id

    def init_grid(self, rows, columns, color):
        grid = []
        for i in range(rows):
            grid.append([])
            for _ in range(columns):  # use _ when variable is not required
                grid[i].append(color)
        return grid

    def reset_grid(self):
        self.visible_grid = self.init_grid(ROWS, COLS, BG_COLOR)
