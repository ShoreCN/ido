# 错误处理中心
class ErrorCenter():
    def __init__(self):
        self.pCanRetry = {}
        self.pCanRetry['DB'] = {}
    def CanRetry(self, szType, szCode):
        try:
            if szCode in self.pCanRetry['szType']:
                return True
        except:
            pass
        return False