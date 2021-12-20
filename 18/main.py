from typing import Union
import ast
import itertools

class SnailfishNumber:
    pass

n = None

class SnailfishNumber:
    left: SnailfishNumber = None
    right: SnailfishNumber = None
    value: int = None
    parent: SnailfishNumber = None
    parent_side: str = None

    def __init__(self, numbers_list_or_int: Union[list, int, SnailfishNumber], parent: SnailfishNumber = None, parent_side: str = None) -> None:
        self.parent = parent
        self.parent_side = parent_side

        if isinstance(numbers_list_or_int, int):
            self.value = numbers_list_or_int
        elif isinstance(numbers_list_or_int, SnailfishNumber):
            self.left = numbers_list_or_int.left
            self.left.parent = self
            self.right = numbers_list_or_int.right
            self.right.parent = self
        else:
            self.left = SnailfishNumber(numbers_list_or_int[0], parent=self, parent_side="left")
            self.right = SnailfishNumber(numbers_list_or_int[1], parent=self, parent_side="right")
    
    def reduce(self):
        number_to_explode = self.get_nested_number_at_depth(4)
        if number_to_explode is not None:
            number_to_explode.explode()
            self.reduce()
        else:
            node = self.get_10_or_greater()
            if node is not None:
                node.split()
                self.reduce()
    
    def is_int(self):
        return self.value is not None

    def get_nested_number_at_depth(self, depth):
        if self.is_int():
            return None
        
        if depth == 0:
            if self.left.is_int() and self.right.is_int():
                return self
            else:
                return None
        
        if isinstance(self.left, SnailfishNumber):
            left_number = self.left.get_nested_number_at_depth(depth-1)
            if left_number is not None:
                return left_number
        
        if isinstance(self.right, SnailfishNumber):
            right_number = self.right.get_nested_number_at_depth(depth-1)
            if right_number is not None:
                return right_number
        
        return None
    
    def get_10_or_greater(self):
        if self.is_int():
            if self.value >= 10:
                return self
        else:
            left_node = self.left.get_10_or_greater()
            if left_node is not None:
                return left_node
            right_node = self.right.get_10_or_greater()
            if right_node is not None:
                return right_node
        return None
                
    
    def split(self):
        left_number = self.value // 2
        right_number = int((self.value + 1) / 2)
        number = SnailfishNumber([left_number, right_number], parent=self.parent, parent_side=self.parent_side)

        if self.parent_side == "left":
            self.parent.left = number
        else:
            self.parent.right = number

    def explode(self):
        left_value = self.left.value
        right_value = self.right.value

        left_node = self.get_first_in_direction("left")
        if left_node is not None:
            left_node.value += left_value
        
        right_node = self.get_first_in_direction("right")
        if right_node is not None:
            right_node.value += right_value
        
        self.left = None
        self.right = None
        self.value = 0
    
    def get_first_in_direction(self, dir: Union["left", "right"]):
        node = self
        if dir == "left":
            while node.parent_side == "left":
                node = node.parent
            if node.parent_side == "right":
                return node.parent.left.get_rightmost_value()
        else:
            while node.parent_side == "right":
                node = node.parent
            if node.parent_side == "left":
                return node.parent.right.get_leftmost_value()
        return None
    
    def get_rightmost_value(self):
        return self.get_farthest_direction_value("right")

    def get_leftmost_value(self):
        return self.get_farthest_direction_value("left")

    def get_farthest_direction_value(self, dir: Union["left", "right"]):
        node = self
        while not node.is_int():
            if dir == "left":
                node = node.left
            else:
                node = node.right
        return node
    
    def __repr__(self):
        if self.is_int():
            return f"{self.value}"
        else:
            return f"[{self.left}, {self.right}]"
    
    def get_magnitude(self):
        if self.is_int():
            return self.value
        
        return 3 * self.left.get_magnitude() + 2 * self.right.get_magnitude()

def snailfish_homework(snailfish_numbers: list):
    pass

def snailfish_add(n1, n2):
    new_number = SnailfishNumber([n1, n2])

    global n
    n = new_number

    new_number.reduce()
    return new_number


def main_from_input(content: str):
    lines = content.strip().split("\n")
    sf_lists = [ast.literal_eval(line.strip()) for line in lines]

    possibilities = itertools.permutations(sf_lists, 2)
    magnitudes = [snailfish_add(l1, l2).get_magnitude() for l1, l2 in possibilities]
    
    score = max(magnitudes)
    print(score)
    return score


def main():
    with open("18/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
""") == 3993

if __name__ == "__main__":
    main()
