#encoding:utf-8


__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import unittest

import xmltodict

from BaseTestCase import BaseTestCase
from TestAPIs.DataCenterAPIs import DataCenterAPIs
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from TestData.StorageDomain import ITC04_SetUp as ModuleData
from TestCases.Host import smart_create_host, smart_del_host

def smart_del_storage_domain(sd_name, xml_del_option, status_code=200):
    '''
    @summary: 智能删除存储域（unattached状态）
    '''
    sd_api = StorageDomainAPIs()
    LogPrint().info("Post-Test: Delete StorageDomain '%s'." % sd_name)
    if sd_api.searchStorageDomainByName(sd_name)['result']['storage_domains']:
        r = sd_api.delStorageDomain(sd_name, xml_del_option)
        return (r['status_code']==status_code)
    else:
        LogPrint().info("Post-Test: StorageDomain '%s' not exists." % sd_name)
        return True


class ITC04_SetUp(BaseTestCase):
    '''
    @summary: “存储域管理”模块测试环境初始化（执行该模块测试用例时，都需要执行该用例搭建初始化环境）
    @note: （1）分别创建三个数据中心（NFS/ISCSI/FC）；
    @note: （2）分别创建三个集群。
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()

    def test_Create_DcAndCluster(self):
        '''
        @summary: 创建3个数据中心和3个集群
        '''
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        
        # 创建3个数据中心（3种类型）
        @BaseTestCase.drive_data(self, self.dm.dc_info)
        def create_data_centers(xml_dc_info):
            LogPrint().info("Pre-Module-Test: Create DataCenter '%s'." % xmltodict.parse(xml_dc_info)['data_center']['name'])
            self.assertTrue(dcapi.createDataCenter(xml_dc_info)['status_code']==self.dm.expected_status_code_create_dc)
        create_data_centers()
        
        # 创建3个集群
        @BaseTestCase.drive_data(self, self.dm.cluster_info)
        def create_clusters(xml_cluster_info):
            LogPrint().info("Pre-Module-Test: Create Cluster '%s' in DataCenter '%s'." % (xmltodict.parse(xml_cluster_info)['cluster']['name'], xmltodict.parse(xml_cluster_info)['cluster']['data_center']['name']))
            self.assertTrue(capi.createCluster(xml_cluster_info)['status_code']==self.dm.expected_status_code_create_cluster)
        create_clusters()
        
        # 在NFS类型DC中创建一个主机host1，并等待其变为UP状态。
        self.assertTrue(smart_create_host(self.dm.host1_name, self.dm.host1_info_xml))
        
class ITC04_TearDown(BaseTestCase):
    '''
    @summary: “主机管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: （1）删除集群；
    @note: （2）删除数据中心；
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = self.initData('ITC04_SetUp')
        
    def test_TearDown(self):
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        
        # 删除主机host1
        self.assertTrue(smart_del_host(self.dm.host1_name, self.dm.xml_del_host_option))
        
        # 删除3个集群
        for cluster in ModuleData.cluster_name_list:
            if capi.searchClusterByName(cluster)['result']['clusters']:
                LogPrint().info("Post-Module-Test: Delete Cluster '%s'." % cluster)
                self.assertTrue(capi.delCluster(cluster)['status_code']==self.dm.expected_status_code_del_dc)
                
        # 删除3个数据中心
        for dc in self.dm.dc_name_list:
            if dcapi.searchDataCenterByName(dc)['result']['data_centers']:
                LogPrint().info("Post-Module-Test: Delete DataCenter '%s'." % dc)
                self.assertTrue(dcapi.delDataCenter(dc)['status_code']==self.dm.expected_status_code_del_cluster)

