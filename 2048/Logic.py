import random


class Game2048:
    def __init__(self):
        self.board = [[0] * 4 for _ in range(4)]
        self.board = self.add_random_tile(self.board)

    @staticmethod
    def set_tile_with_number_two(numbers):
        if not Game2048.has_empty_tile(numbers):
            return None
        found = False
        while not found:
            r = random.randint(0, 3)
            c = random.randint(0, 3)
            if numbers[r][c] == 0:
                numbers[r][c] = 2
                found = True
        return numbers

    @staticmethod
    def has_empty_tile(numbers):
        for i in range(4):
            for j in range(4):
                if numbers[i][j] == 0:
                    return True
        return False

    @staticmethod
    def filter_zero(row):
        tiles = [x for x in row if x != 0]
        return tiles

    @staticmethod
    def slide(row):
        row = Game2048.filter_zero(row)
        for i in range(len(row) - 1):
            if row[i] == row[i + 1]:
                row[i] *= 2
                row[i + 1] = 0
        row = Game2048.filter_zero(row)
        while len(row) < 4:
            row.append(0)
        return row

    def move_tiles(self, numbers, direction):
        if direction == "left":
            return self.slide_left(numbers)
        elif direction == "right":
            return self.slide_right(numbers)
        elif direction == "up":
            return self.slide_up(numbers)
        elif direction == "down":
            return self.slide_down(numbers)
        else:
            return numbers

    def add_random_tile(self, numbers):
        numbers = self.set_tile_with_number_two(numbers)
        return numbers

    def slide_left(self, numbers):
        numbers2 = []
        for row in numbers:
            numbers2.append(self.slide(row))
        return numbers2

    def slide_right(self, numbers):
        numbers2 = []
        for row in numbers:
            row = row[::-1]
            row = self.slide(row)
            row = row[::-1]
            numbers2.append(row)
        return numbers2

    def slide_up(self, numbers):
        numbers2 = [[] for _ in range(4)]
        for i in range(4):
            row = [numbers[j][i] for j in range(4)]
            row = self.slide(row)
            for j in range(4):
                numbers2[j].append(row[j])
        return numbers2

    def slide_down(self, numbers):
        numbers2 = [[] for _ in range(4)]
        for i in range(4):
            row = [numbers[j][i] for j in range(3, -1, -1)]
            row = self.slide(row)
            row.reverse()
            for j in range(4):
                numbers2[j].append(row[j])
        return numbers2
