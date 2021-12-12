def main_from_input(content: str):
    lines = [x.strip() for x in content.strip().split("\n")]
    height_map = [[int(x) for x in line.strip()] for line in lines]
    
    low_points = calc_low_points(height_map)
    basin_sizes = get_basin_sizes(height_map, low_points)

    sorted_basin_sizes = sorted(basin_sizes)

    score = sorted_basin_sizes[-1] * sorted_basin_sizes[-2] * sorted_basin_sizes[-3]
    print(score)
    return score

def calc_low_points(height_map: list[list[int]]):
    low_points = []
    for y in range(len(height_map)):
        for x in range(len(height_map[0])):
            adjacent_values = get_adjacent_values(height_map, x, y)
            value = height_map[y][x]
            is_smaller = calc_is_smaller(value, adjacent_values)
            if is_smaller: low_points.append((x, y))
    return low_points

def get_basin_sizes(height_map, low_points):
    basin_sizes = [get_basin_size(height_map, low_point) for low_point in low_points]
    return basin_sizes

def get_basin_size(height_map, low_point):
    visited_cells = []
    cells_to_visit = [low_point]

    while len(cells_to_visit) != 0:
        cell = cells_to_visit.pop()
        visited_cells.append(cell)

        x, y = cell

        for adjacent_cell in get_adjacent_cells(height_map, x, y):
            adjacent_cell_value = height_map[adjacent_cell[1]][adjacent_cell[0]]
            if adjacent_cell_value != 9 and adjacent_cell not in visited_cells and adjacent_cell not in cells_to_visit: 
                cells_to_visit.append(adjacent_cell)
    
    basin_size = len(visited_cells)
    return basin_size
    


def get_adjacent_values(height_map, x, y):
    adjacent_cells = get_adjacent_cells(height_map, x, y)
    adjacent_values = [height_map[p[1]][p[0]] for p in adjacent_cells]
    return adjacent_values

def get_adjacent_cells(height_map, x, y):
    adjacent_cells = []
    if x > 0: adjacent_cells.append((x-1, y))
    if y > 0: adjacent_cells.append((x, y-1))
    if x < len(height_map[0])-1: adjacent_cells.append((x+1, y))
    if y < len(height_map)-1: adjacent_cells.append((x, y+1))
    return adjacent_cells

def calc_is_smaller(value, adjacent_values):
    for adjacent_value in adjacent_values:
        if adjacent_value <= value: return False
    return True
    

def main():
    with open("09/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
2199943210
3987894921
9856789892
8767896789
9899965678
""") == 1134

if __name__ == "__main__":
    main()
