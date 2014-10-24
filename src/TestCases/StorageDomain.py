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
from copy import deepcopy

import xmltodict

from BaseTestCase import BaseTestCase
from TestAPIs.DataCenterAPIs import DataCenterAPIs, smart_attach_storage_domain, smart_deactive_storage_domain, smart_detach_storage_domain
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs, DataStorageAPIs, ISOStorageAPIs, smart_create_storage_domain, smart_del_storage_domain
from TestAPIs.DiskAPIs import DiskAPIs
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from TestCases.Host import smart_create_host, smart_del_host
from TestCases.Disk import smart_create_disk, smart_delete_disk


class ITC04_SetUp(BaseTestCase):
    '''
    @summary: “存储域管理”模块测试环境初始化（执行该模块测试用例时，都需要执行该用例搭建初始化环境）
    @note: （1）分别创建三个数据中心（NFS/ISCSI/FC）；
    @note: （2）分别创建三个集群；
    @note: （3）在NFS/ISCSI集群中分别创建一个主机；
    @note: （4）分别创建NFS/ISCSI类型Data存储域，创建一个ISO/Export存储域；
    @note: （5）将两个Data存储域分别附加到相应的数据中心，将ISO/Export域附加在NFS数据中心。
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
            LogPrint().info("Pre-Module-Test-1: Create DataCenter '%s'." % xmltodict.parse(xml_dc_info)['data_center']['name'])
            self.assertTrue(dcapi.createDataCenter(xml_dc_info)['status_code']==self.dm.expected_status_code_create_dc)
        create_data_centers()
        
        # 创建3个集群
        @BaseTestCase.drive_data(self, self.dm.cluster_info)
        def create_clusters(xml_cluster_info):
            LogPrint().info("Pre-Module-Test-2: Create Cluster '%s' in DataCenter '%s'." % (xmltodict.parse(xml_cluster_info)['cluster']['name'], xmltodict.parse(xml_cluster_info)['cluster']['data_center']['name']))
            self.assertTrue(capi.createCluster(xml_cluster_info)['status_code']==self.dm.expected_status_code_create_cluster)
        create_clusters()
        
        # 在NFS/ISCSI数据中心中分别创建一个主机，并等待主机UP。
        @BaseTestCase.drive_data(self, self.dm.hosts_info_xml)
        def create_hosts(xml_host_info):
            LogPrint().info("Pre-Module-Test-3: Create Host '%s' in Cluster '%s'." % (xmltodict.parse(xml_host_info)['host']['name'], xmltodict.parse(xml_host_info)['host']['cluster']['name']))
            self.assertTrue(smart_create_host(xmltodict.parse(xml_host_info)['host']['name'], xml_host_info))
        create_hosts()
        
        # 为NFS/ISCSI数据中心分别创建Data域，为NFS数据中心创建ISO/Export域。
        @BaseTestCase.drive_data(self, self.dm.xml_datas_info)
        def create_storage_domains(xml_storage_domain_info):
            sd_name = xmltodict.parse(xml_storage_domain_info)['storage_domain']['name']
            LogPrint().info("Pre-Module-Test-4: Create Data Storage '%s'." % (sd_name))
            self.assertTrue(smart_create_storage_domain(sd_name, xml_storage_domain_info))
        create_storage_domains()
        
        # 将创建的的Data域分别附加到NFS/ISCSI数据中心里。
        LogPrint().info("Pre-Module-Test-5: Attach the data storages to data centers.")
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_iscsi_name, self.dm.data1_iscsi_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.iso1_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))

    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass
        
class ITC04_TearDown(BaseTestCase):
    '''
    @summary: “主机管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: （1）将数据中心里的Data域全部设置为Maintenance状态；
    @note: （2）删除数据中心（非强制）；
    @note: （3）删除unattached状态的Data存储域；
    @note: （4）删除主机；
    @note: （5）删除集群；
    @note: （6）删除数据中心。 
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
        
        # Step1：将ISO域和Export域设置为Maintenance状态
        LogPrint().info("Post-Module-Test-1: Deactivate ISO and Export storage domains.")
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.iso1_name))
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        
        # Step2：将ISO域和Export域从对应的数据中心分离（detach）
        LogPrint().info("Post-Module-Test-2: Deattch ISO and Export storage domains.")
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.iso1_name))
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        
        # Step3：将Data存储域设置为Maintenance状态
        LogPrint().info("Post-Module-Test-3: Deactivate all data storage domains.")
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_iscsi_name, self.dm.data1_iscsi_name))
        
        # 删除3个数据中心（非强制，之后存储域变为Unattached状态）
        for dc in self.dm.dc_name_list:
            if dcapi.searchDataCenterByName(dc)['result']['data_centers']:
                LogPrint().info("Post-Module-Test-4: Delete DataCenter '%s'." % dc)
                self.assertTrue(dcapi.delDataCenter(dc)['status_code']==self.dm.expected_status_code_del_dc)
                
        # 删除3个Unattached状态的Data存储域和ISO/Export域（如果没有配置FC，则删除2个）
        LogPrint().info("Post-Module-Test-5: Delete all storage domains.")
        dict_sd_to_host = {self.dm.data1_nfs_name:self.dm.host1_name, self.dm.data1_iscsi_name:self.dm.host4_name, 
                           self.dm.iso1_name:self.dm.host1_name, self.dm.export1_name:self.dm.host1_name}
        for sd in dict_sd_to_host:
            smart_del_storage_domain(sd, self.dm.xml_del_sd_option, host_name=dict_sd_to_host[sd])
        
        # 删除主机（host1和host4）
        LogPrint().info("Post-Module-Test-6: Delete all hosts.")
        for host_name in [self.dm.host1_name, self.dm.host4_name]:
            self.assertTrue(smart_del_host(host_name, self.dm.xml_del_host_option))
        
        # 删除3个集群
        for cluster in self.dm.cluster_name_list:
            if capi.searchClusterByName(cluster)['result']['clusters']:
                LogPrint().info("Post-Module-Test-7: Delete Cluster '%s'." % cluster)
                self.assertTrue(capi.delCluster(cluster)['status_code']==self.dm.expected_status_code_del_dc)

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
    
    def test_GetStorageDomainsInfo(self):
        '''
        @summary: 测试步骤
        @note: （1）调用相应接口，获取模块级测试环境中的存储域信息；
        @note: （2）操作成功，验证接口返回的状态码、存储域信息是否正确。
        '''
        LogPrint().info("Test: Get info of DataStorage '%s'." % self.dm.data_storage_name)
        r = self.sd_api.getStorageDomainInfo(self.dm.data_storage_name)
        if r['status_code'] == self.dm.expected_statsu_code_get_sd_info:
            dictCompare = DictCompare()
            d1 = self.dm.xml_data_storage_info
            del d1['storage_domain']['host']
            d2 = r['result']
            if dictCompare.isSubsetDict(d1, d2):
                LogPrint().info("PASS: Get DataStorage '%s' info SUCCESS." % self.dm.data_storage_name)
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
        '''
        pass

class ITC0401030101_CreateNfsSd_Normal(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-03创建-01NFS-01正常创建
    @note: 包括Data/ISO/Export三种类型存储域（Unattached状态，不附加到任何数据中心）
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
        @BaseTestCase.drive_data(self, self.dm.data1_info_xml)
        def do_test(xml_info):
            dictCompare = DictCompare()
            d1 = xmltodict.parse(xml_info)
            LogPrint().info("Test: Start creating Data/ISO/Export DataStorages '%s' with NFS type." % d1['storage_domain']['name'])
            r = self.sd_api.createStorageDomain(xml_info)
            if r['status_code'] == self.dm.expected_status_code_create_sd:
                del d1['storage_domain']['host']
                if dictCompare.isSubsetDict(d1, r['result']):
                    LogPrint().info("PASS: Create NFS type StorageDomain '%s' SUCCESS." % d1['storage_domain']['name'])
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Created StorageDomain's info are INCORRECT.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' is INCORRECT when creating new DataStorage." % r['status_code'])
                self.flag = False
            self.assertTrue(self.flag)
        do_test()
            
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的游离存储
        '''
        for sd_name in self.dm.data1_name:
            self.assertTrue(smart_del_storage_domain(sd_name, self.dm.xml_del_sd_option))

