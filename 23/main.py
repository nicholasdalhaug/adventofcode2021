from functools import cache

@cache
def get_lowest_map_path_with_cost(amphimap: str):
    if amphimap == WIN_MAP:
        map_path = [amphimap]
        return (map_path, 0)
    
    amphimap_list = amphimap.split("\n")
    
    possible_movers = get_possible_movers(amphimap_list)

    next_maps_and_costs_accumulated = []
    for mover in possible_movers:
        next_maps_and_costs = get_possible_moves_maps_and_costs(amphimap_list, mover)
        next_maps_and_costs_accumulated.extend(next_maps_and_costs)
    
    lowest_cost = float("inf")
    lowest_cost_map_path = []
    for next_map, move_cost in next_maps_and_costs_accumulated:
        map_path, cost_from_next_map = get_lowest_map_path_with_cost(next_map)
        cost = cost_from_next_map + move_cost
        if cost < lowest_cost:
            lowest_cost = cost
            lowest_cost_map_path = [amphimap, *map_path]
    return (lowest_cost_map_path, lowest_cost)

def get_possible_movers(amphimap_list):
    possible_movers = []
    for y in range(len(amphimap_list)):
        for x in range(len(amphimap_list[y])):
            if amphimap_list[y][x] in "ABCD":
                possible_movers.append((x, y))
    return possible_movers

def get_possible_moves_maps_and_costs(amphimap_list, mover_coord):
    x, y = mover_coord

    possible_moves_maps_and_costs = []
    if y == 2 or y == 3 or y == 4 or y == 5:
        maps_and_costs = get_maps_and_costs_hallway(amphimap_list, mover_coord)
        possible_moves_maps_and_costs.extend(maps_and_costs)
    else:
        assert y == 1
        maps_and_costs = get_maps_and_costs_home(amphimap_list, mover_coord)
        possible_moves_maps_and_costs.extend(maps_and_costs)
    return possible_moves_maps_and_costs

def get_maps_and_costs_home(map_list, from_coord):
    x, y = from_coord
    assert y == 1
    mover_name = map_list[y][x]
    home_x = get_home_x(mover_name)

    dir = -1 if home_x < x else 1

    possible_moves_maps_and_costs = []

    # Check right
    next_x = x + dir
    next_tile = map_list[1][next_x]
    while next_tile == ".":
        if next_x == home_x:
            tile_below = map_list[2][home_x]
            if tile_below == ".":
                tile_2_below = map_list[3][home_x]
                tile_3_below = map_list[4][home_x]
                tile_4_below = map_list[5][home_x]
                if tile_2_below == ".":
                    if tile_3_below == ".":
                        if tile_4_below == ".":
                            map_and_cost = get_map_and_cost_after_move(map_list, from_coord, (home_x, 5))
                            possible_moves_maps_and_costs.append(map_and_cost)
                        elif tile_4_below == mover_name:
                            map_and_cost = get_map_and_cost_after_move(map_list, from_coord, (home_x, 4))
                            possible_moves_maps_and_costs.append(map_and_cost)
                    elif tile_3_below == mover_name and tile_4_below == mover_name:
                        map_and_cost = get_map_and_cost_after_move(map_list, from_coord, (home_x, 3))
                        possible_moves_maps_and_costs.append(map_and_cost)
                elif tile_2_below == mover_name and tile_3_below == mover_name and tile_4_below == mover_name:
                    map_and_cost = get_map_and_cost_after_move(map_list, from_coord, (home_x, 2))
                    possible_moves_maps_and_costs.append(map_and_cost) 
            break

        next_x += dir
        next_tile = map_list[1][next_x]

    return possible_moves_maps_and_costs

