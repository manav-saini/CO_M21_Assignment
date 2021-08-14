import sys
from TABLES import opcode_table
from TABLES import type_table

# address: 0 based indexing, error generation: 1 based indexing

program = [] # input assembly program
bin_program = [] # output binary code
address_table = {} # address of vars and labels. {name: (address, isVariable)}
registers = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}


# location_counter = 0  reset in every pass
instruction_location = 0 # reset in every pass
last_valid_instruction_count = 0

# checks if immediate is a valid immediate
def validImmediate(immediate):
	if len(immediate) == 0:
		return False
	if immediate[0] != "$":
		return False

	if not immediate[1:].isdecimal():
		return False


	if int(immediate[1:]) > 255 or int(immediate[1:]) < 0:
		return False
	
	return True


		
# checks if it is a valid laber or var address
def validMemoryAddress(memory_address, isVariable):
	if memory_address in address_table:
		if isVariable == address_table[memory_address][1]:
			return True
	return False

# checks if it is a valid register name and wheter it can be FLAGS
def validRegister(name, canBeFlags):
	if name in registers:
		if name == "FLAGS":
			if canBeFlags: 
				return True	
			else:
				return False
		return True
	return False


# converts decimal address val to 8 bit adress string
def memoryLocation(int_address):
	address = bin(int_address)[2:]
	if len(address) < 8:
		i = 8 - len(address)
		address = i*"0" + address
	
	return address


# checks the naming syntax of label or var
def validLabelVar(name):
	name = "asd"
	if name in address_table:
		print(f"Declaration of {name} already exists. Error on line: {instruction_location}")
		exit()

	for i in name:
		if i.isalnum or i == "_":
			continue
		else:
			return False
	
	return True
	


# assumes error free code 
# finds address of vars and labels. Checks vars declaration location#
# handles hlt declarations
def pass1():
	program 
	global address_table
	global instruction_location
	global last_valid_instruction_count 

	instruction_location = 0
	isValidVar = True
	noOfInstructions = 0

	for line in program:
		instruction_location = instruction_location + 1
		operands = line.split()
		if len(operands) == 0:
			continue
		last_valid_instruction_count = instruction_location
		if operands[0] == "var":
			if len(operands) != 2:
				print(f"Invalid declaration syntax of var on line: {instruction_location}")
				exit()
			if not isValidVar:
				print(f"Invalid declaration of var on line: {instruction_location}")
				exit()
		else: 
			isValidVar = False
			# label check
			if(operands[0][-1] == ":"):
				if len(operands) == 1:
					print(f"No instruction after label declaration on line: {instruction_location}") 
					exit()
				# DONE: check for valid label name 
				if validLabelVar(operands[0][0:-1]):
					address_table[operands[0][0:-1]] = (memoryLocation(noOfInstructions), False)
			noOfInstructions = noOfInstructions + 1
	
	# hlt handling
	hlt_operand = program[last_valid_instruction_count - 1].split()
	if len(hlt_operand) != 1 and len(hlt_operand) != 2:
		print(f"No hlt statement at end of program")
		exit()
	if len(hlt_operand) == 1:
		if hlt_operand[0] != "hlt":
			print(f"No hlt statement at end of program")
			exit()
	elif hlt_operand[0][-1] == ":" and hlt_operand[0][0:-1] in address_table:
		if hlt_operand[1] != "hlt":
			print("No hlt statement at end of program")
			exit()
	else: 
		print("No hlt statement at end of program")
		exit()

	instruction_location = 0

	for i in range(last_valid_instruction_count-1):
		instruction_location = instruction_location + 1
		line = program[i].split()
		if len(line) == 0:
			continue

		if len(line) == 1:
			if line[0] == "hlt":
				print(f"Invalid declaration of hlt on line {instruction_location}")
				exit()
		if len(line) == 2: 
			if line[0][-1] == ":" and line[0][0:-1] in address_table:
				if line[1] == "hlt":
					print(f"Invalid declaration of hlt on line {instruction_location}")
					exit()
	
	
	# storing var address 

	instruction_location = 0 

	for line in program: 
		instruction_location = instruction_location + 1
		operands = line.split()
		if len(operands) == 0:
			continue

		if operands[0] == "var":
			if validLabelVar(operands[1]):
				address_table[operands[1]] = (memoryLocation(noOfInstructions), True)
		else:
			break
		noOfInstructions = noOfInstructions + 1
	
	# for i in address_table:
	# 	print(i, end= " ")
	# 	print(address_table[i])
	# print("passed Pass1")



