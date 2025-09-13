# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/6/3
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
import threading
import keyboard


from core import core_timer, core_save
from core.core_define import Path_Setting, SettingName
from core.functor import CFunctor

if "g_HotKeyTimeOut" not in globals():
	data = core_save.LoadJson(Path_Setting)
	g_HotKeyTimeOut = data.get(SettingName.TimerResetTime, 2000)


class KeyType:
	Press = 0
	Release = 1
	Hold = 2


class Listerner_Ref:
	def __init__(self, uid):
		self.m_Uid = uid

	def __del__(self):
		if g_Instance:
			g_Instance.RemoveHotKey(self.m_Uid)


class Listerner:
	def __init__(self, uid, keys, func, key_type=KeyType.Press, force_match=False):
		self.m_Uid = uid
		lKey = []
		for _k in keys:
			lKey.append(_k.lower())
		keys = lKey
		self.m_HotKeys = keys
		self.m_ForceMatch = force_match
		self.m_OriKeys = keys.copy()
		self.m_Func = CFunctor(func)
		self.m_KeyType = key_type
		self.m_TimerProxy = None
		self.m_bAllKeys = False
		self.m_bDetect = False

	def TryActive(self, skey, key_type=KeyType.Press):
		if key_type != self.m_KeyType:
			return
		if self.m_bAllKeys:
			if self.m_Func.IsAlive():
				self.m_Func(skey)
			return
		if self.m_HotKeys[0] != skey:
			if self.m_ForceMatch:
				self._Revert()
			return
		self.m_bDetect = True
		self.m_HotKeys.pop(0)

		if self.m_HotKeys:
			if self.m_TimerProxy:
				return
			self.m_TimerProxy = core_timer.CreateOnceTimer(g_HotKeyTimeOut, self._Revert, delta=False)
			return

		self._Revert()
		if not self.m_Func.IsAlive():
			return
		self.m_Func()

	def _Revert(self):
		if not self.m_bDetect:
			return
		self.m_HotKeys = self.m_OriKeys.copy()
		self.m_TimerProxy = None
		self.m_bDetect = False


class Input:
	def __init__(self):
		self.m_uid = 0
		self.m_dListen = {}  # 所有的按键监听器
		self.m_DelCache = []  # 待删除的按键监听器ID列表
		self.m_AddCache = []  # 待添加的按键监听器ID列表
		self.m_lPress = []  # 本轮按键按下列表
		self.m_lHold = []  # 本轮按键按住列表
		self.m_lRelease = []  # 本轮按键释放列表
		self.m_oLock = threading.Lock()  # 线程锁

	def StartListen(self):
		listener_thread = threading.Thread(target=self._keyboard_listener, daemon=True)
		listener_thread.start()

	def _keyboard_listener(self):
		# 监听所有按键按下事件
		keyboard.hook(self._key_hook)
		# 保持程序运行，直到用户中断
		keyboard.wait()

	def _key_hook(self, event):
		sKey = str(event.name).lower()
		sType = str(event.event_type)
		if sType == "down":
			self._on_press(sKey)
		else:
			self._on_release(sKey)

	def _on_press(self, sKey):
		self.m_oLock.acquire()
		if sKey not in self.m_lHold:
			# print("按键按下：", sKey, time.time()*1000)
			self.m_lPress.append(sKey)
			self.m_lHold.append(sKey)
		self.m_oLock.release()

	def _on_release(self, sKey):
		self.m_oLock.acquire()
		self.m_lRelease.append(sKey)
		if sKey in self.m_lHold:
			self.m_lHold.remove(sKey)
		# print("按键释放：", sKey, time.time()*1000)
		self.m_oLock.release()

	def IsKeyHold(self, skey:str):
		skey = skey.lower()
		return skey in self.m_lHold

	def Update(self):
		self.m_oLock.acquire()
		try:
			if self.m_AddCache:
				for oListen in self.m_AddCache:
					self.m_dListen[oListen.m_Uid] = oListen
				self.m_AddCache.clear()
			for sKey in self.m_lPress:
				for uid, oListen in self.m_dListen.items():
					if uid in self.m_DelCache:
						continue
					oListen.TryActive(sKey, KeyType.Press)
			for sKey in self.m_lRelease:
				for uid, oListen in self.m_dListen.items():
					if uid in self.m_DelCache:
						continue
					oListen.TryActive(sKey, KeyType.Release)
			for sKey in self.m_lHold:
				for uid, oListen in self.m_dListen.items():
					if uid in self.m_DelCache:
						continue
					oListen.TryActive(sKey, KeyType.Hold)

			for uid in self.m_DelCache:
				if uid in self.m_dListen:
					del self.m_dListen[uid]
		finally:
			self.m_DelCache.clear()
			self.m_lPress.clear()
			self.m_lRelease.clear()
			self.m_oLock.release()

	def RegisterHotKey(self, keys, func, key_type=KeyType.Press, force_match=False):
		if not func or not keys:
			return
		self.m_uid += 1
		uid = self.m_uid

		if type(keys) is not list:
			keys = [keys]
		else:
			keys = keys.copy()
		oListen = Listerner(uid, keys, func, key_type, force_match)
		self.m_AddCache.append(oListen)
		# self.m_dListen[uid] = oListen
		return Listerner_Ref(uid)

	def RegisterInputCb(self, func):
		if not func:
			return
		self.m_uid += 1
		uid = self.m_uid
		oListen = Listerner(uid, [], func)
		oListen.m_bAllKeys = True
		self.m_dListen[uid] = oListen
		return Listerner_Ref(uid)

	def RemoveHotKey(self, uid):
		if uid in self.m_dListen:
			self.m_DelCache.append(uid)


if "g_Instance" not in globals():
	g_Instance = Input()

# ------------------- api --------------------
Initialize = g_Instance.StartListen
Update = g_Instance.Update
RegisterHotKey = g_Instance.RegisterHotKey
RegisterInputCb = g_Instance.RegisterInputCb
IsKeyHold = g_Instance.IsKeyHold
