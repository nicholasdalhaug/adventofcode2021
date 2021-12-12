def main_from_input(content: str):
    lines = [x.strip() for x in content.strip().split("\n")]
    height_map = [[int(x) for x in line.strip()] for line in lines]
    
    low_point_heights = calc_low_point_heights(height_map)
    risk_levels = [x + 1 for x in low_point_heights]

    sum_risk = sum(risk_levels)
    print(sum_risk)
    return sum_risk

def calc_low_point_heights(height_map: list[list[int]]) -> list[int]:
    low_point_heights = []
    for y in range(len(height_map)):
        for x in range(len(height_map[0])):
            adjacent_values = get_adjacent_values(height_map, x, y)
            value = height_map[y][x]
            is_smaller = calc_is_smaller(value, adjacent_values)
            if is_smaller: low_point_heights.append(value)
    return low_point_heights

def get_adjacent_values(height_map, x, y):
    adjacent_values = []
    if x > 0: adjacent_values.append(height_map[y][x-1])
    if y > 0: adjacent_values.append(height_map[y-1][x])
    if x < len(height_map[0])-1: adjacent_values.append(height_map[y][x+1])
    if y < len(height_map)-1: adjacent_values.append(height_map[y+1][x])
    return adjacent_values

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
""") == 15

if __name__ == "__main__":
    main()
