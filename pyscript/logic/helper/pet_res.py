# --*utf-8*--
# Author：一念断星河
# Crete Data： 2024/12/1
# Desc：不过是大梦一场空，不过是孤影照惊鸿。
import os
from core.core_define import Path_PetRoot


class PetRes:
    def __init__(self):
        self.m_ResName = ""
        self.m_ResPath = ""
        self.m_ResCount = 0
        self.m_CurResIndex = 0

    def LoadRes(self, sFileName):
        self.m_ResName = sFileName
        self.m_ResPath = os.path.join(Path_PetRoot, sFileName)
        for _path in os.listdir(str(self.m_ResPath)):
            if not _path.endswith(".png"):
                continue
            self.m_ResCount += 1

    def HasRes(self):
        return bool(self.m_ResCount)

    def IsNeedUpdate(self):
        return bool(self.m_ResCount > 1)

    def GetNextRes(self):
        self.m_CurResIndex += 1
        if self.m_CurResIndex > self.m_ResCount:
            self.m_CurResIndex = 1
        return os.path.join(self.m_ResPath, f"{self.m_CurResIndex}.png")

    def __repr__(self):
        return f"PetRes: 名字-{self.m_ResName} 路径-{self.m_ResPath} 帧动画数量-{self.m_ResCount}"