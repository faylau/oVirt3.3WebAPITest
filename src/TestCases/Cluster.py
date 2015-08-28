#encoding:utf-8
from __builtin__ import True


__authors__ = ['"wei keke" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/26          初始版本                                                            wei keke 
#---------------------------------------------------------------------------------
'''

import unittest

from BaseTestCase import BaseTestCase
from TestAPIs.DataCenterAPIs import DataCenterAPIs,smart_attach_storage_domain, smart_deactive_storage_domain, smart_detach_storage_domain
from TestAPIs.ClusterAPIs import ClusterAPIs, AffinityGroupsAPIs, smart_create_cluster, smart_delete_cluster, \
smart_create_affinitygroups, smart_delete_affinitygroups
from TestAPIs.StorageDomainAPIs import smart_create_storage_domain, smart_del_storage_domain
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs, smart_del_vm
from TestAPIs.NetworkAPIs import smart_create_network, smart_delete_network
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from TestData.Cluster import ITC02_Setup as ModuleData
from TestAPIs.HostAPIs import smart_create_host,smart_del_host

import xmltodict


class ITC02_Setup(BaseTestCase):
    '''
    @summary: 集群管理模块级测试用例，初始化模块测试环境；
    @note: （1）创建一个数据中心；
    @note: （2）创建一个集群；
    @note: （3）创建一个主机，并等待其变为UP状态；
    @note: （4）创建4个存储域（data1/data2/Export/ISO）；
    @note: （5）将 4个存储域都附加到数据中心；
    @note: （6）创建2个虚拟机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
         
    def test_CreateModuleTestEnv(self):
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
         
        # 创建1个数据中心
        LogPrint().info("Pre-Module-Test-1: Create DataCenter '%s'." % self.dm.dc_name)
        self.assertTrue(dcapi.createDataCenter(self.dm.dc_info)['status_code']==self.dm.expected_status_code_create_dc)
      
        # 创建1个集群
        LogPrint().info("Pre-Module-Test-2: Create Cluster '%s' in DataCenter '%s'." % (self.dm.cluster_name, self.dm.dc_name))
        self.assertTrue(capi.createCluster(self.dm.cluster_info)['status_code']==self.dm.expected_status_code_create_cluster)
      
        # 在数据中心中创建一个主机，并等待主机UP。
        LogPrint().info("Pre-Module-Test-3: Create Host '%s' in Cluster '%s'." % (self.dm.host1_name, self.dm.cluster_name))
        self.assertTrue(smart_create_host(self.dm.host1_name, self.dm.host_info))
     
        # 为数据中心创建Data（data1/data2/export/iso）。
        @BaseTestCase.drive_data(self, self.dm.storage_info)
        def create_storage_domains(xml_storage_domain_info):
            sd_name = xmltodict.parse(xml_storage_domain_info)['storage_domain']['name']
            LogPrint().info("Pre-Module-Test-4: Create Data Storage '%s'." % sd_name)
            self.assertTrue(smart_create_storage_domain(sd_name, xml_storage_domain_info))
        create_storage_domains()
         
        # 将创建的的data1、data2和export、iso域附加到NFS/ISCSI数据中心里。
        LogPrint().info("Pre-Module-Test-5: Attach the storages to data centers.")
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_name, self.dm.data1_nfs_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_name, self.dm.data2_nfs_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_name, self.dm.export1_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_name, self.dm.iso1_name))
        
        #创建2个虚拟机
        LogPrint().info("Pre-Module-Test-6: Create two vms.")
        self.vmapi = VirtualMachineAPIs()
        r1 = self.vmapi.createVm(self.dm.vm1_info)
        if r1['status_code'] == 201:
            self.vm_name = r1['result']['vm']['name']
        else:
            LogPrint().error("Create vm failed.Status-code is WRONG.")
            self.assertTrue(False)
        r2 = self.vmapi.createVm(self.dm.vm2_info)
        if r2['status_code'] == 201:
            self.vm_name = r2['result']['vm']['name']
        else:
            LogPrint().error("Create vm failed.Status-code is WRONG.")
            self.assertTrue(False)

            
