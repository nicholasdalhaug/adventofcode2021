from dataclasses import dataclass

@dataclass
class Position:
    depth: int = 0
    horizontal: int = 0

def main():
    with open("02/input.txt") as file:
        submarine_instructions = [x.strip() for x in file.readlines()]
    
    end_position = traverse_path(submarine_instructions)
    print(end_position)
    print(end_position.depth * end_position.horizontal)

def traverse_path(submarine_instructions):
    position = Position()
    for instruction_with_value in submarine_instructions:
        instruction, value_str = instruction_with_value.split()
        value = int(value_str)

        if instruction == "forward":
            position.horizontal += value
        elif instruction == "up": 
            position.depth -= value
        elif instruction == "down":
            position.depth += value
        else:
            raise Exception("Not valid instruction: {instruction}")
    return position

if __name__ == "__main__":
    main()