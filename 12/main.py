from collections import defaultdict

def main_from_input(content: str):
    lines = [x.strip() for x in content.strip().split("\n")]
    connections = [(line.split("-")[0], line.split("-")[1])  for line in lines]

    edges_dict = defaultdict(lambda: [])
    
    for connection in connections:
        from_node, to_node = connection
        if to_node not in edges_dict[from_node]:
            edges_dict[from_node].append(to_node)
        if from_node not in edges_dict[to_node]:
            edges_dict[to_node].append(from_node)

    paths_to_end = get_paths_to_end("start", edges_dict, ())

    n_paths = len(paths_to_end)
    print(n_paths)
    return n_paths

def get_paths_to_end(start_node: str, edges_dict: dict[str: list[str]], path_so_far: tuple[str]):
    path_so_far = path_so_far + (start_node, )

    can_go_to_nodes = edges_dict[start_node]

    paths = []
    for to_node in can_go_to_nodes:
        if to_node == "end":
            paths.append(path_so_far + ("end", ))
        elif to_node.isupper() or to_node not in path_so_far:
            new_paths = get_paths_to_end(to_node, edges_dict, path_so_far)
            paths.extend(new_paths)
    
    return paths

def main():
    with open("12/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
start-A
start-b
A-c
A-b
b-d
A-end
b-end
""") == 10

assert main_from_input("""
dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc
""") == 19

assert main_from_input("""
fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW
""") == 226

if __name__ == "__main__":
    main()