class ITC020101_GetClustersList(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01基本操作-01获取集群列表
    '''
    def test_GetClustersList(self):
        '''
        @summary: 测试步骤
        @note: （1）获取全部集群列表；
        @note: （2）验证接口返回的状态码是否正确。
        '''
        clusterapi = ClusterAPIs()
        LogPrint().info("Test: Get all clusters list.")
        r = clusterapi.getClustersList()
        if r['status_code']==200:
            LogPrint().info('PASS: Get Clusters list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error('FAIL: Get Clusters list FAIL. Returned status code "%s" is WRONG.' % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
class ITC020102_GetClusterInfo(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-02获取指定集群信息
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1： 创建一个集群
        LogPrint().info("Pre-Test: Create a cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
    def test_GetClusterInfo(self):
        '''
        @summary: 测试用例执行步骤
        @note: （1）获取指定集群的信息；
        @note: （2）验证接口返回的状态码、集群信息是否正确。
        '''
        # 测试1：获取集群的信息，并与期望结果进行对比
        self.clusterapi = ClusterAPIs()
        LogPrint().info("Test: Get cluster's ('%s') info." % self.dm.cluster_name)
        r = self.clusterapi.getClusterInfo(self.dm.cluster_name)
        if r['status_code']==self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.cluster_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Get Cluster '%s' info SUCCESS." % self.dm.cluster_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Get Cluster '%s' info INCORRECT." % self.dm.cluster_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Get Cluster '%s' info FAILED. Returned status code '%s' is WRONG." % (self.dm.cluster_name, r['status_code']))
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test: Delete cluster '%s'." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))
    
class ITC02010301_CreateCluster(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-03创建一个集群-01创建成功
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        self.clusterapi = ClusterAPIs()
        
    def test_CreateCluster(self):
        '''
        @summary: 测试步骤
        @note: （1）创建一个集群；
        @note: （2）操作成功，验证接口返回的状态码、集群信息是否正确。
        '''
        LogPrint().info("Test: Create a cluster '%s'." % self.dm.cluster_name)
        r = self.clusterapi.createCluster(self.dm.cluster_info)
        if r['status_code'] == self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.cluster_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Create Cluster '%s' SUCCESS." % self.dm.cluster_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Create Cluster '%s'  INCORRECT." % self.dm.cluster_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test: Delete cluster '%s'." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))
               
class ITC02010302_CreateCluster_Dup(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-03创建一个集群-02重名
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a cluster %s"%self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
    def test_CreateCluster_Dup(self):
        '''
        @summary: 测试步骤
        @note: （1）创建一个重名的Cluster；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        clusterapi = ClusterAPIs()
        LogPrint().info("Test: Create a cluster with dup name.")
        r = clusterapi.createCluster(self.dm.cluster_info)
        print r
        if r['status_code'] == self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.error_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Returned status code and info are CORRECT while creating cluster with dup name.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned info are INCORRECT while creating cluster with dup name.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG. " % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test: Delete cluster '%s'." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))

class ITC02010303_CreateClusterNoRequired(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-03创建一个集群-03缺少必填参数
    @note: 集群名称、所在数据中心和cpu类型是必填项，验证接口返回码和提示信息
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateClusterNoRequired(self):
        '''
        @summary: 测试步骤
        @note: （1）创建一个集群，缺少必填参数；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        clusterapi = ClusterAPIs()
        self.expected_result_index = 0
        # 使用数据驱动，根据测试数据文件循环创建多个数据中心
        @BaseTestCase.drive_data(self, self.dm.cluster_info)
        def do_test(xml_info):
            self.flag = True
            r = clusterapi.createCluster(xml_info)
            if r['status_code']==self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.expected_result_index]), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT.")
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
        @summary: 无需清理
        '''
        pass
        
class ITC02010401_UpdateCluster_nohost(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-04编辑集群-01集群内无主机
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个集群
        LogPrint().info("Pre-Test: Create cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
    def test_UpdateCluster(self):
        '''
        @summary: 测试步骤
        '''
        clusterapi = ClusterAPIs()
        self.expected_result_index = 0
        # 使用数据驱动，根据测试数据文件循环创建多个数据中心
        @BaseTestCase.drive_data(self, self.dm.cluster_info_new)
        def do_test(xml_info):
            self.flag = True
            r = clusterapi.updateCluster(self.dm.cluster_name, xml_info)
            if r['status_code'] == self.dm.status_code:
                dict_actual = r['result']
                dict_expected = xmltodict.parse(xml_info)
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(dict_expected, dict_actual):
                    LogPrint().info("PASS: ITC02010401_UpdateCluster_nohost SUCCESS." )
                    self.flag = True
                else:
                    LogPrint().error("FAIL: ITC02010401_UpdateCluster_nohost.Error-info  INCORRECT.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: ITC02010401_UpdateCluster_nohost FAILED.Status-code WRONG. " )
                self.flag = False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test: Delete cluster '%s'." % self.dm.cluster_name_new)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name_new))

class ITC0201040201_UpdateCluster_host_cputype(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-04编辑集群-02集群内有主机-01更改集群的cpu类型
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        # 前提1：创建一个集群
        LogPrint().info("Pre-Test-1: Create cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # 前提2：创建一个主机
        LogPrint().info("Pre-Test-2: Create host '%s' for this TC." % self.dm.host_name)
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.host_info))
        
    def test_UpdateCluster_host(self):
        '''
        @summary: 测试步骤
        @note: （1）更改含有主机的集群CPU类型；
        @note: （2）操作成功，验证接口返回的状态码、相关信息是否正确。
        '''
        clusterapi = ClusterAPIs()
        LogPrint().info("Test: Edit cluster's cpu type if there are hosts in this cluster.")
        r = clusterapi.updateCluster(self.dm.cluster_name, self.dm.cluster_info_new)
        if r['status_code'] == self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.expected_info)
            print dict_actual
            print dict_expected
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: ITC0201040201_test_UpdateCluster_host_cputype SUCCESS." )
                self.flag = True
            else:
                LogPrint().error("FAIL: ITC0201040201_test_UpdateCluster_host_cputype .Error-info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test-1: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name,self.dm.host_del_option))
        LogPrint().info("Post-Test-2: Delete cluster '%s'." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))

class ITC0201040202_UpdateCluster_host_upcpu(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-04编辑集群-02集群内有主机-02升高cpu级别
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        # 前提1：创建一个集群
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # 前提2：创建一个主机
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.host_info))
        
    def test_UpdateCluster_host(self):
        '''
        @summary: 测试步骤
        @note: （1）
        @note: （2）
        '''
        clusterapi = ClusterAPIs()
        LogPrint().info("Test: Improve cluster's CPU level while there are hosts in cluster.")
        r = clusterapi.updateCluster(self.dm.cluster_name, self.dm.cluster_info_new)
        if r['status_code'] == self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.expected_info)
            print dict_actual
            print dict_expected
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: ITC0201040202_test_UpdateCluster_host_upcpu SUCCESS." )
                self.flag = True
            else:
                LogPrint().error("FAIL: ITC0201040202_test_UpdateCluster_host_upcpu. Error-info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned tatus_code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test-1: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name,self.dm.host_del_option))
        LogPrint().info("Post-Test-2: Delete cluster '%s'." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))

