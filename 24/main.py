import itertools
from functools import cache

def create_program_functions(program_instructions: str):
    program_parts = ["inp" + p for p in program_instructions.strip().split("inp")[1:]]
    program_functions = [create_function(program_part) for program_part in program_parts]
    return program_functions

def run_program_with_functions(program_functions, input_digits: list[int]):
    state = (0, 0, 0, 0)

    assert len(input_digits) == len(program_functions)

    for i in range(len(input_digits)):
        input_digit = input_digits[i]
        program_function = program_functions[i]

        state = program_function(state, input_digit)
    return state

def create_function(program_instructions_with_start_inp: str):
    @cache
    def f(state: tuple[int], value: int):
        new_state = run_program(program_instructions_with_start_inp, [value], state)
        return new_state
    return f

def run_program(program_instructions: str, input_digits: list[int], old_state: tuple[int]):
    state = old_state
    next_input_digit_index = 0

    instruction_lines_list = [line.strip() for line in program_instructions.strip().split("\n")]
    for instruction_line in instruction_lines_list:
        instruction, *rest = instruction_line.split(" ")
        if instruction == "inp":
            state = inp(state, rest[0], input_digits[next_input_digit_index])
            next_input_digit_index += 1
        else:
            state = do_instruction(state, instruction_line)
    return state

def inp(state, local_variable_name: str, input_digit: int):
    if local_variable_name == "w": return (input_digit, state[1], state[2], state[3])
    elif local_variable_name == "x": return (state[0], input_digit, state[2], state[3])
    elif local_variable_name == "y": return (state[0], state[1], input_digit, state[3])
    elif local_variable_name == "z": return (state[0], state[1], state[2], input_digit)

def do_instruction(state, instruction_line: str):
    instruction, local_variable_name, variable_or_value = instruction_line.split(" ")

    if instruction == "add":
        return add(state, local_variable_name, variable_or_value)
    elif instruction == "mul":
        return mul(state, local_variable_name, variable_or_value)
    elif instruction == "div":
        return div(state, local_variable_name, variable_or_value)
    elif instruction == "mod":
        return mod(state, local_variable_name, variable_or_value)
    elif instruction == "eql":
        return eql(state, local_variable_name, variable_or_value)
    else:
        raise Exception(f"No such instruction {instruction}")

def add(state: tuple[int], local_variable_name: str, variable_or_value: str):
    value = get_value_from_variable_or_value(state, variable_or_value)

    if local_variable_name == "w": return (state[0] + value, state[1], state[2], state[3])
    elif local_variable_name == "x": return (state[0], state[1] + value, state[2], state[3])
    elif local_variable_name == "y": return (state[0], state[1], state[2] + value, state[3])
    elif local_variable_name == "z": return (state[0], state[1], state[2], state[3] + value)

def get_value_from_variable_or_value(state: tuple[int], variable_or_value: str):
    value = None
    if variable_or_value == "w": value = state[0]
    elif variable_or_value == "x": value = state[1]
    elif variable_or_value == "y": value = state[2]
    elif variable_or_value == "z": value = state[3]
    else: value = int(variable_or_value)
    return value

def mul(state: tuple[int], local_variable_name: str, variable_or_value: str):
    value = get_value_from_variable_or_value(state, variable_or_value)

    if local_variable_name == "w": return (state[0] * value, state[1], state[2], state[3])
    elif local_variable_name == "x": return (state[0], state[1] * value, state[2], state[3])
    elif local_variable_name == "y": return (state[0], state[1], state[2] * value, state[3])
    elif local_variable_name == "z": return (state[0], state[1], state[2], state[3] * value)

def div(state: tuple[int], local_variable_name: str, variable_or_value: str):
    value = get_value_from_variable_or_value(state, variable_or_value)

    if local_variable_name == "w": return (int(state[0] / value), state[1], state[2], state[3])
    elif local_variable_name == "x": return (state[0], int(state[1] / value), state[2], state[3])
    elif local_variable_name == "y": return (state[0], state[1], int(state[2] / value), state[3])
    elif local_variable_name == "z": return (state[0], state[1], state[2], int(state[3] / value))

def mod(state: tuple[int], local_variable_name: str, variable_or_value: str):
    value = get_value_from_variable_or_value(state, variable_or_value)

    if local_variable_name == "w": return (state[0] % value, state[1], state[2], state[3])
    elif local_variable_name == "x": return (state[0], state[1] % value, state[2], state[3])
    elif local_variable_name == "y": return (state[0], state[1], state[2] % value, state[3])
    elif local_variable_name == "z": return (state[0], state[1], state[2], state[3] % value)

def eql(state: tuple[int], local_variable_name: str, variable_or_value: str):
    value = get_value_from_variable_or_value(state, variable_or_value)

    if local_variable_name == "w": return (int(state[0] == value), state[1], state[2], state[3])
    elif local_variable_name == "x": return (state[0], int(state[1] == value), state[2], state[3])
    elif local_variable_name == "y": return (state[0], state[1], int(state[2] == value), state[3])
    elif local_variable_name == "z": return (state[0], state[1], state[2], int(state[3] == value))

