from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy

# simulation components
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import BinaryResource
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.isas import ISA
from pathlib import Path

import m5

from m5.objects import MyLocalInstTracker, MyGlobalInstTracker

binary_path = Path("/gem5/configs/bootcamp/local-inst-tracer/simple_workload")


cache_hierarchy = PrivateL1CacheHierarchy(
    l1d_size="64kB",
    l1i_size="64kB",
)

memory = SingleChannelDDR4_2400("1GB")

processor = SimpleProcessor(
    cpu_type = CPUTypes.TIMING,
    num_cores = 8,
    isa = ISA.X86
)

global_inst_tracker = MyGlobalInstTracker(
    inst_threshold = 100000
)
all_trackers = []

for core in processor.get_cores():
    tracker = MyLocalInstTracker(
        global_inst_tracker = global_inst_tracker,
        start_listening = False,
    )
    core.core.probeListener = tracker
    all_trackers.append(tracker)


board = SimpleBoard(
    clk_freq="1GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_se_binary_workload(
    binary = BinaryResource(
        local_path=binary_path.as_posix()
    )
)

def workbegin_handler():
    print("Reached workbegin")
    print("Dump and reset stats")
    m5.stats.reset()
    print("Start listening for instructions")
    for tracker in all_trackers:
        tracker.startListening()
    yield False

def workend_handler():
    print("Reached workend")
    yield False

def max_inst_handler():
    print("Reached MAX_INSTS")
    print("Exiting simulation")
    yield True

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.MAX_INSTS: max_inst_handler(),
        ExitEvent.WORKBEGIN: workbegin_handler(),
        ExitEvent.WORKEND: workend_handler(),
    }
)

simulator.run()
print("Simulation Done")