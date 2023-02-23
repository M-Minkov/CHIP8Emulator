import random

MAX8BIT = int("FF", base=16)


def wait_input():
    return 1


def convert_8bit_to_hex(byte):
    return hex(byte)[2:].upper()


class Chip8:
    def __init__(self):
        self.PC = 0x200
        self.RAM = ["00"] * 4096
        self.V = [0] * 16
        self.DT = 0
        self.ST = 0
        self.I = 0
        self.SP = 0
        self.stack = [0] * 16
        self.keys = [0] * 16

        self.Display = []

        for i in range(32):
            self.Display.append([0] * 64)

        self.characters = [
            ['F0', '90', '90', '90', 'F0'],
            ['20', '60', '20', '20', '70'],
            ['F0', '10', 'F0', '80', 'F0'],
            ['F0', '10', 'F0', '10', 'F0'],
            ['90', '90', 'F0', '10', '10'],
            ['F0', '80', 'F0', '10', 'F0'],
            ['F0', '80', 'F0', '90', 'F0'],
            ['F0', '10', '20', '40', '40'],
            ['F0', '90', 'F0', '90', 'F0'],
            ['F0', '90', 'F0', '10', 'F0'],
            ['F0', '90', 'F0', '90', '90'],
            ['E0', '90', 'E0', '90', 'E0'],
            ['F0', '80', '80', '80', 'F0'],
            ['E0', '90', '90', '90', 'E0'],
            ['F0', '80', 'F0', '80', 'F0'],
            ['F0', '80', 'F0', '80', '80']
        ]

        for i in range(len(self.characters)):
            for j in range(5):
                HEX = self.characters[i][j]
                self.RAM[(5 * i) + j] = HEX

        path = "ROMs/Coin Flipping [Carmelo Cortez, 1978].ch8"
        bytes_of_ROM = self.open_ROM(path)
        self.load_ROM(bytes_of_ROM)

    def update(self, ms_delay):
        amount = int(ms_delay * 0.5)
        if amount < 1:
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
            HEX_format = "{:02x}".format(byte)
            self.RAM[start] = HEX_format
            start += 1

    def get_byte_at_address(self, address):
        return self.RAM[address]

    def get_byte_at_PC(self):
        byte = self.get_byte_at_address(self.PC)
        self.PC += 1
        return byte

    def get_next_opcode(self):
        hex_1 = self.get_byte_at_PC()
        hex_2 = self.get_byte_at_PC()
        return hex_1 + hex_2

    def run_opcode(self, instruction):
        instruction = instruction.upper()
        if instruction[0] == "0":

            if instruction[2:] == "E0":
                for i in range(len(self.Display)):
                    for j in range(len(self.Display[0])):
                        self.Display[i][j] = 0

            elif instruction[2:] == "EE":
                self.PC = self.stack.pop(self.SP)

        elif instruction[0] == "1":
            NNN = int(instruction[1:], base=16)
            self.PC = NNN

        elif instruction[0] == "2":
            self.SP += 1
            self.stack[self.SP] = self.PC
            NNN = int(instruction[1:], base=16)
            self.PC = NNN

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

                self.V[X] += self.V[Y]
                self.V[X] %= 0xFF

            elif instruction[3] == "5":
                if self.V[X] > self.V[Y]:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0

                self.V[X] -= self.V[Y]
                self.V[X] %= 0xFF

            elif instruction[3] == "6":
                self.V[0xF] = self.V[X] & 1
                self.V[X] = self.V[X] // 2

            elif instruction[3] == "7":
                if self.V[Y] > self.V[X]:
                    self.V[0xF] = 1
                else:
                    self.V[0xF] = 0

                self.V[Y] = self.V[Y] - self.V[X]

            elif instruction[3] == "E":
                self.V[0xF] = self.V[X] & int("10000000", base=2)
                self.V[X] = self.V[X] * 2

        elif instruction[0] == "A":
            NNN = int(instruction[1:], base=16)
            self.I = NNN

        elif instruction[0] == "B":
            NNN = int(instruction[1:], base=16)
            PC = self.V[0] + NNN

        elif instruction[0] == "C":
            X = int(instruction[1], base=16)
            NN = int(instruction[2:], base=16)
            random_number = random.randint(0, 255)

            self.V[X] = random_number & NN

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

                number = int(self.RAM[self.I + i], base=16)
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

        elif instruction[0] == "E":
            X = int(instruction[1], base=16)
            NN = instruction[2:]

            if NN == "9E":
                if self.keys[self.V[X]] == 1:
                    self.PC += 2

            else:
                if self.keys[self.V[X]] == 0:
                    self.PC += 2

        elif instruction[0] == "F":
            X = int(instruction[1], base=16)
            NN = instruction[2:]

            if NN == "07":
                self.V[X] = self.DT

            elif NN == "0A":
                K = wait_input()
                self.V[X] = K

            elif NN == "15":
                self.DT = self.V[X]

            elif NN == "18":
                self.ST = self.V[X]

            elif NN == "1E":
                self.I += self.V[X]

            elif NN == "29":
                self.I = self.V[X] * 5

            elif NN == "33":
                number = self.V[X]

                H = number // 100
                T = (number - H) // 10
                O = (number - H) - T

                self.RAM[self.I] = convert_8bit_to_hex(H)
                self.RAM[self.I + 1] = convert_8bit_to_hex(T)
                self.RAM[self.I + 2] = convert_8bit_to_hex(O)

            elif NN == "55":
                for i in range(16):
                    self.RAM[self.I + i] = convert_8bit_to_hex(self.V[i])

            elif NN == "65":
                for i in range(16):
                    # print(type(self.RAM[self.I + i]))
                    self.V[i] = int(self.RAM[self.I + i], base=16)
