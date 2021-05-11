#!/usr/bin/env python3

"""
 This is the Python Banyan GUI that communicates with
 the Newland Banyan Gateway

 Copyright (c) 2019 Alan Yorinks All right reserved.

 Python Banyan is free software; you can redistribute it and/or
 modify it under the terms of the GNU AFFERO GENERAL PUBLIC LICENSE
 Version 3 as published by the Free Software Foundation; either
 or (at your option) any later version.
 This library is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 General Public License for more details.

 You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
 along with this library; if not, write to the Free Software
 Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
import argparse
import signal
from subprocess import run
import sys
import time
import logging
import pathlib
import pandas as pd
import os
import json
import csv
import xlwt
# import dealPicApi
# import auto_Write
# import wechat_demo
# import webComponents

from python_banyan.gateway_base import GatewayBase

import zmq

# noinspection PyAbstractClass
import dealPicApi, auto_Write, webComponents, wechat_demo


class NlGateway(GatewayBase):
    """
    This class implements a Banyan gateway for the Raspberry Pi
    GPIO pins. It implements the Common Unified GPIO Message
    Specification.

    If pipgiod is not currently running, it will start it, and
    no backplane ip address was specified, a local backplane
    will be automatically started. If you specify a backplane
    ip address, you will need to start that backplane manually.
    """

    def __init__(self, *subscriber_list, **kwargs):
        """
        Initialize the class for operation
        :param subscriber_list: A list of subscription topics
        :param kwargs: Command line arguments - see bg4rpi()
                       at the bottom of this file.
        """

        # initialize the parent
        super(NlGateway, self).__init__(subscriber_list=subscriber_list,
                                        back_plane_ip_address=kwargs['back_plane_ip_address'],
                                        subscriber_port=kwargs['subscriber_port'],
                                        publisher_port=kwargs['publisher_port'],
                                        process_name=kwargs['process_name']
                                        )
        log = kwargs['log']
        self.log = log
        if self.log:
            fn = str(pathlib.Path.home()) + "/nlgw.log"
            self.logger = logging.getLogger(__name__)
            logging.basicConfig(filename=fn, filemode='w', level=logging.DEBUG)
            sys.excepthook = self.my_handler

        self.logger.debug("1111111111111")

        # start the banyan receive loop
        try:
            self.receive_loop()
        except KeyboardInterrupt:
            self.clean_up()
            sys.exit(0)

    def additional_banyan_messages(self, topic, payload):
        """
        This method will pass any messages not handled by this class to the
        specific gateway class. Must be overwritten by the hardware gateway
        class.
        :param topic: message topic
        :param payload: message payload
        """
        self.logger.info("type is {0}".format(payload['command']))
        if payload['command'] == 'write_txt':
            self.write_txt(None, payload)
        if payload['command'] == 'out_Put_Screen':
            self.out_Put_Screen(None, payload)
        if payload['command'] == 'test_transmit':
            self.test_transmit(None, payload)
        if payload['command'] == 'formDistinguish_invoice':
            self.formDistinguish_invoice(None, payload)
        if payload['command'] == 'create_CSV':
            self.create_CSV(None, payload)
        if payload['command'] == 'auto_Write':
            self.auto_Write_Out(None, payload)
        if payload['command'] == 'auto_Web_Download':
            self.auto_Web_Download(None, payload)
        if payload['command'] == 'auto_Web_Upload':
            self.auto_Web_Upload(None, payload)
        if payload['command'] == 'send_Wechat':
            self.send_Wechat(None, payload)

        if payload['command'] == 'open_Web':
            self.open_Web(None, payload)
        if payload['command'] == 'web_Input':
            self.web_Input(None, payload)
        if payload['command'] == 'web_Wait':
            self.web_Wait(None, payload)
        if payload['command'] == 'wait_Until_Xpath':
            self.wait_Until_Xpath(None, payload)
        if payload['command'] == 'web_Click':
            self.web_Click(None, payload)
        if payload['command'] == 'switch_Iframe':
            self.switch_Iframe(None, payload)
        if payload['command'] == 'switch_Window':
            self.switch_Window(None, payload)
        if payload['command'] == 'web_GetValue':
            self.web_GetValue(None, payload)
        if payload['command'] == 'web_Value_Return':
            self.web_Value_Return(None, payload)
        if payload['command'] == 'web_PutValue':
            self.web_PutValue(None, payload)

        if payload['command'] == 'init_Oracle_Db':
            self.init_Oracle_Db(None, payload)
        if payload['command'] == 'init_Mysql_Db':
            self.init_Mysql_Db(None, payload)
        if payload['command'] == 'oracle_Write_To_Db':
            self.oracle_Write_To_Db(None, payload)
        if payload['command'] == 'mysql_Write_To_Db':
            self.mysql_Write_To_Db(None, payload)
        if payload['command'] == 'refresh_Web':
            self.refresh_Web(None, payload)
        if payload['command'] == 'read_File_Line':
            self.read_File_Line(None, payload)
        if payload['command'] == 'get_Now_Time':
            self.get_Now_Time(None, payload)

    def write_txt(self, topic, payload):
        self.logger.info("the txt_path is: {0}".format(payload['txt_path']))
        txt_path = payload['txt_path']
        a = [1, 2, 3]
        b = [4, 5, 6]
        data = pd.DataFrame({'a': a, 'b': b})
        df = pd.DataFrame(data)
        df.to_csv(txt_path, index=None, mode='a')
        self.logger.info("123321")

    def out_Put_Screen(self, topic, payload):
        self.logger.info("out_Put_Screen")
        print_info = str(payload['print_info'])
        print('print_info=' + print_info)

    def test_transmit(self, topic, payload):
        self.logger.info("aaaaa")
        trans_num = int(payload['trans_num'])
        print("testRes:", trans_num * 5)
        payload = {'report': 'sonar_data', 'value': trans_num * 5}
        self.publish_payload(payload, 'from_nl_gateway')

    def formDistinguish_invoice(self, topic, payload):
        self.logger.info("formDistinguish_invoice")
        csv_path = payload['csv_path']
        image_path = payload['image_path']
        self.logger.info(csv_path)
        self.logger.info(image_path)

        print(image_path)
        all_File = self.all_path(image_path)

        proj = ["发票代码", "发票号码", "开票日期", "合计金额", "合计税额", "价税合计", "购方名称", "购方税号", "购方地址电话", "开户行及账号"]
        book = xlwt.Workbook()
        sheet = book.add_sheet('Sheet1')
        for i in range(0, len(proj)):
            sheet.write(0, i, proj[i])  # 插入标题

        line = 1
        for filePath in all_File:
            print(filePath)
            self.logger.info(filePath)
            text = json.loads(dealPicApi.screenshot_ocr().do_ocr(filePath).replace("￥", "").replace("'", "\""))
            self.logger.info(text)

            d = [text['发票代码'],
                 text['发票号码'],
                 text['开票日期'],
                 text['合计金额'],
                 text['合计税额'],
                 text['价税合计'],
                 text['购方名称'],
                 text['购方税号'],
                 text['购方地址电话'],
                 text['开户行及账号']]

            for i in range(0, len(d)):
                sheet.write(line, i, d[i])  # 插入数据
            line = line + 1

        book.save(csv_path)

    def all_path(self, dirname):
        result = []  # 所有的文件
        filter = [".png", ".jpg"]
        for maindir, subdir, file_name_list in os.walk(dirname):
            # print("1:",maindir) #当前主目录
            # print("2:",subdir) #当前主目录下的所有目录
            # print("3:",file_name_list)  #当前主目录下的所有文件
            for filename in file_name_list:
                apath = os.path.join(maindir, filename)  # 合并成一个完整路径
                ext = os.path.splitext(apath)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容

                if ext in filter:
                    result.append(apath)
        return result

    def create_CSV(self, topic, payload):
        self.logger.info("create_CSV")
        csv_path = payload['csv_path']
        self.logger.info(csv_path)
        book = xlwt.Workbook()
        sheet = book.add_sheet('Sheet1')
        book.save(csv_path)

    def auto_Write_Out(self, topic, payload):
        self.logger.info("auto_Write_Out")
        web_site = payload['web_site']
        user_name = payload['user_name']
        department = payload['department']
        csv_path = payload['csv_path']

        self.logger.info(web_site)
        self.logger.info(user_name)
        self.logger.info(department)
        self.logger.info(csv_path)
        auto_Write.auto_Write_Deal(user_name, department, web_site, csv_path)

    def auto_Web_Download(self, topic, payload):
        self.logger.info("auto_Web_Download")
        web_site = payload['web_site']
        user_name = payload['user_name']
        pass_word = payload['pass_word']
        csv_path = payload['csv_path']

        self.logger.info(web_site)
        self.logger.info(user_name)
        self.logger.info(pass_word)
        self.logger.info(csv_path)
        # auto_Write.auto_Write_Deal(user_name,department,web_site,csv_path)

    def auto_Web_Upload(self, topic, payload):
        self.logger.info("auto_Web_Upload")
        web_site = payload['web_site']
        user_name = payload['user_name']
        pass_word = payload['pass_word']
        csv_path = payload['csv_path']

        self.logger.info(web_site)
        self.logger.info(user_name)
        self.logger.info(pass_word)
        self.logger.info(csv_path)
        # auto_Write.auto_Write_Deal(user_name,department,web_site,csv_path)

    def send_Wechat(self, topic, payload):
        self.logger.info("send_Wechat")
        user_name_info = payload['user_name']
        group_name = payload['group_name']
        content_info = user_name_info + "的发票识别已完成"

        wechat_demo.WechatDemo(user_name=group_name, content=content_info).send_message()

    def open_Web(self, topic, payload):
        self.logger.info("open_Web")
        driver_name = payload['driver_name']
        web_url = payload['web_url']
        webComponents.init_driver(driver_name, web_url)

    def web_Input(self, topic, payload):
        self.logger.info("web_Input")
        driver_name = payload['driver_name']
        xpath_value = payload['xpath_value']
        input_value = payload['input_value']
        webComponents.element_input(driver_name, xpath_value, input_value)

    def web_Wait(self, topic, payload):
        self.logger.info("web_Wait")
        wait_time = payload['wait_time']
        webComponents.wait(int(wait_time))

    def wait_Until_Xpath(self, topic, payload):
        self.logger.info("wait_Until_Xpath")
        wait_time = payload['wait_time']
        driver_name = payload['driver_name']
        xpath = payload['xpath']
        webComponents.wait_Until_Xpath(int(wait_time), driver_name, xpath)

    def web_Click(self, topic, payload):
        self.logger.info("web_Click")
        driver_name = payload['driver_name']
        xpath_value = payload['xpath_value']
        wait_time = payload['wait_time']
        webComponents.element_click(driver_name, xpath_value, int(wait_time))

    def switch_Iframe(self, topic, payload):
        self.logger.info("switch_Iframe")
        driver_name = payload['driver_name']
        xpath_value = payload['xpath_value']
        webComponents.switch_frame(driver_name, xpath_value)

    def switch_Window(self, topic, payload):
        self.logger.info("switch_Iframe")
        driver_name = payload['driver_name']
        webComponents.switch_window(driver_name)

    def web_GetValue(self, topic, payload):
        self.logger.info("web_GetValue")
        driver_name = payload['driver_name']
        xpath_value = payload['xpath_value']
        key_name = payload['key_name']
        webComponents.element_get(driver_name, xpath_value, key_name)

    def web_Value_Return(self, topic, payload):
        self.logger.info("web_GetValue")
        driver_name = payload['driver_name']
        xpath_value = payload['xpath_value']
        size = webComponents.element_get_return(driver_name, xpath_value)
        payload = {'report': 'sonar_data', 'value': size}
        self.publish_payload(payload, 'from_nl_gateway')

    def web_PutValue(self, topic, payload):
        self.logger.info("web_PutValue")
        driver_name = payload['driver_name']
        xpath_value = payload['xpath_value']
        key_name = payload['key_name']
        webComponents.element_put(driver_name, xpath_value, key_name)

    def init_Oracle_Db(self, topic, payload):
        self.logger.info("init_Oracle_Db")
        db_code = payload['db_code']
        db_host = payload['db_host']
        db_port = payload['db_port']
        db_name = payload['db_name']
        db_user = payload['db_user']
        db_password = payload['db_password']
        webComponents.init_oracle(db_code, db_host, db_port, db_user, db_password, db_name)

    def init_Mysql_Db(self, topic, payload):
        self.logger.info("init_Mysql_Db")
        db_code = payload['db_code']
        db_host = payload['db_host']
        db_port = payload['db_port']
        db_name = payload['db_name']
        db_user = payload['db_user']
        db_password = payload['db_password']
        webComponents.init_mysql(db_code, db_host, db_port, db_user, db_password, db_name)

    def oracle_Write_To_Db(self, topic, payload):
        self.logger.info("oracle_Write_To_Db")
        db_name = payload['db_name']
        table_name = payload['table_name']
        key_name = payload['key_name']
        webComponents.insert_oracle_data(db_name, table_name, key_name)

    def mysql_Write_To_Db(self, topic, payload):
        self.logger.info("mysql_Write_To_Db")
        db_name = payload['db_name']
        table_name = payload['table_name']
        key_name = payload['key_name']
        webComponents.insert_mysql_data(db_name, table_name, key_name)

    def refresh_Web(self, topic, payload):
        self.logger.info("refresh_Web")
        driver_name = payload['driver_name']
        webComponents.refresh_page(driver_name)

    def read_File_Line(self, topic, payload):
        self.logger.info("read_File_Line")
        file_name = payload['file_name']
        line = payload['line']
        result = webComponents.read_text(file_name, int(line))
        payload = {'report': 'sonar_data', 'value': result}

        self.publish_payload(payload, 'from_nl_gateway')

    def get_Now_Time(self, topic, payload):
        self.logger.info("get_Now_Time")
        # webComponents.element_put(driver_name, xpath_value, key_name)

    def read_sonar(self):
        """
        Read the sonar device and convert value to
        centimeters. The value is then published as a report.
        """
        sonar_time = self.sonar.read()
        distance = sonar_time / 29 / 2
        distance = round(distance, 2)
        payload = {'report': 'sonar_data', 'value': distance}
        self.publish_payload(payload, 'from_nl_gateway')

    def init_pins_dictionary(self):
        """
        The pins dictionary is an array of dictionary items that you create
        to describe each GPIO pin. In this dictionary, you can store things
        such as the pins current mode, the last value reported for an input pin
        callback method for an input pin, etc.
        """

        # not used for robohat gateway, but must be initialized.
        self.pins_dictionary = []

    def my_handler(self, xtype, value, tb):
        """
        for logging uncaught exceptions
        :param xtype:
        :param value:
        :param tb:
        :return:
        """
        self.logger.exception("Uncaught exception: {0}".format(str(value)))


def nl_gateway():
    parser = argparse.ArgumentParser()
    parser.add_argument("-b", dest="back_plane_ip_address", default="None",
                        help="None or IP address used by Back Plane")
    parser.add_argument("-m", dest="subscriber_list", default="to_nl_gateway", nargs='+',
                        help="Banyan topics space delimited: topic1 topic2 topic3")
    parser.add_argument("-n", dest="process_name", default="NewlandGateway",
                        help="Set process name in banner")
    parser.add_argument("-p", dest="publisher_port", default='43124',
                        help="Publisher IP port")
    parser.add_argument("-s", dest="subscriber_port", default='43125',
                        help="Subscriber IP port")
    parser.add_argument("-t", dest="loop_time", default=".1",
                        help="Event Loop Timer in seconds")
    parser.add_argument("-l", dest="log", default="True",
                        help="Set to True to turn logging on.")

    args = parser.parse_args()
    if args.back_plane_ip_address == 'None':
        args.back_plane_ip_address = None

    log = args.log.lower()
    if log == 'false':
        log = False
    else:
        log = True

    kw_options = {
        'back_plane_ip_address': args.back_plane_ip_address,
        'publisher_port': args.publisher_port,
        'subscriber_port': args.subscriber_port,
        'process_name': args.process_name,
        'loop_time': float(args.loop_time),
        'log': log}

    try:
        NlGateway(args.subscriber_list, **kw_options)
    except KeyboardInterrupt:
        sys.exit()


def signal_handler(sig, frame):
    print('Exiting Through Signal Handler')
    raise KeyboardInterrupt


# listen for SIGINT
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == '__main__':
    # replace with name of function you defined above
    nl_gateway()
