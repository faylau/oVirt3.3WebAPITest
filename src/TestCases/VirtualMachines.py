#encoding:utf-8
'''
@author: keke
'''
import unittest
from BaseTestCase import BaseTestCase
from TestAPIs.DiskAPIs import DiskAPIs
from TestAPIs.ProfilesAPIs import ProfilesAPIs
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare,wait_until
from Utils.HTMLTestRunner import HTMLTestRunner
from TestAPIs.DataCenterAPIs import DataCenterAPIs,smart_attach_storage_domain,smart_deactive_storage_domain,\
smart_detach_storage_domain,smart_active_storage_domain
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs,VmDiskAPIs,VmNicAPIs,\
    smart_create_vmdisk, smart_delete_vmdisk
from TestAPIs.TemplatesAPIs import TemplatesAPIs, TemplateDisksAPIs,\
    TemplateNicsAPIs,smart_create_template,smart_create_tempnic,smart_delete_template,\
    smart_delete_tempnic
from TestAPIs.HostAPIs import smart_create_host,smart_del_host
from TestAPIs.StorageDomainAPIs import smart_create_storage_domain,smart_del_storage_domain
from TestAPIs.NetworkAPIs import NetworkAPIs
from TestAPIs.DiskAPIs import DiskAPIs,smart_create_disk,smart_delete_disk
import TestData.VirtualMachines.ITC05_SetUp as ModuleData

