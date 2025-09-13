# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/6/4
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
import weakref

from PySide6.QtGui import QIntValidator
from PySide6.QtWidgets import *

from core import core_input, core_save, core_timer, core_event
from core.core_define import Path_Setting, SettingName
from widgets.button import PrimaryPushButton
from widgets.line_edit import LineEdit
from widgets.switch_button import SwitchButton


class Setting_Menu(QWidget):
    def __init__(self, parent):
        super().__init__(None)
        self.setup_ui()
        self.m_ParentProxy = weakref.proxy(parent)

    def setup_ui(self):
        # 主布局 MAIN LAYOUT
        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(10, 10, 10, 10)
        self.layout_main.setSpacing(10)

        data = core_save.LoadJson(Path_Setting)
        size = data.get(SettingName.PetIconSize, 72)
        self.layout_size = QHBoxLayout()
        self.label_size = QLabel("悬浮图标尺寸")
        self.layout_size.addWidget(self.label_size)
        self.edit_size = LineEdit(self)
        self.edit_size.setText(str(size))
        self.edit_size.setValidator(QIntValidator(self.edit_size))
        self.edit_size.setClearButtonEnabled(True)
        self.edit_size.textChanged.connect(self.on_app_size_change)
        self.layout_size.addWidget(self.edit_size)
        self.layout_main.addLayout(self.layout_size)

        data = core_save.LoadJson(Path_Setting)
        iTime = data.get(SettingName.PetIconUpdateTime, 100)
        self.layout_update_time = QHBoxLayout()
        self.label_update_time = QLabel("悬浮图标刷新时间间隔(毫秒)")
        self.layout_update_time.addWidget(self.label_update_time)
        self.edit_update_time = LineEdit(self)
        self.edit_update_time.setText(str(iTime))
        self.edit_update_time.setValidator(QIntValidator(self.edit_update_time))
        self.edit_update_time.setClearButtonEnabled(True)
        self.edit_update_time.textChanged.connect(self.on_app_update_time_change)
        self.layout_update_time.addWidget(self.edit_update_time)
        self.layout_main.addLayout(self.layout_update_time)

        # 修改热键生效超时时长
        self.layout_time = QHBoxLayout()
        self.label_time = QLabel("热键超时(ms)")
        self.layout_time.addWidget(self.label_time)
        self.edit_time = LineEdit(self)
        self.edit_time.setText(str(core_input.g_HotKeyTimeOut))
        self.edit_time.setValidator(QIntValidator(self.edit_time))
        self.edit_time.setClearButtonEnabled(True)
        self.edit_time.textChanged.connect(self.on_hotkey_timeout_change)
        self.layout_time.addWidget(self.edit_time)
        self.layout_main.addLayout(self.layout_time)

        # 修改按键
        data = core_save.LoadJson(Path_Setting)
        sKey = data.get(SettingName.TimerReset, ["F2"])
        self.layout_key = QHBoxLayout()
        self.label_key = QLabel("一键重置所有定时器")
        self.layout_key.addWidget(self.label_key)

        self.edit_keys = LineEdit(self)
        sKey = f"{'、'.join(sKey)}"
        self.edit_keys.setText(sKey.upper())
        self.edit_keys.setReadOnly(True)
        self.edit_keys.Released.connect(self.on_record_keys)
        self.layout_key.addWidget(self.edit_keys)
        self.layout_main.addLayout(self.layout_key)
        self.adjustSize()

    def on_app_size_change(self, sText):
        if not sText:
            sText = 16
        data = core_save.LoadJson(Path_Setting)
        size = int(sText)
        if size < 16:
            size = 16
        data[SettingName.PetIconSize] = size
        core_save.SaveJson(Path_Setting, data)
        core_event.TriggerEvent("RELOAD_PET_RES")

    def on_app_update_time_change(self, sText):
        if not sText:
            sText = 16
        data = core_save.LoadJson(Path_Setting)
        iTime = int(sText)
        if iTime < 16:
            iTime = 16
        data[SettingName.PetIconUpdateTime] = iTime
        core_save.SaveJson(Path_Setting, data)
        core_event.TriggerEvent("RELOAD_PET_RES")

    def on_hotkey_timeout_change(self, sText):
        if not sText:
            return
        try:
            int(sText)
        except:
            sText = 2000
        core_input.g_HotKeyTimeOut = int(sText)
        data = core_save.LoadJson(Path_Setting)
        data[SettingName.TimerResetTime] = int(sText)
        core_save.SaveJson(Path_Setting, data)

    def on_record_keys(self):
        print("开始记录热键")
        # self.button_record_key.setText("热键记录中...")
        self.edit_keys.setText("热键记录中...")
        self._cache_keys = []
        self._cache_key_lister = core_input.RegisterInputCb(self.cache_keys)
        core_timer.CreateOnceTimer(3000, self.stop_cache_keys, delta=False)
        pass

    def cache_keys(self, skey):
        self._cache_keys.append(skey)

    def stop_cache_keys(self):
        print("记录的按键：", self._cache_keys)
        # self.button_record_key.setText("点击记录热键")
        self._cache_key_lister = None
        if not self._cache_keys:
            self._cache_keys = ["F2"]
        sKey = f"{'、'.join(self._cache_keys)}" if self._cache_keys else ""
        data = core_save.LoadJson(Path_Setting)
        data[SettingName.TimerReset] = self._cache_keys
        core_save.SaveJson(Path_Setting, data)
        self._cache_keys = []
        self.edit_keys.setText(sKey)
        self.m_ParentProxy.register_reset_hotkey()
