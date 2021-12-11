from dataclasses import dataclass

@dataclass
class BingoCell:
    value: int
    is_marked: bool

class BingoBoard:
    cell_matrix: list[list[BingoCell]]
    has_bingo: bool = False

    def __init__(self, cell_matrix_str) -> None:
        self.cell_matrix = [
            [BingoCell(int(value_str), False) for value_str in line_str.strip().split()]
            for line_str in cell_matrix_str
        ]
    
    def mark_if_exists(self, value) -> None:
        for x in range(len(self.cell_matrix[0])):
            for y in range(len(self.cell_matrix)):
                x_y_value = self.cell_matrix[y][x].value
                if x_y_value == value:
                    self.mark(x, y)
    
    def mark(self, x, y) -> None:
        self.cell_matrix[y][x].is_marked = True

        row = self.cell_matrix[y]
        col = [self.cell_matrix[y_i][x] for y_i in range(len(self.cell_matrix))]

        if check_if_all_marked(row) or check_if_all_marked(col):
            self.has_bingo = True
    
    def get_sum_of_unmarked_numbers(self):
        result_sum = 0

        for x in range(len(self.cell_matrix[0])):
            for y in range(len(self.cell_matrix)):
                cell = self.cell_matrix[y][x]
                if not cell.is_marked:
                    result_sum += cell.value
        
        return result_sum


def check_if_all_marked(cells: list[BingoCell]) -> bool:
    for cell in cells:
        if not cell.is_marked:
            return False
    return True

def play_from_input(input_content: str):
    content_parts = input_content.split("\n\n")
    number_sequence = [int(x) for x in content_parts[0].strip().split(",")]
    boards = [BingoBoard(boards_str.strip().split("\n")) for boards_str in content_parts[1:]]
    
    score = play_bingo(boards, number_sequence)
    print(score)
    return score

def play_bingo(boards:list[BingoBoard], number_sequence):
    step_i = 0
    board_that_has_bingo = None

    while board_that_has_bingo is None and step_i < len(number_sequence):
        number = number_sequence[step_i]

        print(f"The number is {number}")

        for board in boards:
            board.mark_if_exists(number)
        
        indices_to_pop = []
        for board_i in range(len(boards)):
            board = boards[board_i]
            if board.has_bingo:
                if len(boards) == 1:
                    board_that_has_bingo = boards[0]
                    break
                indices_to_pop.append(board_i)
        
        for index_to_pop in sorted(indices_to_pop, reverse=True):
            boards.pop(index_to_pop)
        
        
        
        step_i += 1
    
    if board_that_has_bingo is not None:
        score = calc_board_score(board_that_has_bingo, number)
        return score
    else:
        pass

def calc_board_score(board: BingoBoard, winning_number: int) -> int:
    unmarked_sum = board.get_sum_of_unmarked_numbers()
    score = unmarked_sum * winning_number
    return score

def main():
    with open("04/input.txt") as file:
        content = file.read()
    
    play_from_input(content)

assert play_from_input("""
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""") == 1924

if __name__ == "__main__":
    main()
