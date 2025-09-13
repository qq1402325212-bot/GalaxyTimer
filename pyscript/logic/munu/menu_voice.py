# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/6/4
# Desc：不过是大梦一场空，不过是孤影照惊鸿。

from PySide6.QtCore import Qt
from PySide6.QtWidgets import *

from core import core_voice
from widgets.slider import Slider
from widgets.switch_button import SwitchButton


class Voice_Menu(QWidget):
	def __init__(self):
		super().__init__(None)
		self.setup_ui()
	
	def setup_ui(self):
		# 主布局 MAIN LAYOUT
		self.layout_main = QVBoxLayout(self)
		self.layout_main.setContentsMargins(10, 10, 10, 10)
		self.layout_main.setSpacing(10)
		
		voice_instance = core_voice.g_Instance
		
		# 开关
		self.layout_switch = QHBoxLayout()
		self.label_switch = QLabel("语音总开关")
		self.layout_switch.addWidget(self.label_switch)
		self.button_switch = SwitchButton("", "")
		self.button_switch.setChecked(voice_instance.m_Switch)
		self.button_switch.checkedChanged.connect(self.on_change_switch)
		self.layout_switch.addWidget(self.button_switch)
		self.layout_main.addLayout(self.layout_switch)
		
		# 修改音量
		self.layout_volume = QHBoxLayout()
		self.label_volume = QLabel("语音音量")
		self.layout_volume.addWidget(self.label_volume)
		self.slider_volume = Slider(Qt.Horizontal, self)
		self.slider_volume.sliderReleased.connect(self.on_change_volume)
		self.slider_volume.setRange(0, 100)
		self.slider_volume.setValue(voice_instance.m_volume*100)
		self.layout_volume.addWidget(self.slider_volume)
		self.layout_main.addLayout(self.layout_volume)
		
		# 修改语速
		self.layout_rate = QHBoxLayout()
		self.label_rate = QLabel("语音语速")
		self.layout_rate.addWidget(self.label_rate)
		self.slider_rate = Slider(Qt.Horizontal, self)
		self.slider_rate.setRange(1, 400)
		self.slider_rate.setValue(voice_instance.m_rate)
		self.slider_rate.sliderReleased.connect(self.on_change_rate)
		self.layout_rate.addWidget(self.slider_rate)
		self.layout_main.addLayout(self.layout_rate)
		
		self.adjustSize()
	
	def on_change_switch(self, bSwitch):
		voice_instance = core_voice.g_Instance
		voice_instance.Switch(bSwitch)
		voice_instance.Save()
	
	def on_change_volume(self):
		voice_instance = core_voice.g_Instance
		iVolume = self.slider_volume.value() / 100
		voice_instance.SetVolume(iVolume)
		voice_instance.Save()
	
	def on_change_rate(self):
		voice_instance = core_voice.g_Instance
		iRate = self.slider_rate.value()
		voice_instance.SetRate(iRate)
		voice_instance.Save()
