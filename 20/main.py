class Image:
    data: list[list[str]]

    def __init__(self, image_str: str) -> None:
        self.data = image_str.strip().split("\n")
        self.pad(".")
        self.pad(".")
        self.pad(".")
    
    def pad(self, value):
        height = len(self.data)
        width = len(self.data[0])

        for y in range(height):
            self.data[y] = [value] + list(self.data[y]) + [value]
        self.data = [[value] * (width + 2)] + self.data + [[value] * (width + 2)]
    
    def enhance(self, algorithm):
        result_data = [["." for x in range(len(self.data[0])-2)] for y in range(len(self.data)-2)]

        for y in range(1, len(self.data)-1):
            for x in range(1, len(self.data[0])-1):
                coords = [  (x-1, y-1), (x, y-1), (x+1, y-1),
                            (x-1, y), (x, y), (x+1, y),
                            (x-1, y+1), (x, y+1), (x+1, y+1)]
                values = [self.data[y][x] for x, y in coords]
                bin_value = "".join(["1" if v == "#" else "0" for v in values])
                dec_value = int(bin_value, 2)

                result_value = algorithm[dec_value]
                result_data[y-1][x-1] = result_value
                pass
        
        self.data = result_data

        self.pad(self.data[0][0])

    def count_light(self):
        count = 0
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                value = self.data[y][x]
                if value == "#":
                    count += 1
        return count

def main_from_input(content: str):
    algorithm, image_str = content.strip().split("\n\n")

    image = Image(image_str)
    image.enhance(algorithm)
    image.enhance(algorithm)

    score = image.count_light()
    print(score)
    return score


def main():
    with open("20/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
""") == 35

if __name__ == "__main__":
    main()
