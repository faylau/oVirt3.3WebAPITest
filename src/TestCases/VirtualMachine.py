#coding:utf-8
from Utils import PrintLog
from time import sleep
from TestAPIs import VirtualMachineAPIs
# from TestData.VirtualMachine.scenarios3_Snapshot import vmapi

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>', '"Keke Wei" <keke.wei@cs2c.com.cn>']
__version__ = "V0.3"

'''
# ChangeLog:
#---------------------------------------------------------------------------------------------------
# Version        Date            Desc                                            Author
#---------------------------------------------------------------------------------------------------
# V0.1           2014/11/03      初始版本                                                                                                Liu Fei / keke wei
#---------------------------------------------------------------------------------------------------
# V0.2           2014/11/15      *对自己编写的部分进行了统一的日志信息补充                              Liu Fei
#---------------------------------------------------------------------------------------------------
from __main__ import mod
from time import sleep
'''

from BaseTestCase import BaseTestCase
from TestAPIs.DataCenterAPIs import DataCenterAPIs,smart_attach_storage_domain,smart_deactive_storage_domain, smart_detach_storage_domain
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs, VmDiskAPIs, VmNicAPIs, smart_create_vmdisk, \
    smart_delete_vmdisk, smart_create_vm, smart_del_vm, smart_create_vmnic,smart_delete_vmnic, \
    smart_start_vm, smart_deactive_vmdisk, smart_suspend_vm,smart_stop_vm,\
    VmSnapshotAPIs, smart_active_vmdisk
from TestAPIs.StorageDomainAPIs import smart_create_storage_domain,smart_del_storage_domain, StorageDomainAPIs
from TestAPIs.HostAPIs import smart_create_host,smart_del_host, HostAPIs
from TestAPIs.DiskAPIs import DiskAPIs,smart_create_disk,smart_delete_disk
import TestData.VirtualMachine.ITC05_SetUp as ModuleData
import TestData.VirtualMachine.scenarios1_Snapshot as ModuleData1
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare,wait_until

import unittest
import xmltodict
import time
from collections import OrderedDict

   
class ITC05_SetUp(BaseTestCase):
    '''
    @summary: 虚拟机管理模块级测试用例，初始化模块测试环境；
    @note: （1）创建一个NFS类型数据中心；
    @note: （2）创建一个集群；
    @note: （3）创建一个主机，并等待其变为UP状态；
    @note: （4）创建4个存储域（data1/data2/Export/ISO）；
    @note: （5）将 四个存储域都附加到数据中心；
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
     
        # 为NFS数据中心创建Data（data1/data2/export/iso）。
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
        
        #创建一个虚拟机
        self.vmapi = VirtualMachineAPIs()
        self.Vmdiskapi = VmDiskAPIs()
        r = self.vmapi.createVm(self.dm.vm_info)
        if r['status_code'] == 201:
            self.vm_name = r['result']['vm']['name']
        else:
            LogPrint().error("Create vm failed.Status-code is WRONG.")
            self.assertTrue(False)
        #创建一个虚拟机和磁盘为测试快照场景做准备
    
        r = self.vmapi.createVm(self.dm.vm_scenarios2_info)
        if r['status_code'] == 201:
            self.vm_name = r['result']['vm']['name']
        else:
            LogPrint().error("Create 'VM-Scenarios2' failed.Status-code is WRONG.")
            self.assertTrue(False)
        smart_create_vmdisk(self.dm.snapshot_name,self.dm.xml_disk_info,self.dm.disk_alias,status_code=202)

     
        

class ITC050101_GetVmsList(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-01查看虚拟机列表
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
       
    def test_GetVmsList(self):
        '''
        @summary: 测试步骤
        @note: （1）获取虚拟机列表；
        @note: （2）操作成功，验证接口返回状态码是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Get VMs list.")
        r = vm_api.getVmsList()
        if r['status_code'] == self.dm.expected_status_code_get_vms:
            LogPrint().info("PASS: Get VMs list SUCCESS.")
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG.")
            self.flag = False
        self.assertTrue(self.flag)
       
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass
   
