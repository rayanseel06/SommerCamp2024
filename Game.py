import random

import pygame

from Paddle import Paddle
from Ball import Ball
from Settings import *

pygame.init()


class Game:

    def __init__(self, window):
        self.window = window

        x_left = 10
        x_right = WIN_WIDTH - 10 - PADDLE_WIDTH
        y = (WIN_HEIGHT - PADDLE_HEIGHT) // 2
        self.left_paddle = Paddle(window, WHITE, x_left, y)
        self.right_paddle = Paddle(window, WHITE, x_right, y)

        self.ball = Ball(window, WHITE, WIN_WIDTH // 2, WIN_HEIGHT // 2)

        self.left_score = 0
        self.right_score = 0
        self.left_hits = 0

    def draw(self):
        # This is our central draw method. If we want to display something on the screen, we have to add it in here.

        # Define the background.
        if BG_IMG is None:
            # Fill the background with a specified color.
            self.window.fill(BLACK)
        else:
            # Fill the background with an image you can specify in the Settings.py file.
            self.window.blit(BG_IMG, (0, 0))

        # Draw the dividing lines in the middle
        self.draw_divider()

        # Draw the paddles
        self.left_paddle.draw()
        self.right_paddle.draw()

        # Draw the ball
        self.ball.draw()

        # Draw the score
        self.draw_score()

        # We have to call this one to make sure our drawings get displayed.
        pygame.display.update()

    def draw_divider(self):
        # Draws the dividing lines in the middle of the screen.
        for i in range(10, WIN_HEIGHT, WIN_HEIGHT // 5):
            pygame.draw.rect(self.window, WHITE, (WIN_WIDTH // 2 - 5, i, 10, WIN_HEIGHT // 15))

    def draw_text(self, text, x, y, color=WHITE) -> None:
        text = FONT.render(text, True, color)
        x = x - text.get_width() // 2
        self.window.blit(text, (x, y))

    def move_paddle_keys(self, keys):
        left_paddle_up_key = pygame.K_w
        left_paddle_down_key = pygame.K_s
        right_paddle_up_key = pygame.K_UP
        right_paddle_down_key = pygame.K_DOWN

        # Move left paddle upwards with w and downwards with s
        if keys[left_paddle_up_key]:
            upwards = True
            self.left_paddle.move(upwards)
        if keys[left_paddle_down_key]:
            upwards = False
            self.left_paddle.move(upwards)

        # Move right paddle upwards with up arrow and downwards with down arrow
        if keys[right_paddle_up_key]:
            upwards = True
            self.right_paddle.move(upwards)
        if keys[right_paddle_down_key]:
            upwards = False
            self.right_paddle.move(upwards)

    def handle_collision(self):
        if self.ball_hits_ceiling_or_floor():
            self.ball.y_vel *= -1
            self.ball.y_vel += random.uniform(-1, 1)  # Avoid ball getting stuck on edges

        if self.ball_hits_paddle(self.left_paddle):
            self.left_score += 1
            self.handle_paddle_collision(self.left_paddle)
        elif self.ball_hits_paddle(self.right_paddle):
            self.handle_paddle_collision(self.right_paddle)

    def ball_hits_ceiling_or_floor(self):
        return self.ball.y >= WIN_HEIGHT or self.ball.y <= 0

    def ball_hits_paddle(self, paddle):
        return ((paddle.x <= self.ball.x <= paddle.x + PADDLE_WIDTH) and
                (paddle.y <= self.ball.y <= paddle.y + PADDLE_HEIGHT))

    def handle_paddle_collision(self, paddle):
        # Reverse direction
        self.ball.x_vel *= - 1

        # Change y_vel based on where we hit the paddle
        middle_y = paddle.y + PADDLE_HEIGHT / 2
        difference_y = middle_y - self.ball.y
        reduction_factor = (PADDLE_HEIGHT / 2) / BALL_MAX_VEL
        y_vel = difference_y / reduction_factor
        y_vel = BALL_MAX_VEL if abs(y_vel) > BALL_MAX_VEL else y_vel
        y_vel += random.uniform(-1, 1)  # Avoid endless loops without having to move the paddle
        self.ball.y_vel = -1 * y_vel

    def draw_score(self):
        one_fourth_window_width = WIN_WIDTH // 4
        three_fourths_window_width = WIN_WIDTH * (3 / 4)

        self.draw_text(str(self.left_score), one_fourth_window_width, 20)
        self.draw_text(str(self.right_score), three_fourths_window_width, 20)

    def draw_winning_text(self, player_name):
        self.draw()
        self.draw_text(player_name + " Player Won", WIN_WIDTH // 2, WIN_HEIGHT // 2 - 90)
        pygame.display.update()
        pygame.time.delay(5000)

    def check_winning_condition(self):
        left_player_won = self.left_score >= WINNING_SCORE
        right_player_won = self.right_score >= WINNING_SCORE

        if left_player_won:
            self.draw_winning_text("Left")
            return True
        elif right_player_won:
            self.draw_winning_text("Right")
            return True
        else:
            return False

    # endregion

    # region TODO (B) Output handling
    def move_paddle_networks(self, is_left, network_output):
        if network_output == 0:
            pass

        # 1 means we move upwards
        elif network_output == 1:
            if is_left:
                self.left_paddle.move(True)
            else:
                self.right_paddle.move(True)

        # 2 means we move downwards
        else:
            if is_left:
                self.left_paddle.move(False)
            else:
                self.right_paddle.move(False)

    # endregion
