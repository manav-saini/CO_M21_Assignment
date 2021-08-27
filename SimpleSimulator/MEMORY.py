import sys

register = [0, 0, 0, 0, 0, 0, 0, [0, 0, 0, 0]] # R0-R6 + FLAGS(V,L,G,E), 16 bit each 
program = [] # input binary program 
variables = [] # variables stored as ints 
no_of_instructions = 0 # len(program)
cycle = 0 # tracks cycle no for the bonus qs
memory_access = [] # tracks memory access for bonus qs
memory_access_cycle = [] # tracks corresponding cycle no. for bonus qs
PC = 0 # program counter 


# initializes the memory
def initialize(): 
	global program
	global no_of_instructions
	global PC
	global variables

	for line in sys.stdin:
		if len(line.split()) == 0:
			continue
		program.append(line)

	no_of_instructions = len(program)

	for i in range(256 - no_of_instructions):
		variables.append(0)
	
	PC = 0
	

def to16Bit(value):
	value = bin(value)[2:]

	if len(value) < 16:
		no_of_zeroes = 16 - len(value)
		value = no_of_zeroes*"0" + value

	return value


def to8Bit(value):
	value = bin(value)[2:]

	if len(value) < 8:
		no_of_zeroes = 8 - len(value)
		value = no_of_zeroes*"0" + value

	return value


	

# resets Flags
def resetFlags():
	global register
	for i in range(4):
		register[7][i] = 0


def setFlag(flag_type):
	global register

	if flag_type == "V":
		register[7][0] = 1
	elif flag_type == "L":
		register[7][1] = 1
	elif flag_type == "G":
		register[7][2] = 1
	elif flag_type == "E":
		register[7][3] = 1
	else: 
		print("Invalid flag type")
		exit()


# return value stored in mem_addr from regster of variable
def getData(mem_addr):
	global memory_access_cycle 
	global memory_access
	if len(mem_addr) == 3:
		return register[int(mem_addr, 2)]
	else:
		memory_access.append(int(mem_addr, 2))
		memory_access_cycle.append(cycle)
		return variables[int(mem_addr, 2) - no_of_instructions]


def getIntruction(mem_addr):
	global memory_access_cycle
	global memory_access

	memory_access.append(mem_addr)
	memory_access_cycle.append(cycle)

	return program[mem_addr]

# set instruction for everything except the FLAGS
def setData(mem_addr, value):
	global memory_access
	global memory_access_cycle
	global register 
	global variables

	if value < 0:
		value = 0
		setFlag("V")
	
	value = bin(value)[2:]

	if len(value) > 16:
		value = value[-16:]
		setFlag("V")

	value = int(value, 2)

	if len(mem_addr) == 3: 
		register[int(mem_addr, 2)] = value
	elif len(mem_addr) == 8:
		variables[int(mem_addr, 2) - no_of_instructions] = value
		memory_access.append(int(mem_addr, 2))
		memory_access_cycle.append(cycle)
	

	
	


def printRF():
	print(to8Bit(PC), end=" ")
	for i in range(7):
		print(to16Bit(register[i]), end = " ")
	
	FLAGS = ""

	for i in register[7]:
		if i == 1:
			FLAGS = FLAGS + "1"
		else:
			FLAGS = FLAGS + "0"
	
	FLAGS = 12*"0" + FLAGS

	print(FLAGS)


def dump():
	for i in program:
		print(i, end = "")
	
	if program[len(program)-1][-1] != '\n':
		print()
	
	for i in variables:
		print(to16Bit(i))