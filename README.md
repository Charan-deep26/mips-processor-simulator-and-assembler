# MIPS Processor Simulator and Assembler

A Python-based implementation of a custom two-pass assembler and a 5-stage non-pipelined MIPS processor simulator. The project translates MIPS assembly programs into 32-bit machine code and simulates their execution through the Instruction Fetch (IF), Instruction Decode (ID), Execute (EX), Memory Access (MEM), and Write Back (WB) stages.

## Overview

This project demonstrates fundamental computer architecture concepts by implementing both an assembler and a processor simulator for a subset of the MIPS instruction set architecture (ISA).

The assembler converts MIPS assembly programs into machine code, while the simulator executes the generated instructions cycle-by-cycle, displaying the internal state of the processor during execution.

## Features

- Custom Two-Pass Assembler
  - Automatic label resolution
  - Branch offset calculation
  - Jump address generation

- MIPS Processor Simulator
  - 5-stage non-pipelined execution model
  - Cycle-by-cycle execution tracing
  - Register file simulation
  - Instruction and data memory simulation

- Supported Instructions
  - `addi`
  - `lw`
  - `sw`
  - `beq`
  - `j`
  - `mul`

## Architecture

The processor simulates the following stages:

1. Instruction Fetch (IF)
2. Instruction Decode (ID)
3. Execute (EX)
4. Memory Access (MEM)
5. Write Back (WB)

The simulator maintains:

- 32 General Purpose Registers
- Program Counter (PC)
- Instruction Memory
- Data Memory
- Register Zero ($zero) hardwired to 0

## Project Structure

```text
.
├── assembler.py
├── mips.py
├── assembly.txt
├── binary.txt
├── report.pdf
└── README.md
```

## Example Program

The included assembly program computes the factorial of a number using a loop.

```assembly
lw $t0, 4($zero)
addi $t1, $zero, 1

LOOP:
beq $t0, $zero, DONE
mul $t1, $t1, $t0
addi $t0, $t0, -1
j LOOP

DONE:
sw $t1, 0($zero)
```

For `n = 5`, the simulator stores:

```text
120
```

in Data Memory location `0`.

## How to Run

### Assemble the Program

```bash
python assembler.py
```

This generates:

```text
binary.txt
```

### Run the Simulator

```bash
python mips.py
```

The simulator displays:

- Current cycle number
- Program Counter (PC)
- Instruction being executed
- Actions performed in each stage
- Register values after execution

## Sample Output

```text
Simulation Complete.
Final Factorial Result in Mem[0]: 120
```

## Concepts Demonstrated

- Computer Architecture
- MIPS Instruction Set Architecture
- Two-Pass Assembly
- Branch and Jump Address Resolution
- Instruction Execution Pipeline Stages
- Register File Design
- Memory Organization
- Binary Instruction Encoding

## Technologies Used

- Python
- MIPS Assembly Language
- Computer Architecture

## Author

Charan Deep
