自动化绑定脚本（持续优化中）

本工具集提供 Maya 绑定的自动化功能，旨在提高绑定效率。用户需要预先手动放置必要的骨骼关节，并确保其命名符合规范。

使用流程
运行 window.py 启动工具界面。

在界面中，从本地文件浏览器选择您需要应用的绑定代码文件。

当前可用的核心功能模块包括：

base_rigging.py

space_switch.py

twist_joint.py

核心功能
base_rigging.py (基础绑定):

创建完整的角色基础绑定系统。

包含四肢的 IK/FK 切换功能。

包含躯干与头部的绑定设置。

space_switch.py (空间切换):

为头部和四肢的控制对象添加空间切换功能，使其可以跟随不同的父对象。

twist_joint.py (扭曲关节):

为四肢（如前臂、上臂、大腿、小腿）添加扭曲关节，实现更自然的旋转变形。

详见https://drive.google.com/file/d/1ihw0cqTjXG1QmrBFiOH4zioOy30CWd_j/view?usp=sharing
