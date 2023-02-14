def combine_hexes(hex_1, hex_2):
    hex_1 = hex_1[2:]
    if len(hex_1) == 1:
        hex_1 = "0" + hex_1

    hex_2 = hex_2[2:]
    if len(hex_2) == 1:
        hex_2 = "0" + hex_2

    return (hex_1 + hex_2).upper()


class Chip8:
    def __init__(self):
        self.PC = 0x200
        self.RAM = [0] * 4096
        self.V = [0] * 16
        self.DT = 0
        self.ST = 0
        self.I = 0
        self.SP = 0
        self.stack = [0] * 16

        self.Display = []

        for i in range(32):
            self.Display.append([0] * 64)

        self.characters = [['0xF0', '0x90', '0x90', '0x90', '0xF0'], ['0x20', '0x60', '0x20', '0x20', '0x70'],
                           ['0xF0', '0x10', '0xF0', '0x80', '0xF0'], ['0xF0', '0x10', '0xF0', '0x10', '0xF0'],
                           ['0x90', '0x90', '0xF0', '0x10', '0x10'], ['0xF0', '0x80', '0xF0', '0x10', '0xF0'],
                           ['0xF0', '0x80', '0xF0', '0x90', '0xF0'], ['0xF0', '0x10', '0x20', '0x40', '0x40'],
                           ['0xF0', '0x90', '0xF0', '0x90', '0xF0'], ['0xF0', '0x90', '0xF0', '0x10', '0xF0'],
                           ['0xF0', '0x90', '0xF0', '0x90', '0x90'], ['0xE0', '0x90', '0xE0', '0x90', '0xE0'],
                           ['0xF0', '0x80', '0x80', '0x80', '0xF0'], ['0xE0', '0x90', '0x90', '0x90', '0xE0'],
                           ['0xF0', '0x80', '0xF0', '0x80', '0xF0'], ['0xF0', '0x80', '0xF0', '0x80', '0x80']]

        for i in range(len(self.characters)):
            for j in range(5):
                HEX = self.characters[i][j]
                self.RAM[(5 * i) + j] = HEX

        path = "ROMs/IBM Logo.ch8"
        bytes_of_ROM = self.open_ROM(path)
        self.load_ROM(bytes_of_ROM)

    def update(self, ms_delay):
        amount = int(ms_delay * 0.5)
        if True or amount == 0:
            amount = 1
        for i in range(amount):
            self.one_tick()

    def one_tick(self):
        instruction = self.get_next_opcode()
        self.run_opcode(instruction)

    def open_ROM(self, path):
        """

        :rtype: bytearray
        """
        with open(path, "rb") as f:
            bytes_of_ROM = f.read()
        return bytes_of_ROM

    def load_ROM(self, bytes_of_ROM):
        start = 0x200
        for byte in bytes_of_ROM:
            HEX_format = "0x{:02x}".format(byte)
            self.RAM[start] = HEX_format
            start += 1

    def get_current_byte_at_address(self, address):
        return self.RAM[address]

    def get_current_byte_at_PC(self):
        byte = self.get_current_byte_at_address(self.PC)
        self.PC += 1
        return byte

    def get_next_opcode(self):
        hex_1 = self.get_current_byte_at_PC()
        hex_2 = self.get_current_byte_at_PC()
        return combine_hexes(hex_1, hex_2)

    def run_opcode(self, instruction):
        if instruction[0] == "0":

            if instruction[2:] == "E0":
                for i in range(len(self.Display)):
                    for j in range(len(self.Display[0])):
                        self.Display[i][j] = 0

            elif instruction[2:] == "EE":
                self.PC = self.stack.pop(self.SP)

        elif instruction[0] == "1":
            self.PC = int(instruction[1:], base=16)

        elif instruction[0] == "2":
            self.SP += 1
            self.stack[self.SP] = self.PC
            self.PC = int(instruction[1:], base=16)

        elif instruction[0] == "3":
            X = int(instruction[1], base=16)
            NN = int(instruction[2:], base=16)

            if self.V[X] == NN:
                self.PC += 2

        elif instruction[0] == "4":
            X = int(instruction[1], base=16)
            NN = int(instruction[2:], base=16)

            if self.V[X] != NN:
                self.PC += 2

        elif instruction[0] == "5":
            X = int(instruction[1], base=16)
            Y = int(instruction[2], base=16)

            if self.V[X] == self.V[Y]:
                self.PC += 2

        elif instruction[0] == "6":
            X = int(instruction[1], base=16)
            NN = int(instruction[2:], base=16)

            self.V[X] = NN

        elif instruction[0] == "7":
            X = int(instruction[1], base=16)
            NN = int(instruction[2:], base=16)

            self.V[X] += NN




        elif instruction[0] == "8":
            X = int(instruction[1], base=16)
            Y = int(instruction[2], base=16)

            if instruction[3] == "0":
                self.V[X] = self.V[Y]

            elif instruction[3] == "1":
                self.V[X] = self.V[X] | self.V[Y]

            elif instruction[3] == "2":
                self.V[X] = self.V[X] & self.V[Y]

            elif instruction[3] == "3":
                self.V[X] = self.V[X] ^ self.V[Y]

            elif instruction[3] == "4":

                if self.V[X] + self.V[Y] > 0xFF:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0

        elif instruction[0] == "A":
            NNN = int(instruction[1:], base=16)
            self.I = NNN

        elif instruction[0] == "D":
            X = int(instruction[1], base=16)
            Y = int(instruction[2], base=16)
            N = int(instruction[3], base=16)

            self.V[0xF] = 0

            X = self.V[X] % 64
            Y = self.V[Y] % 32

            for i in range(N):
                # if Y + i >= 32:
                #     break

                number = int(self.RAM[self.I + i][2:], base=16)
                byte = '{:08b}'.format(number)

                for j in range(8):

                    # if X + j >= 64:
                    #     break

                    bit = byte[j]

                    if bit == "1":
                        self.V[0xF] = 1
                        self.Display[Y + i][X + j] = True

                    elif bit == "1" and (not self.Display[Y + i][X + j]):
                        self.Display[Y + i][X + j] = True
