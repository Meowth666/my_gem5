from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import (
    PrivateL1CacheHierarchy
)
from gem5.components.boards.x86_board import X86Board
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.memory import DualChannelDDR4_2400
from gem5.components.processors.cpu_types import CPUTypes
from gem5.isas import ISA
from gem5.resources.resource import obtain_resource
from gem5.simulate.simulator import Simulator
from gem5.utils.requires import requires
import m5
from m5.objects.Root import Root

requires(
    isa_required=ISA.X86,
    kvm_required=True,
)

# -------------------------------
# 1. 硬件配置
# -------------------------------
cache_hierarchy = PrivateL1CacheHierarchy(
    l1d_size="32kB",
    l1i_size="32kB"
)

memory = DualChannelDDR4_2400(size="3GB")

processor = SimpleProcessor(
    cpu_type=CPUTypes.TIMING,
    isa=ISA.X86,
    num_cores=2,
)

board = X86Board(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# ⚠️ 注意：restore checkpoint 时，其实 workload 会被覆盖
board.set_workload(obtain_resource("npb-ep-a"))
# -------------------------------
# 2. 创建 Simulator
# -------------------------------
# simulator = Simulator(board=board)
board._pre_instantiate()
print("Restoring checkpoint...")
m5.instantiate("/gem5/03-cpt")
print("Running the simulation")
print("Simulation will exit after 1e9 ticks")
# -------------------------------
# 3. 运行仿真
# -------------------------------
m5.simulate(1000000000)

print("Simulation Done")
