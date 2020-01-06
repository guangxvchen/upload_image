import os


# 判断路径是否存在
def isPath(path):
    return os.path.exists(path)


# 创建目录
def createPath(path):
    # 创建目录
    # os.mkdir(path)
    # 创建多层目录
    os.makedirs(path)
