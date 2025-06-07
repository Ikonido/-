import curses
import random

KEY_ESC = 27

class SnakeGame:
    def __init__(self, screen, width=40, height=20):
        self.screen = screen
        self.width = width
        self.height = height
        self.snake = [(height // 2, width // 2)]
        self.direction = (0, 1)  # moving right
        self.food = self._place_food()
        self.score = 0

    def _place_food(self):
        while True:
            pos = (random.randint(1, self.height - 2), random.randint(1, self.width - 2))
            if pos not in self.snake:
                return pos

    def _draw_borders(self):
        for x in range(self.width):
            self.screen.addch(0, x, '#')
            self.screen.addch(self.height - 1, x, '#')
        for y in range(self.height):
            self.screen.addch(y, 0, '#')
            self.screen.addch(y, self.width - 1, '#')

    def _render(self):
        self.screen.clear()
        self._draw_borders()
        for y, x in self.snake:
            self.screen.addch(y, x, 'o')
        fy, fx = self.food
        self.screen.addch(fy, fx, '*')
        self.screen.addstr(self.height, 0, f'Score: {self.score}')
        self.screen.refresh()

    def _move_snake(self):
        head_y, head_x = self.snake[0]
        dy, dx = self.direction
        new_head = (head_y + dy, head_x + dx)
        if (new_head[0] in [0, self.height - 1] or
                new_head[1] in [0, self.width - 1] or
                new_head in self.snake):
            return False
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            self.food = self._place_food()
        else:
            self.snake.pop()
        return True

    def step(self, key):
        if key == curses.KEY_UP and self.direction != (1, 0):
            self.direction = (-1, 0)
        elif key == curses.KEY_DOWN and self.direction != (-1, 0):
            self.direction = (1, 0)
        elif key == curses.KEY_LEFT and self.direction != (0, 1):
            self.direction = (0, -1)
        elif key == curses.KEY_RIGHT and self.direction != (0, -1):
            self.direction = (0, 1)
        return self._move_snake()

    def run(self):
        self.screen.nodelay(True)
        key = curses.KEY_RIGHT
        while key != KEY_ESC:
            self._render()
            next_key = self.screen.getch()
            if next_key != -1:
                key = next_key
            if not self.step(key):
                break
            curses.napms(100)
        self.screen.nodelay(False)
        self.screen.addstr(self.height // 2, self.width // 2 - 5, 'Game Over')
        self.screen.addstr(self.height // 2 + 1, self.width // 2 - 6, f'Final Score: {self.score}')
        self.screen.refresh()
        self.screen.getch()

def main(screen):
    curses.curs_set(0)
    game = SnakeGame(screen)
    game.run()

if __name__ == '__main__':
    curses.wrapper(main)
