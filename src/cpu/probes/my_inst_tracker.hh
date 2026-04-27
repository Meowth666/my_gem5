#ifndef __CPU_PROBES_MY_INST_TRACKER_HH__
#define __CPU_PROBES_MY_INST_TRACKER_HH__

#include "debug/InstTracker.hh"
#include "params/MyLocalInstTracker.hh"
#include "params/MyGlobalInstTracker.hh"
#include "sim/probe/probe_listener_object.hh"
#include "sim/sim_exit.hh"

namespace gem5
{
    class MyGlobalInstTracker: public SimObject{
        public:
            MyGlobalInstTracker(const MyGlobalInstTrackerParams &params);
        private:
            uint64_t instCount;
            uint64_t instThreshold;
        public:
            void changeThreshold(uint64_t newThreshold) {
                instThreshold = newThreshold;
            }
            void resetCounter() {
                instCount = 0;
            }
            uint64_t getThreshold() const {
                return instThreshold;
            }
            void checkPc(const uint64_t& inst);
    };

    class MyLocalInstTracker : public ProbeListenerObject
    {
        public:
            MyLocalInstTracker(const MyLocalInstTrackerParams &params);
            virtual void regProbeListeners();
            void checkPc(const uint64_t& inst);
        private:
            typedef ProbeListenerArg<MyLocalInstTracker, uint64_t> MyLocalInstTrackerListener;
            bool listening;
            MyGlobalInstTracker *globalInstTracker;
        public:
            void
            stopListening()
            {
                listening = false;
                listeners.clear();
            }
            void startListening() {
                listening = true;
                regProbeListeners();
            }
            
    };
}

#endif