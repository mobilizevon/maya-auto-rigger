import maya.cmds as cmds

# ========================
# 全局配置
# ========================
SPACE_OPTIONS = ["World", "Cog", "Chest", "Head", "Pelvis", "Neck", "Clavicle", "Scapula"]
SPACE_GROUPS = {
    "World": "grp_m_worldSpaceLocs_001",
    "Cog": "grp_m_cogSpaceLocs_001",
    "Chest": "grp_m_chestSpaceLocs_001",
    "Head": "grp_m_headSpaceLocs_001",
    "Pelvis": "grp_m_pelvisSpaceLocs_001",
    "Neck": "grp_m_neckSpaceLocs_001",
    "Clavicle": "grp_<side>_clavicleSpaceLocs_001",  # 动态占位符
    "Scapula": "grp_<side>_scapulaSpaceLocs_001"  # 动态占位符
}

# 定义组名与父对象的映射关系
group_parents = [
    ("grp_m_worldSpaceLocs_001", "ctrl_m_world_001"),
    ("grp_m_cogSpaceLocs_001", "output_m_cog_001"),
    ("grp_m_chestSpaceLocs_001", "jnt_m_spine_006"),
    ("grp_m_headSpaceLocs_001", "jnt_m_headLocal_001"),
    ("grp_m_pelvisSpaceLocs_001", "jnt_m_pelvisLocal_001"),
    ("grp_m_neckSpaceLocs_001", "output_m_headIkBendB_001"),
    ("grp_l_scapulaSpaceLocs_001", "output_l_scapula_001"),
    ("grp_r_scapulaSpaceLocs_001", "output_r_scapula_001"),
    ("grp_l_clavicleSpaceLocs_001", "output_l_clavicle_001"),
    ("grp_r_clavicleSpaceLocs_001", "output_r_clavicle_001")
]

# 空间组配置（所有命名规则统一）
space_groups = {
    'handIk': {'sides': ['l', 'r']},  # 左右处理
    'ankleIk': {'sides': ['l', 'r']},  # 左右处理
}

# ========================
# 核心函数
# ========================


def create_space_switch(ctrl_name, space_group, prefix, space_options, space_group_map, constraint_type="parent"):
    """
    为控制器创建空间切换系统（完整实现）

    参数:
        ctrl_name: 控制器名称 (e.g. 'ctrl_l_handIk_001')
        space_group: 空间组名称 (e.g. 'space_l_handIk_001')
        prefix: 命名前缀 (e.g. 'l_hand')
        space_options: 空间选项列表 (e.g. ['World', 'Clavicle'])
        space_group_map: 空间组映射字典
        constraint_type: 约束类型 - "parent"(父子约束)或"orient"(旋转约束)
    """
    # 1. 确定左右侧
    side = "l" if prefix.startswith("l_") else "r" if prefix.startswith("r_") else "m"

    # 2. 添加空间枚举属性
    if not cmds.objExists(f"{ctrl_name}.space"):
        enum_str = ":".join([f"{opt}={i}" for i, opt in enumerate(space_options)])
        cmds.addAttr(ctrl_name, ln="space", at="enum", enumName=enum_str, keyable=True)

    # 3. 创建/复用空间定位器
    locators = []
    for opt in space_options:
        # 动态生成空间组名（处理占位符）
        base_group = space_group_map.get(opt)
        group_name = (
                         base_group.replace("<side>", side)
                         if base_group and "<side>" in base_group
                         else base_group
                     ) or space_group_map["World"]  # 默认使用World组

        loc_name = f"loc_{prefix}Space{opt}_001"
        zero_name = f"zero_{prefix}Space{opt}_001"

        # 定位器存在则复用，否则创建
        if not cmds.objExists(loc_name):
            loc = cmds.spaceLocator(name=loc_name)[0]
            zero_group = cmds.group(loc, name=zero_name)
            cmds.parent(zero_group, group_name)
            cmds.matchTransform(zero_group, space_group)
        else:
            loc = loc_name
        locators.append(loc)

    # 4. 根据约束类型创建约束系统
    if constraint_type.lower() == "orient":
        # 旋转约束
        constraint_node = f"{space_group}_orientConstraint"
        if not cmds.objExists(constraint_node):
            constraint_node = cmds.orientConstraint(
                *locators,
                space_group,
                maintainOffset=False,
                name=constraint_node
            )[0]
            cmds.setAttr(f"{constraint_node}.interpType", 2)  # 最短路径插值
    else:
        # 默认使用父子约束
        constraint_node = f"{space_group}_parentConstraint"
        if not cmds.objExists(constraint_node):
            constraint_node = cmds.parentConstraint(
                *locators,
                space_group,
                maintainOffset=False,
                name=constraint_node
            )[0]
            cmds.setAttr(f"{constraint_node}.interpType", 2)  # 最短路径插值

    # 5. 连接条件切换逻辑
    for i, (opt, loc) in enumerate(zip(space_options, locators)):
        cond_node = f"cond_{prefix}Space{opt}_001"
        weight_attr = f"{constraint_node}.{loc}W{i}"

        if not cmds.objExists(cond_node):
            cond = cmds.createNode("condition", name=cond_node)
            cmds.connectAttr(f"{ctrl_name}.space", f"{cond}.firstTerm")
            cmds.setAttr(f"{cond}.secondTerm", i)
            cmds.setAttr(f"{cond}.operation", 0)  # 等于操作
            cmds.setAttr(f"{cond}.colorIfTrueR", 1)
            cmds.setAttr(f"{cond}.colorIfFalseR", 0)
            cmds.connectAttr(f"{cond}.outColorR", weight_attr)


