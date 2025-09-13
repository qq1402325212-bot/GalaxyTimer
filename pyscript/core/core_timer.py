# --*utf-8*--
# Author：一念断星河
# Crete Data：2024/4/28
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
import time

from .functor import CFunctor


# 写一个python定时器，每隔一段时间执行一次任务

class TimerMgr:
    def __init__(self):
        self._uid = 0
        self._times = {}
        self._iFrame = 0

    def add_timer(self, interval: int, func, count, delta, *args, **kwargs):
        self._uid += 1
        timer = Timer(interval, func, count, delta, *args, **kwargs)
        self._times[self._uid] = timer
        return self._uid

    def remove_timer(self, t_id):
        if t_id in self._times:
            self._times[t_id].Destroy()

    def get_frame(self):
        return self._iFrame

    def update(self, deltaTimeMs):
        self._iFrame += 1
        clears = []
        for t_id in list(self._times.keys()):
            timer = self._times.get(t_id, None)
            if not timer:
                continue
            if timer.IsDestroy():
                clears.append(t_id)
                continue
            timer.TryExecute(deltaTimeMs)

        for t_id in clears:
            del self._times[t_id]


class Timer:
    def __init__(self, interval: int, func, count, delta, *args, **kwargs):
        self._interval = interval
        self._recordTime = time.time() * 1000
        self._nextTime = self._recordTime + interval
        self._count = count
        self._needDelta = delta
        self._func = CFunctor(func, *args, **kwargs)

    def TryExecute(self, deltaTimeMs):
        self._recordTime += deltaTimeMs
        if self._recordTime <= self._nextTime:
            return
        deltaTimeMs = self._interval + self._recordTime - self._nextTime
        self._nextTime = self._recordTime + self._interval
        self._count -= 1
        if self._needDelta:
            self._func(deltaTimeMs)
        else:
            self._func()

    def IsDestroy(self):
        return self._count == 0

    def Destroy(self):
        self._count = 0


class Timer_Ref:
    def __init__(self, uid):
        self.m_Uid = uid

    def __del__(self):
        if g_Instance:
            g_Instance.remove_timer(self.m_Uid)


if "g_Instance" not in globals():
    g_Instance = TimerMgr()


def Initialize():
    pass


def CreateTimer(intervalMs: int, func, count, delta=False, *args, **kwargs):
    """
    创建一个定时器
    :param intervalMs: 定时器间隔时间 MS
    :param func: 定时器回调函数
    :param count: 定时器执行次数
        :param delta: 回调时是否需要传递时间差
    :param args: 参数
    :param kwargs: 参数
    :return: 定时器ID
    """
    uid = g_Instance.add_timer(intervalMs, func, count, delta, *args, **kwargs)
    return Timer_Ref(uid)


def CreateOnceTimer(intervalMs: int, func, delta=False, *args, **kwargs):
    """
    创建一个定时器
    :param intervalMs: 定时器间隔时间 MS
    :param func: 定时器回调函数
    :param count: 定时器执行次数
    :param delta: 回调时是否需要传递时间差
    :param args: 参数
    :param kwargs: 参数
    :return: 定时器ID
    """
    return g_Instance.add_timer(intervalMs, func, 1, delta, *args, **kwargs)


def CreateAlwaysTimer(intervalMs: int, func, delta=False, *args, **kwargs):
    """
    创建一个定时器
    :param intervalMs: 定时器间隔时间 MS
    :param func: 定时器回调函数
    :param count: 定时器执行次数
    :param delta: 回调时是否需要传递时间差
    :param args: 参数
    :param kwargs: 参数
    :return: 定时器ID
    """
    uid = g_Instance.add_timer(intervalMs, func, -1, delta, *args, **kwargs)
    return Timer_Ref(uid)


def UpdateTimer(deltaTimeMs):
    g_Instance.update(deltaTimeMs)


def GetFrameCount():
    return g_Instance.get_frame()