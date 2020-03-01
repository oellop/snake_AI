import curses
from curses import KEY_RIGHT, KEY_LEFT, KEY_DOWN, KEY_UP
from random import randint

HEIGHT = 25
WIDTH  = 35
TIMEOUT = 1000
BASE_LENGTH = 3

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
        print(self.tail)
        self.tail_end = self.tail[-1]
        self.score = 0
        self.window = window
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

    def eat_food(self):
        self.score+=1
        self.tail.append(self.tail_end)
        print(self.tail)

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
            print('crashed')
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

curses.initscr()
window = curses.newwin(HEIGHT, WIDTH, 0, 0)
window.timeout(TIMEOUT)
window.keypad(1)
curses.noecho()
curses.curs_set(0)
window.border(0)
exit = 0
snake = Snake(window)
food = Food(window)

while exit == 0:
    window.clear()
    window.border(0)
    snake.render()
    food.render()
    window.addstr(0, 0, 'Score : {}'.format(snake.score))
    event = window.getch()

    if event == 27:
        window.clear()
        window.addstr(0, 0, 'Game exited. Press space to restart or q to exit program')
        key = -1
        while key != 27 and key != 137:
            key = window.getch()

        if key == 137:
            exit = 1

        if key == 27:
            #TODO Initialize game
            exit = 1
    if snake.head_x == food.y and snake.head_y == food.x:
        snake.eat_food()
        food.delete(window)
        food = Food(window)

    if event in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
        snake.change_direction(event)

    snake.update()

    if snake.crashed==1 :
        print('chrr')
        window.clear()
        window.addstr(int(HEIGHT/2), int(WIDTH/2), 'You lost')
        window.border(0)
        key = -1
        while key != 27 and key != 137:
            key = window.getch()

curses.endwin()
