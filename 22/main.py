from enum import Enum
from dataclasses import dataclass

class CubeState(Enum):
    OFF = 0
    ON = 1

def cube_state_from_string(cube_state: str) -> CubeState:
    if cube_state == "on": return CubeState.ON
    else: return CubeState.OFF

@dataclass
class CuboidRegion:
    x_from: int
    y_from: int
    z_from: int
    x_to: int
    y_to: int
    z_to: int

class Cuboid:
    pass

# A cuboid without children has all cubes ON in its region
class Cuboid:
    children: list[Cuboid]
    region: CuboidRegion

    def __init__(self, region: CuboidRegion) -> None:
        self.region = region
        self.children = []
    
    def count_on(self):
        if len(self.children) == 0:
            width = self.region.x_to + 1 - self.region.x_from
            height = self.region.z_to + 1 - self.region.z_from
            depth = self.region.y_to + 1 - self.region.y_from
            n_on = width * height * depth
            return n_on
        else:
            children_count_sum = sum([c.count_on() for c in self.children])
            return children_count_sum
    
    def _ensure_covering(self, region: CuboidRegion):
        self.region.x_from = min(self.region.x_from, region.x_from)
        self.region.x_to = max(self.region.x_to, region.x_to)
        self.region.y_from = min(self.region.y_from, region.y_from)
        self.region.y_to = max(self.region.y_to, region.y_to)
        self.region.z_from = min(self.region.z_from, region.z_from)
        self.region.z_to = max(self.region.z_to, region.z_to)

    def turn_off(self, region: CuboidRegion):
        if check_if_region_outside(self.region, region):
            return
        
        if len(self.children) == 0:
            new_regions = split_region(self.region, region)
            new_regions_on = list(filter(lambda r: check_if_region_outside(region, r), new_regions))
            self.children = [Cuboid(sub_reg) for sub_reg in new_regions_on]
            if len(self.children) == 0:
                self.region = CuboidRegion(0, 0, 0, -1, -1, -1)
            return
        
        children_to_remove = []
        for child in self.children:
            if check_if_region_covering(region, child.region):
                children_to_remove.append(child)
            elif check_if_region_outside(region, child.region):
                continue
            else:
                child.turn_off(region)
        
        for child in children_to_remove:
            self.children.remove(child)
        
        if len(self.children) == 0:
            self.region = CuboidRegion(0, 0, 0, -1, -1, -1)
    
    def change_state(self, region: CuboidRegion, state: CubeState):
        if state == CubeState.OFF:
            self.turn_off(region)
        else:
            if len(self.children) == 0:
                self.children.append(Cuboid(copy_region(self.region)))
            self.turn_off(region)
            self._ensure_covering(region)
            
            self.children.append(Cuboid(region))

        # if check_if_region_outside(self.region, region):
        #     if len(self.children) == 0:
        #         if state == CubeState.OFF:
        #             return
        #         self.children.append(Cuboid(CuboidRegion(self.region)))
        #         self.children.append(Cuboid(CuboidRegion(region)))
        #         self._ensure_covering(region)
        #         return
        #     else:
        #         self.children.append(Cuboid(CuboidRegion(region)))
        #         self._ensure_covering(region)
        #         return
        # elif check_if_region_covering(self.region, region):
        #     if len(self.children) == 0:
        #         if state == CubeState.ON:
        #             return
        #         else:
        #             new_regions = split_region(self.region, region) + split_region(region, self.region)
        #             new_unique_regions = remove_multiples(new_regions)
        #             new_regions_on = filter(lambda sub_reg: not check_if_region_covering(region, sub_reg), new_unique_regions)
        #             self.children = [Cuboid(sub_reg) for sub_reg in new_regions_on]
        #             return
        #     else:
        #         # Can have collisions between children and new region
        #         pass
        # else:
        #     if len(self.children) == 0:
        #         self.children.append(Cuboid(CuboidRegion(self.region)))
        #     self._ensure_covering(region)
        #     # TODO: Ensure that the increase does not collide with other cuboids
                
        # # We are now covering the region, but possibly have multiple children colliding with it. 
        # children_colliding = filter(lambda c: check_if_region_collides(c.region, region), self.children)

