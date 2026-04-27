#include "bootcamp/hello-sim-object/hello_sim_object.hh"

#include <iostream>

#include "base/trace.hh"
#include "debug/HelloExampleFlag.hh"
#include "sim/eventq.hh"

namespace gem5
{
    // 构造函数：接收Python传递的所有参数（params包含num_hellos、goodbye_object）
    HelloSimObject::HelloSimObject(const HelloSimObjectParams& params):
    // 1. 初始化父类 SimObject（gem5 硬性要求）
    SimObject(params),
    // 2. 初始化剩余打印次数 = Python传入的 num_hellos（比如5）
    remainingHellosToPrintByEvent(params.num_hellos),
    // 3. 初始化事件对象：绑定要执行的函数 + 给事件命名
    nextHelloEvent([this](){ processNextHelloEvent(); }, name() + "nextHelloEvent"),
    // 4. 初始化指针：绑定Python传入的 GoodByeSimObject 对象
    goodByeObject(params.goodbye_object)
    {
        // 校验参数：如果num_hellos≤0，直接报错退出
        fatal_if(params.num_hellos <= 0, "num_hellos should be positive!");
        // 循环打印：构造函数里直接输出 Hello（无延时，一次性打完）
        for (int i = 0; i < params.num_hellos; i++) {
            std::cout << "i: " << i << ", Hello from HelloSimObject's constructor!" << std::endl;
        }
        // gem5 调试日志（只有开启调试开关时才打印）
        DPRINTF(HelloExampleFlag, "%s: Hello from HelloSimObject's constructor!\n", __func__);
    }

    void
    HelloSimObject::processNextHelloEvent()
    {
        std::cout << "tick: " << curTick() << ", Hello from HelloSimObject::processNextHelloEvent!" << std::endl;
        remainingHellosToPrintByEvent--;
        if (remainingHellosToPrintByEvent > 0) {
            schedule(nextHelloEvent, curTick() + 500);
        } 
        else {
            goodByeObject->sayGoodBye();
        }
    }

    void
    HelloSimObject::startup()
    {
        std::cout << "START_UP_HELLO" << std::endl;
        panic_if(curTick() != 0, "startup called at a tick other than 0");
        panic_if(nextHelloEvent.scheduled(), "nextHelloEvent is scheduled before HelloSimObject::startup is called!");
        schedule(nextHelloEvent, curTick() + 500);
    }
} // namespace gem5