class ITC040101_GetStorageDomainsList(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-01查看全部存储域列表
    '''
    def test_GetStorageDomainsList(self):
        sd_api = StorageDomainAPIs()
        r = sd_api.getStorageDomainsList()
        if r['status_code']==200:
            LogPrint().info('PASS: Get StorageDomains list SUCCESS.')
        else:
            LogPrint().error('FAIL: Get StorageDomains list FAILED. Returned status code "%s" is incorrect.' % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)

class ITC040102_GetStorageDomainInfo(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-02查看存储域信息
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        self.sd_api = StorageDomainAPIs()
        
        # 前提1：创建一个NFS类型存储域（data1，游离）
        LogPrint().info("Pre-Test: Create a DataStorage '%s' for this test case." % self.dm.data1_name)
        r = self.sd_api.createStorageDomain(self.dm.data1_info_xml)
        self.assertTrue(r['status_code']==self.dm.expected_status_code_create_sd)
    
    def test_GetStorageDomainsInfo(self):
        '''
        @summary: 测试步骤
        @note: （1）调用相应接口，获取存储域信息；
        @note: （2）操作成功，验证接口返回的状态码、存储域信息是否正确。
        '''
        LogPrint().info("Test: Get info of DataStorage '%s'." % self.dm.data1_name)
        r = self.sd_api.getStorageDomainInfo(self.dm.data1_name)
        if r['status_code'] == self.dm.expected_statsu_code_get_sd_info:
            dictCompare = DictCompare()
            d1 = xmltodict.parse(self.dm.data1_info_xml)
            del d1['storage_domain']['host']
            d2 = r['result']
            if dictCompare.isSubsetDict(d1, d2):
                LogPrint().info("PASS: Get DataStorage '%s' info SUCCESS." % self.dm.data1_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Get StorageDomain's info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT while Get sd's info." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的游离存储
        '''
        LogPrint().info("Post-Test: Delete the DataStorage '%s'." % self.dm.data1_name)
        r = self.sd_api.delStorageDomain(self.dm.data1_name, self.dm.xml_del_storage_domain_option)
        self.assertTrue(r['status_code']==self.dm.expected_status_code_del_sd)

class ITC0401030101_CreateNfsSd_Normal(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-03创建-01NFS-01正常创建
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        self.sd_api = StorageDomainAPIs()
        
    def test_CreateNfsSd_Normal(self):
        '''
        @summary: 测试步骤
        @note: （1）创建一个NFS的Data类型存储域，不附加到任何数据中心；
        @note: （2）操作成功，验证接口返回的状态码、提示信息是否正确。
        '''
        # 创建NFS的Data类型存储域（unattached状态）
        LogPrint().info("Test: Start creating DataStorage '%s' with NFS type." % self.dm.data1_name)
        r = self.sd_api.createStorageDomain(self.dm.data1_info_xml)
        if r['status_code'] == self.dm.expected_status_code_create_sd:
            dictCompare = DictCompare()
            d1 = xmltodict.parse(self.dm.data1_info_xml)
            del d1['storage_domain']['host']
            if dictCompare.isSubsetDict(d1, r['result']):
                LogPrint().info("PASS: Create NFS type StorageDomain '%s' SUCCESS." % self.dm.data1_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Created StorageDomain's info are INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT when creating new DataStorage." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的游离存储
        '''
        LogPrint().info("Post-Test: Delete the DataStorage '%s'." % self.dm.data1_name)
        r = self.sd_api.delStorageDomain(self.dm.data1_name, self.dm.xml_del_sd_option)
        self.assertTrue(r['status_code']==self.dm.expected_status_code_del_sd)

class ITC0401030102_CreateNfsSd_DupName(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-03创建-01NFS-02重名
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个存储域sd1
        self.sd_api = StorageDomainAPIs()
        LogPrint().info("Pre-Test: Create the 1st StorageDomain with name '%s'." % self.dm.data1_name)
        r = self.sd_api.createStorageDomain(self.dm.data1_info_xml)
        self.assertTrue(r['status_code'] == self.dm.expected_info_create_sd)
        
    def test_CreateNfsSd_DupName(self):
        '''
        @summary: 测试步骤
        @note: （1）创建一个同名的存储域sd2
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        LogPrint().info("Test: Create 2nd StorageDomain with Dup name '%s'." % self.dm.data1_name)
        r = self.sd_api.createStorageDomain(self.dm.data2_info_xml)
        if r['status_code'] == self.dm.expected_status_code_create_sd_dup_name:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_create_sd_dup_name), r['result']):
                LogPrint().info("PASS: Returned status_code and messages are CORRECT while creating StorageDomain with Dup Name.")
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
        @summary: 资源清理
        @note: （1）删除创建的存储域
        '''
        smart_del_storage_domain(self.dm.data1_name, self.dm.xml_del_sd_option, self.dm.expected_status_code_del_sd)

class ITC0401030103_CreateNfsSd_NameVerify(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-03创建-01NFS-03名称有效性验证
    @todo: 未完成
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
    
    def test_CreateNfsSd_NameVerify(self):
        '''
        @summary: 测试步骤
        @note: （1）验证创建Storage Domain时输入名称的有效性；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        sd_api = StorageDomainAPIs()
        r = sd_api.createStorageDomain(self.dm.sd_info_list)
        print r['status_code']
        print xmltodict.unparse(r['result'], pretty=True)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        for sd in self.dm.sd_name_list:
            smart_del_storage_domain(sd, self.dm.xml_del_sd_option, self.dm.expected_status_code_del_sd)

class ITC0401030104_CreateNfsSd_IpVerify(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-03创建-01NFS-04地址有效性验证
    '''
    def setUp(self):
        '''
        @summary: 初始化测试环境
        '''
        self.dm = super(self.__class__, self).setUp()
        self.sd_api = StorageDomainAPIs()
        
    def test_CreateNfsSd_IpVerify(self):
        '''
        @summary: 测试步骤
        @note: （1）输入各种不合法的IP，创建存储域；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        # 使用数据驱动，根据测试数据文件循环创建多个名称非法的主机
        @BaseTestCase.drive_data(self, self.dm.xml_sd_info_list)
        def do_test(xml_info):
            r = self.sd_api.createStorageDomain(xml_info)
            # 验证接口返回状态码是否正确
            if r['status_code'] == self.dm.expected_status_code_create_sd_fail:
                # 验证接口返回提示信息是否正确
                sd_ip = xmltodict.parse(xml_info)['storage_domain']['storage']['address']
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_create_sd_fail), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT when create storage domain with invalid IP address '%s'." % sd_ip)
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned messages are INCORRECT when create storage domain with the invalid IP address '%s'." % sd_ip)
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' is INCORRECT." % (r['status_code']))
                self.flag = False
            self.assertTrue(self.flag)
            
        do_test()
            
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        smart_del_storage_domain(self.dm.sd_name, self.dm.xml_del_sd_option)

class ITC0401030105_CreateNfsSd_PathVerify(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-03创建-01NFS-05路径有效性验证
    '''
    def setUp(self):
        '''
        @summary: 初始化测试环境
        '''
        self.dm = super(self.__class__, self).setUp()
        self.sd_api = StorageDomainAPIs()
        
    def test_CreateNfsSd_PathVerify(self):
        '''
        @summary: 测试步骤
        @note: （1）输入各种不合法的Path，创建存储域；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        # 使用数据驱动，根据测试数据文件循环创建多个Path非法的存储域
        @BaseTestCase.drive_data(self, self.dm.xml_sd_info_list)
        def do_test(xml_info):
            r = self.sd_api.createStorageDomain(xml_info)
            # 验证接口返回状态码是否正确
            if r['status_code'] == self.dm.expected_status_code_create_sd_fail:
                # 验证接口返回提示信息是否正确
                sd_path = xmltodict.parse(xml_info)['storage_domain']['storage']['path']
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_create_sd_fail), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT when create storage domain with invalid Path '%s'." % sd_path)
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned messages are INCORRECT when create storage domain with the invalid Path '%s'." % sd_path)
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' is INCORRECT." % (r['status_code']))
                self.flag = False
            self.assertTrue(self.flag)
            
        do_test()
            
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        smart_del_storage_domain(self.dm.sd_name, self.dm.xml_del_sd_option)



if __name__ == "__main__":
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["StorageDomain.ITC0401030105_CreateNfsSd_PathVerify"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)

#     fileName = r"d:\result.html"
#     fp = file(fileName, 'wb')
#     runner = HTMLTestRunner(stream=fp, title=u"测试结果", description=u"测试报告")
#     runner.run(testSuite)