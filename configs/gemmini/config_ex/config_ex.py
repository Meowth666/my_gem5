from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.private_l1_cache_hierarchy import PrivateL1CacheHierarchy
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import BinaryResource
from gem5.simulate.simulator import Simulator
from gem5.isas import ISA
from m5.objects import *
from m5.objects.GemminiSimObject import GemminiSimObject

dir_path = os.path.dirname(os.path.realpath(__file__))

cache_hierarchy = PrivateL1CacheHierarchy(l1d_size="32KiB", l1i_size="32KiB")
memory = SingleChannelDDR3_1600("1GiB")

gemmini = GemminiSimObject()
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1, isa=ISA.RISCV)
core = processor.cores[0]
core.core.GemMini = gemmini

print("------------------")
# print(core.core.GemMini.config_ex)
print("Connect to CPU")

board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy
)

board.set_se_binary_workload(BinaryResource(dir_path + "/config_ex_test"))
simulator = Simulator(board=board)
simulator.run()
print("Simulate End")
