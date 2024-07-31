from Game import Game
from Settings import *

if __name__ == "__main__":
    # Set the window width and height and initialise the game.
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("2-Player Mode")
    game = Game(window)

    # Game loop which gets repeated all the time.
    run = True
    clock = pygame.time.Clock()  # The clock helps us to limit the upper frame rate.
    while run:
        clock.tick(FPS)
        game.draw()

        # This for loop is responsible for closing the window if we click on the red close button.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Move the paddles
        keys = pygame.key.get_pressed()
        game.move_paddle_keys(keys)

        # Move the ball
        game.ball.move()

        # Collision detection
        game.handle_collision()

        # Reset the ball
        if game.ball.x < 0:
            game.right_score = game.right_score + 1
            game.ball.reset()
        elif game.ball.x > WIN_WIDTH:
            game.left_score = game.left_score + 1
            game.ball.reset()

        # Check if one player has won the game
        if game.check_winning_condition():
            run = False

    # End the Game
    pygame.quit()
