def main_from_input(content: str):
    lines = [x.strip() for x in content.strip().split("\n")]

    valid_lines = []
    for line in lines:
        score = calc_syntax_score_for_line(line)
        if score == 0: valid_lines.append(line)
    
    autocomplete_scores = [calc_autocomplete_score_for_line(line) for line in valid_lines]

    sorted_autocomplete_scores = sorted(autocomplete_scores)

    score = sorted_autocomplete_scores[len(autocomplete_scores)//2]
    
    print(score)
    return score

open_chars = "([{<"
close_chars = ")]}>"

def get_corresponding_char(char):
    if char in open_chars: 
        i = open_chars.index(char)
        return close_chars[i]
    if char in close_chars: 
        i = close_chars.index(char)
        return open_chars[i]
    raise Exception(f"Invalid syntax char: {char}")


def calc_autocomplete_score_for_line(line: str) -> int:
    relevant_open_chars = [line[0]]
    for char in line[1:]:
        if char in open_chars: relevant_open_chars.append(char)
        elif char == get_corresponding_char(relevant_open_chars[-1]):
            relevant_open_chars.pop()
    
    chars_to_correct = [get_corresponding_char(char) for char in relevant_open_chars[::-1]]
    total_score = 0
    for char in chars_to_correct:
        total_score *= 5
        total_score += calc_autocomplete_score_for_char(char)
    
    return total_score
    
def calc_autocomplete_score_for_char(char: str) -> int:
    if char == ")": return 1
    if char == "]": return 2
    if char == "}": return 3
    if char == ">": return 4
    raise Exception(f"Invalid autocomplete char: {char}")

def calc_syntax_score_for_line(line: str) -> int:
    if line[0] not in open_chars: return calc_syntax_score_for_char(line[0])

    relevant_open_chars = [line[0]]
    for char in line[1:]:
        if char in open_chars: relevant_open_chars.append(char)
        elif char == get_corresponding_char(relevant_open_chars[-1]):
            relevant_open_chars.pop()
        else:
            return calc_syntax_score_for_char(char)
    
    return 0

def calc_syntax_score_for_char(char: str) -> int:
    if char == ")": return 3
    if char == "]": return 57
    if char == "}": return 1197
    if char == ">": return 25137
    raise Exception(f"Invalid syntax char: {char}")

def main():
    with open("10/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
""") == 288957

if __name__ == "__main__":
    main()
