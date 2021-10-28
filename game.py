"""
Snake Eater
Made with PyGame
"""

import pygame, sys, time, random, os


class Player:
    def __init__(self, name, score) -> None:
        self.name = name
        self.score = score
    def __repr__(self) -> str:
        return f'score: {self.score}; name: {self.name}'


# Difficulty settings
# Easy      ->  10
# Medium    ->  25
# Hard      ->  40
# Harder    ->  60
# Impossible->  120
difficulty = 25

# Window size
frame_size_x = int(720*1.5)
frame_size_y = int(480*1.5)

# Checks for errors encountered
check_errors = pygame.init()
# pygame.init() example output -> (6, 0)
# second number in tuple gives number of errors
if check_errors[1] > 0:
    print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
    sys.exit(-1)
else:
    print('[+] Game successfully initialised')


# Initialise game window
pygame.display.set_caption('Snake Eater')
game_window = pygame.display.set_mode((frame_size_x, frame_size_y))


# Colors (R, G, B)
black = pygame.Color(0, 0, 0)
white = pygame.Color(255, 255, 255)
red = pygame.Color(255, 0, 0)
green = pygame.Color(0, 255, 0)
blue = pygame.Color(0, 0, 255)


# FPS (frames per second) controller
fps_controller = pygame.time.Clock()


# Game variables
snake_pos = [100, 50]
snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
food_spawn = True

direction = 'RIGHT'
change_to = direction

score = 0
name = ''

INGAME = False
INPUTING = False
SCOREBOARD = []

try:
    f = open('leaderboard')
    lines = f.read().split('\n')
    for i in lines:
        if len(i)<1:
            continue
        SCOREBOARD.append(Player(i.split('|')[0], int(i.split('|')[1])))
except OSError:
    print('error loading scoreboard')

def export():
    f = open('leaderboard', 'w')
    lines =[]
    for i in SCOREBOARD:
        lines.append(f'{i.name}|{i.score}')
    f.write('\n'.join(lines))



# Game Over
def game_over():
    my_font = pygame.font.SysFont('times new roman', 90)
    game_over_surface = my_font.render('YOU DIED', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/4)
    game_window.fill(black)
    game_window.blit(game_over_surface, game_over_rect)

    sc = [i for i in SCOREBOARD]
    s = Player('a', score)

    sc.append(s)
    print(sc)
    sc.sort(key=lambda c: c.score, reverse=True)

    ranking = 0

    for i in range(len(sc)):
        if sc[i].score == s.score:
            ranking = i+1

    my_font = pygame.font.SysFont('times new roman', 20)
    game_over_surface = my_font.render(f'rankings: {ranking}', True, red)
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (frame_size_x/2, frame_size_y/2)
    game_window.blit(game_over_surface, game_over_rect)

    show_score(0, red, 'times', 20)
    pygame.display.flip()
    time.sleep(3)

    # pygame.quit()
    # sys.exit()


# Score
def show_score(choice, color, font, size):
    score_font = pygame.font.SysFont(font, size)
    score_surface = score_font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    if choice == 1:
        score_rect.midtop = (frame_size_x/10, 15)
    else:
        score_rect.midtop = (frame_size_x/2, frame_size_y/1.25)
    game_window.blit(score_surface, score_rect)
    # pygame.display.flip()


# Main logic

