#ifndef __GEMMINI_GEMMINI_SIM_OBJECT_HH__
#define __GEMMINI_GEMMINI_SIM_OBJECT_HH__

#include "params/GemminiSimObject.hh"
#include "sim/eventq.hh"
#include "sim/sim_object.hh"

namespace gem5
{

class GemminiSimObject : public SimObject
{
  private:
    // ====== 内部状态（先做最小版本） ======
    
    // config_ex 相关参数
    bool mode;            // rs1[2]
    bool relu;            // rs1[3]
    bool A_transpose;     // rs1[8]
    bool B_transpose;     // rs1[9]

    uint16_t A_stride;    // rs1[31:16]
    float scale;          // rs1[63:32]
    uint32_t shift;       // rs2[31:0]

  public:
    // ====== 构造函数 ======
    GemminiSimObject(const GemminiSimObjectParams &params);
    // ====== 对外接口（给 ISA 调用） ======
    void config_ex(uint64_t rs1, uint64_t rs2);

  private:
    // ====== 内部工具函数 ======
    void parseConfigEx(uint64_t rs1, uint64_t rs2);
    void printConfig();
};

} // namespace gem5

#endif // __GEMMINI_GEMMINI_SIM_OBJECT_HH__