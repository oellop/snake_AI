import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from numpy import arctan, pi, sqrt, arccos, max, argmax, expand_dims, reshape, min, mean
from random import randint
import sys
from genetic_algorithm import *


HEIGHT = 25
WIDTH  = 35
WIDTH_APP = WIDTH + 20
BASE_LENGTH = 3
TIMEOUT = 10

class Snake(object):
    def __init__(self, windows, auto = 0):
        self.head_char = '0'
        self.tail_char = '='
        self.head_y = randint(5, WIDTH - 5)
        self.head_x = randint(5, HEIGHT - 5)
        self.tail = []
        self.crashed = 0
        self.angle = 0
        self.top_dist = 0
        self.down_dist = 0
        self.right_dist = 0
        self.left_dist = 0
        self.obs_top = 0
        self.obs_down = 0
        self.obs_left = 0
        self.obs_right = 0
        self.count = 0
        self.dist_list = []
        self.count_score = 0
        self.obs_wall = 0

        for i in range(1, BASE_LENGTH):
            self.tail.append([self.head_y-i, self.head_x])

        self.tail_end = self.tail[-1]
        self.score = 0
        self.window = windows
        self.direction = KEY_RIGHT
        if auto == 0:
            self.direction_map = {
                KEY_UP: self.move_up,
                KEY_DOWN: self.move_down,
                KEY_LEFT: self.move_left,
                KEY_RIGHT: self.move_right
            }
        else:
            self.direction_map = {
                0: self.move_up,
                1: self.move_down,
                2: self.move_left,
                3: self.move_right
            }


    def render(self):
        self.window.addstr(self.head_x, self.head_y, self.head_char)

        for (x,y) in self.tail:
            self.window.addstr(y, x, self.tail_char)

        self.window.addstr(1, WIDTH+1, 'top dist : {0:.2f}'.format((self.top_dist)))
        self.window.addstr(2, WIDTH+1, 'down dist : {0:.2f}'.format((self.down_dist)))
        self.window.addstr(3, WIDTH+1, 'left dist : {0:.2f}'.format((self.left_dist)))
        self.window.addstr(4, WIDTH+1, 'right dist : {0:.2f}'.format((self.right_dist)))
        self.window.addstr(5, WIDTH+1, 'obs top : {}'.format(int(self.obs_top)))
        self.window.addstr(6, WIDTH+1, 'obs down : {}'.format(int(self.obs_down)))
        self.window.addstr(7, WIDTH+1, 'obs left : {}'.format(int(self.obs_left)))
        self.window.addstr(8, WIDTH+1, 'obs right : {}'.format(int(self.obs_right)))

    def eat_food(self, window):
        self.score+=1
        self.count_score = 0
        self.tail.append(self.tail_end)
        self.window.timeout(TIMEOUT - 3 * self.score)

    def move_up(self):
        self.head_x -= 1
        if self.head_x < 1:
            self.obs_wall = 1
            # self.head_x = HEIGHT - 2

    def move_down(self):
        self.head_x += 1
        if self.head_x > HEIGHT - 2:
            self.obs_wall = 1
            # self.head_x = 1

    def move_left(self):
        self.head_y -= 1
        if self.head_y < 1:
            self.obs_wall = 1
            # self.head_y = WIDTH - 2

    def move_right(self):
        self.head_y += 1
        if self.head_y > WIDTH - 2:
            self.obs_wall = 1
            # self.head_y = 1

    def change_direction(self, dir):
        if self.direction == dir:
            self.count +=1
        else:
            self.count = 0

        if self.count == 60:
            self.crashed = 1


        self.direction = dir

    def update(self, food):
        self.count_score+=1
        if self.count_score == 60:
            self.crashed = 1

        if self.obs_wall == 1:
            self.crashed = 1

        last_coord = [self.head_y, self.head_x]

        if last_coord in self.tail:
            self.crashed = 1
        mod = sqrt((food.y - self.head_x)*(food.y - self.head_x) + (food.x - self.head_y)*(food.x - self.head_y))

        self.direction_map[self.direction]()
        for i in range(len(self.tail)):
            (last_coord[0], last_coord[1]), (self.tail[i][0], self.tail[i][1]) = (self.tail[i][0], self.tail[i][1]), (last_coord[0], last_coord[1])

        self.tail_end = [last_coord[0], last_coord[1]]

    def collide_wall(self, x, y):
        wall = 0
        if x < 1:
            wall = 1

        if x > HEIGHT - 2:
            wall = 1
            # self.head_x = 1

        if y < 1:
            wall = 1

        if y > WIDTH - 2:
            wall = 1

        return wall


    def get_input_NN(self, food):

        self.down_dist = sqrt((food.y - self.head_x -1)*(food.y - self.head_x - 1) + (food.x - self.head_y)*(food.x - self.head_y))
        self.top_dist = sqrt((food.y - self.head_x + 1)*(food.y - self.head_x + 1) + (food.x - self.head_y)*(food.x - self.head_y))
        self.right_dist = sqrt((food.y - self.head_x)*(food.y - self.head_x) + (food.x - self.head_y - 1)*(food.x - self.head_y - 1))
        self.left_dist = sqrt((food.y - self.head_x)*(food.y - self.head_x) + (food.x - self.head_y + 1)*(food.x - self.head_y + 1))

        max_dist = max([self.down_dist, self.top_dist, self.right_dist, self.left_dist])

        self.down_dist/=max_dist
        self.top_dist/=max_dist
        self.left_dist/=max_dist
        self.right_dist/=max_dist

        self.dist_list.append(min([self.down_dist, self.top_dist, self.right_dist, self.left_dist]))

        self.obs_left = 1 if ([self.head_y - 1, self.head_x] in self.tail) or self.collide_wall(self.head_x, self.head_y - 1) else 0
        self.obs_right = 1 if [self.head_y + 1, self.head_x] in self.tail or self.collide_wall(self.head_x, self.head_y + 1) else 0
        self.obs_down = 1 if [self.head_y, self.head_x + 1] in self.tail or self.collide_wall(self.head_x + 1, self.head_y) else 0
        self.obs_top = 1 if [self.head_y, self.head_x - 1] in self.tail or self.collide_wall(self.head_x - 1, self.head_y) else 0

        return self.top_dist, self.down_dist, self.right_dist, self.left_dist, self.obs_top, self.obs_down, self.obs_left, self.obs_right

