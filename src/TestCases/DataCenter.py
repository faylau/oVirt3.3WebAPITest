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
from TestAPIs.DataCenterAPIs import DataCenterAPIs, smart_attach_storage_domain, smart_deactive_storage_domain, smart_detach_storage_domain,\
    smart_active_storage_domain
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.HostAPIs import smart_create_host, smart_del_host
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs, smart_create_storage_domain, smart_del_storage_domain
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from TestData.DataCenter import ITC01_SetUp as ModuleData


class ITC01_SetUp(BaseTestCase):
    '''
    @summary: 数据中心模块级测试用例，初始化模块测试环境；
    @note: （1）创建一个NFS类型数据中心；
    @note: （2）创建一个集群；
    @note: （3）创建一个主机，并等待其变为UP状态；
    @note: （4）创建3个存储域（data1/data2/ISO/Export）；
    @note: （5）将 data1 附加到数据中心。
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()

    def test_CreateModuleTestEnv(self):
        '''
        @summary: 创建DataCenter模块测试环境
        '''
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        
        # 创建1个数据中心（nfs类型）
        LogPrint().info("Pre-Module-Test-1: Create DataCenter '%s'." % self.dm.dc_nfs_name)
        self.assertTrue(dcapi.createDataCenter(self.dm.xml_dc_info)['status_code']==self.dm.expected_status_code_create_dc)
    
        # 创建1个集群
        LogPrint().info("Pre-Module-Test-2: Create Cluster '%s' in DataCenter '%s'." % (self.dm.cluster_nfs_name, self.dm.dc_nfs_name))
        self.assertTrue(capi.createCluster(self.dm.xml_cluster_info)['status_code']==self.dm.expected_status_code_create_cluster)
    
        # 在NFS数据中心中创建一个主机，并等待主机UP。
        LogPrint().info("Pre-Module-Test-3: Create Host '%s' in Cluster '%s'." % (self.dm.host1_name, self.dm.cluster_nfs_name))
        self.assertTrue(smart_create_host(self.dm.host1_name, self.dm.xml_host_info))
    
        # 为NFS数据中心分别创建Data（data1/data2）/ISO/Export域。
        @BaseTestCase.drive_data(self, self.dm.xml_storage_info)
        def create_storage_domains(xml_storage_domain_info):
            sd_name = xmltodict.parse(xml_storage_domain_info)['storage_domain']['name']
            LogPrint().info("Pre-Module-Test-4: Create Data Storage '%s'." % sd_name)
            self.assertTrue(smart_create_storage_domain(sd_name, xml_storage_domain_info))
        create_storage_domains()
        
        # 将创建的的data1附加到NFS/ISCSI数据中心里（data2/Iso/Export处于游离状态）。
        LogPrint().info("Pre-Module-Test-5: Attach the data storages to data centers.")
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))

    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass

class ITC010101_GetDCList(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-01获取数据中心列表
    '''
    def test_GetDataCentersList(self):
        dcapi = DataCenterAPIs()
        r = dcapi.getDataCentersList()
        if r['status_code']==200:
            LogPrint().info('Get DataCenters list SUCCESS.')
        else:
            LogPrint().error('Get DataCenters list FAIL.')
            self.flag = False
        self.assertTrue(self.flag)
        
class ITC010102_GetDCInfo(BaseTestCase):
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

class ITC01010301_CreateDC(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-03创建-01正常创建
    @note: 包括3种类型数据中心（NFS、ISCSI和FC）
    @note: 包括3种兼容版本（3.1、3.2、3.3）
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        
    def test_CreateDC(self):
        '''
        @summary: 测试用例执行步骤
        '''     
        # 使用数据驱动，根据测试数据文件循环创建多个数据中心
        @BaseTestCase.drive_data(self, self.dm.dc_info)
        def do_test(xml_info):
            self.flag = True
            dc_name = xmltodict.parse(xml_info)['data_center']['name']
            r = self.dcapi.createDataCenter(xml_info)
            if r['status_code']==self.dm.status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(xml_info), r['result']):
                    LogPrint().info("Create DataCenter '%s' SUCCESS." % dc_name)
                else:
                    LogPrint().error("Create DataCenter '%s' SUCCESS, but DataCenter info INCORRECT." % dc_name)
                    self.flag = False
            else:
                LogPrint().error("Create DataCenter '%s' FAILED. " % dc_name)
                self.flag = False
            self.assertTrue(self.flag)
            
        do_test()
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        for dc in self.dm.dc_name:
            if self.dcapi.searchDataCenterByName(dc):
                self.dcapi.delDataCenter(dc)
                
