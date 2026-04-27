# 导入gem5所有模块的基类：SimObject（所有自定义硬件模块必须继承它）
from m5.objects.SimObject import SimObject
# 导入gem5的参数定义工具（Param是核心，用来给模块加配置）
from m5.params import *

# 第一个自定义模块：HelloSimObject
class HelloSimObject(SimObject):
    # 1. gem5内部唯一识别名（必须和C++类名一致）
    type = "HelloSimObject"
    # 2. 绑定：这个Python类对应的C++头文件路径
    cxx_header = "bootcamp/hello-sim-object/hello_sim_object.hh"
    # 3. 绑定：这个Python类对应的C++类全名（带命名空间）→ C++gem5::HelloSimObject
    cxx_class = "gem5::HelloSimObject"
    # 4. 定义整数参数 → 你最困惑的点2 参数名：num_hellos  注释"Number of times to say Hello."  类型： int
    num_hellos = Param.Int("Number of times to say Hello.")
    # 5. 定义模块关联参数 → 你最困惑的点3
    goodbye_object = Param.GoodByeSimObject("GoodByeSimObject to say goodbye after done saying hello.")

# 第二个自定义模块：GoodByeSimObject
class GoodByeSimObject(SimObject):
    type = "GoodByeSimObject"
    cxx_header = "bootcamp/hello-sim-object/goodbye_sim_object.hh"
    cxx_class = "gem5::GoodByeSimObject"