#encoding:utf-8


__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/09          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
# V0.2           2014/11/13          *调整代码格式                                                  Liu Fei
#                                    *修正ITC03010307中的问题                        
#                                    *注释掉了未完成的2个TC             
#---------------------------------------------------------------------------------
'''

import unittest

import xmltodict

from BaseTestCase import BaseTestCase
from TestAPIs.DataCenterAPIs import DataCenterAPIs, smart_attach_storage_domain, smart_deactive_storage_domain
from TestAPIs.HostAPIs import HostAPIs, HostNicAPIs, smart_create_host, smart_del_host
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.StorageDomainAPIs import smart_create_storage_domain, smart_del_storage_domain
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from Utils.Util import wait_until
from TestData.Host import ITC03_SetUp as ModuleData


class ITC03_SetUp(BaseTestCase):
    '''
    @summary: “主机管理”模块测试环境初始化（执行该模块测试用例时，都需要执行该用例搭建初始化环境）
    @note: （1）创建一个数据中心（NFS）；
    @note: （2）创建一个集群；
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()

    def test_Create_DC_Cluster(self):
        '''
        @summary: 创建一个数据中心和一个集群
        '''
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        LogPrint().info("Pre-Module-Test-1: Create DataCenter '%s'." % self.dm.dc_name)
        dcapi.createDataCenter(self.dm.dc_info)
        LogPrint().info("Pre-Module-Test-2: Create Cluster '%s' in DataCenter '%s'." % (self.dm.cluster_name, self.dm.dc_name))
        capi.createCluster(self.dm.cluster_info)
        