def get_maps_and_costs_hallway(map_list, from_coord):
    x, y = from_coord
    assert y > 1

    mover_name = map_list[y][x]
    home_x = get_home_x(mover_name)

    if y == 5 and x == home_x:
        return []
    if y == 4 and x == home_x and map_list[5][home_x] == mover_name:
        return []
    if y == 3 and x == home_x  and map_list[4][home_x] == mover_name and map_list[5][home_x] == mover_name:
        return []
    if y == 2 and x == home_x and map_list[3][home_x] == mover_name and map_list[4][home_x] == mover_name and map_list[5][home_x] == mover_name:
        return []
    if y  == 5 and map_list[4][x] != ".":
        return []
    if y  == 4 and map_list[3][x] != ".":
        return []
    if y  == 3 and map_list[2][x] != ".":
        return []

    possible_moves_maps_and_costs = []
    if map_list[1][x-1] == ".":
        map_and_cost = get_map_and_cost_after_move(map_list, from_coord, (x-1, 1))
        possible_moves_maps_and_costs.append(map_and_cost)

        # Check left
        next_x = x-2
        next_tile = map_list[1][next_x]
        while next_tile == ".":
            tile_below = map_list[2][next_x]
            if tile_below == "#":
                map_and_cost = get_map_and_cost_after_move(map_list, from_coord, (next_x, 1))
                possible_moves_maps_and_costs.append(map_and_cost)

            next_x -= 1
            next_tile = map_list[1][next_x]
    if map_list[1][x+1] == ".":
        map_and_cost = get_map_and_cost_after_move(map_list, from_coord, (x+1, 1))
        possible_moves_maps_and_costs.append(map_and_cost)

        # Check right
        next_x = x+2
        next_tile = map_list[1][next_x]
        while next_tile == ".":
            tile_below = map_list[2][next_x]
            if tile_below == "#":
                map_and_cost = get_map_and_cost_after_move(map_list, from_coord, (next_x, 1))
                possible_moves_maps_and_costs.append(map_and_cost)

            next_x += 1
            next_tile = map_list[1][next_x]
    return possible_moves_maps_and_costs

def get_map_and_cost_after_move(map_list, from_coord, to_coord):
    x, y = from_coord
    x_to, y_to = to_coord
    mover_name = map_list[y][x]
    mover_cost = get_mover_cost(mover_name)

    next_map = get_map_after_move(map_list, from_coord, to_coord)

    n_steps = y - 1 + abs(x_to - x) + y_to - 1
    cost = n_steps * mover_cost
    
    return (next_map, cost)

def get_map_after_move(map_list, from_coord, to_coord):
    map_grid = [list(map_list[y]) for y in range(len(map_list))]

    mover_name = map_grid[from_coord[1]][from_coord[0]]
    
    map_grid[from_coord[1]][from_coord[0]] = "."
    map_grid[to_coord[1]][to_coord[0]] = mover_name

    next_map_str = ("".join(["".join(row) + "\n" for row in map_grid])).strip()
    return next_map_str

def get_home_x(mover_name: str):
    if mover_name == "A": return 3
    if mover_name == "B": return 5
    if mover_name == "C": return 7
    if mover_name == "D": return 9
    raise Exception(f"No such mover name {mover_name}")

def get_mover_cost(mover_name: str) -> int:
    if mover_name == "A": return 1
    if mover_name == "B": return 10
    if mover_name == "C": return 100
    if mover_name == "D": return 1000
    raise Exception(f"No such mover name {mover_name}")

def main_from_input(content: str):
    amphimap = content.strip()

    map_lines = amphimap.split("\n")
    map_lines.insert(3, "  #D#C#B#A#")
    map_lines.insert(4, "  #D#B#A#C#")

    amphimap = get_map_after_move(map_lines, (3,2), (3,2))

    map_path, score = get_lowest_map_path_with_cost(amphimap)

    print()
    for map_str in map_path:
        print(map_str)
        print()
    
    print(score)
    return score

def main():
    with open("23/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

WIN_MAP = """#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########"""

# assert main_from_input("""
# #############
# #.........A.#
# ###.#B#C#D###
#   #A#B#C#D#
#   #########
# """) == 8

# assert main_from_input("""
# #############
# #...........#
# ###A#B#C#D###
#   #A#B#C#D#
#   #########
# """) == 0

# # Useful
# assert main_from_input("""
# #############
# #.A.........#
# ###.#B#C#D###
#   #A#B#C#D#
#   #########
# """) == 2

assert main_from_input("""
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
""") == 44169

if __name__ == "__main__":
    main()