# ========================
# 辅助函数（完整子模块）
# ========================
def add_space_attribute(ctrl_name, options):
    """为控制器添加空间枚举属性"""
    if not cmds.attributeQuery("space", node=ctrl_name, exists=True):
        enum_names = ":".join([f"{opt}={i}" for i, opt in enumerate(options)])
        cmds.addAttr(
            ctrl_name,
            longName="space",
            attributeType="enum",
            enumName=enum_names,
            keyable=True
        )


def create_space_locators(prefix, space_group, options, group_mapping, constraint_type="parent"):
    """创建空间定位器组（含左右处理）"""
    side = "l" if prefix.startswith("l_") else "r" if prefix.startswith("r_") else "m"
    locators = []

    for opt in options:
        # 动态生成组名
        base_group = group_mapping.get(opt)
        group_name = (
                         base_group.replace("<side>", side)
                         if base_group and "<side>" in base_group
                         else base_group
                     ) or group_mapping["World"]

        loc_name = f"loc_{prefix}Space{opt}_001"
        zero_name = f"zero_{prefix}Space{opt}_001"

        if not cmds.objExists(loc_name):
            loc = cmds.spaceLocator(name=loc_name)[0]
            zero_group = cmds.group(loc, name=zero_name)
            cmds.parent(zero_group, group_name)
            cmds.matchTransform(zero_group, space_group)
        else:
            loc = loc_name
        locators.append(loc)

    return locators


def setup_space_constraints(space_group, locators, constraint_type="parent"):
    """创建约束节点"""
    if constraint_type.lower() == "orient":
        constraint_node = cmds.orientConstraint(
            *locators,
            space_group,
            maintainOffset=False,
            name=f"{space_group}_orientConstraint"
        )[0]
    else:
        constraint_node = cmds.parentConstraint(
            *locators,
            space_group,
            maintainOffset=False,
            name=f"{space_group}_parentConstraint"
        )[0]

    cmds.setAttr(f"{constraint_node}.interpType", 2)
    return constraint_node


def connect_switch_logic(ctrl_name, constraint_node, locators, options, prefix):
    """连接条件节点控制约束权重"""
    for i, (opt, loc) in enumerate(zip(options, locators)):
        cond_node = cmds.createNode("condition", name=f"cond_{prefix}Space{opt}_001")
        weight_attr = f"{constraint_node}.{loc}W{i}"

        cmds.connectAttr(f"{ctrl_name}.space", f"{cond_node}.firstTerm")
        cmds.setAttr(f"{cond_node}.secondTerm", i)
        cmds.setAttr(f"{cond_node}.operation", 0)
        cmds.setAttr(f"{cond_node}.colorIfTrueR", 1)
        cmds.setAttr(f"{cond_node}.colorIfFalseR", 0)
        cmds.connectAttr(f"{cond_node}.outColorR", weight_attr)


# ========================
# 调用示例
# ========================

# 批量创建空间组
for group_type, config in space_groups.items():
    for side in config['sides']:
        # 统一命名规则
        space_name = f"space_{side}_{group_type}_001"
        driven_name = f"driven_{side}_{group_type}_001"
        connect_name = f"connect_{side}_{group_type}_001"

        # 创建并设置空间组
        cmds.group(em=True, n=space_name)
        cmds.matchTransform(space_name, driven_name)
        cmds.parent(space_name, driven_name)
        cmds.parent(connect_name, space_name)