class ITC01010302_CreateExistDC(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-03创建-02重复创建
    @note: 创建重名的数据中心（与Default重名）
    @precondition: 存在缺省的数据中心Default
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        
    def test_CreateExistDC(self):
        '''
        @summary: 创建重名数据中心（Default），检查接口返回的状态码以及提示信息是否符合预期。
        '''
        r = self.dcapi.createDataCenter(self.dm.dc_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: The returned status code and messages are CORRECT when create exist DC.")
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECCT when create exist DC.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s', INCORRECT. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理（本次测试没有需要清理的资源）
        '''
        BaseTestCase.tearDown(self)
        
class ITC0101030301_CreateDC_NoRequiredParams(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-03创建-03参数验证-01缺少必填参数
    @note: 创建数据中心，缺少必需要的参数（数据中心有3个必需参数：名称、存储域、兼容版本），验证接口返回状态码及提示信息是否符合预期。
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        
    def test_CreateDCWithoutRequiredParams(self):
        '''
        @summary: 创建数据中心，缺少必需要的参数（数据中心有3个必需参数：名称、存储域、兼容版本），检查接口返回的状态码以及提示信息是否符合预期。
        '''
        # 本用例有3种测试情况，所以期望结果也有3种，这个变量代表期望结果的索引值
        self.expected_result_index = 0
        # 使用数据驱动，根据测试数据文件循环创建多个数据中心
        @BaseTestCase.drive_data(self, self.dm.dc_info)
        def do_test(xml_info):
            self.flag = True
            r = self.dcapi.createDataCenter(xml_info)
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
        '''
        @summary: 资源清理（本次测试没有需要清理的资源）
        '''
        BaseTestCase.tearDown(self)   
        
class ITC0101030302_CreateDC_VerifyName(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-03创建-03参数验证-02名称有效性验证
    @note: 
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        
    def test_CreateDC_VerifyName(self):
        '''
        @summary: 创建数据中心，验证数据中心名称参数有效性
        '''
        # 本用例有多种测试情况，所以期望结果也有多种，这个变量代表期望结果的索引值
        self.expected_result_index = 0
        # 使用数据驱动，根据测试数据文件循环创建多个数据中心
        @BaseTestCase.drive_data(self, self.dm.dc_info)
        def do_test(xml_info):
            self.flag = True
            r = self.dcapi.createDataCenter(xml_info)
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
        '''
        @summary: 资源清理（本次测试没有需要清理的资源）
        '''
        pass

class ITC01010401_UpdateUninitializedDC(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-04编辑-01编辑Uninitialized状态数据中心
    @note: Uninitialized数据中心的每一项均可编辑，这里重点测试name、description、type以及version等4项
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Test: Create a DataCenter '%s'." % self.dm.pre_dc_name)
        self.dcapi.createDataCenter(self.dm.pre_dc_info)
        
    def test_UpdateUninitializedDC(self):
        '''
        @summary: 测试用例执行步骤
        STEP 1：编辑Uninitialized数据中心
        STEP 2：验证接口返回状态码以及检查编辑后的数据中心信息是否正确
        '''     

        self.flag = True
        r = self.dcapi.updateDataCenter(self.dm.pre_dc_name, self.dm.test_dc_info)
#         print r['status_code']
#         print xmltodict.unparse(r['result'], pretty=True)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.test_dc_info), r['result']):
                LogPrint().info("PASS: Update DataCenter SUCCESS.")
            else:
                LogPrint().error("FAIL: Update DataCenter FAIL, the actual dc info not equals to expected.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code of update operation INCORRECT.")
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        for dc_name in [self.dm.pre_dc_name, self.dm.test_dc_name]:
            if self.dcapi.searchDataCenterByName(dc_name)['result']['data_centers']:
                LogPrint().info("Post-Test: Delete the created/updated DataCenter '%s'." % dc_name)
                self.dcapi.delDataCenter(dc_name)
            
class ITC01010403_UpdateDC_DupName(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-04编辑-03数据中心重名
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Test: Create 2 DataCenters '%s and %s'." % (self.dm.dc_name_list[0], self.dm.dc_name_list[1]))
        
        @BaseTestCase.drive_data(self, self.dm.pre_dc_info)
        def do_test(xml_info):
            self.dcapi.createDataCenter(xml_info)
            
        do_test()
        
    def test_UpdateUninitializedDC(self):
        '''
        @summary: 测试用例执行步骤
        STEP 1：将一个DC名称编辑为另一个已存在的DC名称
        STEP 2：验证接口返回状态码以及检查编辑后的数据中心信息是否正确
        '''     
        self.flag = True
        r = self.dcapi.updateDataCenter(self.dm.target_dc_name, self.dm.test_dc_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when Update DC with a Dup name.")
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Operation FAIL, The returned status code is INCORRECT.")
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        for dc_name in self.dm.dc_name_list:
            if self.dcapi.searchDataCenterByName(dc_name)['result']['data_centers']:
                LogPrint().info("Post-Test: Delete the created/updated DataCenter '%s'." % dc_name)
                self.dcapi.delDataCenter(dc_name)
                
class ITC01010404_UpdateDCVersion_HighToLow(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-04编辑-04兼容版本由高到低
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Test: Create a DataCenter '%s' with high version.")
        self.dcapi.createDataCenter(self.dm.pre_dc_info)

    def test_UpdateDCVersion_HighToLow(self):
        '''
        @summary: 测试用例执行步骤
        STEP 1：将一个低版本的数据中心修改为高版本
        STEP 2：操作失败，验证接口返回状态码以及检查编辑后的数据中心信息是否正确
        '''     
        self.flag = True
        r = self.dcapi.updateDataCenter(self.dm.dc_name, self.dm.update_dc_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(r['result'], xmltodict.parse(self.dm.expected_info)):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when Update DC to lower version.")
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Operation FAIL. The returned status code is INCORRECT.")
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers']:
            LogPrint().info("Post-Test: Delete the created/updated DataCenter '%s'." % self.dm.dc_name)
            self.dcapi.delDataCenter(self.dm.dc_name)
            
class ITC01010501_DelDC_Uninitialized(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-05删除-01常规删除
    @note: 删除Uninitialized状态的数据中心
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Test: Create a DataCenter '%s'." % self.dm.dc_name)
        # PreStep-01：创建一个数据中心，其状态为Uninitialized
        self.dcapi.createDataCenter(self.dm.pre_dc_info)
        
    def test_DelDC_Uninitialized(self):
        '''
        @summary: 测试用例执行步骤
        STEP 1：删除一个Uninitialized状态的数据中心
        STEP 2：操作成功，验证接口返回状态码以及检查编辑后的数据中心信息是否正确
        '''     
        self.flag = True
        r = self.dcapi.delDataCenter(self.dm.dc_name)
        if r['status_code']==self.dm.expected_status_code:
            if self.dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers'] is None:
                LogPrint().info("PASS: Returned status code is CORRECT and Delete DC SUCCESS.")
            else:
                LogPrint().error("FAIL: Delete DC FAILED, the DC still exists.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Operation FAIL. The returned status code is INCORRECT.")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers']:
            LogPrint().info("Post-Test: Delete the created/updated DataCenter '%s'." % self.dm.dc_name)
            self.dcapi.delDataCenter(self.dm.dc_name)
      
class ITC01010502_DelDC_Force(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-01数据中心操作-05删除-02强制删除
    @note: 强制删除Uninitialized状态的数据中心
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.dcapi = DataCenterAPIs()
        LogPrint().info("Pre-Test: Create a DataCenter '%s'." % self.dm.dc_name)
        # PreStep-01：创建一个数据中心，其状态为Uninitialized
        self.dcapi.createDataCenter(self.dm.pre_dc_info)
        
    def test_DelDC_Uninitialized(self):
        '''
        @summary: 测试用例执行步骤
        STEP 1：强制删除一个Uninitialized状态的数据中心
        STEP 2：操作成功，验证接口返回状态码以及检查编辑后的数据中心信息是否正确
        '''     
        self.flag = True
        r = self.dcapi.delDataCenter(self.dm.dc_name, self.dm.del_dc_option)
        if r['status_code']==self.dm.expected_status_code:
            if not self.dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers']:
                LogPrint().info("PASS: Force-Delete DC SUCCESS. Returned status code is CORRECT.")
            else:
                LogPrint().error("FAIL: Force-Delete DC FAILED, the DC still exists.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Operation FAIL. The returned status code is INCORRECT.")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers']:
            LogPrint().info("Post-Test: Delete the created/updated DataCenter '%s'." % self.dm.dc_name)
            self.dcapi.delDataCenter(self.dm.dc_name)

class ITC010201_GetStorageDomainsOfDC(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-01查看存储域列表
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境（使用的是模块级测试环境，在ITC01_SetUp用例中创建）。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()

    def test_GetStorageDomainsOfDC(self):
        '''
        @summary: 测试步骤
        @note: （1）调用相应接口，获取数据中心存储域列表；
        @note: （2）操作成功，验证接口返回的状态码是否正确。
        '''
        dc_api = DataCenterAPIs()
        LogPrint().info("Test: Get storage domains list for data center '%s'." % ModuleData.dc_nfs_name)
        r = dc_api.getDCStorageDomainsList(ModuleData.dc_nfs_name)
        if r['status_code'] == 200:
            LogPrint().info("PASS: Get storage domains list for data center '%s' SUCCESS." % ModuleData.dc_nfs_name)
            self.flag = True
        else:
            LogPrint().error("FAIL: Get storage domains list fAILED. Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass

class ITC010202_GetStorageDomainInfoInDC(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-02查看存储域信息
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境（测试使用的数据中心、存储域是在ITC01_SetUp中创建的模块级测试环境）
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
    def test_GetStorageDomainInfoInDC(self):
        '''
        @summary: 测试步骤
        @note: （1）调用相应接口，查询DC-NFS-ITC01中data1-nfs-ITC01存储域信息；
        @note: （2）操作成功，验证接口返回的状态码、存储域信息是否正确。
        '''
        dc_api = DataCenterAPIs()
        LogPrint().info("Test: Get storage domain '%s' info from data center '%s'." % (ModuleData.data1_nfs_name, ModuleData.dc_nfs_name))
        r = dc_api.getDCStorageDomainInfo(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name)
        if r['status_code'] == self.dm.expected_status_code_get_sd_info:
            d1 = xmltodict.parse(self.dm.xml_sd_info)
            if DictCompare().isSubsetDict(d1, r['result']):
                LogPrint().info("PASS: Get storage domain '%s' info SUCCESS." % ModuleData.data1_nfs_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Get storage domain info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass

class ITC0102030101_AttachDataStorage_Master(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-03附加-01附加Data域-01Master
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        self.dc_api = DataCenterAPIs()
        self.cluster_api = ClusterAPIs()
        
        # 前提1：创建一个新的NFS数据中心
        LogPrint().info("Pre-Module-Test-1: Create DataCenter '%s'." % self.dm.dc_nfs_name)
        self.assertTrue(self.dc_api.createDataCenter(self.dm.xml_dc_info)['status_code']==self.dm.expected_status_code_create_dc)
        
        # 前提2：创建一个新的集群
        LogPrint().info("Pre-Module-Test-2: Create Cluster '%s' in DataCenter '%s'." % (self.dm.cluster_nfs_name, self.dm.dc_nfs_name))
        self.assertTrue(self.cluster_api.createCluster(self.dm.xml_cluster_info)['status_code']==self.dm.expected_status_code_create_cluster)
        
        # 前提3：创建一个新的主机
        LogPrint().info("Pre-Module-Test-3: Create Host '%s' in Cluster '%s'." % (self.dm.host_name, self.dm.cluster_nfs_name))
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.xml_host_info))
        
        # 前提4：准备一个unattached状态的data域（模块测试环境中的data2可以使用）
        LogPrint().info("Pre-Module-Test-4: Use unattached data storage '%s' for testing." % ModuleData.data2_nfs_name)

    def test_AttachDataStorage_Master(self):
        '''
        @summary: 测试步骤
        @note: （1）将data2_nfs附加到数据中心，成为Master存储域；
        @note: （2）验证接口返回的状态码是否正确。
        '''
        LogPrint().info("Test: Attach storage domain '%s' to data center '%s'." % (ModuleData.data2_nfs_name, self.dm.dc_nfs_name))
        r = self.dc_api.attachStorageDomainToDC(self.dm.dc_nfs_name, ModuleData.data2_nfs_name)
        if r['status_code'] == 201 and self.dc_api.getDCStorageDomainStatus(self.dm.dc_nfs_name, ModuleData.data2_nfs_name)=='active':
            LogPrint().info("PASS: Attach storage domain '%s' to data center '%s' SUCCESS." % (ModuleData.data2_nfs_name, self.dm.dc_nfs_name))
            self.flag = True
        else:
            LogPrint().error("FAIL: Attach storage domain '%s' to data center '%s' FAILED." % (ModuleData.data2_nfs_name, self.dm.dc_nfs_name))
            self.flag = False
        self.assertTrue (self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）
        '''
        # Step1：将data1存储域设置为Maintenance状态
        LogPrint().info("Post-Module-Test-1: Deactivate data storage domains '%s'." % ModuleData.data2_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, ModuleData.data2_nfs_name))
        
        # Step2：删除数据中心dc1（非强制，之后存储域变为Unattached状态）
        if self.dc_api.searchDataCenterByName(self.dm.dc_nfs_name)['result']['data_centers']:
            LogPrint().info("Post-Module-Test-2: Delete DataCenter '%s'." % self.dm.dc_nfs_name)
            self.assertTrue(self.dc_api.delDataCenter(self.dm.dc_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)

        # Step3：删除主机（host2）
        LogPrint().info("Post-Module-Test-3: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name, self.dm.xml_del_host_option))
        
        # Step4：删除集群cluster2
        if self.cluster_api.searchClusterByName(self.dm.cluster_nfs_name)['result']['clusters']:
            LogPrint().info("Post-Module-Test-4: Delete Cluster '%s'." % self.dm.cluster_nfs_name)
            self.assertTrue(self.cluster_api.delCluster(self.dm.cluster_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)

class ITC0102030102_AttachDataStorage_NotMaster(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-03附加-01附加Data域-02非Master
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dc_api = DataCenterAPIs()
        self.sd_api = StorageDomainAPIs()
        
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 验证目标存储域是否存在
        self.assertTrue(StorageDomainAPIs().searchStorageDomainByName(ModuleData.dc_nfs_name))
        
    def test_AttachDataStorage_NotMaster(self):
        '''
        @summary: 测试步骤
        @note: （1）将data2（data2-nfs-ITC01）附加到已有Master存储域的数据中心（DC-NFS-ITC01）；
        @note: （2）操作成功，验证接口返回的状态码、存储域信息中的data_center字段是否正确。
        '''
        LogPrint().info("Test: Attach data storage '%s' to datacenter '%s'." % (ModuleData.data2_nfs_name, ModuleData.dc_nfs_name))
        r = self.dc_api.attachStorageDomainToDC(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name)
        if r['status_code'] == self.dm.expected_status_code_attach_sd:
            data_storage_info = self.dc_api.getDCStorageDomainInfo(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name)['result']
            if data_storage_info['storage_domain']['data_center']['@id'] == self.dc_api.getDataCenterIdByName(ModuleData.dc_nfs_name):
                LogPrint().info("PASS: Attach data storage '%s' to data center '%s' SUCCESS." % (ModuleData.data2_nfs_name, ModuleData.dc_nfs_name))
                self.flag = True
            else:
                LogPrint().error("FAIL: Attach data storage '%s' to data center '%s' FAILED." % (ModuleData.data2_nfs_name, ModuleData.dc_nfs_name))
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status_code '%s' is Wrong after attaching storage domain to data center." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）将data2从数据中心分离（先维护，再分离），使其恢复为unattached状态。
        '''
        LogPrint().info("Post-Test-1: Deactivate storage domain to 'Maintenance'.")
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name))
        LogPrint().info("Post-Test-2: Detach storage domain from data center.")
        self.assertTrue(smart_detach_storage_domain(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name))

class ITC0102030201_AttachIsoStorage(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-03附加-02附加ISO域-01一个ISO域
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 初始化测试环境，使用模块级测试环境（dc_nfs/iso1）
    
    def test_ITC0102030201_AttachIsoStorage(self):
        '''
        @summary: 测试步骤
        @note: （1）将iso1附加到数据中心；
        @note: （2）操作成功，验证接口返回状态码、存储域所属DC信息是否正确。
        '''
        dc_api = DataCenterAPIs()
        LogPrint().info("Test: Begin to attach the ISO storage '%s' to Data Center '%s'." % (ModuleData.iso1_name, ModuleData.dc_nfs_name))
        r = dc_api.attachStorageDomainToDC(ModuleData.dc_nfs_name, ModuleData.iso1_name)
        if r['status_code'] == self.dm.expected_status_code_attach_sd:
            iso_info = dc_api.getDCStorageDomainInfo(ModuleData.dc_nfs_name, ModuleData.iso1_name)['result']
            if iso_info['storage_domain']['data_center']['@id'] == dc_api.getDataCenterIdByName(ModuleData.dc_nfs_name):
                LogPrint().info("PASS: Attach ISO storage '%s' to DataCenter '%s' SUCCESS." % (ModuleData.iso1_name, ModuleData.dc_nfs_name))
                self.flag = True
            else:
                LogPrint().error("FAIL: Attach ISO storage '%s' to DataCenter '%s' FAIL." % (ModuleData.iso1_name, ModuleData.dc_nfs_name))
                self.flag = False
        else:
            LogPrint().error("FAIL: Attach operation FAILED. Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = True
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）将ISO域设置为维护状态；
        @note: （2）将ISO域从数据中心分离。
        '''
        LogPrint().info("Post-Test-1: Deactivate storage domain to 'Maintenance'.")
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.iso1_name))
        LogPrint().info("Post-Test-2: Detach storage domain from data center.")
        self.assertTrue(smart_detach_storage_domain(ModuleData.dc_nfs_name, ModuleData.iso1_name))

class ITC0102030202_AttachIsoStorage_Second(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-03附加-02附加ISO域-02多个ISO域失败
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境；
        @note: （1）将模块测试环境中的ISO1附加到数据中心；
        @note: （2）创建一个新的ISO域（ISO2，本用例测试使用）。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test-1：将模块测试环境中的ISO1附加到数据中心
        self.assertTrue(smart_attach_storage_domain(ModuleData.dc_nfs_name, ModuleData.iso1_name))
        
        # Pre-Test-2：创建一个新的ISO域（ISO2）
        self.assertTrue(smart_create_storage_domain(self.dm.iso2_name, self.dm.xml_iso2_info))
        
    def test_AttachIsoStorage_Second(self):
        dc_api = DataCenterAPIs()
        # Test-1: 将ISO2附加到数据中心（预期操作失败）
        LogPrint().info("Test: Attach more than 1 iso storages to DataCenter.")
        r = dc_api.attachStorageDomainToDC(ModuleData.dc_nfs_name, self.dm.iso2_name)
        if r['status_code'] == self.dm.expected_status_code_attach_sd_fail:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_attach_sd_fail), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT while attaching more than 1 iso storage to DataCenter.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT while attaching more than 1 iso storages to DataCenter: \n %s" % xmltodict.unparse(r['result'], pretty=True))
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned staus code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        # 将ISO1维护、分离
        LogPrint().info("Post-Test-1: Deactivate and Detach the Module iso storage '%s' from DataCenter." % ModuleData.iso1_name)
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.iso1_name))
        self.assertTrue(smart_detach_storage_domain(ModuleData.dc_nfs_name, ModuleData.iso1_name))
        
        # 将ISO2删除
        LogPrint().info("Post-Test-2: Delete iso storage '%s' from DataCenter." % self.dm.iso2_name)
        self.assertTrue(smart_del_storage_domain(self.dm.iso2_name, self.dm.xml_del_iso_option, ModuleData.host1_name))

class ITC0102030301_AttachExportStorage(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-03附加-03附加Export域-01一个Export域
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 初始化测试环境，使用模块级测试环境（dc_nfs/export1）
    
    def test__AttachExportStorage(self):
        '''
        @summary: 测试步骤
        @note: （1）将export11附加到数据中心；
        @note: （2）操作成功，验证接口返回状态码、存储域所属DC信息是否正确。
        '''
        dc_api = DataCenterAPIs()
        LogPrint().info("Test: Begin to attach the Export storage '%s' to Data Center '%s'." % (ModuleData.export1_name, ModuleData.dc_nfs_name))
        r = dc_api.attachStorageDomainToDC(ModuleData.dc_nfs_name, ModuleData.export1_name)
        if r['status_code'] == self.dm.expected_status_code_attach_sd:
            export_info = dc_api.getDCStorageDomainInfo(ModuleData.dc_nfs_name, ModuleData.export1_name)['result']
            if export_info['storage_domain']['data_center']['@id'] == dc_api.getDataCenterIdByName(ModuleData.dc_nfs_name):
                LogPrint().info("PASS: Attach Export storage '%s' to DataCenter '%s' SUCCESS." % (ModuleData.export1_name, ModuleData.dc_nfs_name))
                self.flag = True
            else:
                LogPrint().error("FAIL: Attach Export storage '%s' to DataCenter '%s' FAIL." % (ModuleData.export1_name, ModuleData.dc_nfs_name))
                self.flag = False
        else:
            LogPrint().error("FAIL: Attach operation FAILED. Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = True
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）将export1域设置为维护状态；
        @note: （2）将export域从数据中心分离（不删除，因为export1是模块级测试环境）。
        '''
        LogPrint().info("Post-Test-1: Deactivate storage domain '%s' to 'Maintenance'." % ModuleData.export1_name)
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.export1_name))
        LogPrint().info("Post-Test-2: Detach storage domain '%s' from data center." % ModuleData.export1_name)
        self.assertTrue(smart_detach_storage_domain(ModuleData.dc_nfs_name, ModuleData.export1_name))

class ITC0102030302_AttachExportStorage_Second(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-03附加-03附加Export域-02多个Export域失败
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境；
        @note: （1）将模块测试环境中的export1附加到数据中心；
        @note: （2）创建一个新的Export域（export2，本用例测试使用）。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test-1：将模块测试环境中的export1附加到数据中心
        LogPrint().info("Pre-Test-1: Attach Export storage '%s' (already exist) to DataCenter '%s'." % (ModuleData.export1_name, ModuleData.dc_nfs_name))
        self.assertTrue(smart_attach_storage_domain(ModuleData.dc_nfs_name, ModuleData.export1_name))
        
        # Pre-Test-2：创建一个新的Export域（export2）
        LogPrint().info("Pre-Test-2: Create a new Export storage '%s' for test." % self.dm.export2_name)
        self.assertTrue(smart_create_storage_domain(self.dm.export2_name, self.dm.xml_export2_info))
        
    def test_AttachExportStorage_Second(self):
        '''
        @summary: 测试步骤
        @note: （1）将export2附加到数据中心（数据中心已有Export域）；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        dc_api = DataCenterAPIs()
        
        # Test-1: 将export2附加到数据中心（预期操作失败）
        LogPrint().info("Test: Attach more than 1 Export storages to DataCenter.")
        r = dc_api.attachStorageDomainToDC(ModuleData.dc_nfs_name, self.dm.export2_name)
        if r['status_code'] == self.dm.expected_status_code_attach_sd_fail:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_attach_sd_fail), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT while attaching more than 1 Export storage to DataCenter.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT while attaching more than 1 Export storages to DataCenter: \n %s" % xmltodict.unparse(r['result'], pretty=True))
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        # 将export1维护、分离
        LogPrint().info("Post-Test-1: Deactivate and Detach the Module Export storage '%s' from DataCenter." % ModuleData.export1_name)
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.export1_name))
        self.assertTrue(smart_detach_storage_domain(ModuleData.dc_nfs_name, ModuleData.export1_name))
        
        # 将export2删除
        LogPrint().info("Post-Test-2: Delete Export storage '%s' from DataCenter." % self.dm.export2_name)
        self.assertTrue(smart_del_storage_domain(self.dm.export2_name, self.dm.xml_del_export_option, ModuleData.host1_name))