import xmltodict


   
class ITC05_SetUp(BaseTestCase):
    '''
    @summary: 虚拟机管理模块级测试用例，初始化模块测试环境；
    @note: （1）创建一个NFS类型数据中心；
    @note: （2）创建一个集群；
    @note: （3）创建一个主机，并等待其变为UP状态；
    @note: （4）创建4个存储域（data1/data2/Export/ISO）；
    @note: （5）将 data1 附加到数据中心；
    @note: （6）创建一个虚拟机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateModuleTestEnv(self):
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
    
        # 为NFS数据中心创建Data（data1/data2/export）。
        @BaseTestCase.drive_data(self, self.dm.xml_storage_info)
        def create_storage_domains(xml_storage_domain_info):
            sd_name = xmltodict.parse(xml_storage_domain_info)['storage_domain']['name']
            LogPrint().info("Pre-Module-Test-4: Create Data Storage '%s'." % sd_name)
            self.assertTrue(smart_create_storage_domain(sd_name, xml_storage_domain_info))
        create_storage_domains()
        
        # 将创建的的data1和export域附加到NFS/ISCSI数据中心里。
        LogPrint().info("Pre-Module-Test-5: Attach the data storages to data centers.")
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        #创建一个虚拟机
        self.vmapi = VirtualMachineAPIs()
        r = self.vmapi.createVm(self.dm.vm_info)
        if r['status_code'] == 201:
            self.vm_name = r['result']['vm']['name']
        else:
            LogPrint().error("Create vm failed.Status-code is wrong.")
            self.assertTrue(False)
        
            
class ITC05_TearDown(BaseTestCase):
    '''
    @summary: “虚拟机管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: （1）删除虚拟机
    @note: （2）将导出域设置为Maintenance状态；分离导出域；
    @note: （3）将数据中心里的Data域（data1）设置为Maintenance状态；
    @note: （4）删除数据中心dc（非强制）；
    @note: （5）删除所有unattached状态的存储域（data1/data2/export/iso）；
    @note: （6）删除主机host1；
    @note: （7）删除集群cluster1。
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = self.initData('ITC05_SetUp')
        
    def test_TearDown(self):
        vmapi=VirtualMachineAPIs()
        #Step1：删除虚拟机
        vmapi.delVm(self.dm.vm_name)
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        # Step2：将export存储域设置为Maintenance状态,然后从数据中心分离
        LogPrint().info("Post-Module-Test-1: Deactivate storage domains '%s'." % self.dm.export1_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        LogPrint().info("Post-Module-Test-1: Detach storage domains '%s'." % self.dm.export1_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        # Step3：将data1存储域设置为Maintenance状态
        LogPrint().info("Post-Module-Test-1: Deactivate data storage domains '%s'." % self.dm.data1_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
        
        # Step4：删除数据中心dc1（非强制，之后存储域变为Unattached状态）
        if dcapi.searchDataCenterByName(self.dm.dc_nfs_name)['result']['data_centers']:
            LogPrint().info("Post-Module-Test-2: Delete DataCenter '%s'." % self.dm.dc_nfs_name)
            self.assertTrue(dcapi.delDataCenter(self.dm.dc_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)
                
        # Step5：删除3个Unattached状态存储域（data1/data2/export1）
        LogPrint().info("Post-Module-Test-3: Delete all unattached storage domains.")
        dict_sd_to_host = [self.dm.data1_nfs_name, self.dm.data2_nfs_name,self.dm.iso1_name,self.dm.export1_name]
        for sd in dict_sd_to_host:
            smart_del_storage_domain(sd, self.dm.xml_del_sd_option, host_name=self.dm.host1_name)
        
        # Step6：删除主机（host1）
        LogPrint().info("Post-Module-Test-6: Delete host '%s'." % self.dm.host1_name)
        self.assertTrue(smart_del_host(self.dm.host1_name, self.dm.xml_del_host_option))
        
        # Step7：删除集群cluster1
        if capi.searchClusterByName(self.dm.cluster_nfs_name)['result']['clusters']:
            LogPrint().info("Post-Module-Test-5: Delete Cluster '%s'." % self.dm.cluster_nfs_name)
            self.assertTrue(capi.delCluster(self.dm.cluster_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)


class ITC050301_GetVMDiskList(BaseTestCase):

    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
    def test_GetVMDiskList(self):
        vmdisk_api = VmDiskAPIs()
        r = vmdisk_api.getVmDisksList(ModuleData.vm_name)
        if r['status_code'] == 200:
            LogPrint().info("Get VMDiskList success.")
            self.assertTrue(True)
        else:
            LogPrint().error("Get VMDiskList fail.The status_code is wrong.")
            self.assertTrue(False)
        
class ITC050302_GetVMDiskInfo(BaseTestCase):
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_vmdisk(ModuleData.vm_name,self.dm.disk_info,self.dm.disk_name))
        self.vmdisk_api = VmDiskAPIs()
    def test_GetVMDiskInfo(self):
        self.flag=True
        r = self.vmdisk_api.getVmDiskInfo(ModuleData.vm_name, self.dm.disk_name)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("Get GetVMDiskInfo success.")
        else:
            LogPrint().error("Get GetVMDiskInfo fail.The Template info is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name,self.dm.disk_name))
       
class ITC0503030101_CreateVMDisk_normal(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理 -03创建磁盘-01创建内部磁盘 -01成功创建 
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
    def test_CreateVMDisk_normal(self):
        self.vmdisk_api = VmDiskAPIs()
        self.expected_result_index = 0
        @BaseTestCase.drive_data(self, self.dm.disk_info)
        def do_test(xml_info):
            self.flag=True
            r = self.vmdisk_api.createVmDisk(ModuleData.vm_name, xml_info)
            def is_disk_ok():
                return self.vmdisk_api.getVmDiskStatus(ModuleData.vm_name, disk_alias=self.dm.disk_name[self.expected_result_index])=='ok'
            if r['status_code'] == self.dm.expected_status_code:
                if wait_until(is_disk_ok, 600, 10):
                    LogPrint().info("Create Disk '%s' for '%s'ok."%(self.dm.disk_name[self.expected_result_index],ModuleData.vm_name))
                else:
                    LogPrint().error("Create Disk '%s' for '%s'overtime"%(self.dm.disk_name[self.expected_result_index],ModuleData.vm_name))
                    self.flag=False
            else:
                LogPrint().error("Create Disk '%s' for '%s' failed.Status-code is wrong."%(self.dm.disk_name[self.expected_result_index],ModuleData.vm_name))
                self.flag=False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
    def tearDown(self):
        for index in range(0,2):
            self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name[index]))
class ITC0503030102_CreateVMDisk_noRequired(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理 -03创建磁盘-01创建内部磁盘 -02参数完整性
    '''   
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
    def test_CreateVMDisk_noRequired(self):
        self.vmdisk_api = VmDiskAPIs()
        self.expected_result_index = 0
        @BaseTestCase.drive_data(self, self.dm.disk_info)
        def do_test(xml_info):
            self.flag=True
            r = self.vmdisk_api.createVmDisk(ModuleData.vm_name, xml_info)
            if r['status_code'] == self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.expected_result_index]), r['result']):
                    LogPrint().info("PASS:ITC0503030102_CreateVMDisk_noRequired")
                else:
                    LogPrint().error("FAIL:ITC0503030102_CreateVMDisk_noRequired.Error-info is wrong.")
                    self.flag=False
            else:
                LogPrint().error("FAIL:ITC0503030102_CreateVMDisk_noRequired.Status-code is wrong.")
                self.flag=False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
    def tearDown(self):
        for index in range(0,4):
            self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name[index]))     

class ITC0503030201_CreateVMDisk_attach(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理 -03创建磁盘-02附加已有磁盘
    '''   
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        r=smart_create_disk(self.dm.disk_info, disk_alias=self.dm.disk_name)
        self.assertTrue(r[0])
        self.disk_id = r[1]
        
    def test_CreateVMDisk_attachshare(self):
        self.vmdisk_api = VmDiskAPIs()
        self.flag=True
        self.disk_info = '''
        <disk id = "%s"/>            
        '''%self.disk_id
        r = self.vmdisk_api.createVmDisk(ModuleData.vm_name, self.disk_info)
        print r
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.disk_info), r['result']):
                LogPrint().info("PASS:ITC05030302_CreateVMDisk_attach")
            else:
                LogPrint().error("FAIL:ITC05030302_CreateVMDisk_attach.Error-info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:ITC05030302_CreateVMDisk_attach.Status-code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))       

class ITC05030401_UpdateVMDisk(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-04编辑磁盘-01成功编辑
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        self.assertTrue(smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name))
    def test_UpdateVMDisk(self):
        self.flag=True
        r = self.vmdisk_api.updateVmDisk(ModuleData.vm_name, self.dm.disk_name, self.dm.update_disk_info)
        print r
        if r['status_code']==self.dm.expected_status_code:
            dictCompare=DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.update_disk_info), r['result']):
                LogPrint().info("Update vmdisk '%s' success."%self.dm.disk_name)
            else:
                LogPrint().info("Update vmdisk '%s' fail.The disk-info is wrong."%self.dm.disk_name)
                self.flag=False
        else:
            LogPrint().info("Update vmdisk '%s' fail.The status_code is wrong."%self.dm.disk_name)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name_new))
    
                                                   
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test_cases = ["VirtualMachines.ITC05030401_UpdateVMDisk"]
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)