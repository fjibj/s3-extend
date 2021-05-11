# _*_ coding:utf-8 _*_
from time import sleep
import requests
from selenium import webdriver
import xlrd
from xlrd import xldate_as_tuple

def auto_Write_Deal(name, department, url, biao):
    #获取excle路径,目前路径是我的本地
    xl = xlrd.open_workbook(biao)
    # 获取第一页
    table = xl.sheets()[0]
    # 获取一共多少行
    rows = table.nrows
    cols=table.ncols
    # 获取第二行的值
    row = table.row_values(1)
    '''#处理第三列的日期数据,先转化成元祖
    date = xlrd.xldate_as_tuple(table.cell(1,2).value,0)
    date=list(date)#再转化成list
    date0=date[0:3]#再次切片
    date0="".join('%s'%id for id in date0)'''
    #webdriver的路径也是我的本地
    mydriver=r"D:\workspace\webdriver\chromedriver.exe"
    driver = webdriver.Chrome(mydriver)
    driver.implicitly_wait(15)#隐式等待
    driver.get(url)
    driver.maximize_window()
    #自己定义姓名
    #输入名字
    driver.find_elements_by_css_selector('.el-input__inner')[0].send_keys(name)
    sleep(0.3)
    #输入部门
    driver.find_elements_by_css_selector('.el-input__inner')[1].send_keys(department)
    sleep(0.3)
    #输入发票代码
    fapiaodaima=str(row[0])
    driver.find_elements_by_css_selector('.el-input__inner')[-10].send_keys(fapiaodaima)
    sleep(0.3)
    #输入发票号码
    fapiaohaoma=str(row[1])
    driver.find_elements_by_css_selector('.el-input__inner')[-9].send_keys(fapiaohaoma)
    sleep(0.3)
    #输入开票日期
    kaipiaoriqi=str(row[2])
    driver.find_elements_by_css_selector('.el-input__inner')[-8].send_keys(kaipiaoriqi)
    sleep(0.3)
    #输入合计金额
    totalmoney=str(row[3])
    driver.find_elements_by_css_selector('.el-input__inner')[-7].send_keys(totalmoney)
    sleep(0.3)
    #输入合计税额
    totalshui=str(row[4])
    driver.find_elements_by_css_selector('.el-input__inner')[-6].send_keys(totalshui)
    sleep(0.3)
    #输入输入价税合计
    totaljiashui=str(row[5])
    driver.find_elements_by_css_selector('.el-input__inner')[-5].send_keys(totaljiashui)
    sleep(0.3)
    #输入购方名称
    shoppingname=str(row[6])
    driver.find_elements_by_css_selector('.el-input__inner')[-4].send_keys(shoppingname)
    sleep(0.3)
    #输入购方税号
    shoppingnumber=str(row[7])
    driver.find_elements_by_css_selector('.el-input__inner')[-3].send_keys(shoppingnumber)
    sleep(0.3)
    #输入购方地址电话
    dizhiidianhua=str(row[8])
    driver.find_elements_by_css_selector('.el-input__inner')[-2].send_keys(dizhiidianhua)
    sleep(0.3)
    #输入开户行以及账号
    kaihuzhanghao=str(row[9])
    driver.find_elements_by_css_selector('.el-input__inner')[-1].send_keys(kaihuzhanghao)
    sleep(1)
    row0=rows-2
    a=0
    if rows !=0:
        for i in range(row0):
            a=i+2
            row = table.row_values(a)
            '''#处理单元格数据
            date = xlrd.xldate_as_tuple(table.cell(a,2).value, 0)
            date = list(date)  # 再转化成list
            date0 = date[0:3]  # 再次切片
            #转化成字符串
            date0 = "".join('%s' % id for id in date0)'''
            #点击+号
            driver.find_element_by_css_selector('.el-icon-plus').click()
            # 输入发票代码
            fapiaodaima = str(row[0])
            driver.find_elements_by_css_selector('.el-input__inner')[-10].send_keys(fapiaodaima)
            sleep(0.3)
            # 输入发票号码
            fapiaohaoma = str(row[1])
            driver.find_elements_by_css_selector('.el-input__inner')[-9].send_keys(fapiaohaoma)
            sleep(0.3)
    		#输入开票日期
            kaipiaoriqi=str(row[2])
            driver.find_elements_by_css_selector('.el-input__inner')[-8].send_keys(kaipiaoriqi)
            sleep(0.3)
            # 输入合计金额
            totalmoney = str(row[3])
            driver.find_elements_by_css_selector('.el-input__inner')[-7].send_keys(totalmoney)
            sleep(0.3)
            # 输入合计税额
            totalshui = str(row[4])
            driver.find_elements_by_css_selector('.el-input__inner')[-6].send_keys(totalshui)
            sleep(0.3)
            # 输入输入价税合计
            totaljiashui = str(row[5])
            driver.find_elements_by_css_selector('.el-input__inner')[-5].send_keys(totaljiashui)
            sleep(0.3)
            # 输入购方名称
            shoppingname = str(row[6])
            driver.find_elements_by_css_selector('.el-input__inner')[-4].send_keys(shoppingname)
            sleep(0.3)
            # 输入购方税号
            shoppingnumber = str(row[7])
            driver.find_elements_by_css_selector('.el-input__inner')[-3].send_keys(shoppingnumber)
            sleep(0.3)
            # 输入购方地址电话
            dizhiidianhua = str(row[8])
            driver.find_elements_by_css_selector('.el-input__inner')[-2].send_keys(dizhiidianhua)
            sleep(0.3)
            # 输入开户行以及账号
            kaihuzhanghao = str(row[9])
            driver.find_elements_by_css_selector('.el-input__inner')[-1].send_keys(kaihuzhanghao)
            sleep(1)
        #点击提交
        driver.find_elements_by_css_selector('.el-button--primary')[-1].click()
        sleep(1)
    
    else:
        # 点击提交
        driver.find_elements_by_css_selector('.el-button--primary')[-1].click()
        sleep(1)
    
#    driver.close()