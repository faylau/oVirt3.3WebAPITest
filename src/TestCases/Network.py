#encoding:utf-8


__authors__ = ['"Wei Keke" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/09          初始版本                                                            Wei Keke 
#---------------------------------------------------------------------------------
'''

import unittest

from BaseTestCase import BaseTestCase
from TestAPIs.NetworkAPIs import NetworkAPIs, NetworkProfilesAPIs, smart_create_network, smart_delete_network
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from TestAPIs.ProfilesAPIs import ProfilesAPIs
from TestAPIs.DataCenterAPIs import DataCenterAPIs
from TestData.Network import ITC05_Setup as ModuleData

import xmltodict

class ITC05_Setup(BaseTestCase):
    '''
    @summary: “集群管理”模块测试环境初始化（执行该模块测试用例时，都需要执行该用例搭建初始化环境）
    @note: （1）创建一个数据中心（NFS）；
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()

    def test_Create_DC(self):
        '''
        @summary: 创建一个数据中心
        '''
        dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Module-Test: Create DataCenter '%s'." % self.dm.dc_name)
        dcapi.createDataCenter(self.dm.dc_info)

class ITC050101_GetNetworkList(BaseTestCase):
    '''
    @summary: ITCxxxx:
    '''
    def test_GetNetworkList(self):
        '''
        @summary: 测试步骤
        @note: （1）获取所有逻辑网络列表；
        @note: （2）验证接口返回的状态码是否正确。
        '''
        self.nwapi = NetworkAPIs()
        r = self.nwapi.getNetworksList()
        if r['status_code']==200:
            LogPrint().info('PASS: Get Network list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error('FAIL: Get Network list FAIL. Returned status code "%s" is Wrong.' % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
class ITC050102_GetNetworkInfo(BaseTestCase):
    '''
    @summary: ITC-05网络管理-01基本操作-02获取指定网络信息
    @note: 为简化测试前提，所有网络操作均在Default数据中心内
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()
        # 准备1：创建一个网络
        LogPrint().info("Pre-Test: Create a network '%s' for this TC." % self.dm.nw_name)
        self.assertTrue(smart_create_network(self.dm.nw_info,self.dm.nw_name))
        
    def test_GetNetworkInfo_name(self):
        '''
        @summary: 测试用例执行步骤
        @note: （1）根据名称获取指定逻辑网络的信息；
        @note: （2）验证接口返回的状态码、接口信息是否正确。
        '''
        # 测试1：根据网络名称和数据中心名称获取网络信息（在同一数据中心内网络名称是唯一的）
        LogPrint().info("Test: Get the network's ('%s') info by name." % self.dm.nw_name)
        r = self.nwapi.getNetworkInfo(nw_name=self.dm.nw_name,dc_name=ModuleData.dc_name)
        if r['status_code']==self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.nw_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Get Network's ('%s') info SUCCESS." % self.dm.nw_name )
                self.flag = True
            else:
                LogPrint().error("FAIL: Get Network's ('%s') info INCORRECT." % self.dm.nw_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Get Network info FAILED. Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def test_GetNetworkInfo_id(self):
        '''
        @summary: 测试用例执行步骤
        @note: （1）根据ID获取指定逻辑网络的信息；
        @note: （2）验证接口返回的状态码、接口信息是否正确。
        '''
        # 测试1：根据网络id获取网络信息
        nw_id = self.nwapi.getNetworkIdByName(self.dm.nw_name, self.dm.dc_name)
        LogPrint().info("Test: Get the network's ('%s') info by id ('%s')." % (self.dm.nw_name, nw_id))
        r = self.nwapi.getNetworkInfo(nw_id=nw_id)
        if r['status_code']==self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.nw_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Get Network info SUCCESS by ID." )
                self.flag = True
            else:
                LogPrint().error("FAIL: Get Network info INCORRECT by ID.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Get Network info FAILED. Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)

    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test: Delete network '%s'." % self.dm.nw_name)
        self.assertTrue(smart_delete_network(self.dm.nw_name,self.dm.dc_name))    

class ITC05010301_CreateNetwork(BaseTestCase):
    '''
    @summary: ITC-05网络管理-01基本操作-03创建一个新的网络-01成功创建
    @note: 为简化测试，均默认在Default数据中心内创建
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #检查数据中心内是否已有该网络，如果有，删除它 
#         if self.nwapi.searchNetworkByName(self.dm.nw_name):
#             self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name) 
        self.assertTrue(smart_delete_network(self.dm.nw_name, self.dm.dc_name))
        
    def test_CreateNetwork(self): 
        r = self.nwapi.createNetwork(self.dm.nw_info)
        if r['status_code'] == self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.nw_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Create Network  SUCCESS." )
                self.flag = True
            else:
                LogPrint().error("FAIL: Create Network's info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Create Network FAILED. Returned status code '%s' is Wrong." % r['status_code'] )
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        self.assertTrue(smart_delete_network(self.dm.nw_name,self.dm.dc_name)) 
        
class ITC05010302_CreateNetwork_VerifyName(BaseTestCase):
    '''
    @summary: ITC-05网络管理-01基本操作-03创建一个新的网络-02验证名称合法性
    @note: 为简化测试，均默认在Default数据中心内创建
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs() 
          
    def test_CreateNetwork_VerifyName(self):
        '''
        @summary: 验证名称合法性，分为两种：1）包含非法字符 2）字符长度超出范围。检查返回状态码和提示信息
        ''' 
        # 本用例有多种测试情况，所以期望结果也有多种，这个变量代表期望结果的索引值
        self.expected_result_index = 0
        # 使用数据驱动，根据测试数据文件循环创建多个网络
        @BaseTestCase.drive_data(self, self.dm.nw_info)
        def do_test(xml_info):
            r = self.nwapi.createNetwork(xml_info)
            if r['status_code']==self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.expected_result_index]), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT.")
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned messages are INCORRECT.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' is WRONG while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
                self.flag = False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
   
class ITC05010303_CreateNetwork_DupName(BaseTestCase):
    '''
    @summary: ITC-05网络管理-01基本操作-03创建一个新的网络-03同一数据中心内网络重名
    @note: 为简化测试，均默认在Default数据中心内创建
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()
        '''
        @note: 如果该数据中心内不存在网络，就创建一个网络
        '''
#         print self.nwapi.searchNetworkByName(self.dm.nw_name)
        if not self.nwapi.searchNetworkByName(self.dm.nw_name)['result']['networks']:
            self.nwapi.createNetwork(self.dm.nw_info) 
          
    def test_CreateNetwork_DupName(self):
        '''
        @note: 检查返回状态码和提示信息
        '''
        r = self.nwapi.createNetwork(self.dm.nw_info)
#         print r['result']
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            print xmltodict.parse(self.dm.expected_info)
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when create dup network.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECCT when create dup network.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        self.assertTrue(smart_delete_network(self.dm.nw_name,self.dm.dc_name))
        
class ITC05010304_CreateNetwork_NoRequired(BaseTestCase):
    '''
    @summary: ITC-05网络管理-01基本操作-03创建一个新的网络-04缺少必填项
    @note: 为简化测试，均默认在Default数据中心内创建
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs() 
          
    def test_CreateNetwork_NoRequired(self):
        '''
        @summary: 缺少必填项：网络名称和所在数据中心id。检查返回状态码和提示信息
        ''' 
        # 本用例有多种测试情况，所以期望结果也有多种，这个变量代表期望结果的索引值
        self.expected_result_index = 0
        
        # 使用数据驱动，根据测试数据文件循环创建多个网络
        @BaseTestCase.drive_data(self, self.dm.nw_info)
        def do_test(xml_info):
            r = self.nwapi.createNetwork(xml_info)
            if r['status_code']==self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.expected_result_index]), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT.")
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned messages are INCORRECT.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
                self.flag = False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()

class ITC05010305_CreateNetwork_DupVlan(BaseTestCase):
    '''
    @summary: ITC-05网络管理-01基本操作-03创建一个新的网络-05同一数据中心内网络vlan id重复
    @note: 为简化测试，均默认在Default数据中心内创建
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()
        #创建一个网络，vlan id=2
        self.assertTrue(smart_create_network(self.dm.nw_info1, self.dm.nw_name1))
        
    def test_CreateNetwork_DupVlan(self):
        '''
        @note: 检查返回状态码和提示信息
        '''
        r = self.nwapi.createNetwork(self.dm.nw_info2)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when create dup_vlan network.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECCT when create dup_vlan network.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)

    def tearDown(self):
        self.assertTrue(smart_delete_network(self.dm.nw_name1,self.dm.dc_name))
        
class ITC05010401_UpdateNetwork(BaseTestCase):
    '''
    @summary: ITC-05网络管理-01基本操作-04编辑网络-01成功编辑
    @note: 为简化测试，在Default数据中心内进行网络操作
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络 
        self.assertTrue(smart_create_network(self.dm.nw_info, self.dm.nw_name)) 
        
    def test_UpdateNetwork(self): 
        r = self.nwapi.updateNetwork(self.dm.nw_name, self.dm.dc_name, self.dm.update_info)
        if r['status_code'] == self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.update_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Update Network info SUCCESS." )
                self.flag = True
            else:
                LogPrint().error("FAIL: Update Network info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Update Network info FAILED. Returned status code '%s' is WRONG." % r['status_code'] )
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        #删除该网络，清空环境
        self.assertTrue(smart_delete_network(self.dm.new_nw_name,self.dm.dc_name))
        
class ITC05010402_UpdateNetwork_DupName(BaseTestCase):
    '''
    @summary: ITC-05网络管理-01基本操作-04编辑网络-02网络名称重复
    @note: 为简化测试，在Default数据中心内进行网络操作
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建两个网络network001和network002 
        self.assertTrue(smart_create_network(self.dm.nw_info1, self.dm.nw_name1)) 
        self.assertTrue(smart_create_network(self.dm.nw_info2, self.dm.nw_name2))  
        
    def test_UpdateNetwork(self):
        #对network001进行编辑：名称修改为network002 
        r = self.nwapi.updateNetwork(self.dm.nw_name1, self.dm.dc_name, self.dm.update_info)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: The returned status code and messages are CORRECT when update dup network.")
                self.flag = True
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECCT when update dup network.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        #删除该网络，清空环境
        self.assertTrue(smart_delete_network(self.dm.nw_name1,self.dm.dc_name))
        self.assertTrue(smart_delete_network(self.dm.nw_name2,self.dm.dc_name))

class ITC050105_DeleteNetwork(BaseTestCase):
    '''
    @summary: ITC-05网络管理-01基本操作-05删除网络
    @note: 为简化测试，在Default数据中心内进行网络操作
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络 
        self.assertTrue(smart_create_network(self.dm.nw_info, self.dm.nw_name))
        
    def test_UpdateNetwork(self): 
        r = self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
        if r['status_code'] == self.dm.expected_status_code:
            if not self.nwapi.isNetworkExist(self.dm.nw_name, self.dm.dc_name):
                LogPrint().info("PASS: Delete network success.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Delete network fail.The network is still exist.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag) 
        
    def tearDown(self):
        '''
        @summary: 删除该网络，清空环境
        '''
        self.assertTrue(smart_delete_network(self.dm.nw_name,self.dm.dc_name))

class ITC050201_GetNetworkProfileList(BaseTestCase):
    '''
    @summary: 测试环境准备，创建一个网络并为它创建若干配置集
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        
        #首先新建一个网络并获取其id
        LogPrint().info("Pre-Test-1: Create a new network '%s'." % self.dm.nw_name)
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        
        #为该网络创建多个配置集
        LogPrint().info("Pre-Test-2: Create multi-profiles for network '%s'." % self.dm.nw_name) 
        self.proapi = ProfilesAPIs()
        @BaseTestCase.drive_data(self, self.dm.profile_info)
        def do_test(xml_info):
            self.proapi.createProfiles(xml_info,self.nw_id)
        do_test()
  
    def test_GetNetworkProfileList(self):
        '''
        @summary: 获取网络的配置集列表
        '''
        self.nwproapi = NetworkProfilesAPIs()
        LogPrint().info("Test: To get all NetworkProfiles list.")
        r = self.nwproapi.getNetworkProfileList(self.nw_id)
        if r['status_code']==self.dm.expected_status_code:
            LogPrint().info('PASS: Get NetworkProfile list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error('FAIL: Get Network Profile list FAIL. Returned status code "%s" is WRONG.' % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 清除该网络及配置集
        '''
        LogPrint().info("Post-Test: Delete network '%s' and it's profiles." % self.dm.nw_name)
        self.assertTrue(smart_delete_network(self.dm.nw_name,self.dm.dc_name))

class ITC050202_GetNetworkProfileInfo(BaseTestCase):
    '''
    @summary: 测试环境准备，创建一个网络并为它创建若干配置集
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        #为该网络创建多个配置集 
        self.proapi = ProfilesAPIs()
        self.proapi.createProfiles(self.dm.profile_info,self.nw_id)
  
    def test_GetNetworkProfileInfo(self):
        '''
        @summary: 获取网络的配置集信息
        '''
        self.nwproapi = NetworkProfilesAPIs()
        r = self.nwproapi.getNetworkProfileInfo(self.nw_id, self.dm.profile_name)
        if r['status_code']==self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse((self.dm.profile_info %self.nw_id))
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Get NetworkProfile Info SUCCESS." )
                self.flag = True
            else:
                LogPrint().error("FAIL: Get NetworkProfile Info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Get NetworkProfile Info FAILED. Returned status code '%s' is WRONG." % r['status_code'] )
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 清除该网络及配置集
        '''
        LogPrint().info("Post-Test: Delete network '%s' and it's profiles." % self.dm.nw_name)
        self.assertTrue(smart_delete_network(self.dm.nw_name,self.dm.dc_name))    
        
class ITC05_TearDown(BaseTestCase):
    '''
    @summary: “集群管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: 删除数据中心；
    '''
    def test_TearDown(self):
        dcapi = DataCenterAPIs()
        if dcapi.searchDataCenterByName(ModuleData.dc_name)['result']['data_centers']:
            LogPrint().info("Post-Module-Test: Delete DataCenter '%s'." % ModuleData.dc_name)
            dcapi.delDataCenter(ModuleData.dc_name)   

if __name__ == "__main__":

    test_cases = ["Network.ITC05010305_CreateNetwork_DupVlan"]
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)