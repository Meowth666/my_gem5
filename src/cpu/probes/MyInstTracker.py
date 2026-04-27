from m5.objects import SimObject
from m5.objects.Probe import ProbeListenerObject
from m5.params import *
from m5.util.pybind import *

class MyGlobalInstTracker(SimObject):
    type = "MyGlobalInstTracker"
    cxx_header = "cpu/probes/my_inst_tracker.hh"
    cxx_class = "gem5::MyGlobalInstTracker"
    cxx_exports = [
        PyBindMethod("changeThreshold"),
        PyBindMethod("resetCounter"),
        PyBindMethod("getThreshold")
    ]
    inst_threshold = Param.Counter("The instruction threshold to trigger an"
                                                                " exit event")
    
class MyLocalInstTracker(ProbeListenerObject):
    type = "MyLocalInstTracker"
    cxx_header = "cpu/probes/my_inst_tracker.hh"
    cxx_class = "gem5::MyLocalInstTracker"
    cxx_exports = [
        PyBindMethod("stopListening"),
        PyBindMethod("startListening")
    ]
    global_inst_tracker = Param.MyGlobalInstTracker("Global instruction tracker")
    start_listening = Param.Counter(True, "Start listening for instructions")


