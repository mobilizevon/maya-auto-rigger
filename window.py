import maya.cmds as cmds
from PySide2 import QtWidgets, QtCore, QtGui
import os
import sys
import importlib
import traceback
import importlib.util
import ast  # 用于解析函数而不执行代码


# 获取Maya主窗口
def get_maya_main_window():
    """获取Maya的主窗口对象"""
    # 方法1: 使用OpenMayaUI
    try:
        import maya.OpenMayaUI as omui
        ptr = omui.MQtUtil.mainWindow()
        if ptr is not None:
            # 尝试使用shiboken2
            try:
                from shiboken2 import wrapInstance
                return wrapInstance(int(ptr), QtWidgets.QWidget)
            except:
                pass
    except:
        pass

    # 方法2: 遍历顶级窗口
    app = QtWidgets.QApplication.instance()
    for widget in app.topLevelWidgets():
        if widget.objectName() == "MayaWindow":
            return widget

    # 方法3: 创建临时窗口获取父窗口
    temp_window = QtWidgets.QMainWindow()
    parent = temp_window.parent()
    temp_window.deleteLater()
    return parent if parent else None


class MayaToolWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        # 如果无法获取主窗口，则使用None
        if parent is None:
            parent = get_maya_main_window()
        super().__init__(parent)
        self.setWindowTitle("Maya 工具集")
        self.setMinimumSize(600, 400)
        self.setup_ui()
        self.module_paths = {}  # 存储模块路径
        self.current_module = None  # 当前选中的模块对象
        self.module_functions = {}  # 存储模块函数信息
        self.undo_stack = []  # 存储撤销信息
        self.max_undo_steps = 5  # 最大保存的撤销步骤数
        self.undo_counter = 0  # 撤销文件计数器
        self.redo_stack = []  # 存储重做信息

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)

        # 创建选项卡
        self.tab_widget = QtWidgets.QTabWidget()
        main_layout.addWidget(self.tab_widget)

        # 添加模块管理选项卡
        self.setup_module_tab()

        # 添加日志输出区域
        log_group = QtWidgets.QGroupBox("执行日志")
        log_layout = QtWidgets.QVBoxLayout()
        self.log_output = QtWidgets.QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setStyleSheet("""
            QTextEdit {
                background-color: #1e1e1e; 
                color: #dcdcdc;
                font-family: Consolas, 'Courier New', monospace;
                font-size: 10pt;
            }
        """)
        log_layout.addWidget(self.log_output)
        log_group.setLayout(log_layout)
        main_layout.addWidget(log_group)

        # 添加全局操作按钮区域
        self.setup_global_buttons(main_layout)

        # 状态栏
        self.status_bar = QtWidgets.QStatusBar()
        self.status_bar.showMessage("就绪")
        main_layout.addWidget(self.status_bar)

    def setup_global_buttons(self, layout):
        """设置全局操作按钮区域，包括撤回、重做等"""
        btn_frame = QtWidgets.QFrame()
        btn_layout = QtWidgets.QHBoxLayout(btn_frame)

        # 添加撤回按钮
        self.undo_btn = QtWidgets.QPushButton("撤回")
        self.undo_btn.setIcon(QtWidgets.QApplication.style().standardIcon(
            QtWidgets.QStyle.SP_ArrowBack))
        self.undo_btn.setToolTip("Ctrl+Z")
        self.undo_btn.setEnabled(False)
        self.undo_btn.clicked.connect(self.undo_action)
        btn_layout.addWidget(self.undo_btn)

        # 添加重做按钮
        self.redo_btn = QtWidgets.QPushButton("重做")
        self.redo_btn.setIcon(QtWidgets.QApplication.style().standardIcon(
            QtWidgets.QStyle.SP_ArrowForward))
        self.redo_btn.setToolTip("Ctrl+Y")
        self.redo_btn.setEnabled(False)
        self.redo_btn.clicked.connect(self.redo_action)
        btn_layout.addWidget(self.redo_btn)

        # 添加清除历史按钮
        clear_btn = QtWidgets.QPushButton("清除历史")
        clear_btn.setIcon(QtWidgets.QApplication.style().standardIcon(
            QtWidgets.QStyle.SP_DialogDiscardButton))
        clear_btn.setToolTip("清除所有撤销历史")
        clear_btn.clicked.connect(self.clear_undo_history)
        btn_layout.addWidget(clear_btn)

        # 添加历史状态显示
        self.history_label = QtWidgets.QLabel("历史: 0/0")
        btn_layout.addWidget(self.history_label)

        btn_layout.addStretch()

        # 设置快捷键
        shortcut_undo = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Z"), self)
        shortcut_undo.activated.connect(self.undo_action)

        shortcut_redo = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Y"), self)
        shortcut_redo.activated.connect(self.redo_action)

        layout.addWidget(btn_frame)

    def setup_module_tab(self):
        """设置模块管理选项卡"""
        module_tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(module_tab)

        # 模块列表
        module_list_group = QtWidgets.QGroupBox("可用模块")
        module_list_layout = QtWidgets.QVBoxLayout()

        # 模块列表控件
        self.module_list = QtWidgets.QListWidget()
        self.module_list.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.module_list.setFixedHeight(150)
        self.module_list.itemSelectionChanged.connect(self.on_module_selected)
        module_list_layout.addWidget(self.module_list)

        # 添加/删除模块按钮
        btn_layout = QtWidgets.QHBoxLayout()
        self.add_module_btn = QtWidgets.QPushButton("添加模块")
        self.add_module_btn.clicked.connect(self.add_module)
        self.remove_module_btn = QtWidgets.QPushButton("移除模块")
        self.remove_module_btn.clicked.connect(self.remove_module)
        btn_layout.addWidget(self.add_module_btn)
        btn_layout.addWidget(self.remove_module_btn)
        module_list_layout.addLayout(btn_layout)

        module_list_group.setLayout(module_list_layout)
        layout.addWidget(module_list_group)

        # 模块功能按钮
        function_group = QtWidgets.QGroupBox("模块功能")
        function_layout = QtWidgets.QGridLayout()

        # 创建动态按钮区域
        self.button_container = QtWidgets.QWidget()
        self.button_layout = QtWidgets.QVBoxLayout(self.button_container)
        function_layout.addWidget(self.button_container, 0, 0, 1, 3)

        # 执行按钮
        self.execute_btn = QtWidgets.QPushButton("执行模块")
        self.execute_btn.clicked.connect(self.execute_module)
        function_layout.addWidget(self.execute_btn, 1, 1)

        function_group.setLayout(function_layout)
        layout.addWidget(function_group)

        self.tab_widget.addTab(module_tab, "模块管理")

    def add_module(self):
        """添加新模块到列表"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, "选择Python模块", "", "Python Files (*.py)"
        )

        if file_path:
            module_name = os.path.splitext(os.path.basename(file_path))[0]

            # 检查是否已添加
            if any(self.module_list.item(i).text() == module_name
                   for i in range(self.module_list.count())):
                self.log(f"模块 '{module_name}' 已存在")
                return

            # 添加到列表
            self.module_list.addItem(module_name)
            self.module_paths[module_name] = file_path
            self.log(f"添加模块: {module_name}")

    def remove_module(self):
        """移除选中的模块"""
        selected = self.module_list.selectedItems()
        if not selected:
            return

        item = selected[0]
        module_name = item.text()

        # 从字典和列表中移除
        self.module_list.takeItem(self.module_list.row(item))
        if module_name in self.module_paths:
            del self.module_paths[module_name]
        if module_name in self.module_functions:
            del self.module_functions[module_name]

        self.log(f"移除模块: {module_name}")

    def on_module_selected(self):
        """当选择新模块时加载其函数列表（但不执行模块）"""
        selected = self.module_list.selectedItems()
        if not selected:
            return

        module_name = selected[0].text()
        self.load_module_functions(module_name)

    def load_module_functions(self, module_name):
        """解析模块中的函数而不执行代码"""
        # 清除现有按钮
        while self.button_layout.count():
            item = self.button_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 获取模块路径
        file_path = self.module_paths.get(module_name)
        if not file_path or not os.path.exists(file_path):
            self.log(f"找不到模块文件: {module_name}")
            return

        try:
            # 读取文件内容
            encoding = self.detect_encoding(file_path) or 'utf-8'
            with open(file_path, 'r', encoding=encoding) as f:
                code_str = f.read()

            # 使用ast解析模块，提取函数定义
            module_node = ast.parse(code_str, filename=file_path)
            functions = []
            for node in ast.walk(module_node):
                if isinstance(node, ast.FunctionDef):
                    functions.append(node.name)

            # 保存函数列表供以后使用
            self.module_functions[module_name] = {
                'file_path': file_path,
                'functions': functions,
                'encoding': encoding
            }

            # 为每个函数创建按钮
            for func_name in functions:
                btn = QtWidgets.QPushButton(func_name)
                btn.setProperty("module", module_name)  # 存储模块名而不是模块对象
                btn.setProperty("function", func_name)
                btn.clicked.connect(self.execute_function)
                self.button_layout.addWidget(btn)

            self.log(f"加载 {len(functions)} 个函数来自 {module_name}")

        except Exception as e:
            self.log(f"解析模块错误: {str(e)}")
            traceback.print_exc()

    def detect_encoding(self, file_path):
        """自动检测文件编码"""
        try:
            import chardet
            with open(file_path, 'rb') as f:
                raw_data = f.read(4096)  # 读取前4KB足够检测编码
                result = chardet.detect(raw_data)
                return result['encoding']
        except ImportError:
            # 如果没有chardet，使用默认UTF-8
            return 'utf-8'
        except Exception:
            return 'utf-8'

    def create_undo_point(self, action_name):
        """
        创建撤销点
        :param action_name: 操作名称，用于在历史记录中显示
        """
        try:
            # 创建唯一的文件名称
            self.undo_counter += 1
            file_path = os.path.join(
                cmds.internalVar(userTmpDir=True),
                f"undo_state_{self.undo_counter}.ma"
            )

            # 保存当前场景
            current_scene = cmds.file(query=True, sceneName=True)

            # 如果没有场景名称，使用新建的场景
            if not current_scene or not os.path.exists(current_scene):
                current_scene = file_path
                cmds.file(rename=file_path)

            # 保存场景副本作为撤销点
            cmds.file(save=True, type='mayaAscii', force=True)
            backup_path = file_path
            cmds.file(rename=backup_path)
            cmds.file(save=True, force=True, type="mayaAscii")

            # 恢复原来的文件路径
            if current_scene != backup_path:
                cmds.file(rename=current_scene)

            # 保存撤销信息
            undo_info = {
                'file': backup_path,
                'timestamp': QtCore.QDateTime.currentDateTime().toString(),
                'action': action_name,
                'index': len(self.undo_stack) + 1
            }

            # 如果超过最大步数，删除最旧的记录
            if len(self.undo_stack) >= self.max_undo_steps:
                oldest = self.undo_stack.pop(0)
                try:
                    if os.path.exists(oldest['file']):
                        os.remove(oldest['file'])
                except:
                    pass

            # 添加到撤销栈
            self.undo_stack.append(undo_info)
            # 清除重做栈，因为有了新操作
            self.clear_redo_stack()
            self.log(f"创建撤销点: {action_name}")
            self.update_undo_ui()

            return True
        except Exception as e:
            self.log(f"创建撤销点失败: {str(e)}")
            traceback.print_exc()
            return False

    def undo_action(self):
        """执行撤回操作"""
        if not self.undo_stack:
            return

        try:
            # 获取最新的撤销点
            undo_info = self.undo_stack.pop()
            action_name = undo_info['action']

            # 保存当前场景到重做点
            current_scene = cmds.file(query=True, sceneName=True)
            if current_scene and os.path.exists(current_scene):
                # 创建重做点
                redo_counter = len(self.redo_stack) + 1
                redo_path = os.path.join(
                    cmds.internalVar(userTmpDir=True),
                    f"redo_state_{redo_counter}.ma"
                )

                # 保存当前场景到重做点
                cmds.file(rename=redo_path)
                cmds.file(save=True, force=True, type="mayaAscii")

                # 添加重做信息
                redo_info = {
                    'file': redo_path,
                    'timestamp': QtCore.QDateTime.currentDateTime().toString(),
                    'action': f"重做: {action_name}",
                    'index': len(self.redo_stack) + 1
                }
                self.redo_stack.append(redo_info)

            # 重置Maya状态
            if os.path.exists(undo_info['file']):
                # 打开撤销点文件
                cmds.file(undo_info['file'], open=True, force=True)

                # 更新重做按钮状态
                self.redo_btn.setEnabled(True)

                self.log(f"撤回操作: {action_name}")
            else:
                self.log(f"撤销点文件已丢失: {undo_info['file']}")

            self.update_undo_ui()

        except Exception as e:
            self.log(f"撤回操作失败: {str(e)}")
            traceback.print_exc()

    def redo_action(self):
        """执行重做操作"""
        if not self.redo_stack:
            return

        try:
            # 获取最新的重做点
            redo_info = self.redo_stack.pop()

            # 保存当前场景到撤销点
            current_scene = cmds.file(query=True, sceneName=True)
            if current_scene and os.path.exists(current_scene):
                # 保存到撤销点
                self.undo_counter += 1
                undo_path = os.path.join(
                    cmds.internalVar(userTmpDir=True),
                    f"undo_state_{self.undo_counter}.ma"
                )

                # 保存当前场景到撤销点
                cmds.file(rename=undo_path)
                cmds.file(save=True, force=True, type="mayaAscii")

                # 添加到撤销栈
                undo_info = {
                    'file': undo_path,
                    'timestamp': QtCore.QDateTime.currentDateTime().toString(),
                    'action': f"重做: {redo_info['action']}",
                    'index': len(self.undo_stack) + 1
                }
                self.undo_stack.append(undo_info)

            # 打开重做点文件
            if os.path.exists(redo_info['file']):
                cmds.file(redo_info['file'], open=True, force=True)

                self.log(f"重做操作: {redo_info['action']}")
                self.update_undo_ui()
            else:
                self.log(f"重做点文件已丢失: {redo_info['file']}")

        except Exception as e:
            self.log(f"重做操作失败: {str(e)}")
            traceback.print_exc()

    def clear_undo_history(self):
        """清除所有撤销历史"""
        # 删除所有撤销文件
        for undo_info in self.undo_stack:
            try:
                if os.path.exists(undo_info['file']):
                    os.remove(undo_info['file'])
            except:
                pass

        # 同时清除重做历史
        self.clear_redo_stack()

        self.undo_stack = []
        self.log("已清除所有撤销历史")
        self.update_undo_ui()

    def clear_redo_stack(self):
        """清除重做栈"""
        for redo_info in self.redo_stack:
            try:
                if os.path.exists(redo_info['file']):
                    os.remove(redo_info['file'])
            except:
                pass
        self.redo_stack = []
        self.redo_btn.setEnabled(False)

    def update_undo_ui(self):
        """更新撤销相关的UI状态"""
        # 更新按钮状态
        self.undo_btn.setEnabled(len(self.undo_stack) > 0)
        self.redo_btn.setEnabled(len(self.redo_stack) > 0)

        # 更新历史标签
        self.history_label.setText(f"历史: {len(self.undo_stack)}/{self.max_undo_steps}")

    def execute_function(self):
        """执行选中的函数"""
        btn = self.sender()
        if not btn:
            return

        module_name = btn.property("module")
        func_name = btn.property("function")

        # 获取模块信息
        module_info = self.module_functions.get(module_name)
        if not module_info:
            self.log(f"未找到模块信息: {module_name}")
            return

        file_path = module_info['file_path']
        encoding = module_info['encoding']

        try:
            # 1. 首先创建撤销点
            if not self.create_undo_point(f"{module_name}.{func_name}"):
                self.log(f"警告: 撤销点创建失败，继续执行函数 '{func_name}'")

            # 2. 动态加载模块
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)

            # 3. 执行模块代码（只执行一次）
            with open(file_path, 'r', encoding=encoding) as f:
                code = f.read()

            compiled_code = compile(code, file_path, 'exec')
            spec.loader.exec_module(module)

            # 4. 获取并执行函数
            func = getattr(module, func_name)
            self.log(f"执行函数: {func_name}()")
            func()
            self.log(f"函数 {func_name}() 执行完成")
        except Exception as e:
            self.log(f"执行错误: {str(e)}")
            traceback.print_exc()

    def execute_module(self):
        """执行整个模块（按原样执行脚本）"""
        selected = self.module_list.selectedItems()
        if not selected:
            self.log("请先选择一个模块")
            return

        module_name = selected[0].text()
        module_info = self.module_functions.get(module_name)

        if not module_info:
            self.log(f"未找到模块信息: {module_name}")
            return

        file_path = module_info['file_path']
        encoding = module_info['encoding']

        try:
            # 1. 首先创建撤销点
            if not self.create_undo_point(f"模块 {module_name}"):
                self.log(f"警告: 撤销点创建失败，继续执行模块 '{module_name}'")

            # 2. 记录执行开始
            self.log(f"开始执行模块: {module_name}")

            # 3. 直接执行整个脚本文件
            with open(file_path, 'r', encoding=encoding) as f:
                code = f.read()

            # 4. 编译并执行
            compiled_code = compile(code, file_path, 'exec')
            exec(compiled_code, globals())

            self.log(f"模块 {module_name} 执行完成")
        except Exception as e:
            self.log(f"执行错误: {str(e)}")
            traceback.print_exc()

    def log(self, message):
        """添加日志信息"""
        timestamp = QtCore.QDateTime.currentDateTime().toString("hh:mm:ss")
        self.log_output.append(f"[{timestamp}] {message}")
        self.status_bar.showMessage(message)

        # 自动滚动到底部
        self.log_output.verticalScrollBar().setValue(
            self.log_output.verticalScrollBar().maximum()
        )

        # 确保UI更新
        QtCore.QCoreApplication.processEvents()


# 显示窗口
def show_tool_window():
    # 防止重复打开窗口
    app = QtWidgets.QApplication.instance()
    for widget in app.topLevelWidgets():
        if widget.objectName() == "MayaToolWindow":
            widget.close()
            widget.deleteLater()

    window = MayaToolWindow()
    window.setObjectName("MayaToolWindow")
    window.show()
    return window


# 在Maya中运行
if __name__ == "__main__":
    show_tool_window()