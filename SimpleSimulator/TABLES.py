# instruction name: (opcode, type)
opcode_table = {
	"00000": ("add", "A"), 
	"00001": ("sub", "A"), 
	"00010": ("mov_imm", "B"), 
	"00011": ("mov_reg", "C"),  
	"00100": ("ld", "D"), 
	"00101": ("st", "D"),
	"00110": ("mul", "A"), 
	"00111": ("div", "C"), 
	"01000": ("rs", "B"), 
	"01001": ("ls", "B"), 
	"01010": ("xor", "A"), 
	"01011": ("or", "A"), 
	"01100": ("and", "A"),
	"01101": ("not", "C"), 
	"01110": ("cmp", "C"), 
	"01111": ("jmp", "E"), 
	"10000": ("jlt", "E"), 
	"10001": ("jgt", "E"), 
	"10010": ("je", "E"), 
	"10011": ("hlt", "F")
	}

# # type name: (no. of operands, no. of unused bytes, type of operand1, type of operand2 ....)
# type_table = {
# 	"A": (3, 2, "reg", "reg", "reg"),
# 	"B": (2, 0, "reg", "imm"),
# 	"C": (2, 5, "reg", "reg"),
# 	"D": (2, 0, "reg", "mem_addr_var"),
# 	"E": (1, 3, "mem_addr_label"),
# 	"F": (0, 11)
# }