class ITC0201040203_UpdateCluster_host_name(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-04编辑集群-02集群内有主机-03更改名称
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
        # 前提1：首先创建一个集群
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # 前提2：创建一个主机
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.host_info))
        
    def test_UpdateCluster_host(self):
        '''
        @summary: 测试步骤
        @note: （1）
        @note: （2）
        '''
        clusterapi = ClusterAPIs()
        LogPrint().info("Test: Edit cluster's name while there are hosts in cluster.")
        r = clusterapi.updateCluster(self.dm.cluster_name, self.dm.cluster_info_new)
        if r['status_code'] == self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.cluster_info_new)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: ITC0201040203_test_UpdateCluster_host_name SUCCESS." )
                self.flag = True
            else:
                LogPrint().error("FAIL: ITC0201040203_test_UpdateCluster_host_name. Error-info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: ITC0201040203_test_UpdateCluster_host_name.Status_code is wrong. ")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test-1: Delete host '%s'." % self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name,self.dm.host_del_option))
        LogPrint().info("Post-Test-2: Delete cluster '%s'." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name_new))

class ITC02010501_DeleteCluster_clear(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-05删除集群-01干净集群
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        
        # 准备1：创建一个集群
        LogPrint().info("Pre-Test: Create a cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
    def test_DeleteCluster(self):
        '''
        @summary: 测试用例执行步骤
        @note: （1）删除一个干净的集群；
        @note: （2）操作成功，验证接口返回的状态码是否正确，验证被删除的集群不再存在。
        '''
        clusterapi = ClusterAPIs()
        # 测试1：获取集群的信息，并与期望结果进行对比
        LogPrint().info("Test: Delete the clean cluster '%s'." % self.dm.cluster_name)
        r = clusterapi.delCluster(self.dm.cluster_name)
        if r['status_code'] == self.dm.status_code:
#             print self.clusterapi.searchClusterByName(self.dm.cluster_name)['result']['clusters']
            if not clusterapi.searchClusterByName(self.dm.cluster_name)['result']['clusters']:
                LogPrint().info("PASS: Delete Cluster '%s' info SUCCESS." % self.dm.cluster_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: The Cluster '%s' is still exist ." % self.dm.cluster_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test: Delete cluster '%s'." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))
        
class ITC02010502_DeleteCluster_host(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-05删除集群-02集群内有主机
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        # 前提1：创建一个集群
        LogPrint().info("Pre-Test-1: Create cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # 前提2：创建一个主机
        LogPrint().info("Pre-Test-2: Create host '%s' for this TC." % self.dm.host_name)
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.host_info))
        
    def test_DeleteCluster_host(self):
        '''
        @summary: 测试用例执行步骤
        @note: （1）删除包含主机的集群
        @note: （2）操作失败，验证返回状态码，验证报错信息
        '''
        clusterapi = ClusterAPIs()
        LogPrint().info("Test: Delete cluster %s."% self.dm.cluster_name)
        r = clusterapi.delCluster(self.dm.cluster_name)
#         print r
        if r['status_code'] == self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.expected_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Returned status code and messages are CORRECT." )
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned message is  INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is wrong. ")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test-1: Delete host %s. "% self.dm.host_name)
        self.assertTrue(smart_del_host(self.dm.host_name, self.dm.host_del_option))
        LogPrint().info("Post-Test-2: Delete cluster %s. " % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name)) 
              
