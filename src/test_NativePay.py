#!/usr/bin/env python
#-*- coding:utf-8 -*-

# 主扫交易，返回最终结果
import xlrd
import os
import requests
import json
import time
import sys
import unittest
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email.header import Header
from threading import Timer
from common import Log
from common import Encrypt
from common.order import db_connect
from common.order import order_opera
from common import get_Config
from data.data_opera import data_Op

sheet_name = 'apiPay'
data1 = data_Op().get_data(sheet = sheet_name)

# logobj = Log.loggerClass('debug')

class test_nativePay(unittest.TestCase):
    @classmethod
    def test_Native(self):
        error_cases = []
        nrows = data_Op().get_rowNum(sheet_name)
        for i in range(1, nrows-1):
            num = str(data1[i]['No']).replace("\n", "").replace("\r", "")
            api_name = data1[i]['API Name'].replace("\n", "").replace("\r", "")
            api_host = data1[i]['Host'].replace("\n", "").replace("\r", "")
            request_url = data1[i]['Request Url'].replace("\n", "").replace("\r", "")
            method = data1[i]['Method'].replace("\n", "").replace("\r", "")
            request_data_type = data1[i]['Request Data Type'].replace("\n", "").replace("\r", "")
            request_data = data1[i]['Request Data'].replace("\n", "").replace("\r", "")
            check_point = data1[i]['Check_Point'].replace("\n", "").replace("\r", "")
            message = data1[i]['except_result'].replace("\n", "").replace("\r", "")

            try:
                    # 调用接口请求方法，后面会讲到
                resp = test_nativePay.request_interface(api_host, request_url, method, request_data, check_point)
                # logobj.info(resp, 'info')
                print(resp)

                outTradeNo = resp['outTradeNo']
                transactionNo = resp['transactionNo']
                paystate = resp['payState']

                if paystate != '00':
                    # append只接收一个参数，所以要将四个参数括在一起，当一个参数来传递
                    # 请求失败，则向error_cases中增加一条记录
                    if transactionNo == None:
                        transactionNo = '0'
                        error_cases.append((outTradeNo, transactionNo, paystate, "交易异常"))
                        # logobj.info(error_cases,'info')
                        print("交易异常")
                    else:
                        error_cases.append((outTradeNo, transactionNo, paystate, "交易异常"))
                        # logobj.info(error_cases,'info')
                        print("交易异常")
            except Exception as e:
                print(e)
                #logobj.debug(e)
                print("订单{}交易失败，请检查失败原因！".format(outTradeNo))
                # logobj.debug("订单{}交易失败，请检查失败原因！".format(outTradeNo))
                    # 访问异常，也向error_cases中增加一条记录
                if transactionNo == None:
                    transactionNo = '0'
                    error_cases.append((outTradeNo ,  transactionNo , paystate  , "交易异常"))
                    # logobj.info(error_cases,'info')
                    print("交易异常")

                else:
                    error_cases.append((outTradeNo ,  transactionNo , paystate  , "交易异常"))
                    # logobj.info(error_cases,'info')
                    print("交易异常")
        return error_cases

    def request_interface(api_host, request_url, method, request_data, check_point):
        # 构造请求headers
        headers = {'Content-Type': 'application/json; charset=UTF-8',
                   'x-efps-sign': Encrypt.req_encrypt(request_data),
                   'x-efps-sign-no': get_Config.get_signno_Conf()
                   }
        # 判断请求方式，如果是GET，则调用get请求，POST调post请求，都不是，则抛出异常
        if method == "GET":
            r = requests.get(url=api_host + request_url, params=json.loads(request_data), headers=headers)
            result_json = r.json()  # 引入json模板，将响应结果转变为字典格式
            return_Code = result_json['returnCode']  # 获取响应返回的returnCode值
            if check_point == return_Code:  # 断言，判断预期值是否与响应参数returnCode一致
                print("接口请求成功，结果返回值为\n{}. ".format(r.text))
                return return_Code
            else:
                print("接口请求失败！！！结果返回值为\n{}.".format(r.text))
                return return_Code

        elif method == "POST":
            payload1 = json.dumps(request_data)  # 接受python的基本数据类型，然后将其序列化为string
            payload2 = json.loads(payload1)  # 接受一个合法字符串，然后将其反序列化为python的基本数据类型
            r = requests.post(url=api_host + request_url, data=payload2, headers=headers)
            result_json = r.json()  # 引入json模板，将响应结果转变为字典格式
            out_Trade_No = result_json['outTradeNo']  # 获取响应返回的outTradeNo值
            return_Code = result_json['returnCode']  # 获取响应返回的returnCode值
            if check_point == return_Code:  # 断言，判断预期值是否与响应参数returnCode一致
                # logobj.debug("第{}个接口'{}'请求成功，结果返回值为\n{}.".format(num, api_name, r.text), 'debug')
                # print("第{}个接口'{}'请求成功，结果返回值为\n{}.".format(num, api_name, r.text))
                order_inq = db_connect.order_query(out_Trade_No)  # 调用函数连接数据库，查询transaction_no
                if len(order_inq) != 0:  # 判断transaction_no是否为空
                    state_mod = order_opera.state_modify(order_inq)  # 调用函数修改订单状态
                    # print(state_mod)
                    if state_mod == 'success':  # 判断code是否为success
                        # logobj.debug('修改clr状态成功！', 'debug')
                        print('修改clr状态成功！')
                        # t = Timer(1.0, result_query)   # 指定1秒后执行result_query函数
                        # t.start()
                        time.sleep(5)
                        result_que = order_opera.result_query(order_inq)
                        paystate = result_que['payState']  # 直接获取响应返回的paystate值
                        # returnCode = result_que['returnCode']
                        # returnMsg = result_que['returnMsg']
                        if paystate == '00':
                            # logobj.debug('交易成功', 'debug')
                            print("交易成功")
                            return result_que
                        elif paystate == '01':
                            # logobj.debug("交易失败，请检查失败原因！", 'debug')
                            print("交易失败，请检查失败原因！")
                            return result_que
                        else:
                            # logobj.debug("交易未返回终态，请检查错误原因！", 'debug')
                            print("交易未返回终态，请检查错误原因！")
                            return result_que
                    else:
                        print('修改clr状态失败！')
                else:
                    print("交易请求未生成transaction_no，请检查错误原因！")
            else:
                print("接口请求失败！！！结果返回值为\n{}.".format(r.text))
        else:
            print("接口请求方式有误！！！请确认字段【Method】值是否正确，正确值为大写的GET或POST。")
            return 400, "请求方式有误"







