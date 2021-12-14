def main_from_input(content: str):
    polymer_template, pair_insertions_str = content.strip().split("\n\n")
    
    pair_insertions_dict = {}
    for pair_insertion_str in pair_insertions_str.strip().split("\n"):
        pair, insertion = pair_insertion_str.strip().split(" -> ")
        pair_insertions_dict[pair] = insertion

    polymer = polymer_template
    for _ in range(10):
        polymer = insertion_step(polymer, pair_insertions_dict)
    
    score = most_common_minus_least_common(polymer)
    print(score)
    return score

def insertion_step(polymer, pair_insertions_dict):
    insertions = []

    for p_i in range(len(polymer)-1):
        pair = polymer[p_i:p_i+2]
        insertion = pair_insertions_dict[pair]
        insertions.append((insertion, p_i))
    
    new_polymer = polymer
    for insertion_tuple in insertions[::-1]:
        insertion, p_i = insertion_tuple
        new_polymer = new_polymer[:p_i+1] + insertion + new_polymer[p_i+1:]
    
    return new_polymer

def most_common_minus_least_common(polymer: str):
    counts = {p: polymer.count(p) for p in set(polymer)}
    max_value = max(counts.values())
    min_value = min(counts.values())
    value = max_value - min_value
    return value

def main():
    with open("14/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
""") == 1588

if __name__ == "__main__":
    main()
