# Game over scenario and pausing a game
import pygame
from pygame.locals import *
import time
import random
import sys

SIZE = 40

class Apple:
    def __init__(self, parent_screen):
        image = ["fruits/fruit_1.png", "fruits/fruit_2.png", "fruits/fruit_3.png", "fruits/fruit_4.png", "fruits/fruit_5.png", "fruits/fruit_6.png", "fruits/fruit_7.png", "fruits/fruit_8.png","fruits/fruit_9.png" ]
        select = random.choice(image)
        self.parent_screen = parent_screen
        self.image = pygame.image.load(select).convert_alpha()
        self.x = 120
        self.y = 120

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        image = ["fruits/fruit_1.png", "fruits/fruit_2.png", "fruits/fruit_3.png", "fruits/fruit_4.png", "fruits/fruit_5.png", "fruits/fruit_6.png", "fruits/fruit_7.png", "fruits/fruit_8.png","fruits/fruit_9.png" ]
        select = random.choice(image)
        self.image = pygame.image.load(select).convert_alpha()
        self.x = random.randint(1,18)*SIZE
        self.y = random.randint(1,14)*SIZE

class Snake:
    def __init__(self, parent_screen):
        smake_blocks = ["snake_blocks/dark_blue.jpg", "snake_blocks/blue.jpg", "snake_blocks/orange.jpg", "snake_blocks/pink.jpg", "snake_blocks/Yellow.jpg", "snake_blocks/violet.jpg"]
        block = random.choice(smake_blocks)
        self.parent_screen = parent_screen
        self.image = pygame.image.load(block).convert_alpha()
        self.direction = 'down'

        self.length = 1
        self.x = [40]
        self.y = [40]

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def walk(self):
        # update body
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]

        # update head
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE

        self.draw()

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))
        pygame.display.flip()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_background_music()
        pygame.display.set_caption("Snake and fruit Game")
        self.surface = pygame.display.set_mode((800, 617))
        self.snake = Snake(self.surface)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()

    def render_background(self):
        bg = pygame.image.load("background.jpg")
        self.surface.blit(bg, (0,0))

    def reset(self):
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True
        return False

    def play_background_music(self):
        pygame.mixer.music.load('tones/Background music.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0)

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake eating apple scenario
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("tones/ding.mp3")
            self.snake.increase_length()
            self.apple.move()

        # snake colliding with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("tones/crash.mp3")
                raise "Collision occured"

    def display_score(self):
        font = pygame.font.SysFont('arial',30)
        score = font.render(f"Score: {self.snake.length}",True,(250,250,250))
        self.surface.blit(score,(690,5))

    def play_sound(self, sound):
        audio = pygame.mixer.Sound(sound)
        pygame.mixer.Sound.play(audio)
        
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game over! Your score is {self.snake.length}.", True, (247, 107, 7))
        self.surface.blit(line1, (250,300))
        line2 = font.render("To play again press Enter. To exit press Escape!", True, (247, 7, 7))
        self.surface.blit(line2, (150, 350))
        pygame.mixer.music.pause()

        pygame.display.flip()

    def run(self):
        running = True
        pause = False

        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        self.play_background_music()
                        pause = False

                    if not pause:
                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False
            try:

                if not pause:
                    self.play()

            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.25)

if __name__ == '__main__':
    game = Game()
    game.run()