import maya.cmds as cmds
import math

# 定义组的名称列表
groups = ["geometry", "controls", "rigNodes", "joints"]

base_chains = {
    "arm": [
        "jnt_l_upperArm_001",
        "jnt_l_elbow_001",
        "jnt_l_wrist_001",
        "jnt_l_wristEnd_001"
    ],
    "leg": [
        "jnt_l_upperLeg_001",
        "jnt_l_knee_001",
        "jnt_l_ankle_001",
        "jnt_l_ball_001",
        "jnt_l_toeEnd_001"
    ]
}



# 定义属性及其类型和参数
master_attributes = {
    "geometryVis": {"type": "bool", "default": True, "target_group": "geometry", "target_attribute": "visibility"},
    "resolution": {"type": "enum", "options": "Low:Medium:High", "default": 0, "target_group": "geometry",
                   "target_attribute": "none"},
    "controlsVis": {"type": "bool", "default": True, "target_group": "controls", "target_attribute": "visibility"},
    "jointsVis": {"type": "bool", "default": True, "target_group": "joints", "target_attribute": "visibility"},
    "rigNodesVis": {"type": "bool", "default": True, "target_group": "rigNodes", "target_attribute": "visibility"},
    "geometryDisplayType": {"type": "enum", "options": "Normal:Template:Reference", "default": 0,
                            "target_group": "geometry", "target_attribute": "overrideDisplayType"},
}

