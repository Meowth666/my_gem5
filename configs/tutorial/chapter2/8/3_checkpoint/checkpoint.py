from gem5.components.boards.x86_board import X86Board
from gem5.components.processors.cpu_types import CPUTypes
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import (
    ExitEvent,
    Simulator,
)
from gem5.utils.requires import requires
import m5

requires(
    isa_required=ISA.X86,
    kvm_required=True,
)

# NoCache（用于 fast-forward）
from gem5.components.cachehierarchies.classic.no_cache import NoCache
cache_hierarchy = NoCache()

# 内存
from gem5.components.memory.single_channel import SingleChannelDDR4_2400
memory = SingleChannelDDR4_2400(size="3GiB")   # ✅ 建议改成 GiB

# KVM CPU（快）
processor = SimpleProcessor(
    cpu_type=CPUTypes.KVM,
    isa=ISA.X86,
    num_cores=2,
)

for proc in processor.get_cores():
    proc.core.usePerf = False

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

board.set_workload(obtain_resource("npb-ep-a"))

# 🔥 checkpoint 触发点（Linux boot 完成）
def workbegin_handler():
    print("Done booting Linux")
    print("Take a checkpoint")

    # ✅ 官方推荐方式
    m5.checkpoint("03-cpt")

    yield True   # 继续仿真

simulator = Simulator(
    board=board,
    on_exit_event={
        ExitEvent.WORKBEGIN: workbegin_handler(),
    }
)

print("Running the simulation")
print("Using KVM cpu")

simulator.run()

print("Simulation Done")