class Food(object):
    def __init__(self, window, char='Q'):
        self.y = randint(1, HEIGHT - 2)
        self.x = randint(1, WIDTH - 2)
        self.char = char
        self.window = window

    def render(self):
        self.window.addstr(self.y, self.x, self.char)

    def delete(self, window):
        self.window.delch(self.y, self.x)

class GameApp(object):

    def __init__(self, model = None, auto = 0):
        curses.initscr()
        self.window = curses.newwin(HEIGHT, WIDTH_APP, 0, 0)
        self.window.keypad(1)
        self.window.timeout(TIMEOUT)
        curses.noecho()
        curses.curs_set(0)
        self.window.border(0)
        self.exit = 0
        self.model = model
        self.auto = auto
        self.score = 0
        self.mean_dist = 0

    def start(self, model = None):
        self.snake = Snake(self.window, self.auto)
        self.food = Food(self.window)
        self.running()
        if self.auto == 1:
            curses.endwin()

    @property
    def set_model(self, _model):
        self.model = _model

    def running(self):
        while self.exit == 0:
            self.window.clear()
            self.window.border(0)
            self.window.vline(0, WIDTH,'|', HEIGHT)
            self.snake.render()
            self.food.render()
            self.window.addstr(0, 0, 'Score : {}'.format(self.snake.score))
            self.event = self.window.getch()

            if self.event == 27:
                self.window.clear()
                self.window.addstr(0, 0, 'Game paused.\nPress space to continue or esc to exit.')
                self.key = -1
                while self.key != 27 and self.key != 32:
                    self.key = self.window.getch()

                if self.key == 27:
                    self.exiting()
                    break

            if self.snake.head_x == self.food.y and self.snake.head_y == self.food.x:
                self.snake.eat_food(self.window)
                self.food.delete(self.window)
                self.food = Food(self.window)

            input = self.snake.get_input_NN(self.food)

            input = expand_dims(input, axis= 0)
            input = expand_dims(input, axis= 0)
            if self.auto == 0:
                if self.event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
                    self.snake.change_direction(self.event)
            else:

                self.snake.change_direction(np.argmax(self.model.predict(input)))


            self.snake.update(self.food)

            if self.snake.crashed==1 :

                self.exit = 1
                self.score = self.snake.score
                self.mean_dist = mean(self.snake.dist_list)
                if self.auto == 0:
                    self.exit = 0
                    self.exiting()

                break


    def exiting(self):
        self.window.clear()
        self.window.addstr(int(HEIGHT/2), int(WIDTH/2) - 4 , 'You lost')
        self.window.addstr(int(HEIGHT/2) + 1, int(WIDTH/2) - 5, 'Score : {}'.format(self.snake.score))
        self.window.addstr(int(HEIGHT/2) + 2, int(WIDTH/2) - 15 , 'Press ESQ to quit or press space')
        self.window.addstr(int(HEIGHT/2) + 2, int(WIDTH/2) - 5 , 'to restart')
        self.window.border(0)
        self.window.vline(0, WIDTH,'|', HEIGHT)
        self.key = -1
        while self.key != 27 and self.key != 32:
            self.key = self.window.getch()
        if self.key==27:
            curses.endwin()
        if self.key==32:
            self.start()

# model = create_model()
# App = GameApp( auto = 0)
# App.start()
