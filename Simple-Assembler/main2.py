import sys

# address: 0 based indexing, error generation: 1 based indexing

program = [] # input assembly program
bin_program = [] # output binary code
address_table = {} # address of vars and labels. {name: (address, isVariable)}

location_counter = 0 # reset in every pass
instruction_location = 0
last_valid_instruction_count = 0



# assumes error free code 
# finds address of vars and labels. Checks vars declaration location
def pass1():
	global program 
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
				exit
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
				# TODO: check for valid label name 
				address_table[operands[0][0:-1]] = (noOfInstructions, False)
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
			if line[0][-1] == ":" and line[0:-1] in address_table:
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
			address_table[operands[1]] = (noOfInstructions, True)
		else:
			break







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
	








main()
