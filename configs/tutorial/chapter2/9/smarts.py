import argparse
import math
from pathlib import Path

from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_private_l2_walk_cache_hierarchy import (
    PrivateL1PrivateL2WalkCacheHierarchy,
)
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_switchable_processor import SimpleSwitchableProcessor
from gem5.isas import ISA
from gem5.simulate.exit_event import ExitEvent
from gem5.simulate.simulator import Simulator
from gem5.resources.resource import BinaryResource
from gem5.utils.requires import requires
import json
import m5

requires(isa_required=ISA.X86)

cache_hierarchy = PrivateL1PrivateL2WalkCacheHierarchy(
    l1d_size="32kB",
    l1i_size="32kB",
    l2_size="256kB",
)

memory = DualChannelDDR4_2400(size="3GB")

processor = SimpleSwitchableProcessor(
    starting_core_type=CPUTypes.ATOMIC,
    switch_core_type=CPUTypes.O3,
    isa=ISA.X86,
    num_cores=1,
)

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_se_binary_workload(
    binary=BinaryResource(local_path=Path("/gem5/configs/tutorial/chapter2/9/simple_workload").as_posix())
)

def smarts_generator(
    k: int, U: int, W: int, processor
):
    is_switchable = isinstance(processor, SimpleSwitchableProcessor)
    warmup_start = U * (k - 1) - W
    warmup_plus_detailed = U + W
    counter = 0

    while is_switchable:
        print(f"curTick is {m5.curTick()}")
        print("got to warmup start\n")

        print("switch core type")
        # switch core type
        processor.switch()
        print(
            "now schedule for end of warmup and start of detailed simluation\n"
        )
        # schedule for warmup end
        # schedule for detailed simulation end
        processor.get_cores()[0]._set_simpoint([W, warmup_plus_detailed], True)
        print("fall back to simulation\n")
        # fall back to simualtion
        yield False

        # reached warmup end
        print(f"curTick is {m5.curTick()}")
        print("got to detail simulation start\n")
        print("now reset m5 stats\n")

        # reset stats
        m5.stats.reset()
        print("fall back to simulation\n")
        # fall back to simulation
        yield False

        # reached end of detailed simulation
        print(f"curTick is {m5.curTick()}")
        print("got to end of detail simulation\n")
        print("now dump stats\n")
        # dump stats
        m5.stats.dump()

        # switch core type
        print("switch core type\n")
        processor.switch()
        print(
            "now schedule for next warmup start and detail simulation start\n"
        )
        # schedule for the next start of warmup
        print("schedule for the next start of warmup\n")
        processor.get_cores()[0]._set_simpoint([warmup_start], True)
        print("increase n counter\n")
        # increment sample counter
        counter += 1
        print("switch core type to functional core type")
        print("fall back to simulation\n")
        yield False

program_length = 9115640
ideal_region_length = math.ceil(program_length/50)
ideal_U = 1000
ideal_k = math.ceil(ideal_region_length/ideal_U)
ideal_W = 2 * ideal_U

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.SIMPOINT_BEGIN: smarts_generator(
            k=ideal_k,
            U=ideal_U,
            W=ideal_W,
            processor=processor,
        )
    }
)

processor.get_cores()[0]._set_simpoint([1], False)
simulator.run()

print("Simulation Done")
