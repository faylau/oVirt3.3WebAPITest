#coding:utf-8
'''
Created on 2012-10-16
@summary: The base class for all test case classes.
@author: fei.liu@cs2c.com.cn, huicong.ding@cs2c.com.cn
@version: v0.4
'''

'''
# ChangeLog:
# Version    Date            Desc                Author
# --------------------------------------------------------
# V0.1       09/19/2014      初始版本                                Liu Fei
# --------------------------------------------------------
'''

import os
import unittest

from Utils.PrintLog import LogPrint

class BaseTestCase(unittest.TestCase):
    '''
    @summary: 所有TestCase的父类
    '''
    def setUp(self):
        # 加载全局配置文件中的数据
        dict_data = load_global_config()
        
        
    def initData(self):
        '''
        @summary: 为用例初始化测试数据集；
        @param : 无
        @return: 返回一个测试数据集data；
        '''
        curPath = os.path.abspath(os.path.dirname(__file__))
        # module_name = os.path.realpath(sys.argv[0]).split(os.path.sep)[-1][:-3]
        module_name = str(self.__module__).split(".")[-1]
        test_case = str(self.__class__.__name__)
        dataPath = os.path.dirname(curPath) + os.path.sep + "Data" + os.path.sep + module_name
        dataFilePath = dataPath + os.path.sep + test_case + ".xml"

        if os.path.exists(dataFilePath):
            dl = dataload(dataFilePath)
            private_dict_data = dl.load()
        else:
            printLog("The TestCase <" + test_case + "> has no data file.", "warn")
            private_dict_data = {}
            
        # 读取模块通用测试数据文件
        module_data = dataPath + '.xml'
        if os.path.exists(module_data):
            module_dict_data = dataload(module_data).load()
        else:
            printLog("The TestCase <%s> has no module data file." % test_case, "Warn")
            module_dict_data = {}
        
        # 加载全局配置文件
        global_dict_data = load_global_config()
        dict_data = dict(dict(private_dict_data, **module_dict_data), **global_dict_data)
        
        # 从全局配置文件中获取待测应用系统IP地址
#         ip = load_global_config()['globalconf']['ip']['value']
#         host_name = execSshCmd(ip, ['hostname'], dict_data["globalconf"]['ssh_username']['value'], dict_data['globalconf']['ssh_password']['value'])
#         dict_data['globalconf']['hostname']['value'] = host_name
        
        return dict_data

    def tearDown(self):
        '''
        @summary: 资源清理及回收
        '''
        pass
    
    def setTestResult(self, result='pass', message='No more message.'):
        if result.lower() == 'pass':
            printLog("Test case has been executed successfully, here is the message: %s" % message, 'pass')
            # self.assertTrue(True, "True")
        elif result.lower() == 'fail':
            printLog(message)
            raise self.failureException("Test case execute failed, here is the message: %s" % message)
        else:
            printLog("The test result should be 'pass' or 'fail', your input is not supported.", "error")
            return False
        
    def setResultFasle(self, message):
        return self.setTestResult('fail', message)

    def drive_data(self):
        '''
        @summary: 数据驱动用例使用的装饰器
        @param:
            f: function
        @bug: 还未找到装饰器调用函数时，传递给函数参数的方法
        '''
        def _call(f):
            def __call():
                dict_data = self.initData()
                for key in dict_data['case']['datadrive']:
                    if key != 'value':
                        data = dict_data['case']['datadrive'][key]
                        return_ = f(data)
                return return_
            return __call
        return _call
            
if __name__ == "__main__":
    
    unittest.main()