# validates mov instruction of both types B & C
def checkMov(instruction):

	if len(instruction) != 3:
		print(f"Wrong instruction syntax on line: {instruction_location}")
		exit()
	
	if not validRegister(instruction[1], False):
		print(f"Invalid register on line: {instruction_location}")
		exit()

	validSecondOperand = False
	if validRegister(instruction[2], True):
		validSecondOperand = True
	elif validImmediate(instruction[2]):
		validSecondOperand = True
	
	if not validSecondOperand:
		print(f"No immediate or register in the second operand of mov instruction on line: {instruction_location}")
		exit()


def buildMovBinary(operands):
	binary_instruction = ""

	# unused bits and opcode 
	if validRegister(operands[2], True):
		binary_instruction = binary_instruction + opcode_table["mov"][1][0]
		binary_instruction = binary_instruction + 5*"0"
	else:
		binary_instruction = binary_instruction + opcode_table["mov"][0][0]
	
	# 1st register
	binary_instruction = binary_instruction + registers[operands[1]]

	if validRegister(operands[2], True):
		binary_instruction = binary_instruction + registers[operands[2]]
	else:
		immediate = int(operands[2][1:])
		immediate = bin(immediate)[2:]
		if len(immediate) < 8:
			no_of_zeroes = 8 - len(immediate)
			immediate = no_of_zeroes*"0" + immediate
		binary_instruction = binary_instruction + immediate
	
	return binary_instruction



def buildBinary(operands):
	binary_instruction = ""
	instruction_type = opcode_table[operands[0]][1]
	if instruction_type == "F":
		binary_instruction = opcode_table[operands[0]][0] + 11*"0"
		return binary_instruction
	# opcode
	binary_instruction = binary_instruction + opcode_table[operands[0]][0]

	# unused bits
	binary_instruction = binary_instruction + type_table[instruction_type][1]*"0"

	#operands

	for i in range(type_table[instruction_type][0]):
		j = i + 2
		if type_table[instruction_type][j] == "reg":
			binary_instruction = binary_instruction + registers[operands[1+i]]
		elif type_table[instruction_type][j] == "imm":
			immediate = int(operands[i+1][1:])
			immediate = bin(immediate)[2:]
			if len(immediate) < 8:
				no_of_zeroes = 8 - len(immediate)
				immediate = no_of_zeroes*"0" + immediate
			binary_instruction = binary_instruction + immediate
		else:
			binary_instruction = binary_instruction + address_table[operands[i+1]][0]


	return binary_instruction



# validates every instruction type except for mov instruction
def check(instruction):
	instruction_type = opcode_table[instruction[0]][1]

	if len(instruction[1:]) != type_table[instruction_type][0]:
		print(f"Wrong instruction syntax on line: {instruction_location}")
		exit()

	for i in range(type_table[instruction_type][0]):
		j = i + 2

		if type_table[instruction_type][j] == "reg":
			if not validRegister(instruction[i+1], False):
				print(f"Invalid register name on line: {instruction_location}")
				exit()
		elif type_table[instruction_type][j] == "imm":
			if not validImmediate(instruction[i+1]):
				print(f"Invalid immediate on line: {instruction_location}")
				exit()
		elif type_table[instruction_type][j] == "mem_addr_var":
			if not validMemoryAddress(instruction[i+1], True):
				print(f"Invalid variable address on line: {instruction_location}")
				exit()
		else: # label adrress
			if not validMemoryAddress(instruction[i+1], False):
				print(f"Invalid label address on line: {instruction_location}")
				exit()
	



# handles opcode validation for each instruction and 
# calls the relevant check fn for each type of instruction

def pass2():
	global instruction_location
	global bin_program

	instruction_location = 0
	
	for line in program:
		instruction_location = instruction_location + 1
		operands = line.split()

		if len(operands) == 0:
			continue

		if operands[0] == "var":
			continue

		if operands[0][-1] == ":":
			if operands[1] in opcode_table:
				if operands[1] != "mov":
					check(operands[1:])
					bin_program.append(buildBinary(operands[1:]))
				else: # mov instruction
					checkMov(operands[1:])
					bin_program.append(buildMovBinary(operands[1:]))
			else:
				print(f"Invalid instruction name on line: {instruction_location}")
				exit()
		else:
			if operands[0] in opcode_table:
				if operands[0] != "mov":
					check(operands)
					bin_program.append(buildBinary(operands))
				else: # mov instruction
					checkMov(operands)
					bin_program.append(buildMovBinary(operands))
			else:
				print(f"Invalid instruction name on line: {instruction_location}")
				exit()	



# reads input
def loadProgram():
	global program
	for line in sys.stdin:
		program.append(line)


def main():
	global program 
	loadProgram()
	# check if program is empty
	isEmpty = True
	for line in program:
		if len(line.split()) > 0:
			isEmpty = False
			break
	

	if isEmpty:
		exit()

	pass1()
	pass2()

	for line in bin_program:
		print(line, end = "\n")







main()
