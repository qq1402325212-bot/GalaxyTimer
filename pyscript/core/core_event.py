# --*utf-8*--
# Author：一念断星河
# Crete Data：2023/10/15
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
import weakref


class CTrigger:
    def __init__(self, func, bind_obj=None):
        self.m_bDestroy = False
        self.m_temp = func
        self.m_oRefFunc = weakref.ref(func)
        self.m_oRefObj = weakref.ref(bind_obj) if bind_obj else None

    def Destroy(self):
        self.m_bDestroy = True

    def isActive(self):
        if self.m_bDestroy:
            return False
        if not self.m_oRefFunc():
            return False
        if self.m_oRefObj and not self.m_oRefObj():
            return False
        return True

    def __call__(self, args, kwargs):
        self.m_oRefFunc()(*args, **kwargs)


class CEventObj:
    def __init__(self):
        self.m_id = 0
        self.m_dTrigger = {}
        self.m_bInTrigger = False
        self.m_bDirty = False

    def AddTrigger(self, func, bindObj=None):
        self.m_id += 1
        triggerId = self.m_id
        oFunc = CTrigger(func, bindObj)
        self.m_dTrigger[triggerId] = oFunc
        return triggerId

    def RemoveTrigger(self, triggerId):
        if triggerId is None:
            for k, oTrigger in self.m_dTrigger.items():
                oTrigger.Destroy()
        else:
            if triggerId not in self.m_dTrigger:
                return
            oTrigger = self.m_dTrigger[triggerId]
            oTrigger.Destroy()
        if self.m_bInTrigger:
            self.m_bDirty = True
            return
        self.ClearTrigger()

    def ClearTrigger(self):
        lRemove = []
        for k, oTrigger in self.m_dTrigger.items():
            if not oTrigger.isActive():
                lRemove.append(oTrigger)
        for k in lRemove:
            del self.m_dTrigger[k]
        self.m_bDirty = False

    def __call__(self, args, kwargs):
        lRemove = []
        self.m_bInTrigger = True
        for k, oTrigger in self.m_dTrigger.items():
            if not oTrigger.isActive():
                lRemove.append(k)
                continue
            oTrigger(args, kwargs)
        self.m_bInTrigger = False
        for k in lRemove:
            del self.m_dTrigger[k]
        if self.m_bDirty:
            self.ClearTrigger()

    def isActive(self):
        return len(self.m_dTrigger) > 0


class CTriggerRef:
    def __init__(self, eventKey, triggerId):
        self.m_eventId = eventKey
        self.m_triggerId = triggerId

    def __del__(self):
        g_Instance.RemoveEventTrigger(self.m_eventId, self.m_triggerId)


class CEventSystem:
    def __init__(self):
        self.m_dEventMap = {}
        self.m_iDeep = 0

    def RemoveEventTrigger(self, eventKey, triggerId=None):
        if eventKey not in self.m_dEventMap:
            return
        oEvent = self.m_dEventMap[eventKey]
        oEvent.RemoveTrigger(triggerId)

    def BindEvent(self, eventKey, oFunc, bindObj=None):
        if not oFunc:
            return None
        if eventKey not in self.m_dEventMap.keys():
            self.m_dEventMap[eventKey] = CEventObj()
        oEvent = self.m_dEventMap[eventKey]
        triggerId = oEvent.AddTrigger(oFunc, bindObj)
        return triggerId

    def AddEventTrigger(self, eventKey, oFunc, bindObj=None):
        if eventKey not in self.m_dEventMap.keys():
            self.m_dEventMap[eventKey] = CEventObj()
        oEvent = self.m_dEventMap[eventKey]
        triggerId = oEvent.AddTrigger(oFunc, bindObj)
        return CTriggerRef(eventKey, triggerId)

    def TriggerEvent(self, eventKey, args, kwargs):
        if eventKey not in self.m_dEventMap:
            return
        oEvent = self.m_dEventMap[eventKey]
        self.m_iDeep += 1
        if self.m_iDeep > 100:
            self.m_iDeep = 0
            print(f"EventSystem.TriggerEvent {eventKey} too deep")
            return
        oEvent(args, kwargs)
        self.m_iDeep -= 1


if "g_Instance" not in globals():
    g_Instance = CEventSystem()


def Initialize():
    pass


def BindEvent(eventKey, oFunc, bindObj=None):
    """绑定事件, 不需要保存返回值, 会自动保存"""
    return g_Instance.BindEvent(eventKey, oFunc, bindObj)


def AddEventTrigger(eventKey, oFunc, bindObj=None):
    """绑定事件, 需要保存返回值, 删除会自动清理"""
    return g_Instance.AddEventTrigger(eventKey, oFunc, bindObj)


def TriggerEvent(eventKey, *args, **kwargs):
    """触发事件"""
    # 这里不解包了, 传入的参数是一个元组和一个字典
    # 实际调用的时候, 再自动解包
    g_Instance.TriggerEvent(eventKey, args, kwargs)


def RemoveEventTrigger(eventKey, triggerId=None):
    """移除事件"""
    g_Instance.RemoveEventTrigger(eventKey, triggerId)