def reduce_instruction_line(state: list[str], instruction_line: str):
    instruction, variable_name, variable_or_value = instruction_line.split(" ")
    variable_index = index_from_variable_name(variable_name)
    value = get_value_from_variable_or_value_str(state, variable_or_value)

    new_state = list(state)
    if instruction == "add":
        if value == "0":
            new_state[variable_index] = f"{state[variable_index]}"
        elif state[variable_index] == "0":
            new_state[variable_index] = f"{value}"
        else:
            new_state[variable_index] = f"{state[variable_index]} + {value}"
    elif instruction == "mul":
        if value == "0" or state[variable_index] == "0":
            new_state[variable_index] = f"0"
        elif value == "1":
            new_state[variable_index] = f"{state[variable_index]}"
        else:
            new_state[variable_index] = f"({state[variable_index]}) * ({value})"
    elif instruction == "div":
            new_state[variable_index] = f"int({state[variable_index]} / {value})"
    elif instruction == "mod":
        if value == "1":
            new_state[variable_index] = f"{state[variable_index]}"
        else:
            new_state[variable_index] = f"({state[variable_index]}) % {value}"
    elif instruction == "eql":
        if variable_name == variable_or_value or state[variable_index] == variable_or_value:
            new_state[variable_index] = f"1"
        else:
            new_state[variable_index] = f"int(({state[variable_index]}) == ({value}))"
    else:
        raise Exception(f"No such instruction {instruction}")
    
    for i in range(len(state)):
        sub_state = state[i]
        if len(sub_state) < 20:
            try:
                result = eval(sub_state)
                state[i] = str(result)
            except Exception as e:
                pass
    
    return tuple(new_state)


def get_value_from_variable_or_value_str(state: list[str], variable_or_value: str):
    value = None
    if variable_or_value == "w": value = state[0]
    elif variable_or_value == "x": value = state[1]
    elif variable_or_value == "y": value = state[2]
    elif variable_or_value == "z": value = state[3]
    else: value = variable_or_value
    return value       


def index_from_variable_name(variable_name: str):
    if variable_name == "w": return 0
    elif variable_name == "x": return 1
    elif variable_name == "y": return 2
    elif variable_name == "z": return 3

def reduce_sub_program(start_state, sub_program_lines):
    end_state = list(start_state)

    for line in sub_program_lines:
        end_state = reduce_instruction_line(end_state, line)

    return tuple(end_state)

