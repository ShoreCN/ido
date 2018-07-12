import platform
import os

class Config():
    def __init__(self):
        self.environment = 'DEBUG'
    def CheckEnv(self):
        if platform.system() != 'Windows':
            szPath = os.path.abspath(__file__)
            try:
                szPath.index('Test')
                self.environment = 'DEBUG'
            except:
                self.environment = ''
    def IsDebug(self):
        if self.environment == 'DEBUG':
            return True
        return False
    def GetDbName(self):
        if self.IsDebug():
           return 'TestIDO'
        return "IDO"
    def GetPublicDbName(self):
        return "Public"
    def GetWfSvcPort(self):
        if self.IsDebug():
            return 7711
        return 7712
    def GetCoreSvcPort(self):
        return 6612