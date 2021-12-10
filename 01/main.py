
def main():
    with open("01/input.txt") as file:
        depth_measurements_strs = file.readlines()
    depth_measurements_nums = [int(x.strip()) for x in depth_measurements_strs]

    n_increases = count_increases(depth_measurements_nums)
    print(n_increases)

def count_increases(numbers):
    n_increases = 0
    for i in range(1, len(numbers)):
        if numbers[i] > numbers[i-1]:
            n_increases += 1

    return n_increases

if __name__ == "__main__":
    main()
