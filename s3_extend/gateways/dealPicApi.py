# -*- coding: utf-8 -*-
'''
@author: Carry
@contact: xkx94317@gmail.com
@file: cut_pic.py
@time: 2020/9/16 17:36 
@desc: 
'''
import base64
import requests
class screenshot_ocr():

    def __init__(self):
        self.access_token = '24.64d34a72ca6c9675bebd1761bd4e6c67.2592000.1618731291.282335-16097526'

    def do_ocr(self, img_path: str) -> str:
        with open(img_path, "rb") as f:
            ret = self.post_baidu_api_invoice(f.read())
        return self.get_info(ret)

    def post_baidu_api_invoice(self, img_bytes):
        url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/vat_invoice?access_token={}'.format(self.access_token)
        api_params = {
            'image': base64.b64encode(img_bytes).decode(),
        }
        resp = requests.post(url, data=api_params)
        result = resp.json()
        print(result)
        return result

    def get_info(self, ret):
        ret_dit = {}
        ret_dit['发票代码'] = ret['words_result']['InvoiceCode']
        ret_dit['发票号码'] = ret['words_result']['InvoiceNum']
        ret_dit['开票日期'] = ret['words_result']['InvoiceDate']
        ret_dit['合计金额'] = ret['words_result']['TotalAmount']
        ret_dit['价税合计'] = ret['words_result']['AmountInFiguers']
        ret_dit['购方名称'] = ret['words_result']['PurchaserName']
        ret_dit['购方税号'] = ret['words_result']['PurchaserRegisterNum']
        ret_dit['合计税额'] = ret['words_result']['TotalTax']
        ret_dit['购方地址电话'] = ret['words_result']['PurchaserAddress']
        ret_dit['开户行及账号'] = ret['words_result']['PurchaserBank']
        # print(ret_dit)
        return str(ret_dit)


if __name__ == '__main__':
    ret = screenshot_ocr().do_ocr("E:\\workspace\\config\\立成收\\立成收\\invoice_01.jpg")
    print(ret)
