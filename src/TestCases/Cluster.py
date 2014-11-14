#encoding:utf-8


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
from TestAPIs.DataCenterAPIs import DataCenterAPIs
from TestAPIs.ClusterAPIs import ClusterAPIs,smart_create_cluster,smart_delete_cluster
from TestAPIs.NetworkAPIs import NetworkAPIs,smart_create_network,smart_delete_network
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from TestData.Cluster import ITC02_Setup as ModuleData
from TestAPIs.HostAPIs import smart_create_host,smart_del_host

import xmltodict


class ITC02_Setup(BaseTestCase):
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
            
class ITC020101_GetClustersList(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01基本操作-01获取集群列表
    '''
    def test_GetClustersList(self):
        clusterapi = ClusterAPIs()
        r = clusterapi.getClustersList()
        if r['status_code']==200:
            LogPrint().info('Get Clusters list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error('Get Clusters list FAIL.')
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
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
    def test_GetClusterInfo(self):
        '''
        @summary: 测试用例执行步骤
        '''
        # 测试1：获取集群的信息，并与期望结果进行对比
        self.clusterapi = ClusterAPIs()
        r = self.clusterapi.getClusterInfo(self.dm.cluster_name)
        print r['status_code']
        if r['status_code']==self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.cluster_info)
            print dict_expected
            print dict_actual
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Get Cluster '%s' info SUCCESS." % self.dm.cluster_name)
#                 return True
            else:
                LogPrint().error("Get Cluster '%s' info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Get Cluster '%s' info FAILED. " % self.dm.cluster_name)
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))
    
class ITC02010301_CreateCluster(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-03创建一个集群-01创建成功
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.clusterapi = ClusterAPIs()
        
    def test_CreateCluster(self):
        r=self.clusterapi.createCluster(self.dm.cluster_info)
        if r['status_code'] == self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.cluster_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Create Cluster '%s' SUCCESS." % self.dm.cluster_name)
#                 return True
            else:
                LogPrint().error("Create Cluster '%s'  INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Get/Create Cluster '%s' FAILED. " % self.dm.cluster_name)
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))
               
class ITC02010302_CreateCluster_Dup(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-03创建一个集群-02重名
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
    def test_CreateCluster_Dup(self):
        r=self.clusterapi.createCluster(self.dm.cluster_info)
        if r['status_code'] == self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.error_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Test of CreateCluster_dup '%s' SUCCESS." % self.dm.cluster_name)
#                 return True
            else:
                LogPrint().error("Test of CreateCluster_dup '%s'  INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Test of CreateCluster_dup '%s' FAILED. " % self.dm.cluster_name)
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
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
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        self.clusterapi = ClusterAPIs()
        
    def test_CreateClusterNoRequired(self):
        self.expected_result_index = 0
        # 使用数据驱动，根据测试数据文件循环创建多个数据中心
        @BaseTestCase.drive_data(self, self.dm.cluster_info)
        def do_test(xml_info):
            self.flag = True
            r = self.clusterapi.createCluster(xml_info)
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
        @summary: 无需清理
        '''
        
class ITC02010401_UpdateCluster_nohost(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-04编辑集群-01集群内无主机
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        # 首先创建一个集群
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
    def test_UpdateCluster(self):
        self.expected_result_index = 0
        # 使用数据驱动，根据测试数据文件循环创建多个数据中心
        @BaseTestCase.drive_data(self, self.dm.cluster_info_new)
        def do_test(xml_info):
            self.flag = True
            r=self.clusterapi.updateCluster(self.dm.cluster_name,xml_info)
            if r['status_code'] ==self.dm.status_code:
                dict_actual = r['result']
                dict_expected = xmltodict.parse(xml_info)
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(dict_expected, dict_actual):
                    LogPrint().info("PASS:ITC02010401_UpdateCluster_nohost SUCCESS." )
#                 return True
                else:
                    LogPrint().error("FAIL:ITC02010401_UpdateCluster_nohost.Error-info  INCORRECT.")
                    self.flag = False
            else:
                LogPrint().error("FAIL:ITC02010401_UpdateCluster_nohost FAILED.Status-code WRONG. " )
                self.flag = False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name_new))