class ITC050102_GetVmInfo(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-02查看虚拟机信息
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
           
        # 前提1：创建一个虚拟机vm-ITC050102
        LogPrint().info("Pre-Test: Create a vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
           
    def test_GetVmInfo(self):
        '''
        @summary: 测试步骤
        @note: （1）调用相关接口，获取指定VM信息；
        @note: （2）操作成功，验证接口返回验证码、虚拟机信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Get vm '%s' info." % self.dm.vm_name)
        r = vm_api.getVmInfo(self.dm.vm_name)
        if r['status_code'] == self.dm.expected_status_code_get_vm_info:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.xml_vm_info), r['result']):
                LogPrint().info("PASS: Get vm '%s' info SUCCESS." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Get vm '%s' info INCORRECT." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
           
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
   
class ITC05010301_CreateVm_Normal(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-03创建-01普通创建
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
           
    def test_CreateVm_Normal(self):
        '''
        @summary: 测试步骤
        @note: （1）创建一个普通机（使用Blank模板）；
        @note: （2）操作成功，验证接口返回的状态码、虚拟机信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Create a vm '%s' from template 'Blank'." % self.dm.vm_name)
        r = vm_api.createVm(self.dm.xml_vm_info)
        if r['status_code'] == self.dm.expected_status_code_create_vm:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.xml_vm_info), r['result']):
                LogPrint().info("PASS: Create vm '%s' SUCCESS." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Create vm '%s' FAILED, returned vm info are INCORRECT." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG when creating vm '%s'." % (r['status_code'], self.dm.vm_name))
            self.flag = False
        self.assertTrue(self.flag)
       
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的虚拟机；
        '''
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
   
class ITC05010303_CreateVm_DupName(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-03创建-03重名
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
           
        # 前提1：创建一个虚拟机vm1
        LogPrint().info("Pre-Test: Create the 1st vm with name '%s'." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
           
    def test_CreateVm_DupName(self):
        '''
        @summary: 测试步骤
        @note: （1）创建一个重名的虚拟机；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Create the 2nd vm with dup name '%s'." % self.dm.vm_name)
        r = vm_api.createVm(self.dm.xml_vm_info)
        if r['status_code'] == self.dm.expected_status_code_create_vm_dup:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_create_vm_dup), r['result']):
                LogPrint().info("PASS: Returned messages are CORRECT while creating vm with dup name.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT while creating vm with dup name.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG when creating vm with dup name '%s'." % (r['status_code']))
            self.flag = False
        self.assertTrue(self.flag)
       
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的虚拟机；
        '''
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
   
class ITC05010304_CreateVm_NameVerify(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-03创建-04名称有效性
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
           
    def test_CreateVm_DupName(self):
        '''
        @summary: 测试步骤
        @note: （1）使用无效虚拟机名创建虚拟机；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        self.i = 0
        @BaseTestCase.drive_data(self, self.dm.xml_vm_info)
        def do_test(vm_info):
            LogPrint().info("Test: Create vm with invalid name '%s'." % xmltodict.parse(vm_info)['vm']['name'])
            r = vm_api.createVm(vm_info)
            if r['status_code'] == self.dm.expected_status_code_create_vm_invalid_name:
                if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.i]), r['result']):
                    LogPrint().info("PASS: Returned messages are CORRECT while creating vm with invalid name.")
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned messages are INCORRECT while creating vm with invalid name.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' is WRONG when creating vm with invalid name '%s'." % (r['status_code']))
                self.flag = False
            self.i += 1
            self.assertTrue(self.flag)
        do_test()
       
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的虚拟机；
        '''
        # 如果虚拟机存在，则删除，否则给出提示信息。
        for vm_name in self.dm.vm_name_list:
            LogPrint().info("Post-Test: Delete vm '%s'." % vm_name)
            self.assertTrue(smart_del_vm(vm_name))
   
class ITC05010305_CreateVm_NoRequiredParams(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-03创建-05缺少必填参数
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
           
    def test_CreateVm_NoRequiredParams(self):
        '''
        @summary: 测试步骤
        @note: （1）使用缺少必填参数（name、cluster、template）的xml文件创建虚拟机；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
           
        self.dict_vms = OrderedDict()
        self.dict_vms[self.dm.vm1_name] = self.dm.xml_vm1_info
        self.dict_vms[self.dm.vm2_name] = self.dm.xml_vm2_info
        self.dict_vms[self.dm.vm3_name] = self.dm.xml_vm3_info
           
        LogPrint().info("Test: Create vm without required parameters (name/cluster/template).")
        self.i = 0
        for vm_name in self.dict_vms:
            r = vm_api.createVm(self.dict_vms[vm_name])
            if r['status_code'] == self.dm.expected_status_code_list[self.i]:
                if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.i]), r['result']):
                    LogPrint().info("PASS: Returned messages are CORRECT while creating vm without required parameters (name/cluster/template).")
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Returned messages are INCORRECT while creating vm without parameters (name/cluster/template).")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' is WRONG when creating vm without parameters (name/cluster/template).")
                self.flag = False
            self.assertTrue(self.flag)
            self.i += 1
   
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的虚拟机；
        '''
        # 如果虚拟机存在，则删除，否则给出提示信息。
        for vm_name in self.dict_vms:
            LogPrint().info("Post-Test: Delete vm '%s'." % vm_name)
            self.assertTrue(smart_del_vm(vm_name))
   
class ITC05010403_EditVm_DupName(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-04编辑-03重名
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
           
        # 前提1：创建一个虚拟机vm1
        LogPrint().info("Pre-Test: Create a vm with name '%s'." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
           
    def test_EditVm_DupName(self):
        '''
        @summary: 测试步骤
        @note: （1）编辑虚拟机，使用重复的名称；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Edit vm '%s' with dup name '%s'." % (self.dm.vm_name, ModuleData.vm_name))
        r = vm_api.updateVm(self.dm.vm_name, self.dm.xml_vm_update_info)
        if r['status_code'] == self.dm.expected_status_code_edit_vm_dup:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_edit_vm_dup), r['result']):
                LogPrint().info("PASS: Returned messages are CORRECT while edit vm with dup name.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT while edit vm with dup name.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG when edit vm with dup name '%s'." % (r['status_code']))
            self.flag = False
        self.assertTrue(self.flag)
       
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的虚拟机；
        '''
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
        
class ITC0501040401_EditVm_AddCpuOnline(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-04编辑-04更改cpu-01在线增加cpu个数
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
        
        #前提1：创建一个虚拟机vm1，cpu个数为2
        LogPrint().info("Pre-Test-1: Create a vm %s with two cpus." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.vm_info))
        
        #前提2：启动虚拟机
        LogPrint().info("Pre-Test-2: Start the vm %s." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
        
    def test__EditVm_AddCpuOnline(self):
        '''
        @summary: 测试步骤
        @note: （1）增加虚拟机cpu个数（2增加到4）
        @note: （2）验证接口返回的状态码及信息
        '''
        self.flag = True
        self.vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Add cpus online to vm %s." % self.dm.vm_name)
        r = self.vm_api.updateVm(self.dm.vm_name, self.dm.cpu_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.cpu_info), r['result']):
                LogPrint().info("PASS: Add cpus online to vm success.")
            else:
                LogPrint().error("FAIL: Add cpus online to vm fail. The cpu info is wrong.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Add cpus online to vm fail. The status_code is %s." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理：删除创建的虚拟机
        '''
        LogPrint().info("Post-Test: Delete the vm %s." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
   
class ITC0501050101_DelVm_Normal_Down(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-05删除-01普通删除-01Down状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
           
        # 前提1：创建一个虚拟机vm1
        LogPrint().info("Pre-Test: Create a vm with name '%s'." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
           
    def test_DelVm_Normal_Down(self):
        '''
        @summary: 测试步骤
        @note: （1）删除Down状态的虚拟机；
        @note: （2）操作成功，验证接口返回的状态码、相关信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Delete vm '%s' with 'Down' state." % self.dm.vm_name)
        r = vm_api.delVm(self.dm.vm_name)
        if r['status_code'] == self.dm.expected_status_code_del_vm:
            if not vm_api.searchVmByName(self.dm.vm_name):
                LogPrint().info("PASS: Delete vm '%s' SUCCESS." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Delete vm '%s' FAILED." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
       
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的虚拟机；
        '''
        LogPrint().info("Post-Test: Delete vm '%s' if it exist." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
   
class ITC0501050102_DelVm_Normal_Up(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-05删除-01普通删除-02Up状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
           
        # 前提1：创建一个虚拟机vm1，并启动。
        LogPrint().info("Pre-Test: Create and Start vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        self.assertTrue(smart_start_vm(self.dm.vm_name))
           
    def test_DelVm_Normal_Up(self):
        '''
        @summary: 测试步骤
        @note: （1）删除Up状态的虚拟机；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Delete vm '%s' with 'Up' state." % self.dm.vm_name)
        r = vm_api.delVm(self.dm.vm_name)
        if r['status_code'] == self.dm.expected_status_code_del_vm_up:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_del_vm_up), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT while deleting vm '%s' with 'up' state." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT while deleting vm '%s' with 'up' state." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
       
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的虚拟机；
        '''
        LogPrint().info("Post-Test: Delete vm '%s' if it exist." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
   
class ITC05010502_DelVm_WithoutDisk(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-05删除-02不删除磁盘
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        self.dm = super(self.__class__, self).setUp()
           
        # 前提1：创建一个虚拟机vm1
        LogPrint().info("Pre-Test-1: Create a vm with name '%s'." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
           
        # 前提2：为虚拟机添加一个磁盘disk1
        LogPrint().info("Pre-Test-2: Create a disk '%s' and attach it to vm '%s'." % (self.dm.disk_alias, self.dm.vm_name))
        r = smart_create_vmdisk(self.dm.vm_name, self.dm.xml_disk_info, self.dm.disk_alias)
        self.disk_id = r[1]
        self.assertTrue(r[0])
           
    def test_DelVm_WithoutDisk(self):
        '''
        @summary: 测试步骤
        @note: （1）删除虚拟机，但不删除磁盘；
        @note: （2）操作成功，验证接口返回的状态码、相关信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        disk_api = DiskAPIs()
        LogPrint().info("Test: Delete vm '%s' without its disk '%s'." % (self.dm.vm_name, self.dm.disk_alias))
        r = vm_api.delVm(self.dm.vm_name, self.dm.xml_del_vm_without_disk)
        if r['status_code'] == self.dm.expected_status_code_del_vm:
            if not vm_api.searchVmByName(self.dm.vm_name) and disk_api.searchDiskByAlias(self.dm.disk_alias)['result']['disks']:
                LogPrint().info("PASS: Delete vm '%s' without disk SUCCESS." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Delete vm '%s' without disk FAILED. Vm still exists or Disk is removed." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG while deleting vm '%s' without disk." % (r['status_code'], self.dm.vm_name))
            self.flag = False
        self.assertTrue(self.flag)
       
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的磁盘；
        @note: （1）删除创建的虚拟机。
        '''
        LogPrint().info("Post-Test-1: Delete vm '%s' if it exist." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
        LogPrint().info("Post-Test-2: Delete disk '%s' if it exist." % self.dm.disk_alias)
        self.assertTrue(smart_delete_disk(self.disk_id))
   
class ITC05010503_DelVm_Force(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-05删除-03强制删除
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()        
            
        # 前提1：创建一个虚拟机vm1
        LogPrint().info("Pre-Test: Create a vm with name '%s' for this TC." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
    def test_DelVm_WithoutDisk(self):
        '''
        @summary: 测试步骤
        @note: （1）强制删除虚拟机；
        @note: （2）操作成功，验证接口返回的状态码、相关信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Force delete vm '%s'." % self.dm.vm_name)
        r = vm_api.delVm(self.dm.vm_name, self.dm.xml_del_vm_force)
        if r['status_code'] == self.dm.expected_status_code_del_vm:
            if not vm_api.searchVmByName(self.dm.vm_name):
                LogPrint().info("PASS: Force delete vm '%s' SUCCESS." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Force delete vm '%s' FAILED. Vm still exists." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG while force deleting vm '%s'." % (r['status_code'], self.dm.vm_name))
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的磁盘；
        @note: （1）删除创建的虚拟机。
        '''
        LogPrint().info("Post-Test: Delete vm '%s' if it exist." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name, self.dm.xml_del_vm_force))
            
class ITC05010504_DelVm_DeleteProtect(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-01虚拟机操作-05删除-04删除保护
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试环境
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1（设置“删除保护”项）
        LogPrint().info("Pre-Test: Create vm '%s' with 'Delete Protect' optoin." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
    def test_DelVm_DeleteProtect(self):
        '''
        @summary: 测试步骤
        @note: （1）删除虚拟机vm1（有删除保护选项）；
        @note: （2）操作失败，检查接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Delete vm '%s' with 'Delete Protect' option." % self.dm.vm_name)
        r = vm_api.delVm(self.dm.vm_name)
        if r['status_code'] == self.dm.expected_status_code_del_vm_fail:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_del_vm_fail), r['result']):
                LogPrint().info("PASS: Returned status code and info are CORRECT while deleting vm '%s' with 'Delete Protect' option." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned info are INCORRECT while deleting vm '%s' with 'Delete Protect' option." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test-1：编辑虚拟机，取消“删除保护”项
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Post-Test-1: Edit vm '%s' to cancel the 'Delete Protect' option." % self.dm.vm_name)
        self.assertTrue(vm_api.updateVm(self.dm.vm_name, self.dm.xml_vm_update_info)['status_code']==self.dm.expected_status_code_update_vm)
            
        # Post-Test-2：删除虚拟机
        LogPrint().info("Post-Test-2: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name, self.dm.xml_del_vm_force)) 
    
class ITC0502010101_StartVm_Down_NoDisk_MultiStartDevices(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-01启动-01Down状态-01无磁盘（有多个启动设备）
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试环境
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1，定义多个启动设备（光驱、磁盘等）
        LogPrint().info("Pre-Test: Create vm '%s' with multi-start-devices." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
    def test_StartVm_Down_NoDisk_MultiStartDevices(self):
        '''
        @summary: 测试步骤
        @note: （1）运行虚拟机；
        @note: （2）操作成功，检查接口返回的状态码、相关信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Start vm '%s' without disk in 'down' state (which have multi-start devices)." % self.dm.vm_name)
        r = vm_api.startVm(self.dm.vm_name)
        def is_vm_up():
            return vm_api.getVmStatus(self.dm.vm_name)=='up'
        if wait_until(is_vm_up, 600, 5):
            if r['status_code'] == 200:
                LogPrint().info("PASS: Start vm '%s' SUCCESS." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Start vm '%s' FAILED. Returned status code is INCORRECT." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Start vm '%s' FAILED. It's final state is not 'UP'." % self.dm.vm_name)
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机vm1
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
    
class ITC0502010102_StartVm_Down_NoDisk_StartFromHd(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-01启动-01Down状态-01无磁盘（只有一个启动设备：硬盘）
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试环境
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1，定义一个启动设备（硬盘）
        LogPrint().info("Pre-Test: Create vm '%s' with only one start device (hard disk)." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
    def test_StartVm_Down_NoDisk_StartFromHd(self):
        '''
        @summary: 测试步骤
        @note: （1）运行虚拟机；
        @note: （2）操作失败，检查接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Start vm '%s' without disk in 'down' state (have multi-start devices)." % self.dm.vm_name)
        r = vm_api.startVm(self.dm.vm_name)
        if r['status_code'] == self.dm.expected_status_code_start_vm_without_disk_fail:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_start_vm_without_disk_fail), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned messages are INCORRECT.")
        else:
            LogPrint().error("FAIL: Returned status code '%s' is INCORRECT." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机vm1
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
    
class ITC0502010103_StartVm_Down_StartFromHd(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-01启动-01Down状态-01无磁盘（只有一个启动设备：硬盘）
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试环境
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1，定义一个启动设备（硬盘）
        LogPrint().info("Pre-Test-1: Create vm '%s' with 'hd' as start divice." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
        # 前提2：为虚拟机vm1创建一个虚拟磁盘disk1
        LogPrint().info("Pre-Test-2: Create disk '%s' for vm '%s'." % (self.dm.disk_alias, self.dm.vm_name))
        self.assertTrue(smart_create_vmdisk(self.dm.vm_name, self.dm.xml_disk_info, self.dm.disk_alias))
            
    def test_StartVm_Down_StartFromHd(self):
        '''
        @summary: 测试步骤
        @note: （1）运行虚拟机；
        @note: （2）操作失败，检查接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Start vm '%s' with disk in 'down' state from hd device." % self.dm.vm_name)
        r = vm_api.startVm(self.dm.vm_name)
        def is_vm_up():
            return vm_api.getVmStatus(self.dm.vm_name)=='up'
        if wait_until(is_vm_up, 600, 5):
            if r['status_code'] == self.dm.expected_status_code_start_vm_with_disk:
                LogPrint().info("PASS: Start vm '%s' SUCCESS." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Start vm '%s' FAILED. Returned status code is INCORRECT." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Start vm '%s' FAILED. It's final state is not 'UP'." % self.dm.vm_name)
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机vm1
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
   
# class ITC05020102_StartVm_Suspended(BaseTestCase):
#     '''
#     @summary: ITC-05虚拟机管理-02生命周期管理-01启动-02Suspended状态
#     @note: 暂不运行该用例，因为该用例可能导致最终的TearDown运行失败（始终提示数据中心存在运行的任务，无法删除存储清空资源。）
#     '''
#     def setUp(self):
#         '''
#         @summary: 初始化测试数据、测试环境。
#         '''
#         # 初始化测试环境
#         self.dm = super(self.__class__, self).setUp()
#             
#         # 前提1：创建一个虚拟机vm1（第一启动设备为cd-rom）
#         LogPrint().info("Pre-Test-1: Create vm '%s' with 'cd-rom' as 1st start device." % self.dm.vm_name)
#         self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
#             
#         # 前提2：启动虚拟机，然后将其设置为suspended状态。
#         LogPrint().info("Pre-Test-2: Start vm '%s' and then make it in 'suspended' state." % self.dm.vm_name)
#         self.assertTrue(smart_start_vm(self.dm.vm_name))
#         self.assertTrue(smart_suspend_vm(self.dm.vm_name))
#             
#     def test_StartVm_Down_StartFromHd(self):
#         '''
#         @summary: 测试步骤
#         @note: （1）运行虚拟机；
#         @note: （2）操作成功，检查接口返回的状态码、提示信息是否正确。
#         '''
#         vm_api = VirtualMachineAPIs()
#         LogPrint().info("Test: Start vm '%s' with disk in 'suspended' state." % self.dm.vm_name)
#         r = vm_api.startVm(self.dm.vm_name)
#         def is_vm_up():
#             return vm_api.getVmStatus(self.dm.vm_name)=='up'
#         if wait_until(is_vm_up, 600, 5):
#             if r['status_code'] == self.dm.expected_status_code_start_vm_from_suspended:
#                 LogPrint().info("PASS: Start vm '%s' from 'suspended' state SUCCESS." % self.dm.vm_name)
#                 self.flag = True
#             else:
#                 LogPrint().error("FAIL: Start vm '%s' FAILED. Returned status code is INCORRECT." % self.dm.vm_name)
#                 self.flag = False
#         else:
#             LogPrint().error("FAIL: Start vm '%s' FAILED. It's final state is not 'UP'." % self.dm.vm_name)
#             self.flag = False
#         self.assertTrue(self.flag)
#             
#     def tearDown(self):
#         '''
#         @summary: 资源清理
#         '''
#         # Post-Test：删除虚拟机vm1
#         LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
#         self.assertTrue(smart_del_vm(self.dm.vm_name))
    
class ITC05020103_StartVm_Once(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-01启动-03只运行一次
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试环境
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1
        LogPrint().info("Pre-Tests-1: Create vm '%s' for this TC." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
        # 前提2：为虚拟机vm1创建一个磁盘disk1
        LogPrint().info("Pre-Test-2: Create disk '%s' for vm '%s'." % (self.dm.disk_alias, self.dm.vm_name))
        self.assertTrue(smart_create_vmdisk(self.dm.vm_name, self.dm.xml_disk_info, self.dm.disk_alias))
            
    def test_StartVm_Once(self):
        '''
        @summary: 测试步骤
        @note: （1）运行虚拟机；
        @note: （2）操作成功，检查接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Start vm '%s' by 'once'." % self.dm.vm_name)
        r = vm_api.startVm(self.dm.vm_name, self.dm.xml_start_vm_once)
        def is_vm_up():
            return vm_api.getVmStatus(self.dm.vm_name)=='up'
        if wait_until(is_vm_up, 600, 5):
            if r['status_code'] == self.dm.expected_status_code_start_vm_once:
                if DictCompare().isSubsetDict(xmltodict.parse(self.dm.xml_start_vm_once)['action'], vm_api.getVmInfo(self.dm.vm_name)['result']):
                    LogPrint().info("PASS: Start vm '%s' by 'once' SUCCESS." % self.dm.vm_name)
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Start vm '%s' SUCCESS, but its info not equals to 'xml_start_vm_once'." % self.dm.vm_name)
                    self.flag = False
            else:
                LogPrint().error("FAIL: Start vm '%s' by 'once' FAILED. Returned status code '%s' is INCORRECT." % (self.dm.vm_name, r['status_code']))
                self.flag = False
        else:
            LogPrint().error("FAIL: Start vm '%s' by 'once' FAILED. It's final state is not 'UP'." % self.dm.vm_name)
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机vm1
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
    
class ITC05020104_StartVm_Paused(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-01启动-04以暂停方式启动
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试环境
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1（第一启动设备为cdrom）
        LogPrint().info("Pre-Test: Create vm '%s' with 'cdrom' as 1st start device." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
    def test_StartVm_Paused(self):
        '''
        @summary: 测试步骤
        @note: （1）以暂停方式运行虚拟机；
        @note: （2）操作成功，检查接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Start vm '%s' by 'paused'." % self.dm.vm_name)
        r = vm_api.startVm(self.dm.vm_name, self.dm.xml_start_vm_paused)
        def is_vm_paused():
            return vm_api.getVmStatus(self.dm.vm_name)=='paused'
        if wait_until(is_vm_paused, 600, 5):
            if r['status_code'] == self.dm.expected_status_code_start_vm_paused:
                LogPrint().info("PASS: Start vm '%s' by 'paused' SUCCESS." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Start vm '%s' by 'paused' FAILED. Returned status code '%s' is INCORRECT." % (self.dm.vm_name, r['status_code']))
                self.flag = False
        else:
            LogPrint().error("FAIL: Start vm '%s' by 'paused' FAILED. It's final state is not 'Paused'." % self.dm.vm_name)
            self.flag = False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机vm1
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))            
    
class ITC05020201_StopVm_Up(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-02断电-01Up状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1，并启动。
        LogPrint().info("Pre-Test-1: Create vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        LogPrint().info("Pre-Test-2: Start vm '%s' to 'up' state." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
            
    def test_StopVm_Up(self):
        '''
        @summary: 测试步骤
        @note: （1）对虚拟机进行断电操作；
        @note: （2）操作成功，验证接口返回的状态码、VM的最终状态是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Stop vm '%s' from 'up' state." % self.dm.vm_name)
        r = vm_api.stopVm(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_stop_vm:
            if vm_api.getVmStatus(self.dm.vm_name)=='down':
                LogPrint().info("PASS: Stop vm '%s' from 'up' state SUCCESS." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Stop vm '%s' from 'up' state FAILED. Vm's final state is not 'down'." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
    
class ITC05020202_StopVm_Suspended(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-02断电-02Suspended状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1，启动，挂起。
        LogPrint().info("Pre-Test-1: Create a vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        LogPrint().info("Pre-Test-2: Start vm '%s' to 'up' state." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
        LogPrint().info("Pre-Test-3: Suspend a vm '%s' to 'suspended' state." % self.dm.vm_name)
        self.assertTrue(smart_suspend_vm(self.dm.vm_name))
            
    def test_StopVm_Suspended(self):
        '''
        @summary: 测试步骤
        @note: （1）对Suspended状态虚拟机进行断电操作；
        @note: （2）操作成功，验证接口返回的状态码、VM的最终状态是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        def is_vm_down():
            return vm_api.getVmStatus(self.dm.vm_name)=='down'
        LogPrint().info("Test: Stop vm '%s' from 'suspended' state." % self.dm.vm_name)
        r = vm_api.stopVm(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_stop_vm:
            if wait_until(is_vm_down, 600, 5):
                LogPrint().info("PASS: Stop vm '%s' from 'suspended' state SUCCESS." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Stop vm '%s' from 'suspended' state FAILED. Vm's final state is not 'down'." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))       
    
class ITC05020203_StopVm_Down(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-02断电-03Down状态失败
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1，处于Down状态。
        LogPrint().info("Pre-Test: Create a vm '%s' in 'Down' state for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
    def test_StopVm_Down(self):
        '''
        @summary: 测试步骤
        @note: （1）对Down状态虚拟机进行断电操作；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Stop vm '%s' from 'Down' state." % self.dm.vm_name)
        r = vm_api.stopVm(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_stop_vm_down:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_stop_vm_down), r['result']):
                LogPrint().info("PASS: Returned status code and info are CORRECT while stopping vm '%s' from 'down' state." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned info are INCORRECT while stopping vm '%s' from 'down' state." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))

# class ITC05020301_ShutdownVm_Up(BaseTestCase):
#     '''
#     @summary: ITC-05虚拟机管理-02生命周期管理-03关闭-01Up状态
#     @todo: 未完成，有OS的虚拟机才能正常shutdown，目前自动化测试环境中没有这样的虚拟机。
#     '''
#     def setUp(self):
#         '''
#         @summary: 初始化测试数据、测试环境。
#         '''
#         # 初始化测试数据
#         self.dm = super(self.__class__, self).setUp()
#          
#         # 前提1：创建一个虚拟机vm1，并启动。
#         LogPrint().info("Pre-Test-1: Create a vm '%s' for test." % self.dm.vm_name)
#         self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
#         LogPrint().info("Pre-Test-2: Start vm '%s' for test." % self.dm.vm_name)
#         self.assertTrue(smart_start_vm(self.dm.vm_name))
#          
#     def test_StopVm_Down(self):
#         '''
#         @summary: 测试步骤
#         @note: （1）对UP状态虚拟机进行Shutdown操作；
#         @note: （2）操作成功，验证接口返回的状态码、虚拟机最终状态是否正确。
#         '''
#         vm_api = VirtualMachineAPIs()
#         def is_vm_down():
#             return vm_api.getVmStatus(self.dm.vm_name)=='down'
#         LogPrint().info("Test: Shutdown vm '%s' from 'up' state." % self.dm.vm_name)
#         r = vm_api.shutdownVm(self.dm.vm_name)
#         if r['status_code']==self.dm.expected_status_code_shutdown_vm:
#             if wait_until(is_vm_down, 600, 5):
#                 LogPrint().info("PASS: Returned status code and info are CORRECT while shutdown vm '%s' from 'up' state." % self.dm.vm_name)
#                 self.flag = True
#             else:
#                 LogPrint().error("FAIL: Shutdown vm '%s' FAILED. It's final state is not 'down'." % self.dm.vm_name)
#                 self.flag = False
#         else:
#             LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
#             self.flag = False
#         self.assertTrue(self.flag)
#  
#     def tearDown(self):
#         '''
#         @summary: 资源清理
#         '''
#         # Post-Test：删除虚拟机
#         LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
#         self.assertTrue(smart_del_vm(self.dm.vm_name)) 
    
class ITC05020302_ShutdownVm_Suspended(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-03关闭-02Suspended状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
             
        # 前提1：创建一个虚拟机vm1，启动，挂起。
        LogPrint().info("Pre-Test-1: Create a vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        LogPrint().info("Pre-Test-2: Start vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
        LogPrint().info("Pre-Test-3: Suspend vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_suspend_vm(self.dm.vm_name))
             
    def test_StopVm_Down(self):
        '''
        @summary: 测试步骤
        @note: （1）对Suspended状态虚拟机进行Shutdown操作；
        @note: （2）操作成功，验证接口返回的状态码、虚拟机最终状态是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        def is_vm_down():
            return vm_api.getVmStatus(self.dm.vm_name)=='down'
        LogPrint().info("Test: Shutdown vm '%s' from 'suspended' state." % self.dm.vm_name)
        r = vm_api.shutdownVm(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_shutdown_vm_suspended:
            if wait_until(is_vm_down, 600, 5):
                LogPrint().info("PASS: Returned status code and info are CORRECT while shutdown vm '%s' from 'suspended' state." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Shutdown vm '%s' in 'suspended' state FAILED. It's final state is not 'down'." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name)) 
     
class ITC05020303_ShutdownVm_Down(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-03关闭-03Down状态失败
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
             
        # 前提1：创建一个虚拟机vm1，处于Down状态。
        LogPrint().info("Pre-Test: Create a vm '%s' in 'Down' state for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
             
    def test_StopVm_Down(self):
        '''
        @summary: 测试步骤
        @note: （1）对Down状态虚拟机进行Shutdown操作；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: SHUTDOWN vm '%s' from 'Down' state." % self.dm.vm_name)
        r = vm_api.shutdownVm(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_shutdown_vm_down:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_shutdown_vm_down), r['result']):
                LogPrint().info("PASS: Returned status code and info are CORRECT while SHUTDOWN vm '%s' from 'down' state." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned info are INCORRECT while SHUTDOWN vm '%s' from 'down' state." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))   
     
class ITC05020401_SuspendVm_Up(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-04挂起-01Up状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
             
        # 前提1：创建一个虚拟机vm1，并启动。
        LogPrint().info("Pre-Test-1: Create a vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        LogPrint().info("Pre-Test-2: Start vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
             
    def test_SuspendVm_Up(self):
        '''
        @summary: 测试步骤
        @note: （1）对UP状态虚拟机进行Suspend操作；
        @note: （2）操作成功，验证接口返回的状态码、虚拟机最终状态是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        def is_vm_suspended():
            return vm_api.getVmStatus(self.dm.vm_name)=='suspended'
        LogPrint().info("Test: Suspend vm '%s' from 'up' state." % self.dm.vm_name)
        r = vm_api.suspendVm(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_suspend_vm:
            if wait_until(is_vm_suspended, 600, 5):
                LogPrint().info("PASS: Returned status code and info are CORRECT while SUSPEND vm '%s' from 'up' state." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: SUSPEND vm '%s' FAILED. It's final state is not 'suspended'." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test-1：删除虚拟机
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name)) 
     
class ITC05020402_SuspendVm_Down(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-04挂起-02Down状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
             
        # 前提1：创建一个虚拟机vm1，处于Down状态。
        LogPrint().info("Pre-Test: Create a vm '%s' in 'Down' state for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
             
    def test_StopVm_Down(self):
        '''
        @summary: 测试步骤
        @note: （1）对Down状态虚拟机进行Suspend操作；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: SUSPEND vm '%s' from 'Down' state." % self.dm.vm_name)
        r = vm_api.suspendVm(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_suspend_vm_down:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_suspend_vm_down), r['result']):
                LogPrint().info("PASS: Returned status code and info are CORRECT while SUSPEND vm '%s' from 'down' state." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned info are INCORRECT while SUSPEND vm '%s' from 'down' state." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))   
   
class ITC05020403_SuspendVm_Suspended(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-04挂起-03Suspend状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1，启动，挂起。
        LogPrint().info("Pre-Test-1: Create a vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        LogPrint().info("Pre-Test-2: Start vm '%s' to 'up' state." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
        LogPrint().info("Pre-Test-3: Suspend a vm '%s' to 'suspended' state." % self.dm.vm_name)
        self.assertTrue(smart_suspend_vm(self.dm.vm_name))
            
    def test_StopVm_Down(self):
        '''
        @summary: 测试步骤
        @note: （1）对Suspended状态虚拟机进行Suspend操作；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: SUSPEND vm '%s' from 'suspended' state." % self.dm.vm_name)
        r = vm_api.suspendVm(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_suspend_vm_suspended:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_suspend_vm_suspended), r['result']):
                LogPrint().info("PASS: Returned status code and info are CORRECT while SUSPEND vm '%s' from 'suspended' state." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned info are INCORRECT while SUSPEND vm '%s' from 'suspended' state." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        # Post-Test：删除虚拟机
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))  
                       
class ITC05020501_MigrateVm_AutoSelectHost(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-05迁移-01自动选择主机
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1；
        LogPrint().info("Pre-Test-1: Create vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
        # 前提2：为虚拟机创建磁盘disk1；
        LogPrint().info("Pre-Test-2: Create disk '%s' for vm '%s'." % (self.dm.disk_alias, self.dm.vm_name))
        self.assertTrue(smart_create_vmdisk(self.dm.vm_name, self.dm.xml_disk_info, self.dm.disk_alias))
            
        # 前提3：启动虚拟机（缺省运行在host1上）
        LogPrint().info("Pre-Test-3: Start vm '%s' to 'up' state on host '%s'." % (self.dm.vm_name, ModuleData.host1_name))
        self.assertTrue(smart_start_vm(self.dm.vm_name))
            
        # 前提4：再新建一个主机host2（等待其变为UP状态，迁移用）
        LogPrint().info("Pre-Test-4: Create 2nd host '%s' for vm migration." % self.dm.host2_name)
        smart_create_host(self.dm.host2_name, self.dm.xml_host2_info)
            
    def test_MigrateVm_AutoSelectHost(self):
        '''
        @summary: 操作步骤
        @note: （1）进行迁移操作，自动选择迁移主机；
        @note: （2）操作成功，验证接口返回的状态码、相关信息是否正确。 
        '''
        def is_vm_up():
            return vm_api.getVmStatus(self.dm.vm_name)=='up'
        vm_api = VirtualMachineAPIs()
        host_api = HostAPIs()
        LogPrint().info("Test: Begin to migrate vm '%s' by Auto-Select host way." % self.dm.vm_name)
        r = vm_api.migrateVm(self.dm.vm_name, self.dm.xml_migrate_vm_option)
        if r['status_code'] == self.dm.expected_status_code_migrate_vm:
            if wait_until(is_vm_up, 600, 5) and vm_api.getVmInfo(self.dm.vm_name)['result']['vm']['host']['@id']==host_api.getHostIdByName(self.dm.host2_name):
                LogPrint().info("PASS: Migrate vm '%s' from host '%s' to '%s' SUCCESS." % (self.dm.vm_name, ModuleData.host1_name, self.dm.host2_name))
                self.flag = True
            else:
                LogPrint().error("FAIL: Migrate vm '%s' FAILED. Vm's state is not 'up' or vm is not running on host '%s'." % (self.dm.vm_name, self.dm.host2_name))
                self.flag = False
        else:
            LogPrint().error("FAIL: Migrate vm '%s' FAILED. Returned status code '%s' is WRONG." % (self.dm.vm_name, r['status_code']))
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）掉电虚拟机；
        @note: （2）删除虚拟机及磁盘。
        '''
        # Post-Test-1：删除虚拟机及磁盘
        LogPrint().info("Post-Test-1: Delete vm '%s' and it's disk '%s'." % (self.dm.vm_name, self.dm.disk_alias))
        self.assertTrue(smart_del_vm(self.dm.vm_name))
            
        # Post-Test-2: 删除主机host2
        LogPrint().info("Post-Test-2: Delete host '%s'." % self.dm.host2_name)
        self.assertTrue(smart_del_host(self.dm.host2_name, self.dm.xml_del_host_option))
            
class ITC05020502_MigrateVm_HandSelectHost(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-05迁移-02手动选择主机
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1；
        LogPrint().info("Pre-Test-1: Create vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
        # 前提2：为虚拟机创建磁盘disk1；
        LogPrint().info("Pre-Test-2: Create disk '%s' for vm '%s'." % (self.dm.disk_alias, self.dm.vm_name))
        self.assertTrue(smart_create_vmdisk(self.dm.vm_name, self.dm.xml_disk_info, self.dm.disk_alias))
            
        # 前提3：启动虚拟机（缺省运行在host1上）
        LogPrint().info("Pre-Test-3: Start vm '%s' to 'up' state." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
            
        # 前提4：再新建一个主机host2（等待其变为UP状态，迁移用）
        LogPrint().info("Pre-Test-4: Create 2nd host '%s' for vm migration." % self.dm.host2_name)
        smart_create_host(self.dm.host2_name, self.dm.xml_host2_info)
            
    def test_MigrateVm_HandSelectHost(self):
        '''
        @summary: 操作步骤
        @note: （1）进行迁移操作，手动选择迁移主机；
        @note: （2）操作成功，验证接口返回的状态码、相关信息是否正确。 
        '''
        def is_vm_up():
            return vm_api.getVmStatus(self.dm.vm_name)=='up'
        vm_api = VirtualMachineAPIs()
        host_api = HostAPIs()
        LogPrint().info("Test: Begin to migrate vm '%s' to host '%s' by Hand-Select." % (self.dm.vm_name, self.dm.host2_name))
        # xml_migrate_vm_option中定义的手动选择迁移的主机
        r = vm_api.migrateVm(self.dm.vm_name, self.dm.xml_migrate_vm_option)
        if r['status_code'] == self.dm.expected_status_code_migrate_vm:
            if wait_until(is_vm_up, 600, 5) and vm_api.getVmInfo(self.dm.vm_name)['result']['vm']['host']['@id']==host_api.getHostIdByName(self.dm.host2_name):
                LogPrint().info("PASS: Migrate vm '%s' to '%s' by Hand-Select SUCCESS." % (self.dm.vm_name, ModuleData.host1_name))
                self.flag = True
            else:
                LogPrint().error("FAIL: Migrate vm '%s' FAILED. Vm's state is not 'up' or it's not running on '%s'." % (self.dm.vm_name, self.dm.host2_name))
                self.flag = False
        else:
            LogPrint().error("FAIL: Migrate vm '%s' FAILED. Returned status code '%s' is WRONG." % (self.dm.vm_name, r['status_code']))
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）掉电虚拟机；
        @note: （2）删除虚拟机及磁盘。
        '''
        # Post-Test-1：删除虚拟机及磁盘
        LogPrint().info("Post-Test-1: Delete vm '%s' and it's disk '%s'." % (self.dm.vm_name, self.dm.disk_alias))
        self.assertTrue(smart_del_vm(self.dm.vm_name))
            
        # Post-Test-2: 删除主机host2
        LogPrint().info("Post-Test-2: Delete host '%s'." % self.dm.host2_name)
        self.assertTrue(smart_del_host(self.dm.host2_name, self.dm.xml_del_host_option))
    
class ITC05020503_MigrateVm_OnlyOneHost(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-05迁移-03只有一个主机
    @note: 只有一个主机时，虚拟机无法迁移；
    @bug: 提示信息不完整，可能是问题。
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1；
        LogPrint().info("Pre-Test-1: Create vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
        # 前提2：为虚拟机创建磁盘disk1；
        LogPrint().info("Pre-Test-2: Create disk '%s' for vm '%s'." % (self.dm.disk_alias, self.dm.vm_name))
        self.assertTrue(smart_create_vmdisk(self.dm.vm_name, self.dm.xml_disk_info, self.dm.disk_alias))
            
        # 前提3：启动虚拟机
        LogPrint().info("Pre-Test-3: Start vm '%s' to 'up' state." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
            
    def test_MigrateVm_AutoSelectHost(self):
        '''
        @summary: 操作步骤
        @note: （1）进行迁移操作，自动选择迁移主机；
        @note: （2）操作成功，验证接口返回的状态码、相关信息是否正确。 
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Begin to migrate vm '%s' while only 1 host exist." % self.dm.vm_name)
        r = vm_api.migrateVm(self.dm.vm_name, self.dm.xml_migrate_vm_option)
        if r['status_code'] == self.dm.expected_status_code_migrate_vm_fail:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_migrate_vm_fail), r['result']):
                LogPrint().info("PASS: Returned status code and info are CORRECT when migrating vm with only 1 host.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned info are CORRECT when migrating vm with only 1 host.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG when migrating vm with only 1 host." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）掉电虚拟机；
        @note: （2）删除虚拟机及磁盘。
        '''
        # Post-Test：删除虚拟机及磁盘
        LogPrint().info("Post-Test: Delete vm '%s' and it's disk '%s'." % (self.dm.vm_name, self.dm.disk_alias))
        self.assertTrue(smart_del_vm(self.dm.vm_name))
    
class ITC05020504_MigrateVm_NotAllowMigration(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-05迁移-04虚拟机设置不允许迁移
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1（设置为不允许迁移）；
        LogPrint().info("Pre-Test-1: Create vm '%s' with 'Migration Not Allowed' option for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
        # 前提2：为虚拟机创建磁盘disk1；
        LogPrint().info("Pre-Test-2: Create disk '%s' for vm '%s'." % (self.dm.disk_alias, self.dm.vm_name))
        self.assertTrue(smart_create_vmdisk(self.dm.vm_name, self.dm.xml_disk_info, self.dm.disk_alias))
            
        # 前提3：启动虚拟机（缺省运行在host1上）
        LogPrint().info("Pre-Test-3: Start vm '%s' to 'up' state." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
            
        # 前提4：再新建一个主机host2（等待其变为UP状态，迁移用）
        LogPrint().info("Pre-Test-4: Create 2nd host '%s' for vm migration." % self.dm.host2_name)
        smart_create_host(self.dm.host2_name, self.dm.xml_host2_info)
            
    def test_MigrateVm_NotAllowMigration(self):
        '''
        @summary: 操作步骤
        @note: （1）对设置为不允许迁移的VM进行迁移操作；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。 
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Migrate vm '%s' with 'Migration Not Allowed' option." % self.dm.vm_name)
        r = vm_api.migrateVm(self.dm.vm_name)
        if r['status_code'] == self.dm.expected_status_code_migrate_vm_not_allow:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_migrate_vm_not_allow), r['result']):
                LogPrint().info("PASS: Returned status code and info are CORRECT when migrating vm with 'Migration Not Allowed' option.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned info are CORRECT when migrating vm with 'Migration Not Allowed' option.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG when migrating vm with 'Migration Not Allowed' option." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）掉电虚拟机；
        @note: （2）删除虚拟机及磁盘。
        '''
        # Post-Test-1：删除虚拟机及磁盘
        LogPrint().info("Post-Test-1: Delete vm '%s' and it's disk '%s'." % (self.dm.vm_name, self.dm.disk_alias))
        self.assertTrue(smart_del_vm(self.dm.vm_name))
            
        # Post-Test-2: 删除主机host2
        LogPrint().info("Post-Test-2: Delete host '%s'." % self.dm.host2_name)
        self.assertTrue(smart_del_host(self.dm.host2_name, self.dm.xml_del_host_option))
    
class ITC05020601_CancelMigration_DuringMigration(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-06取消迁移-01迁移过程中
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1；
        LogPrint().info("Pre-Test-1: Create vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
        # 前提2：为虚拟机创建磁盘disk1；
        LogPrint().info("Pre-Test-2: Create disk '%s' for vm '%s'." % (self.dm.disk_alias, self.dm.vm_name))
        self.assertTrue(smart_create_vmdisk(self.dm.vm_name, self.dm.xml_disk_info, self.dm.disk_alias))
            
        # 前提3：启动虚拟机（缺省运行在host1上）
        LogPrint().info("Pre-Test-3: Start vm '%s' to 'up' state." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
            
        # 前提4：再新建一个主机host2（等待其变为UP状态，迁移用）
        LogPrint().info("Pre-Test-4: Create 2nd host '%s' for vm migration." % self.dm.host2_name)
        smart_create_host(self.dm.host2_name, self.dm.xml_host2_info)
            
    def test_MigrateVm_AutoSelectHost(self):
        '''
        @summary: 操作步骤
        @note: （1）进行迁移操作，自动选择迁移主机；
        @note: （2）操作成功，验证接口返回的状态码、相关信息是否正确。 
        '''
        def is_vm_migrating():
            return vm_api.getVmStatus(self.dm.vm_name)=='migrating'
        def is_vm_up():
            return vm_api.getVmStatus(self.dm.vm_name)=='up'
        vm_api = VirtualMachineAPIs()
        host_api = HostAPIs()
        LogPrint().info("Test-Step-1: Begin to migrate vm '%s'." % self.dm.vm_name)
        r = vm_api.migrateVm(self.dm.vm_name)
        if r['status_code'] == self.dm.expected_status_code_migrate_vm and wait_until(is_vm_migrating, 600, 5):
            LogPrint().info("Test-Step-1-PASS: Vm '%s' is in 'migrating' state." % self.dm.vm_name)
            LogPrint().info("Test-Step-2: Begin 'Cancel-Migration' action.")
            r1 = vm_api.cancelMigration(self.dm.vm_name)
            if r1['status_code']==self.dm.expected_status_code_cancel_migration:
                if wait_until(is_vm_up, 600, 5) and vm_api.getVmInfo(self.dm.vm_name)['result']['vm']['host']['@id']==host_api.getHostIdByName(ModuleData.host1_name):
                    LogPrint().info("PASS: Cancel Migration SUCCESS.")
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Cancel Migration FAILED. Vm's final state is not 'Up' or vm's host is WRONG.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' is WRONG while Cancel-Migration." % r1['status_code'])
                self.flag = False
            self.assertTrue(self.flag)
        else:
            LogPrint().error("Test-Step-1-FAIL: Migrate vm '%s' FAILED. Maybe the vm's state is not 'migrating'." % self.dm.vm_name)
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）掉电虚拟机；
        @note: （2）删除虚拟机及磁盘。
        '''
        # Post-Test-1：删除虚拟机及磁盘
        LogPrint().info("Post-Test-1: Delete vm '%s' and it's disk '%s'." % (self.dm.vm_name, self.dm.disk_alias))
        self.assertTrue(smart_del_vm(self.dm.vm_name))
            
        # Post-Test-2: 删除主机host2
        LogPrint().info("Post-Test-2: Delete host '%s'." % self.dm.host2_name)
        self.assertTrue(smart_del_host(self.dm.host2_name, self.dm.xml_del_host_option))
    
class ITC05020602_CancelMigration_NotDuringMigration(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-06取消迁移-02非迁移过程中
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
            
        # 前提1：创建一个虚拟机vm1；
        LogPrint().info("Pre-Test-1: Create vm '%s' for test." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
            
        # 前提2：为虚拟机创建磁盘disk1；
        LogPrint().info("Pre-Test-2: Create disk '%s' for vm '%s'." % (self.dm.disk_alias, self.dm.vm_name))
        self.assertTrue(smart_create_vmdisk(self.dm.vm_name, self.dm.xml_disk_info, self.dm.disk_alias))
            
        # 前提3：启动虚拟机（缺省运行在host1上）
        LogPrint().info("Pre-Test-3: Start vm '%s' to 'up' state." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))
            
        # 前提4：再新建一个主机host2（等待其变为UP状态，迁移用）
        LogPrint().info("Pre-Test-4: Create 2nd host '%s' for vm migration." % self.dm.host2_name)
        smart_create_host(self.dm.host2_name, self.dm.xml_host2_info)
            
    def test_CancelMigration_NotDuringMigration(self):
        '''
        @summary: 操作步骤
        @note: （1）进行迁移操作（自动选择迁移主机）；
        @note: （2）操作失败，验证接口返回的状态码、提示信息是否正确。 
        '''
        vm_api = VirtualMachineAPIs()
    
        LogPrint().info("Test: Begin 'Cancel-Migration' action while vm is not in migration progress.")
        r = vm_api.cancelMigration(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_cancel_migration_fail:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info_cancel_migration_fail), r['result']):
                LogPrint().info("PASS: Retured status code and info are CORRECT.")
                self.flag = True
            else:
                LogPrint().error("FAIL: Returned info are INCORRECT.\n'%s'" % xmltodict.unparse(r['result'], pretty=True))
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）掉电虚拟机；
        @note: （2）删除虚拟机及磁盘。
        '''
        # Post-Test-1：删除虚拟机及磁盘
        LogPrint().info("Post-Test-1: Delete vm '%s' and it's disk '%s'." % (self.dm.vm_name, self.dm.disk_alias))
        self.assertTrue(smart_del_vm(self.dm.vm_name))
            
        # Post-Test-2: 删除主机host2
        LogPrint().info("Post-Test-2: Delete host '%s'." % self.dm.host2_name)
        self.assertTrue(smart_del_host(self.dm.host2_name, self.dm.xml_del_host_option))

class ITC050301_GetVMDiskList(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理 -01获取磁盘列表
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据
        '''
        self.dm = super(self.__class__, self).setUp()
            
    def test_GetVMDiskList(self):
        '''
        @summary: 测试步骤
        @note: 操作成功，验证返回状态码
        '''
        vmdisk_api = VmDiskAPIs()
        LogPrint().info("Test: Get disk list of %s."%ModuleData.vm_name)
        r = vmdisk_api.getVmDisksList(ModuleData.vm_name)
        if r['status_code'] == 200:
            LogPrint().info("PASS: Get disk list of %s SUCCESS."%ModuleData.vm_name)
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code is WRONG.")
            self.falg = False
        self.assertTrue(self.flag)
            
class ITC050302_GetVMDiskInfo(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理 -02获取磁盘详情
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据
        '''
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create Disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmdisk(ModuleData.vm_name,self.dm.disk_info,self.dm.disk_name))
    
    def test_GetVMDiskInfo(self):
        '''
        @note: 操作成功，验证返回状态码及接口返回信息
        '''
        vmdisk_api = VmDiskAPIs()
        LogPrint().info("Test: Get Disk %s info of Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r = vmdisk_api.getVmDiskInfo(ModuleData.vm_name, self.dm.disk_name)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("PASS: Get GetVMDiskInfo SUCCESS.")
            self.flag = True
        else:
            LogPrint().error("FAIL: Get GetVMDiskInfo fail.The disk info is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
            
    def tearDown(self):
        '''
        @note: 清理测试环境
        '''
        LogPrint().info("Post-Test: Delete disk %s."%self.dm.disk_name)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name,self.dm.disk_name))
           
class ITC0503030101_CreateVMDisk_normal(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理 -03创建磁盘-01创建内部磁盘 -01成功创建 
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
          
    def test_CreateVMDisk_normal(self):
        '''
        @summary: 创建不同配置的虚拟机磁盘
        @note: 操作成功，验证返回状态码及接口返回信息
        '''
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
                    LogPrint().info("PASS: Create Disk '%s' for '%s'ok."%(self.dm.disk_name[self.expected_result_index],ModuleData.vm_name))
                else:
                    LogPrint().error("FAIL: Create Disk '%s' for '%s'overtime"%(self.dm.disk_name[self.expected_result_index],ModuleData.vm_name))
                    self.flag=False
            else:
                LogPrint().error("FAIL: Create Disk '%s' for '%s' failed.Status-code is WRONG."%(self.dm.disk_name[self.expected_result_index],ModuleData.vm_name))
                self.flag=False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
          
    def tearDown(self):
        for index in range(0,2):
            LogPrint().info("Post-Test: Delete disk %s."%self.dm.disk_name[index])
            self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name[index]))
    
class ITC0503030102_CreateVMDisk_noRequired(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理 -03创建磁盘-01创建内部磁盘 -02参数完整性
    '''   
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
          
    def test_CreateVMDisk_noRequired(self):
        '''
        @summary: 创建虚拟机磁盘,缺少必填项
        @note: 操作失败，验证返回状态码及接口返回信息
        '''
        self.vmdisk_api = VmDiskAPIs()
        self.expected_result_index = 0
        @BaseTestCase.drive_data(self, self.dm.disk_info)
        def do_test(xml_info):
            self.flag=True
            r = self.vmdisk_api.createVmDisk(ModuleData.vm_name, xml_info)
            if r['status_code'] == self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.expected_result_index]), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT.")
                else:
                    LogPrint().error("FAIL: Returned messages are WRONG.")
                    self.flag=False
            else:
                LogPrint().error("FAIL: Returned status code are WRONG.")
                self.flag=False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
          
    def tearDown(self):
        for index in range(0,4):
            LogPrint().info("Post-Test: Delete disk %s."%self.dm.disk_name[index])
            self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name[index]))     
    
class ITC05030302_CreateVMDisk_attach(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理 -03创建磁盘-02附加已有磁盘
    '''   
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create disk %s."%self.dm.disk_name)
        r=smart_create_disk(self.dm.disk_info, disk_alias=self.dm.disk_name)
        self.assertTrue(r[0])
        self.disk_id = r[1]
            
    def test_CreateVMDisk_attachshare(self):
        '''
        @summary: 创建虚拟机磁盘,附加已有磁盘
        @note: 操作成功，验证返回状态码及接口返回信息
        '''
        self.vmdisk_api = VmDiskAPIs()
        self.flag=True
        self.disk_info = '''
        <disk id = "%s"/>            
        '''%self.disk_id
        LogPrint().info("Test: Create disk attaching %s."%self.dm.disk_name)
        r = self.vmdisk_api.createVmDisk(ModuleData.vm_name, self.disk_info)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.disk_info), r['result']):
                LogPrint().info("PASS:Create disk attaching %s SUCCESS."%self.dm.disk_name)
            else:
                LogPrint().error("FAIL: Error-info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Status-code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
                
    def tearDown(self):
        LogPrint().info("Post-Test: Delete disk %s."%self.dm.disk_name)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))       
    
class ITC05030401_UpdateVMDisk_vmdown(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-04编辑磁盘-01虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        
    def test_active(self):
        '''
        @summary: 虚拟机关机时，编辑其激活的磁盘
        @note: 操作成功，验证返回状态码及接口返回信息
        '''
        self.flag=True
        LogPrint().info("Test: Update active disk %s when Vm %s is down."%(self.dm.disk_name, ModuleData.vm_name))
        r = self.vmdisk_api.updateVmDisk(ModuleData.vm_name, self.dm.disk_name, self.dm.update_disk_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare=DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.update_disk_info), r['result']):
                LogPrint().info("PASS: Update active vmdisk '%s' SUCCESS."%self.dm.disk_name)
            else:
                LogPrint().info("FAIL: Update active vmdisk '%s' fail.The disk-info is WRONG."%self.dm.disk_name)
                self.flag=False
        else:
            LogPrint().info("FAIL: Update active vmdisk '%s' fail.The status_code is WRONG."%self.dm.disk_name)
            self.flag=False
        self.assertTrue(self.flag)
        
    def test_deactive(self):
        '''
        @summary: 虚拟机关机时，编辑其非激活的磁盘
        @note: 操作成功，验证返回状态码及接口返回信息
        '''
        self.flag=True
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
        LogPrint().info("Test: Update deactive disk %s when Vm %s is down."%(self.dm.disk_name, ModuleData.vm_name))
        r = self.vmdisk_api.updateVmDisk(ModuleData.vm_name, self.dm.disk_name, self.dm.update_disk_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare=DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.update_disk_info), r['result']):
                LogPrint().info("PASS: Update deactive vmdisk '%s' to '%s'SUCCESS."%(self.dm.disk_name, self.dm.disk_name_new))
            else:
                LogPrint().info("FAIL: Update deactive vmdisk '%s' fail.The disk-info is WRONG."%self.dm.disk_name)
                self.flag=False
        else:
            LogPrint().info("FAIL: Update deactive vmdisk '%s' fail.The status_code is WRONG."%self.dm.disk_name)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        LogPrint().info("Post-Test: Delete disk %s."%self.dm.disk_name_new)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name_new))
    
class ITC0503040201_UpdateVMDisk_vmrun_active(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-04编辑磁盘-02虚拟机运行-01磁盘激活
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test-1: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        LogPrint().info("Pre-Test-2: Start Vm %s."%(ModuleData.vm_name))
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 600, 10):
            LogPrint().info("Start vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Start vm overtime.")
            self.assertTrue(False)
        
    def test_active(self):
        '''
        @summary: 虚拟机运行时，编辑其激活的磁盘
        @note: 操作失败，验证返回状态码及接口返回信息
        '''
        self.flag=True
        LogPrint().info("Test: Update active disk %s when Vm %s is running."%(self.dm.disk_name, ModuleData.vm_name))
        r = self.vmdisk_api.updateVmDisk(ModuleData.vm_name, self.dm.disk_name, self.dm.update_disk_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare=DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT.")
            else:
                LogPrint().info("FAIL: Returned  messages are WRONG.")
                self.flag=False
        else:
            LogPrint().info("FAIL: Returned status code are WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
        
   
    def tearDown(self):
        LogPrint().info("Post-Test-1: Stop Vm %s."%(ModuleData.vm_name))
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 600, 10):
            LogPrint().info("Stop vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        LogPrint().info("Post-Test-2: Delete disk %s."%(self.dm.disk_name ))      
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
           
class ITC0503040202_UpdateVMDisk_vmrun_deactive(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-04编辑磁盘-02虚拟机运行-02磁盘非激活
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test-1: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        LogPrint().info("Pre-Test-2: Start Vm %s."%(ModuleData.vm_name))
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 600, 10):
            LogPrint().info("Start vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Start vm overtime.")
            self.assertTrue(False)
        
    def test_deactive(self):
        '''
        @summary: 虚拟机运行时，编辑其非激活的磁盘
        @note: 操作成功，验证返回状态码及接口返回信息
        '''
        self.flag=True
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
        LogPrint().info("Test: Update deactive disk %s when Vm %s is running."%(self.dm.disk_name, ModuleData.vm_name))
        r = self.vmdisk_api.updateVmDisk(ModuleData.vm_name, self.dm.disk_name, self.dm.update_disk_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare=DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.update_disk_info), r['result']):
                LogPrint().info("PASS: Update  deactive vmdisk '%s' SUCCESS."%self.dm.disk_name)
            else:
                LogPrint().info("FAIL: Update deactive vmdisk '%s' fail.The disk-info is WRONG."%self.dm.disk_name)
                self.flag=False
        else:
            LogPrint().info("FAIL: Update deactive vmdisk '%s' fail.The status_code is WRONG."%self.dm.disk_name)
            self.flag=False
        self.assertTrue(self.flag)
   
    def tearDown(self):
        LogPrint().info("Post-Test-1: Stop Vm %s."%(ModuleData.vm_name))
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 600, 10):
            LogPrint().info("Stop vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)  
        LogPrint().info("Post-Test-2: Delete disk %s."%(self.dm.disk_name ))     
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name_new))
                        
class ITC05030403_UpdateVMDisk_volexpansion(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03磁盘管理-04编辑磁盘-03扩容
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
         
        # 初始化测试环境
        LogPrint().info("Pre-Test-1: Create a vm %s for this testcase." % self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.vm_info))
        LogPrint().info("Pre-Test-2: Create a disk %s for vm %s." % (self.dm.disk_alias, self.dm.vm_name))
        r = smart_create_vmdisk(self.dm.vm_name, self.dm.disk_info, self.dm.disk_alias)
        self.vmdisk_api = VmDiskAPIs()
        self.assertTrue(r[0])
        
    def test_volexpansion_vmdown(self):
        '''
        @summary: 虚拟机关闭状态下对其磁盘进行离线扩容
        @note: 验证接口返回的状态码及信息
        '''
        self.flag = True
        def is_vmdisk_ok():
            return self.vmdisk_api.getVmDiskStatus(self.dm.vm_name, self.dm.disk_alias) == 'ok'
        LogPrint().info("Test: Expand the disk %s when vm %s is down." % (self.dm.disk_alias, self.dm.vm_name))
        r = self.vmdisk_api.updateVmDisk(self.dm.vm_name, self.dm.disk_alias, self.dm.update_disk_info_down)
        if r['status_code'] == self.dm.expected_status_code:
            if wait_until(is_vmdisk_ok, 600, 5):
                if DictCompare().isSubsetDict(xmltodict.parse(self.dm.update_disk_info_down), self.vmdisk_api.getVmDiskInfo(self.dm.vm_name, self.dm.disk_alias)['result']):
                    LogPrint().info("PASS: Expand the disk %s from 5G to 10G success." % self.dm.disk_alias)
                else:
                    LogPrint().error("FAIL: Expand the disk %s from 5G to 10G fail. The disk info is wrong." % self.dm.disk_alias)
                    self.flag = False
            else:
                LogPrint().error("FAIL: Expand the disk %s from 5G to 10G fail. The disk status is wrong." % self.dm.disk_alias)
                self.flag = False
        else:
            LogPrint().error("FAIL: Expand the disk %s from 5G to 10G fail. The status_code %s is wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
 
    def test_volexpansion_vmrun(self):
        '''
        @summary: 虚拟机运行状态下对其磁盘进行在线扩容
        @note: 验证接口返回的状态码及信息
        '''
        self.flag = True
        def is_vmdisk_ok():
            return self.vmdisk_api.getVmDiskStatus(self.dm.vm_name, self.dm.disk_alias) == 'ok' 
        LogPrint().info("Pre-Test-3: Start the vm %s." % self.dm.vm_name)
        self.assertTrue(smart_start_vm(self.dm.vm_name))    
        LogPrint().info("Test: Expand the disk %s when vm %s is running." % (self.dm.disk_alias, self.dm.vm_name))
        r = self.vmdisk_api.updateVmDisk(self.dm.vm_name, self.dm.disk_alias, self.dm.update_disk_info_run)
        if r['status_code'] == self.dm.expected_status_code:
            if wait_until(is_vmdisk_ok, 600, 5):
                if DictCompare().isSubsetDict(xmltodict.parse(self.dm.update_disk_info_run), self.vmdisk_api.getVmDiskInfo(self.dm.vm_name, self.dm.disk_alias)['result']):
                    LogPrint().info("PASS: Expand the disk %s from 5G to 10G success." % self.dm.disk_alias)
                else:
                    LogPrint().error("FAIL: Expand the disk %s from 5G to 10G fail. The disk info is wrong." % self.dm.disk_alias)
                    self.flag = False
            else:
                LogPrint().error("FAIL: Expand the disk %s from 5G to 10G fail. The disk status is wrong." % self.dm.disk_alias)
                self.flag = False
        else:
            LogPrint().error("FAIL: Expand the disk %s from 5G to 10G fail. The status_code %s is wrong." % r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)      
        
    def tearDown(self):
        '''
        @summary: 测试环境清理，删除创建的虚拟机
        '''
        LogPrint().info("Post-Test: Delete the vm %s." % self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))     

class ITC05030501_DeleteVMDisk_option(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-05删除磁盘-01是否永久删除
    '''  
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试数据
        self.dm = super(self.__class__, self).setUp()
         
        # 初始化测试环境
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name)) 
        r = smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
         
    def test_detach(self):
        '''
        @summary: 将磁盘从虚拟机分离，而不删除
        @note: 操作成功，验证返回状态码，验证虚拟机的磁盘是否存在，验证磁盘是否存在
        '''
        self.flag = True
        LogPrint().info("Test: Detach disk %s from Vm %s." % (self.dm.disk_name, ModuleData.vm_name))
        r = self.vmdisk_api.delVmDisk(ModuleData.vm_name, disk_id=self.disk_id, xml_del_disk_option=self.dm.del_disk_option_detach)
        if r['status_code']==self.dm.expected_status_code:
            if not self.vmdisk_api.is_vmdisk_exist(ModuleData.vm_name, self.disk_id) and DiskAPIs().isExist(self.disk_id):
                LogPrint().info("PASS: Detach disk from vm SUCCESS.")
            elif self.vmdisk_api.is_vmdisk_exist(ModuleData.vm_name, self.disk_id):
                LogPrint().error("FAIL: Detach disk from vm fail.")
                self.flag=False
            elif not DiskAPIs().isExist(self.disk_id):
                LogPrint().error("FAIL: Disk is also deleted.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Detach disk from vm fail.Status_code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
        
    def test_remove(self):
        '''
        @summary: 将磁盘从虚拟机永久删除
        @note: 操作成功，验证返回状态码，验证虚拟机的磁盘是否存在，验证磁盘是否存在
        '''
        self.flag = True
        LogPrint().info("Test: Remove disk %s from Vm %s." % (self.dm.disk_name, ModuleData.vm_name))
        r = self.vmdisk_api.delVmDisk(ModuleData.vm_name, disk_id=self.disk_id, xml_del_disk_option=self.dm.del_disk_option_remove)
        if r['status_code']==self.dm.expected_status_code:
            if not self.vmdisk_api.is_vmdisk_exist(ModuleData.vm_name, self.disk_id) and not DiskAPIs().isExist(self.disk_id):
                LogPrint().info("PASS: Remove disk from vm SUCCESS.")
            elif self.vmdisk_api.is_vmdisk_exist(ModuleData.vm_name, self.disk_id):
                LogPrint().error("FAIL: Remove disk from vm fail.")
                self.flag=False
            elif DiskAPIs().isExist(self.disk_id):
                LogPrint().error("FAIL: Disk is still exist.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Remove disk from vm fail.Status_code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        LogPrint().info("Post-Test: Delete disk %s." % self.dm.disk_name)
        self.assertTrue(smart_delete_disk(self.disk_id)) 
    
class ITC05030502_DeleteActiveVMDisk_vmrun(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-05删除磁盘-02磁盘激活状态，虚拟机运行
    ''' 
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test-1: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        #启动虚拟机
        LogPrint().info("Pre-Test-2: Start Vm %s."%(ModuleData.vm_name))
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 600, 10):
            LogPrint().info("Start vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Start vm overtime.")
            self.assertTrue(False)
              
    def test(self):
        '''
        @summary: 虚拟机运行时，删除激活的磁盘
        @note: 操作失败，验证返回状态码及接口返回信息
        '''    
        self.flag=True
        LogPrint().info("Test: Delete disk %s when vm %s is running."%(self.dm.disk_name, ModuleData.vm_name))
        r=self.vmdisk_api.delVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        if r['status_code'] == self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                    LogPrint().info("PASS: Returned status code and messages are CORRECT.")
                else:
                    LogPrint().error("FAIL: Returned messages are WRONG.")
                    self.flag=False
        else:
            LogPrint().error("FAIL: Returned status code are WRONG.")
            self.flag=False
            
    def tearDown(self):
        LogPrint().info("Post-Test-1: Stop Vm %s."%(ModuleData.vm_name))  
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 600, 10):
            LogPrint().info("Stop vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        LogPrint().info("Post-Test-2: Delete disk %s."%(self.dm.disk_name ))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))  
            
class ITC05030601_activeVMDisk_vmrun(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-06激活磁盘-01虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test-1: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        #启动虚拟机
        LogPrint().info("Pre-Test-2: Start Vm %s."%(ModuleData.vm_name))
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 600, 10):
            LogPrint().info("Start vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Start vm overtime.")
            self.assertTrue(False)
        LogPrint().info("Pre-Test-3: Deactive disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
              
    def test_active(self):
        '''
        @summary: 虚拟机运行时，激活磁盘
        @note: 操作失败，验证返回状态码及返回信息
        '''    
        self.flag=True
        LogPrint().info("Test: Active disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=self.vmdisk_api.activateVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        def is_disk_active():
            return VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name, disk_id=self.disk_id)['result']['disk']['active']=='true'
        if r['status_code']==self.dm.expected_status_code:
            dictCompare = DictCompare()
            print xmltodict.unparse(r['result'], pretty=True)
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL: Returned messages are WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Returned status code are WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        LogPrint().info("Post-Test-1: Stop Vm %s."%(ModuleData.vm_name)) 
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 600, 10):
            LogPrint().info("Stop vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        LogPrint().info("Post-Test-2: Delete disk %s."%(self.dm.disk_name ))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
   
class ITC05030602_activeVMDisk_vmdown(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-06激活磁盘-02虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test-1: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        LogPrint().info("Pre-Test-2: Deactive disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
          
    def test_active(self):
        '''
        @summary: 虚拟机关机时，激活磁盘
        @note: 操作成功，验证返回状态码及磁盘状态
        '''    
        self.flag=True
        LogPrint().info("Test: Active disk %s when Vm %s is down."%(self.dm.disk_name, ModuleData.vm_name))
        r=self.vmdisk_api.activateVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        def is_disk_active():
            return VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name, disk_id=self.disk_id)['result']['disk']['active']=='true'
        if r['status_code']==self.dm.expected_status_code:
            if wait_until(is_disk_active, 60, 10):
                LogPrint().info("PASS: Active vmdisk SUCCESS when vm is down.")
            else:
                LogPrint().error("FAIL: Active vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Active vmdisk fail when vm is down.Status_code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        LogPrint().info("Post-Test: Delete disk %s."%(self.dm.disk_name ))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
   
class ITC05030701_deactiveVMDisk_vmrun(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-07取消激活磁盘-01虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test-1: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        LogPrint().info("Pre-Test-2: Start Vm %s."%(ModuleData.vm_name))
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 600, 10):
            LogPrint().info("Pre-Test:Start vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Pre-Test:Start vm overtime.")
            self.assertTrue(False)
              
    def test_deactive(self):
        '''
        @summary: 虚拟机运行时，取消激活磁盘
        @note: 操作成功，验证返回状态码及磁盘状态
        '''    
        self.flag=True
        LogPrint().info("Test: Dective disk %s when Vm %s is running."%(self.dm.disk_name, ModuleData.vm_name))
        r=self.vmdisk_api.deactivateVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        def is_disk_deactive():
            return VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name, disk_id=self.disk_id)['result']['disk']['active']=='false'
        if r['status_code']==self.dm.expected_status_code:
            if wait_until(is_disk_deactive, 60, 10):
                LogPrint().info("PASS: Deactive vmdisk SUCCESS when vm is running.")
            else:
                LogPrint().error("FAIL: Deactive vmdisk overtime when vm is running.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Deactive vmdisk fail when vm is running.Status_code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        LogPrint().info("Post-Test-1: Stop Vm %s."%(ModuleData.vm_name))
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 600, 10):
            LogPrint().info("Stop vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        LogPrint().info("Post-Test-2: Delete disk %s."%(self.dm.disk_name ))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
           
class ITC05030702_deactiveVMDisk_vmdown(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-07取消激活磁盘-02虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
          
    def test_deactive(self):
        '''
        @summary: 虚拟机关机时，取消激活磁盘
        @note: 操作成功，验证返回状态码及磁盘状态
        '''    
        self.flag=True
        LogPrint().info("Test: Dective disk %s when Vm %s is down."%(self.dm.disk_name, ModuleData.vm_name))
        r=self.vmdisk_api.deactivateVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        def is_disk_deactive():
            return VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name, disk_id=self.disk_id)['result']['disk']['active']=='false'
        if r['status_code']==self.dm.expected_status_code:
            if wait_until(is_disk_deactive, 60, 10):
                LogPrint().info("PASS: Deactive vmdisk SUCCESS when vm is down.")
            else:
                LogPrint().error("FAIL: Deactive vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Deactive vmdisk fail when vm is down.Status_code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        LogPrint().info("Post-Test: Delete disk %s."%(self.dm.disk_name))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
   
class ITC05030801_MoveactiveVMDisk_vmdown(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-08移动激活的磁盘-01虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
          
    def test_move(self):
        '''
        @summary: 虚拟机关机时，移动激活的磁盘
        @note: 操作成功，验证返回状态码及磁盘状态
        '''    
        self.flag=True
        LogPrint().info("Test: Move disk %s."%(self.dm.disk_name))
        r=self.vmdisk_api.moveVmDisk(ModuleData.vm_name, self.dm.move_option, self.disk_id)
        def is_disk_ok():
            return VmDiskAPIs().getVmDiskStatus(ModuleData.vm_name, disk_id=self.disk_id)=='ok'
        if r['status_code']==self.dm.expected_status_code:
            time.sleep(10)
            if wait_until(is_disk_ok, 600, 10):
                if VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name,disk_id=self.disk_id)['result']['disk']['storage_domains']\
                ['storage_domain']['@id']==StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data2_nfs_name):
                    LogPrint().info("PASS: Move vmdisk SUCCESS when vm is down.")
                else:
                    LogPrint().error("FAIL: Move vmdisk fail when vm is down.The des-storage is WRONG.")
                    self.flag=False
            else:
                LogPrint().error("FAIL: Move vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Move vmdisk fail when vm is down.Status_code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        LogPrint().info("Post-Test: Delete disk %s."%(self.dm.disk_name ))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
   
# class ITC05030802_MoveactiveVMDisk_vmrun(BaseTestCase):
#     '''
#     @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-08移动激活的磁盘-02虚拟机运行
#     @note: 虚拟机运行时，磁盘是否共享，移动激活磁盘结果不同
#     '''
#     def setUp(self):
#         self.dm = super(self.__class__, self).setUp()
#         self.vmdisk_api = VmDiskAPIs()
#         r_unshare=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info_unshare, self.dm.disk_name_unshare)
#         self.disk_id_unshare = r_unshare[1]
#         self.assertTrue(r_unshare[0])
#         r_share=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info_share, self.dm.disk_name_share)
#         self.disk_id_share = r_share[1]
#         self.assertTrue(r_share[0])
#         VirtualMachineAPIs().startVm(ModuleData.vm_name)
#         def is_vm_up():
#             return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
#         if wait_until(is_vm_up, 600, 10):
#             LogPrint().info("Pre-Test:Start vm SUCCESS.")
#             self.assertTrue(True)
#         else:
#             LogPrint().info("Pre-Test:Start vm overtime.")
#             self.assertTrue(False)
#     def test_move_unshare(self):
#         '''
#         @note: 磁盘设置为非共享的
#         '''
#         self.flag=True
#         r=self.vmdisk_api.moveVmDisk(ModuleData.vm_name, self.dm.move_option, self.disk_id_unshare)
#         def is_disk_ok():
#             return VmDiskAPIs().getVmDiskStatus(ModuleData.vm_name, disk_id=self.disk_id_unshare)=='ok'
#         if r['status_code']==self.dm.expected_status_code_unshare:
#             if wait_until(is_disk_ok, 600, 10):
#                 if VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name,disk_id=self.disk_id_unshare)['result']['disk']['storage_domains']\
#                 ['storage_domain']['@id']==StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data2_nfs_name):
#                     LogPrint().info("Move vmdisk SUCCESS when vm is down.")
#                 else:
#                     LogPrint().error("Move vmdisk fail when vm is down.The des-storage is WRONG.")
#                     self.flag=False
#             else:
#                 LogPrint().error("Move vmdisk overtime when vm is down.")
#                 self.flag=False
#         else:
#             LogPrint().error("Move vmdisk fail when vm is down.Status_code is WRONG.")
#             self.flag=False
#         self.assertTrue(self.flag)
#          
#     def test_move_share(self):
#         '''
#         @note: 磁盘设置为共享的
#         '''
#         self.flag=True
#         r=self.vmdisk_api.moveVmDisk(ModuleData.vm_name, self.dm.move_option, self.disk_id_share)
#         if r['status_code']==self.dm.expected_status_code_share:
#             if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
#                 LogPrint().info("PASS:Can't move active and sharable vmdisk when vm is running.")
#             else:
#                 LogPrint().error("FAIL:Error-info is WRONG.")
#                 self.flag=False
#         else:
#             LogPrint().error("FAIL:Status_code is WRONG.")
#             self.flag=False
#         self.assertTrue(self.flag)
#          
#     def tearDown(self):
#         VirtualMachineAPIs().stopVm(ModuleData.vm_name)
#         def is_vm_down():
#             return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
#         if wait_until(is_vm_down, 600, 10):
#             LogPrint().info("Stop vm SUCCESS.")
#             self.assertTrue(True)
#         else:
#             LogPrint().info("Stop vm overtime.")
#             self.assertTrue(False)
#         self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name_share))
#         self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name_unshare))
   
class ITC05030901_MovedeactiveVMDisk_vmdown(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-09移动非激活的磁盘-01虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test-1: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        #取消激活磁盘
        LogPrint().info("Pre-Test-2: Deactive disk %s."%(self.dm.disk_name))
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
          
    def test_move(self):
        '''
        @summary: 虚拟机关机时，移动非激活的磁盘
        @note: 操作成功，验证返回状态码及磁盘状态
        '''    
        self.flag=True
        LogPrint().info("Test: Move disk %s."%(self.dm.disk_name))
        r=self.vmdisk_api.moveVmDisk(ModuleData.vm_name, self.dm.move_option, self.disk_id)
        def is_disk_ok():
            return VmDiskAPIs().getVmDiskStatus(ModuleData.vm_name, disk_id=self.disk_id)=='ok'
        if r['status_code']==self.dm.expected_status_code:
            time.sleep(10)
            if wait_until(is_disk_ok, 600, 10):
                if VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name,disk_id=self.disk_id)['result']['disk']['storage_domains']\
                ['storage_domain']['@id']==StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data2_nfs_name):
                    LogPrint().info("PASS: Move vmdisk SUCCESS when vm is down.")
                else:
                    LogPrint().error("FAIL: Move vmdisk fail when vm is down.The des-storage is WRONG.")
                    self.flag=False
            else:
                LogPrint().error("FAIL: Move vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Move vmdisk fail when vm is down.Status_code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        LogPrint().info("Post-Test: Delete disk %s."%(self.dm.disk_name ))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
           
class ITC05030902_MovedeactiveVMDisk_vmrun(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-09移动非激活的磁盘-02虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test-1: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        #启动虚拟机
        LogPrint().info("Pre-Test-2: Start Vm %s."%(ModuleData.vm_name))
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 600, 10):
            LogPrint().info("Pre-Test:Start vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Pre-Test:Start vm overtime.")
            self.assertTrue(False)
        #取消激活磁盘
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
           
    def test_move(self):
        '''
        @summary: 虚拟机运行时，移动非激活的磁盘
        @note: 操作成功，验证返回状态码及磁盘状态
        '''    
        self.flag=True
        LogPrint().info("Test: Move disk %s."%(self.dm.disk_name))
        r=self.vmdisk_api.moveVmDisk(ModuleData.vm_name, self.dm.move_option, self.disk_id)
        def is_disk_ok():
            return VmDiskAPIs().getVmDiskStatus(ModuleData.vm_name, disk_id=self.disk_id)=='ok'
        if r['status_code']==self.dm.expected_status_code:
            time.sleep(10)
            if wait_until(is_disk_ok, 600, 10):
                if VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name,disk_id=self.disk_id)['result']['disk']['storage_domains']\
                ['storage_domain']['@id']==StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data2_nfs_name):
                    LogPrint().info("PASS: Move vmdisk SUCCESS when vm is down.")
                else:
                    LogPrint().error("FAIL: Move vmdisk fail when vm is down.The des-storage is WRONG.")
                    self.flag=False
            else:
                LogPrint().error("FAIL: Move vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Move vmdisk fail when vm is down.Status_code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        LogPrint().info("Post-Test-1: Stop Vm %s."%(ModuleData.vm_name))
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 600, 10):
            LogPrint().info("Stop vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        LogPrint().info("Post-Test-2: Delete disk %s."%(self.dm.disk_name ))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
   
class ITC050310_statisticsVmDisk(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-03虚拟机磁盘管理-10磁盘统计信息
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        LogPrint().info("Pre-Test: Create disk %s for Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
          
    def test(self):
        self.flag=True
        LogPrint().info("Test: Get statics of disk %s."%(self.dm.disk_name))
        r = self.vmdisk_api.statisticsVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("PASS:Get statistics of vmdisk SUCCESS.")
        else:
            LogPrint().error("FAIL:Get statistics of vmdisk fail.")
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        LogPrint().info("Post-Test: Delete disk %s of Vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
   
class ITC050401_GetVmNicList(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-01获取网络接口列表
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
          
    def test(self):
        '''
        @note: 获取网络接口列表
        @note: 操作成功，验证返回状态码
        '''
        LogPrint().info("Test: Get Vm %s nic list."%ModuleData.vm_name)
        r=self.vmnic_api.getVmNicsList(ModuleData.vm_name)
        if r['status_code']==200:
            LogPrint().info("PASS:Get vmnic list SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().error("FAIL:Get vmnic list fail.")
            self.assertTru(False)
            
class ITC050402_GetVmNicInfo(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-02获取网络接口详情
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test: Create a nic %s for Vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
     
    def test(self):
        '''
        @note: 获取网络接口详情
        @note: 操作成功，验证返回状态码及接口返回信息
        '''
        self.flag=True
        LogPrint().info("Test: Get nic '%s' info of Vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        r=self.vmnic_api.getVmNicInfo(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.nic_info), r['result']):
                LogPrint().info("PASS:Get vmnic info SUCCESS.")
            else:
                LogPrint().error("FAIL:Get vmnic info fail.The info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Get vmnic info.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        LogPrint().info("Post-Test: Delete a nic %s for Vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
  
class ITC05040301_CreateVmNic_normal(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-03创建-01正常创建
    @note: 考虑有无配置集的两种情况
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
     
    def test_noproid(self):
        '''
        @note: 创建网络接口，不指定配置集
        @note: 操作成功，验证返回状态码和接口返回信息
        '''
        self.flag=True
        LogPrint().info("Test: Create a nic for vm %s without profile."%ModuleData.vm_name)
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info_noproid)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.nic_info_noproid), r['result']):
                LogPrint().info("PASS:Create vmnic %s without profile SUCCESS."%self.dm.nic_name)
            else:
                LogPrint().error("FAIL:Create vmnic without profile fail.The info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Create vmnic without profile fail.The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
     
    def test_proid(self):
        '''
        @note: 创建网络接口，指定配置集
        @note: 操作成功，验证返回状态码和接口返回信息
        '''
        self.flag=True
        LogPrint().info("Test: Create a nic for vm %s with profile."%ModuleData.vm_name)
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info_proid)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.nic_info_proid), r['result']):
                LogPrint().info("PASS:Create vmnic with profile SUCCESS.")
            else:
                LogPrint().error("FAIL:Create vmnic with profile fail.The info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Create vmnic with profile fail.The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        LogPrint().info("Post-Test: Delete nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
      
class ITC05040302_CreateVmNic_dupname(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-03创建-02重名
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
     
    def test(self):
        '''
        @note: 创建网络接口，重名
        @note: 操作失败，验证返回状态码和接口返回信息
        '''
        self.flag=True
        LogPrint().info("Test: Create dupname nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL:Returned messages is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL: The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        LogPrint().info("Post-Test: Delete nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
  
class ITC05040303_CreateVmNic_norequired(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-03创建-03参数完整性
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
     
    def test_name(self):
        '''
        @note: 创建网络接口，缺少必填项
        @note: 操作失败，验证返回状态码和接口返回信息
        '''
        self.flag=True
        LogPrint().info("Test: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Returned status_code and error-info CORRECT.")
            else:
                LogPrint().error("FAIL:Returned error-info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Returned status_code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)
              
    def tearDown(self):
        LogPrint().info("Post-Test: Delete nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
      
class ITC05040304_CreateVmNic_verifyname(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-03创建-04验证名称合法性
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
     
    def test(self):
        '''
        @note: 创建网络接口，名称不合法
        @note: 操作失败，验证返回状态码和接口返回信息
        '''
        self.flag=True
        LogPrint().info("Test: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Returned status_code and error-info CORRECT.")
            else:
                LogPrint().error("FAIL:Returned error-info is WRONG.")
                self.flag=False
                print xmltodict.unparse(r['result'],pretty=True)
        else:
            LogPrint().error("FAIL:Returned status_code is WRONG.")
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)     
     
    def tearDown(self):
        LogPrint().info("Post-Test: Delete a nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
  
class ITC05040305_CreateVmNic_verifymac(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-03创建-05 验证mac地址合法性
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
     
    def test(self):
        '''
        @note: 创建网络接口，mac地址不合法
        @note: 操作失败，验证返回状态码和接口返回信息
        '''
        self.flag=True
        LogPrint().info("Test: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Returned status_code and error-info CORRECT.")
            else:
                LogPrint().error("FAIL:Returned error-info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Returned status_code is WRONG.")
            self.flag=False
        self.assertTrue(self.flag)     
     
    def tearDown(self):
        LogPrint().info("Post-Test: Delete a nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
  
class ITC05040401_UpdateVmNic_normal(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-04编辑网络接口-01正常编辑
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
     
    def test(self):
        '''
        @note: 编辑网络接口
        @note: 操作成功，验证返回状态码和接口返回信息
        '''
        LogPrint().info("Test: Update a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        r=self.vmnic_api.updateVmNic(ModuleData.vm_name, self.dm.nic_name, self.dm.update_vm_nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.update_vm_nic_info), r['result']):
                LogPrint().info("PASS:Update vmnic SUCCESS.")
            else:
                LogPrint().error("FAIL:Update vmnic fail.The info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Update vmnic fail.The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        LogPrint().info("Post-Test: Delete a nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.new_nic_name))
  
class ITC05040402_UpdateVmNic_dupname(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-04编辑网络接口-02重名
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test: Create two nics '%s' '%s' for vm %s."%(self.dm.nic_name1, self.dm.nic_name2, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info1, self.dm.nic_name1))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info2, self.dm.nic_name2))
     
    def test(self):
        '''
        @note: 编辑网络接口，重名
        @note: 操作失败，验证返回状态码和接口返回信息
        '''
        LogPrint().info("Test: Update nic %s of vm %s."%(self.dm.nic_name1, ModuleData.vm_name))
        r=self.vmnic_api.updateVmNic(ModuleData.vm_name, self.dm.nic_name1, self.dm.update_vm_nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL:Returned messages is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL:The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        LogPrint().info("Post-Test: Delete two nics '%s' '%s' of vm %s."%(self.dm.nic_name1, self.dm.nic_name2, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name1))     
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name2)) 
  
class ITC05040403_UpdateVmNic_type(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-04编辑网络接口-03编辑接口类型
    @note: 虚拟机运行状态下
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test-1: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
        LogPrint().info("Pre-Test-2: Create a disk %s for vm and start vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        r=smart_create_vmdisk(ModuleData.vm_name,self.dm.disk_info, self.dm.disk_name)
        self.assertTrue(r[0])
        self.disk_id=r[1]
        self.assertTrue(smart_start_vm(ModuleData.vm_name))
         
    def test(self):
        '''
        @note: 编辑网络接口，改变接口类型
        @note: 操作成功，验证返回状态码和接口返回信息
        '''
        LogPrint().info("Test: Update interface-type of nic %s."%(self.dm.nic_name))
        r=self.vmnic_api.updateVmNic(ModuleData.vm_name, self.dm.nic_name, self.dm.update_vm_nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.update_vm_nic_info), r['result']):
                LogPrint().info("PASS: Update interface-type of nic %s SUCCESS."%(self.dm.nic_name))
            else:
                LogPrint().error("FAIL: The info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL: The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
         
    def tearDown(self):
        LogPrint().info("Post-Test-1: Stop vm %s."%ModuleData.vm_name)
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 600, 10):
            LogPrint().info("Stop vm SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        LogPrint().info("Post-Test-2: Delete disk %s."%self.dm.disk_name)
        self.assertTrue(smart_delete_disk(self.disk_id))
        LogPrint().info("Post-Test-3: Delete a nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
  
class ITC05040404_UpdateVmNic_dupmac(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-04编辑网络接口-04mac已被使用
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test: Create two nics '%s' '%s' for vm %s."%(self.dm.nic_name1, self.dm.nic_name2, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info1, self.dm.nic_name1))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info2, self.dm.nic_name2))
     
    def test(self):
        '''
        @note: 编辑网络接口，重复mac地址
        @note: 操作失败，验证返回状态码和接口返回信息
        '''
        LogPrint().info("Test: Update nic %s of vm %s."%(self.dm.nic_name1, ModuleData.vm_name))
        r=self.vmnic_api.updateVmNic(ModuleData.vm_name, self.dm.nic_name1, self.dm.update_vm_nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL:Returned messages is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL:The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        LogPrint().info("Post-Test: Delete two nics '%s' '%s' of vm %s."%(self.dm.nic_name1, self.dm.nic_name2, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name1))     
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name2)) 
  
class ITC05040501_ActiveVmNic_vmrun(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-05激活网络接口-01虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test-1: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
        LogPrint().info("Pre-Test-2: Create a disk %s for vm and start vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name))
        self.assertTrue(smart_start_vm(ModuleData.vm_name))
     
    def test(self):
        '''
        @note: 虚拟机运行时，激活网络接口
        @note: 操作成功，验证返回状态码和网络接口状态
        '''
        LogPrint().info("Test: Active nic %s when vm %s is running."%(self.dm.nic_name, ModuleData.vm_name))
        r=self.vmnic_api.activateVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if self.vmnic_api.getVmNicInfo(ModuleData.vm_name, self.dm.nic_name)['result']['nic']['active']=='true':
                LogPrint().info("PASS: Active vmnic SUCCESS when vm is running.")
            else:
                LogPrint().error("FAIL: Active vmnic fail when vm is running.The info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Active vmnic fail when vm is running.The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        LogPrint().info("Post-Test-1: Stop vm %s."%ModuleData.vm_name)
        self.assertTrue(smart_stop_vm(ModuleData.vm_name))
        LogPrint().info("Post-Test-2: Delete disk %s."%self.dm.disk_name)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
        LogPrint().info("Post-Test-3: Delete a nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
  
class ITC05040502_ActiveVmNic_vmdown(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-05激活网络接口-02虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
          
    def test(self):
        '''
        @note: 虚拟机关机时，激活网络接口
        @note: 操作成功，验证返回状态码和网络接口状态
        '''
        LogPrint().info("Test: Active nic %s when vm %s is down."%(self.dm.nic_name, ModuleData.vm_name))
        r=self.vmnic_api.activateVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if self.vmnic_api.getVmNicInfo(ModuleData.vm_name, self.dm.nic_name)['result']['nic']['active']=='true':
                LogPrint().info("PASS: Active vmnic SUCCESS when vm is down.")
            else:
                LogPrint().error("FAIL: Active vmnic fail when vm is down.The info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Active vmnic fail when vm is down.The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        LogPrint().info("Post-Test: Delete a nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
  
class ITC05040601_DeactiveVmNic_vmrun(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-06取消激活网络接口-01虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test-1: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
        LogPrint().info("Pre-Test-2: Create a disk %s for vm and start vm %s."%(self.dm.disk_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name))
        self.assertTrue(smart_start_vm(ModuleData.vm_name))
     
    def test(self):
        '''
        @note: 虚拟机运行时，取消激活网络接口
        @note: 操作成功，验证返回状态码和网络接口状态
        '''
        LogPrint().info("Test: Deactive nic %s when vm %s is running."%(self.dm.nic_name, ModuleData.vm_name))
        r=self.vmnic_api.deactivateVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if self.vmnic_api.getVmNicInfo(ModuleData.vm_name, self.dm.nic_name)['result']['nic']['active']=='false':
                LogPrint().info("PASS: Deactive vmnic SUCCESS when vm is running.")
            else:
                LogPrint().error("FAIL: Deactive vmnic fail when vm is running.The info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Deactive vmnic fail when vm is running.The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        LogPrint().info("Post-Test-1: Stop vm %s."%ModuleData.vm_name)
        self.assertTrue(smart_stop_vm(ModuleData.vm_name))
        LogPrint().info("Post-Test-2: Delete disk %s."%self.dm.disk_name)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
        LogPrint().info("Post-Test-3: Delete a nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
  
class ITC05040602_DeactiveVmNic_vmdown(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-06取消激活网络接口-02虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
     
    def test(self):
        '''
        @note: 虚拟机关机时，取消激活网络接口
        @note: 操作成功，验证返回状态码和网络接口状态
        '''
        LogPrint().info("Test: Deactive nic %s when vm %s is down."%(self.dm.nic_name, ModuleData.vm_name))
        r=self.vmnic_api.deactivateVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if self.vmnic_api.getVmNicInfo(ModuleData.vm_name, self.dm.nic_name)['result']['nic']['active']=='false':
                LogPrint().info("PASS: Deactive vmnic SUCCESS when vm is down.")
            else:
                LogPrint().error("FAIL: Deactive vmnic fail when vm is down.The info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL: Deactive vmnic fail when vm is down.The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        LogPrint().info("Post-Test: Delete vmnic %s."%self.dm.nic_name)
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
          
class ITC05040701_DeleteVmNic_vmdown_plugged(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-07删除网络接口-01虚拟机down
    '''
    def setUp(self):
        '''
        '''
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
          
    def test(self):
        '''
        @note: 虚拟机关机时，删除已插入的网络接口
        @note: 操作成功，验证返回状态码和网络接口是否存在
        '''
        LogPrint().info("Test: Delete nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        r = self.vmnic_api.delVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if not self.vmnic_api.isVmNicExist(ModuleData.vm_name, self.dm.nic_name):
                LogPrint().info("PASS:Delete vmnic SUCCESS.")
                self.flag = True
            else:
                LogPrint().error("FAIL:Delete vmnic fail.The vmnic is still exist.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Delete vmnic fail.The status_code is '%s'."%r['status_code'])
#             print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        '''
        '''
        LogPrint().info("Post-Test: Delete vmnic %s."%self.dm.nic_name)
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
  
class ITC05040702_DeleteVmNic_vmrun_plugged(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-04网络接口-07删除网络接口-02虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        LogPrint().info("Pre-Test-1: Create a nic %s for vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
        LogPrint().info("Pre-Test-2: Create a disk and start vm.")
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.assertTrue(r[0])
        self.disk_id = r[1]
        self.assertTrue(smart_start_vm(ModuleData.vm_name))
          
    def test_DeleteVmNic_vmrun_plugged(self):
        '''
        @note: 虚拟机运行时，删除已插入的网络接口
        @note: 操作失败，验证返回状态码和报错信息
        '''
        LogPrint().info("Test: Delete nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        r = self.vmnic_api.delVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Can not delete plugged nic when vm is running.")
                self.flag = True
            else:
                LogPrint().error("FAIL:The error-info is WRONG.")
                self.flag=False
        else:
            LogPrint().error("FAIL:The status_code is '%s'."%r['status_code'])
#             print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
          
    def tearDown(self):
        LogPrint().info("Post-Test-1: Stop vm %s."%ModuleData.vm_name)
        self.assertTrue(smart_stop_vm(ModuleData.vm_name))
        LogPrint().info("Post-Test-2: Delete disk %s."%self.dm.disk_name)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
        LogPrint().info("Post-Test-3: Delete a nic %s of vm %s."%(self.dm.nic_name, ModuleData.vm_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))

class scenarios1_Snapshot(BaseTestCase):
    '''
    @summary: 创建离线快照
    @note: 创建离线快照为后面的恢复和克隆做前提条件；
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.snp_api = VmSnapshotAPIs()
     
    def test_CreateSnapshot_Offline(self):
        LogPrint().info("Test: Create a offline snapshot by vm %s" %ModuleData.snapshot_name)
        r = self.snp_api.createVmSnapshot(ModuleData.snapshot_name, self.dm.snapshot_info)
        if r['status_code'] == self.dm.expected_status_code:
#             if DictCompare().isSubsetDict(xmltodict.parse(self.dm.snapshot_info), r['result']):
            LogPrint().info("PASS:Create snapshot by description %s success."%self.dm.description)
            self.flag=True
#             else:
#                 LogPrint().error("FAIL:Create snapshot by description %s fail." %self.dm.description)
#                 self.flag=False
        else:
            LogPrint().error("FAIL:Create offline snapshot fail.The status_code is '%s'."%r['status_code'])
            self.flag=False
        self.assertTrue(self.flag)

class scenarios2_Snapshot(BaseTestCase):
    '''
    @summary: 克隆和恢复快照；
    @note: 克隆快照需要虚拟机状态为down的时候，才能进行恢复快照；
    '''
    
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.snp_api = VmSnapshotAPIs()
        self.vmapi=VirtualMachineAPIs()
        
    def test_cloneVmFromSnapshot(self):
        LogPrint().info("Test:Clone offline_snapshot from VM '%s' as a vm machine" %ModuleData.snapshot_name)
        def is_snapshot_OK():
            return self.snp_api.getVmSnapshotStatus(ModuleData.snapshot_name,self.dm.snapshot_id)=='ok'
        if wait_until(is_snapshot_OK, 300, 5):
            LogPrint().info("INFO-STEP: Create offsnapshot vm '%s' finished." % self.dm.cloneVmname)
        r = self.snp_api.cloneVmFromSnapshot(self.dm.xml_clone_vm_option)
        if r['status_code'] == self.dm.expected_status_code_create_vm:
            print r['status_code']
            #if DictCompare().isSubsetDict(xmltodict.parse(self.dm.xml_clone_vm_option), r['result']):
            LogPrint().info("PASS: Clone a offline_snapshot by description '%s' as a vm machine SUCCESS." %self.dm.description) 
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG when creating vm '%s'." % (r['status_code'], ModuleData.snapshot_name))
            self.flag = False
        self.assertTrue(self.flag)
        
    def test_restoreVmSnapshot(self):
        LogPrint().info("Test:Restore vm '%s' snapshot" %ModuleData.snapshot_name)
        def is_vm_down():
            return self.vmapi.getVmStatus(self.dm.cloneVmname)=='down'
        if wait_until(is_vm_down, 300, 5):
            LogPrint().info("INFO-STEP: clone vm '%s' finished." % self.dm.cloneVmname)
        r = self.snp_api.restoreVmSnapshot(ModuleData.snapshot_name, self.dm.snapshot_id)
        if r['status_code'] == self.dm.expected_status_code_restore_vm:
            LogPrint().info("PASS: Restore offline_snapshot form vm '%s' SUCCESS." %ModuleData.snapshot_name)
            self.flag = True        
        else:
            LogPrint.info("FAIL: Returned status code '%s' is WRONG when restore snaphot" %r['status_code'])
            self.flag = False
        self.assert_(self.flag)
        smart_del_vm(self.dm.cloneVmname, xml_del_vm_option=None, status_code=200)
        
class scenarios3_Snapshot(BaseTestCase):
    
    '''
    @summary: 创建单独磁盘在线快照；
    @note: 创建快照之前虚拟机必须处于开机状态；
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.snp_api = VmSnapshotAPIs()
        self.vmdisk_api = VmDiskAPIs() 
        self.vmapi = VirtualMachineAPIs           
        smart_start_vm(ModuleData.snapshot_name, self.dm.xml_start_vm_once, status_code=200)
         
    def test_CreateSnapshot_online(self):
        LogPrint().info("Test:Create a online with disk snapshot from vm '%s'" %ModuleData.snapshot_name)
        r = self.snp_api.createVmSnapshot(ModuleData.snapshot_name, self.dm.xml_snapshotOnline_info) 
        if r['status_code'] == self.dm.expected_status_code_SnapshotOnline:
            LogPrint().info("PASS:Create online with disk snapshot for vm '%s' SUCESS" %ModuleData.snapshot_name)
            self.flag = True
        else:
            LogPrint().info("FAIL: Returned status code '%s' is WRONG when create online with disk." %r['status_code'])
            self.flag = False   
        self.assertTrue(self.flag)
    
        
class scenarios4_Snapshot(BaseTestCase):
    
    '''
    @summary: 克隆和恢复在线快照；
    @note: 恢复和克隆在线快照之前虚拟机必须处于关机状态；
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.cloneapi = VmSnapshotAPIs()
        self.vmapi=VirtualMachineAPIs()
        
    def test_CloneVmFrom_OnlineSnapshot(self):
        LogPrint().info("Test:Clone Online_snapshot from VM '%s' as a vm machine" %ModuleData.snapshot_name)
        def is_snapshot_OK():
            return self.cloneapi.getVmSnapshotStatus(ModuleData.snapshot_name,self.dm.snapshot_id)=='ok'
        if wait_until(is_snapshot_OK, 300, 5):
            LogPrint().info("INFO-STEP: Create onlinesnapshot vm '%s' finished." % self.dm.cloneVmname)
        r = self.cloneapi.cloneVmFromSnapshot(self.dm.xml_clone_vm_option)
        if r['status_code'] == self.dm.expected_status_code_Clone_vm:
            #if DictCompare().isSubsetDict(xmltodict.parse(self.dm.xml_clone_vm_option), r['result']):
            LogPrint().info("PASS: Clone a Online_snapshot by description '%s' as a vm machine SUCCESS." % self.dm.snapshot_description) 
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code '%s' is WRONG when creating vm '%s'." % (r['status_code'], ModuleData.snapshot_name))
            self.flag = False
        self.assertTrue(self.flag)
        
        
    def test_RestoreVM_onlineSnapshot(self):
        def is_vm_down():
            return self.vmapi.getVmStatus(self.dm.cloneVmname)=='down'
        if wait_until(is_vm_down, 300, 5):
            LogPrint().info("INFO-STEP: clone vm '%s' finished." % self.dm.cloneVmname)
        smart_stop_vm(ModuleData.snapshot_name, status_code=200)
        LogPrint().info("Test:Restore a online with disk snapshot from vm '%s'" %ModuleData.snapshot_name)
        r = self.cloneapi.restoreVmSnapshot(ModuleData.snapshot_name,self.dm.snapshot_id, self.dm.xml_restore_vm_option)
        if r['status_code'] == self.dm.expect_status_code_clone:
            LogPrint().info("PASS:Restore online snapshot with disk SUCESS")
            self.flag=True
        else:
            LogPrint().info("FAIL: Returned status code '%s' is WRONG")
            self.flag = False
        self.assertTrue(self.flag) 
        smart_del_vm(ModuleData.snapshot_name, xml_del_vm_option=None, status_code=200)
        smart_del_vm(self.dm.cloneVmname, xml_del_vm_option=None, status_code=200)

        

#     def test_RestoreSnapshot_Online(self):
#         LogPrint().info("Test:Restore a onlinewith disk snapshot from vm '%s'" %ModuleData.snapshot_name)
                                 
class ITC05_TearDown(BaseTestCase):
    '''
    @summary: “虚拟机管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: （1）删除虚拟机
    @note: （2）将导出域设置为Maintenance状态；分离导出域；
    @note: （3）将数据中心里的Data域（data1）设置为Maintenance状态,并从数据中心内分离；
    @note: （4）将data2域设置为Maintenance状态；
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
        '''
        @summary: 模块级测试资源清理
        '''
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
         
        # Step1：删除虚拟机
        LogPrint().info("Post-Module-Test-1: Delete vm '%s'." % ModuleData.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
         
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
         
        # Step8：删除集群cluster1
        if capi.searchClusterByName(self.dm.cluster_nfs_name)['result']['clusters']:
            LogPrint().info("Post-Module-Test-8: Delete Cluster '%s'." % self.dm.cluster_nfs_name)
            self.assertTrue(capi.delCluster(self.dm.cluster_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)
            
if __name__ == "__main__":

    test_cases = ["VirtualMachine.scenarios4_Snapshot"]

    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)
    
    
