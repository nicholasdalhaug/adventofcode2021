def main_from_input(content: str):
    lines = [x.strip() for x in content.strip().split("\n")]

    total_score = 0
    for line in lines:
        score = calc_syntax_score_for_line(line)
        total_score += score
    
    print(total_score)
    return total_score

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
""") == 26397

if __name__ == "__main__":
    main()