class ITC0201040201_UpdateCluster_host_cputype(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-04编辑集群-02集群内有主机-01更改集群的cpu类型
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        # 首先创建一个集群
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # 创建一个主机
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.host_info))
    def test_UpdateCluster_host(self):
        r=self.clusterapi.updateCluster(self.dm.cluster_name,self.dm.cluster_info_new)
        print r
        if r['status_code'] ==self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.expected_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS:ITC0201040201_test_UpdateCluster_host_cputype SUCCESS." )
#                 return True
            else:
                LogPrint().error("FAIL:ITC0201040201_test_UpdateCluster_host_cputype .Error-info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL:ITC0201040201_test_UpdateCluster_host_cputype.Status_code WRONG")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_del_host(self.dm.host_name,self.dm.host_del_option))
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
        # 首先创建一个集群
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # 创建一个主机
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.host_info))
    def test_UpdateCluster_host(self):
        r=self.clusterapi.updateCluster(self.dm.cluster_name,self.dm.cluster_info_new)
        print r
        if r['status_code'] ==self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.expected_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS:ITC0201040202_test_UpdateCluster_host_upcpu SUCCESS." )
#                 return True
            else:
                LogPrint().error("FAIL:ITC0201040202_test_UpdateCluster_host_upcpu. Error-info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL:ITC0201040202_test_UpdateCluster_host_upcpu.Status_code is wrong. ")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_del_host(self.dm.host_name,self.dm.host_del_option))
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name))

class ITC0201040203_UpdateCluster_host_name(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-04编辑集群-02集群内有主机-03更改名称
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        # 首先创建一个集群
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # 创建一个主机
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.host_info))
    def test_UpdateCluster_host(self):
        r=self.clusterapi.updateCluster(self.dm.cluster_name,self.dm.cluster_info_new)
        print r
        if r['status_code'] ==self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.cluster_info_new)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS:ITC0201040203_test_UpdateCluster_host_name SUCCESS." )
#                 return True
            else:
                LogPrint().error("FAIL:ITC0201040203_test_UpdateCluster_host_name. Error-info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL:ITC0201040203_test_UpdateCluster_host_name.Status_code is wrong. ")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_del_host(self.dm.host_name,self.dm.host_del_option))
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
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
    def test_DeleteCluster(self):
        '''
        @summary: 测试用例执行步骤
        '''
        # 测试1：获取集群的信息，并与期望结果进行对比
        r = self.clusterapi.delCluster(self.dm.cluster_name)
        if r['status_code']==self.dm.status_code:
            print self.clusterapi.searchClusterByName(self.dm.cluster_name)['result']['clusters']
            if not self.clusterapi.searchClusterByName(self.dm.cluster_name)['result']['clusters']:
                LogPrint().info("Delete Cluster '%s' info SUCCESS." % self.dm.cluster_name)
#                 return True
            else:
                LogPrint().error("Delete Cluster '%s' info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Delete Cluster '%s' FAILED. " % self.dm.cluster_name)
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
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
        # 首先创建一个集群
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # 创建一个主机
        self.assertTrue(smart_create_host(self.dm.host_name, self.dm.host_info))
    def test_DeleteCluster_host(self):
        r=self.clusterapi.delCluster(self.dm.cluster_name)
        print r
        if r['status_code'] ==self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.expected_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS:ITC02010502_DeleteCluster_host SUCCESS." )