class ITC0401030102_CreateNfsSd_DupName(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-03创建-01NFS-02重名
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        @note: 前提是已经存在一个存储域（在模块级测试环境中已经有一个存储域了）
        @todo: 涉及到存储连接的问题，此用例暂时不要运行。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        self.sd_api = StorageDomainAPIs()
        
    def test_CreateNfsSd_DupName(self):
        '''
        @summary: 测试步骤
        @note: （1）创建一个同名的存储域sd2
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        LogPrint().info("Test: Create a StorageDomain with Dup name '%s'." % self.dm.data1_name)
        r = self.sd_api.createStorageDomain(self.dm.data1_info_xml)
        print xmltodict.unparse(r['result'], pretty=True)
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
        pass

class ITC0401030103_CreateNfsSd_NameVerify(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-03创建-01NFS-03名称有效性验证
    @todo: 未完成，涉及到存储连接无法删除的问题。
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

class ITC0401030106_CreateNfsSd_NoRequiredParams(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-03创建-01NFS-06缺少必需项
    @todo: 存在storage connection的问题，该用例暂时无法正常运行。
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateNfsSd_NoRequiredParams(self):
        '''
        @summary: 测试步骤
        @note: （1）必填项包括name/type/host/storage(type/address/path)；
        @note: （2）分别验证缺少必填项时接口返回的状态码、提示信息是否正确。
        '''
        sd_api = StorageDomainAPIs()
        self.index = 0
        LogPrint().info("Test: Verify the returned status code and messages while creating data storage without required parameters.")
        @BaseTestCase.drive_data(self, self.dm.xml_sd_info_list)
        def do_test(xml_info):
            r = sd_api.createStorageDomain(xml_info)
#             print r['status_code']
#             print xmltodict.unparse(r['result'], pretty=True)
            if r['status_code'] == self.dm.expected_return_info_list[self.index][0]:
                if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_return_info_list[self.index][1]), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT while creating data storage without required parameters.")
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned messages are INCORRECT.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' INCORRECT." % r['status_code'])
                self.flag = False
            self.index += 1
            self.assertTrue(self.flag)
        do_test()
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        self.assertTrue(smart_del_storage_domain(self.dm.sd_name, self.dm.xml_del_sd_option))
            
class ITC0401030201_CreateIscsiSd_Normal(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-03创建-02ISCSI-01正常创建
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateIscsiSd_Normal(self):
        '''
        @summary: 测试步骤
        @note: （1）创建一个ISCSI类型的Data存储域；
        @note: （2）操作成功，验证接口返回的状态码、存储域信息是否正确。
        '''
        sd_api = StorageDomainAPIs()
        r = sd_api.createStorageDomain(self.dm.data1_info_xml)
        if r['status_code'] == self.dm.expected_status_code_create_sd:
            d1 = xmltodict.parse(self.dm.data1_info_xml)
            del d1['storage_domain']['host']
            del d1['storage_domain']['storage']['override_luns']
            d2 = deepcopy(r['result'])
            del d2['storage_domain']['storage']['volume_group']
            d2['storage_domain']['storage']['logical_unit'] = r['result']['storage_domain']['storage']['volume_group']['logical_unit']
            if DictCompare().isSubsetDict(d1, d2):
                LogPrint().info("PASS: Create ISCSI storage '%s' SUCCESS." % self.dm.data1_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Create ISCSI storage '%s' FAILED. Returned sd info INCORRECT." % self.dm.data1_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' INCORRECT while creating ISCSI DataStorage." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理，删除创建的ISCSI存储域。
        '''
        self.assertTrue(smart_del_storage_domain(self.dm.data1_name, self.dm.xml_del_sd_option))

class ITC0401040102_EditNfsSd_Unattached(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-04编辑-01NFS-02Unattached状态无法编辑
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个data类型存储域data1
        self.sd_api = StorageDomainAPIs()
        LogPrint().info("Pre-Test: Create a new NFS Data Storage '%s'." % self.dm.data_name)
        self.assertTrue(smart_create_storage_domain(self.dm.data_name, self.dm.xml_data_info))
        
    def test_EditNfsSd_Normal(self):
        '''
        @summary: 测试步骤
        @note: （1）编辑存储域的名称；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        r = self.sd_api.updateStorageDomain(self.dm.data_name, self.dm.xml_data_info_new)
        if r['status_code'] == self.dm.expected_status_code_edit_sd_unattached:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_edit_sd_unattached), r['result']):
                LogPrint().info("PASS: Returned status code and messages are INCORRECT while edit storage domain in 'unattached' state.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT while edit storage domain in 'unattached' state.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' are INCORRECT while edit storage domain in 'unattached' state." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理，删除创建的存储域。
        '''
        for sd_name in [self.dm.data_name, self.dm.data_name_new]:
            self.assertTrue(smart_del_storage_domain(sd_name, self.dm.xml_del_sd_option))

class ITC0401050101_DelNfsSd_Unattached(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-05删除-01NFS-01Unattached状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个NFS类型的Data Storage，处于Unattached状态。
        self.sd_api = StorageDomainAPIs()
        LogPrint().info("Pre-Test: Create a new NFS Data Storage '%s'." % self.dm.data_name)
        self.assertTrue(smart_create_storage_domain(self.dm.data_name, self.dm.xml_data_info))
        
    def test_DelNfsSd_Unattached(self):
        '''
        @summary: 测试步骤
        @note: （1）删除处于Unattached状态的NFS类型Data存储域；
        @note: （2）操作成功，验证接口返回状态码、相关信息是否正确。
        '''
        r = self.sd_api.delStorageDomain(self.dm.data_name, self.dm.xml_del_sd_option)
        if r['status_code'] == self.dm.expected_status_code_del_sd:
            if not self.sd_api.searchStorageDomainByName(self.dm.data_name)['result']['storage_domains']:
                LogPrint().info("PASS: Delete unattached Storage Domain '%s' SUCCESS." % self.dm.data_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: The deleted Storage Domain '%s' still exists." % self.dm.data_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' INCORRECT while deleting Storage Domain '%s'." % (r['status_code'], self.dm.data_name))
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        self.assertTrue(smart_del_storage_domain(self.dm.data_name, self.dm.xml_del_sd_option))

class ITC0401050201_DelIscsiSd_Unattached(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-05删除-02ISCSI-01Unattached状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个NFS类型的Data Storage，处于Unattached状态。
        self.sd_api = StorageDomainAPIs()
        LogPrint().info("Pre-Test: Create a new ISCSI Data Storage '%s'." % self.dm.data_name)
        self.assertTrue(smart_create_storage_domain(self.dm.data_name, self.dm.xml_data_info))
        
    def test_DelIscsiSd_Unattached(self):
        '''
        @summary: 测试步骤
        @note: （1）删除处于Unattached状态的ISCSI类型Data存储域；
        @note: （2）操作成功，验证接口返回状态码、相关信息是否正确。
        '''
        r = self.sd_api.delStorageDomain(self.dm.data_name, self.dm.xml_del_sd_option)
        if r['status_code'] == self.dm.expected_status_code_del_sd:
            if not self.sd_api.searchStorageDomainByName(self.dm.data_name)['result']['storage_domains']:
                LogPrint().info("PASS: Delete unattached Storage Domain '%s' SUCCESS." % self.dm.data_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: The deleted Storage Domain '%s' still exists." % self.dm.data_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' INCORRECT while deleting Storage Domain '%s'." % (r['status_code'], self.dm.data_name))
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        self.assertTrue(smart_del_storage_domain(self.dm.data_name, self.dm.xml_del_sd_option))

class ITC04010601_DestroySd_Unattached(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-06销毁-01Unattached状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        self.sd_api = StorageDomainAPIs()
        
        # 前提1：创建一个ISO存储域（Unattached状态）
        LogPrint().info("Pre-Test: Create a ISO storage domain '%s' for test." % self.dm.iso_name)
        self.assertTrue(smart_create_storage_domain(self.dm.iso_name, self.dm.xml_iso_info))
        
    def test_DestroySd_Unattached(self):
        '''
        @summary: 测试步骤
        @note: （1）对Unattached状态的ISO存储域进行销毁操作；
        @note: （2）操作成功，验证接口返回的状态码、提示信息是否正确。
        '''
        # 对ISO存储域进行Destroy操作（通过在删除项中设置destroy参数实现）
        LogPrint().info("Test: Destroy the ISO storage domain '%s'." % self.dm.iso_name)
        r = self.sd_api.delStorageDomain(self.dm.iso_name, self.dm.xml_destroy_iso_option)
        if r['status_code'] == self.dm.expected_status_code_destroy_sd:
            if not self.sd_api.searchStorageDomainByName(self.dm.iso_name)['result']['storage_domains']:
                LogPrint().info("PASS: Destroy the ISO storage domain '%s' SUCCESS." % self.dm.iso_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: The ISO storage domain '%s' still exists after destroyed." % self.dm.iso_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT while destroying a storage domain." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）导入被销毁的存储域；
        @note: （2）删除该存储域（被销毁的存储域，只有在导入之后删除才能被再次被创建）。
        '''
        # Post-Test-1：导入被销毁的存储域
        LogPrint().info("Post-Test-1: Import the destroyed storage domain '%s' for deleting." % self.dm.iso_name)
        r = self.sd_api.importStorageDomain(self.dm.xml_import_iso_info)
        self.assertTrue(r['status_code']==self.dm.expected_status_code_import_sd)
        
        # Post-Test-2：删除该存储域（以便后续重复使用该存储创建存储域）
        LogPrint().info("Post-Test-2: Delete the imported storage domain '%s' for reusing." % self.dm.iso_name)
        r = self.sd_api.delStorageDomain(self.dm.iso_name, self.dm.xml_del_iso_option)
        self.assertTrue(r['status_code']==self.dm.expected_status_code_del_sd)

class ITC04010701_ImportSd_Unattached(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-01存储域操作-07导入-01ISO域
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        self.sd_api = StorageDomainAPIs()
        
        # 前提1：创建一个ISO存储域（Unattached状态）
        LogPrint().info("Pre-Test-1: Create a ISO storage domain '%s' for import test." % self.dm.iso_name)
        self.assertTrue(smart_create_storage_domain(self.dm.iso_name, self.dm.xml_iso_info))
        
        # 前提2：销毁（destroy）该ISO存储域
        LogPrint().info("Pre-Test-2: Destroy the ISO storage domain '%s' for import test." % self.dm.iso_name)
        r = self.sd_api.delStorageDomain(self.dm.iso_name, self.dm.xml_destroy_iso_option)
        self.assertTrue(r['status_code'] == self.dm.expected_status_code_del_sd)
        
    def test_DestroySd_Unattached(self):
        '''
        @summary: 测试步骤
        @note: （1）导入一个已被销毁的ISO存储域；
        @note: （2）操作成功，验证接口返回的状态码、提示信息是否正确。
        '''
        # 对ISO存储域进行Destroy操作（通过在删除项中设置destroy参数实现）
        LogPrint().info("Test: Import the destroyed ISO storage domain '%s'." % self.dm.iso_name)
        r = self.sd_api.importStorageDomain(self.dm.xml_import_iso_info)
        if r['status_code'] == self.dm.expected_status_code_import_sd:
            if self.sd_api.searchStorageDomainByName(self.dm.iso_name)['result']['storage_domains']:
                LogPrint().info("PASS: Import the destroyed ISO storage domain '%s' SUCCESS." % self.dm.iso_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: The storage domain '%s' does not exist after importing." % self.dm.iso_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT while importing a destroyed storage domain." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除该存储域（被销毁的存储域，只有在导入之后删除才能被再次被创建）。
        '''      
        # Post-Test：删除该存储域（以便后续重复使用该存储创建存储域）
        LogPrint().info("Post-Test: Delete the imported storage domain '%s' for reusing later." % self.dm.iso_name)
        r = self.sd_api.delStorageDomain(self.dm.iso_name, self.dm.xml_del_iso_option)
        self.assertTrue(r['status_code']==self.dm.expected_status_code_del_sd)

class ITC040201_GetDisksFromDataStorage(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-02Data域磁盘管理-01查看磁盘列表
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：在Data存储域中创建一个磁盘
        r = smart_create_disk(self.dm.xml_disk_info)
        self.assertTrue(r[0])
        self.disk_id = r[1]
        
    def test_GetDisksFromDataStorage(self):
        '''
        @summary: 测试步骤
        @note: （1）调用相应接口，获取Data存储域中的disk列表；
        @note: （2）操作成功，验证接口返回的状态码、disk列表是否正确。
        '''
        self.data_storage_api = DataStorageAPIs()
        LogPrint().info("Test: Get disks list of Data Storage '%s'." % self.dm.data1_name)
        r = self.data_storage_api.getDisksListFromDataStorage(self.dm.data1_name)
        if r['status_code'] == self.dm.expected_status_code_get_disk_list_in_data_storage:
            LogPrint().info("PASS: Get the disks list from Data Storage '%s' SUCCESS." % self.dm.data1_name)
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的磁盘；
        '''
        LogPrint().info("Post-Test: Delete disk '%s' from data storage '%s'." % (self.dm.disk_name, self.dm.data1_name))
        self.assertTrue(smart_delete_disk(self.disk_id, self.dm.xml_del_disk_option))

class ITC040202_GetDiskInfoFromDataStorage(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-02Data域磁盘管理-02查看磁盘详细信息
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：在存储域中创建一个磁盘
        r = smart_create_disk(self.dm.xml_disk_info)
        self.assertTrue(r[0])
        self.disk_id = r[1]
    
    def test_GetDiskInfoFromDataStorage(self):
        '''
        @summary: 测试步骤
        @note: （1）查询指定存储域中磁盘信息；
        @note: （2）操作成功，验证接口返回的状态码、磁盘信息是否正确。
        '''
        ds_api = DataStorageAPIs()
        LogPrint().info("Test: Get disk '%s' info from the data storage '%s'." % (self.dm.disk_name, self.dm.data1_name))
        r = ds_api.getDiskInfoFromDataStorage(self.dm.data1_name, self.disk_id)
        if r['status_code'] == self.dm.expected_status_code_get_disk_info:
            d1 = xmltodict.parse(self.dm.xml_disk_info)
            if DictCompare().isSubsetDict(d1, r['result']):
                LogPrint().info("PASS: Get disk '%s' info from the data storage '%s' SUCCESS." % (self.dm.disk_name, self.dm.data1_name))
                self.flag = True
            else:
                LogPrint().error("FAIL: Get disk info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' INCORRECT while get disk info from data storage." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的磁盘
        '''
        self.assertTrue(smart_delete_disk(self.disk_id, self.dm.xml_del_disk_option))

class ITC04020301_DelDiskFromDataStorage_OK(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-02Data域磁盘管理-03删除存储域中的磁盘-01OK状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：在Active状态的存储域中创建一个磁盘
        r = smart_create_disk(self.dm.xml_disk_info, disk_alias=self.dm.disk_name)
        self.assertTrue(r[0])
        self.disk_id = r[1]
        
    def test_DelDiskFromDataStorage_OK(self):
        '''
        @summary: 测试步骤
        @note: （1）调用相应接口，删除创建的磁盘；
        @note: （2）操作成功，验证接口返回的状态码、相关信息是否正确。
        '''
        ds_api = DataStorageAPIs()
        disk_api = DiskAPIs()
        r = ds_api.delDiskFromDataStorage(self.dm.data1_name, disk_id=self.disk_id)
        if r['status_code']==self.dm.expected_status_code_del_disk:
            try:
                disk_api.getDiskInfo(self.disk_id)
                LogPrint().error("FAIL: Delete disk FAILED, still exist.")
                self.flag = False
            except:
                LogPrint().info("PASS: Delete disk '%s' from Data Storage '%s' SUCCESS." %(self.dm.disk_name, self.dm.data1_name))
                self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG while deleting disk." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除磁盘（如果存在的话）
        '''
        self.assertTrue(smart_delete_disk(self.disk_id))

class ITC040301_GetFilesFromIsoStorage(BaseTestCase):
    '''
    @summary: ITC-04存储域管理-03ISO域文件管理-01查看ISO域文件列表
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
    def test_GetFilesFromIsoStorage(self):
        '''
        @summary: 测试步骤
        @note: （1）调用相关接口，获得ISO域中所有文件列表；
        @note: （2）操作成功，验证接口返回的状态码、相关信息是否正确。
        '''
        iso_api = ISOStorageAPIs()
        LogPrint().info("Test: Get files list from ISO Storage '%s'." % self.dm.iso_storage_name)
        r = iso_api.getFilesListFromISOStorage(self.dm.iso_storage_name)
        if r['status_code'] == self.dm.expected_status_code_get_files_from_IsoStorage:
            LogPrint().info("PASS: Get files list SUCCESS from ISO Storage '%s'." % self.dm.iso_storage_name)
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' is Wrong while gettig files list from ISO Storage '%s'." % (r['status_code'], self.dm.iso_storage_name))
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass

if __name__ == "__main__":
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["StorageDomain.ITC040301_GetFilesFromIsoStorage"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)

#     fileName = r"d:\result.html"
#     fp = file(fileName, 'wb')
#     runner = HTMLTestRunner(stream=fp, title=u"测试结果", description=u"测试报告")
#     runner.run(testSuite)