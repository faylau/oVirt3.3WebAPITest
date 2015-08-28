#encoding:utf-8
from TestAPIs.VirtualMachineAPIs import VmNicAPIs, smart_create_vm, smart_create_vmdisk,\
    smart_start_vm, smart_stop_vm, smart_del_vm, VirtualMachineAPIs,\
    smart_create_vmnic
from time import sleep


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
from TestAPIs.DataCenterAPIs import DataCenterAPIs,smart_attach_storage_domain,smart_deactive_storage_domain, smart_detach_storage_domain
from TestAPIs.ClusterAPIs import ClusterAPIs, GlusterVolumeAPIs, smart_create_cluster, smart_delete_cluster,\
    smart_stop_volume,smart_start_volume,smart_delete_volume
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare, wait_until
from TestData.Volume import ITC10_SetUp as ModuleData
from TestAPIs.HostAPIs import smart_create_host,smart_del_host
from TestAPIs.StorageDomainAPIs import smart_create_storage_domain,smart_del_storage_domain, StorageDomainAPIs
from TestAPIs.TemplatesAPIs import TemplatesAPIs, smart_create_template, smart_delete_template
import xmltodict


class ITC10_SetUp(BaseTestCase):
    '''
    @summary: “集群管理”模块测试环境初始化（执行该模块测试用例时，都需要执行该用例搭建初始化环境）
    @note: （1）创建一个数据中心（共享）
    @note: （2）创建一个集群，开启集群服务
    @note: （3）为集群添加两台主机
    @note: （4）添加一个nfs类型的data存储
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()

    def test_SetUp_ENV(self):
        '''
        @summary: 创建一个数据中心
        '''
        dcapi = DataCenterAPIs()
        # 创建1个数据中心（共享类型）
        LogPrint().info("Pre-Module-Test-1: Create DataCenter '%s'." % self.dm.dc_nfs_name)
        self.assertTrue(dcapi.createDataCenter(self.dm.xml_dc_info)['status_code']==self.dm.expected_status_code_create_dc)
        capi = ClusterAPIs()
        # 创建1个集群,开启集群服务
        LogPrint().info("Pre-Module-Test-2: Create Cluster '%s' in DataCenter '%s'." % (self.dm.cluster_nfs_name, self.dm.dc_nfs_name))
        self.assertTrue(capi.createCluster(self.dm.xml_cluster_info)['status_code']==self.dm.expected_status_code_create_cluster)
      
        # 在NFS数据中心中创建两个主机，并等待主机UP。
        LogPrint().info("Pre-Module-Test-3: Create Host '%s' in Cluster '%s'." % (self.dm.host1_name, self.dm.cluster_nfs_name))
        self.assertTrue(smart_create_host(self.dm.host1_name, self.dm.xml_host1_info))
        self.assertTrue(smart_create_host(self.dm.host2_name, self.dm.xml_host2_info))
     
        # 为数据中心创建Data域。
        @BaseTestCase.drive_data(self, self.dm.xml_storage_info)
        def create_storage_domains(xml_storage_domain_info):
            sd_name = xmltodict.parse(xml_storage_domain_info)['storage_domain']['name']
            LogPrint().info("Pre-Module-Test-4: Create Data Storage '%s'." % sd_name)
            self.assertTrue(smart_create_storage_domain(sd_name, xml_storage_domain_info))
        create_storage_domains()
         
        # 将创建的的data1、data2和export、iso域附加到NFS/ISCSI数据中心里。
        LogPrint().info("Pre-Module-Test-5: Attach the data storages to data centers.")
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.data2_nfs_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.iso1_name))
        

     
class ITC1001_scene1(BaseTestCase):
    '''
    @summary: ITC-10卷管理-01场景：建立卷-启动卷-建立glusterfs存储-附加到数据中心-创建虚拟机-添加磁盘-启动虚拟机-关闭虚拟机-创建一个普通模板-创建子模板
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
        
           
    def test_Scene(self):
        '''
        @summary: 测试场景描述
        '''
        volumeapi = GlusterVolumeAPIs()
        #创建一个distributed_replicate类型的卷disrep，Replica Count=2，brick=4
        LogPrint().info("Create volume disrep")
        r = volumeapi.createGlusterVolume(self.dm.cluster_name, self.dm.xml_volume_disrep)
        if r['status_code'] == self.dm.expected_status_code_create_volume:
            LogPrint().info("PASS:Create volume disrep success.")
            self.flag = True
        else:
            LogPrint().error("FAIL:Status_code is WRONG.")
            self.flag = False
        self.assertTrue(self.flag)
           
        LogPrint().info("Start volume disrep")
        r = volumeapi.startGlusterVolume(self.dm.cluster_name, "disrep")
        if r['status_code'] == self.dm.expected_status_code_start_volume:
            def is_volume_up():
                return volumeapi.getClusterVolumeStatus(self.dm.cluster_name, "disrep") == "up"
            if wait_until(is_volume_up, 600, 5):
                LogPrint().info("PASS:Start volume disrep success.")
                self.flag = True
            else:
                LogPrint().error("FAIL:Start volume failed.Status is not UP.")
                self.flag = False
        else:
            LogPrint().error("FAIL:Status_code is WRONG.")
            self.flag = False
        self.assertTrue(self.flag)
