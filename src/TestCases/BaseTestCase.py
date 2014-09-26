#encoding:utf-8

'''
Created on 2014-09-23
@summary: The base class for all test case classes.
@author: fei.liu@cs2c.com.cn
@version: v0.1
'''

'''
# ChangeLog:
# Version    Date            Desc                Author
# --------------------------------------------------------
# V0.1       09/23/2014      初始版本                                Liu Fei
# --------------------------------------------------------
'''

import os
import unittest
import importlib

from Utils.PrintLog import LogPrint

class BaseTestCase(unittest.TestCase):
    '''
    @summary: 所有TestCase的父类
    '''
    def setUp(self):
        self.flag = False
        return self.initData()
        
    def initData(self):
        '''
        @summary: 为测试用例初始化数据集；
        @param : 无
        @return: 返回一个测试数据集data（存放测试数据的.py模块名称，通过这个模块名可以读取.py文件中的测试数据）
        '''
        curPath = os.path.abspath(os.path.dirname(__file__))
        module_name = str(self.__module__)
        test_case = str(self.__class__.__name__)
        dataPath = os.path.dirname(curPath) + os.path.sep + "TestData" + os.path.sep + module_name
        dataFilePath = dataPath + os.path.sep + test_case + ".py"
        if os.path.exists(dataFilePath):
            data_module = 'TestData.%s.%s' % (module_name, test_case)
            return importlib.import_module(data_module)
        else:
            LogPrint().warning("The TestCase <" + test_case + "> has no data file.")
            return None

    def tearDown(self):
        '''
        @summary: 资源清理及回收
        '''
        pass
    
if __name__ == "__main__":
    
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["BaseTestCase.BaseTestCase"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)

