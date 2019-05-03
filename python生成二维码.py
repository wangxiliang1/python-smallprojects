#sudo pip3 install qrcode
import qrcode
import sys

def run(url,path):
    #生成二维码图片以及扫码跳转的链接地址
    qr_image = qrcode.make(url)
    #二维码保存的路径
    qr_image.save(path)

#argv:获取 "命令行" python/python3 后跟的所有参数
#                 python3 python二维码.py https://www.baidu.com/ /home/wxl/img/baibu.png
args = sys.argv
print(args)
if len(args) != 3:
    print('argv长度无效')
    #等待1秒退出程序
    sys.exit(1)
url = args[1]
print(url)
path = args[2]
print(path)
run(url,path)


# 命令行执行:python3 python二维码.py https://www.baidu.com/ /home/wxl/img/baibu.png
#详解:python3 python二维码.py     运行代码脚本
#    https://www.baidu.com/     扫二维码需要跳转到的页面
#    /home/wxl/img/baidu.png    二维码生成保存的路径,baidu.png,名称自取,以.png格式结尾