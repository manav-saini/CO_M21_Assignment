import MEMORY as MEM
import EXECUTION_ENGINE as EE 
import matplotlib.pyplot as plt

MEM.initialize()

halted = False
next_instruction = 0

while not halted:
	instruction = MEM.getIntruction(MEM.PC)
	
	next_instruction, halted =  EE.execute(instruction)

	MEM.printRF()

	MEM.PC = next_instruction
	MEM.cycle = MEM.cycle + 1



MEM.dump()

# Scatter plot 

plt.scatter(MEM.memory_access_cycle, MEM.memory_access)
plt.xlabel("Cycle")
plt.ylabel("Memory Address")
plt.savefig("scatter_plot.png", bbox_inches = "tight")
