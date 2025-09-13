# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/6/4
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
import weakref

from PySide6.QtGui import QIntValidator, QColor, QCursor
from PySide6.QtWidgets import *

from core import core_input, core_timer, core_voice, core_event
from core.functor import CFunctor
from logic.timer.timer_info import TimerProxy
from widgets.button import PrimaryPushButton
from widgets.line_edit import LineEdit
from widgets.switch_button import SwitchButton


class Timer_Menu(QWidget):
    def __init__(self, timer_info, close_menu_func, del_timer_func):
        super().__init__(None)
        self.timer_info: "TimerProxy" = weakref.proxy(timer_info)

        self._record_key_index = None
        self._edit_key = []
        self._edit_view = None

        self.del_timer_func = del_timer_func
        self.close_menu_func = close_menu_func

        self._cache_key_lister = None
        self._cache_keys = []

        self.setup_ui(timer_info)

    def setup_ui(self, timer_info: "TimerProxy"):
        # 主布局 MAIN LAYOUT
        self.layout_main = QVBoxLayout(self)
        self.layout_main.setContentsMargins(10, 10, 10, 10)
        self.layout_main.setSpacing(10)

        # 开关
        self.layout_switch = QHBoxLayout()
        self.label_switch = QLabel("定时器开关")
        self.layout_switch.addWidget(self.label_switch)
        self.button_switch = SwitchButton("", "")
        self.button_switch.setChecked(timer_info.m_bOpen)
        self.button_switch.checkedChanged.connect(timer_info.ChangeSwitch)
        self.layout_switch.addWidget(self.button_switch)
        self.layout_main.addLayout(self.layout_switch)

        # 开关
        self.layout_reset = QHBoxLayout()
        self.label_reset = QLabel("允许一键重置")
        self.layout_reset.addWidget(self.label_reset)
        self.button_reset = SwitchButton("", "")
        self.button_reset.setChecked(timer_info.m_bReset)
        self.button_reset.checkedChanged.connect(self.on_reset_change)
        self.layout_reset.addWidget(self.button_reset)
        self.layout_main.addLayout(self.layout_reset)

        # 严格热键模式
        self.layout_force_match = QHBoxLayout()
        self.label_force_match = QLabel("严格匹配热键")
        self.layout_force_match.addWidget(self.label_force_match)
        self.button_force_match = SwitchButton("", "")
        self.button_force_match.setChecked(timer_info.m_forceMatch)
        self.button_force_match.checkedChanged.connect(self.on_force_match_change)
        self.layout_force_match.addWidget(self.button_force_match)
        self.layout_main.addLayout(self.layout_force_match)

        # 重复触发
        self.layout_trigger = QHBoxLayout()
        self.label_trigger = QLabel("允许冷却时触发")
        self.layout_trigger.addWidget(self.label_trigger)
        self.button_trigger = SwitchButton("", "")
        self.button_trigger.setChecked(timer_info.m_bTriggerInCd)
        self.button_trigger.checkedChanged.connect(self.on_trigger_change)
        self.layout_trigger.addWidget(self.button_trigger)
        self.layout_main.addLayout(self.layout_trigger)


        # 循环记时
        self.layout_cycle = QHBoxLayout()
        self.label_cycle = QLabel("自动循环触发")
        self.layout_cycle.addWidget(self.label_cycle)
        self.button_cycle = SwitchButton("", "")
        self.button_cycle.setChecked(timer_info.m_bCycle)
        self.button_cycle.checkedChanged.connect(self.on_cycle_change)
        self.layout_cycle.addWidget(self.button_cycle)
        self.layout_main.addLayout(self.layout_cycle)

        # 文本|图标
        self.layout_textoricon = QHBoxLayout()
        self.label_textoricon = QLabel("图标定时器")
        self.layout_textoricon.addWidget(self.label_textoricon)
        self.button_textoricon = SwitchButton("", "")
        self.button_textoricon.setChecked(timer_info.m_bIconTimer)
        self.button_textoricon.checkedChanged.connect(self.on_textoricon_change)
        self.layout_textoricon.addWidget(self.button_textoricon)
        self.layout_main.addLayout(self.layout_textoricon)

        # 语音播报
        self.layout_voice = QHBoxLayout()
        self.label_voice = QLabel("语音播报")
        self.layout_voice.addWidget(self.label_voice)
        self.button_voice = SwitchButton("", "")
        self.button_voice.setChecked(timer_info.m_bVoice)
        self.button_voice.checkedChanged.connect(self.on_voice_change)
        self.layout_voice.addWidget(self.button_voice)
        self.layout_main.addLayout(self.layout_voice)

        # 修改名称
        self.layout_name = QHBoxLayout()
        self.label_name = QLabel("名称")
        self.layout_name.addWidget(self.label_name)
        self.edit_name = LineEdit(self)
        self.edit_name.setText(timer_info.m_sName)
        self.edit_name.setPlaceholderText('请输入定时器名字')
        self.edit_name.setClearButtonEnabled(True)
        self.edit_name.editingFinished.connect(self.on_name_change)
        self.layout_name.addWidget(self.edit_name)
        self.layout_main.addLayout(self.layout_name)

        # 修改时间
        self.layout_group = QHBoxLayout()
        self.label_group = QLabel("分组")
        self.layout_group.addWidget(self.label_group)
        self.edit_group = LineEdit(self)
        self.edit_group.setText(str(int(timer_info.m_groupId)))
        self.edit_group.setPlaceholderText('定时器分组')
        self.edit_group.setValidator(QIntValidator(self.edit_group))
        self.edit_group.setClearButtonEnabled(True)
        self.edit_group.editingFinished.connect(self.on_group_change)
        self.layout_group.addWidget(self.edit_group)
        self.layout_main.addLayout(self.layout_group)

        # 修改时间
        self.layout_time = QHBoxLayout()
        self.label_time = QLabel("时间")
        self.layout_time.addWidget(self.label_time)
        self.edit_time = LineEdit(self)
        self.edit_time.setText(str(timer_info.m_fTotalTime))
        self.edit_time.setPlaceholderText('定时器时间')
        self.edit_time.setValidator(QIntValidator(self.edit_time))
        self.edit_time.setClearButtonEnabled(True)
        self.edit_time.editingFinished.connect(self.on_time_change)
        self.layout_time.addWidget(self.edit_time)
        self.layout_main.addLayout(self.layout_time)

        bIconTimer = timer_info.m_bIconTimer
        if bIconTimer:
            # 修改图标
            self.layout_icon = QHBoxLayout()
            self.label_icon = QLabel("图标")
            self.layout_icon.addWidget(self.label_icon)
            self.edit_icon = LineEdit(self)
            self.edit_icon.setText(timer_info.m_sPic)
            self.edit_icon.setPlaceholderText('图标名 Resources/icon下')
            self.edit_icon.setClearButtonEnabled(True)
            self.edit_icon.editingFinished.connect(self.on_icon_change)
            self.layout_icon.addWidget(self.edit_icon)
            self.layout_main.addLayout(self.layout_icon)

            # 倒计时图标
            self.layout_mask = QHBoxLayout()
            self.label_mask = QLabel("遮罩")
            self.layout_mask.addWidget(self.label_mask)
            self.edit_mask = LineEdit(self)
            self.edit_mask.setText(timer_info.m_sMaskPic)
            self.edit_mask.setPlaceholderText('默认灰色遮罩')
            self.edit_mask.setClearButtonEnabled(True)
            self.edit_mask.editingFinished.connect(self.on_mask_change)
            self.layout_mask.addWidget(self.edit_mask)
            self.layout_main.addLayout(self.layout_mask)

            # 修改图标大小
            self.layout_icon_size = QHBoxLayout()
            self.label_icon_size = QLabel("大小")
            self.layout_icon_size.addWidget(self.label_icon_size)
            self.edit_icon_size = LineEdit(self)
            if timer_info.m_iConSize != 0:
                self.edit_icon_size.setText(str(timer_info.m_iConSize))
            self.edit_icon_size.setPlaceholderText('图标尺寸')
            self.edit_icon_size.setValidator(QIntValidator(self.edit_icon_size))
            self.edit_icon_size.setClearButtonEnabled(True)
            self.edit_icon_size.editingFinished.connect(self.on_icon_size_change)
            self.layout_icon_size.addWidget(self.edit_icon_size)
            self.layout_main.addLayout(self.layout_icon_size)

            # 修改边框大小
            self.layout_board_size = QHBoxLayout()
            self.label_board_size = QLabel("边框")
            self.layout_board_size.addWidget(self.label_board_size)
            self.edit_board_size = LineEdit(self)
            self.edit_board_size.setText(str(timer_info.m_iBoardSize))
            self.edit_board_size.setPlaceholderText('边框尺寸')
            self.edit_board_size.setValidator(QIntValidator(self.edit_board_size))
            self.edit_board_size.setClearButtonEnabled(True)
            self.edit_board_size.editingFinished.connect(self.on_board_size_change)
            self.layout_board_size.addWidget(self.edit_board_size)
            self.layout_main.addLayout(self.layout_board_size)

        # 修改字号
        self.layout_font_size = QHBoxLayout()
        self.label_font_size = QLabel("字号")
        self.layout_font_size.addWidget(self.label_font_size)
        self.edit_font_size = LineEdit(self)
        self.edit_font_size.setText(str(timer_info.m_iFontSize))
        self.edit_font_size.setPlaceholderText('请输入字号')
        self.edit_font_size.setValidator(QIntValidator(self.edit_font_size))
        self.edit_font_size.setClearButtonEnabled(True)
        self.edit_font_size.editingFinished.connect(self.on_font_size_change)
        self.layout_font_size.addWidget(self.edit_font_size)
        self.layout_main.addLayout(self.layout_font_size)

        # 修改冷却文本
        self.layout_cd_text = QHBoxLayout()
        self.labe_cd_text = QLabel("冷却提示")
        self.layout_cd_text.addWidget(self.labe_cd_text)
        self.edit_cd_text = LineEdit(self)
        self.edit_cd_text.setText(timer_info.m_sCD)
        self.edit_cd_text.setPlaceholderText('请输入定时器冷却提示')
        self.edit_cd_text.setClearButtonEnabled(True)
        self.edit_cd_text.editingFinished.connect(self.on_cd_text_change)
        self.layout_cd_text.addWidget(self.edit_cd_text)
        self.layout_main.addLayout(self.layout_cd_text)

        # 修改就绪文本
        self.layout_ready_text = QHBoxLayout()
        self.label_ready_text = QLabel("就绪提示")
        self.layout_ready_text.addWidget(self.label_ready_text)
        self.edit_ready_text = LineEdit(self)
        self.edit_ready_text.setText(timer_info.m_sReady)
        self.edit_ready_text.setPlaceholderText('请输入定时器就绪文本')
        self.edit_ready_text.setClearButtonEnabled(True)
        self.edit_ready_text.editingFinished.connect(self.on_ready_text_change)
        self.layout_ready_text.addWidget(self.edit_ready_text)
        self.layout_main.addLayout(self.layout_ready_text)

        if not bIconTimer:
            # 冷却文本颜色
            self.layout_cd_text_color = QHBoxLayout()
            self.labe_cd_text_color = QLabel("冷却文本颜色")
            self.layout_cd_text_color.addWidget(self.labe_cd_text_color)
            self.edit_cd_text_color = LineEdit(self)
            self.edit_cd_text_color.setText(timer_info.m_cdColor)
            self.edit_cd_text_color.setPlaceholderText('冷却文本颜色, 如#FF0000')
            self.edit_cd_text_color.setClearButtonEnabled(True)
            self.edit_cd_text_color.editingFinished.connect(self.on_cd_text_color_change)
            self.layout_cd_text_color.addWidget(self.edit_cd_text_color)
            self.layout_main.addLayout(self.layout_cd_text_color)
            # 就绪文本颜色
            self.layout_ready_text_color = QHBoxLayout()
            self.labe_ready_text_color = QLabel("就绪文本颜色")
            self.layout_ready_text_color.addWidget(self.labe_ready_text_color)
            self.edit_ready_text_color = LineEdit(self)
            self.edit_ready_text_color.setText(timer_info.m_readyColor)
            self.edit_ready_text_color.setPlaceholderText('冷却文本颜色, 如#FF0000')
            self.edit_ready_text_color.setClearButtonEnabled(True)
            self.edit_ready_text_color.editingFinished.connect(self.on_ready_text_color_change)
            self.layout_ready_text_color.addWidget(self.edit_ready_text_color)
            self.layout_main.addLayout(self.layout_ready_text_color)
        else:
            self.layout_cd_text_color = QHBoxLayout()
            self.labe_cd_text_color = QLabel("文本颜色")
            self.layout_cd_text_color.addWidget(self.labe_cd_text_color)
            self.edit_cd_text_color = LineEdit(self)
            self.edit_cd_text_color.setText(timer_info.m_cdColor)
            self.edit_cd_text_color.setPlaceholderText('冷却文本颜色, 如#FF0000')
            self.edit_cd_text_color.setClearButtonEnabled(True)
            self.edit_cd_text_color.editingFinished.connect(self.on_cd_text_color_change)
            self.layout_cd_text_color.addWidget(self.edit_cd_text_color)
            self.layout_main.addLayout(self.layout_cd_text_color)

        # 背景颜色
        self.layout_bg_text_color = QHBoxLayout()
        self.labe_bg_text_color = QLabel("背景颜色")
        self.layout_bg_text_color.addWidget(self.labe_bg_text_color)
        self.edit_bg_text_color = LineEdit(self)
        self.edit_bg_text_color.setText(timer_info.m_bgColor)
        self.edit_bg_text_color.setPlaceholderText('冷却文本颜色, 如#FF0000')
        self.edit_bg_text_color.setClearButtonEnabled(True)
        self.edit_bg_text_color.editingFinished.connect(self.on_bg_text_color_change)
        self.layout_bg_text_color.addWidget(self.edit_bg_text_color)
        self.layout_main.addLayout(self.layout_bg_text_color)

        if bIconTimer:
            # 边框颜色
            self.layout_board_color = QHBoxLayout()
            self.labe_board_color = QLabel("边框颜色")
            self.layout_board_color.addWidget(self.labe_board_color)
            self.edit_board_color = LineEdit(self)
            self.edit_board_color.setText(timer_info.m_boardColor)
            self.edit_board_color.setPlaceholderText('边框颜色, 如#FF0000')
            self.edit_board_color.setClearButtonEnabled(True)
            self.edit_board_color.editingFinished.connect(self.on_board_color_change)
            self.layout_board_color.addWidget(self.edit_board_color)
            self.layout_main.addLayout(self.layout_board_color)

        # 修改按键
        self.hot_key_widgets = []
        for index, keycode in enumerate(timer_info.m_lKeyCode):
            layout_key = QHBoxLayout()
            label_key = QLabel(f"热键")
            layout_key.addWidget(label_key)

            edit_keys = LineEdit(self)
            edit_keys.setText(f"{'、'.join(keycode)}")
            edit_keys.setReadOnly(True)
            edit_keys.Released.connect(CFunctor(self.on_record_keys, index))
            layout_key.addWidget(edit_keys)
            self.layout_main.addLayout(layout_key)

            self.hot_key_widgets.append(layout_key)
            self.hot_key_widgets.append(label_key)
            self._edit_key.append(edit_keys)

        self.button_add_key = PrimaryPushButton("新增热键(加到最后)", self)
        self.button_add_key.clicked.connect(self.on_add_keys)
        self.layout_main.addWidget(self.button_add_key)

        if len(timer_info.m_lKeyCode) > 1:
            self.button_remove_key = PrimaryPushButton("删除热键(最后一个)", self)
            self.button_remove_key.clicked.connect(self.on_remove_key)
            self.button_remove_key.setStyleSheet("background-color: red; color: white;border-radius:5px;")
            self.layout_main.addWidget(self.button_remove_key)

        self.button_reset_pos = PrimaryPushButton("点击重置位置", self)
        self.button_reset_pos.clicked.connect(self.on_reset_pos)
        self.layout_main.addWidget(self.button_reset_pos)

        self.button_delete = PrimaryPushButton("删除定时器", self)
        self.button_delete.clicked.connect(self.on_delete)
        self.button_delete.setStyleSheet("background-color: red; color: white;border-radius:5px;")
        self.layout_main.addWidget(self.button_delete)

        # self.setMinimumSize(120, 50)
        self.adjustSize()

    def on_reset_change(self, bReset):
        self.timer_info.m_bReset = bReset
        self.timer_info.OnEdit()

    def on_trigger_change(self, bTrigger):
        self.timer_info.m_bTriggerInCd = bTrigger
        self.timer_info.OnEdit()

    def on_force_match_change(self, force):
        print("1111111111")
        self.timer_info.m_forceMatch = force
        self.timer_info.OnEdit()

    def on_cycle_change(self, bCycle):
        self.timer_info.m_bCycle = bCycle
        self.timer_info.OnEdit()

    def on_textoricon_change(self, bIconTimer):
        self.timer_info.m_bIconTimer = bIconTimer
        self.timer_info.OnEdit()
        self.close_menu_func()
        core_event.TriggerEvent("REOPEN_MENU")

    def on_voice_change(self, bVoice):
        self.timer_info.m_bVoice = bVoice
        self.timer_info.OnEdit()

    def on_time_change(self):
        sText = self.edit_time.text()
        if not sText:
            return
        self.timer_info.m_fTotalTime = int(sText)
        self.timer_info.m_fTotalTimeMs = self.timer_info.m_fTotalTime * 1000
        self.timer_info.OnEdit()
        pass

    def on_group_change(self):
        sText = self.edit_group.text()
        if not sText:
            return
        self.timer_info.m_groupId = int(sText)
        self.timer_info.OnEdit()
        self.close_menu_func()
        core_event.TriggerEvent("RELOAD_TIMER")
        core_event.TriggerEvent("REOPEN_MENU")
        pass

    def on_font_size_change(self):
        sText = self.edit_font_size.text()
        if not sText:
            return
        self.timer_info.m_iFontSize = int(sText)
        self.timer_info.OnEdit()

    def on_name_change(self):
        sText = self.edit_name.text()
        if not sText:
            return
        self.timer_info.m_sName = sText
        self.timer_info.OnEdit()
        self.close_menu_func()
        core_event.TriggerEvent("REOPEN_MENU")
        pass

    def on_cd_text_change(self):
        sText = self.edit_cd_text.text()
        if not sText:
            return
        self.timer_info.m_sCD = sText
        self.timer_info.OnEdit()

    def on_cd_text_color_change(self):
        sText = self.edit_cd_text_color.text()
        if not sText:
            return
        try:
            oColor = QColor.fromString(sText)
        except:
            return
        self.timer_info.m_cdColor = sText
        self.timer_info.OnEdit()

    def on_ready_text_change(self):
        sText = self.edit_ready_text.text()
        if not sText:
            return
        self.timer_info.m_sReady = sText
        self.timer_info.OnEdit()

    def on_ready_text_color_change(self):
        sText = self.edit_ready_text_color.text()
        if not sText:
            return
        try:
            oColor = QColor.fromString(sText)
        except:
            return
        self.timer_info.m_readyColor = sText
        self.timer_info.OnEdit()

    def on_bg_text_color_change(self):
        sText = self.edit_bg_text_color.text()
        if not sText:
            return
        try:
            oColor = QColor.fromString(sText)
        except:
            return
        self.timer_info.m_bgColor = sText
        self.timer_info.OnEdit()

    def on_board_color_change(self):
        sText = self.edit_board_color.text()
        if not sText:
            return
        try:
            oColor = QColor.fromString(sText)
        except:
            return
        self.timer_info.m_boardColor = sText
        self.timer_info.OnEdit()

    def on_reset_pos(self):
        x, y = QCursor.pos().toTuple()
        self.timer_info.m_tPos = (x, y)
        self.timer_info.OnEdit()
        self.close_menu_func()

    def on_delete(self):
        print("准备删除：", self.timer_info.m_uuid)
        self.timer_info.ChangeSwitch(False)
        self.del_timer_func(self.timer_info.m_uuid)
        # self.close()
        self.close_menu_func()
        core_event.TriggerEvent("REOPEN_MENU")
        pass

    def on_record_keys(self, index):
        print("开始记录热键")
        if self._record_key_index is not None:
            return
        self._record_key_index = index  # 当前正在记录的按键索引
        lineEdit = self._edit_key[index]
        lineEdit.setText("热键记录中...")
        self._cache_keys.clear()
        self._cache_key_lister = core_input.RegisterInputCb(self.cache_keys)
        core_timer.CreateOnceTimer(3000, self.stop_cache_keys, delta=False)
        pass

    def on_add_keys(self):
        print("新增热键")
        self.timer_info.m_lKeyCode.append([])
        self.timer_info.Save()

        bNeedClose = not self.timer_info.m_bOpen
        self.timer_info.ChangeSwitch(True)
        if bNeedClose:
            self.timer_info.ChangeSwitch(False)

    def on_remove_key(self):
        print("删除热键")
        self.timer_info.m_lKeyCode.pop()
        self.timer_info.OnEdit()

        bNeedClose = not self.timer_info.m_bOpen
        self.timer_info.ChangeSwitch(True)
        if bNeedClose:
            self.timer_info.ChangeSwitch(False)

    def cache_keys(self, skey):
        self._cache_keys.append(skey)

    def stop_cache_keys(self):
        print("记录的按键：", self._cache_keys)
        index = self._record_key_index
        self._record_key_index = None
        self._cache_key_lister = None
        self.timer_info.m_lKeyCode[index] = self._cache_keys
        self.timer_info.OnEdit()
        lineEdit = self._edit_key[index]
        lineEdit.setText(f"{'、'.join(self._cache_keys)}")
        self._cache_keys = []

    def on_icon_change(self):
        sText = self.edit_icon.text()
        if sText and not str(sText).endswith(".png") and not str(sText).endswith(".jpg"):
            core_voice.Speak("图标配置请输入timer_icon目录下的图片名， 比如aaa.png")
            return
        self.timer_info.m_sPic = sText
        self.timer_info.OnEdit()
        pass

    def on_mask_change(self):
        sText = self.edit_mask.text()
        if sText and not str(sText).endswith(".png") and not str(sText).endswith(".jpg"):
            core_voice.Speak("遮罩配置请输入timer_icon目录下的图片名， 比如aaa.png")
            return
        self.timer_info.m_sMaskPic = sText
        print(self.timer_info.m_sMaskPic)
        self.timer_info.OnEdit()
        pass

    def on_icon_size_change(self):
        sText = self.edit_icon_size.text()
        if not sText:
            iSize = 32
        else:
            try:
                iSize = int(sText)
            except:
                iSize = 32
        if iSize < 10:
            core_voice.Speak("图标尺寸不能太小了！")
            iSize = 0
        self.timer_info.m_iConSize = iSize
        self.timer_info.OnEdit()

    def on_board_size_change(self):
        sText = self.edit_board_size.text()
        if not sText:
            self.timer_info.m_iBoardSize = 0
        else:
            self.timer_info.m_iBoardSize = int(sText)
        self.timer_info.OnEdit()