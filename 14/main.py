from collections import defaultdict

def main_from_input(content: str):
    polymer_template, pair_insertions_str = content.strip().split("\n\n")
    
    pair_insertions_dict = {}
    for pair_insertion_str in pair_insertions_str.strip().split("\n"):
        pair, insertion = pair_insertion_str.strip().split(" -> ")
        pair_insertions_dict[pair] = insertion

    pairs = defaultdict(lambda: 0)
    for p_i in range(len(polymer_template)-1):
        pair = polymer_template[p_i:p_i+2]
        pairs[pair] += 1

    for i in range(40):
        print(i)
        pairs = insertion_step(pairs, pair_insertions_dict)
    
    last = polymer_template[-1]
    score = most_common_minus_least_common(pairs, last)
    print(score)
    return score

def insertion_step(pairs, pair_insertions_dict):
    new_pairs = defaultdict(lambda: 0)

    for pair in pairs:
        n_times = pairs[pair]

        insertion = pair_insertions_dict[pair]

        pair_1 = pair[0] + insertion
        pair_2 = insertion + pair[1]

        new_pairs[pair_1] += n_times
        new_pairs[pair_2] += n_times

    return new_pairs

def most_common_minus_least_common(pairs, last):
    counts = defaultdict(lambda: 0)
    for pair in pairs:
        p = pair[0]
        counts[p] += pairs[pair]
    counts[last] += 1

    #counts = {p: polymer.count(p) for p in set(polymer)}
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
""") == 2188189693529

if __name__ == "__main__":
    main()
