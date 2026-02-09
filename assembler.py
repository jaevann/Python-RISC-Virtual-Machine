
# 0 -> normal instruction
# 1 -> jmp instruction
# 2 -> 0 operand instruction
instructions = {
    "add" : [0, 0],
    "addi" : [1, 0],
    "cmp" : [2, 0],
    "jmp" : [3, 1, 0],
    "jz" : [3, 1, 1],
    "jnz" : [3, 1, 2],
    "jlt" : [3, 1, 3],
    "jge" : [3, 1, 4],
    "hlt" : [4, 2]
}

def parse_operand(token: str) -> int:
    try:
        return int(token)
    except ValueError:
        raise Exception(f"Invalid operand {token}")

def is_label(tokens):
	return tokens[0].endswith(":")

def assemble(src: str) -> list[list[int]]:
    lines = src.split("\n")
    program = []
    for line in lines:
        line = line.strip()
        if not line:
            continue

        tokens = line.split()
        instruction = tokens[0]

        if not instruction in instructions:
            raise Exception(f"Invalid instruction {instruction}")
        
        info = instructions[instruction]
        opcode = info[0]
        kind = info[1]

        tokenized_line = [opcode]

        if kind == 0:
            if len(tokens) != 3:
                raise Exception(f"{instruction} expects 2 operands")
            tokenized_line.append(parse_operand(tokens[1]))
            tokenized_line.append(parse_operand(tokens[2]))

        elif kind == 1:
            if len(tokens) != 2:
                raise Exception(f"{instruction} expects 1 operand")
            jmp_type = info[2]
            tokenized_line.append(jmp_type)
            tokenized_line.append(parse_operand(tokens[1]))

        elif kind == 2:
            tokenized_line.append(0)
            tokenized_line.append(0)
        
        program.append(tokenized_line)

    return program
