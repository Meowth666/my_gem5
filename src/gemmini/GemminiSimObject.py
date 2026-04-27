# 导入gem5所有模块的基类：SimObject（所有自定义硬件模块必须继承它）
from m5.objects.SimObject import SimObject
# 导入gem5的参数定义工具（Param是核心，用来给模块加配置）
from m5.params import *

# 自定义模块：GemminiSimObject
class GemminiSimObject(SimObject):
    # 1. gem5内部唯一识别名（必须和C++类名一致）
    type = "GemminiSimObject"
    # 2. 绑定：这个Python类对应的C++头文件路径
    cxx_header = "gemmini/gemmini_sim_object.hh"
    # 3. 绑定：这个Python类对应的C++类全名（带命名空间）→ C++gem5::HelloSimObject
    cxx_class = "gem5::GemminiSimObject"
    