# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/6/3
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
import weakref

from core import core_save
from core.core_define import Path_Timer, Path_Setting, SettingName
from logic.timer.timer_label import Timer_Flyout


class TimerProxy:
	def __init__(self, uid, data):
		self.m_uuid = int(uid)
		self.m_sName = data.get('sName', "新建定时器")
		self.m_sCD = data.get('sCDText', '冷却中')
		self.m_sPic = data.get('sPic', "")
		self.m_sMaskPic = data.get('sMaskPic', "")
		self.m_sReady = data.get('sReadyText', '已就绪')
		self.m_fTotalTime = int(data.get('iTime', 3))
		self.m_fTotalTimeMs = self.m_fTotalTime * 1000
		self.m_iFontSize = int(data.get('iFontSize', 18))
		self.m_iConSize = int(data.get('iConSize', 50))
		self.m_iBoardSize = int(data.get('iBoardSize', 0))
		self.m_lKeyCode = data.get('lKeyCode', [])
		self.m_bOpen = data.get('bOpen', False)  # 是否开启
		self.m_bReset = data.get('bReset', False)  # 允许被重置
		self.m_bTriggerInCd = data.get('bTriggerInCd', True)  # 允许冷却时触发
		self.m_bCycle = data.get('bCycle', False)  # 循环触发
		self.m_bVoice = data.get('bVoice', True)  # 语音播报
		self.m_bIconTimer = data.get('bIconTimer', True)  # 文本|图标定时器
		self.m_tPos = tuple(data.get('tPos', (0, 0)))
		self.m_tPos = int(self.m_tPos[0]), int(self.m_tPos[1])
		self.m_cdColor = data.get('cdColor', "#FF0000")
		self.m_readyColor = data.get('readyColor', "#00FFFF")
		self.m_bgColor = data.get('bgColor', "#00000000")
		self.m_boardColor = data.get('boardColor', "#000000")
		self.m_groupId = data.get('groupId', 0)
		self.m_forceMatch = data.get('force_match', False)
		self.m_FlyView: "Timer_Flyout" = None

		# 存档兼容
		if not self.m_lKeyCode:
			self.m_lKeyCode = [[]]
			self.Save()
		if self.m_lKeyCode and type(self.m_lKeyCode[0]) == str:
			self.m_lKeyCode = [self.m_lKeyCode]
			self.Save()

		if self.m_bOpen:
			self._CreateFlyView()
	
	def Reset(self):
		# 不允许重置
		if not self.m_bReset:
			return
		if not self.m_bOpen:
			return
		self.m_FlyView.OnRefresh()

	def OnEdit(self):
		self.Save()
		if not self.m_bOpen:
			return
		self.m_FlyView.OnRefresh()
	
	def ChangeSwitch(self, bSwitch):
		if self.m_bOpen == bSwitch:
			return
		if not bSwitch:
			if self.m_FlyView:
				self.m_FlyView.close()
				self.m_FlyView = None
			self.m_bOpen = False
			self.Save()
		else:
			self._CreateFlyView()
			self.m_bOpen = True
			self.Save()
		pass
	
	def _CreateFlyView(self):
		if self.m_FlyView:
			self.m_FlyView.close()
		self.m_FlyView = Timer_Flyout(weakref.proxy(self))
		self.m_FlyView.show()
	
	def Save(self):
		try:
			data = core_save.LoadJson(Path_Timer)
			self.m_uuid = int(self.m_uuid)
			time_info = data.get(str(self.m_uuid), {})
			time_info["sName"] = self.m_sName
			time_info["sCDText"] = self.m_sCD
			time_info["sPic"] = self.m_sPic
			time_info["sMaskPic"] = self.m_sMaskPic
			time_info["sReadyText"] = self.m_sReady
			time_info["iTime"] = self.m_fTotalTime
			time_info["lKeyCode"] = self.m_lKeyCode
			time_info["bOpen"] = self.m_bOpen
			time_info["bReset"] = self.m_bReset
			time_info["bTriggerInCd"] = self.m_bTriggerInCd
			time_info["bCycle"] = self.m_bCycle
			time_info["bVoice"] = self.m_bVoice
			time_info["bIconTimer"] = self.m_bIconTimer
			time_info["iFontSize"] = self.m_iFontSize
			time_info["iBoardSize"] = self.m_iBoardSize
			time_info["iConSize"] = self.m_iConSize
			time_info["cdColor"] = self.m_cdColor
			time_info["readyColor"] = self.m_readyColor
			time_info["bgColor"] = self.m_bgColor
			time_info["boardColor"] = self.m_boardColor
			time_info["groupId"] = self.m_groupId
			time_info["force_match"] = self.m_forceMatch
			time_info["tPos"] = [int(self.m_tPos[0]), int(self.m_tPos[1])]
			
			data[str(self.m_uuid)] = time_info
			core_save.SaveJson(Path_Timer, data)
		except IOError as e:
			print(e)
			pass
		pass
	
	def OnMove(self, qPoint):
		if not self.m_FlyView:
			return
		self.m_FlyView.move(qPoint)
		pass
