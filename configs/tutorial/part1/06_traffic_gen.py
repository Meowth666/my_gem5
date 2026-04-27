# Copyright (c) 2021 The Regents of the University of California
# All rights reserved.

import m5

from my_components.cache_hierarchy import MyPrivateL1SharedL2CacheHierarchy
from my_components.hybrid_generator import HybridGenerator

from gem5.components.boards.test_board import TestBoard
from gem5.components.memory import SingleChannelDDR3_1600
from gem5.components.processors.linear_generator import LinearGenerator
from gem5.components.processors.random_generator import RandomGenerator
from gem5.simulate.simulator import Simulator

# -------------------------------
# 1. 构建 Cache / Memory / Generator
# -------------------------------

cache_hierarchy = MyPrivateL1SharedL2CacheHierarchy()

memory = SingleChannelDDR3_1600()

# Traffic Generator（线性访问）
generator = RandomGenerator(
    num_cores=1,
    rate="1GB/s"
)
# generator = HybridGenerator(
#     num_cores=6
# )
# -------------------------------
# 2. 构建 Board（系统）
# -------------------------------

motherboard = TestBoard(
    clk_freq="3GHz",
    generator=generator,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# -------------------------------
# 3. 使用 Simulator（关键！）
# -------------------------------

simulator = Simulator(board=motherboard)

# -------------------------------
# 4. 启动 traffic + 运行仿真
# -------------------------------

print("Beginning simulation!")

# 启动流量（注意：components体系仍需手动start）
# generator.start_traffic()

# 运行仿真（内部会自动 instantiate + simulate）
simulator.run()

print("Simulation finished at tick {}".format(m5.curTick()))
