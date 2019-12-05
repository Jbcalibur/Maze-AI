from random import choice, random, randrange
from time import sleep
from os import system
from sys import stderr
from threading import Thread
from collections import deque
from util import Cell, Direction


class Maze:
    def __init__(self, height, width=None, path_to_build=None):
        self.height = (height if height > 0 else 1)

        if width is None:
            self.width = height
        else:
            self.width = (width if width > 0 else 1)

        if path_to_build is None:
            self.__path_to_build = (self.height if self.height > self.width else self.width)
        else:
            self.__path_to_build = (path_to_build if path_to_build > 0 else 1)

        self.__build()

    def __str__(self):
        sret = ""
        for line in self.map:
            for case in line:
                sret += case.value
            sret += '\n'
        return sret[:-1]

    def __build(self):
        self.map = []
        self.__max_cell = self.width * self.height
        self.__building_flag = True

        for _ in range(self.height):
            line = []
            for _ in range(self.width):
                line.append(Cell.WALL)
            self.map.append(line)

        self.__make_path(0, 0)
        self.__make_path(self.height-1, self.width-1)
        self.__make_path(*self.__get_path_start(), self.__path_to_build)

        self.map[0][0] = Cell.START
        self.map[self.height-1][self.width-1] = Cell.FINISH
        
        self.map.insert(0, [Cell.WALL]*self.width)
        for line in self.map:
            line.insert(0, Cell.WALL)
            line.append(Cell.WALL)
        self.map.append([Cell.WALL]*(self.width+2))

    def __make_path(self, line, column, iter=1):
        if iter > 0:
            ancestor = deque(2*[None], maxlen=2)
            for index in range(self.width):
                direction_list = list(Direction)
                if ancestor[0]:
                    direction_list.append(ancestor[0])

                    if ancestor[0] is Direction.LEFT:
                        direction_list.remove(Direction.RIGHT)
                    elif ancestor[0] is Direction.RIGHT:
                        direction_list.remove(Direction.LEFT)
                    elif ancestor[0] is Direction.UP:
                        direction_list.remove(Direction.DOWN)
                    elif ancestor[0] is Direction.DOWN:
                        direction_list.remove(Direction.UP)

                if ancestor[1]:
                    direction_list.append(ancestor[1])
                direction = choice(direction_list)
                loop_flag = True
                threshold = 5
                while loop_flag:
                    tmp_column = column
                    tmp_line = line

                    avoid_out_of_bound = [
                        direction is Direction.LEFT and column == 0,
                        direction is Direction.RIGHT and column == self.width-1,
                        direction is Direction.UP and line == 0,
                        direction is Direction.DOWN and line == self.height-1
                    ]

                    if direction is Direction.LEFT:
                        tmp_column -= 1
                    elif direction is Direction.RIGHT:
                        tmp_column += 1
                    elif direction is Direction.UP:
                        tmp_line -= 1
                    elif direction is Direction.DOWN:
                        tmp_line += 1

                    if any(avoid_out_of_bound) or self.map[tmp_line][tmp_column] == Cell.FLOOR:
                        direction = choice(direction_list)
                        threshold -= 1
                        if threshold < 0:
                            return self.__make_path(*self.__get_path_start(), iter-1)
                    else:
                        loop_flag = False
                        column = tmp_column
                        line = tmp_line
                        ancestor.appendleft(direction)

                self.map[line][column] = Cell.FLOOR
            return self.__make_path(*self.__get_path_start(), iter-1)

    def __get_path_start(self):
        threshold = 5
        while True:
            line = randrange(len(self.map))
            column = randrange(len(self.map[0]))
            if self.map[line][column] == Cell.FLOOR:
                threshold -= 1
                if threshold < 0:
                    return line, column
            else:
                return line, column


if __name__ == "__main__":
    maze = Maze(25, 50, 15)
    print(maze)
