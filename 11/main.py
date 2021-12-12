import numpy as np

class EnergyMatrix:
    def __init__(self, energy_ints_matrix: list[list[int]]) -> None:
        self.energy_ints_matrix = energy_ints_matrix
        self.n_flashes = 0

    def step(self):
        for y in range(len(self.energy_ints_matrix)):
            for x in range(len(self.energy_ints_matrix[0])):
                self.energy_ints_matrix[y][x] += 1
        
        self.flash_matrix()

        self.set_flashed_to_0()
    
    def flash_matrix(self):
        cells_to_flash = []
        for y in range(len(self.energy_ints_matrix)):
            for x in range(len(self.energy_ints_matrix[0])):
                value = self.energy_ints_matrix[y][x]
                if value == 10:
                    cells_to_flash.append((x, y))
        
        for cell in cells_to_flash:
            xc, yc = cell
            self.flash_cell(xc, yc)
    
    def flash_cell(self, x, y):
        self.n_flashes += 1

        adjacent_cells = self.get_adjacent_cells(x, y)
        for cell in adjacent_cells:
            xc, yc = cell

            self.energy_ints_matrix[yc][xc] += 1
            if self.energy_ints_matrix[yc][xc] == 10:
                self.flash_cell(xc, yc)

    def get_adjacent_cells(self, x, y):
        delta_cells = np.array([
            np.array([-1, -1]),
            np.array([-1, 0]),
            np.array([-1, 1]),
            np.array([0, -1]),
            np.array([0, 1]),
            np.array([1, -1]),
            np.array([1, 0]),
            np.array([1, 1])
        ])

        cell = np.array([x, y])

        cells = delta_cells + cell

        adjacent_cells = [(xc, yc) for xc, yc in cells if 0 <= xc < len(self.energy_ints_matrix[0]) and 0 <= yc < len(self.energy_ints_matrix)]

        return adjacent_cells
    
    def set_flashed_to_0(self):
        for y in range(len(self.energy_ints_matrix)):
            for x in range(len(self.energy_ints_matrix[0])):
                value = self.energy_ints_matrix[y][x]
                if value >= 10:
                    self.energy_ints_matrix[y][x] = 0
    
    def have_all_just_flashed(self) -> bool:
        for y in range(len(self.energy_ints_matrix)):
            for x in range(len(self.energy_ints_matrix[0])):
                if self.energy_ints_matrix[y][x] != 0: return False
        return True

def main_from_input(content: str):
    lines = [x.strip() for x in content.strip().split("\n")]
    energy_ints_matrix = [[int(x) for x in line] for line in lines]

    energy_matrix = EnergyMatrix(energy_ints_matrix)

    step_i = 0
    while not energy_matrix.have_all_just_flashed():
        step_i += 1
        energy_matrix.step()
    
    print(step_i)
    return step_i

def main():
    with open("11/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
""") == 195

if __name__ == "__main__":
    main()
