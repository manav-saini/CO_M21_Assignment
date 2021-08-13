import sys
from sys import stdin

complete_input = sys.stdin.read()
registers = {"R0": "000", "R1": "001", "R2": "010", "R3": "011", "R4": "100", "R5": "101", "R6": "110", "FLAGS": "111"}
opcode = {"add": "00000", "sub": "00001", "mov_imm": "00010", "mov_reg": "00011", "ld": "00100", "st": "00101",
          "mul": "00110", "div": "00111", "rs": "01000", "ls": "01001", "xor": "01010", "or": "01011", "and": "01100",
          "not": "01101", "cmp": "01110", "jmp": "01111", "jlt": "10000", "jgt": "10001", "je": "10010", "hlt": "10011"}


def check(instruction, arr):
    if instruction == "add" and len(arr) == 4 and arr[1] in registers and arr[2] in registers and arr[3] in registers:
        return True
    elif instruction == "sub" and len(arr) == 4 and arr[1] in registers and arr[2] in registers and arr[3] in registers:
        return True
    elif instruction == "mov" and len(arr) == 3 and arr[1] in registers:
        if arr[2] in registers:
            return True
        else:  # checking the syntax for immediate
            dollar = 0
            num = 0
            for i in arr[2]:
                if i == "$":
                    dollar = 1
                elif isinstance(i, int):  # checking whether dollar sign follows integer values or not
                    num += 1
            if dollar == 1 and num == len(arr[2]) - 1:
                return True
            else:
                return False
    elif instruction == "mul" and len(arr) == 4 and arr[1] in registers and arr[2] in registers and arr[3] in registers:
        return True
    elif instruction == "div" and len(arr) == 3 and arr[1] in registers and arr[2] in registers:
        return True
    elif instruction == "xor" and len(arr) == 4 and arr[1] in registers and arr[2] in registers and arr[3] in registers:
        return True
    elif instruction == "or" and len(arr) == 4 and arr[1] in registers and arr[2] in registers and arr[3] in registers:
        return True
    elif instruction == "and" and len(arr) == 4 and arr[1] in registers and arr[2] in registers and arr[3] in registers:
        return True
    elif instruction == "not" and len(arr) == 3 and arr[1] in registers and arr[2] in registers:
        return True
    elif instruction == "cmp" and len(arr) == 3 and arr[1] in registers and arr[2] in registers:
        return True


for line in stdin:
    line_array = line.split()
    if line == "":
        continue
    elif line_array[0] == "add" and check("add", line_array):
        print()
