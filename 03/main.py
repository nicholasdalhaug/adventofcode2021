from dataclasses import dataclass

@dataclass
class Report:
    gamma_rate: int
    epsilon_rate: int

def main():
    with open("03/input.txt") as file:
        numbers = [x.strip() for x in file.readlines()]

    report = calc_report(numbers)
    power_consumption = report.epsilon_rate * report.gamma_rate
    print(power_consumption)

def calc_report(numbers):
    column_sums = [0]*len(numbers[0])

    for number in numbers:
        for column_i in range(len(column_sums)):
            column_sums[column_i] += int(number[column_i])
    
    gamma_rate_arr = [str(round(x / (len(numbers)))) for x in column_sums]
    epsilon_rate_arr = ["1" if x == "0" else "0" for x in gamma_rate_arr]

    gamma_rate_dec = int("0b" + "".join(gamma_rate_arr), 2)
    epsilon_rate_dec = int("0b" + "".join(epsilon_rate_arr), 2)
    report = Report(
        gamma_rate=gamma_rate_dec, 
        epsilon_rate=epsilon_rate_dec
    )
    return report

if __name__ == "__main__":
    main()