class ITC030101_GetHostsList(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-01获取主机列表
    '''
    def test_GetDataCentersList(self):
        '''
        @summary: 测试步骤
        @note: （1）获取全部主机列表；
        @note: （2）操作成功，验证接口返回的状态码是否正确。
        '''
        host_api = HostAPIs()
        LogPrint().info("Test: Get all hosts list in all DataCenters.")
        r = host_api.getHostsList()
        if r['status_code'] == 200:
            LogPrint().info('PASS: Get Hosts list SUCCESS.')
        else:
            LogPrint().error('FAIL: Get Hosts list FAILED. Returned status code "%s" is INCORRECT.' % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)

class ITC030102_GetHostInfo(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-02查看主机信息
    '''
    def setUp(self):
        '''
        @summary: 测试环境准备－创建1个主机，并将其加入到模块级的数据中心和集群中。
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        
        # 创建一个主机，并等待其变为UP状态。
        LogPrint().info("Pre-Test: Create a host '%s' for this test case." % self.dm.host_name)
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
    def test_GetHostInfo(self):
        '''
        @summary: 测试用例执行步骤
        @note: （1）查询指定主机信息
        @note: （2）验证接口返回状态验证码、结果是否正确
        '''
        host_api = HostAPIs()
        def is_host_up():
            return host_api.getHostStatus(self.dm.host_name)=='up'
        if wait_until(is_host_up, 120, 5):
            r = host_api.getHostInfo(self.dm.host_name)
            if r['status_code']==self.dm.status_code:
                dictCompare = DictCompare()
                d1 = xmltodict.parse(self.dm.xml_host_info)
                del d1['host']['root_password']
                if dictCompare.isSubsetDict(d1, r['result']):
                    LogPrint().info("PASS: Get host '%s' info SUCCESS." % self.dm.host_name)
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Get host info incorrectly.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' is INCORRECT." % r['status_code'])
                self.flag = False
            self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源回收（删除创建的主机）
        '''
        LogPrint().info("Post-Test: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name, self.dm.xml_del_option))

class ITC03010301_CreateHost_Normal(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-03创建-01常规创建
    '''
    def setUp(self):
        '''
        @summary: 测试环境准备－创建1个主机，并将其加入到模块级的数据中心和集群中。
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        
    def test_GetHostInfo(self):
        '''
        @summary: 测试用例执行步骤
        @note: （1）查询指定主机信息
        @note: （2）验证接口返回状态验证码、结果是否正确
        '''
        host_api = HostAPIs()
        LogPrint().info('Test: Create Host "%s" in Cluster "%s".' % (self.dm.host_name, ModuleData.cluster_name))
        r = host_api.createHost(self.dm.xml_host_info)
        def is_host_up():
            return host_api.getHostStatus(self.dm.host_name)=='up'
        if wait_until(is_host_up, 200, 5):
            if r['status_code']==self.dm.status_code:
                dictCompare = DictCompare()
                d1 = xmltodict.parse(self.dm.xml_host_info)
                del d1['host']['root_password']
                if dictCompare.isSubsetDict(d1, r['result']):
                    LogPrint().info("PASS: Create host '%s' SUCCESS." % self.dm.host_name)
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned info of created host are incorrectly.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' is INCORRECT." % r['status_code'])
                self.flag = False
        else:
            self.flag = False
            LogPrint().error("FAIL: Create host '%s' FAILED. The state of host is '%s'." % (self.dm.host_name, self.host_api.getHostStatus(self.dm.host_name)))

        
    def tearDown(self):
        '''
        @summary: 资源回收（删除创建的主机）
        '''
        LogPrint().info("Post-Test: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name, self.dm.xml_del_option))

class ITC03010302_CreateHost_PowerManagement(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-03创建-02电源管理
    @note: 本用例只针对IPMI类型的电源管理接口进行测试，若需要使用ILO等，则需要根据实现情况修改测试数据中的主机电源管理配置信息。
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据以及测试环境
        @note: （1）创建第一个主机host1（不带电源管理）
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提：创建第一个主机host1，并等待其变为UP状态
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % self.dm.host1_name)
        self.assertTrue(smart_create_host(self.dm.host1_name, self.dm.xml_host1_info))
        
    def test_CreateHost_PowerManagement(self):
        '''
        @summary: 测试步骤
        @note: （1）创建第二个带有电源管理配置的主机host2
        @note: （2）创建成功，验证接口返回的状态码、host2信息是否正确。
        '''
        self.host_api = HostAPIs()
        LogPrint().info("Test: Create 2nd host '%s' with power management." % self.dm.host2_name)
        r = self.host_api.createHost(self.dm.xml_host2_info)
        def is_host_up():
            return self.host_api.getHostStatus(self.dm.host2_name)=='up'
        if wait_until(is_host_up, 200, 5):
            if r['status_code'] == self.dm.expected_status_code_create_host:
                dictCompare = DictCompare()
                d1 = xmltodict.parse(self.dm.xml_host2_info)
                del d1['host']['root_password']
                del d1['host']['power_management']['password']
                d2 = r['result']
                if dictCompare.isSubsetDict(d1, d2):
                    LogPrint().info("PASS: Create 2ed host '%s' SUCCESS." % self.dm.host2_name)
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Create 2ed host '%s' with Power Management FAILED. It's configurations are INCORRECT." % self.dm.host2_name)
                    self.flag = True
            else:
                LogPrint().error("FAIL: Create 2ed host '%s' with Power Management FAILED. Returned status code is INCORRECT." % self.dm.host2_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Create 2ed host '%s' with Power Management FAILED. It's state is not 'UP'." % self.dm.host2_name)
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理，分别删除两个创建的主机。
        '''
        hosts_list = [self.dm.host2_name, self.dm.host1_name]
        for host in hosts_list:
            LogPrint().info("Post-Test: Delete host '%s'." % host)
            self.assertTrue(smart_del_host(host, self.dm.xml_host_del_option))

class ITC03010303_CreateHost_DupName(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-03创建-03重名
    '''
    def setUp(self):
        '''
        @summary: 测试环境准备
        @note: 创建1个主机
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        # 前提1：创建1个主机
        LogPrint().info("Pre-Test: Create 1st host '%s' for this TC." % self.dm.host_name)
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
    
    def test_CreateHost_DupName(self):
        '''
        @summary: 测试步骤
        @note: （1）创建一个重名的主机
        @note: （2）操作失败，验证接口返回状态码、返回提示信息是否正确。
        '''
        host_api = HostAPIs()
        LogPrint().info("Test: Create 2nd host with duplicate name.")
        r = host_api.createHost(self.dm.xml_host_info)
        if r['status_code']==self.dm.status_code:
            dictCompare = DictCompare()
            d1 = xmltodict.parse(self.dm.expect_result)
            if dictCompare.isSubsetDict(d1, r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when creating host with duplicate name.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are incorrectly.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT." % r['status_code'])
            self.flag = False
            
    def tearDown(self):
        '''
        @summary: 清理资源
        @note: 删除创建的主机
        '''
        LogPrint().info("Post-Test: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name, self.dm.xml_del_option))

class ITC03010304_CreateHost_NameVerify(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-03创建-04名称有效性验证
    '''
    def setUp(self):
        '''
        @summary: 初始化测试环境（获取相应的测试数据）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateHost_NameVerify(self):
        '''
        @summary: 测试步骤
        @note: （1）输入各种不合法的name，创建主机；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        host_api = HostAPIs()
        
        # 本用例有多种测试情况，所以期望结果也有多种，这个变量代表期望结果的索引值
        self.expected_result_index = 0
        
        # 使用数据驱动，根据测试数据文件循环创建多个名称非法的主机。
        @BaseTestCase.drive_data(self, self.dm.xml_host_info)
        def do_test(xml_info):
            r = host_api.createHost(xml_info)
            # 比较接口返回状态码、提示信息是否正确
            if r['status_code'] == self.dm.expected_status_code:
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
    
    def tearDown(self):
        '''
        @summary: 资源清理，若上述主机创建成功则需要将其删除。
        '''
        pass
    
class ITC03010305_CreateHost_IpVerify(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-03创建-05IP有效性验证
    '''
    def setUp(self):
        '''
        @summary: 初始化测试环境
        '''
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateHost_IpVerify(self):
        '''
        @summary: 测试步骤
        @note: （1）输入各种不合法的IP，创建主机；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        host_api = HostAPIs()
        # 使用数据驱动，根据测试数据文件循环创建多个名称非法的主机
        @BaseTestCase.drive_data(self, self.dm.xml_host_info)
        def do_test(xml_info):
            host_ip = xmltodict.parse(xml_info)['host']['address']
            r = host_api.createHost(xml_info)
            # 验证接口返回状态码是否正确
            if r['status_code'] == self.dm.expected_status_code:
                # 验证接口返回提示信息是否正确
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT when create host with invalid IP address '%s'." % host_ip)
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned messages are INCORRECT when create host with the invalid IP address '%s'." % host_ip)
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
                self.flag = False
            self.assertTrue(self.flag)
            
        do_test()
            
    def tearDown(self):
        '''
        @summary: 资源清理（主机创建失败，不需要进行资源清理。）
        '''
        pass

class ITC03010306_CreateHost_IncorrectPassword(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-03创建-06root密码错误
    '''
    def setUp(self):
        '''
        @summary: 初始化测试环境
        '''
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateHost_IncorrectIp(self):
        '''
        @summary: 测试步骤
        @note: （1）输入不正确的IP，创建主机；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        host_api = HostAPIs()
        LogPrint().info("Test: Create host with wrong root password.")
        r = host_api.createHost(self.dm.xml_host_info)
        # 判断接口返回状态码是否正确
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            # 判断接口返回提示信息是否正确
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when create host with incorrect password.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT when create host with incorrect password.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理（本用例主机创建失败，不需要进行清理）
        '''
        pass
    
class ITC03010307_CreateHost_NoRequiredParams(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-03创建-07缺少必填参数
    '''
    def setUp(self):
        '''
        @summary: 初始化测试环境
        '''
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateHost_NoRequiredParams(self):
        '''
        @summary: 测试步骤
        @note: （1）缺少主机名称
        @note: （2）缺少主机地址
        @note: （3）缺少root密码
        @note: （4）缺少Cluster的情况下，缺省加入到Default集群中（此项测试不进行）
        @note: （5）创建主机失败，验证接口返回的状态码、提示信息是否正确
        '''
        host_api = HostAPIs()
        
        # 本用例有多种测试情况，所以期望结果也有多种，该变量代表期望结果的索引值
        self.expected_result_index = 0
        
        # 使用数据驱动，根据测试数据文件循环创建多个缺少必要参数的主机
        @BaseTestCase.drive_data(self, self.dm.xml_host_info)
        def do_test(xml_info):
            r = host_api.createHost(xml_info)
            if r['status_code']==self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.expected_result_index]), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT when create host without required params.")
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned messages are INCORRECT when create host without required params.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
                self.flag = False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
            
        do_test()
        
    def tearDown(self):
        pass
    
class ITC0301040101_EditHost_Up_VerifyEditableOptions(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-04编辑-01Active状态-01验证可编辑项
    '''
    def setUp(self):
        '''
        @summary: 准备测试环境
        @note: （1）创建一个主机，等待其变为Up状态
        '''
        # 获取测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 创建一个主机，并等待其状态为Up。
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % self.dm.init_name)
        self.assertTrue(smart_create_host(self.dm.init_name, self.dm.xml_host_info))
        
    def test_EditHost_Up_VerifyEditableOptions(self):
        '''
        @summary: 测试步骤
        @note: （1）在UP状态下修改可编辑的项：主机名称、描述；
        @note: （2）验证接口返回状态码、编辑后的信息是否正确。
        '''
        host_api = HostAPIs()
        LogPrint().info("Test: Edit the editable options while host is 'UP' state.")
        r = host_api.updateHost(self.dm.init_name, self.dm.xml_update_info)
        # 判断接口返回状态码是否正确
        if r['status_code'] == self.dm.expected_status_code_edit_host:
            dictCompare = DictCompare()
            # 判断接口返回的编辑后主机信息与修改的信息是否一致
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.xml_update_info), r['result']):
                LogPrint().info("PASS: Edit host's name and desc SUCCESS in UP state.")
                self.flag = True
            else:
                LogPrint().info("FAIL: The updated host's name and desc are different to expected.")
                self.flag = False
        else:
            LogPrint().info("FAIL: The returned status code '%s' by update option is INCORRECT, it should be '%s'." % (r['status_code'], self.dm.expected_status_code_edit_host))
            self.flag = False
        self.assertTrue(self.flag)

    def tearDown(self):
        '''
        @summary: 资源清理
        @note: 删除创建的主机
        '''
        for host_name in [self.dm.new_name, self.dm.init_name]:
            LogPrint().info("Post-Test: Delete host '%s'." % host_name)
            self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))
                    
class ITC0301040102_EditHost_Up_VerifyUneditableOptions(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-04编辑-01Up状态-02验证不可编辑项
    '''
    def setUp(self):
        '''
        @summary: 准备测试环境
        @note: （1）创建一个主机，等待其变为Up状态；
        '''
        # 获取测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 创建一个主机，并等待其状态为Up。
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % self.dm.host_name)
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
    def test_EditHost_Up_VerifyUneditableOptions(self):
        '''
        @summary: 测试步骤
        @note: （1）在UP状态下修改不可编辑的项：IP、密码、Cluster等；
        @note: （2）验证操作失败后，接口返回状态码、编辑后的信息是否正确。
        '''
        host_api = HostAPIs()
        LogPrint().info("Test: Verify the Un-Editable options while host in 'UP' state.")
        r = host_api.updateHost(self.dm.host_name, self.dm.xml_host_update_info)
        # 判断接口返回状态码是否正确
        if r['status_code'] == self.dm.expected_status_code_edit_host:
            dictCompare = DictCompare()
            # 判断接口返回的编辑后主机信息与修改的信息是否一致
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_edit_host), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when modified the uneditable option the host in UP state.")
                self.flag = True
            else:
                LogPrint().info("FAIL: Returned messages are INCORRECT when modify the host's parameters with UP state.")
                self.flag = False
        else:
            LogPrint().info("FAIL: Returned status code '%s' by update option is INCORRECT, it should be '%s'." % (r['status_code'], self.dm.expected_status_code_edit_host))
            self.flag = False
        self.assertTrue(self.flag)

    def tearDown(self):
        '''
        @summary: 资源清理
        @note: 删除创建的主机
        '''
        LogPrint().info("Post-Test: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name, self.dm.xml_host_del_option))

class ITC0301040201_EditHost_Maintenance_VerifyEditableOptions(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-04编辑-02Maintenance状态-01验证可编辑项
    '''
    def setUp(self):
        '''
        @summary: 准备测试环境
        @note: （1）创建一个主机，等待其变为Up状态；
        @note: （2）在同一数据中心里创建一个新的Cluster；
        '''
        # 获取测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个主机，将其加入指定集群（ITC03_SetUp.py中指定的集群），并等待其状态为Up。
        self.host_api = HostAPIs()
        LogPrint().info("Pre-Test-1: Create host '%s' and add it in to cluster '%s'." % (self.dm.init_host_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_host(self.dm.init_host_name, self.dm.xml_host_info))
        
        # 前提2：在同一数据中心里创建一个新的集群（用于修改Host的所属Cluster时使用）
        self.cluster_api = ClusterAPIs()
        LogPrint().info('Pre-Test-2: Create a new cluster "%s" in DataCenter "%s".' % (self.dm.cluster1_name, ModuleData.dc_name))
        r = self.cluster_api.createCluster(self.dm.xml_cluster1_info)
        if r['status_code'] == self.dm.expected_status_code_create_cluster:
            LogPrint().info("Pre-Test-2-PASS: Create a new Cluster '%s' SUCCESS." % self.dm.cluster1_name)
            self.flag = True
        else:
            LogPrint().error("Pre-Test-2-FAIL: Create new Cluster '%s' FAILED." %self.dm.cluster1_name)
            self.flag = False
        self.assertTrue(self.flag)
        
        # 前提3：将主机设置为Maintenance状态
        LogPrint().info("Pre-Test-3: Deactivate host '%s'." % self.dm.init_host_name)
        r = self.host_api.deactiveHost(self.dm.init_host_name)
        def is_host_maintenance():
                return self.host_api.getHostStatus(self.dm.init_host_name)=='maintenance'
        if wait_until(is_host_maintenance, 120, 5):
            LogPrint().info("Pre-Test-3-PASS: Deactive host '%s'SUCCESS." % self.dm.init_host_name)
            self.flag = True
        else:
            LogPrint().info("Pre-Test-3-FAIL: Deactive host '%s'FAILED." % self.dm.init_host_name)
            self.flag = False
        self.assertTrue(self.flag)
        
    def test_EditHost_Maintenance_VerifyEditableOptions(self):
        '''
        @summary: 测试步骤
        @note: （1）在Maintenance状态下修改可编辑的项：主机名称、注释、所属集群；
        @note: （2）验证接口返回状态码、编辑后的信息是否正确。
        '''
        LogPrint().info("Test: Update host in 'Maintenance' state.")
        r = self.host_api.updateHost(self.dm.init_host_name, self.dm.xml_host_update_info)
        # 判断接口返回状态码是否正确
        if r['status_code'] == self.dm.expected_status_code_edit_host:
            dictCompare = DictCompare()
            # 在r['result']['cluster']下加入['name']，以方便与数据文件中的期望结果进行对比。
            r['result']['host']['cluster']['name'] = self.cluster_api.getClusterNameById(r['result']['host']['cluster']['@id'])
            # 判断接口返回的编辑后主机信息与修改的信息是否一致
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.xml_host_update_info), r['result']):
                LogPrint().info("PASS: Edit host's name/comment/cluster SUCCESS in Maintenance state.")
                self.flag = True
            else:
                LogPrint().info("FAIL: The updated host's name/comment/cluster are different to expected.")
                self.flag = False
        else:
            LogPrint().info("FAIL: The returned status code '%s' by update operation is INCORRECT, it should be '%s'." % (r['status_code'], self.dm.expected_status_code_edit_host))
            self.flag = False
        self.assertTrue(self.flag)

    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的主机；
        @note: （2）删除创建的集群。 
        '''
        # 删除主机
        for host_name in [self.dm.new_name, self.dm.init_host_name]:
            LogPrint().info("Post-Test-1: Delete host '%s'." % host_name)
            self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))
        
        # 删除本用例中新建的Cluster
        if self.cluster_api.searchClusterByName(self.dm.cluster1_name)['result']['clusters']:
            LogPrint().info("Post-Test-2: Delete the created Cluster '%s' in this TestCase." % self.dm.cluster1_name)
            r = self.cluster_api.delCluster(self.dm.cluster1_name, self.dm.xml_cluster_del_option)
            self.assertTrue(r['status_code']==self.dm.expected_status_code_del_cluster)

class ITC0301040202_EditHost_Maintenance_VerifyUneditableOptions(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-04编辑-02Maintenance状态-02验证不可编辑项
    '''
    def setUp(self):
        '''
        @summary: 准备测试环境
        @note: （1）创建一个主机，等待其变为Up状态；
        '''
        # 获取测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个主机，并等待其状态为Up。
        self.host_api = HostAPIs()
        LogPrint().info('Pre-Test-1: Create Host "%s" in Cluster "%s".' % (self.dm.host_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
        # 前提2：将主机设置为Maintenance状态
        LogPrint().info("Pre-Test-2: Deactivate host '%s'." % self.dm.host_name)
        self.host_api.deactiveHost(self.dm.host_name)
        def is_host_maintenance():
                return self.host_api.getHostStatus(self.dm.host_name)=='maintenance'
        if wait_until(is_host_maintenance, 120, 5):
            LogPrint().info("Pre-Test2-PASS: Deactive host '%s'SUCCESS." % self.dm.host_name)
            self.flag = True
        else:
            LogPrint().info("Pre-Test2-FAIL: Deactive host '%s'FAILED." % self.dm.host_name)
            self.flag = False
        self.assertTrue(self.flag)
        
    def test_EditHost_Maintenance_VerifyUneditableOptions(self):
        '''
        @summary: 测试步骤
        @note: （1）在Maintenance状态下修改不可编辑的项：IP、密码等；
        @note: （2）验证操作失败后，接口返回状态码、编辑后的信息是否正确。
        '''
        LogPrint().info("Test: Edit the Un-Editable options while host in 'Maintenance' state.")
        r = self.host_api.updateHost(self.dm.host_name, self.dm.xml_host_update_info)
        # 判断接口返回状态码是否正确
        if r['status_code'] == self.dm.expected_status_code_edit_host_fail:
            dictCompare = DictCompare()
            # 判断接口返回的编辑后主机信息与修改的信息是否一致
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_edit_host), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when modified the uneditable option the host in MAINTENANCE state.")
                self.flag = True
            else:
                LogPrint().info("FAIL: Returned messages are INCORRECT when modify the host's parameters with MAINTENANCE state.")
                self.flag = False
        else:
            LogPrint().info("FAIL: Returned status code '%s' by update option is INCORRECT, it should be '%s'." % (r['status_code'], self.dm.expected_status_code_edit_host_fail))
            self.flag = False
        self.assertTrue(self.flag)

    def tearDown(self):
        '''
        @summary: 资源清理
        @note: 删除创建的主机
        '''
        LogPrint().info("Post-Test: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name, self.dm.xml_host_del_option))
                
class ITC03010403_EditHost_DupName(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-04编辑-03重名
    '''
    def setUp(self):
        '''
        @summary: 前提条件
        @note: 创建两个主机，等待其变为UP状态。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建两个主机host1和host2，并等待其变为UP状态
        self.host_api = HostAPIs()
        self.hosts_info = {self.dm.host1_name:self.dm.xml_host1_info, self.dm.host2_name:self.dm.xml_host2_info}
        LogPrint().info("Pre-Test: Create 2 hosts '%s' and '%s' for this test." % (self.dm.host1_name, self.dm.host2_name))
        for host_name in self.hosts_info:
            self.assertTrue(smart_create_host(host_name, self.hosts_info[host_name]))
        
    def test_EditHost_DupName(self):
        '''
        @summary: 测试步骤
        @note: （1）编辑其中一个主机，将名称更改为另一主机的名称（重名）；
        @note: （2）编辑失败，验证接口返回状态码、提示信息是否正确。
        '''
        LogPrint().info("Test: Edit the host's with a duplicate name.")
        r = self.host_api.updateHost(self.dm.host2_name, self.dm.xml_host2_update_info)
        if r['status_code'] == self.dm.expected_status_code_edit_host_fail:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_edit_host_dup_name), r['result']):
                LogPrint().info("PASS: Returned status code and messages are COORECT when edit host with Dup Name.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned status code and messages are INCOORECT when edit host with Dup Name.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCOORECT when edit host with Dup Name." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理，删除setUp中创建的两个host
        @note: （1）将host设置为maintenance模式；
        @note: （2）删除host。
        '''        
        hosts_list = [self.dm.host1_name, self.dm.host2_name]
        for host in hosts_list:
            LogPrint().info("Post-Test: Delete host '%s'." % host)
            self.assertTrue(smart_del_host(host, self.dm.xml_host_del_option))
                    
class ITC03010501_DelHost_Normal(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-05删除-01普通删除
    @note: 将主机设置为Maintenanece状态后，通过接口发送delete请求，不附带任何删除选项。
    '''
    def setUp(self):
        '''
        @summary: 准备测试环境，初始化测试数据，创建一个Host。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个主机
        LogPrint().info("Pre-Test: Create 1 host '%s' for this TC." % self.dm.host_name)
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
    def test_DelHost_Normal(self):
        '''
        @summary:  测试步骤
        @note: （1）将主机设置为Maintenance状态；
        @note: （2）删除主机（普通删除：delete请求不带任何选项参数）
        @note: （3）删除成功，验证接口返回状态码、实际结果是否正确。
        '''
        host_api = HostAPIs()
        def is_host_maintenance():
            return host_api.getHostStatus(self.dm.host_name)=='maintenance'
        LogPrint().info("Test-1: Deactivate host '%s' to maintenance state." % self.dm.host_name)
        host_api.deactiveHost(self.dm.host_name)
        if wait_until(is_host_maintenance, 120, 5):
            LogPrint().info("Test-2: Delete the host '%s' from cluster." % self.dm.host_name)
            r = host_api.delHost(self.dm.host_name)
            if r['status_code'] == self.dm.expected_status_code_del_host_normal and host_api.searchHostByName(self.dm.host_name):
                LogPrint().info("PASS: Delete host '%s' SUCCESS." % self.dm.host_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Delete host '%s' FAILED. Maybe the returned status code is not '%s', or the host was not deleted." % (self.dm.host_name, self.dm.expected_status_code_del_host_normal))
                self.flag = False
        else:
            LogPrint().error("Test-1-FAIL: Set host '%s' to 'Maintenance' FAILED." % self.host_name)
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        LogPrint().info("Post-Test: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name, self.dm.xml_host_del_option))

class ITC03010502_DelHost_Force(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-05删除-02强制删除
    @note: 将主机设置为Maintenance状态后，通过接口发送delete请求，带force参数。
    '''
    def setUp(self):
        '''
        @summary: 准备测试环境，初始化测试数据，创建一个Host。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 创建一个主机
        LogPrint().info("Pre-Test: Create 1 host '%s' for this TC." % self.dm.host_name)
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
    def test_DelHost_Force(self):
        '''
        @summary:  测试步骤
        @note: （1）将主机设置为Maintenance状态；
        @note: （2）删除主机（普通删除：delete请求带force参数）
        @note: （3）删除成功，验证接口返回状态码、实际结果是否正确。
        '''
        host_api = HostAPIs()
        def is_host_maintenance():
            return host_api.getHostStatus(self.dm.host_name)=='maintenance'
        LogPrint().info("Test-1: Deactivate host '%s' to maintenance state." % self.dm.host_name)
        host_api.deactiveHost(self.dm.host_name)
        if wait_until(is_host_maintenance, 120, 5):
            LogPrint().info("Test-2: Delete host '%s' from cluster." % self.dm.host_name)
            r = host_api.delHost(self.dm.host_name, self.dm.xml_del_host_option)
            if r['status_code'] == self.dm.expected_status_code_del_host_force and host_api.searchHostByName(self.dm.host_name):
                LogPrint().info("PASS: Delete host '%s' SUCCESS." % self.dm.host_name)
            else:
                LogPrint().error("FAIL: Delete host '%s' FAILED. Maybe the returned status code is not '%s', or the host was not deleted." % (self.dm.host_name, self.dm.expected_status_code_del_host_normal))
                self.flag = False
        else:
            LogPrint().error("Test-1-FAIL: Set host '%s' to 'Maintenance' FAILED." % self.host_name)
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        LogPrint().info("Post-Test: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name, self.dm.xml_host_del_option))    

class ITC03010503_DelHost_Up(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-05删除-03无法删除UP状态主机
    '''
    def setUp(self):
        '''
        @summary: 准备测试环境，初始化测试数据，创建一个Host。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 创建一个主机
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % self.dm.host_name)
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
    def test_DelHost_Up(self):
        '''
        @summary:  测试步骤
        @note: （1）对UP状态主机进行删除操作
        @note: （2）操作失败，验证接口返回状态码、实际结果是否正确。
        '''
        host_api = HostAPIs()
        LogPrint().info("Test: Delete host '%s' with UP state." % self.dm.host_name)
        r = host_api.delHost(self.dm.host_name)
        if r['status_code'] == self.dm.expected_status_code_del_host_up:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_del_host_up), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT while delete host '%s' with UP state." % self.dm.host_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT while delete host '%s' with UP state." % self.dm.host_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code_del_host_up))
            self.flag = False

        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理－－删除主机
        '''
        LogPrint().info("Post-Test: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name, self.dm.xml_host_del_option))

class ITC03010601_ActivateHost_Maintenance(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-06激活-01激活维护状态主机
    '''
    def setUp(self):
        '''
        @summary: 获取测试数据，创造测试前提条件。
        @note: （1）新建一个主机，并等待其变为UP状态；
        @note: （2）将该主机设置为Maintenance状态。
        '''
        # 自动获取测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个主机，将其加入指定集群（ITC03_SetUp.py中指定的集群），并等待其状态为Up。
        self.host_api = HostAPIs()
        LogPrint().info('Pre-Test-1: Create Host "%s" in Cluster "%s".' % (self.dm.host_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
        # 前提2：将主机设置为Maintenance状态
        self.host_api.deactiveHost(self.dm.host_name)
        def is_host_maintenance():
            return self.host_api.getHostStatus(self.dm.host_name)=='maintenance'
        LogPrint().info("Pre-Test-2: Deactivate host '%s'." % self.dm.host_name)
        if wait_until(is_host_maintenance, 120, 5):
            LogPrint().info("Pre-Test2-PASS: Deactivate host '%s'SUCCESS." % self.dm.host_name)
            self.flag = True
        else:
            LogPrint().error("Pre-Test2-FAIL: Deactivate host '%s'FAILED." % self.dm.host_name)
            self.flag = False
        self.assertTrue(self.flag)
        
    def test_ActiveHost_Maintenance(self):
        '''
        @summary: 测试步骤
        @note: （1）激活一个Maintenance状态的主机
        @note: （2）操作成功，验证返回的状态码是否正确，主机最终是否变为UP状态。
        '''
        def is_host_up():
            return self.host_api.getHostStatus(self.dm.host_name) == 'up'
        LogPrint().info("Test: Activate a host with 'Maintenance' state.")
        r = self.host_api.activeHost(self.dm.host_name)
        if r['status_code']==self.dm.expected_status_code_active_host:
            if wait_until(is_host_up, 200, 5):
                LogPrint().info("PASS: Activate host '%s' SUCCESS." % self.dm.host_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Activate host'%s' FAILED, it's state is '%s'." % (self.dm.host_name, self.host_api.gethoststatus(self.dm.host_name)))
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status_code '%s' is INCORRECT, it should be '%s'." % (r['status_code'], self.dm.expected_status_code_active_host))
            self.flag = False
            
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源回收，删除主机。
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC03010602_ActivateHost_Up(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-06激活-02激活UP状态主机
    '''
    def setUp(self):
        '''
        @summary: 创建前提条件
        @note: （1）新建一个host，使其处于UP状态。
        '''
        # 获取测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个主机，将其加入指定集群（ITC03_SetUp.py中指定的集群），并等待其状态为Up。
        LogPrint().info('Pre-Test: Create Host "%s" in Cluster "%s".' % (self.dm.host_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
    def test_ActivateHost_Up(self):
        '''
        @summary: 测试步骤
        @note: （1）激活一个已经处于UP状态的主机；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        host_api = HostAPIs()
        dictCompare = DictCompare()
        LogPrint().info("Test: Activate host '%s' in 'UP' state." % self.dm.host_name)
        r = host_api.activeHost(self.dm.host_name)
        if r['status_code']==self.dm.expected_status_code_active_host_fail and dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_active_host_fail), r['result']):
            LogPrint().info("PASS: Returned status_code and messages are CORRECT while activate a host with UP state.")
            self.flag = True
        elif r['status_code']==self.dm.expected_status_code_active_host_fail:
            LogPrint().error("FAIL: Returned messages are INCORRECT: '%s'." % xmltodict.unparse(r['result'], pretty=True))
            self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源回收，删除主机。
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))
        
class ITC03010701_DeactivateHost_Up(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-07取消激活-01取消激活UP状态主机
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据及测试环境
        @note: （1）创建一个主机，并等待其处于UP状态（该主机上没有运行任何虚拟机）。
        '''
        # 获取测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个主机，将其加入指定集群（ITC03_SetUp.py中指定的集群），并等待其状态为Up。
        LogPrint().info('Pre-Test: Create Host "%s" in Cluster "%s".' % (self.dm.host_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
    def test_DeactivateHost_Up(self):
        '''
        @summary: 测试步骤
        @note: （1）对一个UP状态主机进行“维护”操作（主机未运行任何虚拟机）；
        @note: （2）操作成功，验证接口返回状态码，以及虚拟机最终状态是否正确。
        '''
        host_api = HostAPIs()
        host_name = self.dm.host_name
        def is_host_maintenance():
            return host_api.getHostStatus(host_name)=='maintenance'
        LogPrint().info("Test: Deactivate host '%s' with 'Maintenance' state." % host_name)
        r = host_api.deactiveHost(host_name)
        if r['status_code']==self.dm.expected_status_code_deactive_host and wait_until(is_host_maintenance, 150, 5):
            LogPrint().info("PASS: Deactivate host '%s' into Maintenance state SUCCESS." % host_name)
            self.flag = True
        elif r['status_code'] != self.dm.expected_status_code_deactive_host:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT." % r['status_code'])
            self.flag = False
        else:
            LogPrint().error("FAIL: Host state '%s' is INCORRECT." % self.host_api.getHostStatus(host_name))
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理－－删除主机
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC03010702_DeactivateHost_Maintenance(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-07取消激活-02取消激活非UP状态主机
    @note: 此处仅针对处于“维护”状态的主机进行Deactivate操作测试。
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据和测试环境
        @note: （1）新建主机，等待其UP状态；
        @note: （2）将主机设置为Maintenance状态。
        '''
        # 自动获取测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个主机，将其加入指定集群（ITC03_SetUp.py中指定的集群），并等待其状态为Up。
        self.host_api = HostAPIs()
        LogPrint().info('Pre-Test-1: Create Host "%s" in Cluster "%s".' % (self.dm.host_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
        # 前提2：将主机设置为Maintenance状态
        self.host_api.deactiveHost(self.dm.host_name)
        def is_host_maintenance():
            return self.host_api.getHostStatus(self.dm.host_name)=='maintenance'
        LogPrint().info("Pre-Test-2: Deactivate host '%s'." % self.dm.host_name)
        if wait_until(is_host_maintenance, 120, 5):
            LogPrint().info("Pre-Test2-PASS: Deactivate host '%s'SUCCESS." % self.dm.host_name)
            self.flag = True
        else:
            LogPrint().error("Pre-Test2-FAIL: Deactivate host '%s'FAILED." % self.dm.host_name)
            self.flag = False
        self.assertTrue(self.flag)
        
    def test_DeactivateHost_Maintenance(self):
        '''
        @summary: 测试步骤
        @note: （1）对Maintenance状态主机进行Deactive操作；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        host_name = self.dm.host_name
        dictCompare = DictCompare()
        LogPrint().info("Test: Deactivate host with non-up state.")
        r = self.host_api.deactiveHost(host_name)
        if r['status_code']==self.dm.expected_status_code_deactive_host_fail:
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_deactive_host_fail), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT after Deactivate a maintenance host.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT: '%s'." % xmltodict.unparse(r['result'], pretty=True))
                self.flag = False
        else: 
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
       
    def tearDown(self):
        '''
        @summary: 资源清理－－删除主机
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC03010801_InstallHost_Maintenance(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-08安装-01主机Maintenance状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据和测试环境
        @note: （1）创建一个主机，使其处于UP状态；
        @note: （2）设置主机为Maintenance状态。
        '''
        # 自动获取测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个主机，将其加入指定集群（ITC03_SetUp.py中指定的集群），并等待其状态为Up。
        self.host_api = HostAPIs()
        LogPrint().info('Pre-Test-1: Create Host "%s" in Cluster "%s".' % (self.dm.host_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
        # 前提2：将主机设置为Maintenance状态
        LogPrint().info("Pre-Test-2: Deactivate host '%s'." % self.dm.host_name)
        self.host_api.deactiveHost(self.dm.host_name)
        def is_host_maintenance():
            return self.host_api.getHostStatus(self.dm.host_name)=='maintenance'
        if wait_until(is_host_maintenance, 120, 5):
            LogPrint().info("Pre-Test2-PASS: Deactive host '%s'SUCCESS." % self.dm.host_name)
            self.flag = True
        else:
            LogPrint().error("Pre-Test2-FAIL: Deactive host '%s'FAILED." % self.dm.host_name)
            self.flag = False
        self.assertTrue(self.flag)
        
    def test_InstallHost(self):
        '''
        @summary: 测试步骤
        @note: （1）调用安装主机的接口；
        @note: （2）操作成功，验证接口返回的状态码、信息是否正确。
        '''
        host_name = self.dm.host_name
        def is_host_up():
            return self.host_api.getHostStatus(host_name)=='up'
        def is_host_install():
            return self.host_api.getHostStatus(host_name)=='installing'
        LogPrint().info("Test: Install host '%s' while in 'Maintenance' state." % host_name)
        r = self.host_api.installHost(host_name, self.dm.xml_install_option)
        if r['status_code'] == self.dm.expected_status_code_install_host:
            if wait_until(is_host_install, 50, 5) and wait_until(is_host_up, 200, 5):
                LogPrint().info("PASS: Install host '%s' SUCCESS." % host_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: The state of host '%s' is NOT 'installing' or 'up' when installing host.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT after installing host." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除主机
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC03010802_InstallHost_Up(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-08安装-02主机UP状态无法Install
    '''
    def setUp(self):
        '''
        @summary: 测试环境准备
        @note: （1）创建一个主机，使其处于UP状态。
        '''
        # 自动获取测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个主机，将其加入指定集群（ITC03_SetUp.py中指定的集群），并等待其状态为Up。
        LogPrint().info('Pre-Test: Create Host "%s" in Cluster "%s".' % (self.dm.host_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
    def test_InstallHost_Up(self):
        '''
        @summary: 测试步骤
        @note: （1）对一个UP状态主机进行install操作；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        host_api = HostAPIs()
        dictCompare = DictCompare()
        LogPrint().info("Test: Install host '%s' while in 'UP' state." % self.dm.host_name)
        r = host_api.installHost(self.dm.host_name, self.dm.xml_install_option)
        if r['status_code'] == self.dm.expected_status_code_install_host_fail:
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_install_host_fail), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when install host with 'UP' state.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT when installing host with 'UP' state.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT when installing host with 'UP' state." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理－－删除主机
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

# class ITC0301090201_FenceHost_Stop_HostMaintenance(BaseTestCase):
#     '''
#     @summary: ITC-03主机管理-01主机操作-09电源管理-02关闭-01主机Maintenance状态
#     @todo: 未完成
#     '''
#     def setUp(self):
#         '''
#         @summary: 初始化测试数据、测试环境
#         @note: （1）新建两个主机host1和host2，其中host2配置了电源管理；
#         @note: （2）将host2设置为Maintenance状态。
#         '''
#         # 初始化测试数据
#         self.dm = super(self.__class__, self).setUp()
#         
#         # 前提1：创建2个主机（host1、host2），其中host2有电源管理。
#         self.host_api = HostAPIs()
#         dict_hosts = {self.dm.host1_name:self.dm.xml_host1_info, self.dm.host2_name:self.dm.xml_host2_info}
#         for host_name in dict_hosts:
#             self.assertTrue(smart_create_host(host_name, dict_hosts[host_name]))
# #             r = self.host_api.createHost(dict_hosts[host_name])
# #             def is_host_up():
# #                 return self.host_api.getHostStatus(host_name)=='up'
# #             if wait_until(is_host_up, 200, 5):
# #                 if r['status_code'] == self.dm.expected_status_code_create_host:
# #                     LogPrint().info("PASS: Create host '%s' SUCCESS." % host_name)
# #                     self.flag = True
# #                 else:
# #                     LogPrint().error("FAIL: Create host '%s' FAILED. Returned status code is INCORRECT." % host_name)
# #                     self.flag = False
# #             else:
# #                 LogPrint().error("FAIL: Create host '%s' with Power Management FAILED. It's state is not 'UP'." % host_name)
# #                 self.flag = False
# #             self.assertTrue(self.flag)
#         
#         # 前提2：将主机host2设置为Maintenance状态
#         self.host_api.deactiveHost(self.dm.host2_name)
#         def is_host_maintenance():
#                 return self.host_api.getHostStatus(self.dm.host2_name)=='maintenance'
#         LogPrint().info("Pre-Test-Step2: Deactive host '%s'." % self.dm.host2_name)
#         if wait_until(is_host_maintenance, 120, 5):
#             LogPrint().info("Pre-Test2-PASS: Deactive host '%s'SUCCESS." % self.dm.host2_name)
#         else:
#             LogPrint().error("Pre-Test2-FAIL: Deactive host '%s'FAILED." % self.dm.host2_name)
#             self.flag = False
#         self.assertTrue(self.flag)
#         
#     def test_FenceHost_Stop_HostMaintenance(self):
#         '''
#         @summary: 测试步骤
#         @note: （1）对处于Maintenance状态的host2通过电源管理执行stop操作；
#         @note: （2）操作成功，验证接口返回的状态码、信息以及host2的最终状态是否正确。
#         '''
#         r = self.host_api.fenceHost(self.dm.host2_name, self.dm.xml_fence_option)
#         print r['status_code']
#         print xmltodict.unparse(r['result'], pretty=True)
#         
#     def tearDown(self):
#         '''
#         @summary: 资源清理
#         '''

# class ITC0301090202_FenceHost_Stop_HostUp(BaseTestCase):
#     '''
#     @summary: ITC-03主机管理-01主机操作-09电源管理-02关闭-02主机UP状态Stop失败
#     @note: 当主机处于非Maintenance状态时，验证通过电源管理执行stop操作失败。
#     @todo: 未完成
#     '''
#     def setUp(self):
#         '''
#         @summary: 初始化测试数据、测试环境
#         @note: （1）新建两个主机host1和host2，其中host2配置了电源管理。
#         '''
#         # 初始化测试数据
#         self.dm = super(self.__class__, self).setUp()
#         
#         # Pre-Test-Step1：创建2个主机（host1、host2），其中host2有电源管理。
#         self.host_api = HostAPIs()
#         dict_hosts = {self.dm.host1_name:self.dm.xml_host1_info, self.dm.host2_name:self.dm.xml_host2_info}
#         for host_name in dict_hosts:
#             r = self.host_api.createHost(dict_hosts[host_name])
#             def is_host_up():
#                 return self.host_api.getHostStatus(host_name)=='up'
#             if wait_until(is_host_up, 200, 5):
#                 if r['status_code'] == self.dm.expected_status_code_create_host:
#                     LogPrint().info("PASS: Create host '%s' SUCCESS." % host_name)
#                     self.flag = True
#                 else:
#                     LogPrint().error("FAIL: Create host '%s' FAILED. Returned status code is INCORRECT." % host_name)
#                     self.flag = False
#             else:
#                 LogPrint().error("FAIL: Create host '%s' with Power Management FAILED. It's state is not 'UP'." % host_name)
#                 self.flag = False
#             self.assertTrue(self.flag)
#             
#     def test_FenceHost_Stop(self):
#         '''
#         @summary: 测试步骤
#         @note: （1）向主机发送fence-stop请求；
#         @note: （2）操作成功，验证接口返回状态码、提示信息、主机最终状态（down）是否正确。
#         '''
#         dictCompare = DictCompare()
#         r = self.host_api.fenceHost(self.dm.host2_name, self.dm.xml_fence_option)
#         if r['status_code'] == self.dm.expected_status_code_fence_stop_fail:
#             if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_fence_stop_fail), r['result']):
#                 LogPrint().info("PASS: Returned status code and messages are CORRECT when fence-stop a host with UP state.")
#                 self.flag = True
#             else:
#                 LogPrint().error("FAIL: Returned messages are INCORRECT when fence-stop a host with UP state.")
#                 self.flag = False
#         else:
#             LogPrint().error("FAIL: Returned status code '%s' is INCORRECT when fence-stop a host with UP state.")
#             self.flag = False
#         self.assertTrue(self.flag)
#         
#     def tearDown(self):
#         '''
#         @summary: 资源清理，分别删除两个创建的主机。
#         '''
#         def is_host_maintenance():
#             return self.host_api.getHostStatus(host)=='maintenance'
#         hosts_list = [self.dm.host2_name, self.dm.host1_name]
#         for host in hosts_list:
#             if self.host_api.searchHostByName(host)['result']['hosts'] and is_host_maintenance():
#                 LogPrint().info("Post-Test: Delete host '%s'." % host)
#                 r = self.host_api.delHost(host, self.dm.xml_host_del_option)
#                 if r['status_code'] == self.dm.expected_status_code_del_host:
#                     LogPrint().info("Post-Test_PASS: Delete host '%s' SUCCESS." % host)
#                     self.flag = True
#                 else:
#                     LogPrint().error("Post-Test_PASS: Delete host '%s' FAILED." % host)
#                     self.flag = False
#             elif self.host_api.searchHostByName(host)['result']['hosts'] and not is_host_maintenance():
#                 LogPrint().info("Post-Test: Deactive the host '%s' to maintenance state." % host)
#                 self.host_api.deactiveHost(host)
#                 if wait_until(is_host_maintenance, 150, 5):
#                     LogPrint().info("Post-Test: Delete the host '%s'." % host)
#                     self.host_api.delHost(host, self.dm.xml_host_del_option)

class ITC0301090401_FenceHost_Status_CorrectIpmi(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-09电源管理-04状态-01IPMI配置正确
    @note: 获取主机的电源管理（IPMI）状态。如IPMI的地址、用户名或密码正确时，该接口返回的状态为on。
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据和测试环境
        @note: （1）创建一个无配置电源管理的主机host1
        @note: （2）创建一个配置电源管理的主机host2
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test：创建2个主机（host1、host2），其中host2有电源管理。
        dict_hosts = {self.dm.host1_name:self.dm.xml_host1_info, self.dm.host2_name:self.dm.xml_host2_info}
        for host_name in dict_hosts:
            LogPrint().info("Pre-Test: Create host '%s' for this TC." % host_name)
            self.assertTrue(smart_create_host(host_name, dict_hosts[host_name]))
        
    def test_FenceHost_Status(self):
        '''
        @summary: 测试步骤
        @note: （1）对电源管理host发送status的fence请求；
        @note: （2）操作成功，验证接口的返回码、返回信息是否正确。
        '''
        host_api = HostAPIs()
        dictCompare = DictCompare()
        LogPrint().info("Test: Get host IPMI state.")
        r = host_api.fenceHost(self.dm.host2_name, self.dm.xml_fence_option)
        if r['status_code'] == self.dm.expected_status_code_fence_status:
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_fence_status), r['result']):
                LogPrint().info("PASS: Get fence status for host '%s' SUCCESS." %self.dm.host2_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT after fence status for host '%s'." % self.dm.host2_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT after fence status for host.")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理，分别删除两个创建的主机。
        '''
        hosts_list = [self.dm.host2_name, self.dm.host1_name]
        for host in hosts_list:
            LogPrint().info("Post-Test: Delete host '%s'." % host)
            self.assertTrue(smart_del_host(host, self.dm.xml_host_del_option))

class ITC0301090402_FenceHost_Status_IncorrectIpmi(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-09电源管理-04状态-02IPMI配置不正确
    @note: 获取主机的电源管理（IPMI）状态。如IPMI的地址、用户名或密码不正确时，该接口返回的状态为failed。
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据和测试环境
        @note: （1）创建一个无配置电源管理的主机host1
        @note: （2）创建一个配置电源管理的主机host2
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test1：创建2个主机（host1、host2），其中host2有电源管理。
        dict_hosts = {self.dm.host1_name:self.dm.xml_host1_info, self.dm.host2_name:self.dm.xml_host2_info}
        for host_name in dict_hosts:
            LogPrint().info("Pre-Test: Create host '%s' for this TC." % host_name)
            self.assertTrue(smart_create_host(host_name, dict_hosts[host_name]))
        
    def test_FenceHost_Status_IncorrectIpmi(self):
        '''
        @summary: 测试步骤
        @note: （1）对电源管理host发送status的fence请求；
        @note: （2）操作成功，验证接口的返回码、返回信息是否正确。
        '''
        host_api = HostAPIs()
        dictCompare = DictCompare()
        LogPrint().info("Test: Get host IMPI state with WRONG IPMI address/user/password.")
        r = host_api.fenceHost(self.dm.host2_name, self.dm.xml_fence_option)
        if r['status_code'] == self.dm.expected_status_code_fence_status:
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_fence_status), r['result']):
                LogPrint().info("PASS: Get fence status and messages for host '%s' SUCCESS." %self.dm.host2_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT after fence status for host '%s'." % self.dm.host2_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT after fence status for host.")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理，分别删除两个创建的主机。
        '''
        hosts_list = [self.dm.host2_name, self.dm.host1_name]
        for host_name in hosts_list:
            LogPrint().info("Post-Test: Delete host '%s'." % host_name)
            self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC03011001_DiscoveryIscsi_Normal(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-10ISCSI存储发现-01基本功能
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境
        @note: （1）新建一个主机host1，处于UP状态。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test：创建主机host1
        host_name = self.dm.host_name
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % host_name)
        self.assertTrue(smart_create_host(host_name, self.dm.xml_host_info))
        
    def test_DiscoveryIscsi_Normal(self):
        '''
        @summary: 测试步骤
        @note: （1）调用host的存储管理子接口，发现一个iscsi存储域；
        @note: （2）操作成功，验证接口返回的状态码及信息是否正确。
        '''
        host_api = HostAPIs()
        LogPrint().info("Test: Discovery ISCSI targets.")
        r = host_api.iscsiDiscoverByHost(self.dm.host_name, self.dm.xml_iscsi_info)
        if r['status_code'] == self.dm.expected_status_code_discovery_iscsi:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.xml_iscsi_info), r['result']):
                LogPrint().info("PASS: Discovery iscsi targets SUCCESS.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Discovery iscsi targets FAILED. Returned iscsi info are INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Discovery iscsi targets FAILED. Returned status code '%s' INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)    
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC03011002_DiscoveryIscsi_IncorrectIp(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-10ISCSI存储发现-02IP或Port不正确
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test-Step1：创建主机host1
        host_name = self.dm.host_name
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % host_name)
        self.assertTrue(smart_create_host(host_name, self.dm.xml_host_info))
        
    def test_DiscoveryIscsi_IncorrectIp(self):
        '''
        @summary: 测试步骤
        @note: （1）执行相应接口探测一个错误IP或Port的iscsi服务器；
        @note: （2）测试失败，验证接口返回的状态码、提示信息是否正确。
        '''
        host_api = HostAPIs()
        LogPrint().info("Test: Test the iscsi-discovery operation with Wrong IP or Port.")
        @BaseTestCase.drive_data(self, self.dm.xml_iscsi_info_list)
        def do_test(xml_iscsi_info):
            r = host_api.iscsiDiscoverByHost(self.dm.host_name, xml_iscsi_info)
            if r['status_code'] == self.dm.expected_status_code_discovery_iscsi_fail:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_discovery_iscsi_fail), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT when discovering iscsi with wrong IP or Port.")
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned messages are INCORRECT when discovering iscsi with wrong IP or Port.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' INCORRECT when discovering iscsi with wrong IP or Port." % r['status_code'])
                self.flag = False
            self.assertTrue(self.flag)  
        do_test()

    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC030111_LoginIscsi_Normal(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-11ISCSI存储挂载
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境
        @note: （1）新建一个主机host1，处于UP状态。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test：创建主机host1
        host_name = self.dm.host_name
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % host_name)
        self.assertTrue(smart_create_host(host_name, self.dm.xml_host_info))
        
    def test_LoginIscsi_Normal(self):
        '''
        @summary: 测试步骤
        @note: （1）调用host的存储管理子接口，发现一个iscsi存储域；
        @note: （2）操作成功，验证接口返回的状态码及信息是否正确。
        '''
        host_api = HostAPIs()
        LogPrint().info("Test: Use host to login a iscsi target.")
        r = host_api.iscsiLogin(self.dm.host_name, self.dm.xml_target_info)
        if r['status_code'] == self.dm.expected_status_code_login_iscsi:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.xml_target_info), r['result']):
                LogPrint().info("PASS: Login iscsi target '%s' SUCCESS." % self.dm.iscsi_target['target'])
                self.flag = True
            else:
                LogPrint().error("FAIL: Login iscsi target FAILED. Returned target info are INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Login iscsi target FAILED. Returned status code '%s' INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)    
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC030112_CommitNetwork(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-12提交保存主机网络配置
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境
        @note: （1）新建一个主机host1，处于UP状态。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test：创建主机host1
        host_name = self.dm.host_name
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % host_name)
        self.assertTrue(smart_create_host(host_name, self.dm.xml_host_info))
        
    def test_DiscoveryIscsi_Normal(self):
        '''
        @summary: 测试步骤
        @note: （1）调用host的存储管理子接口，发现一个iscsi存储域；
        @note: （2）操作成功，验证接口返回的状态码及信息是否正确。
        '''
        host_api = HostAPIs()
        LogPrint().info("Test: Commit host networks.")
        r = host_api.commitNetConfig(self.dm.host_name)
        if r['status_code'] == self.dm.expected_status_code_commit_network:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_commit_network), r['result']):
                LogPrint().info("PASS: Commit host's network SUCCESS.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Commit host's netwirk FAILED. Returned operation state '%s' is INCORRECT." % r['result']['action']['status']['state'])
                self.flag = False
        else:
            LogPrint().error("FAIL: Commit host's network FAILED. Returned status code '%s' INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)    
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC03011301_SelectSpm_Up(BaseTestCase):
    '''
    @summary: ITC-03主机管理-01主机操作-13选择SPM-01选择UP主机
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据，测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        self.dc_api = DataCenterAPIs()
        self.cluster_api = ClusterAPIs()
        # 前提1：创建数据中心和集群
        LogPrint().info("Pre-Test-1: Create DataCenter '%s' and Cluster '%s'." % (self.dm.dc1_name, self.dm.cluster1_name))
        self.dc_api.createDataCenter(self.dm.xml_dc1_info)
        self.cluster_api.createCluster(self.dm.xml_cluster1_info)
        # 前提2：创建第1个主机（host1）
        LogPrint().info("Pre-Test-2: Create the 1st host '%s'." % self.dm.host1_name)
        self.host_api = HostAPIs()
        self.assertTrue(smart_create_host(self.dm.host1_name, self.dm.xml_host1_info))
        # 前提3：创建并附加Data存储域data1-nfs
        LogPrint().info("Pre-Test-3: Create and Attach data storage '%s' to DataCenter '%s'." % (self.dm.data1_nfs_name, self.dm.dc1_name))
        self.assertTrue(smart_create_storage_domain(self.dm.data1_nfs_name, self.dm.xml_data1_info))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc1_name, self.dm.data1_nfs_name))
        # 前提4：创建第2个主机（加入到同一数据中心）
        LogPrint().info("Pre-Test-4: Create 2nd host '%s' in the same DataCenter." % self.dm.host2_name)
        self.assertTrue(smart_create_host(self.dm.host2_name, self.dm.xml_host2_info))
            
    def test_SelectSpm_Up(self):
        '''
        @summary: 测试步骤
        @note: （1）将非spm主机（host2）设置为spm；
        @note: （2）操作成功，验证接口返回的状态码、信息是否正确。
        '''
        LogPrint().info("Test: Force select host '%s' as SPM." % self.dm.host2_name)
        r = self.host_api.forceSelectSPM(self.dm.host2_name)
        if r['status_code'] == self.dm.expected_status_code_select_spm:
            if self.host_api.getSPMInfo(self.dm.host2_name)['is_spm']:
                LogPrint().info("PASS: Force select host '%s' as SPM SUCCESS." % self.dm.host2_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Force select host '%s' as SPM FAILED." % self.dm.host2_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
            
        
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）将host1重新设置为SPM；
        @note: （2）将host2设置为维护状态，并删除；
        @note: （3）将data1设置为维护状态；
        @note: （4）删除数据中心（非强制，之后data存储域变为Unattached状态）
        @note: （5）删除unattached状态的data1存储域；
        @note: （6）删除主机host1;
        @note: （7）删除集群。
        '''
        LogPrint().info("Post-Test-1: Re-select host1 '%s' as SPM." % self.dm.host1_name)
        self.assertTrue(self.host_api.forceSelectSPM(self.dm.host1_name)['status_code']==self.dm.expected_status_code_select_spm)
        LogPrint().info("Post-Test-2: Delete host2 '%s'." % self.dm.host2_name)
        self.assertTrue(smart_del_host(self.dm.host2_name, self.dm.xml_host_del_option))
        LogPrint().info("Post-Test-3: Deactivate storage domain '%s'." % self.dm.data1_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc1_name, self.dm.data1_nfs_name))
        LogPrint().info("Post-Test-4: Delete DataCenter '%s'." % self.dm.dc1_name)
        if self.dc_api.searchDataCenterByName(self.dm.dc1_name)['result']['data_centers']:
            self.assertTrue(self.dc_api.delDataCenter(self.dm.dc1_name)['status_code']==self.dm.expected_status_code_del_dc)
        LogPrint().info("Post-Test-5: Delete storage domain '%s'." % self.dm.data1_nfs_name)
        self.assertTrue(smart_del_storage_domain(self.dm.data1_nfs_name, self.dm.xml_del_sd_option))
        LogPrint().info("Post-Test-6: Delete host '%s'." % self.dm.host1_name)
        self.assertTrue(smart_del_host(self.dm.host1_name, self.dm.xml_host_del_option))
        LogPrint().info("Post-Test-7: Delete cluster '%s'." % self.dm.cluster1_name)
        self.assertTrue(self.cluster_api.delCluster(self.dm.cluster1_name)['status_code'] == self.dm.expected_status_code_del_cluster)

class ITC030201_GetHostNicList(BaseTestCase):
    '''
    @summary: ITC-03主机管理-02主机网络接口操作-01查看主机网络接口列表
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境
        @note: （1）新建一个主机host1，处于UP状态。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test-Step1：创建主机host1
        host_name = self.dm.host_name
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % host_name)
        self.assertTrue(smart_create_host(host_name, self.dm.xml_host_info))
        
    def test_GetHostNicList(self):
        '''
        @summary: 测试步骤
        @note: （1）调用host的网络管理子接口，获取主机网络接口集；
        @note: （2）操作成功，验证接口返回的状态码及信息是否正确。
        '''
        host_nic_api = HostNicAPIs()
        LogPrint().info("Test: Get nics list of host '%s'." % self.dm.host_name)
        r = host_nic_api.getHostNicsList(self.dm.host_name)
        if r['status_code'] == self.dm.expected_status_code_get_host_nic_list:
            LogPrint().info("PASS: Get host nic list SUCCESS.")
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)    
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC030202_GetHostNicInfo(BaseTestCase):
    '''
    @summary: ITC-03主机管理-02主机网络接口操作-02查看主机网络接口信息
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境
        @note: （1）新建一个主机host1，处于UP状态。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test-Step1：创建主机host1
        host_name = self.dm.host_name
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % host_name)
        self.assertTrue(smart_create_host(host_name, self.dm.xml_host_info))
        
    def test_GetHostNicInfo(self):
        '''
        @summary: 测试步骤
        @note: （1）调用host的网络管理子接口，获取主机网络接口信息；
        @note: （2）操作成功，验证接口返回的状态码及信息是否正确。
        '''
        host_nic_api = HostNicAPIs()
        LogPrint().info("Test: Get nic '%s' info of host '%s'." % (self.dm.nic_name, self.dm.host_name))
        r = host_nic_api.getHostNicInfo(self.dm.host_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code_get_host_nic_info:
            LogPrint().info("PASS: Get host nic '%s' info SUCCESS." % self.dm.nic_name)
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)    
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC0304_HostNicStatistics(BaseTestCase):
    '''
    @summary: ITC-03主机管理-04主机网络接口统计
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境
        @note: （1）新建一个主机host1，处于UP状态。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test：创建主机host1
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % self.dm.host_name)
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
    def test_GetHostNicStatistics(self):
        '''
        @summary: 测试步骤
        @note: （1）调用host的网络管理子接口，获取主机网络接口统计信息；
        @note: （2）操作成功，验证接口返回的状态码及信息是否正确。
        '''
        host_nic_api = HostNicAPIs()
        LogPrint().info("Test: Get nic '%s' statistics info of host '%s'." % (self.dm.nic_name, self.dm.host_name))
        r = host_nic_api.getHostNicStatistics(self.dm.host_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code_get_host_nic_statistics:
            LogPrint().info("PASS: Get host nic '%s' statistics SUCCESS." % self.dm.nic_name)
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)    
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))

class ITC0305_HostStatistics(BaseTestCase):
    '''
    @summary: ITC-03主机管理-05主机信息统计
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境
        @note: （1）新建一个主机host1，处于UP状态。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test-Step1：创建主机host1
        LogPrint().info("Pre-Test: Create host '%s' for this TC." % self.dm.host_name)
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
    def test_GetHostStatistics(self):
        '''
        @summary: 测试步骤
        @note: （1）获取主机口统计信息；
        @note: （2）操作成功，验证接口返回的状态码及信息是否正确。
        '''
        host_nic_api = HostNicAPIs()
        LogPrint().info("Test: Get statistics info of host '%s'." % (self.dm.host_name))
        r = host_nic_api.getHostStatistics(self.dm.host_name)
        if r['status_code'] == self.dm.expected_status_code_get_host_statistics:
            LogPrint().info("PASS: Get host '%s' statistics SUCCESS." % self.dm.host_name)
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)    
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # 删除主机
        host_name = self.dm.host_name
        LogPrint().info("Post-Test: Delete host '%s'." % host_name)
        self.assertTrue(smart_del_host(host_name, self.dm.xml_host_del_option))
        
class ITC03_TearDown(BaseTestCase):
    '''
    @summary: “主机管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: （1）删除集群；
    @note: （2）删除数据中心；
    '''
    def test_TearDown(self):
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        if capi.searchClusterByName(ModuleData.cluster_name)['result']['clusters']:
            LogPrint().info("Post-Module-Test: Delete Cluster '%s'." % ModuleData.cluster_name)
            capi.delCluster(ModuleData.cluster_name)
        if dcapi.searchDataCenterByName(ModuleData.dc_name)['result']['data_centers']:
            LogPrint().info("Post-Module-Test: Delete DataCenter '%s'." % ModuleData.dc_name)
            dcapi.delDataCenter(ModuleData.dc_name)

if __name__ == "__main__":
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["Host.ITC03011301_SelectSpm_Up"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)