def split_region(region_to_split: CuboidRegion, region_based_on: CuboidRegion) -> list[CuboidRegion]:
    regions_to_split = [region_to_split]
    if region_to_split.x_from < region_based_on.x_from <= region_to_split.x_to:
        regions_to_split = split_regions_along(regions_to_split, "x", region_based_on.x_from)
    if region_to_split.x_from <= region_based_on.x_to < region_to_split.x_to:
        regions_to_split = split_regions_along(regions_to_split, "x", region_based_on.x_to+1)
    if region_to_split.y_from < region_based_on.y_from <= region_to_split.y_to:
        regions_to_split = split_regions_along(regions_to_split, "y", region_based_on.y_from)
    if region_to_split.y_from <= region_based_on.y_to < region_to_split.y_to:
        regions_to_split = split_regions_along(regions_to_split, "y", region_based_on.y_to+1)
    if region_to_split.z_from < region_based_on.z_from <= region_to_split.z_to:
        regions_to_split = split_regions_along(regions_to_split, "z", region_based_on.z_from)
    if region_to_split.z_from <= region_based_on.z_to < region_to_split.z_to:
        regions_to_split = split_regions_along(regions_to_split, "z", region_based_on.z_to+1)
    return regions_to_split

def split_regions_along(regions: list[CuboidRegion], axis: str, value: int) -> list[CuboidRegion]:
    new_regions = []
    for region in regions:
        if axis == "x" and region.x_from < value <= region.x_to:
            new_regions.append(CuboidRegion(region.x_from, region.y_from, region.z_from, value-1, region.y_to, region.z_to))
            new_regions.append(CuboidRegion(value, region.y_from, region.z_from, region.x_to, region.y_to, region.z_to))
        elif axis == "y" and region.y_from < value <= region.y_to:
            new_regions.append(CuboidRegion(region.x_from, region.y_from, region.z_from, region.x_to, value-1, region.z_to))
            new_regions.append(CuboidRegion(region.x_from, value, region.z_from, region.x_to, region.y_to, region.z_to))
        elif axis == "z" and region.z_from < value <= region.z_to:
            new_regions.append(CuboidRegion(region.x_from, region.y_from, region.z_from, region.x_to, region.y_to, value-1))
            new_regions.append(CuboidRegion(region.x_from, region.y_from, value, region.x_to, region.y_to, region.z_to))
        else:
            new_regions.append(region)
    return new_regions

# def remove_multiples(regions: list[CuboidRegion]) -> list[CuboidRegion]:
#     unique_region_tuples = set([(r.x_from, r.y_from, r.z_from, r.x_to, r.y_to, r.z_to) for r in regions])
#     unique_regions = [CuboidRegion(x_from, y_from, z_from, x_to, y_to, z_to) for x_from, y_from, z_from, x_to, y_to, z_to in unique_region_tuples]
#     return unique_regions

def check_if_region_covering(super_region: CuboidRegion, sub_region: CuboidRegion) -> bool:
    return super_region.x_from <= sub_region.x_from and \
        sub_region.x_to <= super_region.x_to and \
        super_region.y_from <= sub_region.y_from and \
        sub_region.y_to <= super_region.y_to and \
        super_region.z_from <= sub_region.z_from and \
        sub_region.z_to <= super_region.z_to

def check_if_region_outside(super_region: CuboidRegion, sub_region: CuboidRegion) -> bool:
    return sub_region.x_to < super_region.x_from or \
        sub_region.x_from > super_region.x_to or \
        sub_region.y_to < super_region.y_from or \
        sub_region.y_from > super_region.y_to or \
        sub_region.z_to < super_region.z_from or \
        sub_region.z_from > super_region.z_to

def check_if_region_collides(super_region: CuboidRegion, sub_region: CuboidRegion) -> bool:
    return not check_if_region_outside(super_region, sub_region)

def copy_region(region: CuboidRegion) -> CuboidRegion:
    return CuboidRegion(region.x_from, region.y_from, region.z_from, region.x_to, region.y_to, region.z_to)

