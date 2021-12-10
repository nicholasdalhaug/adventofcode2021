
def main():
    with open("01/input.txt") as file:
        depth_measurements_strs = file.readlines()
    depth_measurements_nums = [int(x.strip()) for x in depth_measurements_strs]

    window_sums = calc_3_window_sums(depth_measurements_nums)
    n_increases = count_increases(window_sums)
    print(n_increases)

def calc_3_window_sums(numbers):
    window_sums = [
        numbers[i-1] + numbers[i] + numbers[i+1]
        for i in range(1, len(numbers)-1)
    ]
    return window_sums

def count_increases(numbers):
    n_increases = 0
    for i in range(1, len(numbers)):
        if numbers[i] > numbers[i-1]:
            n_increases += 1

    return n_increases

if __name__ == "__main__":
    main()