class ITC020201_GetClusterNetworkList(BaseTestCase):
    '''
    @summary: ITC-02集群管理-02集群网络基本操作-01获取集群网络列表
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        
        # 准备1：创建一个集群
        LogPrint().info("Pre-Test-1: Create cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
    def test_GetClusterNetworkList(self):
        '''
        @summary: 测试用例执行步骤
        @note: （1）获取集群的网络列表
        @note: （2）操作成功，验证返回状态码
        '''
        clusterapi = ClusterAPIs()
        LogPrint().info("Test: Get the cluster %s's network list. "% self.dm.cluster_name)
        r = clusterapi.getClusterNetworkList(self.dm.cluster_name)
        if r['status_code'] == self.dm.status_code:
            LogPrint().info('PASS: Get Cluster %s Network list SUCCESS.'% self.dm.cluster_name)
            self.flag = True
        else:
            LogPrint().error('FAIL: Get Cluster %s Network list FAIL.'% self.dm.cluster_name)
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test-1: Delete cluster %s. "% self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))
            
class ITC020202_GetClusterNetworkInfo(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-02获取指定集群的网络信息
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        # step1:创建一个集群
        LogPrint().info("Pre-Test-1: Create cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # step2：创建一个逻辑网络
        LogPrint().info("Pre-Test-2: Create network '%s' for this TC." % self.dm.nw_name)
        self.assertTrue(smart_create_network(self.dm.nw_info, self.dm.nw_name))
        # step3:附加该网络到集群上
        LogPrint().info("Pre-Test-3: Attach network '%s'to cluster '%s' for this TC." % (self.dm.nw_name, self.dm.cluster_name))
        self.clusterapi = ClusterAPIs()
        self.clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        
    def test_GetClusterNetworkInfo(self):
        '''
        @summary: 测试用例执行步骤
        @note: 操作成功，验证网络信息
        '''
        LogPrint().info("Test: Get the cluster %s's network info. "% self.dm.cluster_name)
        r= self.clusterapi.getClusterNetworkInfo(self.dm.cluster_name, self.dm.nw_name)
        dict_actual = r
        dict_expected = xmltodict.parse(self.dm.nw_info)
        dictCompare = DictCompare()
        if dictCompare.isSubsetDict(dict_expected, dict_actual):
            LogPrint().info("PASS: Get ClusterNetwork '%s' info SUCCESS." % self.dm.nw_name)
#                 return True
        else:
            LogPrint().error("FAIL: Returned message is WRONG. ")
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test-1: Delete network '%s' for this TC." % self.dm.nw_name)
        self.assertTrue(smart_delete_network(self.dm.nw_name, self.dm.dc_name))
        LogPrint().info("Post-Test-2: Delete cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))
            
class ITC020203_attachNetworktoCluster(BaseTestCase):
    '''
    @summary: ITC-02集群管理-02集群网络操作-03将网络附加到集群
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        #step1:创建一个集群
        LogPrint().info("Pre-Test-1: Create cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        #step2：创建一个逻辑网络
        LogPrint().info("Pre-Test-2: Create network '%s' for this TC." % self.dm.nw_name)
        self.assertTrue(smart_create_network(self.dm.nw_info, self.dm.nw_name))
        
    def test_attachNetworktoCluster(self):
        '''
        @summary: 测试用例执行步骤
        @note: （1）测试将网络附加到集群
        @note: （2）操作成功，验证返回状态码，验证网络是否附加到集群
        '''
        LogPrint().info("Test: Attach Network %s to Cluster %s. "%(self.dm.nw_name, self.dm.cluster_name))
        clusterapi = ClusterAPIs()
        r = clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        print r
        if r['status_code'] == self.dm.status_code:
            cluster_id = r['result']['network']['cluster']['@id']
            cluster_name = clusterapi.getClusterNameById(cluster_id)
            if cluster_name == self.dm.cluster_name:
                LogPrint().info("PASS: Attach Network %s to Cluster %s SUCCESS." %(self.dm.nw_name, self.dm.cluster_name) )
#                 return True
            else:
                LogPrint().error("FAIL: Attach Network %s to Cluster %s FAIL."%(self.dm.nw_name, self.dm.cluster_name))
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is WRONG. ")
            self.flag = False
        self.assertTrue(self.flag)
             
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test-1: Delete network '%s' for this TC." % self.dm.nw_name)
        self.assertTrue(smart_delete_network(self.dm.nw_name, self.dm.dc_name))
        LogPrint().info("Post-Test-2: Delete cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))    

class ITC020204_detachNetworkFromCluster(BaseTestCase):
    '''
    @summary: ITC-02集群管理-02集群网络操作-04将网络从集群分离
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        # step1:创建一个集群
        LogPrint().info("Pre-Test-1: Create cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # step2：创建一个逻辑网络
        LogPrint().info("Pre-Test-2: Create network '%s' for this TC." % self.dm.nw_name)
        self.assertTrue(smart_create_network(self.dm.nw_info, self.dm.nw_name))
        # step3:附加该网络到集群上
        LogPrint().info("Pre-Test-3: Attach network '%s'to cluster '%s' for this TC." % (self.dm.nw_name, self.dm.cluster_name))
        self.clusterapi = ClusterAPIs()
        self.clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        
    def test_detachNetworkFromCluster(self):
        '''
        @summary: 测试用例执行步骤
        @note: 测试将网络从集群中分离
        @note: 操作成功，验证返回状态码，验证集群中是否有该网络
        '''
        LogPrint().info("Test: Detach Network %s from Cluster %s. "%(self.dm.nw_name, self.dm.cluster_name))
        r = self.clusterapi.detachNetworkFromCluster(self.dm.cluster_name, self.dm.nw_name)
        if r['status_code'] ==self.dm.status_code:
            #检查集群中网络是否存在
            if not self.clusterapi.getClusterNetworkInfo(self.dm.cluster_name, self.dm.nw_name):
                LogPrint().info("PASS: Detach Network %s from Cluster %s SUCCESS. "%(self.dm.nw_name, self.dm.cluster_name) )
            else:
                LogPrint().info("FAIL: Cluster %s still has Network %s. "%(self.dm.cluster_name, self.dm.nw_name)) 
        else:
            LogPrint().info("FAIL: Returned status code is WRONG.")
              
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test-1: Delete network '%s' for this TC." % self.dm.nw_name)
        self.assertTrue(smart_delete_network(self.dm.nw_name, self.dm.dc_name))
        LogPrint().info("Post-Test-2: Delete cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name)) 

class ITC020205_UpdateNetworkofCluster(BaseTestCase):
    '''
    @summary: ITC-02集群管理-02集群网络操作-05更新集群网络信息
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        # step1:创建一个集群
        LogPrint().info("Pre-Test-1: Create cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # step2：创建一个逻辑网络
        LogPrint().info("Pre-Test-2: Create network '%s' for this TC." % self.dm.nw_name)
        self.assertTrue(smart_create_network(self.dm.nw_info, self.dm.nw_name))
        # step3:附加该网络到集群上
        LogPrint().info("Pre-Test-3: Attach network '%s'to cluster '%s' for this TC." % (self.dm.nw_name, self.dm.cluster_name))
        self.clusterapi = ClusterAPIs()
        self.clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        
    def test_UpdateNetworkofCluster(self):
        '''
        @summary: 测试用例执行步骤
        @note: 更新集群网络信息
        @note: 操作成功，验证返回状态码，验证更新信息是否正确
        '''
        LogPrint().info("Test: Update Network %s of Cluster %s. "%(self.dm.nw_name, self.dm.cluster_name))
        r = self.clusterapi.updateNetworkOfCluster(self.dm.cluster_name, self.dm.nw_name, self.dm.nw_info_new)
        if r['status_code'] ==self.dm.status_code:
            dict_actual = self.clusterapi.getClusterNetworkInfo(self.dm.cluster_name, self.dm.nw_name)
            #dict_expected = {'network':xmltodict.parse(self.dm.nw_info_new)['network']}
            dict_expected = xmltodict.parse(self.dm.nw_info_new)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS: Detach Network %s from Cluster %s SUCCESS. "%(self.dm.nw_name, self.dm.cluster_name) )
            else:
                LogPrint().info("FAIL: Returned message is WRONG. ") 
        else:
            LogPrint().info("FAIL: Returned status code is WRONG." )
              
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test-1: Delete network '%s' for this TC." % self.dm.nw_name)
        self.assertTrue(smart_delete_network(self.dm.nw_name, self.dm.dc_name))
        LogPrint().info("Post-Test-2: Delete cluster '%s' for this TC." % self.dm.cluster_name)
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name)) 
        
class ITC020301_GetAffinityGroupsList(BaseTestCase):
    '''
    @summary: ITC-02集群管理-03亲和组-01查看亲和组列表
    '''
    def setUp(self):
        pass
    
    def test_GetAffinityGroupsList(self):
        '''
        @summary: 测试用例执行步骤
        @note: 获取亲和组列表
        @note: 验证接口返回状态码是否正确
        '''
        self.affinitygroups_api = AffinityGroupsAPIs()
        LogPrint().info("Test: Get AffinityGroups List of cluster %s." % ModuleData.cluster_name)
        r = self.affinitygroups_api.getAffinityGroupsList(ModuleData.cluster_name)
        if r['status_code']==200:
            LogPrint().info('PASS: Get AffinityGroups List Success.')
            self.flag = True
        else:
            LogPrint().error("FAIL: Get AffinityGroups List Fail.")
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        pass
    
class ITC020302_GetAffinityGroupsInfo(BaseTestCase):
    '''
    @summary: ITC-02集群管理-03亲和组-02查看指定亲和组信息
    '''
    def setUp(self):
        '''
        @summary: 测试环境初始化
        '''
        #调用父类方法，获取该用例对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        #创建一个亲和组
        LogPrint().info("Pre-Test-1: Create affinitygroups '%s' for this TC" % self.dm.group_name)
        self.assertTrue(smart_create_affinitygroups(ModuleData.cluster_name, self.dm.group_info, self.dm.group_name))
    
    def test_GetAffinityGroupsInfo(self):
        '''
        @summary: 测试用例执行步骤
        @note: 获取指定亲和组信息
        @note: 验证返回状态码及接口返回信息
        '''
        self.flag = True
        self.affinitygroups_api = AffinityGroupsAPIs()
        LogPrint().info("Test: Get %s info of %s" % (self.dm.group_name, ModuleData.cluster_name))
        r = self.affinitygroups_api.getAffinityGroupsInfo(ModuleData.cluster_name, self.dm.group_name)   
        if r['status_code'] == self.dm.status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.group_info), r['result']):
                LogPrint().info("PASS: Get AffinityGroups info success.")
            else:
                LogPrint().error("FAIL: Get AffinityGroups info fail. The info is wrong.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Get AffinityGroups info fail. The status_code is %s." % r['status_code'])
            print xmltodict.unparse(r['result'], pretty=True)
            self.flag = False
        self.assertTrue(self.flag)    
        
    def tearDown(self):
        '''
        @summary: 测试结束后资源清理
        '''
        LogPrint().info("Post-Test-1: Delete affinitygroups %s for this TC." % self.dm.group_name)
        self.assertTrue(smart_delete_affinitygroups(ModuleData.cluster_name, self.dm.group_name))
        
