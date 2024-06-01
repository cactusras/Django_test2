from datetime import date, datetime, time
from json import JSONEncoder

class CustomEncoder(JSONEncoder):
    def default(self, obj):
        # 自定義你的編碼邏輯，例如處理特定的數據類型
        # 這裡是一個示例，可以根據你的需求進行調整
        if isinstance(obj, time):
            print(obj, 'is time')
            return obj.strftime('%H:%M')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            print(obj, 'is others')
            return super().default(obj)
