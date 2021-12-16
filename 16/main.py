import math

class SubPacket:
    def __init__(self, bin_packet) -> None:
        self.bin = bin_packet

        self.packet_version = bin_packet[:3]
        self.type_id = bin_packet[3:6]

        self.sub_packets: list[SubPacket] = []

        if self.type_id == "100":
            i = 6
            literals = []
            while bin_packet[i] == "1":
                literal = bin_packet[i+1:i+5]
                literals.append(literal)
                i += 5
            assert bin_packet[i] == "0"
            literal = bin_packet[i+1:i+5]
            literals.append(literal)
            self.bin = self.bin[:i+5]

            self.literal = "".join(literals)
        else:
            self.length_type_id = bin_packet[6]
            if self.length_type_id == "0":
                total_length_of_sub_packets = int(bin_packet[7:22],2)
                self.bin = self.bin[:22+total_length_of_sub_packets]
                
                i = 22
                while i < len(self.bin):
                    sub_bin = self.bin[i:]
                    sub_packet = SubPacket(sub_bin)
                    self.sub_packets.append(sub_packet)

                    i += len(sub_packet.bin)
            else:
                assert self.length_type_id == "1"
                number_of_sub_packets = int(bin_packet[7:18],2)
                for _ in range(number_of_sub_packets):
                    length_so_far = sum(len(sub.bin) for sub in self.sub_packets)
                    sub_bin = bin_packet[18+length_so_far:]
                    sub_packet = SubPacket(sub_bin)
                    self.sub_packets.append(sub_packet)
                length_sub_packets = sum(len(sub.bin) for sub in self.sub_packets)
                self.bin = self.bin[:18+length_sub_packets]
        
    def get_sum_version_numbers(self) -> int:
        sum_versions = int(self.packet_version, 2)
        for sub_packet in self.sub_packets:
            sum_versions += sub_packet.get_sum_version_numbers()
        return sum_versions
    
    def get_value(self):
        type_id = int(self.type_id,2)

        values = [p.get_value() for p in self.sub_packets]

        if type_id == 4:
            return int(self.literal,2)
        if type_id == 0:
            return sum(values)
        if type_id == 1:
            return math.prod(values)
        if type_id == 2:
            return min(values)
        if type_id == 3:
            return max(values)
        if type_id == 5:
            return 1 if values[0] > values[1] else 0
        if type_id == 6:
            return 1 if values[0] < values[1] else 0
        if type_id == 7:
            return 1 if values[0] == values[1] else 0
        raise Exception(f"No such type id {type_id}")

def main_from_input(content: str):
    hex_transmission_str = content.strip()
    bin_transmission = f"{int(hex_transmission_str, 16):0>{len(hex_transmission_str)*4}b}"

    packet = SubPacket(bin_transmission)

    score = packet.get_value()

    print(score)
    return score

def main():
    with open("16/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

assert main_from_input("""
C200B40A82
""") == 3

assert main_from_input("""
04005AC33890
""") == 54

assert main_from_input("""
880086C3E88112
""") == 7

assert main_from_input("""
CE00C43D881120
""") == 9

assert main_from_input("""
D8005AC2A8F0
""") == 1

assert main_from_input("""
F600BC2D8F
""") == 0

assert main_from_input("""
9C005AC2F8F0
""") == 0

assert main_from_input("""
9C0141080250320F1802104A08
""") == 1

if __name__ == "__main__":
    main()
