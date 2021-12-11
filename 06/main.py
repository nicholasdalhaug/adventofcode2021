

def main_from_input(content: str):
    fish_timers = [int(x) for x in content.strip().split(",")]

    for _ in range(80):
        fish_timers = step_fish_timers(fish_timers)
    
    score = len(fish_timers)
    print(score)
    return score

def step_fish_timers(fish_timers: list[int]) -> list[int]:
    new_fishes_with_timers = []
    new_fish_timers = []

    for fish_timer in fish_timers:
        if fish_timer == 0:
            new_fish_timers.append(6)
            new_fishes_with_timers.append(8)
        else:
            new_fish_timers.append(fish_timer - 1)
    
    new_fish_timers.extend(new_fishes_with_timers)
    return new_fish_timers

def main():
    with open("06/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
3,4,3,1,2
""") == 5934

if __name__ == "__main__":
    main()