def main_from_input(content: str):
    reboot_steps = content.strip().split("\n")

    cuboid = None
    for step in reboot_steps:
        parts = step.strip().split()
        new_state = cube_state_from_string(parts[0])
        region_str = parts[1]
        region_dims_nums = [[int(x) for x in p.split("=")[1].split("..")] for p in region_str.split(",")]

        cuboid_region = CuboidRegion(region_dims_nums[0][0], region_dims_nums[1][0], region_dims_nums[2][0], region_dims_nums[0][1], region_dims_nums[1][1], region_dims_nums[2][1])

        if check_if_region_outside(CuboidRegion(-50, -50, -50, 50, 50, 50), cuboid_region):
            continue

        if cuboid is None:
            assert new_state == CubeState.ON
            cuboid = Cuboid(cuboid_region)
        else:
            cuboid.change_state(cuboid_region, new_state)
        
        #print(cuboid.count_on())
        print("",end="")
    
    score = cuboid.count_on()
    print(score)
    return score

def main():
    with open("22/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

# 1D tests

## Has been helpful
assert main_from_input("""
on x=0..2,y=10..10,z=10..10
off x=-49..10,y=10..10,z=10..10
""") == 0

## Has been helpful
assert main_from_input("""
on x=10..12,y=10..10,z=10..10
on x=14..16,y=10..10,z=10..10
off x=12..14,y=10..10,z=10..10
""") == 4



print("", end="")

# 2D tests
assert main_from_input("""
on x=10..11,y=10..11,z=10..10
on x=7..8,y=10..11,z=10..10
off x=8..10,y=11..12,z=10..10
""") == 6

print("", end="")



assert main_from_input("""
on x=9..11,y=9..11,z=10..10
on x=10..12,y=10..12,z=10..10
""") == 14

assert main_from_input("""
on x=9..11,y=9..11,z=10..10
on x=10..12,y=10..12,z=10..10
""") == 14

assert main_from_input("""
on x=9..11,y=9..11,z=10..10
off x=10..12,y=10..12,z=10..10
on x=9..11,y=9..11,z=10..10
off x=10..12,y=10..12,z=10..10
""") == 5

assert main_from_input("""
on x=10..12,y=10..12,z=10..10
off x=9..11,y=9..11,z=10..10
""") == 5

assert main_from_input("""
on x=-12..-10,y=-12..-10,z=-10..-10
off x=-11..-9,y=-11..-9,z=-10..-10
""") == 5






assert main_from_input("""
on x=10..12,y=10..12,z=10..10
on x=11..13,y=11..13,z=10..10
off x=9..11,y=9..11,z=10..10
on x=10..10,y=10..10,z=10..10
""") == 11

assert main_from_input("""
on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10
""") == 39

print("", end="")

assert main_from_input("""
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
""") == 590784

assert main_from_input("""
on x=-20..26,y=-36..17,z=-47..7
on x=-20..33,y=-21..23,z=-26..28
on x=-22..28,y=-29..23,z=-38..16
on x=-46..7,y=-6..46,z=-50..-1
on x=-49..1,y=-3..46,z=-24..28
on x=2..47,y=-22..22,z=-23..27
on x=-27..23,y=-28..26,z=-21..29
on x=-39..5,y=-6..47,z=-3..44
on x=-30..21,y=-8..43,z=-13..34
on x=-22..26,y=-27..20,z=-29..19
off x=-48..-32,y=26..41,z=-47..-37
on x=-12..35,y=6..50,z=-50..-2
off x=-48..-32,y=-32..-16,z=-15..-5
on x=-18..26,y=-33..15,z=-7..46
off x=-40..-22,y=-38..-28,z=23..41
on x=-16..35,y=-41..10,z=-47..6
off x=-32..-23,y=11..30,z=-14..3
on x=-49..-5,y=-3..45,z=-29..18
off x=18..30,y=-20..-8,z=-3..13
on x=-41..9,y=-7..43,z=-33..15
on x=-54112..-39298,y=-85059..-49293,z=-27449..7877
on x=967..23432,y=45373..81175,z=27513..53682
""") == 590784

if __name__ == "__main__":
    main()
