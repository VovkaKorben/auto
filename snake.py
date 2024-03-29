import pygame
import random

#################################################################
#
#   CONSTANTS
#

SQUARE_SIZE = 10
FIELD_SIZE_X = 50
FIELD_SIZE_Y = 40
BACKGROUND_COLOR = (0, 0, 0)
GRID_COLOR = (3, 20, 5)
SNAKE_COLOR = (73, 153, 0)
APPLE_COLOR = (177, 10, 20)
SCORE_COLOR = (250, 230, 0)
GAME_SPEED = 5
SPAWN_LEN = 5


def main():
    #################################################################
    #
    #   SERVICE ROUTINES
    #

    def create_apple(snake_body):
        while True:
            ax, ay = random.randint(0, FIELD_SIZE_X - 1), random.randint(0, FIELD_SIZE_Y - 1)
            if not (ax, ay) in snake_body:
                return (ax, ay)

    def reset_game():
        direction = 0
        cx, cy = FIELD_SIZE_X // 2, FIELD_SIZE_Y // 2
        cx += SPAWN_LEN // 2
        body = []
        for x in range(SPAWN_LEN):
            body.append((cx, cy))
            cx -= 1
        apple = create_apple(body)
        return direction, body, apple, 5

    #################################################################
    #
    #   INTIALIZATION PART
    #

    # initialize the pygame module
    pygame.init()
    pygame.display.set_caption("Snake game")

    # create a surface on screen
    screen = pygame.display.set_mode((FIELD_SIZE_X * SQUARE_SIZE + 1, FIELD_SIZE_Y * SQUARE_SIZE + 1))
    font = pygame.font.SysFont("arial.ttf", 26)

    # define a variables to control the main loop
    running = True
    clock = pygame.time.Clock()

    # init the snake with default parameters
    direction, body, apple, game_speed = reset_game()

    #################################################################
    #
    #   MAIN LOOP
    #

    while running:
        for event in pygame.event.get():
            # check if window closed
            if event.type == pygame.QUIT:
                running = False
                break

            #################################################################
            #
            #   PROCESS USER INPUT
            #

            # check user keys press
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break
                elif event.key == pygame.K_RIGHT:
                    direction = 0
                elif event.key == pygame.K_DOWN:
                    direction = 1
                elif event.key == pygame.K_LEFT:
                    direction = 2
                elif event.key == pygame.K_UP:
                    direction = 3

        #################################################################
        #
        #   NEW GAME STATE CALCULATE
        #

        # calculation new head position
        head_x, head_y = body[0]
        if direction == 0:
            head_x += 1
        elif direction == 1:
            head_y += 1
        elif direction == 2:
            head_x -= 1
        else:
            head_y -= 1

        # check for out of field and eating itself
        if head_x >= FIELD_SIZE_X or head_x < 0 or head_y >= FIELD_SIZE_Y or head_y < 0 or (head_x, head_y) in body:
            direction, body, apple, game_speed = reset_game()

        # apple eat
        elif (head_x, head_y) == apple:
            body.insert(0, (head_x, head_y))
            apple = create_apple(body)
            game_speed += 1

        # otherwise just move the snake
        else:
            body = body[:-1]
            body.insert(0, (head_x, head_y))

        #################################################################
        #
        #   DRAW GAME STATE TO THE SCREEN
        #

        # clear background
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 0, FIELD_SIZE_X * SQUARE_SIZE, FIELD_SIZE_Y * SQUARE_SIZE))

        # draw game grid
        for x in range(FIELD_SIZE_X + 1):
            pygame.draw.line(screen, GRID_COLOR, (x * SQUARE_SIZE, 0), ((x * SQUARE_SIZE, FIELD_SIZE_Y * SQUARE_SIZE)))
        for y in range(FIELD_SIZE_Y + 1):
            pygame.draw.line(screen, GRID_COLOR, (0, y * SQUARE_SIZE), ((FIELD_SIZE_X * SQUARE_SIZE, y * SQUARE_SIZE)))

        # draw score
        score_text = font.render("Score: {}".format(len(body) - SPAWN_LEN), True, SCORE_COLOR)
        screen.blit(score_text, (10, 10))

        # draw snake body
        for c in body:
            pygame.draw.rect(
                screen,
                SNAKE_COLOR,
                (c[0] * SQUARE_SIZE + 1, c[1] * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1),
            )

        # draw the apple
        pygame.draw.rect(
            screen,
            APPLE_COLOR,
            (apple[0] * SQUARE_SIZE + 1, apple[1] * SQUARE_SIZE + 1, SQUARE_SIZE - 1, SQUARE_SIZE - 1),
        )

        # show all drawed things to the user
        pygame.display.update()

        clock.tick(game_speed)


if __name__ == "__main__":
    main()
