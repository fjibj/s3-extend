# -*- coding: utf-8 -*-
'''
@file: job_01.py
@time: 2021/3/23 11:30 
@desc: 
'''
import datetime
import functools
import json
import os
import re
import sys

import cx_Oracle
import pymysql
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

BROWSER_DICT = {}  # 存放浏览器
DB_DICT = {}  # 存放数据库
RESULT = {}  # 存放获取内容

option = webdriver.ChromeOptions()
# 防止打印一些无用的日志
option.add_experimental_option("excludeSwitches", ['enable-automation', 'enable-logging'])


def catch_exception(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print('捕获异常：{} ,报错方法：{}'.format(e, func.__name__))

    return wrapper


def drop_down(browser, xpath):
    from selenium.webdriver.support.ui import Select
    """下面用三种方法对下拉列表进行选择"""
    # 通过index进行选择下拉列表的值(根据排列的位置进行选择)
    Select(browser.find_element_by_xpath(xpath)).select_by_index(1)  # 选择下拉列表的15
    time.sleep(2)
    # # 通过value进行选择（通过列表中value的值进行选择）
    # Select(browser.find_element_by_xpath(xpath)).select_by_value("2")  # 选择下拉列表的20
    # time.sleep(2)
    # # 通过选项文字进行选择
    # Select(browser.find_element_by_xpath(xpath)).select_by_visible_text("25")  # 选择下拉列表的25
    # time.sleep(2)


def judge_driver(driver_name):
    return BROWSER_DICT[driver_name]


@catch_exception
def init_driver(driver_name, url):
    '''
    初始化并访问url
    '''
    try:
        browser = webdriver.Chrome(sys._MEIPASS + '\\chromedriver.exe', chrome_options=option)
    except:
        browser = webdriver.Chrome(chrome_options=option)  # 本地
    BROWSER_DICT[driver_name] = browser
    BROWSER_DICT[driver_name].get(url)
    # time.sleep(3)


@catch_exception
def element_input(driver_name, xpath, keywords):
    '''
    输入字符
    '''
    browser = judge_driver(driver_name)
    browser.find_element(By.XPATH, xpath).send_keys(keywords)


def wait(num):
    time.sleep(num)


def wait_Until_Xpath(num, driver_name, xpath):
    browser = judge_driver(driver_name)
    value = 0
    times = 1
    while value == 0:
        value = len(browser.find_elements(By.XPATH, xpath))
        print('wait times:', times)
        times = times + 1
        time.sleep(num)
        if value != 0:
            break


@catch_exception
def element_click(driver_name, xpath, num):
    '''
    点击
    '''
    browser = judge_driver(driver_name)
    # print('save cookie')
    # save_cookie(browser)
    # print('save cookie done')
    browser.find_element(By.XPATH, xpath).click()
    time.sleep(1 + int(num))


@catch_exception
def element_get(driver_name, xpath, key):
    '''
    获取内容 save
    '''
    browser = judge_driver(driver_name)
    try:
        value = browser.find_element(By.XPATH, xpath).text
    except:
        iframes = browser.find_elements_by_tag_name('iframe')
        for iframe in iframes:
            try:
                browser.switch_to.frame(iframe)
                value = browser.find_element(By.XPATH, xpath).text
                time.sleep(1)
                break
            except:
                browser.switch_to.default_content()
                pass

    RESULT[key] = value
    print(RESULT)


@catch_exception
def area_api(num):
    '''
    根据手机号获取地区名称 苏州rpa需求
    '''
    num = 'http://10.41.114.83:7008/poineer/interface/oss/getMsisdnCounty.do?msisdn=' + num
    county_name = requests.get(num).json().get('RETMESSAGE').get('COUNTYNAME')
    return county_name


@catch_exception
def page_down(driver_name):
    browser = judge_driver(driver_name)
    browser.find_element(By.XPATH, '//*').send_keys(Keys.PAGE_DOWN)


# @catch_exception
# def element_get(driver_name, xpath, key):
#     '''
#     获取内容 save
#     2021 04 15 定制开发， 取冒号后得数字
#     '''
#     browser = judge_driver(driver_name)
#     try:
#         value = browser.find_element(By.XPATH, xpath).text
#     except:
#         iframes = browser.find_elements_by_tag_name('iframe')
#         for iframe in iframes:
#             try:
#                 browser.switch_to.frame(iframe)
#                 value = browser.find_element(By.XPATH, xpath).text
#                 time.sleep(1)
#                 break
#             except:
#                 browser.switch_to.default_content()
#                 pass
#     if ':' in value:
#         RESULT[key] = value.split(':')[1]
#     else:
#         RESULT[key] = value.split('：')[1]
#     print(RESULT)


@catch_exception
def element_get_return(driver_name, xpath):
    '''
    获取内容return
    '''
    browser = judge_driver(driver_name)
    print(xpath)
    value = len(browser.find_elements(By.XPATH, xpath))
    print("value=", value)
    return value


@catch_exception
def element_put(driver_name, xpath, key):
    '''
    根据key 填入字符
    '''
    browser = judge_driver(driver_name)
    browser.find_element(By.XPATH, xpath).send_keys(RESULT[key])


@catch_exception
def switch_frame(driver_name, xpath):
    '''
    切换frame并点击
    '''
    browser = judge_driver(driver_name)
    iframes = browser.find_elements_by_tag_name('iframe')
    for iframe in iframes:
        try:
            browser.switch_to.frame(iframe)
            browser.find_element(By.XPATH, xpath).click()
            time.sleep(1)
            break
        except:
            browser.switch_to.default_content()
            pass


def switch_window(driver_name):
    '''
    切换到最后一个窗口
    '''
    browser = judge_driver(driver_name)
    browser.switch_to.window(browser.window_handles[-1])
    time.sleep(1)


class MysqlHandler():
    '''
    连接数据库
    '''

    def __init__(self, host, port, user, passwd, db):
        self.conn = pymysql.connect(
            host=host,
            port=int(port),
            user=user,
            passwd=passwd,
            db=db,
            charset='utf8'
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 返回结果为数组

    def query(self, sql):
        self.cursor.execute(sql)
        res = self.cursor.fetchall()
        return res

    def insert(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def query_max_id(self, id_name, table):
        sql = 'SELECT MAX({}) FROM {}'.format(id_name, table)
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return res

    def close(self):
        self.cursor.close()
        self.conn.close()


def init_mysql(mysql_name, host, port, user, passwd, db):
    mysql = MysqlHandler(host, port, user, passwd, db)
    DB_DICT[mysql_name] = mysql


def query_mysql_data(mysql_name, table):
    '''
    查询数据
    '''
    mysql = DB_DICT[mysql_name]
    sql = "SELECT * from  " + table
    res = mysql.query(sql)
    print(res)


def insert_mysql_data(mysql_name, table, id_name):
    '''
    插入数据，数据库名，表名，所查询自增id名
    '''
    mysql = DB_DICT[mysql_name]

    maxid = mysql.query_max_id(id_name, table)
    next_id = maxid['MAX({})'.format(id_name)] + 1
    # RESULT = {'name': 'xx', 'age': 22, 'gender': '男', 'city': 'ssssss'}
    RESULT[id_name] = next_id
    colms = ''
    ss = ''
    for i in RESULT.keys():
        colms = colms + i + ','
        # ss = ss + '%s,'
    values = ''
    for i in RESULT.keys():
        values = values + str(RESULT[i]) + ','
    sql = "INSERT INTO " + table + " ({}) VALUES ({})".format(colms[:-1],
                                                              '\'' + values[:-1].replace(',', '\',\'') + '\'')
    print(sql)
    mysql.insert(sql)

    # 清理内存字典
    RESULT.clear()

    # 待验证
    # query = 'insert into rpa_demo ({}) values ({})'.format(colms[:-1], ss[:-1])
    # print(query)
    # values = (列名1, 列名2, 列名3, 列名4, 列名5, 列名6)
    # cs1.execute(query, values)


class OracleHandler:
    def __init__(self, connectStr):
        self.connect = cx_Oracle.connect(connectStr)
        self.cursor = self.connect.cursor()

    def select(self, sql):
        print("查询结果个数：", self.cursor.execute(sql))
        result = self.cursor.fetchall()
        print(str(result[0][0]))

    def insert(self, sql):
        self.cursor.execute(sql)
        self.connect.commit()
        # 关闭游标
        # self.close()
        # self.connect.close()

    def query_max_id(self, id_name, table):
        sql = 'SELECT MAX({}) FROM {}'.format(id_name, table)
        self.cursor.execute(sql)
        res = self.cursor.fetchone()
        return res


def init_oracle(db_name, host, port, user, passwd, db):
    s = '{}/{}@{}:{}/{}'.format(user, passwd, host, port, db)
    # conn = OracleHandler('jsai/jsai123@172.32.148.120:1521/bidev')  # 测试
    conn = OracleHandler(s)
    DB_DICT[db_name] = conn


def insert_oracle_data(db_name, table, id_name):
    '''
    插入数据
    '''
    db = DB_DICT[db_name]
    maxid = db.query_max_id(id_name, table)
    next_id = maxid[0] + 1
    # RESULT = {'NAME': 'test', 'PIC_NAME': 'xx', 'RESPECT_CODE': 'ss', 'RESPECT_MESSAGE': 'ss',
    #           'CREATE_DATE': 'sss', 'BEGIN_TIME': 'ss', 'END_TIME': 'sss', 'SPEND_TIME': 'sss'}
    RESULT[id_name] = next_id
    colms = ''
    ss = ''
    for i in RESULT.keys():
        colms = colms + i + ','
        # ss = ss + '%s,'
    values = ''
    for i in RESULT.keys():
        values = values + str(RESULT[i]) + ','
    sql = "INSERT INTO " + table + " ({}) VALUES ({})".format(colms[:-1],
                                                              '\'' + values[:-1].replace(',', '\',\'') + '\'')
    print(sql)
    db.insert(sql)

    # 清理内存字典
    RESULT.clear()


def refresh_page(driver_name):
    '''
    刷新界面
    '''
    driver = judge_driver(driver_name)
    driver.refresh()
    time.sleep(2)


def get_date():
    '''
    返回毫秒级当前时间
    '''

    # dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    t = time.time()
    print(int(round(t * 1000)))
    return int(round(t * 1000))


@catch_exception
def read_text(file_path, i):
    '''
    读文件第i行的内容,文件行数 > i > 0
    '''
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(lines[i - 1])
        return lines[i - 1].strip()


# def get_date(driver_name, date, xpath):
#     '''
#     无锡移动定制开发 ，根据日期获取次日还是次月生效
#     '''
#     # browser = judge_driver(driver_name)
#     date = '2021- 04 -01'
#     date = date.replace(' ', '').replace(' ', '')
#     # ts = int(time.mktime(time.strptime(date, "%Y-%m-%d")))
#     # dt = int(time.time())
#     mon = datetime.datetime.today().month  # 当前月份
#     _mon = int(re.search('.*-(.*)-.*', date).group(1))  # 传入月份
#     if _mon > mon:
#         # 次月生效
#         browser.find_element(By.XPATH, xpath + '[1]').click()
#     elif _mon == mon:
#         # 次日生效
#         browser.find_element(By.XPATH, xpath + '[1]').click()
#     time.sleep(3)

def save_cookie(browser):
    jsonCookies = json.dumps(browser.get_cookies())
    print(jsonCookies)
    with open('cookies.txt', 'w') as f:
        f.write(jsonCookies)


if __name__ == '__main__':
    # host = '172.32.148.120'
    # port = '1521'
    # user = 'jsai'
    # passwd = 'jsai123'
    # db = 'bidev'
    # init_oracle('oraclel01', host, port, user, passwd, db)
    # insert_oracle_data('oraclel01', 'ai_bx_result_seal', 'RESULT')

    # host = '172.32.148.20'
    # port = '3306'
    # user = 'root'
    # passwd = 'root'
    # db = 'rpa'
    # init_mysql('mysql01', host, port, user, passwd, db)
    # insert_mysql_data('mysql01', 'rpa_demo', 'id')

    # url = 'https://www.baidu.com'
    url = 'http://new4a.js.cmcc/uac/web3/jsp/login/login.jsp'
    url = 'http://nguc.cs.cmos/nguc/ngucportal/login.html'
    driver_name = 'chrome01'
    init_driver(driver_name, url)
    # refresh_page(driver_name)
    # BROWSER_DICT[driver_name].quit()

    # get_date('', '', '')
