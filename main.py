from vm import VM
from assembler import assemble

vm = VM()

program = """
addi 0 0
addi 1 2
addi 2 10
addi 3 0
cmp 2 3
jz 4
add 0 1
addi 2 -1
jmp -4
hlt
"""

bytecode = assemble(program)

for instruction in bytecode:
    vm.add_instruction(instruction[0], instruction[1], instruction[2])

vm.run()
