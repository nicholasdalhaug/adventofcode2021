import numpy as np
import cv2

class Map:
    map_matrix: list[list[str]]

    def __init__(self, coords) -> None:
        self.map_matrix = [[]]

        for coord in coords:
            self.add(coord)

    def add(self, coord):
        self.ensure_enough_space(coord)
        x,y = coord
        self.map_matrix[y][x] = 1
    
    def ensure_enough_space(self, coord):
        x,y = coord

        if x > len(self.map_matrix[0]) - 1:
            self.add_cols(x - len(self.map_matrix[0]) + 1)
        if y > len(self.map_matrix) - 1:
            self.add_rows(y - len(self.map_matrix) + 1)

    def add_cols(self, n_cols):
        for _ in range(n_cols):
            for y in range(len(self.map_matrix)):
                self.map_matrix[y].append(0)

    def add_rows(self, n_rows):
        for _ in range(n_rows):
            self.map_matrix.append([0 for _ in range(len(self.map_matrix[0]))])
    
    def fold(self, axis: str, value: int):
        if axis == "y":
            self.fold_up(value)
        elif axis == "x":
            self.fold_left(value)
        else:
            raise Exception(f"No such axis {axis}")

    def fold_left(self, value: int):
        for x_delta in range(len(self.map_matrix[0]) - value - 1):
            x_left = value - 1 - x_delta
            x_right = value + 1 + x_delta
            for y in range(len(self.map_matrix)):
                if self.map_matrix[y][x_right] == 1:
                    self.map_matrix[y][x_left] = 1

        for y in range(len(self.map_matrix)):
            for _ in range(len(self.map_matrix[y]) - value):
                self.map_matrix[y].pop()

    def fold_up(self, value: int):
        for y_delta in range(len(self.map_matrix) - value - 1):
            y_upper = value - 1 - y_delta
            y_lower = value + 1 + y_delta
            for x in range(len(self.map_matrix[0])):
                if self.map_matrix[y_lower][x] == 1:
                    self.map_matrix[y_upper][x] = 1

        for _ in range(len(self.map_matrix) - value):
            self.map_matrix.pop()

    def count_dots(self) -> int:
        n_dots = 0
        for y in range(len(self.map_matrix)):
            for x in range(len(self.map_matrix[0])):
                if self.map_matrix[y][x] == 1: 
                    n_dots += 1
        return n_dots
    
    def print(self):
        np_arr = np.array(self.map_matrix, dtype=np.uint8)
        np_arr[np_arr == 1] = 255

        cv2.namedWindow("Paper folding", cv2.WINDOW_NORMAL)

        cv2.imshow("Paper folding", np_arr)
        cv2.waitKey(0)


def main_from_input(content: str):
    lines_str, folds_str = content.strip().split("\n\n")
    lines = [line.strip() for line in lines_str.strip().split("\n")]
    folds_lines = [line.strip() for line in folds_str.strip().split("\n")]

    coords = []
    for line in lines:
        x_str, y_str = line.strip().split(",")
        coords.append((int(x_str), int(y_str)))

    map = Map(coords)
    map.print()

    for fold_inst in folds_lines:
        axis, value_str = fold_inst.lstrip("fold along ").strip().split("=")
        value = int(value_str)
        map.fold(axis, value)

        
        map.print()
        break
    
    score = map.count_dots()
    print(score)
    return score

def main():
    with open("13/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
""") == 17

if __name__ == "__main__":
    main()
