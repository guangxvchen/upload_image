import time


# 返回一个当前 formats 的时间类型
def timeFormat(formats):
    return time.strftime(formats, time.localtime())