class ITC0102030401_AttachStorage_NoActiveDataStorage(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-03附加-04错误验证-01缺少正常状态Data域时附加其他存储
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # Pre-Test-1：将当前DC-NFS-ITC01中的主存储域设置为Maintenance状态
        LogPrint().info("Pre-Test: Deactivate DataStorage '%s' for this test case." % ModuleData.data1_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name))
        
    def test_AttachStorage_NoActiveDataStorage(self):
        '''
        @summary: 测试步骤
        @note: （1）将已存在的ISO域iso1附加到数据中心（DC-NFS-ITC01）
        @note: （2）操作失败（因为数据中心缺少Active状态的Data域），验证接口返回的状态码、提示信息是否正确。
        '''
        dc_api = DataCenterAPIs()
        LogPrint().info("Test: Begin to attach a storage to DataCenter without active data_storage.")
        r = dc_api.attachStorageDomainToDC(ModuleData.dc_nfs_name, ModuleData.iso1_name)
        if r['status_code'] == self.dm.expected_status_code_attach_sd_fail:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_attach_sd_fail), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT while attaching a storage to DataCenter without active data_storage.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are CORRECT while attaching a storage to DataCenter without active data_storage.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）重新激活data1-nfs-ITC01
        '''
        LogPrint().info("Post-Test: Activate data_storage '%s' again." % ModuleData.data1_nfs_name)
        self.assertTrue(smart_active_storage_domain(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name))

class ITC01020401_DetachStorage_Iso(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-04分离-01分离ISO存储域
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：附加一个ISO域到数据中心
        LogPrint().info("Pre-Test-1: Attach the '%s' storage to DataCenter '%s'." % (ModuleData.iso1_name, ModuleData.dc_nfs_name))
        self.assertTrue(smart_attach_storage_domain(ModuleData.dc_nfs_name, ModuleData.iso1_name))
        
        # 前提2：将该ISO域设置为维护状态
        LogPrint().info("Pre-Test-2: Set the storage domain '%s' to 'maintenance' state." % ModuleData.iso1_name)
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.iso1_name))
        
    def test_DetachStorage_Iso(self):
        '''
        @summary: 测试步骤
        @note: （1）将iso1设置为维护状态；
        @note: （2）将iso1从数据中心分离；
        @note: （3）操作成功，验证接口返回的状态码、相关信息是否正确。
        '''
        dc_api = DataCenterAPIs()
        sd_api = StorageDomainAPIs()
        LogPrint().info("Test: Detach ISO storage from DataCenter.")
        r = dc_api.detachStorageDomainFromDC(ModuleData.dc_nfs_name, ModuleData.iso1_name, self.dm.xml_detach_iso_option)
        if r['status_code'] == self.dm.expected_status_code_detach_sd:
            if sd_api.getStorageDomainStatus(ModuleData.iso1_name) == 'unattached':
                LogPrint().info("PASS: Detach ISO storage '%s' from DataCenter SUCCESS." % ModuleData.iso1_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Detach ISO storage '%s' from DataCenter FAILED." % ModuleData.iso1_name)
                self.flag = False
        else:
            LogPrint().info("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass

class ITC01020402_DetachStorage_Export(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-04分离-02分离Export存储域
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：附加一个Export域到数据中心
        LogPrint().info("Pre-Test-1: Attach the '%s' storage to DataCenter '%s'." % (ModuleData.export1_name, ModuleData.dc_nfs_name))
        self.assertTrue(smart_attach_storage_domain(ModuleData.dc_nfs_name, ModuleData.export1_name))
        
        # 前提2：将该Export域设置为维护状态
        LogPrint().info("Pre-Test-2: Set the storage domain '%s' to 'maintenance' state." % ModuleData.export1_name)
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.export1_name))
        
    def test_DetachStorage_Export(self):
        '''
        @summary: 测试步骤
        @note: （1）将export1设置为维护状态；
        @note: （2）将export1从数据中心分离；
        @note: （3）操作成功，验证接口返回的状态码、相关信息是否正确。
        '''
        dc_api = DataCenterAPIs()
        sd_api = StorageDomainAPIs()
        LogPrint().info("Test: Detach Export storage from DataCenter.")
        r = dc_api.detachStorageDomainFromDC(ModuleData.dc_nfs_name, ModuleData.export1_name, self.dm.xml_detach_export_option)
        if r['status_code'] == self.dm.expected_status_code_detach_sd:
            if sd_api.getStorageDomainStatus(ModuleData.export1_name) == 'unattached':
                LogPrint().info("PASS: Detach Export storage '%s' from DataCenter SUCCESS." % ModuleData.export1_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Detach Export storage '%s' from DataCenter FAILED." % ModuleData.export1_name)
                self.flag = False
        else:
            LogPrint().info("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass

class ITC0102040301_DetachStorage_Data_Normal(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-04分离-03分离Data域-01附加有多个Data域
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：附加第二个Data域到数据中心（模块级数据中心已经有一个Data域）
        LogPrint().info("Pre-Test-1: Attach the 2nd DataStorage '%s' to DataCenter '%s'." % (ModuleData.data2_nfs_name, ModuleData.dc_nfs_name))
        self.assertTrue(smart_attach_storage_domain(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name))
        
        # 前提2：将该Data域设置为维护状态
        LogPrint().info("Pre-Test-2: Set the DataStorage '%s' to 'maintenance' state." % ModuleData.data2_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name))
        
    def test_DetachStorage_Export(self):
        '''
        @summary: 测试步骤
        @note: （1）将data2设置为维护状态；
        @note: （2）将data2从数据中心分离；
        @note: （3）操作成功，验证接口返回的状态码、相关信息是否正确。
        '''
        dc_api = DataCenterAPIs()
        sd_api = StorageDomainAPIs()
        LogPrint().info("Test: Detach Data storage from DataCenter.")
        r = dc_api.detachStorageDomainFromDC(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name, self.dm.xml_detach_data_option)
        if r['status_code'] == self.dm.expected_status_code_detach_sd:
            if sd_api.getStorageDomainStatus(ModuleData.data2_nfs_name) == 'unattached':
                LogPrint().info("PASS: Detach Data storage '%s' from DataCenter SUCCESS." % ModuleData.data2_nfs_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Detach Data storage '%s' from DataCenter FAILED." % ModuleData.data2_nfs_name)
                self.flag = False
        else:
            LogPrint().info("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass        

class ITC0102040302_DetachStorage_Data_One(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-04分离-03分离Data域-02只有一个Data域时失败
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：将模块测试环境中的data1-nfs域设置为维护状态
        LogPrint().info("Pre-Test: Set the DataStorage '%s' to 'maintenance' state." % ModuleData.data1_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name))
        
    def test_DetachStorage_Data_One(self):
        '''
        @summary: 测试步骤
        @note: （1）将data1从数据中心分离；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        dc_api = DataCenterAPIs()
        LogPrint().info("Test: Detach Data storage '%s' from DataCenter." % ModuleData.data1_nfs_name)
        r = dc_api.detachStorageDomainFromDC(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name, self.dm.xml_detach_data_option)
        if r['status_code'] == self.dm.expected_status_code_detach_sd_fail:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_detach_sd_fail), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT while detaching Data storage '%s' from DataCenter." % ModuleData.data1_nfs_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT.")
                self.flag = False
        else:
            LogPrint().info("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        self.assertTrue(smart_active_storage_domain(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name))     

class ITC01020501_ActivateStorage_Normal(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-05激活-01正常激活
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：附加data2，然后将其设置为Maintenance状态。
        LogPrint().info("Pre-Test: Attach data storage '%s' and set it's state as 'Maintenance'." % ModuleData.data2_nfs_name)
        self.assertTrue(smart_attach_storage_domain(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name))
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name))
        
    def test_ActivateStorage_Normal(self):
        '''
        @summary: 测试步骤
        @note: （1）将data2激活；
        @note: （2）操作成功，验证接口返回状态码、存储域状态是否正确。
        '''
        dc_api = DataCenterAPIs()
        LogPrint().info("Test: Activate data storage '%s'." % ModuleData.data2_nfs_name)
        r = dc_api.activeDCStorageDomain(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name)
        if r['status_code'] == self.dm.expected_status_code_activate_sd:
            if dc_api.getDCStorageDomainStatus(ModuleData.dc_nfs_name, ModuleData.data2_nfs_name) == 'active':
                LogPrint().info("PASS: Activate storage domain '%s' SUCCESS." % ModuleData.data2_nfs_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Activate storage domain '%s' FAILED." % ModuleData.data2_nfs_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        LogPrint().info("Post-Test: Deactivate and Detach storage '%s' from DataCenter '%s'." % (ModuleData.data2_nfs_name, ModuleData.dc_nfs_name))
        self.assertTrue(smart_deactive_storage_domain(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name))
        self.assertTrue(smart_detach_storage_domain(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name))

class ITC01020601_DeactivateStorage_Normal(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-02存储域操作-06取消激活-01Active状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
    def test_DeactivateStorage_Normal(self):
        '''
        @summary: 测试步骤
        @note: （1）取消激活data1-nfs；
        @note: （2）操作成功，验证接口返回的状态码、存储域状态是否正确。
        '''
        dc_api = DataCenterAPIs()
        LogPrint().info("Test: Deactivate storage domain '%s'." % ModuleData.data1_nfs_name)
        r = dc_api.deactiveDCStorageDomain(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name)
        if r['status_code'] == self.dm.expected_status_code_deactivate_sd:
            if dc_api.getDCStorageDomainStatus(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name) == 'maintenance':
                LogPrint().info("PASS: Deactivate storage domain '%s' SUCCESS." % ModuleData.data1_nfs_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Deactivate storage domain '%s' FAILED. It's state is not 'maintenance'." % ModuleData.data1_nfs_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        LogPrint().info("Post-Test: Activate data storage '%s'." % ModuleData.data1_nfs_name)
        self.assertTrue(smart_active_storage_domain(ModuleData.dc_nfs_name, ModuleData.data1_nfs_name))

class ITC010301_GetClustersInDataCenter(BaseTestCase):
    '''
    @summary: ITC-01数据中心管理-03集群操作-01查看集群列表
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
    def test_GetClustersInDataCenter(self):
        '''
        @summary: 测试步骤
        @note: （1）获取数据中心下的集群列表；
        @note: （2）操作成功，验证接口返回的状态码是否正确。
        '''
        dc_api = DataCenterAPIs()
        r = dc_api.getDCClustersList(ModuleData.dc_nfs_name)
        if r['status_code'] == self.dm.expected_status_code_get_clusters_in_dc:
            LogPrint().info("PASS: Get clustes list in DataCenter '%s' SUCCESS." % ModuleData.dc_nfs_name)
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass

class ITC01_TearDown(BaseTestCase):
    '''
    @summary: “数据中心管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: （1）将数据中心里的Data域（data1）设置为Maintenance状态；
    @note: （2）删除数据中心dc（非强制）；
    @note: （3）删除所有unattached状态的存储域（data1/data2/iso1/export1）；
    @note: （4）删除主机host1；
    @note: （5）删除集群cluster1。 
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = self.initData('ITC01_SetUp')
        
    def test_TearDown(self):
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        
        # Step1：将data1存储域设置为Maintenance状态
        LogPrint().info("Post-Module-Test-1: Deactivate data storage domains '%s'." % self.dm.data1_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
        
        # Step2：删除数据中心dc1（非强制，之后存储域变为Unattached状态）
        if dcapi.searchDataCenterByName(self.dm.dc_nfs_name)['result']['data_centers']:
            LogPrint().info("Post-Module-Test-2: Delete DataCenter '%s'." % self.dm.dc_nfs_name)
            self.assertTrue(dcapi.delDataCenter(self.dm.dc_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)
                
        # Step3：删除4个Unattached状态存储域（data1/data2/iso1/export1）
        LogPrint().info("Post-Module-Test-3: Delete all unattached storage domains.")
        dict_sd_to_host = [self.dm.data1_nfs_name, self.dm.data2_nfs_name, self.dm.iso1_name, self.dm.export1_name]
        for sd in dict_sd_to_host:
            smart_del_storage_domain(sd, self.dm.xml_del_sd_option, host_name=self.dm.host1_name)
        
        # Step4：删除主机（host1）
        LogPrint().info("Post-Module-Test-6: Delete host '%s'." % self.dm.host1_name)
        self.assertTrue(smart_del_host(self.dm.host1_name, self.dm.xml_del_host_option))
        
        # Step5：删除集群cluster1
        if capi.searchClusterByName(self.dm.cluster_nfs_name)['result']['clusters']:
            LogPrint().info("Post-Module-Test-5: Delete Cluster '%s'." % self.dm.cluster_nfs_name)
            self.assertTrue(capi.delCluster(self.dm.cluster_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)

if __name__ == "__main__":
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["DataCenter.ITC01_TearDown"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)

#     fileName = r"d:\result.html"
#     fp = file(fileName, 'wb')
#     runner = HTMLTestRunner(stream=fp, title=u"测试结果", description=u"测试报告")
#     runner.run(testSuite)