class ITC02030301_CreateAffinityGroups_novms(BaseTestCase):
    '''
    @summary: ITC-02集群管理-03亲和组-03创建亲和组-01不添加虚拟机
    '''
    def setUp(self):
        '''
        @summary: 测试环境初始化
        '''
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateAffinityGroups_twovms(self):
        '''
        @summary: 测试用例执行步骤
        @note: 创建一个亲和组，不添加虚拟机
        @note: 验证状态返回码及接口返回信息
        '''
        self.flag = True
        self.affinitygroups_api = AffinityGroupsAPIs()
        LogPrint().info("Test: Create affinitygroups without vms in cluster %s." % ModuleData.cluster_name)
        r = self.affinitygroups_api.createAffinityGroups(ModuleData.cluster_name, self.dm.group_info)
        if r['status_code'] == self.dm.status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.group_info), r['result']):
                LogPrint().info("PASS: Create affinitygroups %s success." % self.dm.group_name)
            else:
                LogPrint().error("FAIL: Create affinitygroups fail. The info is wrong" )
                self.flag = False
        else:
            LogPrint().error("FAIL: Create affinitygroups fail. The status_code is %s." % r['status_code'])
            self.flag = False
            print xmltodict.unparse(r['result'], pretty=True)
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后资源清理
        '''
        LogPrint().info("Post-Test-1: Delete affinitygroups %s for this TC." % self.dm.group_name)
        self.assertTrue(smart_delete_affinitygroups(ModuleData.cluster_name, self.dm.group_name))
        
class ITC02030302_CreateAffinityGroups_twovms(BaseTestCase):
    '''
    @summary: ITC-02集群管理-03亲和组-03创建亲和组-02添加两个虚拟机
    '''
    def setUp(self):
        '''
        @summary: 测试环境初始化
        '''
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateAffinityGroups_twovms(self):
        '''
        @summary: 测试用例执行步骤
        @note: 创建一个亲和组，添加两个虚拟机
        @note: 验证状态返回码
        '''
        self.flag = True
        self.affinitygroups_api = AffinityGroupsAPIs()
        LogPrint().info("Test: Create affinitygroups %s in cluster %s and add two vms." % (self.dm.group_name, ModuleData.cluster_name))
        r1 = self.affinitygroups_api.createAffinityGroups(ModuleData.cluster_name, self.dm.group_info)
        if r1['status_code'] == self.dm.status_code_creategroups:
            r2 = self.affinitygroups_api.addVmtoAffinityGroups(ModuleData.cluster_name, self.dm.group_name, ModuleData.vm1_name)
            if r2['status_code'] == self.dm.status_code_addvms:
                r3 = self.affinitygroups_api.addVmtoAffinityGroups(ModuleData.cluster_name, self.dm.group_name, ModuleData.vm2_name)
                if r3['status_code'] == self.dm.status_code_addvms:
                    LogPrint().info("PASS: Create affinitygroups and add two vms success.")
                else:
                    LogPrint().info("FAIL: Add vm2 to affinitygroups fail. The status_code is %s." % r3['status_code'])
                    self.flag = False
            else:
                LogPrint().info("FAIL: Add vm1 to affinitygroups fail. The status_code is %s." % r2['status_code'])
                self.flag = False
        else:
            LogPrint().info("FAIL: Create affinitygroups fail. The status_code is %s." % r1['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
           
    def tearDown(self):
        '''
        @summary: 测试结束后资源清理
        '''
        LogPrint().info("Post-Test-1: Delete affinitygroups %s for this TC." % self.dm.group_name)
        self.assertTrue(smart_delete_affinitygroups(ModuleData.cluster_name, self.dm.group_name))

class ITC02030401_UpdateAffinityGroups_groupinfo(BaseTestCase):
    '''
    @summary: ITC-02集群管理-03亲和组-04编辑亲和组-01编辑组信息
    '''
    def setUp(self):
        '''
        @summary: 测试环境初始化
        '''
        self.dm = super(self.__class__, self).setUp()
        #创建一个亲和组
        LogPrint().info("Pre-Test-1: Create affinitygroups %s in cluster %s for this TC." % (self.dm.group_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_affinitygroups(ModuleData.cluster_name, self.dm.group_info, self.dm.group_name))
        #添加一个虚拟机到亲和组
        self.affinitygroups_api = AffinityGroupsAPIs()
        LogPrint().info("Pre-Test-2: Add vm %s to affinitygroups %s." % (ModuleData.vm1_name, self.dm.group_name))
        self.affinitygroups_api.addVmtoAffinityGroups(ModuleData.cluster_name, self.dm.group_name, ModuleData.vm1_name)
    
    def test_UpdateAffinityGroups_groupinfo(self):
        '''
        @summary: 测试用例执行步骤
        @note: 编辑指定亲和组信息(名称、描述、极性、Enforcing)
        @note: 验证状态返回码及接口返回信息
        '''
        self.flag = True
        LogPrint().info("Test: Update affinitygroups %s info in cluster %s." % (self.dm.group_name, ModuleData.cluster_name))
        r = self.affinitygroups_api.updateAffinityGroups(ModuleData.cluster_name, self.dm.group_name, self.dm.update_info)
        if r['status_code'] == self.dm.status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.update_info), r['result']):
                LogPrint().info("PASS: Update affinitygroups info success.")
            else:
                LogPrint().error("FAIL: Update affinitygroups info fail. The info is wrong.")
                self.flag = False
                print xmltodict.unparse(r['result'], pretty=True)
        else:
            LogPrint().info("FAIL: Update affinitygroups info fail. The status_code is %s." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)       
        
    def tearDown(self):
        '''
        @summary: 测试结束后资源清理
        '''
        LogPrint().info("Post-Test-1: Delete affinitygroups %s for this TC." % self.dm.update_name)
        self.assertTrue(smart_delete_affinitygroups(ModuleData.cluster_name, self.dm.update_name))
        
class ITC02030402_UpdateAffinityGroups_vms(BaseTestCase):
    '''
    @summary: ITC-02集群管理-03亲和组-04编辑亲和组-02删除、增加亲和组中的虚拟机
    '''
    def setUp(self):
        '''
        @summary: 测试环境初始化
        '''
        self.dm = super(self.__class__, self).setUp()
        #创建一个亲和组
        LogPrint().info("Pre-Test-1: Create affinitygroups %s in cluster %s for this TC." % (self.dm.group_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_affinitygroups(ModuleData.cluster_name, self.dm.group_info, self.dm.group_name))
        #添加一个虚拟机到亲和组
        self.affinitygroups_api = AffinityGroupsAPIs()
        LogPrint().info("Pre-Test-2: Add vm %s to affinitygroups %s." % (ModuleData.vm1_name, self.dm.group_name))
        self.affinitygroups_api.addVmtoAffinityGroups(ModuleData.cluster_name, self.dm.group_name, ModuleData.vm1_name)
    
    def test_UpdateAffinityGroups_vms(self):
        '''
        @summary: 测试用例执行步骤
        @note: 删除亲和组中原有虚拟机，并添加新的虚拟机
        @note: 验证状态返回码
        '''
        self.flag = True
        LogPrint().info("Test: Update vms in affinitygroups %s." % self.dm.group_name)
        r1 = self.affinitygroups_api.removeVmfromAffinityGroups(ModuleData.cluster_name, self.dm.group_name, ModuleData.vm1_name)
        if r1['status_code'] == self.dm.status_code:
            r2 = self.affinitygroups_api.addVmtoAffinityGroups(ModuleData.cluster_name, self.dm.group_name, ModuleData.vm2_name)
            if r2['status_code'] == self.dm.status_code:
                LogPrint().info("PASS: Update vms in affinitygroups %s success." % self.dm.group_name)
            else:
                LogPrint().info("FAIL: Add vm %s to affinitygroups %s fail. The status_code is %s." % (ModuleData.vm2_name,self.dm.group_name,r2['status_code']))
                self.flag = False
        else:
            LogPrint().error("FAIL: Remove vm %s from affinitygroups %s fail. The status_code is %s." % (ModuleData.vm1_name,self.dm.group_name,r1['status_code']))
            self.flag = False 
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后资源清理
        '''
        LogPrint().info("Post-Test-1: Delete affinitygroups %s for this TC." % self.dm.group_name)
        self.assertTrue(smart_delete_affinitygroups(ModuleData.cluster_name, self.dm.group_name))
        