def main():

    global difficulty, frame_size_x, frame_size_y, check_errors, game_window, black, white, red, green, blue, fps_controller, snake_pos, snake_body
    global food_pos, food_spawn, direction, change_to, score, INGAME, SCOREBOARD, name, INPUTING


    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                if INGAME:
                    # W -> Up; S -> Down; A -> Left; D -> Right
                    if event.key == pygame.K_UP or event.key == ord('w'):
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN or event.key == ord('s'):
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT or event.key == ord('a'):
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT or event.key == ord('d'):
                        change_to = 'RIGHT'
                    # # Esc -> Create event to quit the game
                    # if event.key == pygame.K_ESCAPE:
                    #     pygame.event.post(pygame.event.Event(pygame.QUIT))
                    
                
                elif INPUTING:
                    
                    if event.key != pygame.K_RETURN:
                        
                        if event.key == pygame.K_BACKSPACE:
                            name = name[:-1]
                            print(len(name))
                        elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                            break;
                        else:
                            try:
                                name += chr(event.key)
                            except ValueError:
                                pass
                    else:
                        INPUTING = False
                        INGAME = True

                else: # viewing scoreboard
                    
                    if event.key == pygame.K_SPACE or event.key == ord(' '):
                        
                        INPUTING = True
                        print("2"+str(INPUTING))
                        

        # Making sure the snake cannot move in the opposite direction instantaneously
        

        if INGAME:
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'

            # Moving the snake
            if direction == 'UP':
                snake_pos[1] -= 10
            if direction == 'DOWN':
                snake_pos[1] += 10
            if direction == 'LEFT':
                snake_pos[0] -= 10
            if direction == 'RIGHT':
                snake_pos[0] += 10

            # Snake body growing mechanism
            snake_body.insert(0, list(snake_pos))
            if snake_pos[0] == food_pos[0] and snake_pos[1] == food_pos[1]:
                score += 1
                food_spawn = False
            else:
                snake_body.pop()

            # Spawning food on the screen
            if not food_spawn:
                food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
            food_spawn = True

            # GFX
            game_window.fill(black)
            for pos in snake_body:
                # Snake body
                # .draw.rect(play_surface, color, xy-coordinate)
                # xy-coordinate -> .Rect(x, y, size_x, size_y)
                pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

            # Snake food
            pygame.draw.rect(game_window, white, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

            # Game Over conditions
            # Getting out of bounds
            if snake_pos[0] < 0 or snake_pos[0] > frame_size_x-10:
                game_over()
                INGAME = False
            if snake_pos[1] < 0 or snake_pos[1] > frame_size_y-10:
                game_over()
                INGAME = False
            # Touching the snake body
            for block in snake_body[1:]:
                if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                    game_over()
                    INGAME = False

            show_score(1, white, 'consolas', 20)

            if(not INGAME):
                snake_pos = [100, 50]
                snake_body = [[100, 50], [100-10, 50], [100-(2*10), 50]]

                food_pos = [random.randrange(1, (frame_size_x//10)) * 10, random.randrange(1, (frame_size_y//10)) * 10]
                food_spawn = True

                direction = 'RIGHT'
                change_to = direction

                p = Player(name, score)

                SCOREBOARD.append(p)
                SCOREBOARD.sort(key=lambda c: c.score, reverse=True)

                export()

                score = 0
                name = ''
                
            # Refresh game screen
            pygame.display.update()
            # Refresh rate
            fps_controller.tick(difficulty)

        else:
            # if viewing scoreboard
            game_window.fill(black)
            if(not INPUTING):
                
                score_font = pygame.font.SysFont("times", 40)
                score_surface = score_font.render('!Welcome to the Snake Game!', True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (frame_size_x/2, frame_size_y/10)
                game_window.blit(score_surface, score_rect)

                score_font = pygame.font.SysFont("times", 30)
                score_surface = score_font.render('Leaderboard', True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (frame_size_x/2, frame_size_y/10 + 60)
                game_window.blit(score_surface, score_rect)

                score_surface = score_font.render('!Press Space To Start!', True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (frame_size_x/2, frame_size_y-frame_size_y/6)
                game_window.blit(score_surface, score_rect)

                score_surface = score_font.render(f'{len(SCOREBOARD)} Players', True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (100, frame_size_y/2)
                game_window.blit(score_surface, score_rect)

                score_font = pygame.font.SysFont("times", 20)

                score_surface = score_font.render('Reworked By Andy Yang', True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (110, frame_size_y-50)
                game_window.blit(score_surface, score_rect)
                score_surface = score_font.render('Class of 2023', True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (60, frame_size_y-25)
                game_window.blit(score_surface, score_rect)

                score_surface = score_font.render('Tech Solution Team', True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (frame_size_x-100, frame_size_y-25)
                game_window.blit(score_surface, score_rect)

                score_surface = score_font.render('Original Author: rajatdiptabiswas', True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (frame_size_x/2, frame_size_y-20)
                game_window.blit(score_surface, score_rect)



                for i in range(len(SCOREBOARD)):
                    if(i>11):
                        break

                    score_surface = score_font.render(f'{SCOREBOARD[i].name} : {SCOREBOARD[i].score}', True, white)
                    score_rect = score_surface.get_rect()
                    score_rect.midtop = (frame_size_x/2, frame_size_y/10+100+30*i)
                    game_window.blit(score_surface, score_rect)

            else:
                score_font = pygame.font.SysFont("times", 40)
                score_surface = score_font.render('Enter Your Name', True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (frame_size_x/2, frame_size_y/10)
                game_window.blit(score_surface, score_rect)

                score_font = pygame.font.SysFont("times", 30)
                score_surface = score_font.render(name, True, white)
                score_rect = score_surface.get_rect()
                score_rect.midtop = (frame_size_x/2, frame_size_y/10+60)
                game_window.blit(score_surface, score_rect)


            # Refresh game screen
            pygame.display.update()
            # Refresh rate
            fps_controller.tick(difficulty)




if __name__ == "__main__":
    main()