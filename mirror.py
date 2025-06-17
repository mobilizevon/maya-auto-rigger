import maya.cmds as cmds


def mirror_curve_cv_positions():
    """镜像NURBS曲线控制点位置，支持_l_/_r_和L_/R_命名规则"""

    # 获取选中的transform节点
    selected_transforms = cmds.ls(selection=True, type='transform')

    if not selected_transforms:
        cmds.warning("请选择一个或多个控制器transform节点")
        return

    # 预先收集所有目标曲线，减少重复检查
    existing_transforms = set(cmds.ls(type='transform'))

    for transform in selected_transforms:
        # 获取曲线形状节点（优化查询方式）
        curves = cmds.listRelatives(transform, shapes=True, type='nurbsCurve', fullPath=True)

        if not curves:
            cmds.warning(f"'{transform}' 不包含NURBS曲线，跳过")
            continue

        curve = curves[0]  # 使用完整路径名避免歧义

        # 确定镜像目标名称（支持更多命名约定）
        target_name = None
        if '_l_' in transform.lower():
            target_name = transform.replace('_l_', '_r_').replace('_L_', '_R_')
        elif '_r_' in transform.lower():
            target_name = transform.replace('_r_', '_l_').replace('_R_', '_L_')
        elif transform.startswith(('L_', 'l_')):
            prefix = 'R_' if transform[0] == 'L' else 'r_'
            target_name = prefix + transform[2:]
        elif transform.startswith(('R_', 'r_')):
            prefix = 'L_' if transform[0] == 'R' else 'l_'
            target_name = prefix + transform[2:]

        if not target_name or target_name == transform:
            cmds.warning(f"无法确定 '{transform}' 的镜像目标，跳过")
            continue

        # 检查目标是否存在（使用预先收集的集合加快检查）
        if target_name not in existing_transforms:
            cmds.warning(f"未找到镜像目标 '{target_name}'，跳过")
            continue

        # 获取目标曲线形状节点
        target_curves = cmds.listRelatives(target_name, shapes=True, type='nurbsCurve', fullPath=True)
        if not target_curves:
            cmds.warning(f"目标 '{target_name}' 不包含NURBS曲线，跳过")
            continue

        target_curve = target_curves[0]

        # 获取所有CV点位置（优化查询方式）
        cv_count = cmds.getAttr(f"{curve}.controlPoints", size=True)
        cv_positions = [cmds.pointPosition(f"{curve}.cv[{i}]", world=True)
                        for i in range(cv_count)]

        # 镜像控制点位置（X轴镜像）
        mirrored_positions = [[-pos[0], pos[1], pos[2]] for pos in cv_positions]

        # 批量设置目标CV位置（减少xform调用）
        for i, pos in enumerate(mirrored_positions):
            cmds.xform(f"{target_curve}.cv[{i}]", translation=pos, worldSpace=True)

        print(f"成功镜像: {transform} → {target_name} ({cv_count}个控制点)")


# 添加UI调用入口
def show_mirror_curve_ui():
    """显示镜像曲线UI（非阻塞式）"""
    if cmds.window('mirrorCurveUI', exists=True):
        cmds.deleteUI('mirrorCurveUI')

    cmds.window('mirrorCurveUI', title="镜像曲线控制点", width=300)
    cmds.columnLayout(adjustableColumn=True)
    cmds.text(label="选择要镜像的曲线控制器")
    cmds.button(label="执行镜像", command=lambda x: mirror_curve_cv_positions())
    cmds.button(label="关闭", command=lambda x: cmds.deleteUI('mirrorCurveUI'))

    # 非阻塞式显示窗口
    cmds.showWindow('mirrorCurveUI')


# 执行方式建议
if __name__ == "__main__":
    # 使用非阻塞式UI方式
    show_mirror_curve_ui()