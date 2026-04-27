#ifndef __BOOTCAMP_HELLO_SIM_OBJECT_HELLO_SIM_OBJECT_HH__
#define __BOOTCAMP_HELLO_SIM_OBJECT_HELLO_SIM_OBJECT_HH__

#include "bootcamp/hello-sim-object/goodbye_sim_object.hh"
#include "params/HelloSimObject.hh"
#include "sim/sim_object.hh"
#include "sim/eventq.hh"

namespace gem5
{

class HelloSimObject: public SimObject
{
  private:
    // 剩余需要打印的Hello次数（对应Python的num_hellos参数）
    int remainingHellosToPrintByEvent;
    // gem5事件包装器：用来调度「打印Hello」的事件
    EventFunctionWrapper nextHelloEvent;
    // 事件处理函数：真正执行「打印一次Hello」的逻辑
    void processNextHelloEvent();
    // 指针：持有GoodByeSimObject的引用（对应Python的goodbye_object参数）
    GoodByeSimObject* goodByeObject;
  public:
    // 构造函数：接收Python传过来的所有参数
    HelloSimObject(const HelloSimObjectParams& params);
    // 重写SimObject的startup函数：gem5模拟启动时自动调用
    virtual void startup() override;
};

} // namespace gem5

#endif // __BOOTCAMP_HELLO_SIM_OBJECT_HELLO_SIM_OBJECT_HH__
