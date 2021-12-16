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

def main_from_input(content: str):
    hex_transmission_str = content.strip()
    bin_transmission = f"{int(hex_transmission_str, 16):0>{len(hex_transmission_str)*4}b}"

    packet = SubPacket(bin_transmission)

    score = packet.get_sum_version_numbers()

    print(score)
    return score

def main():
    with open("16/input.txt") as file:
        content = file.read()
    
    main_from_input(content)

# Type id 0
main_from_input("""
38006F45291200
""")
# Type id 1
main_from_input("""
EE00D40C823060
""")

assert main_from_input("""
8A004A801A8002F478
""") == 16

assert main_from_input("""
620080001611562C8802118E34
""") == 12

assert main_from_input("""
C0015000016115A2E0802F182340
""") == 23

assert main_from_input("""
A0016C880162017C3686B18A3D4780
""") == 31

if __name__ == "__main__":
    main()
