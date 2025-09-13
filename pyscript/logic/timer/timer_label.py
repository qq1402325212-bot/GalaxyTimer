# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/6/3
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
import os
from typing import TYPE_CHECKING

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *

from core import core_input, core_timer
from core import core_voice
from core.core_define import Path_IconRoot

if TYPE_CHECKING:
    from logic.timer.timer_info import TimerProxy


class Timer_Flyout(QLabel):
    def __init__(self, timeProxy: "TimerProxy"):
        super().__init__(None)
        # self.setGeometry(1800, 800, 300, 300)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAutoFillBackground(False)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

        self.timerInfoProxy = timeProxy
        self.m_Timer = None
        self.m_Listens = []

        self._Pixmap = None
        self._MaskPixmap = None
        self._font = None

        self.OnRefresh()

    def OnRefresh(self):
        """
        刷新数据
        """
        self._Pixmap = None
        self._MaskPixmap = None
        self.setText("")

        timeProxy = self.timerInfoProxy

        # 图标
        bIconTimer = timeProxy.m_bIconTimer

        if bIconTimer:
            if self.timerInfoProxy.m_sPic:
                icon_path = os.path.join(Path_IconRoot, self.timerInfoProxy.m_sPic)
                if os.path.exists(icon_path):
                    self._Pixmap = QPixmap()
                    self._Pixmap.load(str(icon_path))
                    self._Pixmap = self._Pixmap.scaled(QSize(self.timerInfoProxy.m_iConSize, self.timerInfoProxy.m_iConSize))

            if self.timerInfoProxy.m_sMaskPic:
                icon_path = os.path.join(Path_IconRoot, self.timerInfoProxy.m_sMaskPic)
                if os.path.exists(icon_path):
                    self._MaskPixmap = QPixmap()
                    self._MaskPixmap.load(str(icon_path))
                    self._MaskPixmap = self._MaskPixmap.scaled(QSize(self.timerInfoProxy.m_iConSize, self.timerInfoProxy.m_iConSize))
            self.resize(self.timerInfoProxy.m_iConSize, self.timerInfoProxy.m_iConSize)
        else:
            # 文本
            self.setText(timeProxy.m_sReady)

        # 字号
        self._font = QFont()
        self._font.setPointSize(self.timerInfoProxy.m_iFontSize)
        self.setFont(self._font)

        # 倒计时
        self.m_fCurTimeMs = timeProxy.m_fTotalTimeMs
        # 热键
        self.m_Listens.clear()
        for keycode in timeProxy.m_lKeyCode:
            if not keycode:
                continue
            proxy = core_input.RegisterHotKey(keycode, self.RefreshCountDown, force_match=self.timerInfoProxy.m_forceMatch)
            self.m_Listens.append(proxy)
        # 定时器
        self.m_Timer = None

        # 适配
        self.adjustSize()

        self.move(*timeProxy.m_tPos)
        self.update()
        pass

    def RefreshCountDown(self):
        """
        重置倒计时
        """
        if self.m_Timer is not None:
            if self.timerInfoProxy.m_bCycle:
                self.OnRefresh()
                if self.timerInfoProxy.m_bVoice:
                    core_voice.Speak(f"{self.timerInfoProxy.m_sReady}")
                return
            if not self.timerInfoProxy.m_bTriggerInCd:
                return
        timeProxy = self.timerInfoProxy

        # 刷新当前时间
        self.m_fCurTimeMs = timeProxy.m_fTotalTimeMs

        # 开启倒计时
        self.m_Timer = core_timer.CreateAlwaysTimer(1, self.OnCountDown, delta=True)
        cycleText = "循环" if self.timerInfoProxy.m_bCycle else ""
        if self.timerInfoProxy.m_bVoice:
            core_voice.Speak(f"{timeProxy.m_sName}开始{cycleText}计时！")

    def OnCountDown(self, deltaMs):
        """
        倒计时持续中
        """
        self.m_fCurTimeMs -= deltaMs
        if self.m_fCurTimeMs <= 0:
            if not self.timerInfoProxy.m_bCycle:
                self.OnRefresh()
                if self.timerInfoProxy.m_bVoice:
                    core_voice.Speak(f"{self.timerInfoProxy.m_sReady}")
                return
            else:
                self.m_fCurTimeMs += self.timerInfoProxy.m_fTotalTimeMs
        bIconTimer = self.timerInfoProxy.m_bIconTimer
        sInfo = self.timerInfoProxy.m_sCD+" " if not bIconTimer else ""
        sInfoUnit = " s" if not bIconTimer else ""
        self.setText(f"{sInfo}{int(self.m_fCurTimeMs / 1000)}{sInfoUnit}")
        self.adjustSize()
        pass

    def adjustSize(self):
        if self.timerInfoProxy.m_bIconTimer:
            w, h = self.timerInfoProxy.m_iConSize, self.timerInfoProxy.m_iConSize
        else:
            fontMetrics = QFontMetrics(self.font())
            textWidth = fontMetrics.horizontalAdvance(self.text())
            textHeight = fontMetrics.height()
            w, h = textWidth + 10, textHeight + 10
        # 考虑到内边距和边框等因素，可能需要添加一些额外的空间  
        self.setFixedSize(w, h)

    def paintEvent(self, event):
        painter = QPainter(self)
        _rect = self.rect()
        x = _rect.x() - 1
        y = _rect.y() - 1
        w = _rect.width() + 2
        h = _rect.height() + 2

        ori_rect = QRect(x, y, w, h)
        iBoard = self.timerInfoProxy.m_iBoardSize
        content_rect = QRect(x + iBoard, y + iBoard, w - 2 * iBoard, h - 2 * iBoard)

        # --------------------- 文本定时器 ---------------------
        if not self.timerInfoProxy.m_bIconTimer:
            painter.setBrush(QBrush(QColor(self.timerInfoProxy.m_bgColor)))
            painter.drawRect(ori_rect)

            if self.m_Timer:
                painter.setPen(QPen(QColor(self.timerInfoProxy.m_cdColor), 2))
            else:
                painter.setPen(QPen(QColor(self.timerInfoProxy.m_readyColor), 2))
            painter.drawText(ori_rect, Qt.AlignCenter, self.text())
            return

        # --------------------- 图标定时器 ---------------------
        # 绘制背景颜色f
        painter.setBrush(QBrush(QColor(self.timerInfoProxy.m_bgColor)))
        painter.drawRect(ori_rect)

        # 图标和遮罩的选择f
        if not self.m_Timer:
            # 如果没有定时器
            if self._Pixmap:
                painter.drawPixmap(content_rect, self._Pixmap)
        else:
            if self._MaskPixmap:
                painter.drawPixmap(content_rect, self._MaskPixmap)
            elif self._Pixmap:
                painter.drawPixmap(content_rect, self._Pixmap)
                painter.setBrush(QBrush(QColor("#66000000")))
                painter.drawRect(ori_rect)

        if iBoard > 0:
            # 绘制边框
            painter.setBrush(QBrush(QColor(self.timerInfoProxy.m_boardColor)))
            x += 0.5
            y += 0.5
            w -= 2
            h -= 2
            up_rect = QRect(x, y, w, iBoard)
            down_rect = QRect(x, y+h-iBoard, w, iBoard)
            left_rect = QRect(x, y, iBoard, h)
            right_rect = QRect(x+w-iBoard, y, iBoard, h)
            painter.drawRect(up_rect)
            painter.drawRect(down_rect)
            painter.drawRect(left_rect)
            painter.drawRect(right_rect)

        # 冷却文本的选择
        if self.m_Timer:
            painter.setPen(QPen(QColor(self.timerInfoProxy.m_cdColor), 2))
        else:
            painter.setPen(QPen(QColor(self.timerInfoProxy.m_readyColor), 2))
        painter.drawText(content_rect, Qt.AlignCenter, self.text())

    def IsColorValid(self, color):
        return not str(color).startswith("#00")

    def mousePressEvent(self, QMouseEvent):
        self.pos_first = None
        if QMouseEvent.button() == Qt.LeftButton:
            self.pos_first = QMouseEvent.globalPos() - self.pos()
            QMouseEvent.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))
            return

    def mouseMoveEvent(self, QMouseEvent):
        if not self.pos_first:
            return
        if Qt.LeftButton:
            self.move(QMouseEvent.globalPos() - self.pos_first)
            # self.x, self.y = self.pos().x, self.pos().y
            # self.timerInfoProxy.m_tPos = self.xy()
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        if QMouseEvent.button() != Qt.LeftButton:
            return
        if self.xy() != self.timerInfoProxy.m_tPos:
            pos = self.xy()
            self.timerInfoProxy.m_tPos = int(pos[0]), int(pos[1])
            self.timerInfoProxy.Save()

    def xy(self):
        pos = self.pos()
        return pos.x(), pos.y()