#                 return True
            else:
                LogPrint().error("FAIL:ITC02010502_DeleteCluster_host. Error-info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL:ITC02010502_DeleteCluster_host.Status_code is wrong. ")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_del_host(self.dm.host_name,self.dm.host_del_option))
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
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
    def test_GetClusterNetworkList(self):
        r = self.clusterapi.getClusterNetworkList(self.dm.cluster_name)
        if r['status_code']==self.dm.status_code:
            LogPrint().info('Get ClusterNetwork list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error('Get ClusterNetwork list FAIL.')
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
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
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # step1：创建一个逻辑网络
        self.nwapi = NetworkAPIs()
        self.assertTrue(smart_create_network(self.dm.nw_info, self.dm.nw_name))
        # step2:附加该网络到集群上
        self.clusterapi = ClusterAPIs()
        self.clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        
    def test_GetClusterNetworkInfo(self):
        '''
        @summary: 测试用例执行步骤
        '''
        # 测试1：获取集群的网络信息
        r= self.clusterapi.getClusterNetworkInfo(self.dm.cluster_name, self.dm.nw_name)
        dict_actual = r
        dict_expected = xmltodict.parse(self.dm.nw_info)
        dictCompare = DictCompare()
        if dictCompare.isSubsetDict(dict_expected, dict_actual):
            LogPrint().info("Get ClusterNetwork '%s' info SUCCESS." % self.dm.nw_name)
#                 return True
        else:
            LogPrint().error("Get ClusterNetwork '%s' FAILED. " % self.dm.nw_name)
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_delete_network(self.dm.nw_name,self.dm.dc_name))
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
        
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        # step1：创建一个逻辑网络
        self.nwapi = NetworkAPIs()
        self.assertTrue(smart_create_network(self.dm.nw_info, self.dm.nw_name))
        
    def test_attachNetworktoCluster(self):
        '''
        @summary: 测试用例执行步骤
        '''
        r = self.clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        if r['status_code'] ==self.dm.status_code:
            cluster_id = r['result']['network']['cluster']['@id']
            cluster_name = self.clusterapi.getClusterNameById(cluster_id)
            if cluster_name == self.dm.cluster_name:
                LogPrint().info("attachNetworktoCluster SUCCESS." )
#                 return True
            else:
                LogPrint().error("attachNetworktoCluster INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("attachNetworktoCluster 'FAILED. ")
            self.flag = False
        self.assertTrue(self.flag)
            
        
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_delete_network(self.dm.nw_name,self.dm.dc_name))
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
        
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
        self.nwapi = NetworkAPIs()
        self.assertTrue(smart_create_network(self.dm.nw_info, self.dm.nw_name))
        
        self.clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        
    def test_detachNetworkFromCluster(self):
        '''
        @summary: 测试用例执行步骤
        '''
        r = self.clusterapi.detachNetworkFromCluster(self.dm.cluster_name, self.dm.nw_name)
        if r['status_code'] ==self.dm.status_code:
            #检查集群中网络是否存在
            if not self.clusterapi.getClusterNetworkInfo(self.dm.cluster_name, self.dm.nw_name):
                LogPrint().info("detachNetworkFromCluster SUCCESS." )
            else:
                LogPrint().info("detachNetworkFromCluster INCORRECT." ) 
        else:
            LogPrint().info("detachNetworkFromCluster FAILED." )
              
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_delete_network(self.dm.nw_name,self.dm.dc_name))
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
        self.clusterapi = ClusterAPIs()
        self.assertTrue(smart_create_cluster(self.dm.cluster_info, self.dm.cluster_name))
        
        self.nwapi = NetworkAPIs()
        self.assertTrue(smart_create_network(self.dm.nw_info, self.dm.nw_name))
        
        self.clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        
    def test_UpdateNetworkofCluster(self):
        '''
        @summary: 测试用例执行步骤
        '''
        r = self.clusterapi.updateNetworkOfCluster(self.dm.cluster_name, self.dm.nw_name, self.dm.nw_info_new)
        if r['status_code'] ==self.dm.status_code:
            dict_actual = self.clusterapi.getClusterNetworkInfo(self.dm.cluster_name, self.dm.nw_name)
            #dict_expected = {'network':xmltodict.parse(self.dm.nw_info_new)['network']}
            dict_expected = xmltodict.parse(self.dm.nw_info_new)
            print dict_actual
            print dict_expected
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("UpdateNetworkofCluster SUCCESS." )
            else:
                LogPrint().info("UpdateNetworkofCluster INCORRECT." ) 
        else:
            LogPrint().info("UpdateNetworkofCluster FAILED." )
              
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.assertTrue(smart_delete_network(self.dm.nw_name,self.dm.dc_name))
        self.assertTrue(smart_delete_cluster(self.dm.cluster_name)) 

class ITC02_TearDown(BaseTestCase):
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
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["Cluster.ITC02010503_DeleteCluster_vm"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)
    
    #fileName = r"e:\result.html"
    #fp = file(fileName, 'wb')
    #runner = HTMLTestRunner(stream=fp, title=u"测试结果", description=u"测试报告")
    #runner.run(testSuite)