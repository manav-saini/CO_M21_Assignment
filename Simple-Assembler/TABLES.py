# instruction name: (opcode, type)
opcode_table = {
	"add": ("00000", "A"), 
	"sub": ("00001", "A"), 
	"mov": (("00010", "B"), ("00011", "C")),  
	"ld": ("00100", "D"), 
	"st": ("00101", "D"),
	"mul": ("00110", "A"), 
	"div": ("00111", "C"), 
	"rs": ("01000", "B"), 
	"ls": ("01001", "B"), 
	"xor": ("01010", "A"), 
	"or": ("01011", "A"), 
	"and": ("01100", "A"),
	"not": ("01101", "C"), 
	"cmp": ("01110", "C"), 
	"jmp": ("01111", "E"), 
	"jlt": ("10000", "E"), 
	"jgt": ("10001", "E"), 
	"je": ("10010", "E"), 
	"hlt": ("10011", "F")
	}

# type name: (no. of operands, no. of unused bytes, type of operand1, type of operand2 ....)
type_table = {
	"A": (3, 2, "reg", "reg", "reg"),
	"B": (2, 0, "reg", "imm"),
	"C": (2, 5, "reg", "reg"),
	"D": (2, 0, "reg", "mem_addr_var"),
	"E": (1, 3, "mem_addr_label"),
	"F": (0, 11)
}