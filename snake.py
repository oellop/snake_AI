import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randint

HEIGHT = 25
WIDTH  = 35
BASE_LENGTH = 3
TIMEOUT = 100

class Snake(object):
    def __init__(self, windows):
        self.head_char = '0'
        self.tail_char = '='
        self.head_x = 5
        self.head_y = 5
        self.tail = []
        self.crashed = 0

        for i in range(1, BASE_LENGTH):
            self.tail.append([self.head_y-i, self.head_x])

        self.tail_end = self.tail[-1]
        self.score = 0
        self.window = windows
        self.direction = KEY_RIGHT
        self.direction_map = {
            KEY_UP: self.move_up,
            KEY_DOWN: self.move_down,
            KEY_LEFT: self.move_left,
            KEY_RIGHT: self.move_right
        }

    def render(self):
        self.window.addstr(self.head_x, self.head_y, self.head_char)
        self.window.addstr(0, 20, '{}'.format(self.tail_end))
        for (x,y) in self.tail:
            self.window.addstr(y, x, self.tail_char)

    def eat_food(self, window):
        self.score+=1
        self.tail.append(self.tail_end)
        self.window.timeout(TIMEOUT - 3 * self.score)

    def move_up(self):
        self.head_x -= 1
        if self.head_x < 1:
            self.head_x = HEIGHT - 2

    def move_down(self):
        self.head_x += 1
        if self.head_x > HEIGHT - 2:
            self.head_x = 1

    def move_left(self):
        self.head_y -= 1
        if self.head_y < 1:
            self.head_y = WIDTH - 2

    def move_right(self):
        self.head_y += 1
        if self.head_y > WIDTH - 2:
            self.head_y = 1

    def change_direction(self, dir):
        self.direction = dir

    def update(self):
        last_coord = [self.head_y, self.head_x]
        if last_coord in self.tail:
            self.crashed = 1

        self.direction_map[self.direction]()
        for i in range(len(self.tail)):
            (last_coord[0], last_coord[1]), (self.tail[i][0], self.tail[i][1]) = (self.tail[i][0], self.tail[i][1]), (last_coord[0], last_coord[1])

        self.tail_end = [last_coord[0], last_coord[1]]


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

    def __init__(self):
        curses.initscr()
        self.window = curses.newwin(HEIGHT, WIDTH, 0, 0)
        self.window.keypad(1)
        self.window.timeout(TIMEOUT)
        curses.noecho()
        curses.curs_set(0)
        self.window.border(0)
        self.exit = 0
        self.snake = Snake(self.window)
        self.food = Food(self.window)
        self.running()

    def running(self):
        while self.exit == 0:
            self.window.clear()
            self.window.border(0)
            self.snake.render()
            self.food.render()
            self.window.addstr(0, 0, 'Score : {}'.format(self.snake.score))
            self.event = self.window.getch()

            if self.event == 27:
                self.window.clear()
                self.window.addstr(0, 0, 'Game exited. Press space to restart or q to exit program')
                self.key = -1
                while self.key != 27 and self.key != 137:
                    self.key = self.window.getch()

                if self.key == 137:
                    self.exiting()
                    break

                if self.key == 27:
                    self.exiting()
                    break

            if self.snake.head_x == self.food.y and self.snake.head_y == self.food.x:
                self.snake.eat_food(self.window)
                self.food.delete(self.window)
                self.food = Food(self.window)

            if self.event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
                self.snake.change_direction(self.event)

            self.snake.update()

            if self.snake.crashed==1 :
                self.exiting()
                break


    def exiting(self):
        self.window.clear()
        self.window.addstr(int(HEIGHT/2), int(WIDTH/2) - 4 , 'You lost')
        self.window.addstr(int(HEIGHT/2) + 1, int(WIDTH/2) - 5, 'Score : {}'.format(self.snake.score))
        self.window.addstr(int(HEIGHT/2) + 2, int(WIDTH/2) - 8 , 'Press ESQ to quit')
        self.window.border(0)
        self.key = -1
        while self.key != 27:
            self.key = self.window.getch()

        curses.endwin()


App = GameApp()