# 批量创建空组并设置父子关系
for group_name, parent_obj in group_parents:
    if not cmds.objExists(group_name):
        cmds.group(em=True, n=group_name)
        cmds.hide(group_name)

    if cmds.objExists(parent_obj):
        cmds.parent(group_name, parent_obj)
    else:
        print(f"// Warning: 父对象 '{parent_obj}' 不存在，跳过层级设置 //")

cmds.hide("grp_?_*SpaceLocs_001")

create_space_switch(
    ctrl_name="ctrl_l_handIk_001",
    space_group="space_l_handIk_001",
    prefix="l_handIk",
    space_options=["World", "Cog", "Chest", "Head", "Pelvis"],
    space_group_map=SPACE_GROUPS
)

create_space_switch(
    ctrl_name="ctrl_r_handIk_001",
    space_group="space_r_handIk_001",
    prefix="r_handIk",
    space_options=["World", "Cog", "Chest", "Head", "Pelvis"],
    space_group_map=SPACE_GROUPS
)

create_space_switch(
    ctrl_name="ctrl_l_ankleIk_001",
    space_group="space_l_ankleIk_001",
    prefix="l_ankleIk",
    space_options=["World", "Cog", "Pelvis"],
    space_group_map=SPACE_GROUPS
)

create_space_switch(
    ctrl_name="ctrl_r_ankleIk_001",
    space_group="space_r_ankleIk_001",
    prefix="r_ankleIk",
    space_options=["World", "Cog", "Pelvis"],
    space_group_map=SPACE_GROUPS
)

create_space_switch(
    ctrl_name="ctrl_l_elbowIkGuide_001",
    space_group="space_l_elbowIkGuide_001",
    prefix="l_elbowIkGuide",
    space_options=["World", "Cog", "Chest", "Head", "Pelvis"],
    space_group_map=SPACE_GROUPS
)

create_space_switch(
    ctrl_name="ctrl_r_elbowIkGuide_001",
    space_group="space_r_elbowIkGuide_001",
    prefix="r_elbowIkGuide",
    space_options=["World", "Cog", "Chest", "Head", "Pelvis"],
    space_group_map=SPACE_GROUPS
)

create_space_switch(
    ctrl_name="ctrl_l_kneeIkGuide_001",
    space_group="space_l_kneeIkGuide_001",
    prefix="l_kneeIkGuide",
    space_options=["World", "Cog", "Pelvis"],
    space_group_map=SPACE_GROUPS
)
create_space_switch(
    ctrl_name="ctrl_r_kneeIkGuide_001",
    space_group="space_r_kneeIkGuide_001",
    prefix="r_kneeIkGuide",
    space_options=["World", "Cog", "Pelvis"],
    space_group_map=SPACE_GROUPS
)

create_space_switch(
    ctrl_name="ctrl_m_headIk_001",
    space_group="space_m_headIk_001",
    prefix="m_headIk",
    space_options=["World", "Cog", "Chest", "Neck"],
    space_group_map=SPACE_GROUPS,
    constraint_type='orient'

)

create_space_switch(
    ctrl_name="ctrl_l_upperArmFk_001",
    space_group="space_l_upperArmFk_001",
    prefix="l_upperArmFk",
    space_options=["World", "Cog", "Chest", "Clavicle", "Scapula"],
    space_group_map=SPACE_GROUPS,
    constraint_type='orient'
)

create_space_switch(
    ctrl_name="ctrl_r_upperArmFk_001",
    space_group="space_r_upperArmFk_001",
    prefix="r_upperArmFk",
    space_options=["World", "Cog", "Chest", "Clavicle", "Scapula"],
    space_group_map=SPACE_GROUPS,
    constraint_type='orient'
)

create_space_switch(
    ctrl_name="ctrl_l_upperLegFk_001",
    space_group="space_l_upperLegFk_001",
    prefix="l_upperLegFk",
    space_options=["World", "Cog", "Pelvis"],
    space_group_map=SPACE_GROUPS,
    constraint_type='orient'
)

create_space_switch(
    ctrl_name="ctrl_r_upperLegFk_001",
    space_group="space_r_upperLegFk_001",
    prefix="r_upperLegFk",
    space_options=["World", "Cog", "Pelvis"],
    space_group_map=SPACE_GROUPS,
    constraint_type='orient'
)
