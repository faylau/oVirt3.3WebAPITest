#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/23          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import unittest

import xmltodict

from BaseTestCase import BaseTestCase
from TestAPIs.DataCenterAPIs import DataCenterAPIs
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from Utils.HTMLTestRunner import HTMLTestRunner

class ITC010101_GetDataCentersList(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-01获取数据中心列表
    '''
    def test_GetDataCentersList(self):
        dcapi = DataCenterAPIs()
        r = dcapi.getDataCentersList()
        if r['status_code']==200:
            LogPrint().info('Get DataCenters list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error('Get DataCenters list FAIL.')
            self.flag = False
        self.assertTrue(self.flag)
        
class ITC010102_GetDataCenterInfo(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-02获取指定数据中心信息
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        
        # 准备1：创建一个数据中心
        self.dcapi = DataCenterAPIs()
        self.dcapi.createDataCenter(self.dm.dc_info)
        
    def test_GetDataCenterInfo(self):
        '''
        @summary: 测试用例执行步骤
        '''
        # 测试1：获取数据中心的信息，并与期望结果进行对比
        r = self.dcapi.getDataCenterInfo(self.dm.dc_name)
        if r['status_code']==200:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.dc_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Get DataCenter '%s' info SUCCESS." % self.dm.dc_name)
            else:
                LogPrint().error("Get DataCenter '%s' info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Get/Create DataCenter '%s' FAILED. " % self.dm.dc_name)
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.dcapi.searchDataCenterByName(self.dm.dc_name):
            self.dcapi.delDataCenter(self.dm.dc_name)

    
            


if __name__ == "__main__":
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["DataCenter.ITC010102_GetDataCenterInfo"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
#     unittest.TextTestRunner(verbosity=2).run(testSuite)

    fileName = r"d:\result.html"
    fp = file(fileName, 'wb')
    runner = HTMLTestRunner(stream=fp, title=u"测试结果", description=u"测试报告")
    runner.run(testSuite)