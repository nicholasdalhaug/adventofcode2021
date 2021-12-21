from dataclasses import dataclass

@dataclass
class Player:
    position: int
    score: int = 0

class DiracDice:
    p1: Player
    p2: Player

    n_dice_rolls = 0
    n_dice_sides = 100
    n_spaces = 10

    def __init__(self, p1_start, p2_start) -> None:
        self.p1 = Player(p1_start)
        self.p2 = Player(p2_start)

    def play(self):
        while True:
            dice_rolls = [self.get_dice_roll() for _ in range(3)]
            p1_rolls_sum = sum(dice_rolls)
            p1_new_loc = (self.p1.position + p1_rolls_sum - 1) % self.n_spaces + 1
            self.p1.score += p1_new_loc
            self.p1.position = p1_new_loc
            if self.p1.score >= 1000:
                return
            
            dice_rolls = [self.get_dice_roll() for _ in range(3)]
            p2_rolls_sum = sum(dice_rolls)
            p2_new_loc = (self.p2.position + p2_rolls_sum - 1) % self.n_spaces + 1
            self.p2.score += p2_new_loc
            self.p2.position = p2_new_loc
            if self.p2.score >= 1000:
                return
            
            pass

    def get_dice_roll(self):
        dice_value = (self.n_dice_rolls + 1 - 1) % self.n_dice_sides + 1
        self.n_dice_rolls += 1
        return dice_value

    def get_score(self):
        lose_points = min(self.p1.score, self.p2.score)
        game_score = lose_points * self.n_dice_rolls
        return game_score


def main_from_input(content: str):
    p1_str, p2_str = content.strip().split("\n")
    p1_start = int(p1_str.strip()[-1])
    p2_start = int(p2_str.strip()[-1])

    game = DiracDice(p1_start, p2_start)
    game.play()

    score = game.get_score()
    print(score)
    return score

def main():
    with open("21/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
Player 1 starting position: 4
Player 2 starting position: 8
""") == 739785

if __name__ == "__main__":
    main()
