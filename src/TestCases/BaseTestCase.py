#encoding:utf-8

'''
Created on 2014-09-23
@summary: The base class for all test case classes.
@author: fei.liu@cs2c.com.cn
@version: v0.1
'''
import xmltodict
from collections import OrderedDict

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
        self.flag = True
        return self.initData()
        
    def initData(self, test_case=None):
        '''
        @summary: 为测试用例初始化数据集；
        @param : 无
        @return: 返回一个测试数据集data（存放测试数据的.py模块名称，通过这个模块名可以读取.py文件中的测试数据）
        '''
        curPath = os.path.abspath(os.path.dirname(__file__))
        module_name = str(self.__module__)
        if len(module_name.split('.')) == 2:
            module_name = module_name.split('.')[1]
        if test_case is None:
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
    
    def drive_data(self, xml_data):
        '''
        @summary: 数据驱动用例使用的装饰器
        @param f: function
        '''
        def _call(f):
            def __call():
                dict_data = xmltodict.parse(xml_data)
                for key in dict_data['data_driver']:
                        data_list = dict_data['data_driver'][key]
                        for data in data_list:
                            od = OrderedDict()
                            od[key] = data
#                             print od
                            return_ = f(xmltodict.unparse(od))
                return return_
            return __call
        return _call
    
if __name__ == "__main__":
    
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["BaseTestCase.BaseTestCase"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)

