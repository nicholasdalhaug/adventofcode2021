import itertools
import numpy as np
from scipy.spatial.transform import Rotation as R

class MyException(Exception):
    pass

class Scanner:
    pass

class Scanner:
    name: int
    beacon_coords: list[list[int]]

    t: np.array = None
    R_m: np.array = None

    def __init__(self, name, coords) -> None:
        self.name = name
        self.beacon_coords = coords
    
    def align_with_r(self, scanner: Scanner):
        for p_here in self.beacon_coords:
            for p_there in scanner.beacon_coords:
                p = np.array(p_here)
                p_sol = np.array(p_there)

                for r_x, r_y, r_z in itertools.product([0, 90, 180, 270], repeat=3):
                    R_x = R.from_euler('x', r_x, degrees=True).as_matrix()
                    R_y = R.from_euler('y', r_y, degrees=True).as_matrix()
                    R_z = R.from_euler('z', r_z, degrees=True).as_matrix()
                    R_m = np.dot(R_x, np.dot(R_y, R_z))

                    p_rotated = np.dot(R_m, p)
                    t = p_sol - p_rotated

                    ps_here_transformed = (np.dot(R_m, np.array(self.beacon_coords).T)).T + t
                    if self.at_least_12_equal(ps_here_transformed, np.array(scanner.beacon_coords)):
                        self.t = t
                        self.R_m = R_m
                        return
        raise MyException("Found no solution")
        

    def at_least_12_equal(self, ps_here, ps_there):
        ps_here_set = set([tuple(np.rint(p)) for p in ps_here])
        ps_there_set = set([tuple(p) for p in ps_there])
        commons = set.intersection(ps_here_set, ps_there_set)
        
        if len(commons) >= 12:
            return True
        return False
    
    def get_transformed_points(self):
        ps_here_transformed = (np.dot(self.R_m, np.array(self.beacon_coords).T)).T + self.t
        ps_here_set = set([tuple(np.rint(p)) for p in ps_here_transformed])
        return ps_here_set
    
    def transform(self, R_m, t):
        self.R_m = np.dot(R_m, self.R_m)
        self.t = np.dot(R_m, self.t) + t

def main_from_input(content: str):
    scanners_data = content.strip().split("\n\n")

    scanners: list[Scanner] = []
    for scanner_data in scanners_data:
        lines = scanner_data.strip().split("\n")
        name = int(lines[0].lstrip("--- scanner ").rstrip(" ---"))
        coords = [[int(x) for x in line.strip().split(",")] for line in lines[1:]]
        scanner = Scanner(name, coords)
        scanners.append(scanner)

    scanners[0].t = np.array([0, 0, 0])
    scanners[0].R_m = np.identity(3)

    scanner_align_options = {key: [0] for key in range(len(scanners))}

    scanners_left = scanners[1:]
    while len(scanners_left) != 0:
        print(f"Scanners left: {len(scanners_left)}")
        is_any_placed = False
        for scanner in scanners_left:
            is_aligned = False
            while len(scanner_align_options[scanner.name]) != 0:
                scanner_placed_i = scanner_align_options[scanner.name].pop()
                scanner_placed = scanners[scanner_placed_i]
                try:
                    scanner.align_with_r(scanner_placed)

                    # Align with scanner 0
                    scanner.transform(scanner_placed.R_m, scanner_placed.t)

                    is_aligned = True
                    break
                except MyException as e:
                    continue
            if is_aligned:
                for i in scanner_align_options:
                    scanner_align_options[i].append(scanner.name)
                scanners_left.remove(scanner)
                is_any_placed = True
                break
        if not is_any_placed:
            raise MyException("No scanner possible to place!")

    beacons = set()
    for scanner in scanners:
        measurements = scanner.get_transformed_points()
        beacons = set.union(beacons, measurements)
    
    score = len(beacons)
    print(score)
    return score

#positions = [scanner.t for scanner in scanners]
#differences = [x-y for x, y in itertools.combinations(positions, 2)]
#distances = [abs(d[0]) + abs(d[1]) + abs(d[2]) for d in differences]
#max_distance = max(distances)


def main():
    with open("19/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14
""") == 79

if __name__ == "__main__":
    main()
