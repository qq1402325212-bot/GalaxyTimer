# --*utf-8*--
# Author：一念断星河
# Crete Data： 2025/5/18
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
from core import core_save
from core.core_define import Path_Group


class GroupProxy:
    def __init__(self, uid, data):
        self.m_uuid = int(uid)  # 分组uid
        self.m_sName = data.get('sName', "新建分组")
        self.m_bOpen = data.get('bOpen', False)  # 是否开启
        self.m_lTimer= []  # 当前组内定时器代理

    def ChangeSwitch(self, bSwitch):
        self.m_bOpen = bSwitch
        for timer in self.m_lTimer:
            timer.ChangeSwitch(bSwitch)
        self.Save()

    def Save(self):
        try:
            data = core_save.LoadJson(Path_Group)
            self.m_uuid = int(self.m_uuid)
            time_info = data.get(str(self.m_uuid), {})
            time_info["sName"] = self.m_sName
            time_info["bOpen"] = self.m_bOpen
            data[str(self.m_uuid)] = time_info
            core_save.SaveJson(Path_Group, data)
        except IOError as e:
            print(e)
            pass
        pass