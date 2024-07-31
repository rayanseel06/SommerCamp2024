import pygame

from Util import *
from Settings import *


class Paddle:
    def __init__(self, window, color, x, y):
        self.window = window
        self.color = color
        self.x = x
        self.y = y

    def draw(self):
        draw_rectangle(self.window, self.color, self.x, self.y, PADDLE_WIDTH, PADDLE_HEIGHT)

    def move(self, upwards):
        if upwards:
            self.y = self.y - PADDLE_VEL
            if self.y < 0:
                self.y = 0
        else:
            self.y = self.y + PADDLE_VEL
            if self.y + PADDLE_HEIGHT > WIN_HEIGHT:
                self.y = WIN_HEIGHT - PADDLE_HEIGHT