class ITC020305_DeleteAffinityGroups(BaseTestCase):
    '''
    @summary: ITC-02集群管理-03亲和组-05删除亲和组
    '''
    def setUp(self):
        '''
        @summary: 测试环境初始化
        '''
        self.dm = super(self.__class__, self).setUp()
        #创建一个亲和组
        LogPrint().info("Pre-Test-1: Create affinitygroups %s in cluster %s for this TC." % (self.dm.group_name, ModuleData.cluster_name))
        self.assertTrue(smart_create_affinitygroups(ModuleData.cluster_name, self.dm.group_info, self.dm.group_name))
        #添加一个虚拟机到亲和组
        self.affinitygroups_api = AffinityGroupsAPIs()
        LogPrint().info("Pre-Test-2: Add vm %s to affinitygroups %s." % (ModuleData.vm1_name, self.dm.group_name))
        self.affinitygroups_api.addVmtoAffinityGroups(ModuleData.cluster_name, self.dm.group_name, ModuleData.vm1_name)
        
    def test_DeleteAffinityGroups(self):
        '''
        @summary: 测试用例执行步骤
        @note: 删除亲和组
        @note: 验证状态返回码
        '''
        LogPrint().info("Test: Delete affinitygroups %s in cluster %s." % (self.dm.group_name, ModuleData.cluster_name))
        r = self.affinitygroups_api.deleteAffinityGroups(ModuleData.cluster_name, self.dm.group_name)
        if r['status_code'] == self.dm.status_code:
            LogPrint().info("PASS: Delete affinitygroups %s success." % self.dm.group_name)
            self.flag = True
        else:
            LogPrint().error("FAIL: Delete affinitygroups %s fail. The status_code is %s." % (self.dm.group_name, r['status_code']))
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        pass
        