#       
#     #利用该卷创建一个glusterfs类型的存储域
        sdapi = StorageDomainAPIs()
        LogPrint().info("Create glusterfs storagedomain '%s'."%self.dm.sd_name)
        r = sdapi.createStorageDomain(self.dm.xml_sd_info)
        if r['status_code'] == self.dm.expected_status_code_create_sd:
            LogPrint().info("PASS:Create glusterfs storagedomain '%s' SUCCESS."%self.dm.sd_name)
            self.flag=True
        else:
            LogPrint().info("FAIL:Create glusterfs storagedomain '%s' FAIL."%self.dm.sd_name)
            self.flag=False
        self.assertTrue(self.flag)
#     #将存储域附加到数据中心
        LogPrint().info("Attach glusterfs storagedomain '%s'to DC '%s'."%(self.dm.sd_name, self.dm.dc_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_name, self.dm.sd_name))
#     #创建虚拟机,为虚拟机添加磁盘，启动虚拟机
        LogPrint().info("Create a VM '%s'."%self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        LogPrint().info("ADD DISK '%s' for VM '%s'."%(self.dm.disk_alias,self.dm.vm_name))
        self.assertTrue(smart_create_vmdisk(self.dm.vm_name, self.dm.xml_disk_info, self.dm.disk_alias)[0])
        LogPrint().info("Start VM '%s'."%(self.dm.vm_name))
        self.assertTrue(smart_start_vm(self.dm.vm_name))
#         #关闭虚拟机，创建模板,创建子模板
        LogPrint().info("Stop VM '%s'."%(self.dm.vm_name))
        self.assertTrue(smart_stop_vm(self.dm.vm_name))
        self.assertTrue(smart_create_template(self.dm.base_temp_name, self.dm.temp_info))
        self.assertTrue(smart_create_template(self.dm.base_temp_name, self.dm.zi_temp_info, self.dm.temp_name))
        
    def TearDown(self):
        '''
        @summary: 清理环境，卷删除后应在主机上执行下列操作：
        setfattr -x trusted.glusterfs.volume-id /test/data1
        setfattr -x trusted.gfid /test/data1
        ''' 
        #step1：删除子模板
        self.assertTrue(smart_delete_template(self.dm.base_temp_name,self.dm.temp_name))    
        #step2：删除基础模板
        self.assertTrue(smart_delete_template(self.dm.base_temp_name))  
        #step3：删除虚拟机
        self.assertTrue(smart_del_vm(self.dm.vm_name))   
        #step4：停止卷
        self.assertTrue(smart_stop_volume(self.dm.cluster_name, 'disrep'))
        #step5：删除卷
        self.assertTrue(smart_delete_volume(self.dm.cluster_name, 'disrep'))
        #step6：维护数据域
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name,self.dm.sd_name))
        #step7:分离数据域
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.sd_name))
        #step8：删除数据域
        self.assertTrue(smart_del_storage_domain(self.dm.sd_name, self.dm.xml_del_option))
    