def main_from_input(content: str):
    program_instructions = content.strip()

    # possible_end_states = []
    # sub_programs_wo_inp = program_instructions.split("inp")[1:]
    # for i in range(len(sub_programs_wo_inp)):
    #     sub_program_wo_inp = sub_programs_wo_inp[i].strip()
    #     sub_program_lines = sub_program_wo_inp.split("\n")[1:]
    #     start_state = (f"i{i:02}", f"s{i:02}_x", f"s{i:02}_y", f"s{i:02}_z")
    #     end_state = reduce_sub_program(start_state, sub_program_lines)
    #     possible_end_states.append(end_state)

    # reduced_instructions = reduce_instructions(program_instructions)
    # input_names = [f"input_{n:02}" for n in range(14)]
    # names_included = list(filter(lambda name: name in reduced_instructions[3], input_names))

    cs = [14, 15, 13, -10, 14, -3, -14, 12, 14, 12, -6, -6, -2, -9]

    #(int(s00_z / 1)) * ((25) * (int((int(((s00_z) % 26 + 14) == (i00))) == (0))) + 1) + (i00 + 8) * (int((int(((s00_z) % 26 + 14) == (i00))) == (0)))
    #(int(s01_z / 1)) * ((25) * (int((int(((s01_z) % 26 + 15) == (i01))) == (0))) + 1) + (i01 + 11) * (int((int(((s01_z) % 26 + 15) == (i01))) == (0)))
    #(int(s02_z / 1)) * ((25) * (int((int(((s02_z) % 26 + 13) == (i02))) == (0))) + 1) + (i02 + 2) * (int((int(((s02_z) % 26 + 13) == (i02))) == (0)))
    #(int(s03_z / 26)) * ((25) * (int((int(((s03_z) % 26 + -10) == (i03))) == (0))) + 1) + (i03 + 11) * (int((int(((s03_z) % 26 + -10) == (i03))) == (0)))
    #(int(s04_z / 1)) * ((25) * (int((int(((s04_z) % 26 + 14) == (i04))) == (0))) + 1) + (i04 + 1) * (int((int(((s04_z) % 26 + 14) == (i04))) == (0)))
    #(int(s05_z / 26)) * ((25) * (int((int(((s05_z) % 26 + -3) == (i05))) == (0))) + 1) + (i05 + 5) * (int((int(((s05_z) % 26 + -3) == (i05))) == (0)))
    #(int(s06_z / 26)) * ((25) * (int((int(((s06_z) % 26 + -14) == (i06))) == (0))) + 1) + (i06 + 10) * (int((int(((s06_z) % 26 + -14) == (i06))) == (0)))
    #(int(s07_z / 1)) * ((25) * (int((int(((s07_z) % 26 + 12) == (i07))) == (0))) + 1) + (i07 + 6) * (int((int(((s07_z) % 26 + 12) == (i07))) == (0)))
    #(int(s08_z / 1)) * ((25) * (int((int(((s08_z) % 26 + 14) == (i08))) == (0))) + 1) + (i08 + 1) * (int((int(((s08_z) % 26 + 14) == (i08))) == (0)))
    #(int(s09_z / 1)) * ((25) * (int((int(((s09_z) % 26 + 12) == (i09))) == (0))) + 1) + (i09 + 11) * (int((int(((s09_z) % 26 + 12) == (i09))) == (0)))
    #(int(s10_z / 26)) * ((25) * (int((int(((s10_z) % 26 + -6) == (i10))) == (0))) + 1) + (i10 + 9) * (int((int(((s10_z) % 26 + -6) == (i10))) == (0)))
    #(int(s11_z / 26)) * ((25) * (int((int(((s11_z) % 26 + -6) == (i11))) == (0))) + 1) + (i11 + 14) * (int((int(((s11_z) % 26 + -6) == (i11))) == (0)))
    #(int(s12_z / 26)) * ((25) * (int((int(((s12_z) % 26 + -2) == (i12))) == (0))) + 1) + (i12 + 11) * (int((int(((s12_z) % 26 + -2) == (i12))) == (0)))
    #(int(s13_z / 26)) * ((25) * (int((int(((s13_z) % 26 + -9) == (i13))) == (0))) + 1) + (i13 + 2) * (int((int(((s13_z) % 26 + -9) == (i13))) == (0)))

    
    program_functions = create_program_functions(program_instructions)

    assert len(program_functions) == 14

    # w is always used as input and never has to be a part of the state
    possible_last_function_states = {0: ()}
    possible_next_function_states = {}

    for program_i in range(len(program_functions)):
        program_function = program_functions[program_i]
        if cs[program_i] > 0:
            for possible_last_function_state in possible_last_function_states:
                digits_used_so_far = possible_last_function_states[possible_last_function_state]
                for input_digit in range(1,10):
                    next_state = program_function((input_digit, 0, 0, possible_last_function_state), input_digit)
                    next_z_state = next_state[3]
                    next_digits_used = (*digits_used_so_far, input_digit)
                    if next_z_state in possible_next_function_states:
                        possible_next_function_states[next_z_state] = list(max(int(str(possible_next_function_states[next_z_state])), int(str(next_digits_used))))
                    else:
                        possible_next_function_states[next_z_state] = next_digits_used
        else:
            c = cs[program_i]
            valid_ss = list(filter(lambda s: 1-c <= s%26 <= 9-c, possible_last_function_states))
            invalid_ss = list(filter(lambda s: s not in valid_ss, possible_last_function_states))
            for state in invalid_ss:
                possible_last_function_states.pop(state)
            
            for possible_last_function_state in possible_last_function_states:
                digits_used_so_far = possible_last_function_states[possible_last_function_state]

                input_digit = possible_last_function_state % 26 + c

                next_state = program_function((input_digit, 0, 0, possible_last_function_state), input_digit)
                next_z_state = next_state[3]

                assert next_z_state == possible_last_function_state // 26

                next_digits_used = (*digits_used_so_far, input_digit)
                if next_z_state in possible_next_function_states:
                    earlier_path = possible_next_function_states[next_z_state]
                    new_possible_path = next_digits_used
                    # Smallest found when reversing this
                    possible_next_function_states[next_z_state] = [int(x) for x in str(max(int("".join([str(x) for x in earlier_path])), int("".join([str(x) for x in new_possible_path]))))]
                else:
                    possible_next_function_states[next_z_state] = next_digits_used

        possible_last_function_states = possible_next_function_states
        possible_next_function_states = {}



    all_model_numbers_lists = itertools.product([9,8,7,6,5,4,3,2,1], repeat=14)
    for model_number_list in all_model_numbers_lists:
        result_state = run_program_with_functions(program_functions, model_number_list)
        #print(model_number_list)
        if result_state[3] == 0:
            break
    
    print(model_number_list)

def main():
    with open("24/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

program_functions = create_program_functions("""
    inp w
    add z w
    mod z 2
    div w 2
    add y w
    mod y 2
    div w 2
    add x w
    mod x 2
    div w 2
    mod w 2
""")
result_state = run_program_with_functions(program_functions, [6])
assert result_state == (0, 1, 1, 0)

if __name__ == "__main__":
    main()
