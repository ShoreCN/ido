
import jpush as jpush
class JPush():
    def __init__(self, AppKey, Secret):
        self.AppKey = AppKey
        self.Secret = Secret
    def GetKeyAndSecret(self):
        return self.AppKey, self.Secret

    def SendAlias(self, aAlias,szInfo,pJson = {}, szCaption = ''):
        app_key, master_secret = self.GetKeyAndSecret()
        _jpush = jpush.JPush(app_key, master_secret)
        # _jpush.set_logging("DEBUG")
        push = _jpush.create_push()
        alias1 = {"alias": aAlias}
        # print(alias1)
        push.audience = jpush.audience(
            alias1
        )

        ios_msg = jpush.ios(alert=szInfo, badge="+1", sound="a.caf", extras=pJson)
        android_msg = jpush.android(alert=szInfo)
        push.notification = jpush.notification(alert=szCaption, android=android_msg, ios=ios_msg)
        push.message = jpush.message("content", extras=pJson)
        push.platform = jpush.all_
        # print(push.payload)
        push.options = {"time_to_live": 86400, "sendno": 12345, "apns_production": False}
        push.send()

    def SendNotify(self, szCaption, szInfo, pJson):
        # if Config.environment == 'DEBUG':
        #     return
        app_key, master_secret = self.GetKeyAndSecret()

        import jpush as jpush
        # from conf import app_key, master_secret
        _jpush = jpush.JPush(app_key, master_secret)
        # _jpush.set_logging("DEBUG")
        push = _jpush.create_push()
        push.audience = jpush.all_
        ios_msg = jpush.ios(alert=szInfo, badge="+1", sound="a.caf", extras=pJson)
        android_msg = jpush.android(alert=szInfo)
        push.notification = jpush.notification(alert=szCaption, android=android_msg, ios=ios_msg)
        push.message = jpush.message("content", extras=pJson)
        push.platform = jpush.all_
        apns_production = True
        push.options = {"time_to_live": 86400, "sendno": 12345, "apns_production": False}
        push.send()

    def SendAll(self, szInfo, pJson = {}):
        app_key, master_secret = self.GetKeyAndSecret()
        import jpush as jpush
        # from conf import app_key, master_secret
        _jpush = jpush.JPush(app_key, master_secret)
        # _jpush.set_logging("DEBUG")
        push = _jpush.create_push()
        push.audience = jpush.all_
        ios_msg = jpush.ios(alert=szInfo, badge="+1", sound="a.caf", extras=pJson)
        android_msg = jpush.android(alert=szInfo)
        push.notification = jpush.notification(alert=u"买卖点", android=android_msg, ios=ios_msg)
        push.message = jpush.message("content", extras=pJson)
        push.platform = jpush.all_
        apns_production = True
        push.options = {"time_to_live": 86400, "sendno": 12345, "apns_production": False}
        push.send()



