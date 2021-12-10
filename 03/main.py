from dataclasses import dataclass

@dataclass
class GammaAndEpsilonReport:
    gamma_rate: str
    epsilon_rate: str

def main():
    with open("03/input.txt") as file:
        numbers = [x.strip() for x in file.readlines()]

    ox_rating = calc_ox_rating(numbers)
    co2_rating = calc_co2_rating(numbers)
    life_support_rating = ox_rating * co2_rating
    print(life_support_rating)

def calc_gamma_and_epsilon_report(numbers):
    column_sums = calc_column_sums(numbers)
    
    gamma_rate_arr = [str(math_round(x / (len(numbers)))) for x in column_sums]
    epsilon_rate_arr = ["1" if x == "0" else "0" for x in gamma_rate_arr]

    gamma_rate_bin = "".join(gamma_rate_arr)
    epsilon_rate_bin = "".join(epsilon_rate_arr)

    report = GammaAndEpsilonReport(
        gamma_rate=gamma_rate_bin, 
        epsilon_rate=epsilon_rate_bin
    )
    return report

def math_round(num):
    return int(num + 0.5)

def calc_column_sums(numbers):
    column_sums = [0]*len(numbers[0])

    for number in numbers:
        for column_i in range(len(column_sums)):
            column_sums[column_i] += int(number[column_i])
    
    return column_sums

def calc_ox_rating(numbers, bit_n=0):
    # Using default bit_n to make this a simple recursive function
    g_and_e_report = calc_gamma_and_epsilon_report(numbers)
    mask = g_and_e_report.gamma_rate

    if len(numbers) == 1:
        return int(numbers[0], 2)
    elif len(numbers) == 0:
        raise Exception("What?")
    
    new_numbers = list(filter(lambda num: num[bit_n] == mask[bit_n], numbers))
    result = calc_ox_rating(new_numbers, bit_n+1)
    return result

def calc_co2_rating(numbers, bit_n=0):
    # Using default bit_n to make this a simple recursive function
    g_and_e_report = calc_gamma_and_epsilon_report(numbers)
    mask = g_and_e_report.epsilon_rate

    if len(numbers) == 1:
        return int(numbers[0], 2)
    elif len(numbers) == 0:
        raise Exception("What?")
    
    new_numbers = list(filter(lambda num: num[bit_n] == mask[bit_n], numbers))
    result = calc_co2_rating(new_numbers, bit_n+1)
    return result

assert calc_ox_rating([
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010'
]) == 23

assert calc_co2_rating([
    '00100',
    '11110',
    '10110',
    '10111',
    '10101',
    '01111',
    '00111',
    '11100',
    '10000',
    '11001',
    '00010',
    '01010'
]) == 10

if __name__ == "__main__":
    main()