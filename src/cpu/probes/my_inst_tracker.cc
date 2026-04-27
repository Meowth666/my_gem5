#include "cpu/probes/my_inst_tracker.hh"

namespace gem5{

    MyGlobalInstTracker::MyGlobalInstTracker(const MyGlobalInstTrackerParams &params):
        SimObject(params),
        instCount(0),
        instThreshold(params.inst_threshold)
    {}

    void
    MyGlobalInstTracker::checkPc(const uint64_t& inst)
    {
        instCount ++;
        if (instCount >= instThreshold) {
            exitSimLoopNow("a thread reached the max instruction count");
        }
    }

    MyLocalInstTracker::MyLocalInstTracker(const MyLocalInstTrackerParams &params):
        ProbeListenerObject(params),
        globalInstTracker(params.global_inst_tracker),
        listening(params.start_listening)
    {}

    void
    MyLocalInstTracker::regProbeListeners(){
        if (listening) {
            if (listeners.empty()) {
                connectListener<MyLocalInstTrackerListener>(
                    this, "RetiredInsts", &MyLocalInstTracker::checkPc);
                DPRINTF(InstTracker, "Start listening to RetiredInsts\n");
            }
        }
    }

    void
    MyLocalInstTracker::checkPc(const uint64_t& inst)
    {
        globalInstTracker->checkPc(inst);
    }
}