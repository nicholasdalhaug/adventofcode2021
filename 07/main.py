def main_from_input(content: str):
    values = [int(x) for x in content.strip().split(",")]

    a = 0
    n_fuel = float("inf")
    new_n_fuel = n_fuel

    while new_n_fuel <= n_fuel:
        n_fuel = new_n_fuel

        a += 1
        new_n_fuel = sum([abs(x-a) for x in values])

    a -= 1
    print(n_fuel)
    return n_fuel



def main():
    with open("07/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
16,1,2,0,4,2,7,1,2,14
""") == 37

if __name__ == "__main__":
    main()
