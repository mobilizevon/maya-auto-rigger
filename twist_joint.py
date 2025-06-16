import maya.cmds as cmds


def setup_twist_system(side, limb_part, start_joint, end_joint, parent_joint, ik_parent, twist_direction='start'):
    """
    设置单个twist系统

    参数:
        side (str): 'l' 或 'r' - 左侧或右侧
        limb_part (str): 肢体部分名称 (如 'upperArm', 'elbow', 'upperLeg', 'knee')
        start_joint (str): 起始关节的完整名称
        end_joint (str): 结束关节的完整名称
        parent_joint (str): twist关节的父级
        ik_parent (str): IK手柄的父级
        twist_direction (str): 'start' 或 'end' - twist在靠近起始或结束关节处最强
    """
    # 创建驱动器关节
    driver_prefix = f"jnt_{side}_{limb_part}TwistDriver"

    cmds.select(clear=True)
    cmds.joint(n=f"{driver_prefix}_001")
    cmds.joint(n=f"{driver_prefix}_002")

    # 匹配变换
    cmds.matchTransform(f"{driver_prefix}_001", start_joint)
    cmds.matchTransform(f"{driver_prefix}_002", end_joint, position=True, rotation=False)

    # 冻结变换
    cmds.makeIdentity(f"{driver_prefix}_001", apply=True, translate=True, rotate=True, scale=True)
    cmds.makeIdentity(f"{driver_prefix}_002", apply=True, translate=True, rotate=True, scale=True)

    # 设置父子关系
    cmds.parent(f"{driver_prefix}_001", parent_joint)

    # 创建IK控制器
    cmds.ikHandle(
        startJoint=f"{driver_prefix}_001",  # 起始关节
        endEffector=f"{driver_prefix}_002",  # 末端关节
        solver="ikSCsolver",  # 使用单链IK解算器
        name=f"ikHnd_{side}_{limb_part}TwistDriver_001"
    )

    # 设置IK控制器的父级和约束
    cmds.parent(f"ikHnd_{side}_{limb_part}TwistDriver_001", ik_parent)

    # 如果是上部关节(大臂/大腿)，需要点约束到末端关节
    if limb_part.lower() in ["upperarm", "upperleg"]:
        cmds.pointConstraint(end_joint, f"ikHnd_{side}_{limb_part}TwistDriver_001")

    # 隐藏IK控制器
    cmds.hide(f"ikHnd_{side}_{limb_part}TwistDriver_001")

    # 创建5个twist关节
    twist_joints = []
    for i in range(1, 6):
        joint_name = f"jnt_{side}_{limb_part}Twist_00{i}"
        cmds.select(clear=True)
        cmds.joint(n=joint_name)
        twist_joints.append(joint_name)

    # 匹配所有twist关节的初始位置到驱动器
    for joint in twist_joints:
        cmds.matchTransform(joint, f"{driver_prefix}_001")

    # 冻结变换
    cmds.makeIdentity(f"jnt_{side}_{limb_part}Twist_00?", apply=True, translate=True, rotate=True, scale=True)

    # 设置末端twist关节的位置
    cmds.matchTransform(f"jnt_{side}_{limb_part}Twist_005", end_joint, position=True, rotation=False)

    # 设置中间twist关节的位置（通过点约束）
    cmds.pointConstraint(f"jnt_{side}_{limb_part}Twist_001", f"jnt_{side}_{limb_part}Twist_005",
                         f"jnt_{side}_{limb_part}Twist_002", w=0.75)
    cmds.setAttr(f"jnt_{side}_{limb_part}Twist_002_pointConstraint1.jnt_{side}_{limb_part}Twist_005W1", 0.25)

    cmds.pointConstraint(f"jnt_{side}_{limb_part}Twist_001", f"jnt_{side}_{limb_part}Twist_005",
                         f"jnt_{side}_{limb_part}Twist_003", w=0.5)

    cmds.pointConstraint(f"jnt_{side}_{limb_part}Twist_001", f"jnt_{side}_{limb_part}Twist_005",
                         f"jnt_{side}_{limb_part}Twist_004", w=0.25)
    cmds.setAttr(f"jnt_{side}_{limb_part}Twist_004_pointConstraint1.jnt_{side}_{limb_part}Twist_005W1", 0.75)

    # 删除约束，保留位置
    cmds.delete(f"jnt_{side}_{limb_part}Twist_00?_pointConstraint1")

    # 设置twist关节的父级
    cmds.parent(f"jnt_{side}_{limb_part}Twist_00?", parent_joint)

    # 根据twist方向连接旋转
    if twist_direction == 'start':
        # 大臂/大腿：twist在靠近肩膀/髋部最强
        cmds.connectAttr(f"{driver_prefix}_001.rotateX", f"jnt_{side}_{limb_part}Twist_001.rotateX")

        # 创建乘法节点并连接中间关节
        for i in range(2, 5):
            mult_node = f"mult_{side}_{limb_part}Twist_00{i}"
            cmds.createNode('multDoubleLinear', name=mult_node)
            cmds.connectAttr(f"{driver_prefix}_001.rotateX", f"{mult_node}.input1")
            cmds.connectAttr(f"{mult_node}.output", f"jnt_{side}_{limb_part}Twist_00{i}.rotateX")

        # 设置twist权重递减
        cmds.setAttr(f"mult_{side}_{limb_part}Twist_002.input2", 0.75)
        cmds.setAttr(f"mult_{side}_{limb_part}Twist_003.input2", 0.5)
        cmds.setAttr(f"mult_{side}_{limb_part}Twist_004.input2", 0.25)
    else:
        # 小臂/小腿：twist在靠近手腕/脚踝最强
        cmds.connectAttr(f"{driver_prefix}_001.rotateX", f"jnt_{side}_{limb_part}Twist_005.rotateX")

        # 创建乘法节点并连接中间关节
        for i in range(2, 5):
            mult_node = f"mult_{side}_{limb_part}Twist_00{i}"
            cmds.createNode('multDoubleLinear', name=mult_node)
            cmds.connectAttr(f"{driver_prefix}_001.rotateX", f"{mult_node}.input1")
            cmds.connectAttr(f"{mult_node}.output", f"jnt_{side}_{limb_part}Twist_00{i}.rotateX")

        # 设置twist权重递增
        cmds.setAttr(f"mult_{side}_{limb_part}Twist_002.input2", 0.25)
        cmds.setAttr(f"mult_{side}_{limb_part}Twist_003.input2", 0.5)
        cmds.setAttr(f"mult_{side}_{limb_part}Twist_004.input2", 0.75)

    # 隐藏驱动器关节
    cmds.hide(f"{driver_prefix}_001")


