def main_from_input(content: str):
    lines = [x.strip() for x in content.strip().split("\n")]

    n_output = 0
    for line in lines:
        output_value = deduce_output_value(line)
        n_output += output_value
    
    print(n_output)
    return n_output

def deduce_output_value(line: str) -> int:
    wire_possibilities_dict = {
        "a": ["a", "b", "c", "d", "e", "f", "g"], 
        "b": ["a", "b", "c", "d", "e", "f", "g"], 
        "c": ["a", "b", "c", "d", "e", "f", "g"], 
        "d": ["a", "b", "c", "d", "e", "f", "g"], 
        "e": ["a", "b", "c", "d", "e", "f", "g"], 
        "f": ["a", "b", "c", "d", "e", "f", "g"], 
        "g": ["a", "b", "c", "d", "e", "f", "g"]
    }

    digits = line.replace(" | ", " ").split()

    for digit in digits:
        if len(digit) == 2: # shows a 1 means cf or fc
            wire_possibilities_dict = map_to(digit, "cf", wire_possibilities_dict)
        if len(digit) == 3: # shows a 7
            wire_possibilities_dict = map_to(digit, "acf", wire_possibilities_dict)
        if len(digit) == 4: # shows a 4
            wire_possibilities_dict = map_to(digit, "bcdf", wire_possibilities_dict)
        if len(digit) == 7: # shows a 8
            wire_possibilities_dict = map_to(digit, "abcdefg", wire_possibilities_dict)
        if len(digit) == 6: # shows a 0, 6 or 9 means that the one missing must be d, c or e respectively
            chars_left = list("abcdefg")
            for char in digit:
                chars_left.remove(char)
            char_left = chars_left[0]
            if char_left in wire_possibilities_dict["a"]: wire_possibilities_dict["a"].remove(char_left)
            if char_left in wire_possibilities_dict["b"]: wire_possibilities_dict["b"].remove(char_left)
            if char_left in wire_possibilities_dict["f"]: wire_possibilities_dict["f"].remove(char_left)
            if char_left in wire_possibilities_dict["g"]: wire_possibilities_dict["g"].remove(char_left)
    
    wire_possibilities_dict = reduce(wire_possibilities_dict)

    map_back = {wire_possibilities_dict[key][0]: key for key in wire_possibilities_dict}

    output_values_strs = line.split(" | ")[1].strip().split()

    values = [map_chars_to_value(chars, map_back) for chars in output_values_strs]
    result = int("".join([str(x) for x in values]))
    return result

def map_to(digit_wires, possible_map_to_wires, wire_possibilities_dict):
    # digit_wires = ab then possible_map_to_wires = cf since it is a 1
    # Then we 
    # * remove ab as possibilities for every wire except c and f
    # * remove any other char than a and b from c and f

    for key in wire_possibilities_dict:
        if key not in possible_map_to_wires:
            for digit_wire in digit_wires:
                if digit_wire in wire_possibilities_dict[key]:
                    wire_possibilities_dict[key].remove(digit_wire)
    
    for key in wire_possibilities_dict:
        if key in possible_map_to_wires:
            for possible_key in wire_possibilities_dict:
                if possible_key not in digit_wires:
                    if possible_key in wire_possibilities_dict[key]:
                        wire_possibilities_dict[key].remove(possible_key)
    
    return wire_possibilities_dict

def reduce(wire_possibilities_dict):
    for _ in range(7):
        for key in wire_possibilities_dict:
            if len(wire_possibilities_dict[key]) == 1:
                char = wire_possibilities_dict[key][0]
                for key2 in wire_possibilities_dict:
                    if key2 != key and char in wire_possibilities_dict[key2]:
                        wire_possibilities_dict[key2].remove(char)
    return wire_possibilities_dict

def map_chars_to_value(chars, map_back):
    mapped_chars = [map_back[char] for char in chars]

    mapped_chars_sorted_str = "".join(sorted(mapped_chars))

    if mapped_chars_sorted_str == "abcefg": return 0
    elif mapped_chars_sorted_str == "cf": return 1
    elif mapped_chars_sorted_str == "acdeg": return 2
    elif mapped_chars_sorted_str == "acdfg": return 3
    elif mapped_chars_sorted_str == "bcdf": return 4
    elif mapped_chars_sorted_str == "abdfg": return 5
    elif mapped_chars_sorted_str == "abdefg": return 6
    elif mapped_chars_sorted_str == "acf": return 7
    elif mapped_chars_sorted_str == "abcdefg": return 8
    elif mapped_chars_sorted_str == "abcdfg": return 9
    else: raise Exception(f"This is not a valid number: {mapped_chars_sorted_str}")

def main():
    with open("08/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf
""") == 5353

assert main_from_input("""
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""") == 61229

if __name__ == "__main__":
    main()
