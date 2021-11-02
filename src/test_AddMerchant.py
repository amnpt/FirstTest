# coding=utf-8
import unittest
import time
from data.data_opera import data_Op
from common.myunit import MyTest
from common.base import Page
from testCase.page_obj.add_merchantPage import addMerchant
from testCase.page_obj.enter_menu import en_menu
from common import function
from testCase.page_obj.element_opera import element_Op
from testCase.test1_login import loginTest
from testCase.except_result.result_Assert import res_Assert
data1 = data_Op().get_data(sheet = "addMerchant")

class test_addMerchant(MyTest, Page):  #unittest.TestCase

    @unittest.skip("跳过此用例")
    def test_add1(self,expected=True):
        loginTest(self.driver).test_login2()
        time.sleep(3)
        en_menu(self.driver).enter_Merchant()
        time.sleep(2)
        en_menu(self.driver).enter_addMerchant()

        add = addMerchant(self.driver)
        add.all_insert(platcustomer_code = data1[1]['platcustomercode'], sercustomer_code = data1[1]['sercustomercode'],
                       contacts1 = data1[1]['contacts'], mobile1 = data1[1]['mobile'], email1 = data1[1]['email'],
                   business_man = data1[1]['businessman'], short_name = data1[1]['shortname'], phone1 = data1[1]['phone'],
                   bus_address = data1[1]['busaddress'], up_photo=data1[1]['busphoto'], up_file=data1[1]['zipfile'],
                   buslic_no=data1[1]['buslicenseno'], customer_name=data1[1]['customername'],
                   reg_address=data1[1]['registaddress'], bus_scope=data1[1]['busscope'], leaper_name=data1[1]['leapername'],
                   leaperde_no=data1[1]['leaperdeno'], leaperde_name=data1[1]['leaperdename'],
                   pu_bankcard=data1[1]['pubankcard'], pu_branch=data1[1]['pubranch'],
                   sett_bankcard=data1[1]['settbankcard'], sett_branch=data1[1]['settbranch'],
                   un_shortname=data1[1]['unionshortname'], remark1=data1[1]['remark'])

        add.all_insert(email1=data1[2]['email'])
        time.sleep(10)
        print("输入成功")
        Page.assert_equal(add.add_merchant_success(actual=data1[1]['except_result']),expected)
        function.insert_img(self.driver,data1[0]['screenshot_name'])

    # 数据输入检验
    @classmethod
    def test_add2(self):

        loginTest(self.driver).test_login2()
        time.sleep(3)
        en_menu(self.driver).enter_Merchant()
        time.sleep(2)

        i = 2
        while i <= 2:
            en_menu(self.driver).enter_addMerchant()
            time.sleep(1)
            add = addMerchant(self.driver)
            add.a1_email(email1 = data1[i]['email'])
            element_Op(self.driver).win_mouse()
            time.sleep(2)
            res_Assert(self.driver).emailAs(data1[i]['except_result'], i)
            function.insert_img(self.driver, data1[i]['screenshot_name'])
            # time.sleep(5)
            add.op1_return()
            time.sleep(2)
            i += 1

        # while i > 3 and i <=5:
        #     en_menu(self.driver).enter_addMerchant()
        #     time.sleep(1)
        #     add = addMerchant(self.driver)
        #     add.a1_mobile(mobile1=data1[i]['mobile'])
        #     element_Op(self.driver).win_mouse()
        #     time.sleep(2)
        #     res_Assert(self.driver).mobileAs(data1[i]['except_result'], i)
        #     function.insert_img(self.driver, data1[i]['screenshot_name'])
        #     # time.sleep(5)
        #     add.op1_return()
        #     time.sleep(2)
        #     i += 1

        else:
            pass







