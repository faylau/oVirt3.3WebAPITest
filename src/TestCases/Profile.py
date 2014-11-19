#encoding:utf-8
<<<<<<< HEAD
__authors__ = ['"Wei Keke" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

=======

__authors__ = ['"Wei Keke" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

>>>>>>> 640e45190e0c83f29b30a1cc21b2da390cc17eda
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
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from TestAPIs.NetworkAPIs import NetworkAPIs
from TestAPIs.ProfilesAPIs import ProfilesAPIs
from TestAPIs.DataCenterAPIs import DataCenterAPIs
from TestData.Profile import ITC09_SetUp as ModuleData

import xmltodict

class ITC09_SetUp(BaseTestCase):
    '''
    @summary: “配置集管理”模块测试环境初始化（执行该模块测试用例时，都需要执行该用例搭建初始化环境）
    @note: （1）创建一个数据中心（NFS）；
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()

    def test_Create_DC(self):
        '''
        @summary: 创建一个数据中心
        '''
        dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Module-Test: Create DataCenter '%s'." % self.dm.dc_name)
        dcapi.createDataCenter(self.dm.dc_info)


class ITC0901_GetProfileList(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-01获取所有配置集列表
    '''
    def test_GetProfileList(self):
        '''
        @summary: 获取系统配置集列表
        @note: 操作成功，验证返回状态码
        '''
        self.proapi = ProfilesAPIs()
        LogPrint().info("Test: Get profile list.")
        r = self.proapi.getProfilesList()
        if r['status_code'] == 200:
            LogPrint().info('PASS: Get profile list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error('FAIL: Returned status code is WRONG.')
            self.flag = False
        self.assertTrue(self.flag)
    
class ITC0902_GetProfileInfo(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-02获取指定配置集信息
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        LogPrint().info("Pre-Test-1: Create a network %s for TC."%self.dm.nw_name)
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        self.proapi = ProfilesAPIs()
        LogPrint().info("Pre-Test-2: Create a profile %s for this network."%self.dm.profile_name)
        self.proapi.createProfiles(self.dm.profile_info,self.nw_id)
        
    def test_GetProfileInfo_byname(self):
        '''
        @summary: 根据配置集名称获取其信息
        @note: 操作成功，验证返回状态码，验证接口返回信息
        '''
        self.flag = True
        r = self.proapi.getProfileInfo(profile_name=self.dm.profile_name, nw_id=self.nw_id)
        LogPrint().info("Test-1: Get profile %s by NAME."%self.dm.profile_name)
        if r['status_code'] == self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse((self.dm.profile_info %self.nw_id))
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Get Profile info SUCCESS." )
            else:
                LogPrint().error("FAIL:Returned Profile info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is %s not %s. "% (r['status_code'], self.dm.expected_status_code) )
            self.flag = False
        self.assertTrue(self.flag)
    
    def test_GetProfileInfo_id(self):
        '''
        @summary: 根据配置集id获取信息
        @note: 操作成功，验证返回状态码，验证接口返回信息
        '''
        # 测试1：根据网络id获取网络信息
        self.flag = True
        LogPrint().info("Test-2: Get profile %s by ID."%self.dm.profile_name)
        profile_id = self.proapi.getProfileIdByName(self.dm.profile_name, self.nw_id)
        r = self.proapi.getProfileInfo(profile_id=profile_id)
        if r['status_code'] == self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse((self.dm.profile_info %self.nw_id))
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Get Profile info SUCCESS.")
            else:
                LogPrint().error("FAIL:Returned Profile info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is %s not %s. "% (r['status_code'], self.dm.expected_status_code))
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test: Delete the network %s."%self.dm.nw_name)
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)      

class ITC090301_CreateProfile(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-03创建配置集-01成功创建
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        LogPrint().info("Pre-Test: Create a network %s for TC."%self.dm.nw_name)
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
         
    def test_CreateProfile(self):
        '''
        @summary: 创建配置集
        @note: 操作成功，验证返回状态码，验证接口返回信息
        ''' 
        self.flag = True
        self.proapi = ProfilesAPIs()
        LogPrint().info("Test: Create a profile %s for network %s."%(self.dm.profile_name, self.dm.nw_name))
        r = self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
        if r['status_code'] == self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse((self.dm.profile_info %self.nw_id))
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Create profile %s for network %s SUCCESS."%(self.dm.profile_name, self.dm.nw_name))
#                 return True
            else:
                LogPrint().error("FAIL:Returned Profile info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is %s not %s. "% (r['status_code'], self.dm.expected_status_code) )
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        LogPrint().info("Post-Test: Delete the network %s."%self.dm.nw_name)
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
        
class ITC090302_CreateProfile_VerifyName(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-03创建配置集-02验证名称合法性
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        LogPrint().info("Pre-Test: Create a network %s for TC."%self.dm.nw_name)
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
          
    def test_CreateProfile_VerifyName(self):
        '''
        @summary: 验证名称合法性：包含非法字符
        @note: 操作失败，验证返回状态码和报错信息
        ''' 
        self.proapi = ProfilesAPIs()
        self.flag = True
        LogPrint().info("Test: Create a profile for network %s."%self.dm.nw_name)
        r = self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS: The returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
            self.flag = False
        self.assertTrue(self.flag)
              
    def tearDown(self):
        LogPrint().info("Post-Test: Delete the network %s."%self.dm.nw_name)
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
   
class ITC090303_CreateProfile_DupName(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-03新建一个配置集-03名称重复
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        LogPrint().info("Pre-Test-1: Create a network %s for TC."%self.dm.nw_name)
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        #创建一个配置集
        LogPrint().info("Pre-Test-2: Create a profile %s for this network."%self.dm.profile_name)
        self.proapi = ProfilesAPIs()
        self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
          
    def test_CreateProfile_DupName(self):
        '''
        @note: 操作失败，检查返回状态码和提示信息
        '''
        self.flag = True
        LogPrint().info("Test: Create a dupname profile for network %s."% self.dm.nw_name)
        r = self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: The returned status code and messages are CORRECT when create dup profile.")
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECCT when create dup profile.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete the network %s."%self.dm.nw_name)
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
        
class ITC090304_CreateProfile_NoRequired(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-03创建一个配置集-04验证参数完整性
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        LogPrint().info("Pre-Test: Create a network %s for TC."%self.dm.nw_name)
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
          
    def test_CreateProfile_NoRequired(self):
        '''
        @summary: 分为三种情况，1）缺少名称 2）缺少网络id 3）提供网络名称而非网络id
        @note: 操作失败，验证返回状态码和报错信息
        ''' 
        self.expected_result_index = 0
        self.proapi = ProfilesAPIs()
        @BaseTestCase.drive_data(self, self.dm.profile_info)
        def do_test(xml_info):
            self.flag = True
            LogPrint().info("Test: Create a profile for network %s."%self.dm.nw_name)
            r = self.proapi.createProfiles(xml_info)
            if r['status_code']==self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.expected_result_index]), r['result']):
                    LogPrint().info("PASS: The returned status code and messages are CORRECT.")
                else:
                    LogPrint().error("FAIL: The returned messages are INCORRECT.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: The returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
                self.flag = False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete the network %s."%self.dm.nw_name)
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
         
class ITC090401_UpdateProfile(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-04编辑配置集-01成功编辑
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        LogPrint().info("Pre-Test-1: Create a network %s for TC."%self.dm.nw_name)
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        self.proapi = ProfilesAPIs()
        LogPrint().info("Pre-Test-2: Create a profile %s for this network."%self.dm.profile_name)
        self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
        
    def test_UpdateProfile(self): 
        '''
        @summary: 编辑配置集
        @note: 操作成功，验证返回状态码，验证接口返回信息
        ''' 
        self.flag = True
        LogPrint().info("Test: Update profile %s of network %s."%(self.dm.profile_name, self.dm.nw_name))
        r = self.proapi.updateProfile(self.dm.profile_name, self.nw_id, self.dm.update_info)
        if r['status_code'] == self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.update_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Update Profile info SUCCESS." )
            else:
                LogPrint().error("FAIL: Update Profile info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code)  )            
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        #删除该网络，清空环境
        LogPrint().info("Post-Test: Delete the network %s."%self.dm.nw_name)
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
        
        
class ITC090402_UpdateProfile_DupName(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-04编辑配置集-01重名
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        LogPrint().info("Pre-Test-1: Create a network %s for TC."%self.dm.nw_name)
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        #创建两个配置集
        self.proapi = ProfilesAPIs()
        LogPrint().info("Pre-Test-2: Create a profile %s for this network."%self.dm.profile_name1)
        self.proapi.createProfiles(self.dm.profile_info1, self.nw_id)
        LogPrint().info("Pre-Test-3: Create a profile %s for this network."%self.dm.profile_name2)
        self.proapi.createProfiles(self.dm.profile_info2, self.nw_id)
        
    def test_UpdateProfile(self):
        '''
        @summary: 编辑配置集,重名
        @note: 操作失败，验证返回状态码，验证报错信息
        ''' 
        #编辑配置集1，使其名字和配置集2重名 
        self.flag = True
        LogPrint().info("Test: Update profile %s.Set its name be %s."%(self.dm.profile_name1, self.dm.profile_name2))
        r = self.proapi.updateProfile(self.dm.profile_name1, self.nw_id, self.dm.update_info)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: The returned status code and messages are CORRECT when update dup profile.")
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECCT when update dup profile.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        #删除该网络，清空环境
        LogPrint().info("Post-Test: Delete the network %s."%self.dm.nw_name)
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)    
            
class ITC090403_UpdateProfile_DiffNw(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-04编辑配置集-03更改所在网络
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先网络并获取其id
        LogPrint().info("Pre-Test-1: Create a network %s for TC."%self.dm.nw_name)
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        #为网络创建一个配置集
        LogPrint().info("Pre-Test-2: Create a profile %s for this network."%self.dm.profile_name)
        self.proapi = ProfilesAPIs()
        self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
        
    def test_UpdateNetwork(self):
        '''
        @summary: 编辑配置集,更改所属网络
        @note: 操作失败，验证返回状态码，验证报错信息
        ''' 
        self.flag = True
        LogPrint().info("Test: Update profile %s.Change its network."%self.dm.profile_name)
        r = self.proapi.updateProfile(self.dm.profile_name, self.nw_id, self.dm.update_info)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: The returned status code and messages are CORRECT when update dup network.")
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECCT when update dup network.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        #删除该网络，清空环境
        LogPrint().info("Post-Test: Delete the network %s."%self.dm.nw_name)
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
        
class ITC0905_DeleteProfile(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-05删除配置集
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先网络并获取其id
        LogPrint().info("Pre-Test-1: Create a network %s for TC."%self.dm.nw_name)
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        #为网络创建一个配置集
        LogPrint().info("Pre-Test-2: Create a profile %s for this network."%self.dm.profile_name)
        self.proapi = ProfilesAPIs()
        self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
        
    def test_DeleteProfile(self):
        '''
        @summary: 删除配置集
        @note: 操作成功，验证返回状态码，验证配置集是否存在
        '''  
        self.flag = True
        LogPrint().info("Test: Delete profile %s."%self.dm.profile_name)
        r = self.proapi.delProfile(self.dm.profile_name, self.nw_id)
        if r['status_code'] == self.dm.expected_status_code:
            if not self.proapi.isExist(self.dm.profile_name, self.nw_id):
                LogPrint().info("PASS: Delete profile %s SUCCESS."%self.dm.profile_name)
            else:
                LogPrint().error("FAIL: Profile %s is still exist."%self.dm.profile_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag) 
        
    def tearDown(self):
        #删除该网络，清空环境
        LogPrint().info("Post-Test: Delete the network %s."%self.dm.nw_name)
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)

class ITC09_TearDown(BaseTestCase):
    '''
    @summary: “配置集管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: 删除数据中心；
    '''
    def test_TearDown(self):
        dcapi = DataCenterAPIs()
        if dcapi.searchDataCenterByName(ModuleData.dc_name)['result']['data_centers']:
            LogPrint().info("Post-Module-Test: Delete DataCenter '%s'." % ModuleData.dc_name)
            dcapi.delDataCenter(ModuleData.dc_name)          

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test_cases = ["Profile.ITC09_TearDown"]
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)