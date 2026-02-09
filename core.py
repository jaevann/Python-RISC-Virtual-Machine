class VM:
    def __init__(self, register_count=10):
        self.REGISTER_COUNT = register_count
        self.instructions = []
        self.registers = []
        self.negative_flag = False
        self.zero_flag = True
        self.init_registers()
        # NOTE: instruction register is always the last register

    def init_registers(self):
        for _ in range(self.REGISTER_COUNT):
            self.registers.append(0)

    def add_instruction(self, operand, b, c):
        self.instructions.append([operand, b, c])

    def set_flags(self, result):
        self.negative_flag = result < 0
        self.zero_flag = result == 0

    def check_write_permission(self, register_list):
        for register in register_list:
            if register == len(self.registers)-1:
                raise Exception("Write was attempted on the Instruction Pointer")

    def core_dump(self):
        print("\nRegisters:")
        for i, register in enumerate(self.registers):
            name = f"r{i}" if i < len(self.registers) - 1 else "rip"
            print(f"{name:3} | {register}")

        print(f"\nFlags:\nNegative Flag | {self.negative_flag}\nZero Flag     | {self.zero_flag}")
        print("\nInstructions:")
        ip = self.registers[-1]
        for i, instruction in enumerate(self.instructions):
            pointer = ">" if ip == i else "." if ip > i else " "
            print(f"{pointer} {i} | {instruction}")

    def step(self):
        ip = len(self.registers)-1
        instruction = self.instructions[self.registers[ip]]
        opcode, a, b = instruction

        match opcode:
            case 0:
                #add a b
                self.check_write_permission([a, b])
                self.registers[a] += self.registers[b]
                self.set_flags(self.registers[a])
            case 1:
                #addi a b
                self.check_write_permission([a])
                self.registers[a] += b
                self.set_flags(self.registers[a])
            case 2:
                # cmp a b
                self.check_write_permission([a, b])
                self.set_flags(self.registers[a]-self.registers[b])
            case 3:
                # jump (0->j, 1->jz, 2->jnz, 3->jlt, 4->jge) dest_offset
                if a == 0:
                    self.registers[ip] += b-1
                elif a == 1 and self.zero_flag:
                    self.registers[ip] += b-1
                elif a == 2 and not self.zero_flag:
                    self.registers[ip] += b-1
                elif a == 3 and self.negative_flag:
                    self.registers[ip] += b-1
                elif a == 4 and not self.negative_flag:
                    self.registers[ip] += b-1
            case 4:
                return 1

        self.registers[ip] += 1
        return 0

    def run(self, step_mode=True):
        while True:
            if step_mode:
                self.core_dump()
                input(">>")
            if self.step() == 1:
                break
