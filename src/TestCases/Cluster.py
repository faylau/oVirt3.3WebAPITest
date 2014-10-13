#encoding:utf-8
from TestAPIs.NetworkAPIs import NetworkAPIs

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
from TestAPIs.ClusterAPIs import ClusterAPIs
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare
from Utils.HTMLTestRunner import HTMLTestRunner

import xmltodict

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
        
        # 准备1：创建一个集群
        self.clusterapi = ClusterAPIs()
        self.clusterapi.createCluster(self.dm.cluster_info)
        
    def test_GetClusterInfo(self):
        '''
        @summary: 测试用例执行步骤
        '''
        # 测试1：获取集群的信息，并与期望结果进行对比
        r = self.clusterapi.getClusterInfo(self.dm.cluster_name)
        print r['status_code']
        if r['status_code']==200:
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
        if self.clusterapi.searchClusterByName(self.dm.cluster_name):
            self.clusterapi.delCluster(self.dm.cluster_name)
    

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
        if self.clusterapi.searchClusterByName(self.dm.cluster_name):
            self.clusterapi.delCluster(self.dm.cluster_name)
               
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
        self.clusterapi.createCluster(self.dm.cluster_info)
        
    def test_CreateCluster(self):
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
        if self.clusterapi.searchClusterByName(self.dm.cluster_name):
            self.clusterapi.delCluster(self.dm.cluster_name)

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
        

class ITC020104_UpdateCluster(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-04编辑集群
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        # 首先创建一个集群
        self.clusterapi = ClusterAPIs()
        self.clusterapi.createCluster(self.dm.cluster_info)
        
    def test_UpdateCluster(self):
        r=self.clusterapi.updateCluster(self.dm.cluster_name,self.dm.cluster_info_new)
        if r['status_code'] ==self.dm.status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.cluster_info_new)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Update Cluster '%s' SUCCESS." % self.dm.cluster_name)
#                 return True
            else:
                LogPrint().error("Update Cluster '%s'  INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Update Cluster '%s' FAILED. " % self.dm.cluster_name)
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.clusterapi.searchClusterByName(self.dm.cluster_name_new):
            self.clusterapi.delCluster(self.dm.cluster_name_new)