class ITC02_TearDown(BaseTestCase):
    '''
    @summary: “集群管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    '''
    
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = self.initData('ITC02_Setup')
        
    def test_TearDown(self):
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
         
        # Step1：删除虚拟机
        LogPrint().info("Post-Module-Test-1: Delete vm '%s'." % self.dm.vm1_name)
        self.assertTrue(smart_del_vm(self.dm.vm1_name))
        LogPrint().info("Post-Module-Test-2: Delete vm '%s'." % self.dm.vm2_name)
        self.assertTrue(smart_del_vm(self.dm.vm2_name))
         
        # Step2：将export和iso存储域设置为Maintenance状态,然后从数据中心分离
        LogPrint().info("Post-Module-Test-2-1: Deactivate storage domains '%s'." % self.dm.export1_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_name, self.dm.export1_name))
        LogPrint().info("Post-Module-Test-2-2: Detach storage domains '%s'." % self.dm.export1_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_name, self.dm.export1_name))
        LogPrint().info("Post-Module-Test-2-3: Deactivate storage domains '%s'." % self.dm.iso1_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_name, self.dm.iso1_name))
        LogPrint().info("Post-Module-Test-2-4: Detach storage domains '%s'." % self.dm.iso1_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_name, self.dm.iso1_name))
        
        # Step3：将data2存储域设置为Maintenance状态，然后从数据中心分离
        LogPrint().info("Post-Module-Test-3-1: Deactivate data storage domains '%s'." % self.dm.data2_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_name, self.dm.data2_nfs_name))
        LogPrint().info("Post-Module-Test-3-2: Detach data storage domains '%s'." % self.dm.data2_nfs_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_name, self.dm.data2_nfs_name))
        
        # Step4：将data1存储域设置为Maintenance状态
        LogPrint().info("Post-Module-Test-4: Deactivate data storage domains '%s'." % self.dm.data1_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_name, self.dm.data1_nfs_name))
