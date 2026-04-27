#include <stdio.h>
#include <stdint.h>

int main() {
    uint64_t rs1 = 0;
    uint64_t rs2 = 0;
    uint64_t output = 0;
    // Set some test values
    // rs1 bits:
    //   [2] mode = 1
    //   [3] relu = 0
    //   [8] A_transpose = 1
    //   [9] B_transpose = 0
    //   [31:16] A_stride = 16
    //   [63:32] scale = 1.0f (float bits)
    // rs2 bits:
    //   [31:0] shift = 4

    rs1 = (1 << 2) | (1 << 8);  // mode=1, A_transpose=1
    rs1 |= (16 << 16);          // A_stride=16

    // Set scale = 1.0f (0x3f800000)
    uint32_t scale_bits = 0x3f800000;
    rs1 |= ((uint64_t)scale_bits << 32);

    rs2 = 4;  // shift=4

    printf("Testing config_ex instruction...\n");
    printf("rs1 = 0x%016lx\n", rs1);
    printf("rs2 = 0x%016lx\n", rs2);

    // Execute config_ex instruction
    // .insn r 0x0B, 0x0, 0x00, x0, %0, %1
    // 直接内联自定义指令机器码
    asm volatile(
        ".insn r 0x0f, 0x3, 0x00, x0, %0, %1"
        :
        : "r"(rs1), "r"(rs2)  // 输入：rs1, rs2
        :
    );

    printf("Instruction executed.\n");
    return 0;
}