class ITC020105_DeleteCluster(BaseTestCase):
    '''
    @summary: ITC-02集群管理-01集群操作-05删除集群
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
        
        # 准备1：创建一个集群
        self.clusterapi = ClusterAPIs()
        self.clusterapi.createCluster(self.dm.cluster_info)
        
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
        if self.clusterapi.searchClusterByName(self.dm.cluster_name)['result']['clusters']:
            self.clusterapi.delCluster(self.dm.cluster_name)
            
class ITC020201_GetClusterNetworkList(BaseTestCase):
    '''
    @summary: ITC-02集群管理-02集群网络基本操作-01获取集群网络列表
    '''
    def test_GetClusterNetworkList(self):
        self.dm = super(self.__class__, self).setUp()
        self.clusterapi = ClusterAPIs()
        r = self.clusterapi.getClusterNetworkList(self.dm.cluster_name)
        if r['status_code']==self.dm.status_code:
            LogPrint().info('Get ClusterNetwork list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error('Get ClusterNetwork list FAIL.')
            self.flag = False
        self.assertTrue(self.flag)
            
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
        
        # step1：创建一个逻辑网络,属于Default数据中心
        self.nwapi = NetworkAPIs()
        self.nwapi.createNetwork(self.dm.nw_info)
        # step2:附加该网络到集群上
        self.clusterapi = ClusterAPIs()
        self.clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        
    def test_GetClusterNetworkInfo(self):
        '''
        @summary: 测试用例执行步骤
        '''
        # 测试1：获取集群的网络信息
        r= self.clusterapi.getClusterNetworkInfo(self.dm.cluster_name, self.dm.network_name)
        dict_actual = r
        dict_expected = xmltodict.parse(self.dm.nw_info)
        dictCompare = DictCompare()
        if dictCompare.isSubsetDict(dict_expected, dict_actual):
            LogPrint().info("Get ClusterNetwork '%s' info SUCCESS." % self.dm.network_name)
#                 return True
        else:
            LogPrint().error("Get ClusterNetwork '%s' FAILED. " % self.dm.network_name)
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.nwapi.searchNetworkByName(self.dm.network_name):
            self.nwapi.delNetwork(self.dm.network_name, 'Default')
            
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
        
        # step1：创建一个逻辑网络,属于Default数据中心
        self.nwapi = NetworkAPIs()
        self.nwapi.createNetwork(self.dm.nw_info)
        # step2:创建一个集群，属于Default数据中心
        self.clusterapi = ClusterAPIs()
        self.clusterapi.createCluster(self.dm.cluster_info)
        
    def test_attachNetworktoCluster(self):
        '''
        @summary: 测试用例执行步骤
        '''
        # 测试1：
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
        if self.nwapi.searchNetworkByName(self.dm.network_name):
            self.nwapi.delNetwork(self.dm.network_name, 'Default')
        if self.clusterapi.searchClusterByName(self.dm.cluster_name):
            self.clusterapi.delCluster(self.dm.cluster_name)       

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
        
        # step1：创建一个逻辑网络,属于Default数据中心
        self.nwapi = NetworkAPIs()
        self.nwapi.createNetwork(self.dm.nw_info)
        # step2:创建一个集群，属于Default数据中心
        self.clusterapi = ClusterAPIs()
        self.clusterapi.createCluster(self.dm.cluster_info)
        
        # step3：将网络附加到集群
        self.clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        
    def test_detachNetworkFromCluster(self):
        '''
        @summary: 测试用例执行步骤
        '''
        r = self.clusterapi.detachNetworkFromCluster(self.dm.cluster_name, self.dm.network_name)
        if r['status_code'] ==self.dm.status_code:
            #检查集群中网络是否存在
            if not self.clusterapi.getClusterNetworkInfo(self.dm.cluster_name, self.dm.network_name):
                LogPrint().info("detachNetworkFromCluster SUCCESS." )
            else:
                LogPrint().info("detachNetworkFromCluster INCORRECT." ) 
        else:
            LogPrint().info("detachNetworkFromCluster FAILED." )
              
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        if self.nwapi.searchNetworkByName(self.dm.network_name):
            self.nwapi.delNetwork(self.dm.network_name, 'Default')
        if self.clusterapi.searchClusterByName(self.dm.cluster_name):
            self.clusterapi.delCluster(self.dm.cluster_name)

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
        
        # step1：创建一个逻辑网络,属于Default数据中心
        self.nwapi = NetworkAPIs()
        self.nwapi.createNetwork(self.dm.nw_info)
        # step2:创建一个集群，属于Default数据中心
        self.clusterapi = ClusterAPIs()
        self.clusterapi.createCluster(self.dm.cluster_info)
        
        # step3：将网络附加到集群
        self.clusterapi.attachNetworkToCluster(self.dm.cluster_name, self.dm.nw_info)
        
    def test_UpdateNetworkofCluster(self):
        '''
        @summary: 测试用例执行步骤
        '''
        r = self.clusterapi.updateNetworkOfCluster(self.dm.cluster_name, self.dm.network_name, self.dm.nw_info_new)
        if r['status_code'] ==self.dm.status_code:
            dict_actual = self.clusterapi.getClusterNetworkInfo(self.dm.cluster_name, self.dm.network_name)
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
        if self.nwapi.searchNetworkByName(self.dm.network_name):
            self.nwapi.delNetwork(self.dm.network_name, 'Default')
        if self.clusterapi.searchClusterByName(self.dm.cluster_name):
            self.clusterapi.delCluster(self.dm.cluster_name)



if __name__ == "__main__":
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["Cluster.ITC02010303_CreateClusterNoRequired"]
  
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)
    
    #fileName = r"e:\result.html"
    #fp = file(fileName, 'wb')
    #runner = HTMLTestRunner(stream=fp, title=u"测试结果", description=u"测试报告")
    #runner.run(testSuite)