# 定义控制器形状信息
CTRL_INFO = {
    'shape': {
        'square': {'degree': 1,
                   'point': [[-1, 0, -1], [-1, 0, 1], [1, 0, 1], [1, 0, -1], [-1, 0, -1]],
                   'knot': [0, 1, 2, 3, 4]},
        'arrow': {'degree': 1,
                  'point': [[-0.5, 0, -1], [-0.5, 0, 0], [-1, 0, 0], [0, 0, 1], [1, 0, 0], [0.5, 0, 0], [0.5, 0, -1],
                            [-0.5, 0, -1]],
                  'knot': [0, 1, 2, 3, 4, 5, 6, 7]},
        'cube': {'degree': 1,
                 'point': [[-0.5, 0.5, 0.5], [-0.5, -0.5, 0.5], [0.5, -0.5, 0.5], [0.5, 0.5, 0.5],
                           [-0.5, 0.5, 0.5], [-0.5, 0.5, -0.5], [0.5, 0.5, -0.5], [0.5, 0.5, 0.5],
                           [0.5, -0.5, 0.5], [0.5, -0.5, -0.5], [0.5, 0.5, -0.5], [0.5, -0.5, -0.5],
                           [-0.5, -0.5, -0.5], [-0.5, 0.5, -0.5], [-0.5, -0.5, -0.5], [-0.5, -0.5, 0.5]],
                 'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]},
        'octagon': {'degree': 1,
                    'point': [(math.cos(2 * math.pi * i / 8), 0, math.sin(2 * math.pi * i / 8))
                              for i in range(8)] + [[1, 0, 0]],
                    'knot': list(range(9))},
        'cross': {'degree': 1,
                  'point': [[1, 3, 0], [1, 1, 0], [3, 1, 0], [3, -1, 0], [1, -1, 0], [1, -3, 0], [-1, -3, 0],
                            [-1, -1, 0],
                            [-3, -1, 0], [-3, 1, 0], [-1, 1, 0], [-1, 3, 0], [1, 3, 0]],
                  'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]},
        'cog': {'degree': 1,
                'point': [
                    (0.5, 0, 0), (0.35, 0, 0.35), (0, 0, 0.5), (-0.35, 0, 0.35), (-0.5, 0, 0),
                    (-0.35, 0, -0.35), (0, 0, -0.5), (0.35, 0, -0.35), (0.5, 0, 0)
                ],
                'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8]},
        'headLocal': {'degree': 1,
                      'point': [(0.0, 1.0, 0.0), (0.0, 0.7071067690849304, 0.7071067094802856),
                                (0.0, 0.0, 0.9999999403953552), (0.0, -0.7071067690849304, 0.7071067094802856),
                                (0.0, -1.0, 0.0), (0.0, -0.7071067690849304, -0.7071067094802856),
                                (0.0, 0.0, -0.9999998807907104), (0.0, 0.7071067690849304, -0.7071067094802856),
                                (0.0, 1.0, 0.0), (0.7071067690849304, 0.7071067690849304, 0.0),
                                (1.0, 0.0, 0.0), (0.7071067690849304, -0.7071067690849304, 0.0),
                                (0.0, -1.0, 0.0), (-0.7071067094802856, -0.7071067690849304, 0.0),
                                (-0.9999998807907104, 0.0, 0.0), (-0.7071067094802856, 0.7071067690849304, 0.0),
                                (0.0, 1.0, 0.0), (-0.7071067094802856, 0.7071067690849304, 0.0),
                                (-0.9999998807907104, 0.0, 0.0), (-0.7071067094802856, 0.0, -0.7071067094802856),
                                (0.0, 0.0, -0.9999998807907104), (0.7071067094802856, 0.0, -0.7071067094802856),
                                (1.0, 0.0, 0.0), (0.7071067690849304, 0.0, 0.7071067690849304),
                                (0.0, 0.0, 0.9999999403953552), (-0.7071067094802856, 0.0, 0.7071067094802856),
                                (-0.9999998807907104, 0.0, 0.0)],
                      'knot': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0,
                               16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0]},
        'clavicle': {'degree': 1,
                     'point': [[0, 0, 5], [-1, 0, 6], [0, 0, 7], [1, 0, 6], [0, 0, 5], [0, 0, 0], [0, 0, -5],
                               [-1, 0, -6], [0, 0, -7], [1, 0, -6], [0, 0, -5], [0, 1, -6], [0, 0, -7], [0, -1, -6],
                               [0, 0, -5], [0, 0, 0], [0, 0, 5], [0, 1, 6], [0, 0, 7], [0, -1, 6], [0, 0, 5],
                               [0, 1, 6], [-1, 0, 6], [0, -1, 6], [1, 0, 6], [0, 1, 6], [0, 0, 5], [0, 0, 0],
                               [0, 0, -5], [0, 1, -6], [-1, 0, -6], [0, -1, -6], [1, 0, -6], [0, 1, -6]],
                     'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23,
                              24, 25, 26, 27, 28, 29, 30, 31, 32, 33]},
        'scapulaL': {
            'degree': 1,  # 1 次 B 样条（线性插值，即多段线）
            'point': [
                [13.373194609638492, -2.581291462895584, 12.8058831275416],
                [20.283956464120095, -2.70416136816603, 6.017509772261082],
                [18.988162596908182, -2.890748278129042, 4.684836406511425],
                [12.077400742426562, -2.7678783728585623, 11.473209761791942],
                [13.373194609638492, -2.581291462895584, 12.8058831275416],
                [15.571351046855208, -16.671422312629037, 11.33382213369734],
                [20.58425062251515, -16.782766575005688, 6.378306316622873],
                [20.283956464120095, -2.70416136816603, 6.017509772261082],
                [20.58425062251515, -16.782766575005688, 6.378306316622873],
                [19.288456755303216, -16.969353484968682, 5.045632950873244],
                [18.988162596908182, -2.890748278129042, 4.684836406511425],
                [19.288456755303216, -16.969353484968682, 5.045632950873244],
                [14.27555717964326, -16.85800922259205, 10.001148767947683],
                [12.077400742426562, -2.7678783728585623, 11.473209761791942],
                [14.27555717964326, -16.85800922259205, 10.001148767947683],
                [15.571351046855208, -16.671422312629037, 11.33382213369734],
                [13.373194609638492, -2.581291462895584, 12.8058831275416]
            ],
            'knot': [0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0]},

        'scapulaR': {
            'degree': 1,  # 线性 B 样条（多段线）
            'point': [
                [-13.373196469376804, 2.5808795772834046, -12.805860451019084],
                [-20.283958323858407, 2.7037494825538517, -6.017487095738566],
                [-18.988164456646494, 2.890336392516863, -4.684813729988909],
                [-12.077402602164874, 2.7674664872463826, -11.473187085269426],
                [-13.373196469376804, 2.5808795772834046, -12.805860451019084],
                [-15.571352906593518, 16.671010427016856, -11.333799457174825],
                [-20.584252482253458, 16.782354689393507, -6.378283640100357],
                [-20.283958323858407, 2.7037494825538517, -6.017487095738566],
                [-20.584252482253458, 16.782354689393507, -6.378283640100357],
                [-19.288458615041524, 16.9689415993565, -5.045610274350728],
                [-18.988164456646494, 2.890336392516863, -4.684813729988909],
                [-19.288458615041524, 16.9689415993565, -5.045610274350728],
                [-14.27555903938157, 16.857597336979865, -10.001126091425167],
                [-12.077402602164874, 2.7674664872463826, -11.473187085269426],
                [-14.27555903938157, 16.857597336979865, -10.001126091425167],
                [-15.571352906593518, 16.671010427016856, -11.333799457174825],
                [-13.373196469376804, 2.5808795772834046, -12.805860451019084]
            ],
            'knot': [float(i) for i in range(17)]},

        'pyramidl': {
            'degree': 1,
            'point': [[1, 0, 1], [-1, 0, 1], [-1, 0, -1], [1, 0, -1], [1, 0, 1], [0, 2, 0], [1, 0, 1], [-1, 0, 1],
                      [0, 2, 0], [-1, 0, -1], [0, 2, 0], [1, 0, -1], [0, 2, 0]],
            'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        },
        'pyramidr': {
            'degree': 1,
            'point': [[1, 0, 1], [-1, 0, 1], [-1, 0, -1], [1, 0, -1], [1, 0, 1], [0, -2, 0], [1, 0, 1], [-1, 0, 1],
                      [0, -2, 0], [-1, 0, -1], [0, -2, 0], [1, 0, -1], [0, -2, 0]],
            'knot': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        },

        'clavicleL': {
            'degree': 1,
            'point': [[-1.7430770550733623, -3.3990209831111793, 5.423020977367101],
                      [-3.747160706151803, -3.4494778571300726, 7.9330461594762935],
                      [-1.236651588321227, -3.503550688084539, 9.936429220630608],
                      [0.7674320627572127, -3.453093814065644, 7.426404038521409],
                      [-1.7430770550733623, -3.3990209831111793, 5.423020977367101],
                      [0.0, 0.0, 0.0], [17.599136509119166, -11.14489906377664, -18.277790842991823],
                      [17.677797662270173, -11.305291073596377, -21.251458209383106],
                      [20.59910722500327, -11.878747678161506, -21.143251272755705],
                      [20.520446071852284, -11.718355668341689, -18.169583906364426],
                      [17.599136509119166, -11.14489906377664, -18.277790842991823],
                      [19.50800671725651, -9.447842665434703, -19.811030840220493],
                      [20.59910722500327, -11.878747678161506, -21.143251272755705],
                      [18.690237016865932, -13.575804076503394, -19.610011275527032],
                      [17.599136509119166, -11.14489906377664, -18.277790842991823],
                      [0.0, 0.0, 0.0], [-1.7430770550733623, -3.3990209831111793, 5.423020977367101],
                      [-1.482239354564638, -1.1804210417038317, 7.731462353156961],
                      [-1.236651588321227, -3.503550688084539, 9.936429220630608],
                      [-1.4974892888299558, -5.722150629491884, 7.62798784484074],
                      [-1.7430770550733623, -3.3990209831111793, 5.423020977367101],
                      [0.7674320627572127, -3.453093814065644, 7.426404038521409],
                      [-1.482239354564638, -1.1804210417038317, 7.731462353156961],
                      [-3.747160706151803, -3.4494778571300726, 7.9330461594762935],
                      [-1.4974892888299558, -5.722150629491884, 7.62798784484074],
                      [0.7674320627572127, -3.453093814065644, 7.426404038521409],
                      [-1.7430770550733623, -3.3990209831111793, 5.423020977367101],
                      [0.0, 0.0, 0.0], [17.599136509119166, -11.14489906377664, -18.277790842991823],
                      [20.520446071852284, -11.718355668341689, -18.169583906364426],
                      [18.690237016865932, -13.575804076503394, -19.610011275527032],
                      [17.677797662270173, -11.305291073596377, -21.251458209383106],
                      [19.50800671725651, -9.447842665434703, -19.811030840220493],
                      [20.520446071852284, -11.718355668341689, -18.169583906364426]],
            'knot': [float(i) for i in range(34)]},

        'clavicleR': {'degree': 1,
                     'point': [[1.743, 3.399, -5.423], [3.747, 3.45, -7.933], [1.237, 3.504, -9.936],
                               [-0.767, 3.453, -7.426], [1.743, 3.399, -5.423], [0.0, 0.0, -0.0],
                               [-17.599, 11.145, 18.278], [-17.678, 11.305, 21.251], [-20.599, 11.879, 21.143],
                               [-20.52, 11.718, 18.17], [-17.599, 11.145, 18.278], [-19.508, 9.448, 19.811],
                               [-20.599, 11.879, 21.143], [-18.69, 13.576, 19.61], [-17.599, 11.145, 18.278],
                               [0.0, 0.0, -0.0], [1.743, 3.399, -5.423], [1.482, 1.18, -7.731], [1.237, 3.504, -9.936],
                               [1.497, 5.722, -7.628], [1.743, 3.399, -5.423], [-0.767, 3.453, -7.426],
                               [1.482, 1.18, -7.731], [3.747, 3.45, -7.933], [1.497, 5.722, -7.628],
                               [-0.767, 3.453, -7.426], [1.743, 3.399, -5.423], [0.0, 0.0, -0.0],
                               [-17.599, 11.145, 18.278], [-20.52, 11.718, 18.17], [-18.69, 13.576, 19.61],
                               [-17.678, 11.305, 21.251], [-19.508, 9.448, 19.811], [-20.52, 11.718, 18.17]],
                     'knot': [float(i) for i in range(34)]},

        'ankle': {
                    'degree': 1,  # 1 次 B 样条（线性插值，即多段线）
                    'point': [
                        [6.754, 2.008, 6.877], [6.754, 2.008, -6.39], [-6.754, 2.008, -6.39], [-6.754, 2.008, 6.877],
                        [6.754, 2.008, 6.877], [6.754, -7.158, 23.239], [-6.754, -7.158, 23.239], [-6.754, 2.008, 6.877],
                        [6.754, 2.008, 6.877], [6.754, 2.008, -6.39], [6.754, -11.423, -7.246], [-6.754, -11.423, -7.246],
                        [-6.754, 2.008, -6.39], [6.754, 2.008, -6.39], [6.754, -11.423, -7.246], [6.754, -11.423, 23.239],
                        [-6.754, -11.423, 23.239], [-6.754, -11.423, -7.246], [6.754, -11.423, -7.246], [6.754, -11.423, 23.239],
                        [6.754, -7.158, 23.239], [-6.754, -7.158, 23.239], [-6.754, -11.423, 23.239], [6.754, -11.423, 23.239]
                    ],
                    'knot': [float(i) for i in range(24)]},


        'circleY': 'circleY',
        'circleX': 'circleX'
    },
    'color': {
        'm': [17, 25],  # 中间控制器的颜色
        'l': [6, 15],  # 左侧控制器的颜色
        'r': [13, 4]  # 右侧控制器的颜色
    }
}
DEFAULT_LOCK_HIDE_ATTRS = ['visibility']


# 添加属性函数
def add_attribute(node, attr, config):
    if not cmds.attributeQuery(attr, node=node, exists=True):
        if config["type"] == "enum":
            cmds.addAttr(node, longName=attr, attributeType='enum', enumName=config["options"],
                         defaultValue=config["default"], keyable=True)
        else:
            cmds.addAttr(node, longName=attr, attributeType='bool', defaultValue=config["default"], keyable=True)
    else:
        print(f"属性 {attr} 已存在，跳过添加。")


def scale_controller_shape(ctrl, scale_factor):
    """
    放大控制器的形状点，而不改变其 scale 属性

    Args:
        ctrl (str): 控制器的名称
        scale_factor (float): 放大倍数
    """
    shapes = cmds.listRelatives(ctrl, shapes=True)
    if not shapes:
        print(f"Warning: No shape found for controller {ctrl}.")
        return

    for shape in shapes:
        points = cmds.getAttr(f"{shape}.cv[*]")
        for i in range(len(points)):
            cmds.xform(f"{shape}.cv[{i}]", relative=True, scale=(scale_factor, scale_factor, scale_factor))


def create_curve(ctrl_name, shape):
    """
    创建曲线并返回曲线节点

    Args:
        ctrl_name (str): 控制器的名称
        shape (str): 控制器的形状

    Returns:
        str: 创建的曲线节点
    """
    if shape == 'circleY':
        # 使用circle命令创建圆形
        circle = cmds.circle(name=ctrl_name, normal=(0, 1, 0), radius=1)[0]
        return circle
    elif shape == 'circleX':
        circle = cmds.circle(name=ctrl_name, normal=(1, 0, 0), radius=1)[0]
        return circle
    else:
        curve_info = CTRL_INFO['shape'][shape]
        return cmds.curve(degree=curve_info['degree'], point=curve_info['point'], knot=curve_info['knot'],
                          name=ctrl_name)



def create_hierarchy_nodes(ctrl_name):
    """
    创建控制器的层级节点并返回节点列表

    Args:
        ctrl_name (str): 控制器的名称

    Returns:
        list: 创建的层级节点列表
    """
    nodes = []
    for node_type in ['zero', 'driven', 'space', 'connect', 'offset', 'output']:
        node_name = ctrl_name.replace('ctrl', node_type)
        cmds.createNode('transform', name=node_name)
        nodes.append(node_name)
    return nodes


def setup_sub_controller(ctrl, ctrl_nodes):
    """
    设置子控制器并连接到输出节点

    Args:
        ctrl (str): 主控制器的名称
        ctrl_nodes (list): 层级节点列表
    """
    # 创建子控制器
    sub_ctrl = cmds.duplicate(ctrl, name=ctrl + 'Sub')[0]
    cmds.setAttr(sub_ctrl + '.scale', 0.9, 0.9, 0.9)
    cmds.makeIdentity(sub_ctrl, apply=True, translate=True, rotate=True, scale=True)

    # 调整层级关系
    # sub_ctrl 是 ctrl 的子物体
    cmds.parent(sub_ctrl, ctrl)
    # output 是 sub_ctrl 的子物体
    cmds.parent(ctrl_nodes[5], sub_ctrl)

    # 连接属性
    for attr in ['translate', 'rotate', 'rotateOrder']:
        cmds.connectAttr(f'{sub_ctrl}.{attr}', f'{ctrl_nodes[5]}.{attr}')

    # 添加子控制器可见性属性
    cmds.addAttr(ctrl, longName='subCtrlVis', attributeType='bool', keyable=False)
    cmds.setAttr(ctrl + '.subCtrlVis', channelBox=True)
    cmds.connectAttr(ctrl + '.subCtrlVis', sub_ctrl + '.visibility')


def set_controller_color(ctrl_shape, sub_ctrl_shape=None, side='l'):
    """
    设置控制器和子控制器的颜色

    Args:
        ctrl_shape (str): 主控制器的形状节点
        sub_ctrl_shape (str): 子控制器的形状节点
        side (str): 控制器的侧边标识
    """
    ctrl_color, sub_ctrl_color = CTRL_INFO['color'][side]
    cmds.setAttr(ctrl_shape + '.overrideEnabled', 1)
    cmds.setAttr(ctrl_shape + '.overrideColor', ctrl_color)
    if sub_ctrl_shape:
        cmds.setAttr(sub_ctrl_shape + '.overrideEnabled', 1)
        cmds.setAttr(sub_ctrl_shape + '.overrideColor', sub_ctrl_color)


def create_control(description, side='m', index=1, pos=None, parent=None, lock_hide=None, rotate_order=0,
                   shape='square', size=1, match_type=None, match_target=None, scale_factor=1.0):
    """
    创建控制器

    Args:
        description (str): 控制器的描述名称
        side (str): 控制器的侧边标识（'m'中间, 'l'左侧, 'r'右侧）
        index (int): 控制器的索引号
        pos (str/list): 控制器的位置，可以是变换节点的名称，也可以是位置值
        parent (str): 控制器的父节点
        lock_hide (list): 需要锁定和隐藏的属性
        rotate_order (int): 默认的旋转顺序
        shape (str): 控制器的形状
        size (float): 控制器的大小
        match_type (str): 匹配类型，'position' 仅匹配位置，'transform' 匹配位置和旋转
        match_target (str): 匹配的目标物体名称
        scale_factor (float): 控制器形状点的放大倍数

    Returns:
        str: 控制器的名称
    """
    ctrl_name = f'ctrl_{side}_{description}_{index:03d}'
    ctrl = create_curve(ctrl_name, shape)
    ctrl_shape = cmds.listRelatives(ctrl, shapes=True)[0]
    ctrl_shape = cmds.rename(ctrl_shape, ctrl + 'Shape')

    cmds.setAttr(ctrl + '.scale', size, size, size)
    cmds.makeIdentity(ctrl, apply=True, translate=True, rotate=True, scale=True)

    ctrl_nodes = create_hierarchy_nodes(ctrl_name)
    for i in range(1, len(ctrl_nodes)):
        cmds.parent(ctrl_nodes[i], ctrl_nodes[i - 1])
    cmds.parent(ctrl, ctrl_nodes[4])

    setup_sub_controller(ctrl, ctrl_nodes)

    if parent:
        cmds.parent(ctrl_nodes[0], parent)

    if pos:
        if isinstance(pos, str):
            cmds.matchTransform(ctrl_nodes[0], pos, position=True, rotation=True)
        else:
            if len(pos) >= 1:
                cmds.xform(ctrl_nodes[0], translation=pos[0], worldSpace=True)
            if len(pos) >= 2:
                cmds.xform(ctrl_nodes[0], rotation=pos[1], worldSpace=True)

    if match_target and match_type:
        if match_type == 'position':
            cmds.matchTransform(ctrl_nodes[0], match_target, position=True, rotation=False)
        elif match_type == 'transform':
            cmds.matchTransform(ctrl_nodes[0], match_target, position=True, rotation=True)
        else:
            print("Warning: Invalid match_type. Use 'position' or 'transform'.")

    cmds.setAttr(ctrl + '.rotateOrder', rotate_order, channelBox=True)
    cmds.setAttr(f'{ctrl}Sub.rotateOrder', rotate_order, channelBox=True)

    lock_hide_attrs = DEFAULT_LOCK_HIDE_ATTRS + (lock_hide if lock_hide else [])
    for attr in lock_hide_attrs:
        cmds.setAttr(f'{ctrl}.{attr}', keyable=False, lock=True, channelBox=False)
        cmds.setAttr(f'{ctrl}Sub.{attr}', keyable=False, lock=True, channelBox=False)

    sub_ctrl_shape = cmds.listRelatives(f'{ctrl}Sub', shapes=True)[0]
    set_controller_color(ctrl_shape, sub_ctrl_shape, side)

    if scale_factor != 1.0:
        scale_controller_shape(ctrl, scale_factor)
        scale_controller_shape(f'{ctrl}Sub', scale_factor)

    cmds.parent(ctrl_nodes[5], f'{ctrl}')

    return ctrl


def create_spine_ik(joint_list, curve_name_input, ik_handle_name_input, start_joint_input, end_joint_input,
                    new_joint_1_name_input, new_joint_2_name_input):
    """
    创建脊柱的 Spline IK 控制系统

    :param joint_list: 关节名称列表
    :param curve_name_input: 创建的曲线名称
    :param ik_handle_name_input: IK 控制柄名称
    :param start_joint_input: 起始关节名称
    :param end_joint_input: 结束关节名称
    :param new_joint_1_name_input: 新关节1名称
    :param new_joint_2_name_input: 新关节2名称
    :return: 创建的 Skin Cluster 名称
    """
    # 创建 Spline IK 并让命令自动创建曲线
    ik_handle, effector, curve = cmds.ikHandle(
        name=ik_handle_name_input,
        solver='ikSplineSolver',  # 使用 Spline IK 解算器
        startJoint=start_joint_input,  # 起始关节
        endEffector=end_joint_input,  # 结束关节
        createCurve=True,  # 让 ikHandle 自动创建曲线
        parentCurve=False  # 不将曲线父化到任何对象
    )

    # 重命名自动创建的曲线
    curve = cmds.rename(curve, curve_name_input)

    # 创建两个新关节，并确保它们在世界层级下
    new_joint_1 = cmds.joint(name=new_joint_1_name_input)
    new_joint_2 = cmds.joint(name=new_joint_2_name_input)
    cmds.parent(new_joint_1, world=True)
    cmds.parent(new_joint_2, world=True)

    # 将新关节的位移和旋转匹配到原始关节
    cmds.matchTransform(new_joint_1, start_joint_input, position=True, rotation=True)
    cmds.matchTransform(new_joint_2, end_joint_input, position=True, rotation=True)

    # 选择新关节和曲线
    cmds.select([new_joint_1, new_joint_2, curve_name_input], replace=True)

    # 创建 Skin Cluster
    skin_cluster = cmds.skinCluster(
        [new_joint_1, new_joint_2, curve_name_input],  # 显式传递选择的关节和曲线
        bindMethod=0,  # Closest distance
        skinMethod=0,  # Classic linear
        normalizeWeights=1,  # Interactive
        weightDistribution=0,  # Distance
        maximumInfluences=3,  # Max influences
        removeUnusedInfluence=False,
        includeHiddenSelections=False
    )

    # 输出结果
    print(f"Spline IK 系统已创建:")
    print(f"IK 控制柄: {ik_handle}")
    print(f"曲线: {curve}")
    print(f"Skin Cluster: {skin_cluster}")
    return skin_cluster


def duplicate_joint_chain(original_joints, suffix):
    """复制关节链并添加指定后缀"""
    new_chain = []

    # 先复制所有关节（不保持父子关系）
    for jnt in original_joints:
        new_name = jnt.replace("_001", f"{suffix}_001")
        new_jnt = cmds.duplicate(jnt, name=new_name, parentOnly=True)[0]
        new_chain.append(new_jnt)

    # 重建父子关系
    for parent, child in zip(new_chain, new_chain[1:]):
        cmds.parent(child, parent)

    # 重置旋转值
    for jnt in new_chain:
        cmds.setAttr(f"{jnt}.rotate", 0, 0, 0)

    # 取消整个链的父级关系（相当于shift+p）
    if new_chain:
        cmds.parent(new_chain[0], world=True)

    return new_chain


def create_fk_chain(joint_chain, ctrl_shape='square', ctrl_size=1.0):
    """
    为关节链创建FK控制器系统

    参数:
        joint_chain (list): 关节名称列表，按层级顺序排列
        ctrl_shape (str): 控制器形状，默认为'square'
        ctrl_size (float): 控制器大小，默认为1.0
    """
    if not joint_chain:
        cmds.warning("警告：未提供有效的关节链")
        return

    # 存储所有创建的控制器
    created_ctrls = []

    for i, joint in enumerate(joint_chain):
        # 从关节名称提取description和side
        parts = joint.split('_')
        if len(parts) < 3:
            cmds.warning(f"警告：关节名称格式不正确 {joint}")
            continue

        side = parts[1]  # 获取侧边标识 (l/r/m)
        description = parts[2] # 构建description

        # 创建FK控制器
        ctrl = create_control(
            description=description,
            side=side,
            index=i + 1,  # 从1开始编号
            shape=ctrl_shape,
            size=ctrl_size,
            match_type='transform',  # 匹配位置和旋转
            match_target=joint  # 匹配到当前关节
        )

        # 获取控制器的output节点（约束用）
        output_node = ctrl.replace('ctrl', 'output')

        # 对关节进行父子约束
        cmds.orientConstraint(output_node, joint, maintainOffset=False)

        # 如果是第一个控制器，只记录不处理层级
        if i == 0:
            created_ctrls.append(ctrl)
            continue

        # 从第二个控制器开始，处理层级关系
        prev_output = created_ctrls[-1].replace('ctrl', 'output')
        current_zero = ctrl.replace('ctrl', 'zero')

        # 将当前控制器的zero组放到上一个控制器的output组下
        cmds.parent(current_zero, prev_output)

        created_ctrls.append(ctrl)

    cmds.select(clear=True)
    print(f"FK绑定完成，共创建 {len(created_ctrls)} 个控制器")

def create_ik_with_pole_vector(
        start_joint,
        mid_joint,
        end_joint,
        axis="-z",
        pole_loc_name="loc_ikGuide",
        ik_handle_name="ctrl_ikHandle",
        pole_distance=None
):
    """创建带有极向量约束的IK系统

    参数:
        start_joint (str): IK链起始关节名称
        mid_joint (str): 极向量参考关节（通常为肘/膝关节）
        end_joint (str): IK链结束关节名称
        axis (str): 极向量轴向（格式: +/-轴，如"-z","+y"），默认为"-z"
        pole_loc_name (str): 极向量定位器名称
        ik_handle_name (str): IK手柄名称
        pole_distance (float): 极向量延伸距离（None时自动计算）

    返回:
        tuple: (极向量定位器名称, IK手柄名称)
    """

    # 解析轴向参数
    axis_direction = 1
    if axis.startswith("-"):
        axis_direction = -1
        axis = axis[1:]
    axis = axis.lower()

    # 验证轴向有效性
    axis_index_map = {"x": 0, "y": 4, "z": 8}
    if axis not in axis_index_map:
        raise ValueError("无效轴向，请输入x/y/z")

    # 获取关节位置
    start_pos = cmds.xform(start_joint, q=True, t=True, ws=True)
    mid_pos = cmds.xform(mid_joint, q=True, t=True, ws=True)

    # 计算默认延伸距离（起始关节到中间关节的距离）
    if pole_distance is None:
        dx = start_pos[0] - mid_pos[0]
        dy = start_pos[1] - mid_pos[1]
        dz = start_pos[2] - mid_pos[2]
        pole_distance = math.sqrt(dx ** 2 + dy ** 2 + dz ** 2)

    # 获取中间关节的坐标系方向
    matrix = cmds.getAttr(f"{mid_joint}.worldMatrix")  # 获取完整世界矩阵
    axis_start = axis_index_map[axis]

    # 提取轴向向量并应用方向
    axis_vector = [
        matrix[axis_start] * axis_direction,
        matrix[axis_start + 1] * axis_direction,
        matrix[axis_start + 2] * axis_direction
    ]

    # 标准化向量
    vector_length = math.sqrt(sum(v ** 2 for v in axis_vector))
    if vector_length > 0:
        normalized = [v / vector_length for v in axis_vector]
    else:
        normalized = [0, 0, 0]

    # 计算极向量最终位置
    pole_position = [
        mid_pos[0] + normalized[0] * pole_distance,
        mid_pos[1] + normalized[1] * pole_distance,
        mid_pos[2] + normalized[2] * pole_distance
    ]

    # 创建定位器
    pole_loc = cmds.spaceLocator(name=pole_loc_name)[0]
    cmds.xform(pole_loc, t=pole_position, ws=True)

    # 创建IK手柄
    ik_handle, _ = cmds.ikHandle(
        startJoint=start_joint,
        endEffector=end_joint,
        solver="ikRPsolver",
        createCurve=False,
        name=ik_handle_name
    )
    return pole_loc, ik_handle

def create_connection_line(source, target, site, side="l"):
    # 创建两个定位器，使用side参数
    locator1 = cmds.spaceLocator(name=f"loc_{side}_{site}IkGuide_001")[0]
    locator2 = cmds.spaceLocator(name=f"loc_{side}_{site}IkGuide_002")[0]

    # 将定位器匹配到源和目标对象
    cmds.matchTransform(locator2, target, pos=True, rot=True)
    cmds.matchTransform(locator1, source, pos=True, rot=True)
    cmds.parent(locator2, target)
    cmds.parent(locator1, f"output_{side}_{site}IkGuide_001")

    # 创建一条直线（使用curve命令创建一条线性曲线）
    line = cmds.curve(p=[(0, 0, 0), (0, 0, 0.1)], degree=1, name=f"crv_{side}_{site}IkGuide_001")

    # 获取并重命名形状节点
    line_shapes = cmds.listRelatives(line, shapes=True)
    if line_shapes:
        line_shape = cmds.rename(line_shapes[0], f"crv_{side}_{site}IkGuide_001Shape")
        cmds.setAttr(line_shape + '.overrideEnabled', 1)
        cmds.setAttr(line_shape + '.overrideDisplayType', 2)

    # 连接定位器的世界位置到曲线的控制点
    line_shape = cmds.listRelatives(line, shapes=True)[0]  # 再次获取确保使用正确的名称

    # 连接控制点
    cmds.connectAttr(f"{locator1}.worldPosition[0]", f"{line_shape}.controlPoints[0]")
    cmds.connectAttr(f"{locator2}.worldPosition[0]", f"{line_shape}.controlPoints[1]")

    return {
        "line": line,
        "source_locator": locator1,
        "target_locator": locator2
    }


def create_hand_ik_system(
        start_joint,
        mid_joint,
        end_joint,
        wrist_end_joint,
        side="l",
        axis="-z",
        pole_loc_name="elbowIkGuide",
        ik_handle_name="armIk",
        hand_ctrl_name="handIk",
        pole_distance=None
):
    """创建完整的手部IK系统，包括极向量IK和手部IK

    参数:
        start_joint (str): 手臂IK起始关节(上臂)
        mid_joint (str): 肘部关节(用于极向量)
        end_joint (str): 手腕关节(手臂IK结束关节)
        wrist_end_joint (str): 手腕末端关节(手部IK结束关节)
        side (str): 身体侧("l"或"r")
        axis (str): 极向量轴向(如"-z")
        pole_loc_name (str): 极向量定位器基础名称
        ik_handle_name (str): IK手柄基础名称
        hand_ctrl_name (str): 手部控制器基础名称
        pole_distance (float): 极向量延伸距离(None为自动计算)

    返回:
        dict: 包含所有创建元素的字典
    """

    # 添加侧面前缀
    pole_loc_name = f"loc_{side}_{pole_loc_name}_001"
    ik_handle_name = f"ikHnd_{side}_{ik_handle_name}_001"
    hand_ctrl_name = f"ctrl_{side}_{hand_ctrl_name}_001"

    # 1. 创建手臂极向量IK系统
    pole_loc, arm_ik_handle = create_ik_with_pole_vector(
        start_joint=start_joint,
        mid_joint=mid_joint,
        end_joint=end_joint,
        axis=axis,
        pole_loc_name=pole_loc_name,
        ik_handle_name=ik_handle_name,
        pole_distance=pole_distance
    )

    # 2. 创建肘部控制器
    create_control(
        description='elbowIkGuide',
        side=side,
        shape='cube',
        size=1,
        match_type='transform',
        match_target=pole_loc,
        scale_factor=2
    )

    # 3. 组织层级
    output_pole = f"output_{side}_elbowIkGuide_001"
    cmds.delete(pole_loc)

    # 4. 添加极向量约束
    cmds.poleVectorConstraint(output_pole, arm_ik_handle)

    # 5. 创建手部控制器
    cmds.joint(name=f"ctrl_{side}_handIk_001")
    cmds.matchTransform(f"ctrl_{side}_handIk_001", f"jnt_{side}_wristFk_001", position=True, rotation=True)
    cmds.makeIdentity(f"ctrl_{side}_handIk_001", apply=True, translate=True, rotate=True, scale=True)

    # 6. 创建手部控制器形状
    create_curve('cube1', 'cube')
    scale_controller_shape('cube1', 10)

    # 7. 组织手部控制器层级
    zero_hand = f"zero_{side}_handIk_001"
    cmds.group(em=True, name=zero_hand)
    cmds.matchTransform(zero_hand, f"ctrl_{side}_handIk_001", position=True, rotation=True)
    cmds.parent(f"ctrl_{side}_handIk_001", zero_hand)

    # 8. 添加形状到控制器
    cmds.parent('curveShape1', f"ctrl_{side}_handIk_001", shape=True, add=True)
    cmds.rename("curveShape1", f"ctrl_{side}_handIk_001Shape")
    cmds.setAttr(f"ctrl_{side}_handIk_001.drawStyle", 2)
    cmds.delete("cube1")

    # 9. 将手臂IK手柄父级到手部控制器
    cmds.parent(arm_ik_handle, f"ctrl_{side}_handIk_001")

    # 10. 创建手部IK
    hand_ik_handle, _ = cmds.ikHandle(
        name=f"ikHnd_{side}_handIk_001",
        startJoint=end_joint,
        endEffector=wrist_end_joint,
        solver='ikSCsolver',
        sticky='sticky'
    )

    # 11. 将手部IK父级到手部控制器
    cmds.parent(hand_ik_handle, f"ctrl_{side}_handIk_001")

    # 12. 创建肘部连接线
    source_obj = f"ctrl_{side}_elbowIkGuide_001"
    target_obj = f"jnt_{side}_elbowIk_001"

    connection_result = create_connection_line(source_obj, target_obj,'elbow', side=side)
    cmds.hide(f"loc_{side}_elbowIkGuide_001")
    cmds.hide(f"loc_{side}_elbowIkGuide_002")

    # 返回所有创建的对象
    return {
        'arm_ik_handle': arm_ik_handle,
        'hand_ik_handle': hand_ik_handle,
        'hand_controller': f"ctrl_{side}_handIk_001",
        'elbow_controller': source_obj,
        'connection_line': connection_result['line'],
        'pole_locator': pole_loc
    }


def create_leg_ik_system(
        start_joint,
        mid_joint,
        end_joint,
        ball_joint,
        toe_joint,
        side="l",
        axis="-z",
        pole_loc_name="kneeIkGuide",
        ik_handle_name="legIk",
        hand_ctrl_name="ankleIk",
        pole_distance=None
):
    """创建完整的腿部IK系统，包括极向量IK和腿部IK

    参数:
        start_joint (str): 腿部IK起始关节(大腿)
        mid_joint (str): 膝部关节(用于极向量)
        end_joint (str): 脚腕关节(腿部IK结束关节)
        ball_joint (str): 脚腕末端关节(脚腕IK结束关节)
        toe_joint (str):脚趾末端关节(脚趾IK结束关节)
        side (str): 身体侧("l"或"r")
        axis (str): 极向量轴向(如"-z")
        pole_loc_name (str): 极向量定位器基础名称
        ik_handle_name (str): IK手柄基础名称
        hand_ctrl_name (str): 手部控制器基础名称
        pole_distance (float): 极向量延伸距离(None为自动计算)

    返回:
        dict: 包含所有创建元素的字典
    """

    # 添加侧面前缀
    pole_loc_name = f"loc_{side}_{pole_loc_name}_001"
    ik_handle_name = f"ikHnd_{side}_{ik_handle_name}_001"
    hand_ctrl_name = f"ctrl_{side}_{hand_ctrl_name}_001"

    # 1. 创建腿部极向量IK系统
    pole_loc, leg_ik_handle = create_ik_with_pole_vector(
        start_joint=start_joint,
        mid_joint=mid_joint,
        end_joint=end_joint,
        axis=axis,
        pole_loc_name=pole_loc_name,
        ik_handle_name=ik_handle_name,
        pole_distance=pole_distance
    )

    # 2. 创建膝盖控制器
    create_control(
        description='kneeIkGuide',
        side=side,
        shape='cube',
        size=1,
        match_type='transform',
        match_target=pole_loc,
        scale_factor=2
    )

    # 3. 组织层级
    output_pole = f"output_{side}_kneeIkGuide_001"
    cmds.delete(pole_loc)

    # 4. 添加极向量约束
    cmds.poleVectorConstraint(output_pole, leg_ik_handle)

    # 5. 创建脚踝控制器
    cmds.joint(name=f"ctrl_{side}_ankleIk_001")
    cmds.matchTransform(f"ctrl_{side}_ankleIk_001", f"jnt_{side}_ankleIk_001", position=True, rotation=False)
    locator1 = cmds.spaceLocator(name="locator1")[0]
    locator2 = cmds.spaceLocator(name="locator2")[0]
    cmds.matchTransform(locator1, f"ctrl_{side}_ankleIk_001")
    cmds.move(0, 30, 0, "locator1", relative=True, objectSpace=True)
    cmds.matchTransform(locator2, f"jnt_{side}_toeEndIk_001", position=True, rotation=False)
    constraint = cmds.aimConstraint(
        "locator1",  # 目标物体
        f"ctrl_{side}_ankleIk_001",  # 被约束物体
        aimVector=(0, 1, 0),  # Aim 朝向 Y 轴
        upVector=(0, 0, 1),  # Up 朝向 Z 轴
        worldUpType="object",  # 使用物体作为上方向参考
        worldUpObject="locator2"  # 指定 locator2 为 Up 物体
    )
    constraints = cmds.listConnections(f"ctrl_{side}_ankleIk_001", type="aimConstraint") or []
    cmds.delete(constraints)
    cmds.delete(locator1)
    cmds.delete(locator2)


    cmds.makeIdentity(f"ctrl_{side}_ankleIk_001", apply=True, translate=True, rotate=True, scale=True)

    # 6. 创建脚踝控制器形状
    create_curve('cube1', 'ankle')

    # 7. 组织脚踝控制器层级
    zero_ankle = f"zero_{side}_ankleIk_001"
    cmds.group(em=True, name=zero_ankle)
    cmds.matchTransform(zero_ankle, f"ctrl_{side}_ankleIk_001", position=True, rotation=True)
    cmds.parent(f"ctrl_{side}_ankleIk_001", zero_ankle)

    # 8. 添加形状到控制器
    cmds.parent('curveShape1', f"ctrl_{side}_ankleIk_001", shape=True, add=True)
    cmds.rename("curveShape1", f"ctrl_{side}_ankleIk_001Shape")
    cmds.setAttr(f"ctrl_{side}_ankleIk_001.drawStyle", 2)
    cmds.delete("cube1")
    cmds.parent(leg_ik_handle, f"ctrl_{side}_ankleIk_001")
    set_controller_color(f"ctrl_{side}_ankleIk_001", side=side)

    # 10. 创建脚踝IK
    ball_ik_handle, _ = cmds.ikHandle(
        name=f"ikHnd_{side}_ballIk_001",
        startJoint=end_joint,
        endEffector=ball_joint,
        solver='ikSCsolver',
        sticky='sticky'
    )

    toe_ik_handle, _ = cmds.ikHandle(
        name=f"ikHnd_{side}_toeIk_001",
        startJoint=ball_joint,
        endEffector=toe_joint,
        solver='ikSCsolver',
        sticky='sticky'
    )

    # 12. 创建膝盖连接线
    source_obj = f"ctrl_{side}_kneeIkGuide_001"
    target_obj = f"jnt_{side}_kneeIk_001"

    connection_result = create_connection_line(source_obj, target_obj, 'knee', side=side)
    cmds.hide(f"loc_{side}_kneeIkGuide_001")
    cmds.hide(f"loc_{side}_kneeIkGuide_002")

    # 返回所有创建的对象
    return {
        'leg_ik_handle': leg_ik_handle,
        'ball_ik_handle': ball_ik_handle,
        'hand_controller': f"ctrl_{side}_ankleIk_001",
        'knee_controller': source_obj,
        'connection_line': connection_result['line'],
        'pole_locator': pole_loc
    }

def setup_ik_fk_switch(side='l'):
    """
    设置IK/FK切换系统
    :param side: 身体侧边 ('l' 或 'r')
    """
    # 验证输入参数
    if side not in ['l', 'r']:
        raise ValueError("side参数必须是'l'或'r'")

    # 定义关节链结构
    base_chains = {
        "arm": [
            f"jnt_{side}_upperArm_001",
            f"jnt_{side}_elbow_001",
            f"jnt_{side}_wrist_001",
            f"jnt_{side}_wristEnd_001"
        ],
        "leg": [
            f"jnt_{side}_upperLeg_001",
            f"jnt_{side}_knee_001",
            f"jnt_{side}_ankle_001",
            f"jnt_{side}_ball_001",
            f"jnt_{side}_toeEnd_001"
        ]
    }

    # 定义每个链类型的可见性控制映射
    visibility_controls = {
        "arm": {
            "fk": f"zero_{side}_upperArmFk_001.visibility",
            "ik": [
                f"zero_{side}_handIk_001.visibility",
                f"zero_{side}_elbowIkGuide_001.visibility",
                f"crv_{side}_elbowIkGuide_001.visibility"
            ]
        },
        "leg": {
            "fk": f"zero_{side}_upperLegFk_001.visibility",
            "ik": [
                f"zero_{side}_ankleIk_001.visibility",
                f"zero_{side}_kneeIkGuide_001.visibility",
                f"crv_{side}_kneeIkGuide_001.visibility"
            ]
        }
    }

    for chain_type, joints in base_chains.items():
        # 获取IK/FK混合控制器
        ctrl_name = f"ctrl_{side}_{chain_type}IkFkBlend_001"

        # 检查控制器是否存在
        if not cmds.objExists(ctrl_name):
            cmds.warning(f"控制器 {ctrl_name} 不存在，跳过 {chain_type} 链设置")
            continue

        # 创建反向节点
        rev_node = cmds.createNode("reverse", name=f"rvs_{side}_{chain_type}IkFkBlend_001")
        cmds.connectAttr(f"{ctrl_name}.ikFkBlend", f"{rev_node}.inputX")

        # 设置可见性控制
        # FK可见性
        if cmds.objExists(visibility_controls[chain_type]["fk"]):
            cmds.connectAttr(f"{ctrl_name}.ikFkBlend", visibility_controls[chain_type]["fk"])

        # IK可见性
        for ik_vis in visibility_controls[chain_type]["ik"]:
            if cmds.objExists(ik_vis):
                cmds.connectAttr(f"{rev_node}.outputX", ik_vis)

        # 设置关节约束
        for jnt in joints:
            # 检查基础关节是否存在
            if not cmds.objExists(jnt):
                cmds.warning(f"基础关节 {jnt} 不存在，跳过")
                continue

            # 生成IK和FK关节名称
            jnt_ik = jnt.replace("_001", "Ik_001")
            jnt_fk = jnt.replace("_001", "Fk_001")

            # 检查IK/FK关节是否存在
            if not cmds.objExists(jnt_ik) or not cmds.objExists(jnt_fk):
                cmds.warning(f"IK/FK关节 {jnt_ik} 或 {jnt_fk} 不存在，跳过")
                continue

            # 创建旋转约束
            constraint = cmds.orientConstraint(jnt_ik, jnt_fk, jnt, maintainOffset=False, name=f"oc_{jnt}_ikfk")[0]
            cmds.setAttr(f"{constraint}.interpType", 2)  # 设置为最短路径插值

            # 连接权重
            cmds.connectAttr(f"{ctrl_name}.ikFkBlend", f"{constraint}.{jnt_fk}W1")
            cmds.connectAttr(f"{rev_node}.outputX", f"{constraint}.{jnt_ik}W0")

def orient_joint_chain(root_joint, orient_order="xyz", secondary_axis_orient="yup"):
    """
    定向整个关节链，从根关节到末端关节

    参数:
        root_joint: 关节链的根关节名称
        orient_order: 轴向顺序 (如 "xyz", "yzx"等)，默认为"xyz"
        secondary_axis_orient: 次轴方向 ("yup", "ydown", "zup", "zdown")，默认为"yup"
    """
    # 验证根关节
    if not cmds.objExists(root_joint) or cmds.objectType(root_joint) != 'joint':
        cmds.warning(f"对象 '{root_joint}' 不存在或不是关节!")
        return

    # 验证参数
    valid_orient_orders = ["xyz", "xzy", "yxz", "yzx", "zxy", "zyx"]
    if orient_order.lower() not in valid_orient_orders:
        cmds.warning(f"无效的轴向顺序 '{orient_order}'! 请使用: {', '.join(valid_orient_orders)}")
        return

    valid_secondary_axis = ["yup", "ydown", "zup", "zdown"]
    if secondary_axis_orient.lower() not in valid_secondary_axis:
        cmds.warning(f"无效的次轴方向 '{secondary_axis_orient}'! 请使用: {', '.join(valid_secondary_axis)}")
        return

    # 获取整个关节链
    joint_chain = get_joint_chain(root_joint)
    if not joint_chain:
        cmds.warning(f"在 '{root_joint}' 下未找到关节链!")
        return

    print(f"定向关节链: {' -> '.join(joint_chain)}")
    print(f"参数: 轴向顺序={orient_order}, 次轴方向={secondary_axis_orient}")

    # 冻结变换（确保骨骼处于初始状态）
    cmds.makeIdentity(joint_chain, apply=True, translate=False, rotate=True, scale=True)

    # 从底部向上定向（确保父关节方向正确）
    for joint in reversed(joint_chain[:-1]):  # 跳过末端关节
        children = cmds.listRelatives(joint, children=True, type='joint') or []

        if children:
            # 定向当前关节
            cmds.joint(
                joint,
                edit=True,
                orientJoint=orient_order,
                secondaryAxisOrient=secondary_axis_orient,
                zeroScaleOrient=True,
                children=True
            )
            print(f"定向关节: {joint}")
        else:
            print(f"警告: 关节 '{joint}' 没有子关节，但不在链末端")

    print("关节链定向完成!")


def get_joint_chain(start_joint):
    """
    从起始关节获取整个关节链

    参数:
        start_joint: 起始关节名称

    返回:
        list: 按层级顺序排列的关节链
    """
    chain = [start_joint]
    current = start_joint

    while True:
        # 获取直接子关节（仅限关节类型）
        children = cmds.listRelatives(current, children=True, type='joint') or []

        if not children:
            break  # 到达链末端

        # 如果有多个子关节，取第一个（假设是主链）
        next_joint = children[0]
        chain.append(next_joint)
        current = next_joint

    return chain

def setup_foot(side='l'):
    # 验证side参数有效性
    if side not in ['l', 'r']:
        raise ValueError("Invalid side parameter. Use 'l' or 'r'.")


    # 创建控制器
    create_control('footInnPivot', side=side, shape=f'pyramid{side}', match_type='transform',
                   match_target=f'jntRvs_{side}_footInnPivot_001')

    create_control('footOutPivot', side=side, shape=f'pyramid{side}', match_type='transform',
                   match_target=f'jntRvs_{side}_footOutPivot_001')

    create_control('toePivot', side=side, shape=f'pyramid{side}', match_type='transform',
                   match_target=f'jntRvs_{side}_toePivot_001')

    create_control('heelPivot', side=side, shape=f'pyramid{side}', match_type='transform',
                   match_target=f'jntRvs_{side}_heelPivot_001')

    create_control('ballIk', side=side, shape='cube', match_type='transform',
                   match_target=f'jntRvs_{side}_ballIk_001', scale_factor=5)

    create_control('toeTapIk', side=side, shape='cube', match_type='transform',
                   match_target=f'jntRvs_{side}_toeTapIk_001', scale_factor=5)

    # 设置层级关系
    cmds.parent(f'zero_{side}_ballIk_001', f'output_{side}_footInnPivot_001')
    cmds.parent(f'zero_{side}_toeTapIk_001', f'output_{side}_footInnPivot_001')
    cmds.parent(f'zero_{side}_footInnPivot_001', f'output_{side}_footOutPivot_001')
    cmds.parent(f'zero_{side}_footOutPivot_001', f'output_{side}_toePivot_001')
    cmds.parent(f'zero_{side}_toePivot_001', f'output_{side}_heelPivot_001')

    cmds.parent(f'ikHnd_{side}_toeIk_001', f'output_{side}_toeTapIk_001')
    cmds.parent(f'ikHnd_{side}_ballIk_001', f'output_{side}_ballIk_001')
    cmds.parent(f'ikHnd_{side}_legIk_001', f'output_{side}_ballIk_001')

    # 清理反向关节
    cmds.delete(f'jntRvs_{side}_heelPivot_001')

    # 添加控制属性
    ctrl_name = f'ctrl_{side}_ankleIk_001'
    cmds.addAttr(ctrl_name, longName='footCtrlDivider', niceName='Foot Ctrl --------',
                 attributeType="bool", keyable=True)

    cmds.addAttr(ctrl_name, longName='toeTap', attributeType="float", keyable=True)
    cmds.addAttr(ctrl_name, longName='ballRoll', attributeType="float", keyable=True)
    cmds.addAttr(ctrl_name, longName='toeRoll', attributeType="float", keyable=True, minValue=0)
    cmds.addAttr(ctrl_name, longName='heelRoll', attributeType="float", keyable=True, minValue=0)
    cmds.addAttr(ctrl_name, longName='toeSlide', attributeType="float", keyable=True)
    cmds.addAttr(ctrl_name, longName='heelSlide', attributeType="float", keyable=True)
    cmds.addAttr(ctrl_name, longName='bend', attributeType="float", keyable=True)

    # 连接属性
    cmds.connectAttr(f'{ctrl_name}.toeTap', f'connect_{side}_toeTapIk_001.rotateZ')
    cmds.connectAttr(f'{ctrl_name}.ballRoll', f'connect_{side}_ballIk_001.rotateZ')
    cmds.connectAttr(f'{ctrl_name}.toeRoll', f'connect_{side}_toePivot_001.rotateZ')
    cmds.connectAttr(f'{ctrl_name}.toeSlide', f'connect_{side}_toePivot_001.rotateY')
    cmds.setAttr(f"connect_{side}_toePivot_001.rotateOrder", 5)

    cmds.connectAttr(f'{ctrl_name}.heelRoll', f'connect_{side}_heelPivot_001.rotateZ')
    cmds.connectAttr(f'{ctrl_name}.heelSlide', f'connect_{side}_heelPivot_001.rotateY')
    cmds.setAttr(f"connect_{side}_heelPivot_001.rotateOrder", 5)

    mult_node = cmds.shadingNode('multiplyDivide', asUtility=True, name=f'mult_{side}_footInnPivotRvs_001')
    cmds.connectAttr(f'{ctrl_name}.bend', f'{mult_node}.input1X')
    cmds.setAttr(f"{mult_node}.input2", -1, -1, -1, type="double3")
    cmds.connectAttr(f'{mult_node}.outputX', f'connect_{side}_footInnPivot_001.rotateZ')
    cmds.connectAttr(f'{ctrl_name}.bend', f'connect_{side}_footOutPivot_001.rotateZ')

    # 设置旋转限制
    cmds.transformLimits(f'connect_{side}_footInnPivot_001', erz=(True, False), rz=(0, 0))
    cmds.transformLimits(f'connect_{side}_footOutPivot_001', erz=(True, False), rz=(0, 0))


# 创建一个顶级空组
master_group = cmds.group(em=True, name='master')
if not cmds.objExists('master'):
    raise ValueError("master组创建失败")

# 遍历属性字典并添加属性
for attr, config in master_attributes.items():
    add_attribute('master', attr, config)

# 锁定并隐藏不需要的属性
all_attributes = cmds.listAttr('master', visible=True, keyable=True, scalar=True) or []
for attr in all_attributes:
    if attr not in master_attributes:
        cmds.setAttr(f'master.{attr}', lock=True, keyable=False, channelBox=False)
        print(f"已锁定并隐藏属性: {attr}")

# 创建组并存储到字典中
group_dict = {group_name: cmds.group(em=True, name=group_name) for group_name in groups}
for group in group_dict.values():
    cmds.parent(group, master_group)

# 启用 geometry 组的 overrideEnabled 属性
cmds.setAttr('geometry.overrideEnabled', 1)

# 整理 master 组
rigNodesLocal_group = cmds.group(em=True, name='rigNodesLocal')
rigNodesWorld_group = cmds.group(em=True, name='rigNodesWorld')
cmds.parent(rigNodesLocal_group, group_dict['rigNodes'])
cmds.parent(rigNodesWorld_group, group_dict['rigNodes'])
cmds.parent('jnt_m_spine_001', group_dict['joints'])

# 用户输入模型组的名称，暂时省略
# resolution_groups = {}
# for resolution in ["Low", "Medium", "High"]:
#     while True:
#         # 使用传统的 cmds.promptDialog 调用方式
#         result = cmds.promptDialog(
#             title=f"输入 {resolution} 分辨率组",
#             message=f"请输入 {resolution} 分辨率模型组的名称：\n\n示例：low_res_group",
#             button=["确认", "取消"],
#             defaultButton="确认",
#             cancelButton="取消",
#             dismissString="取消"
#         )
#
#         if result == "取消":
#             raise ValueError("用户取消了操作。")
#
#         # 获取用户输入的组名称
#         group_name = cmds.promptDialog(query=True, text=True)
#
#         # 检查输入的组是否存在
#         if cmds.objExists(group_name):
#             resolution_groups[resolution] = group_name
#             print(f"{resolution} 分辨率模型组已设置为: {group_name}")
#             break
#         else:
#             cmds.warning(f"组 '{group_name}' 不存在！请重新输入。")

##############################################################################################
# 硬编码生成模型组

resolution_groups = {
    "Low": "grp_m_low_body_001",
    "Medium": "grp_m_mid_body_001",
    "High": "grp_m_high_body_001"
}

# 验证组是否存在
for resolution, group_name in resolution_groups.items():
    if not cmds.objExists(group_name):
        cmds.warning(f"组 '{group_name}' 不存在！请检查场景。")
    else:
        print(f"{resolution} 分辨率模型组已设置为: {group_name}")

##############################################################################################

# 遍历 master_attributes 字典，将 master 的属性连接到对应的组
for attr, config in master_attributes.items():
    if attr == "resolution":
        for i, resolution in enumerate(["Low", "Medium", "High"]):
            target_group = resolution_groups[resolution]
            cmds.parent(target_group, 'geometry')
            condition_node = cmds.createNode('condition', name=f'resolution_{resolution}_condition')
            cmds.setAttr(f'{condition_node}.firstTerm', i)
            cmds.setAttr(f'{condition_node}.secondTerm', i)
            cmds.setAttr(f'{condition_node}.operation', 0)
            cmds.setAttr(f'{condition_node}.colorIfTrueR', 1)
            cmds.setAttr(f'{condition_node}.colorIfFalseR', 0)
            cmds.connectAttr(f'master.resolution', f'{condition_node}.firstTerm')
            cmds.connectAttr(f'{condition_node}.outColorR', f'{target_group}.visibility')
            print(f"已连接属性: master.resolution -> {condition_node}.firstTerm -> {target_group}.visibility")
    else:
        source_attr = f"master.{attr}"
        target_attr = f"{config['target_group']}.{config['target_attribute']}"
        if cmds.objExists(target_attr.split('.')[0]) and cmds.attributeQuery(config['target_attribute'],
                                                                             node=config['target_group'], exists=True):
            cmds.connectAttr(source_attr, target_attr)
            print(f"已连接属性: {source_attr} -> {target_attr}")
        else:
            print(f"目标属性不存在: {target_attr}")

# 创建世界控制器
circle = cmds.circle(name="ctrl_m_world_001", nr=(0, 1, 0), r=65)[0]
cmds.delete(circle, constructionHistory=True)
zero_m_world_group = cmds.group(em=True, name='zero_m_world_001')
cmds.parent(circle, zero_m_world_group)
cmds.parent(zero_m_world_group, group_dict['controls'])

# 世界控制器进行父子与缩放约束
cmds.parentConstraint('|master|controls|zero_m_world_001|ctrl_m_world_001', '|master|rigNodes|rigNodesLocal')
cmds.scaleConstraint('|master|controls|zero_m_world_001|ctrl_m_world_001', '|master|rigNodes|rigNodesLocal')
cmds.parentConstraint('|master|controls|zero_m_world_001|ctrl_m_world_001', '|master|joints')
cmds.scaleConstraint('|master|controls|zero_m_world_001|ctrl_m_world_001', '|master|joints')

# 锁定并隐藏master组的子组的所有属性
for group in groups:
    all_attributes = cmds.listAttr(group, visible=True, keyable=True) or []
    for attr in all_attributes:
        cmds.setAttr(f'{group}.{attr}', lock=True, keyable=False, channelBox=False)

# 胸腔控制器创建

create_control(description='cog', shape='octagon', size=50, match_type='position',
               match_target='|master|joints|jnt_m_spine_001', scale_factor=1)
create_control(description='pelvisIk', shape='cube', size=35, match_type='position',
               match_target='|master|joints|jnt_m_spine_001')
create_control(description='chestIk', shape='cube', size=35, match_type='position',
               match_target='|master|joints|jnt_m_spine_001|jnt_m_spine_002|jnt_m_spine_003'
                            '|jnt_m_spine_004|jnt_m_spine_005')
create_control(description='pelvisLocal', shape='circleY', parent='output_m_pelvisIk_001', size=1, match_type='position',
               match_target='|master|joints|jnt_m_spine_001', scale_factor=25)

create_control(description='spineIkBendA', shape='square', size=1, match_type='position',
               match_target='jnt_m_spine_002', scale_factor=25)
create_control(description='spineIkBendB', shape='square', parent='output_m_spineIkBendA_001', size=1,
               match_type='position', match_target='jnt_m_spine_003', scale_factor=25)
create_control(description='spineIkBendC', shape='square', parent='output_m_spineIkBendB_001', size=1,
               match_type='position', match_target='jnt_m_spine_004', scale_factor=25)

cmds.parent('jnt_l_upperLeg_001', world=True)
cmds.parent('jnt_r_upperLeg_001', world=True)
cmds.parent('jnt_l_clavicle_001', world=True)
cmds.parent('jnt_r_clavicle_001', world=True)



# 胸腔splineIk曲线创建
joints = ['jnt_m_spine_001', 'jnt_m_spine_002', 'jnt_m_spine_003', 'jnt_m_spine_004', 'jnt_m_spine_005',
          'jnt_m_spine_006']
curve_name = 'crv_m_spineIk_001'
ik_handle_name = 'ikHnd_m_spineIk_001'
start_joint = 'jnt_m_spine_001'
end_joint = 'jnt_m_spine_005'
new_joint_1_name = 'jnt_m_pelvisIkCrv_001'
new_joint_2_name = 'jnt_m_chestIkCrv_001'

create_spine_ik(joints, curve_name, ik_handle_name, start_joint, end_joint, new_joint_1_name, new_joint_2_name)

cmds.parent('jnt_l_upperLeg_001', 'jnt_m_spine_001')
cmds.parent('jnt_r_upperLeg_001', 'jnt_m_spine_001')

# 胸腔控制器绑定
# 脊柱Ik关节控制器归位
cmds.parent('jnt_m_pelvisIkCrv_001', 'output_m_pelvisIk_001')
cmds.parent('jnt_m_chestIkCrv_001', 'output_m_chestIk_001')

# 创建用于IK扭转控制的定位器
chestIkTwist = cmds.spaceLocator(name='loc_m_chestIkTwist_001')[0]
pelvisIkTwist = cmds.spaceLocator(name='loc_m_pelvisIkTwist_001')[0]
chestIkTwist_group = cmds.group(em=True, name='zero_m_chestIkTwist_001')
pelvisIkTwist_group = cmds.group(em=True, name='zero_m_pelvisIkTwist_001')
cmds.parent(chestIkTwist, chestIkTwist_group)
cmds.parent(pelvisIkTwist, pelvisIkTwist_group)
cmds.matchTransform(chestIkTwist_group, 'jnt_m_spine_006', position=True, rotation=True)
cmds.matchTransform(pelvisIkTwist_group, 'jnt_m_spine_001', position=True, rotation=True)
cmds.parent(chestIkTwist_group, 'output_m_chestIk_001')
cmds.parent(pelvisIkTwist_group, 'output_m_pelvisIk_001')

# 设置IK手柄的扭转控制参数
cmds.setAttr("ikHnd_m_spineIk_001.dTwistControlEnable", 1)
cmds.setAttr("ikHnd_m_spineIk_001.dWorldUpType", 4)
# 连接定位器的世界矩阵到IK手柄属性
cmds.connectAttr('loc_m_pelvisIkTwist_001.worldMatrix[0]', 'ikHnd_m_spineIk_001.dWorldUpMatrix')
cmds.connectAttr('loc_m_chestIkTwist_001.worldMatrix[0]', 'ikHnd_m_spineIk_001.dWorldUpMatrixEnd')

# 清除当前选择
cmds.select(clear=True)

# 创建骨盆局部关节并匹配到脊椎起始位置
jnt_pelvisLocal = cmds.joint(name='jnt_m_pelvisLocal_001', position=(0, 0, 0))
cmds.matchTransform(jnt_pelvisLocal, 'jnt_m_spine_001', position=True, rotation=True)

# 设置骨盆局部控制约束
cmds.parentConstraint('output_m_pelvisLocal_001', '|master|rigNodes|rigNodesLocal')
cmds.setAttr('ctrl_m_pelvisLocal_001.translate', lock=True, keyable=False, channelBox=False)

# 约束骨盆局部关节到输出节点
cmds.parentConstraint('output_m_pelvisLocal_001', 'jnt_m_pelvisLocal_001')

# 设置骨盆局部关节的层级关系
cmds.parent('jnt_m_pelvisLocal_001', 'jnt_m_spine_001')
cmds.parent('jnt_l_upperLeg_001', 'jnt_m_pelvisLocal_001')
cmds.parent('jnt_r_upperLeg_001', 'jnt_m_pelvisLocal_001')
cmds.parent('jnt_l_clavicle_001', 'jnt_m_spine_006')
cmds.parent('jnt_r_clavicle_001', 'jnt_m_spine_006')

# 添加骨盆IK控制器的可见性属性
cmds.addAttr('ctrl_m_pelvisIk_001', longName='localCtrlVis', attributeType='bool', defaultValue=0, keyable=True)

# 连接可见性属性到骨盆局部控制组的可见性
cmds.connectAttr('ctrl_m_pelvisIk_001.localCtrlVis', 'zero_m_pelvisLocal_001.visibility')

# 胸腔控制器整理
cmds.parent('zero_m_chestIk_001', 'output_m_spineIkBendC_001')
cmds.parent('zero_m_cog_001', 'ctrl_m_world_001')
cmds.parent('zero_m_pelvisIk_001', 'output_m_cog_001')
cmds.parent('zero_m_spineIkBendA_001', 'output_m_cog_001')
cmds.parent('crv_m_spineIk_001', 'rigNodesWorld')
cmds.parent('ikHnd_m_spineIk_001', 'rigNodesLocal')

# 创建头部Ik控制器
create_control(description='headIk', shape='cube', size=1, match_type='position',
               match_target='jnt_m_neck_005', scale_factor=20)
create_control(description='headIkLocal', shape='headLocal', size=1, match_type='transform',
               match_target='jnt_m_neck_005', scale_factor=15)
cmds.addAttr('ctrl_m_headIk_001', longName='localCtrlVis', attributeType='bool', defaultValue=0, keyable=True)
cmds.connectAttr('ctrl_m_headIk_001.localCtrlVis', 'zero_m_headIkLocal_001.visibility')

create_control(description='headIkBendA', shape='square', size=1, match_type='position',
               match_target='jnt_m_neck_002', scale_factor=10)
create_control(description='headIkBendB', shape='square', parent='output_m_headIkBendA_001', size=1,
               match_type='position', match_target='jnt_m_neck_003', scale_factor=10)
cmds.setAttr('zero_m_headIkBendA_001.rotateX', 17)

cmds.parent('jnt_m_neck_001', world=True)
joints = ['jnt_m_neck_001', 'jnt_m_neck_002', 'jnt_m_neck_003', 'jnt_m_neck_004', 'jnt_m_neck_005']
curve_name = 'crv_m_neckIk_001'
ik_handle_name = 'ikHnd_m_neckIk_001'
start_joint = 'jnt_m_neck_001'
end_joint = 'jnt_m_neck_005'
neck_joint_1_name = 'jnt_m_neckIkCrv_001'
neck_joint_2_name = 'jnt_m_headIkCrv_001'
print(-1)
create_spine_ik(joints, curve_name, ik_handle_name, start_joint, end_joint, neck_joint_1_name, neck_joint_2_name)

cmds.parent('jnt_m_headIkCrv_001', 'output_m_headIk_001')
cmds.parent('jnt_m_neckIkCrv_001', 'jnt_m_spine_006')
cmds.orientConstraint('output_m_headIkLocal_001', 'jnt_m_headLocal_001')
cmds.pointConstraint('jnt_m_neck_005', 'driven_m_headIkLocal_001')
cmds.orientConstraint('output_m_headIk_001', 'driven_m_headIkLocal_001', maintainOffset=True)

neckIkTwist = cmds.spaceLocator(name='loc_m_neckIkTwist_001')[0]
headIkTwist = cmds.spaceLocator(name='loc_m_headIkTwist_001')[0]
neckIkTwist_group = cmds.group(em=True, name='zero_m_neckIkTwist_001')
headIkTwist_group = cmds.group(em=True, name='zero_m_headIkTwist_001')
cmds.parent(neckIkTwist, neckIkTwist_group)
cmds.parent(headIkTwist, headIkTwist_group)
cmds.matchTransform(neckIkTwist_group, 'jnt_m_neck_001', position=True, rotation=True)
cmds.matchTransform(headIkTwist_group, 'jnt_m_neck_005', position=True, rotation=True)
cmds.parent(neckIkTwist_group, 'jnt_m_spine_006')
cmds.parent(headIkTwist_group, 'output_m_headIk_001')

# 设置IK手柄的扭转控制参数
cmds.setAttr("ikHnd_m_neckIk_001.dTwistControlEnable", 1)
cmds.setAttr("ikHnd_m_neckIk_001.dWorldUpType", 4)
# 连接定位器的世界矩阵到IK手柄属性
cmds.connectAttr('loc_m_neckIkTwist_001.worldMatrix[0]', 'ikHnd_m_neckIk_001.dWorldUpMatrix')
cmds.connectAttr('loc_m_headIkTwist_001.worldMatrix[0]', 'ikHnd_m_neckIk_001.dWorldUpMatrixEnd')
cmds.select(clear=True)

cmds.parent('zero_m_headIk_001', 'output_m_headIkBendB_001')
cmds.parent('zero_m_headIkLocal_001', 'output_m_headIk_001')
cmds.parent('jnt_m_neck_001', 'jnt_m_spine_006')

chestCtrls_group = cmds.group(em=True, name='grp_m_chestCtrls_001')
cmds.parentConstraint('jnt_m_spine_006', 'grp_m_chestCtrls_001')
cmds.parent('grp_m_chestCtrls_001', 'output_m_cog_001')
cmds.parent('zero_m_headIkBendA_001', 'grp_m_chestCtrls_001')
cmds.parent('crv_m_neckIk_001', 'rigNodesWorld')
cmds.parent('ikHnd_m_neckIk_001', 'rigNodesLocal')


# 创建锁骨与肩胛骨控制器
create_control(description='clavicle', side='l', shape='clavicleL', size=1, match_type='transform',
               match_target='jnt_l_clavicle_001', scale_factor=1)
create_control(description='clavicle', side='r', shape='clavicleR', size=1, match_type='transform',
               match_target='jnt_r_clavicle_001', scale_factor=1)
create_control(description='scapula', side='l', shape='scapulaL', size=1, match_type='transform',
               match_target='jnt_l_scapula_001', scale_factor=1)
create_control(description='scapula', side='r', shape='scapulaR', size=1, match_type='transform',
               match_target='jnt_r_scapula_001', scale_factor=1)
cmds.parent('zero_r_scapula_001', 'output_r_clavicle_001')
cmds.parent('zero_l_scapula_001', 'output_l_clavicle_001')

cmds.orientConstraint('output_l_clavicle_001', 'jnt_l_clavicle_001')
cmds.orientConstraint('output_r_clavicle_001', 'jnt_r_clavicle_001')
cmds.orientConstraint('output_l_scapula_001', 'jnt_l_scapula_001')
cmds.orientConstraint('output_r_scapula_001', 'jnt_r_scapula_001')
cmds.parent('zero_l_clavicle_001', 'grp_m_chestCtrls_001')
cmds.parent('zero_r_clavicle_001', 'grp_m_chestCtrls_001')


# shrug控制器创建
create_control(description='shrug', side='l', shape='cube', size=1, match_type='position',
               match_target='jnt_l_scapula_001', scale_factor=10)
create_control(description='shrug', side='r', shape='cube', size=1, match_type='position',
               match_target='jnt_r_scapula_001', scale_factor=10)
cmds.parent('zero_l_shrug_001', 'grp_m_chestCtrls_001')
cmds.parent('zero_r_shrug_001', 'grp_m_chestCtrls_001')
# 创建目标约束
cmds.aimConstraint(
    'output_l_shrug_001',
    'driven_l_clavicle_001',
    aimVector=(1, 0, 0),  # Z轴指向目标
    upVector=(0, 1, 0),   # Y轴朝上
    worldUpType="objectrotation",
    worldUpVector=(0, 1, 0),
    worldUpObject='zero_l_clavicle_001'
)
cmds.aimConstraint(
    'output_r_shrug_001',
    'driven_r_clavicle_001',
    aimVector=(-1, 0, 0),  # Z轴指向目标
    upVector=(0, 1, 0),   # Y轴朝上
    worldUpType="objectrotation",
    worldUpVector=(0, 1, 0),
    worldUpObject='zero_r_clavicle_001'
)

# 为每个部位生成左右侧的IK/FK链
for limb_type in ["arm", "leg"]:
    for side in ["l", "r"]:  # 处理左右侧
        # 获取原始链并替换侧边前缀
        original_chain = [jnt.replace("_l_", f"_{side}_") for jnt in base_chains[limb_type]]

        # 验证原始关节是否存在
        if not all(cmds.objExists(jnt) for jnt in original_chain):
            print(f"Warning: {side.upper()} {limb_type} chain not found, skipping...")
            continue

        # 生成FK和IK链
        for system_type in ["Fk", "Ik"]:
            new_chain = duplicate_joint_chain(original_chain, system_type)
            print(f"Created {side.upper()} {limb_type} {system_type} chain: {'|'.join(new_chain)}")

            # 如果是FK链，自动创建FK控制器（排除最后一个关节）
            if system_type == "Fk":
                # 排除最后一个关节（如wristEnd/toeEnd）
                fk_joints = new_chain[:-1]
                create_fk_chain(fk_joints, ctrl_shape='circleX', ctrl_size=8)

# 手指控制器创建
finger_patterns = {
    'thumb': ['Metacarpal_001', 'Base_001', 'Mid_001'],
    'pinky': ['Metacarpal_001', 'Base_001', 'Mid_001', 'Tip_001'],
    'index': ['Metacarpal_001', 'Base_001', 'Mid_001', 'Tip_001'],
    'middle': ['Metacarpal_001', 'Base_001', 'Mid_001', 'Tip_001'],
    'ring': ['Metacarpal_001', 'Base_001', 'Mid_001', 'Tip_001']
}



cmds.group(em=True, name="grp_l_fingerCtrls_001")
cmds.select(clear=True)
cmds.group(em=True, name="grp_r_fingerCtrls_001")
cmds.select(clear=True)
cmds.parentConstraint("jnt_l_wristEnd_001", "grp_l_fingerCtrls_001")
cmds.select(clear=True)
cmds.parentConstraint("jnt_r_wristEnd_001", "grp_r_fingerCtrls_001")
cmds.select(clear=True)

# 为左右手创建FK控制器
for side in ['r', 'l']:  # r: 右手, l: 左手
    for finger, parts in finger_patterns.items():
        # 生成完整关节名，例如: jnt_r_indexMetacarpal_001
        joints = [f'jnt_{side}_{finger}{part}' for part in parts]
        create_fk_chain(joints, ctrl_shape='circleX', ctrl_size=1.5)
        cmds.parent(f'zero_{side}_{finger}Metacarpal_001', f'grp_{side}_fingerCtrls_001')



# 创建双手ik控制器
create_hand_ik_system(
    start_joint="jnt_l_upperArmIk_001",
    mid_joint="jnt_l_elbowFk_001",
    end_joint="jnt_l_wristIk_001",
    wrist_end_joint="jnt_l_wristEndIk_001",
    side="l",
    axis="-z"
)
create_hand_ik_system(
    start_joint="jnt_r_upperArmIk_001",
    mid_joint="jnt_r_elbowFk_001",
    end_joint="jnt_r_wristIk_001",
    wrist_end_joint="jnt_r_wristEndIk_001",
    side="r",
    axis="z"
)

# 创建双腿ik控制器
create_leg_ik_system(
    start_joint="jnt_l_upperLegIk_001",
    mid_joint="jnt_l_kneeFk_001",
    end_joint="jnt_l_ankleIk_001",
    ball_joint="jnt_l_ballIk_001",
    toe_joint="jnt_l_toeEndIk_001",
    side="l",
    axis="y"
)

create_leg_ik_system(
    start_joint="jnt_r_upperLegIk_001",
    mid_joint="jnt_r_kneeFk_001",
    end_joint="jnt_r_ankleIk_001",
    ball_joint="jnt_r_ballIk_001",
    toe_joint="jnt_r_toeEndIk_001",
    side="r",
    axis="-y"
)

set_controller_color('ctrl_l_handIk_001', side='l')
set_controller_color('ctrl_r_handIk_001', side='r')

# 创建ikFkBlend控制器
for side, x_pos in [('l', 30), ('r', -30)]:
    # 创建手部和腿部的控制器
    for part, y_pos, z_pos in [('arm', 160, -10), ('leg', 94, 0)]:
        ctrl_name = 'ctrl_{}_{}IkFkBlend_001'.format(side, part)
        zero_name = 'zero_{}_{}IkFkBlend_001'.format(side, part)
        # 创建控制器和组
        create_curve(ctrl_name, 'cross')
        cmds.group(em=True, name=zero_name)
        cmds.parent(ctrl_name, zero_name)
        cmds.move(x_pos, y_pos, z_pos, zero_name, absolute=True)
        set_controller_color(ctrl_name, side=side)
        cmds.rename(cmds.listRelatives(ctrl_name, shapes=True)[0], ctrl_name + 'Shape')
        # 设置控制器属性
        for attr in cmds.listAttr(ctrl_name, visible=True, keyable=True) or []:
            cmds.setAttr(f'{ctrl_name}.{attr}', lock=True, keyable=False, channelBox=False)
        cmds.addAttr(ctrl_name, longName="ikFkBlend", attributeType="float", minValue=0, maxValue=1,
                     defaultValue=0, keyable=True)

# 设置ikFkBlend系统
setup_ik_fk_switch(side='l')
setup_ik_fk_switch(side='r')

# 设置脚部细化操作
cmds.select(clear=True)

cmds.joint(n='jntRvs_l_toeTapIk_001')
cmds.matchTransform('jntRvs_l_toeTapIk_001', 'jnt_l_ball_001', position=True, rotation=False)

cmds.select(clear=True)

cmds.joint(n='jntRvs_l_toeTapIk_002')
cmds.matchTransform('jntRvs_l_toeTapIk_002', 'jnt_l_toeEnd_001', position=True, rotation=False)
cmds.parent('jntRvs_l_toeTapIk_002', 'jntRvs_l_toeTapIk_001')
orient_joint_chain('jntRvs_l_toeTapIk_001', orient_order="xyz", secondary_axis_orient="yup")

cmds.select(clear=True)

cmds.joint(n='jntRvs_l_ballIk_001')
cmds.matchTransform('jntRvs_l_ballIk_001', 'jnt_l_ball_001', position=True, rotation=False)

cmds.select(clear=True)

cmds.joint(n='jntRvs_l_ballIk_002')
cmds.matchTransform('jntRvs_l_ballIk_002', 'jnt_l_ankle_001', position=True, rotation=False)
cmds.parent('jntRvs_l_ballIk_002', 'jntRvs_l_ballIk_001')
orient_joint_chain('jntRvs_l_ballIk_001', orient_order="xyz", secondary_axis_orient="yup")

cmds.select(clear=True)

cmds.parent('jntRvs_l_footInnPivot_001', 'jntRvs_l_footOutPivot_001')
orient_joint_chain('jntRvs_l_footOutPivot_001', orient_order="xyz", secondary_axis_orient="yup")
cmds.parent('jntRvs_l_footInnPivot_001', world=True)
cmds.parent('jntRvs_l_footOutPivot_001', 'jntRvs_l_footInnPivot_001')
orient_joint_chain('jntRvs_l_footInnPivot_001', orient_order="xyz", secondary_axis_orient="yup")
cmds.parent('jntRvs_l_footOutPivot_001', world=True)

cmds.parent('jntRvs_l_toePivot_001', 'jntRvs_l_heelPivot_001')
orient_joint_chain('jntRvs_l_heelPivot_001', orient_order="xyz", secondary_axis_orient="yup")
cmds.parent('jntRvs_l_toePivot_001', world=True)
cmds.parent('jntRvs_l_heelPivot_001', 'jntRvs_l_toePivot_001')
orient_joint_chain('jntRvs_l_toePivot_001', orient_order="xyz", secondary_axis_orient="yup")
cmds.parent('jntRvs_l_heelPivot_001', world=True)

cmds.parent('jntRvs_l_ballIk_001', 'jntRvs_l_footInnPivot_001')
cmds.parent('jntRvs_l_toeTapIk_001', 'jntRvs_l_footInnPivot_001')
cmds.parent('jntRvs_l_footInnPivot_001', 'jntRvs_l_footOutPivot_001')
cmds.parent('jntRvs_l_footOutPivot_001', 'jntRvs_l_toePivot_001')
cmds.parent('jntRvs_l_toePivot_001', 'jntRvs_l_heelPivot_001')

# 镜像脚部定位关节链
cmds.mirrorJoint('jntRvs_l_heelPivot_001', mirrorBehavior=True, mirrorYZ=True, searchReplace=['_l_', '_r_'])

setup_foot(side='l')  # 设置左脚
setup_foot(side='r')  # 设置右脚

# 隐藏ikFk关节链
cmds.hide('jnt_?_upperArm??_001', 'jnt_?_upperLeg??_001', 'ikHnd_*_*_001')

# 调整层级结构
cmds.parent('jnt_l_upperArm?k_001', 'jnt_l_scapula_001')
cmds.parent('jnt_r_upperArm?k_001', 'jnt_r_scapula_001')
cmds.parent('zero_l_upperArmFk_001', 'output_l_scapula_001')
cmds.parent('zero_r_upperArmFk_001', 'output_r_scapula_001')
cmds.parent('jnt_?_upperLeg?k_001', 'jnt_m_pelvisLocal_001')
cmds.group(em=True, n='grp_m_pelvisLocalCtrls_001')
cmds.parentConstraint('jnt_m_pelvisLocal_001', 'grp_m_pelvisLocalCtrls_001')
cmds.parent('grp_m_pelvisLocalCtrls_001', 'output_m_cog_001')
cmds.parent('zero_?_upperLegFk_001', 'grp_m_pelvisLocalCtrls_001')
cmds.parent('grp_?_fingerCtrls_001', 'output_m_cog_001')
cmds.parent('zero_?_elbowIkGuide_001', 'output_m_cog_001')
cmds.parent('crv_?_elbowIkGuide_001', 'output_m_cog_001')
cmds.parent('zero_?_handIk_001', 'output_m_cog_001')
cmds.parent('zero_?_kneeIkGuide_001', 'output_m_cog_001')
cmds.parent('crv_?_kneeIkGuide_001', 'output_m_cog_001')
cmds.parent('zero_?_ankleIk_001', 'output_m_cog_001')
cmds.parent('zero_?_armIkFkBlend_001', 'grp_m_chestCtrls_001')
cmds.parent('zero_?_legIkFkBlend_001', 'output_m_cog_001')
cmds.group(em=True, n='output_l_ankleIk_001')
cmds.group(em=True, n='output_r_ankleIk_001')
cmds.matchTransform('output_l_ankleIk_001', 'ctrl_l_ankleIk_001')
cmds.matchTransform('output_r_ankleIk_001', 'ctrl_r_ankleIk_001')
cmds.parent('output_l_ankleIk_001', 'ctrl_l_ankleIk_001')
cmds.parent('output_r_ankleIk_001', 'ctrl_r_ankleIk_001')
cmds.parent('zero_l_heelPivot_001', 'output_l_ankleIk_001')
cmds.parent('zero_r_heelPivot_001', 'output_r_ankleIk_001')

# 设置指引线属性，防止double transform
cmds.setAttr('crv_l_kneeIkGuide_001.inheritsTransform', 0)
cmds.setAttr('crv_r_kneeIkGuide_001.inheritsTransform', 0)
cmds.setAttr('crv_l_elbowIkGuide_001.inheritsTransform', 0)
cmds.setAttr('crv_r_elbowIkGuide_001.inheritsTransform', 0)
cmds.setAttr('crv_l_kneeIkGuide_001.translate', 0, 0, 0)
cmds.setAttr('crv_r_kneeIkGuide_001.translate', 0, 0, 0)
cmds.setAttr('crv_l_elbowIkGuide_001.translate', 0, 0, 0)
cmds.setAttr('crv_r_elbowIkGuide_001.translate', 0, 0, 0)



