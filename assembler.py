import re

OPCODES = {'addi': '001000', 'beq': '000100', 'j': '000010', 'sw': '101011', 'lw': '100011', 'mul': '011100'}
REG_MAP = {'zero': 0, 't0': 8, 't1': 9}
REG = {f'${k}': format(v, '05b') for k, v in REG_MAP.items()}

def assemble():
    # CHANGED: Now points to your roll number file
    with open('BC2025032_assembly.txt', 'r') as f:
        lines = [line.split('#')[0].strip() for line in f]
    
    labels = {}
    instructions = []
    addr = 0
    for line in lines:
        if not line: continue
        if line.endswith(':'):
            labels[line[:-1]] = addr
        else:
            instructions.append((addr, line.replace(',', '')))
            addr += 4

    machine_code = []
    for pc, line in instructions:
        parts = line.split()
        cmd = parts[0]
        
        if cmd == 'addi':
            imm = int(parts[3]) & 0xFFFF
            binary = OPCODES[cmd] + REG[parts[2]] + REG[parts[1]] + format(imm, '016b')
        elif cmd == 'mul':
            binary = OPCODES[cmd] + REG[parts[2]] + REG[parts[3]] + REG[parts[1]] + "00000" + "000010"
        elif cmd == 'beq':
            target = labels[parts[3]]
            offset = ((target - (pc + 4)) // 4) & 0xFFFF
            binary = OPCODES[cmd] + REG[parts[1]] + REG[parts[2]] + format(offset, '016b')
        elif cmd == 'j':
            target = labels[parts[1]]
            binary = OPCODES[cmd] + format(target // 4, '026b')
        elif cmd in ['sw', 'lw']: # CHANGED: Added LW logic
            rt = parts[1]
            match = re.match(r'(-?\d+)\((\$\w+)\)', parts[2])
            imm, rs = int(match.group(1)) & 0xFFFF, match.group(2)
            binary = OPCODES[cmd] + REG[rs] + REG[rt] + format(imm, '016b')
        
        machine_code.append(binary)

    # CHANGED: Now outputs to your roll number file
    with open('BC2025032_binary.txt', 'w') as f:
        f.write('\n'.join(machine_code))
    print("Assembler: BC2025032_binary.txt generated successfully.")

if __name__ == "__main__":
    assemble()