#         LogPrint().info("Post-Module-Test-3-2: Detach data storage domains '%s'." % self.dm.data1_nfs_name)
#         self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
                 
        # Step5：删除数据中心dc1（非强制，之后存储域变为Unattached状态）
        if dcapi.searchDataCenterByName(self.dm.dc_name)['result']['data_centers']:
            LogPrint().info("Post-Module-Test-5: Delete DataCenter '%s'." % self.dm.dc_name)
            self.assertTrue(dcapi.delDataCenter(self.dm.dc_name)['status_code']==self.dm.expected_status_code_del_dc)
                 
        # Step6：删除4个Unattached状态存储域（data1/data2/export1/iso）
        LogPrint().info("Post-Module-Test-6: Delete all unattached storage domains.")
        dict_sd_to_host = [self.dm.data1_nfs_name, self.dm.data2_nfs_name, self.dm.iso1_name, self.dm.export1_name]
        for sd in dict_sd_to_host:
            smart_del_storage_domain(sd, self.dm.xml_del_sd_option, host_name=self.dm.host1_name)
         
        # Step7：删除主机（host1）
        LogPrint().info("Post-Module-Test-7: Delete host '%s'." % self.dm.host1_name)
        self.assertTrue(smart_del_host(self.dm.host1_name, self.dm.xml_del_host_option))
         
        # Step8：删除集群cluster1
        if capi.searchClusterByName(self.dm.cluster_name)['result']['clusters']:
            LogPrint().info("Post-Module-Test-8: Delete Cluster '%s'." % self.dm.cluster_name)
            self.assertTrue(capi.delCluster(self.dm.cluster_name)['status_code']==self.dm.expected_status_code_del_cluster)


if __name__ == "__main__":
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["Cluster.ITC02_TearDown"]
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)

    unittest.TextTestRunner(verbosity=2).run(testSuite)
