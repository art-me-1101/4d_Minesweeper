import pygame
from random import shuffle


class Cell:
    def __init__(self, x, y, z, w):
        self.is_bomb = False
        self.show = False
        self.num = 0
        self.flag = False
        self.pos = x, y, z, w


class Minesweeper:
    def __init__(self, x, y, z, w, left=10, top=10, cell_size=50):
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.width = (x + 1) * self.cell_size * w - cell_size
        self.height = (y + 1) * self.cell_size * z - cell_size
        self.board = [[[[Cell(d, c, b, a) for d in range(x)] for c in range(y)] for b in range(z)] for a in range(w)]

    def rennder(self, screen):
        left, top = self.left, self.top
        for i in range(self.x):
            for j in range(self.y):
                for w in range(self.z):
                    for q in range(self.w):
                        if self.board[q][w][j][i].flag:
                            font = pygame.font.Font(None, 15)
                            text = font.render('Bomb', True, pygame.Color('red'))
                            text_x = left + (self.x + 1) * self.cell_size * w + self.cell_size * i + \
                                     self.cell_size // 2 - text.get_width() // 2
                            text_y = top + (self.y + 1) * self.cell_size * q + self.cell_size * j + \
                                     self.cell_size // 2 - text.get_height() // 2
                            screen.blit(text, (text_x, text_y))
                        elif self.board[q][w][j][i].show:
                            if not self.board[q][w][j][i].is_bomb:
                                font = pygame.font.Font(None, 30)
                                text = font.render(str(self.board[q][w][j][i].num), True, pygame.Color('#b2b5aa'))
                                text_x = left + (self.x + 1) * self.cell_size * w + self.cell_size * i + \
                                         self.cell_size // 2 - text.get_width() // 2
                                text_y = top + (self.y + 1) * self.cell_size * q + self.cell_size * j + \
                                         self.cell_size // 2 - text.get_height() // 2
                                screen.blit(text, (text_x, text_y))
                            else:
                                pygame.draw.rect(screen,
                                                 pygame.Color('red'),
                                                 (left + (self.x + 1) * self.cell_size * w + self.cell_size * i,
                                                  top + (self.y + 1) * self.cell_size * q + self.cell_size * j,
                                                  self.cell_size, self.cell_size))
                        pygame.draw.rect(screen,
                                         pygame.Color('white'),
                                         (left + (self.x + 1) * self.cell_size * w + self.cell_size * i,
                                          top + (self.y + 1) * self.cell_size * q + self.cell_size * j,
                                          self.cell_size, self.cell_size),
                                         width=1)

    def get_cell(self, mouse_pos):
        w = (mouse_pos[0] - self.left) // (self.cell_size * (self.x + 1))
        z = (mouse_pos[1] - self.top) // (self.cell_size * (self.y + 1))
        x = (mouse_pos[0] - self.left) % (self.cell_size * (self.x + 1)) // self.cell_size
        y = (mouse_pos[1] - self.top) % (self.cell_size * (self.y + 1)) // self.cell_size
        if 0 <= x < self.x and 0 <= y < self.y and 0 <= z < self.z and 0 <= w < self.w:
            return x, y, w, z
        return None

    def render_cur(self, pos):
        left, top = self.left, self.top
        pos = self.get_cell(pos)
        if pos is not None:
            x, y, w, z = pos
            for i in range(-1, 2):
                for j in range(-1, 2):
                    for e in range(-1, 2):
                        for q in range(-1, 2):
                            if 0 <= x + i < self.x and 0 <= y + j < self.y and 0 <= z + q < self.z and (
                                    0 <= w + e < self.w):
                                pygame.draw.rect(screen,
                                                 pygame.Color('#47ffff'),
                                                 (left + (self.x + 1) * self.cell_size * (w + e) + self.cell_size * (
                                                         x + i),
                                                  (top + (self.y + 1) * self.cell_size * (z + q) + self.cell_size * (
                                                          y + j)),
                                                  self.cell_size, self.cell_size))

    def game_over(self):
        ...

    def on_click(self, cell):
        if cell is not None:
            que = [self.board[cell[3]][cell[2]][cell[1]][cell[0]]]
            while que:
                cur_cell = que.pop()
                if not cur_cell.show:
                    cur_cell.show = True
                if cur_cell.is_bomb:
                    self.game_over()
                elif cur_cell.num == 0:
                    x, y, z, w = cur_cell.pos
                    for i in range(-1, 2):
                        for j in range(-1, 2):
                            for e in range(-1, 2):
                                for q in range(-1, 2):
                                    if abs(i) + abs(j) + abs(e) + abs(q) != 0 and 0 <= x + i < self.x \
                                            and 0 <= y + j < self.y and 0 <= z + e < self.z and \
                                            0 <= w + q < self.w:
                                        if not self.board[w + q][z + e][y + j][x + i].flag and not \
                                                self.board[w + q][z + e][y + j][x + i].show:
                                            que.append(self.board[w + q][z + e][y + j][x + i])

    def get_click(self, mouse_pos, mode):
        cell = self.get_cell(mouse_pos)
        if mode == 1:
            self.on_click(cell)
        elif mode == 2:
            self.make_flag(cell)

    def make_flag(self, cell):
        self.board[cell[3]][cell[2]][cell[1]][cell[0]].flag = 1 - self.board[cell[3]][cell[2]][cell[1]][cell[0]].flag

    def make_bombs(self, count):
        self.board = [[[[Cell(d, c, b, a) for d in range(self.x)] for c in range(self.y)] for b in range(self.z)] for a
                      in range(self.w)]
        a = [i for i in range(self.x * self.y * self.z * self.w)]
        shuffle(a)
        for i in a[:count]:
            w = i // (self.x * self.y * self.z)
            z = (i % (self.x * self.y * self.z)) // (self.x * self.y)
            y = (i % (self.x * self.y * self.z)) % (self.x * self.y) // self.x
            x = (i % (self.x * self.y * self.z)) % (self.x * self.y) % self.x
            self.board[w][z][y][x].is_bomb = True
        for x in range(self.x):
            for y in range(self.y):
                for z in range(self.z):
                    for w in range(self.w):
                        if not self.board[w][z][y][x].is_bomb:
                            d = 0
                            for i in range(-1, 2):
                                for j in range(-1, 2):
                                    for e in range(-1, 2):
                                        for q in range(-1, 2):
                                            if abs(i) + abs(j) + abs(e) + abs(q) != 0 and 0 <= x + i < self.x \
                                                    and 0 <= y + j < self.y and 0 <= z + e < self.z and \
                                                    0 <= w + q < self.w:
                                                if self.board[w + q][z + e][y + j][x + i].is_bomb:
                                                    d += 1
                            self.board[w][z][y][x].num = d


x, y, z, w = 4, 4, 5, 5

if __name__ == '__main__':
    pygame.init()
    size = widgh, height = 1000, 1000
    board = Minesweeper(x, y, z, w, left=25, top=25, cell_size=40)
    board.make_bombs(10)
    screen = pygame.display.set_mode(size)
    running = True
    fps = 60
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos, 1)
                if event.button == 3:
                    board.get_click(event.pos, 2)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    board.top -= board.cell_size * 2
                if event.key == pygame.K_DOWN:
                    board.top += board.cell_size * 2
                if event.key == pygame.K_RIGHT:
                    board.left += board.cell_size * 2
                if event.key == pygame.K_LEFT:
                    board.left -= board.cell_size * 2
        pos = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))
        board.render_cur(pos)
        board.rennder(screen)
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