def setup_limb_twist(side, limb_type, upper_joint, middle_joint, lower_joint, scapula_or_hip_joint):
    """
    为整个肢体设置twist系统

    参数:
        side (str): 'l' 或 'r' - 左侧或右侧
        limb_type (str): 'arm' 或 'leg' - 肢体类型
        upper_joint (str): 上部关节的完整名称 (如 'jnt_l_upperArm_001')
        middle_joint (str): 中部关节的完整名称 (如 'jnt_l_elbow_001')
        lower_joint (str): 下部关节的完整名称 (如 'jnt_l_wrist_001')
        scapula_or_hip_joint (str): 肩胛骨或髋关节的完整名称
    """
    # 提取关节基本名称
    upper_name = upper_joint.split('_')[-2]  # 例如: upperArm, upperLeg
    middle_name = middle_joint.split('_')[-2]  # 例如: elbow, knee

    # 设置上部twist系统（大臂/大腿）
    setup_twist_system(
        side=side,
        limb_part=upper_name,
        start_joint=upper_joint,
        end_joint=middle_joint,
        parent_joint=upper_joint,
        ik_parent=scapula_or_hip_joint,
        twist_direction='start'
    )

    # 设置下部twist系统（小臂/小腿）
    setup_twist_system(
        side=side,
        limb_part=middle_name,
        start_joint=middle_joint,
        end_joint=lower_joint,
        parent_joint=middle_joint,
        ik_parent=lower_joint,
        twist_direction='end'
    )


# 设置左臂twist
setup_limb_twist(
    side='l',
    limb_type='arm',
    upper_joint='jnt_l_upperArm_001',
    middle_joint='jnt_l_elbow_001',
    lower_joint='jnt_l_wrist_001',
    scapula_or_hip_joint='jnt_l_scapula_001'
)

# 设置右臂twist
setup_limb_twist(
    side='r',
    limb_type='arm',
    upper_joint='jnt_r_upperArm_001',
    middle_joint='jnt_r_elbow_001',
    lower_joint='jnt_r_wrist_001',
    scapula_or_hip_joint='jnt_r_scapula_001'
)

# 设置左腿twist
setup_limb_twist(
    side='l',
    limb_type='leg',
    upper_joint='jnt_l_upperLeg_001',
    middle_joint='jnt_l_knee_001',
    lower_joint='jnt_l_ankle_001',
    scapula_or_hip_joint='jnt_m_pelvisLocal_001'  # 根据实际骨骼层级调整
)

# 设置右腿twist
setup_limb_twist(
    side='r',
    limb_type='leg',
    upper_joint='jnt_r_upperLeg_001',
    middle_joint='jnt_r_knee_001',
    lower_joint='jnt_r_ankle_001',
    scapula_or_hip_joint='jnt_m_pelvisLocal_001'  # 根据实际骨骼层级调整
)