class ITC1002_scene2(BaseTestCase):
    '''
    @summary: ITC-10卷管理-02场景：创建一个卷-添加brick-启动卷
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
           
    def test_Scene(self):
        '''
        @summary: 测试场景描述
        '''
        #step1：创建一个distributed类型的卷
        volumeapi = GlusterVolumeAPIs()
        LogPrint().info("Create volume dis")
        r = volumeapi.createGlusterVolume(self.dm.cluster_name, self.dm.xml_volume_dis)
        print r
        if r['status_code'] == self.dm.expected_status_code_create_volume:
            LogPrint().info("PASS:Create volume dis success.")
            self.flag = True
        else:
            LogPrint().error("FAIL:Status_code is WRONG.")
            self.flag = False
        self.assertTrue(self.flag)
        #step2：添加两个brick
        volume_id = GlusterVolumeAPIs().getVolumeIdByName(self.dm.cluster_name, 'dis')
        r = volumeapi.addbrick(self.dm.cluster_id, volume_id, self.dm.xml_brick_info)
        if r['status_code'] == self.expected_status_code_add_brick:
            LogPrint().info("PASS:ADD brick to volume dis success.")
            self.flag = True
        else:
            LogPrint().error("FAIL:Status_code is WRONG.")
            self.flag = False
        self.assertTrue(self.flag)
        #step3：启动卷
        LogPrint().info("Start volume dis")
        r = volumeapi.startGlusterVolume(self.dm.cluster_name, "dis")
        if r['status_code'] == self.dm.expected_status_code_start_volume:
            def is_volume_up():
                return volumeapi.getClusterVolumeStatus(self.dm.cluster_name, "dis") == "up"
            if wait_until(is_volume_up, 600, 5):
                LogPrint().info("PASS:Start volume dis success.")
                self.flag = True
            else:
                LogPrint().error("FAIL:Start volume failed.Status is not UP.")
                self.flag = False
        else:
            LogPrint().error("FAIL:Status_code is WRONG.")
            self.flag = False
        self.assertTrue(self.flag)
    def TearDown(self):
        '''
        @summary: 清理环境，卷删除后应在主机上执行下列操作：
        setfattr -x trusted.glusterfs.volume-id /test/data1
        setfattr -x trusted.gfid /test/data1
        '''  
        #step1：停止卷
        self.assertTrue(smart_stop_volume(self.dm.cluster_name, 'dis'))
        #step2：删除卷
        self.assertTrue(smart_delete_volume(self.dm.cluster_name, 'dis'))   
class ITC1003_scene3(BaseTestCase):   
    '''
    @summary: 场景3-创建一个虚拟机a-创建模板-创建子模板1-使用最新模板创建虚拟机b-创建子模板2-检查虚拟机b
    @note: 
    ''' 
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
    def test(self):
        #step1:创建一个虚拟机
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info)) 
        #step2:为虚拟机创建模板
        vm_id = VirtualMachineAPIs().getVmIdByName(self.dm.vm_name) 
        TemplatesAPIs().createTemplate(self.dm.xml_temp_info, vm_id)  

class ITC1004_scene4(BaseTestCase):   
    '''
    @summary: 场景3-创建一个虚拟机a-创建模板-创建子模板1-使用最新模板创建虚拟机b-创建子模板2-检查虚拟机b
    @note: 
    ''' 
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
        
           
    def test_Scene(self):
        '''
        @summary: 测试场景描述
        '''
        #step3:为虚拟机创建子模板
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.xml_zi_temp_info1, self.dm.version_name1))
        #step4:使用步骤2模板的最新版本创建虚拟机
        self.assertTrue(smart_create_vm(self.dm.vm_name_new, self.dm.xml_vm_info_temp))
        #step5:为虚拟机增加一个网络接口
        self.assertTrue(smart_create_vmnic(self.dm.vm_name,self.dm.nic_info,self.dm.nic_name))
        #step6:为虚拟机创建一个新的子模板
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.xml_zi_temp_info2, self.dm.version_name2))
        #step7：检查虚拟机信息应该包含网络接口
        if VmNicAPIs().isVmNicExist(self.dm.vm_name_new, self.dm.nic_name):
            LogPrint().info("PASS:ITC1004_scene4.")
            self.assertTrue(True)
        else:
            LogPrint().error("FAIL:ITC1004_scene4.")
            self.assertTrue(False)
        
    def tearDown(self):
        #step1:删除两个虚拟机
        self.assertTrue(smart_del_vm(self.dm.vm_name))
        self.assertTrue(smart_del_vm(self.dm.vm_name_new))
        #step2：删除两个子模板
        self.assertTrue(smart_delete_template(self.dm.temp_name, self.dm.version_name1))
        self.assertTrue(smart_delete_template(self.dm.temp_name, self.dm.version_name2))
        #step3：删除基础模板
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        
    
           
     
class ITC10_TearDown(BaseTestCase):
    '''
    @summary: “虚拟机管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: 
    @note: （2）将导出域设置为Maintenance状态；分离导出域；
    @note: （3）将数据中心里的Data域（data1）设置为Maintenance状态,并从数据中心内分离；
    @note: （4）将data2域设置为Maintenance状态；
    @note: （4）删除数据中心dc（非强制）；
    @note: （5）删除所有unattached状态的存储域（data1/data2/export/iso）；
    @note: （6）删除主机host1 host2；
    @note: （7）删除集群cluster1。
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = self.initData('ITC10_SetUp')
         
    def test_TearDown(self):
        '''
        @summary: 模块级测试资源清理
        '''
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
         
        # Step2：将export和iso存储域设置为Maintenance状态,然后从数据中心分离
        LogPrint().info("Post-Module-Test-2-1: Deactivate storage domains '%s'." % self.dm.export1_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        LogPrint().info("Post-Module-Test-2-2: Detach storage domains '%s'." % self.dm.export1_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        LogPrint().info("Post-Module-Test-2-3: Deactivate storage domains '%s'." % self.dm.iso1_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.iso1_name))
        LogPrint().info("Post-Module-Test-2-4: Detach storage domains '%s'." % self.dm.iso1_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.iso1_name))
        
        # Step3：将data2存储域设置为Maintenance状态，然后从数据中心分离
        LogPrint().info("Post-Module-Test-3-1: Deactivate data storage domains '%s'." % self.dm.data2_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.data2_nfs_name))
        LogPrint().info("Post-Module-Test-3-2: Detach data storage domains '%s'." % self.dm.data2_nfs_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.data2_nfs_name))
        
        # Step4：将data1存储域设置为Maintenance状态
        LogPrint().info("Post-Module-Test-4: Deactivate data storage domains '%s'." % self.dm.data1_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
#         LogPrint().info("Post-Module-Test-3-2: Detach data storage domains '%s'." % self.dm.data1_nfs_name)
#         self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
                 
        # Step5：删除数据中心dc1（非强制，之后存储域变为Unattached状态）
        if dcapi.searchDataCenterByName(self.dm.dc_nfs_name)['result']['data_centers']:
            LogPrint().info("Post-Module-Test-5: Delete DataCenter '%s'." % self.dm.dc_nfs_name)
            self.assertTrue(dcapi.delDataCenter(self.dm.dc_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)
                 
        # Step6：删除4个Unattached状态存储域（data1/data2/export1/iso）
        LogPrint().info("Post-Module-Test-6: Delete all unattached storage domains.")
        dict_sd_to_host = [self.dm.data1_nfs_name, self.dm.data2_nfs_name, self.dm.iso1_name, self.dm.export1_name]
        for sd in dict_sd_to_host:
            smart_del_storage_domain(sd, self.dm.xml_del_sd_option, host_name=self.dm.host1_name)
         
        # Step7：删除主机（host1）
        LogPrint().info("Post-Module-Test-7: Delete host '%s'." % self.dm.host1_name)
        self.assertTrue(smart_del_host(self.dm.host1_name, self.dm.xml_del_host_option))
        LogPrint().info("Post-Module-Test-7: Delete host '%s'." % self.dm.host2_name)
        self.assertTrue(smart_del_host(self.dm.host2_name, self.dm.xml_del_host_option)) 
        # Step8：删除集群cluster1
        if capi.searchClusterByName(self.dm.cluster_nfs_name)['result']['clusters']:
            LogPrint().info("Post-Module-Test-8: Delete Cluster '%s'." % self.dm.cluster_nfs_name)
            self.assertTrue(capi.delCluster(self.dm.cluster_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)
       
        
if __name__ == "__main__":
    # 建立测试套件 testSuite，并添加多个测试用例
    test_cases = ["Volume.ITC1003_scene3","Volume.ITC1004_scene4"]
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
    unittest.TextTestRunner(verbosity=2).run(testSuite)
