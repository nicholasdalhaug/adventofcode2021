def main_from_input(content: str):
    fish_timers_num = [int(x) for x in content.strip().split(",")]

    fish_timers_dict = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0,
        6: 0,
        7: 0,
        8: 0
    }

    for fish_timer in fish_timers_num:
        fish_timers_dict[fish_timer] += 1

    for day in range(256):
        print(f"Day: {day}")
        fish_timers_dict = step_fish_timers(fish_timers_dict)
    
    score = fish_timers_dict[0] \
        + fish_timers_dict[1] \
        + fish_timers_dict[2] \
        + fish_timers_dict[3] \
        + fish_timers_dict[4]\
        + fish_timers_dict[5]\
        + fish_timers_dict[6]\
        + fish_timers_dict[7]\
        + fish_timers_dict[8]

    print(score)
    return score

def step_fish_timers(fish_timers: dict[int: int]) -> list[int]:
    new_fish_timers = {
        0: fish_timers[1], 
        1: fish_timers[2], 
        2: fish_timers[3], 
        3: fish_timers[4], 
        4: fish_timers[5], 
        5: fish_timers[6], 
        6: fish_timers[7] + fish_timers[0], 
        7: fish_timers[8], 
        8: fish_timers[0]
    }
    
    return new_fish_timers

def main():
    with open("06/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
3,4,3,1,2
""") == 26984457539

if __name__ == "__main__":
    main()
