from dataclasses import dataclass
import numpy as np

@dataclass
class Point:
    x: int
    y: int

@dataclass
class Line:
    p1: Point
    p2: Point

    def min_p(self):
        return Point(min(self.p1.x, self.p2.x), min(self.p1.y, self.p2.y))
    
    def max_p(self):
        return Point(max(self.p1.x, self.p2.x), max(self.p1.y, self.p2.y))

@dataclass
class Space:
    value: int = 0

class Map:
    map_matrix: list[list[Space]]

    def __init__(self) -> None:
        self.map_matrix = [[]]

    def add(self, line: Line):
        self.ensure_enough_space(line)

        p1 = np.array([line.p1.x, line.p1.y])
        p2 = np.array([line.p2.x, line.p2.y])

        delta = p2 - p1

        length = max(abs(delta[0]), abs(delta[1]))
        delta_unit = delta / length

        for i in range(length+1):
            p_to_increase = p1 + delta_unit * i
            self.increase(int(p_to_increase[0]), int(p_to_increase[1]))
    
    def ensure_enough_space(self, line: Line):
        max_x = line.max_p().x
        max_y = line.max_p().y

        if max_x > len(self.map_matrix[0]) - 1:
            self.add_cols(max_x - len(self.map_matrix[0]) + 1)
        if max_y > len(self.map_matrix) - 1:
            self.add_rows(max_y - len(self.map_matrix) + 1)

    def add_cols(self, n_cols):
        for _ in range(n_cols):
            for y in range(len(self.map_matrix)):
                self.map_matrix[y].append(Space())

    def add_rows(self, n_rows):
        for _ in range(n_rows):
            self.map_matrix.append([Space() for _ in range(len(self.map_matrix[0]))])
    
    def increase(self, x, y):
        current_space = self.map_matrix[y][x]
        current_space.value = current_space.value + 1

def main_from_input(content: str):
    lines = []
    for line_str in content.strip().split("\n"):
        p1_str, p2_str = line_str.strip().split(" -> ")
        x1, y1 = [int(c) for c in p1_str.split(",")]
        x2, y2 = [int(c) for c in p2_str.split(",")]
        lines.append(Line(Point(x1, y1), Point(x2, y2)))
    
    map = Map()

    for line in lines:
        map.add(line)
    
    n_points = count_points_where_at_least_2_lines(map)
    print(n_points)
    return n_points

def count_points_where_at_least_2_lines(map: Map):
    n_points = 0
    for y in range(len(map.map_matrix)):
        for x in range(len(map.map_matrix[0])):
            if map.map_matrix[y][x].value >= 2:
                n_points += 1
    return n_points

def main():
    with open("05/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
""") == 12

if __name__ == "__main__":
    main()
