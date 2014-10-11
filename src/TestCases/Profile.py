#encoding:utf-8
'''

@author: keke
'''

import unittest

from BaseTestCase import BaseTestCase
from TestAPIs.NetworkAPIs import NetworkAPIs, NetworkProfilesAPIs
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from Utils.HTMLTestRunner import HTMLTestRunner
from TestAPIs.ProfilesAPIs import ProfilesAPIs

import xmltodict

class ITC0601_GetProfileList(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-01获取所有配置集列表
    '''
  
    def test_GetProfileList(self):
        
        self.proapi = ProfilesAPIs()
        r = self.proapi.getProfilesList()
        if r['status_code']==200:
            LogPrint().info('Get profile list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error('Get profile list FAIL.')
            self.flag = False
        self.assertTrue(self.flag)
    
class ITC0602_GetProfileInfo(BaseTestCase):
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
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        self.proapi = ProfilesAPIs()
        self.proapi.createProfiles(self.dm.profile_info,self.nw_id)
        
    def test_GetProfileInfo_byname(self):
        '''
        @summary: 根据配置集名称获取其信息
        '''
        r = self.proapi.getProfileInfo(profile_name=self.dm.profile_name, nw_id=self.nw_id)
        print r['status_code']
        if r['status_code']==self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse((self.dm.profile_info %self.nw_id))
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Get Profile info SUCCESS." )
#                 return True
            else:
                LogPrint().error("Get Profile info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Get Profile info FAILED. " )
            self.flag = False
        self.assertTrue(self.flag)
    
    def test_GetProfileInfo_id(self):
        '''
        @summary: 根据配置集id获取信息
        '''
        # 测试1：根据网络id获取网络信息
        profile_id = self.proapi.getProfileIdByName(self.dm.profile_name, self.nw_id)
        r = self.proapi.getProfileInfo(profile_id=profile_id)
        if r['status_code']==self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse((self.dm.profile_info %self.nw_id))
            print dict_actual
            print dict_expected
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Get Profile info SUCCESS." )
#                 return True
            else:
                LogPrint().error("Get Profile info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Get Profile info FAILED. " )
            self.flag = False
        self.assertTrue(self.flag)
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)      

class ITC060301_CreateProfile(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-03创建配置集-01成功创建
    @note: 为简化测试，均默认在Default数据中心内创建
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
         
    def test_CreateProfile(self): 
        self.proapi = ProfilesAPIs()
        r = self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
        if r['status_code'] == self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse((self.dm.profile_info %self.nw_id))
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Create Profile  SUCCESS." )
#                 return True
            else:
                LogPrint().error("Create Profile  INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Create Profile  FAILED. " )
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
        

class ITC060302_CreateProfile_VerifyName(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-03创建配置集-02验证名称合法性
    @note: 为简化测试，均默认在Default数据中心内创建
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
          
    def test_CreateProfile_VerifyName(self):
        '''
        @summary: 验证名称合法性：包含非法字符
        ''' 
        self.expected_result_index = 0
        self.proapi = ProfilesAPIs()
        @BaseTestCase.drive_data(self, self.dm.profile_info)
        def do_test(xml_info):
            self.flag = True
            print xml_info
            r = self.proapi.createProfiles(xml_info,self.nw_id)
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
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
   
class ITC060303_CreateProfile_DupName(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-03新建一个配置集-03名称重复
    @note: 为简化测试，均默认在Default数据中心内创建
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        #创建一个配置集
        self.proapi = ProfilesAPIs()
        self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
          
    def test_CreateProfile_DupName(self):
        '''
        @note: 检查返回状态码和提示信息
        '''
        r = self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
        print r['result']
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            print xmltodict.parse(self.dm.expected_info)
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
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
        
class ITC060304_CreateProfile_NoRequired(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-03创建一个配置集-04验证参数完整性
    @note: 为简化测试，均默认在Default数据中心内创建
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
          
    def test_CreateProfile_NoRequired(self):
        '''
        @summary: 分为三种情况，1）缺少名称 2）缺少网络id 3）提供网络名称而非网络id
        ''' 
        self.expected_result_index = 0
        self.proapi = ProfilesAPIs()
        @BaseTestCase.drive_data(self, self.dm.profile_info)
        def do_test(xml_info):
            self.flag = True
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
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)


        
class ITC060401_UpdateProfile(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-04编辑配置集-01成功编辑
    @note: 为简化测试，在Default数据中心内进行网络操作
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        self.proapi = ProfilesAPIs()
        self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
        
    def test_UpdateProfile(self): 
        r = self.proapi.updateProfile(self.dm.profile_name, self.nw_id, self.dm.update_info)
        if r['status_code'] == self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.update_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Update Profile info SUCCESS." )
#                 return True
            else:
                LogPrint().error("Update Profile info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Update Profile info FAILED. " )
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        #删除该网络，清空环境
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
        
        
class ITC060402_UpdateProfile_DupName(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-04编辑配置集-01重名
    @note: 为简化测试，在Default数据中心内进行网络操作
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先新建一个网络并获取其id
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        #创建两个配置集
        self.proapi = ProfilesAPIs()
        self.proapi.createProfiles(self.dm.profile_info1, self.nw_id)
        self.proapi.createProfiles(self.dm.profile_info2, self.nw_id)
        
    def test_UpdateProfile(self):
        #编辑配置集1，使其名字和配置集2重名 
        r = self.proapi.updateProfile(self.dm.profile_name1, self.nw_id, self.dm.update_info)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            print xmltodict.parse(self.dm.expected_info)
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
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)    
            
class ITC060403_UpdateProfile_DiffNw(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-04编辑配置集-03更改所在网络
    @note: 为简化测试，在Default数据中心内进行网络操作
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先网络并获取其id
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        #为网络创建一个配置集
        self.proapi = ProfilesAPIs()
        self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
        
    def test_UpdateNetwork(self):
        #编辑配置集，使其网络id为空
        r = self.proapi.updateProfile(self.dm.profile_name, self.nw_id, self.dm.update_info)
        print r
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
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
        

class ITC0605_DeleteProfile(BaseTestCase):
    '''
    @summary: ITC-06配置集管理-05删除配置集
    @note: 为简化测试，在Default数据中心内进行网络操作
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.nwapi = NetworkAPIs()  
        #首先网络并获取其id
        self.nw_id = self.nwapi.createNetwork(self.dm.nw_info)['result']['network']['@id']
        #为网络创建一个配置集
        self.proapi = ProfilesAPIs()
        self.proapi.createProfiles(self.dm.profile_info, self.nw_id)
    def test_DeleteProfile(self): 
        r = self.proapi.delProfile(self.dm.profile_name, self.nw_id)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: The returned status code and messages are CORRECT when delete profile.")
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECCT when delete profile.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag) 
    def tearDown(self):
        #删除该网络，清空环境
        self.nwapi.delNetwork(self.dm.nw_name, self.dm.dc_name)
       

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test_cases = ["Profile.ITC0605_DeleteProfile"]
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)