# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/6/4
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
import weakref
from PySide6.QtWidgets import *

from core import core_event
from logic.timer.timer_group import GroupProxy
from logic.timer.timer_info import TimerProxy
from widgets.button import PrimaryPushButton
from widgets.line_edit import LineEdit
from widgets.switch_button import SwitchButton


class Group_Menu(QWidget):
    def __init__(self, groupInfo, close_menu_func, del_group_func):
        super().__init__(None)
        self.groupInfo: "GroupProxy" = weakref.proxy(groupInfo)
        self.del_group_func = del_group_func
        self.close_menu_func = close_menu_func
        self.setup_ui(groupInfo)

    def setup_ui(self, groupInfo: "GroupProxy"):
        # 主布局 MAIN LAYOUT
        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(10, 10, 10, 10)
        self.layout_main.setSpacing(10)

        # 分组ID
        self.layout_id = QHBoxLayout()
        self.label_id = QLabel("ID")
        self.layout_id.addWidget(self.label_id)
        self.label_idInfo = QLabel(str(self.groupInfo.m_uuid))
        self.layout_id.addWidget(self.label_idInfo)
        self.layout_main.addLayout(self.layout_id)

        # 开关
        self.layout_switch = QHBoxLayout()
        self.label_switch = QLabel("分组开关")
        self.layout_switch.addWidget(self.label_switch)
        self.button_switch = SwitchButton("", "")
        self.button_switch.setChecked(groupInfo.m_bOpen)
        self.button_switch.checkedChanged.connect(self.OnChangeSwitch)
        self.layout_switch.addWidget(self.button_switch)
        self.layout_main.addLayout(self.layout_switch)

        # 修改名称
        self.layout_name = QHBoxLayout()
        self.label_name = QLabel("名称")
        self.layout_name.addWidget(self.label_name)
        self.edit_name = LineEdit(self)
        self.edit_name.setText(groupInfo.m_sName)
        self.edit_name.setPlaceholderText('请输入分组名')
        self.edit_name.setClearButtonEnabled(True)
        self.edit_name.editingFinished.connect(self.on_name_change)
        self.layout_name.addWidget(self.edit_name)
        self.layout_main.addLayout(self.layout_name)

        self.button_delete = PrimaryPushButton("删除分组", self)
        self.button_delete.clicked.connect(self.on_delete)
        self.button_delete.setStyleSheet("background-color: red; color: white;border-radius:5px;")
        self.layout_main.addWidget(self.button_delete)

        self.adjustSize()

    def OnChangeSwitch(self, switch):
        self.groupInfo.ChangeSwitch(switch)
        self.close_menu_func()
        core_event.TriggerEvent("REOPEN_MENU")

    def on_name_change(self):
        sText = self.edit_name.text()
        if not sText:
            return
        self.groupInfo.m_sName = sText
        self.groupInfo.Save()
        self.close_menu_func()
        core_event.TriggerEvent("REOPEN_MENU")
        pass


    def on_delete(self):
        print("准备删除：", self.groupInfo.m_uuid)
        self.groupInfo.ChangeSwitch(False)
        self.del_group_func(self.groupInfo.m_uuid)
        self.close_menu_func()
        core_event.TriggerEvent("REOPEN_MENU")
        pass

