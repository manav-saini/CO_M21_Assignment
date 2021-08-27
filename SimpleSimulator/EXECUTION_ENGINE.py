import MEMORY as MEM
from TABLES import opcode_table

# reg1 = reg2 + reg3
def add(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[7:10]
	reg2_addr = instruction[10:13]
	reg3_addr = instruction[13:16]

	reg2 = MEM.getData(reg2_addr)
	reg3 = MEM.getData(reg3_addr)

	reg1 = reg2 + reg3

	MEM.setData(reg1_addr, reg1)


# reg1 = reg2 - reg3
def sub(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[7:10]
	reg2_addr = instruction[10:13]
	reg3_addr = instruction[13:16]

	reg2 = MEM.getData(reg2_addr)
	reg3 = MEM.getData(reg3_addr)

	reg1 = reg2 - reg3

	MEM.setData(reg1_addr, reg1)

# reg1 = imm
def mov_imm(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[5:8]
	imm = instruction[8:16]

	imm = int(imm, 2)
	
	MEM.setData(reg1_addr, imm)

# reg1 = reg2
def mov_reg(instruction):
	reg1_addr = instruction[10:13]
	reg2_addr = instruction[13:16]

	reg2 = MEM.getData(reg2_addr)
	
	# handling FLAGS
	if reg2_addr == "111":
		val = ""
		for i in reg2: 
			if i == 1:
				val = val + "1"
			else: 
				val = val + "0"
		reg2 = int(val, 2)

	MEM.resetFlags()
	MEM.setData(reg1_addr, reg2)


# reg1 = value(mem_addr)
def ld(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[5:8]
	mem_addr = instruction[8:16]

	val_mem = MEM.getData(mem_addr)

	MEM.setData(reg1_addr, val_mem)

# value(mem_addr) = reg1
def st(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[5:8]
	mem_addr = instruction[8:16]

	reg1 = MEM.getData(reg1_addr)

	MEM.setData(mem_addr, reg1)

# reg1 = reg2 * reg3
def mul(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[7:10]
	reg2_addr = instruction[10:13]
	reg3_addr = instruction[13:16]

	reg2 = MEM.getData(reg2_addr)
	reg3 = MEM.getData(reg3_addr)	

	reg1 = reg2*reg3
	MEM.setData(reg1_addr, reg1)


# reg1/reg2, R0 = quotient, R1 = remainder
def div(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[10:13]
	reg2_addr = instruction[13:16]

	reg1 = MEM.getData(reg1_addr)
	reg2 = MEM.getData(reg2_addr)

	quotient = int(reg1/reg2)
	remainder = reg1%reg2

	MEM.setData("000", quotient)
	MEM.setData("001", remainder)

# reg1 = reg1 >> imm
def rs(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[5:8]
	imm = instruction[8:16]

	imm = int(imm, 2)
	reg1 = MEM.getData(reg1_addr)

	reg1 = reg1 >> imm
	MEM.setData(reg1_addr, reg1)

# reg2 = reg2 << imm
def ls(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[5:8]
	imm = instruction[8:16]

	imm = int(imm, 2)
	reg1 = MEM.getData(reg1_addr)

	reg1 = reg1 << imm
	MEM.setData(reg1_addr, reg1)	

# reg1 = reg2 xor reg3
def XOR(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[7:10]
	reg2_addr = instruction[10:13]
	reg3_addr = instruction[13:16]

	reg2 = MEM.getData(reg2_addr)
	reg3 = MEM.getData(reg3_addr)

	reg1 = reg2^reg3
	MEM.setData(reg1_addr, reg1)

# reg1 = reg2 or reg3
def OR(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[7:10]
	reg2_addr = instruction[10:13]
	reg3_addr = instruction[13:16]

	reg2 = MEM.getData(reg2_addr)
	reg3 = MEM.getData(reg3_addr)

	reg1 = reg2|reg3
	MEM.setData(reg1_addr, reg1)


# reg1 = reg2 and reg3
def AND(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[7:10]
	reg2_addr = instruction[10:13]
	reg3_addr = instruction[13:16]

	reg2 = MEM.getData(reg2_addr)
	reg3 = MEM.getData(reg3_addr)

	reg1 = reg2&reg3
	MEM.setData(reg1_addr, reg1)


# reg1 = not reg2 (unsigned type)
def NOT(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[10:13]
	reg2_addr = instruction[13:16]

	reg2 = MEM.getData(reg2_addr)

	reg2 = bin(reg2)[2:]
	
	if len(reg2) < 16:
		no_of_zeroes = 16 - len(reg2)
		reg2 = no_of_zeroes*"0" + reg2
	
	for i in range(16):
		if reg2[i] == "1":
			reg2 = reg2[0:i] + "0" + reg2[i+1:]
		else:
			reg2 = reg2[0:i] + "1" + reg2[i+1:]
	
	reg2 = int(reg2, 2)
	
	MEM.setData(reg1_addr, reg2)

# compares reg1 and reg2 then sets appropriate FLAG
def cmp(instruction):
	MEM.resetFlags()
	reg1_addr = instruction[10:13]
	reg2_addr = instruction[13:16]

	reg1 = MEM.getData(reg1_addr)
	reg2 = MEM.getData(reg2_addr)

	if reg1 < reg2:
		MEM.setFlag("L")
	elif reg1 > reg2:
		MEM.setFlag("G")
	else: 
		MEM.setFlag("E")
	

# returns new PC address
def jmp(instruction):
	MEM.resetFlags()
	return int(instruction[8:16], 2)

# returns new PC address depending on the lessThan FLAG
def jlt(instruction):
	next_instruction = MEM.PC + 1
	FLAGS = MEM.getData("111")

	if FLAGS[1] == 1:
		next_instruction = int(instruction[8:16], 2)
	
	MEM.resetFlags()
	return next_instruction


# returns new PC address depending on the greaterThan FLAG
def jgt(instruction):
	next_instruction = MEM.PC + 1
	FLAGS = MEM.getData("111")

	if FLAGS[2] == 1:
		next_instruction = int(instruction[8:16], 2)
	
	MEM.resetFlags()
	return next_instruction


# returns new PC address depending on the equalTo FLAG
def je(instruction):
	next_instruction = MEM.PC + 1
	FLAGS = MEM.getData("111")

	if FLAGS[3] == 1:
		next_instruction = int(instruction[8:16], 2)
	
	MEM.resetFlags()
	return next_instruction



def execute(instruction):
	opcode = opcode_table[instruction[0:5]][0]
	halted = False 
	PC = MEM.PC + 1

	if opcode == "hlt":
		MEM.resetFlags()
		halted = True
	elif opcode == "add":
		add(instruction)
	elif opcode == "sub":
		sub(instruction)
	elif opcode == "mov_imm":
		mov_imm(instruction)
	elif opcode == "mov_reg":
		mov_reg(instruction)
	elif opcode == "ld":
		ld(instruction)
	elif opcode == "st":
		st(instruction)
	elif opcode == "mul":
		mul(instruction)
	elif opcode == "div":
		div(instruction)
	elif opcode == "rs":
		rs(instruction)
	elif opcode == "ls":
		ls(instruction)
	elif opcode == "xor":
		XOR(instruction)
	elif opcode == "or":
		OR(instruction)
	elif opcode == "and":
		AND(instruction)
	elif opcode == "not":
		NOT(instruction)
	elif opcode == "cmp":
		cmp(instruction)
	elif opcode == "jmp":
		PC = jmp(instruction)
	elif opcode == "jlt":
		PC = jlt(instruction)
	elif opcode == "jgt":
		PC = jgt(instruction)
	elif opcode == "je":
		PC = je(instruction)

	return (PC, halted)



