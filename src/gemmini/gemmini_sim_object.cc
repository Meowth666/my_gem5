#include "gemmini/gemmini_sim_object.hh"
#include <iostream>
#include "base/trace.hh"
#include "debug/GemminiExampleFlag.hh"
#include "sim/eventq.hh"

namespace gem5
{
    GemminiSimObject::GemminiSimObject(const GemminiSimObjectParams& params): 
        SimObject(params),
        mode(0),
        relu(0),
        A_transpose(0),
        B_transpose(0),
        A_stride(1),     // 默认stride通常设为1
        scale(1.0f),     // 默认不缩放
        shift(0)         // 默认不shift
        {
            printf("-----------Gemmini initialized------------\n");
        }

    void
    GemminiSimObject::config_ex(uint64_t rs1, uint64_t rs2)
    {
        parseConfigEx(rs1, rs2);
        printConfig();
    }
    
    void 
    GemminiSimObject::parseConfigEx(uint64_t rs1, uint64_t rs2){
        // ===== 1. 解析 rs1 =====
        mode        = (rs1 >> 2) & 0x1;
        relu        = (rs1 >> 3) & 0x1;
        A_transpose = (rs1 >> 8) & 0x1;
        B_transpose = (rs1 >> 9) & 0x1;
        A_stride = (rs1 >> 16) & 0xFFFF;
        // ===== 2. 解析 scale（float32）=====
        uint32_t scale_bits = (rs1 >> 32) & 0xFFFFFFFF;
        std::memcpy(&scale, &scale_bits, sizeof(float));
        // ===== 3. 解析 rs2 =====
        shift = rs2 & 0xFFFFFFFF;
    }

    void 
    GemminiSimObject::printConfig(){
        DPRINTF(GemminiExampleFlag, "=== config_ex ===\n");
        DPRINTF(GemminiExampleFlag, "mode            = %d (%s-stationary)\n",
                mode, mode ? "weight" : "output");
        DPRINTF(GemminiExampleFlag, "relu            = %d\n", relu);
        DPRINTF(GemminiExampleFlag, "A_transpose     = %d\n", A_transpose);
        DPRINTF(GemminiExampleFlag, "B_transpose     = %d\n", B_transpose);
        DPRINTF(GemminiExampleFlag, "A_stride        = %d\n", A_stride);
        DPRINTF(GemminiExampleFlag, "scale           = %f\n", scale);
        DPRINTF(GemminiExampleFlag, "shift           = %u\n", shift);
    }

} // namespace gem5


