import math
import random
import pygame

from Util import *
from Settings import *


class Ball:

    def __init__(self, window, color, x, y):
        self.window = window
        self.color = color

        self.x = x
        self.y = y

        self.original_x = x
        self.original_y = y

        self.x_vel, self.y_vel = self.define_starting_direction()

    def draw(self):
        draw_circle(self.window, self.color, self.x, self.y, BALL_RADIUS)

    def move(self):
        self.x = self.x + self.x_vel
        self.y = self.y + self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.x_vel, self.y_vel = self.define_starting_direction()

    def define_starting_direction(self):
        # Defines a random starting direction of the ball.
        angle = 0
        while angle == 0:
            angle = math.radians(random.randrange(-30, 30))
        pos = 1 if random.random() < 0.5 else -1
        x_vel = pos * abs(math.cos(angle) * BALL_MAX_VEL)
        y_vel = math.sin(angle) * BALL_MAX_VEL
        return x_vel, y_vel

    # Used for powerups
    def change_speed(self, delta):
        # Change the speed of the ball in x and y direction by the specified delta
        pass
