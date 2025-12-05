import random
from pathlib import Path

MAX8BIT = int("FF", base=16)
DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 32

FONT_SET = [
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


class Chip8:
	def __init__(self):
		self.characters = FONT_SET
		self.clock_hz = 700
		self.ms_per_timer = 1000 / 60
		self.timer_accumulator = 0.0
		self.waiting_register = None
		self.rom_loaded = False
		self.loaded_rom_bytes = None
		self.rom_path = None
		self.reset()

	def reset(self):
		self.PC = 0x200
		self.RAM = [0] * 4096
		self.V = [0] * 16
		self.DT = 0
		self.ST = 0
		self.I = 0
		self.SP = -1
		self.stack = [0] * 16
		self.keys = [0] * 16
		self.Display = [[0 for _ in range(DISPLAY_WIDTH)] for _ in range(DISPLAY_HEIGHT)]
		self.timer_accumulator = 0.0
		self.waiting_register = None
		self.rom_loaded = False
		for i in range(len(self.characters)):
			for j in range(5):
				hex_value = self.characters[i][j]
				self.RAM[(5 * i) + j] = int(hex_value, base=16)

	def load_rom_from_path(self, path):
		rom_path = Path(path)
		bytes_of_ROM = self.open_ROM(rom_path)
		self.reset()
		self.load_ROM(bytes_of_ROM)
		self.rom_path = str(rom_path)

	def reload_current_rom(self):
		if self.loaded_rom_bytes is None:
			return
		data = bytes(self.loaded_rom_bytes)
		self.reset()
		self.load_ROM(data)

	def update(self, ms_delay):
		if not self.rom_loaded:
			return
		cycles = max(1, int((ms_delay / 1000.0) * self.clock_hz))
		for _ in range(cycles):
			self.one_tick()
		self._update_timers(ms_delay)

	def _update_timers(self, ms_delay):
		self.timer_accumulator += ms_delay
		while self.timer_accumulator >= self.ms_per_timer:
			if self.DT > 0:
				self.DT -= 1
			if self.ST > 0:
				self.ST -= 1
			self.timer_accumulator -= self.ms_per_timer

	def set_key_state(self, key_index, pressed):
		if key_index < 0 or key_index >= len(self.keys):
			return
		self.keys[key_index] = 1 if pressed else 0
		if pressed and self.waiting_register is not None:
			self.V[self.waiting_register] = key_index
			self.waiting_register = None

	def one_tick(self):
		if not self.rom_loaded:
			return
		if self.waiting_register is not None:
			return
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
			self.RAM[start] = byte
			start += 1
		self.loaded_rom_bytes = bytes(bytes_of_ROM)
		self.rom_loaded = True

	def get_byte_at_address(self, address):
		return self.RAM[address]

	def get_byte_at_PC(self):
		byte = self.get_byte_at_address(self.PC)
		self.PC += 1
		return byte

	def get_next_opcode(self):
		hex_1 = self.get_byte_at_PC()
		hex_2 = self.get_byte_at_PC()
		return (hex_1 << 8) | hex_2

	def run_opcode(self, instruction):
		instruction &= 0xFFFF
		opcode = instruction & 0xF000
		X = (instruction & 0x0F00) >> 8
		Y = (instruction & 0x00F0) >> 4
		NNN = instruction & 0x0FFF
		NN = instruction & 0x00FF
		N = instruction & 0x000F

		if opcode == 0x0000:
			if instruction == 0x00E0:
				for i in range(len(self.Display)):
					for j in range(len(self.Display[0])):
						self.Display[i][j] = 0
			elif instruction == 0x00EE:
				if self.SP < 0:
					return
				self.PC = self.stack[self.SP]
				self.SP -= 1
		elif opcode == 0x1000:
			self.PC = NNN
		elif opcode == 0x2000:
			self.SP = (self.SP + 1) % len(self.stack)
			self.stack[self.SP] = self.PC
			self.PC = NNN
		elif opcode == 0x3000:
			if self.V[X] == NN:
				self.PC += 2
		elif opcode == 0x4000:
			if self.V[X] != NN:
				self.PC += 2
		elif opcode == 0x5000:
			if (instruction & 0x000F) == 0 and self.V[X] == self.V[Y]:
				self.PC += 2
		elif opcode == 0x6000:
			self.V[X] = NN
		elif opcode == 0x7000:
			self.V[X] = (self.V[X] + NN) & MAX8BIT
		elif opcode == 0x8000:
			last_nibble = instruction & 0x000F
			if last_nibble == 0x0:
				self.V[X] = self.V[Y]
			elif last_nibble == 0x1:
				self.V[X] = self.V[X] | self.V[Y]
			elif last_nibble == 0x2:
				self.V[X] = self.V[X] & self.V[Y]
			elif last_nibble == 0x3:
				self.V[X] = self.V[X] ^ self.V[Y]
			elif last_nibble == 0x4:
				result = self.V[X] + self.V[Y]
				self.V[0xF] = 1 if result > MAX8BIT else 0
				self.V[X] = result & MAX8BIT
			elif last_nibble == 0x5:
				self.V[0xF] = 1 if self.V[X] >= self.V[Y] else 0
				self.V[X] = (self.V[X] - self.V[Y]) & MAX8BIT
			elif last_nibble == 0x6:
				self.V[0xF] = self.V[X] & 1
				self.V[X] = (self.V[X] >> 1) & MAX8BIT
			elif last_nibble == 0x7:
				self.V[0xF] = 1 if self.V[Y] >= self.V[X] else 0
				self.V[X] = (self.V[Y] - self.V[X]) & MAX8BIT
			elif last_nibble == 0xE:
				self.V[0xF] = 1 if (self.V[X] & 0x80) else 0
				self.V[X] = (self.V[X] << 1) & MAX8BIT
		elif opcode == 0x9000:
			if (instruction & 0x000F) == 0 and self.V[X] != self.V[Y]:
				self.PC += 2
		elif opcode == 0xA000:
			self.I = NNN
		elif opcode == 0xB000:
			self.PC = (self.V[0] + NNN) & 0xFFF
		elif opcode == 0xC000:
			random_number = random.randint(0, 255)
			self.V[X] = random_number & NN
		elif opcode == 0xD000:
			self.draw_sprite(X, Y, N)
		elif opcode == 0xE000:
			key_index = self.V[X] & 0xF
			if NN == 0x9E:
				if self.keys[key_index] == 1:
					self.PC += 2
			elif NN == 0xA1:
				if self.keys[key_index] == 0:
					self.PC += 2
		elif opcode == 0xF000:
			if NN == 0x07:
				self.V[X] = self.DT
			elif NN == 0x0A:
				self.waiting_register = X
			elif NN == 0x15:
				self.DT = self.V[X]
			elif NN == 0x18:
				self.ST = self.V[X]
			elif NN == 0x1E:
				self.I += self.V[X]
				if self.I > 0xFFF:
					self.V[0xF] = 1
					self.I &= 0xFFF
				else:
					self.V[0xF] = 0
			elif NN == 0x29:
				self.I = self.V[X] * 5
			elif NN == 0x33:
				number = self.V[X]
				H = number // 100
				T = (number // 10) % 10
				O = number % 10
				self.RAM[self.I] = H
				self.RAM[self.I + 1] = T
				self.RAM[self.I + 2] = O
			elif NN == 0x55:
				for i in range(X + 1):
					self.RAM[self.I + i] = self.V[i]
			elif NN == 0x65:
				for i in range(X + 1):
					# print(type(self.RAM[self.I + i]))
					self.V[i] = int(self.RAM[self.I + i])

	def draw_sprite(self, X, Y, N):
		self.V[0xF] = 0
		start_x = self.V[X] % DISPLAY_WIDTH
		start_y = self.V[Y] % DISPLAY_HEIGHT
		for i in range(N):
			# if Y + i >= 32:
			#     break
			number = self.RAM[self.I + i]
			byte = '{:08b}'.format(number)
			for j in range(8):
				# if X + j >= 64:
				#     break
				bit = byte[j]
				if bit == "0":
					continue
				row = (start_y + i) % DISPLAY_HEIGHT
				col = (start_x + j) % DISPLAY_WIDTH
				if self.Display[row][col] == 1:
					self.V[0xF] = 1
				self.Display[row][col] ^= 1
