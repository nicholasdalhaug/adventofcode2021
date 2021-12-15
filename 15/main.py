def main_from_input(content: str):
    map_matrix = [[int(x) for x in line.strip()] for line in content.strip().split("\n")]
    x_len = len(map_matrix[0])
    y_len = len(map_matrix)
    increased_map = [[(map_matrix[y%y_len][x%x_len] + x // x_len + y // y_len - 1) % 9 + 1 for x in range(5*x_len)] for y in range(5*y_len)]

    path = get_shortest_path(increased_map, (0, 0))

    end = (len(increased_map[0])-1, len(increased_map)-1)
    risk = path[end][1]

    print(risk)
    return risk

def get_shortest_path(map_matrix, start_coord):
    visited_nodes = {start_coord: (None, 0)}
    start_neighbours = get_neighbours(start_coord, map_matrix)
    nodes_to_visit = {n: (start_coord, map_matrix[n[1]][n[0]]) for n in start_neighbours}

    while len(nodes_to_visit) != 0:
        lowest_cost_node = sorted(nodes_to_visit.items(), key= lambda n: n[1][1])[0][0]
        
        visited_from, cost = nodes_to_visit.pop(lowest_cost_node)

        visited_nodes[lowest_cost_node] = (visited_from, cost)

        neighbours = get_neighbours(lowest_cost_node, map_matrix)
        for n in neighbours:
            cost_to_n = cost + map_matrix[n[1]][n[0]]
            if n not in visited_nodes and (n not in nodes_to_visit or nodes_to_visit[n][1] > cost_to_n):
                nodes_to_visit[n] = (lowest_cost_node, cost_to_n)
                if n == (len(map_matrix[0])-1, len(map_matrix)-1):
                    visited_nodes[n] = (lowest_cost_node, cost_to_n)
                    return visited_nodes

    raise Exception("We never found the end")

def get_neighbours(coord, map_matrix):
    x, y = coord
    neighbours = []
    if x > 0: neighbours.append((x-1, y))
    if x < len(map_matrix[0])-1: neighbours.append((x+1, y))
    if y > 0: neighbours.append((x, y-1))
    if y < len(map_matrix)-1: neighbours.append((x, y+1))
    return neighbours

def main():
    with open("15/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
""") == 315

if __name__ == "__main__":
    main()
