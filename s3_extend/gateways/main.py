import os
import sys
import time
import threading
import subprocess

from python_banyan.backplane.backplane import bp
from ws_gateway import ws_gateway
from nl_gateway import nl_gateway


class S3N2:

    def __init__(self):
        bb = threading.Thread(target=bp)
        bb.setDaemon(True)
        bb.start()
        print('backplane started')

        time.sleep(1)

        ww = threading.Thread(target=ws_gateway, daemon=True)
        # ww.setDaemon(True)
        ww.start()
        print('Websocket Gateway started')

        time.sleep(1)

        nn = threading.Thread(target=nl_gateway, daemon=True)
        # nn.setDaemon(True)
        nn.start()
        print('Nl Gateway started ')

        time.sleep(1)


        # open_web = threading.Thread(target=self.open_web, daemon=True)
        # open_web.start()
        # print('open_web started ')
        #
        # time.sleep(1)
        # print('*' * 10 + '程序启动完成' + '*' * 10)

    def open_web(self):
        from selenium import webdriver

        try:
            browser = webdriver.Chrome(sys._MEIPASS + '\\chromedriver.exe')
            url = sys._MEIPASS + '\\web_build\\index.html'
        except:
            # 本地测试
            browser = webdriver.Chrome()
            url = 'file:///D:\PyCharmProjects_WIN\RPA\s3-extend\s3_extend\gateways\web_build\index.html'
        browser.get(url)


def s3n2x():
    """
    Start the extension
    :return:
    """
    S3N2()
    while True:
        try:
            time.sleep(.4)
        except KeyboardInterrupt:
            sys.exit(0)


if __name__ == '__main__':
    # replace with name of function you defined above
    print('*' * 10 + '程序启动中' + '*' * 10)

    s3n2x()
