# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/6/4
# Desc：不过是大梦一场空，不过是孤影照惊鸿。

from PySide6.QtGui import QFontMetrics
from PySide6.QtWidgets import *


class Help_Info(QWidget):
	def __init__(self):
		super().__init__(None)
		self.setup_ui()

	def setup_ui(self):
		# 主布局 MAIN LAYOUT
		self.layout_main = QVBoxLayout(self)
		self.layout_main.setContentsMargins(4, 4, 4, 4)

		# 修改热键生效超时时长
		self.label = QLabel()
		self.label.setText("B站搜索\n【艾尔之光】GalaxyTimer\nUP主：一念断星河")
		self.adjustSizeToText()
		self.layout_main.addWidget(self.label)
		self.adjustSize()

	def adjustSizeToText(self):

		metrics = QFontMetrics(self.label.font())

		sText = self.label.text()
		lText = sText.split("\n")

		textW, textH = 0, 0
		for text in lText:
			if not text:
				continue
			textW = max(metrics.horizontalAdvance(text), textW)
			textH += metrics.height()

		# 考虑到内边距和边框等因素，可能需要添加一些额外的空间  
		self.label.setFixedSize(textW + 80, textH + 10)
