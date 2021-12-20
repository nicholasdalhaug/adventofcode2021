from dataclasses import dataclass
import math

@dataclass
class TargetArea:
    x_from: int # Lowest
    y_from: int # Lowest
    x_to: int # Highest
    y_to: int # Highest

# x is forward
# y is up/down

class Trajectory:
    def __init__(self, vx_initial: int, vy_initial: int, area: TargetArea) -> None:
        self.vx_initial = vx_initial
        self.vy_initial = vy_initial

        self.positions = []

        vx = vx_initial
        vy = vy_initial

        current_pos = (0,0)
        while not self._check_if_past(current_pos, area):
            self.positions.append(current_pos)
            last_x, last_y = current_pos

            next_x = last_x + vx
            next_y = last_y + vy
            vx = max(0, vx - 1)
            vy -= 1
            

            current_pos = (next_x, next_y)
        
        self.is_hit_area = False
        end_x, end_y = self.positions[-1]
        if area.x_from <= end_x <= area.x_to and \
            area.y_from <= end_y <= area.y_to:
            self.is_hit_area = True

    def _check_if_past(self, pos: tuple[int, int], area: TargetArea) -> bool:
        x, y = pos

        if x <= area.x_to and y >= area.y_from:
            return False
        return True

    def get_highest_y(self) -> int: 
        return max([pos[1] for pos in self.positions])

def main_from_input(content: str):
    x_str, y_str = content.strip().lstrip("target area: ").split(", ")
    x_s = [int(x) for x in x_str.lstrip("x=").split("..")]
    y_s = [int(y) for y in y_str.lstrip("y=").split("..")]
    area = TargetArea(x_s[0], y_s[0], x_s[1], y_s[1])

    vx_from = (-1 + math.sqrt(1 + 8*area.x_from))/2
    vx_range = range(int(vx_from), area.x_to + 1)
    vy_range = range(area.y_from, max(abs(area.y_from), abs(area.y_to)) + 1)

    trajectories: list[Trajectory] = []
    for vx in vx_range:
        for vy in vy_range:
            t = Trajectory(vx, vy, area)
            if t.is_hit_area:
                trajectories.append(t)
    t_heights = [t.get_highest_y() for t in trajectories]
    max_y = max(t_heights)
    t_max_i = t_heights.index(max_y)
    t_max = trajectories[t_max_i]
    
    score = len(trajectories)
    print(score)
    return score


def main():
    with open("17/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
target area: x=20..30, y=-10..-5
""") == 112

if __name__ == "__main__":
    main()
