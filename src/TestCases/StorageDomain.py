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
from TestAPIs.HostAPIs import HostAPIs
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from Utils.Util import wait_until
from TestData.StorageDomain import ITC04_SetUp as ModuleData

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
        
        @BaseTestCase.drive_data(self, self.dm.dc_info)
        def create_data_centers(xml_dc_info):
            LogPrint().info("Pre-Module-Test: Create DataCenter '%s'." % xmltodict.parse(xml_dc_info)['data_center']['name'])
            self.assertTrue(dcapi.createDataCenter(xml_dc_info)['status_code']==self.dm.expected_status_code_create_dc)
        create_data_centers()
        
        @BaseTestCase.drive_data(self, self.dm.cluster_info)
        def create_clusters(xml_cluster_info):
            LogPrint().info("Pre-Module-Test: Create Cluster '%s' in DataCenter '%s'." % (xmltodict.parse(xml_cluster_info)['cluster']['name'], xmltodict.parse(xml_cluster_info)['cluster']['data_center']['name']))
            self.assertTrue(capi.createCluster(xml_cluster_info)['status_code']==self.dm.expected_status_code_create_cluster)
        create_clusters()
        
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
        for cluster in ModuleData.cluster_name_list:
            if capi.searchClusterByName(cluster)['result']['clusters']:
                LogPrint().info("Post-Module-Test: Delete Cluster '%s'." % cluster)
                self.assertTrue(capi.delCluster(cluster)['status_code']==self.dm.expected_status_code_del_dc)
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
        
        # 前提1：新建主机host并处于UP状态
        
        # 前提2：创建一个Data存储域（不加入任何数据中心，处于游离状态）
    
    def test_GetStorageDomainsInfo(self):
        '''
        @summary: 测试步骤
        @note: （1）调用相应接口，获取存储域信息；
        @note: （2）操作成功，验证接口返回的状态码、存储域信息是否正确。
        '''
        pass
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除存储域（维护、分离、删除）
        @note: （2）删除
        '''
        

if __name__ == "__main__":
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["StorageDomain.ITC040101_GetStorageDomainsList"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)

#     fileName = r"d:\result.html"
#     fp = file(fileName, 'wb')
#     runner = HTMLTestRunner(stream=fp, title=u"测试结果", description=u"测试报告")
#     runner.run(testSuite)