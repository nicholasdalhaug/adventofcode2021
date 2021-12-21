import itertools
from functools import cache

def main_from_input(content: str):
    p1_str, p2_str = content.strip().split("\n")
    p1_start = int(p1_str.strip()[-1])
    p2_start = int(p2_str.strip()[-1])

    counts = count_wins(p1_start, p2_start, 0, 0, 1)
    
    score = max(counts)
    print(score)
    return score

@cache
def count_wins(p1_pos, p2_pos, p1_score, p2_score, whose_turn):
    if p1_score >= 21:
        return (1, 0)
    if p2_score >= 21:
        return (0, 1)
    
    dice_sum_values = [sum(d) for d in itertools.product([1, 2, 3], repeat=3)]
    if whose_turn == 1:
        p1_locs = [(p1_pos + d - 1) % 10 + 1 for d in dice_sum_values]
        p1_scores = [p1_score + p1_loc for p1_loc in p1_locs]
        cs = [count_wins(p1_locs[i], p2_pos, p1_scores[i], p2_score, 2) for i in range(len(dice_sum_values))]
    else:
        p2_locs = [(p2_pos + d - 1) % 10 + 1 for d in dice_sum_values]
        p2_scores = [p2_score + p2_loc for p2_loc in p2_locs]
        cs = [count_wins(p1_pos, p2_locs[i], p1_score, p2_scores[i], 1) for i in range(len(dice_sum_values))]

    c1 = sum([c[0] for c in cs])
    c2 = sum([c[1] for c in cs])
    count = (c1, c2)
    return count

def main():
    with open("21/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
Player 1 starting position: 4
Player 2 starting position: 8
""") == 444356092776315

if __name__ == "__main__":
    main()
