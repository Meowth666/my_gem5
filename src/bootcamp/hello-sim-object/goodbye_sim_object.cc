#include "bootcamp/hello-sim-object/goodbye_sim_object.hh"
#include <iostream>
#include "base/trace.hh"
#include "debug/GoodByeExampleFlag.hh"
#include "sim/eventq.hh"

namespace gem5
{
    GoodByeSimObject::GoodByeSimObject(const GoodByeSimObjectParams& params):
        SimObject(params),
        nextGoodByeEvent([this]() { processNextGoodByeEvent(); }, name() + "nextGoodByeEvent" )
    {}

    void
    GoodByeSimObject::sayGoodBye() {
        panic_if(nextGoodByeEvent.scheduled(), "GoodByeSimObject::sayGoodBye called while nextGoodByeEvent is scheduled!");
        schedule(nextGoodByeEvent, curTick() + 500);
    }

    void
    GoodByeSimObject::processNextGoodByeEvent()
    {
        DPRINTF(GoodByeExampleFlag, "%s: GoodBye from GoodByeSimObejct::processNextGoodByeEvent!\n", __func__);
    }

    void
    GoodByeSimObject::startup()
    {
        std::cout << "START_UP_GOODBYE" << std::endl;
        panic_if(curTick() != 0, "startup called at a tick other than 0");
        schedule(nextGoodByeEvent, curTick() + 500);
    }
} // namespace gem5
