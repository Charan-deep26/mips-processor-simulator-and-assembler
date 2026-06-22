class MIPSProcessor:
    def __init__(self, binary_file):
        with open(binary_file, 'r') as f:
            self.imem = [line.strip() for line in f if line.strip()]
        self.regs = [0] * 32
        self.dmem = [0] * 256
        self.pc = 0
        self.cycle = 1
        self.used_regs = {0, 8, 9} 

        # CHANGED: Pre-load the data memory at address 4 with n=5 so LW has something to read
        self.dmem[4] = 5

    def run(self):
        while (self.pc >> 2) < len(self.imem):
            print(f"\n{'='*40}\nCYCLE {self.cycle} | PC: {self.pc}")
            
            instr = self.imem[self.pc >> 2]
            op = instr[0:6]
            rs = int(instr[6:11], 2)
            rt = int(instr[11:16], 2)
            rd = int(instr[16:21], 2)
            imm = int(instr[16:32], 2)
            if imm > 32767: imm -= 65536
            
            print(f"[IF]  Fetched Binary: {instr}")
            print(f"[ID]  Opcode: {op} | rs: R{rs} | rt: R{rt} | imm: {imm}")

            alu_res = 0
            next_pc = self.pc + 4
            
            if op == '001000':
                alu_res = self.regs[rs] + imm
                print(f"[EX]  ALU Add: R{rs}({self.regs[rs]}) + {imm} = {alu_res}")
            elif op == '011100':
                alu_res = self.regs[rs] * self.regs[rt]
                print(f"[EX]  ALU Multiply: R{rs}({self.regs[rs]}) * R{rt}({self.regs[rt]}) = {alu_res}")
            elif op == '000100':
                is_equal = (self.regs[rs] == self.regs[rt])
                if is_equal: next_pc = self.pc + 4 + (imm << 2)
                print(f"[EX]  Branch Check: R{rs}({self.regs[rs]}) == R{rt}({self.regs[rt]}) -> {is_equal}")
            elif op == '000010':
                next_pc = (int(instr[6:32], 2) << 2)
                print(f"[EX]  Jump Target Computed: {next_pc}")
            elif op in ['101011', '100011']: # CHANGED: SW and LW use same address calc
                alu_res = self.regs[rs] + imm
                print(f"[EX]  Address Calc: R{rs}({self.regs[rs]}) + {imm} = {alu_res}")

            mem_out = 0 # Added for LW
            if op == '101011':
                self.dmem[alu_res] = self.regs[rt]
                print(f"[MEM] Write: Mem[{alu_res}] = {self.regs[rt]}")
            elif op == '100011': # CHANGED: LW memory read
                mem_out = self.dmem[alu_res]
                print(f"[MEM] Read: Mem[{alu_res}] = {mem_out}")
            else:
                print(f"[MEM] No memory operation.")

            if op == '001000':
                self.regs[rt] = alu_res
                print(f"[WB]  Reg Write: R{rt} = {alu_res}")
            elif op == '011100':
                self.regs[rd] = alu_res
                print(f"[WB]  Reg Write: R{rd} = {alu_res}")
            elif op == '100011': # CHANGED: LW register write
                self.regs[rt] = mem_out
                print(f"[WB]  Reg Write: R{rt} = {mem_out}")
            else:
                print(f"[WB]  No register writeback.")

            self.regs[0] = 0 
            print("-" * 40)
            reg_map_rev = {0: '$zero', 8: '$t0', 9: '$t1'}
            used_str = " | ".join([f"{reg_map_rev.get(r, f'R{r}')}: {self.regs[r]}" for r in sorted(self.used_regs)])
            print(f"Register State: {used_str}")

            self.pc = next_pc
            self.cycle += 1
        
        print(f"\n{'='*40}\nSimulation Complete. Final Factorial Result in Mem[0]: {self.dmem[0]}")

if __name__ == "__main__":
    # CHANGED: Now points to your roll number file
    MIPSProcessor('BC2025032_binary.txt').run()