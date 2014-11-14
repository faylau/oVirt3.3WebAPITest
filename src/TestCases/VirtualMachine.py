#coding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>', '"Keke Wei" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/11/03      初始版本                                                            Liu Fei / keke wei
#---------------------------------------------------------------------------------
'''

from BaseTestCase import BaseTestCase
from TestAPIs.DataCenterAPIs import DataCenterAPIs,smart_attach_storage_domain,smart_deactive_storage_domain, smart_detach_storage_domain
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs,VmDiskAPIs,VmNicAPIs,\
    smart_create_vmdisk, smart_delete_vmdisk, smart_create_vm, smart_del_vm,\
smart_start_vm, smart_deactive_vmdisk,smart_create_vmnic,smart_delete_vmnic,\
    smart_start_vm, smart_deactive_vmdisk, smart_suspend_vm,smart_stop_vm
from TestAPIs.TemplatesAPIs import TemplatesAPIs, TemplateDisksAPIs,\
    TemplateNicsAPIs,smart_create_template,smart_create_tempnic,smart_delete_template,\
    smart_delete_tempnic
from TestAPIs.HostAPIs import smart_create_host,smart_del_host
from TestAPIs.StorageDomainAPIs import smart_create_storage_domain,smart_del_storage_domain,\
    StorageDomainAPIs
from TestAPIs.TemplatesAPIs import TemplatesAPIs, TemplateDisksAPIs, TemplateNicsAPIs,smart_create_template,smart_create_tempnic,smart_delete_template, smart_delete_tempnic
from TestAPIs.HostAPIs import smart_create_host,smart_del_host, HostAPIs
from TestAPIs.StorageDomainAPIs import smart_create_storage_domain,smart_del_storage_domain, StorageDomainAPIs

from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs,VmDiskAPIs,VmNicAPIs, smart_create_vmdisk, smart_delete_vmdisk, smart_create_vm, smart_del_vm,\
    smart_start_vm, smart_create_vmnic,smart_delete_vmnic, smart_deactive_vmdisk, smart_suspend_vm
from TestAPIs.TemplatesAPIs import TemplatesAPIs, TemplateDisksAPIs, TemplateNicsAPIs, smart_create_template, smart_create_tempnic, smart_delete_template, smart_delete_tempnic
from TestAPIs.HostAPIs import smart_create_host,smart_del_host, HostAPIs
from TestAPIs.StorageDomainAPIs import smart_create_storage_domain,smart_del_storage_domain, StorageDomainAPIs
from TestAPIs.NetworkAPIs import NetworkAPIs
from TestAPIs.DiskAPIs import DiskAPIs,smart_create_disk,smart_delete_disk
import TestData.VirtualMachine.ITC05_SetUp as ModuleData

from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare,wait_until
from Utils.HTMLTestRunner import HTMLTestRunner

import unittest
import xmltodict
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
        r = self.vmapi.createVm(self.dm.vm_info)
        if r['status_code'] == 201:
            self.vm_name = r['result']['vm']['name']
        else:
            LogPrint().error("Create vm failed.Status-code is wrong.")
            self.assertTrue(False)
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
                LogPrint().info("PASS: Get vm '%s' info success." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Get vm '%s' info INCORRECT." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
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
                LogPrint().info("PASS: Create vm '%s' success." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Create vm '%s' FAILED, returned vm info are INCORRECT." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is Wrong when creating vm '%s'." % (r['status_code'], self.dm.vm_name))
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
            LogPrint().error("FAIL: Returned status code '%s' is Wrong when creating vm with dup name '%s'." % (r['status_code']))
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
                LogPrint().error("FAIL: Returned status code '%s' is Wrong when creating vm with invalid name '%s'." % (r['status_code']))
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
                LogPrint().error("FAIL: Returned status code '%s' is Wrong when creating vm without parameters (name/cluster/template).")
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
            LogPrint().error("FAIL: Returned status code '%s' is Wrong when edit vm with dup name '%s'." % (r['status_code']))
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的虚拟机；
        '''
        LogPrint().info("Post-Test: Delete vm '%s'." % self.dm.vm_name)
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
                LogPrint().info("PASS: Delete vm '%s' success." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Delete vm '%s' FAILED." % self.dm.vm_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
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
        LogPrint().info("Pre-Test: Create a vm with name '%s'." % self.dm.vm_name)
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
            LogPrint().error("FAIL: Returned status code '%s' is Wrong." % r['status_code'])
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
            LogPrint().error("FAIL: Returned status code '%s' is Wrong while deleting vm '%s' without disk." % (r['status_code'], self.dm.vm_name))
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
        self.dm = super(self.__class__, self).setUp()        
        # 前提1：创建一个虚拟机vm1
        LogPrint().info("Pre-Test-1: Create a vm with name '%s'." % self.dm.vm_name)
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
            LogPrint().error("FAIL: Returned status code '%s' is Wrong while force deleting vm '%s'." % (r['status_code'], self.dm.vm_name))
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        '''
        @summary: 资源清理
        @note: （1）删除创建的磁盘；
        @note: （1）删除创建的虚拟机。
        '''
        LogPrint().info("Post-Test-1: Delete vm '%s' if it exist." % self.dm.vm_name)
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
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        
    def test_StartVm_Down_NoDisk_MultiStartDevices(self):
        '''
        @summary: 测试步骤
        @note: （1）运行虚拟机；
        @note: （2）操作成功，检查接口返回的状态码、相关信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Start vm '%s' without disk in 'down' state (have multi-start devices)." % self.dm.vm_name)
        r = vm_api.startVm(self.dm.vm_name)
        def is_vm_up():
            return vm_api.getVmStatus(self.dm.vm_name)=='up'
        if wait_until(is_vm_up, 300, 5):
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
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        
        # 前提2：为虚拟机vm1创建一个虚拟磁盘disk1
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
        if wait_until(is_vm_up, 300, 5):
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

class ITC05020102_StartVm_Suspended(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-01启动-02Suspended状态
    '''
    def setUp(self):
        '''
        @summary: 初始化测试数据、测试环境。
        '''
        # 初始化测试环境
        self.dm = super(self.__class__, self).setUp()
        
        # 前提1：创建一个虚拟机vm1（第一启动设备为cd-rom）
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        
        # 前提2：启动虚拟机，然后将其设置为suspended状态。
        self.assertTrue(smart_start_vm(self.dm.vm_name))
        self.assertTrue(smart_suspend_vm(self.dm.vm_name))
        
    def test_StartVm_Down_StartFromHd(self):
        '''
        @summary: 测试步骤
        @note: （1）运行虚拟机；
        @note: （2）操作成功，检查接口返回的状态码、提示信息是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        LogPrint().info("Test: Start vm '%s' with disk in 'suspended' state." % self.dm.vm_name)
        r = vm_api.startVm(self.dm.vm_name)
        def is_vm_up():
            return vm_api.getVmStatus(self.dm.vm_name)=='up'
        if wait_until(is_vm_up, 300, 5):
            if r['status_code'] == self.dm.expected_status_code_start_vm_from_suspended:
                LogPrint().info("PASS: Start vm '%s' from 'suspended' state SUCCESS." % self.dm.vm_name)
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
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.xml_vm_info))
        
        # 前提2：为虚拟机vm1创建一个磁盘disk1
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
        if wait_until(is_vm_up, 300, 5):
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
        if wait_until(is_vm_paused, 300, 5):
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
        LogPrint().info("Pre-Test-1: Create a vm '%s' for test." % self.dm.vm_name)
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
            if wait_until(is_vm_down, 300, 5):
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
        LogPrint().info("Pre-Test-1: Create a vm '%s' for test." % self.dm.vm_name)
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

class ITC05020301_ShutdownVm_Up(BaseTestCase):
    '''
    @summary: ITC-05虚拟机管理-02生命周期管理-03关闭-01Up状态
    @todo: 未完成，有OS的虚拟机才能正常shutdown，目前自动化测试环境中没有这样的虚拟机。
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
        
    def test_StopVm_Down(self):
        '''
        @summary: 测试步骤
        @note: （1）对UP状态虚拟机进行Shutdown操作；
        @note: （2）操作成功，验证接口返回的状态码、虚拟机最终状态是否正确。
        '''
        vm_api = VirtualMachineAPIs()
        def is_vm_down():
            return vm_api.getVmStatus(self.dm.vm_name)=='down'
        LogPrint().info("Test: Shutdown vm '%s' from 'up' state." % self.dm.vm_name)
        r = vm_api.shutdownVm(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_shutdown_vm:
            if wait_until(is_vm_down, 300, 5):
                LogPrint().info("PASS: Returned status code and info are CORRECT while shutdown vm '%s' from 'up' state." % self.dm.vm_name)
                self.flag = True
            else:
                LogPrint().error("FAIL: Shutdown vm '%s' FAILED. It's final state is not 'down'." % self.dm.vm_name)
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
        LogPrint().info("Test: Shutdown vm '%s' from 'up' state." % self.dm.vm_name)
        r = vm_api.shutdownVm(self.dm.vm_name)
        if r['status_code']==self.dm.expected_status_code_shutdown_vm_suspended:
            if wait_until(is_vm_down, 300, 5):
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
        LogPrint().info("Pre-Test-1: Create a vm '%s' for test." % self.dm.vm_name)
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
            if wait_until(is_vm_suspended, 300, 5):
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
        LogPrint().info("Post-Test-1: Delete vm '%s'." % self.dm.vm_name)
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
        LogPrint().info("Pre-Test-1: Create a vm '%s' for test." % self.dm.vm_name)
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
        def is_vm_up():
            return vm_api.getVmStatus(self.dm.vm_name)=='up'
        vm_api = VirtualMachineAPIs()
        host_api = HostAPIs()
        LogPrint().info("Test: Begin to migrate vm '%s' by Auto-Select host way." % self.dm.vm_name)
        r = vm_api.migrateVm(self.dm.vm_name, self.dm.xml_migrate_vm_option)
        if r['status_code'] == self.dm.expected_status_code_migrate_vm:
            if wait_until(is_vm_up, 300, 5) and vm_api.getVmInfo(self.dm.vm_name)['result']['vm']['host']['@id']==host_api.getHostIdByName(self.dm.host2_name):
                LogPrint().info("PASS: Migrate vm '%s' from '%s' to '%s' SUCCESS." % (self.dm.vm_name, ModuleData.host1_name, self.dm.host2_name))
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
            if wait_until(is_vm_up, 300, 5) and vm_api.getVmInfo(self.dm.vm_name)['result']['vm']['host']['@id']==host_api.getHostIdByName(self.dm.host2_name):
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
        if r['status_code'] == self.dm.expected_status_code_migrate_vm and wait_until(is_vm_migrating, 300, 5):
            LogPrint().info("Test-Info-1: Vm '%s' is in 'migrating' state." % self.dm.vm_name)
            LogPrint().info("Test-Step-2: Begin 'Cancel-Migration' action.")
            r1 = vm_api.cancelMigration(self.dm.vm_name)
            if r1['status_code']==self.dm.expected_status_code_cancel_migration:
                if wait_until(is_vm_up, 300, 5) and vm_api.getVmInfo(self.dm.vm_name)['result']['vm']['host']['@id']==host_api.getHostIdByName(ModuleData.host1_name):
                    LogPrint().info("PASS: Cancel Migration SUCCESS.")
                    self.flag = True
                else:
                    LogPrint().error("FAIL: Cancel Migration FAILED. Vm's final state is not 'Up' or vm's host is Wrong.")
                    self.flag = False
            else:
                LogPrint().error("FAIL: Returned status code '%s' is WRONG while Cancel-Migration." % r1['status_code'])
                self.flag = False
            self.assertTrue(self.flag)
        else:
            LogPrint().error("Test-Step1-FAIL: Migrate vm '%s' FAILED. Maybe the vm's state is not 'migrating'." % self.dm.vm_name)
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

class ITC05030401_UpdateVMDisk_vmdown(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-04编辑磁盘-01虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
    
    def test_active(self):
        self.flag=True
        r = self.vmdisk_api.updateVmDisk(ModuleData.vm_name, self.dm.disk_name, self.dm.update_disk_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare=DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.update_disk_info), r['result']):
                LogPrint().info("Update  active vmdisk '%s' success."%self.dm.disk_name)
            else:
                LogPrint().info("Update active vmdisk '%s' fail.The disk-info is wrong."%self.dm.disk_name)
                self.flag=False
        else:
            LogPrint().info("Update active vmdisk '%s' fail.The status_code is wrong."%self.dm.disk_name)
            self.flag=False
        self.assertTrue(self.flag)
    
    def test_deactive(self):
        self.flag=True
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
        r = self.vmdisk_api.updateVmDisk(ModuleData.vm_name, self.dm.disk_name, self.dm.update_disk_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare=DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.update_disk_info), r['result']):
                LogPrint().info("Update  deactive vmdisk '%s' success."%self.dm.disk_name)
            else:
                LogPrint().info("Update deactive vmdisk '%s' fail.The disk-info is wrong."%self.dm.disk_name)
                self.flag=False
        else:
            LogPrint().info("Update deactive vmdisk '%s' fail.The status_code is wrong."%self.dm.disk_name)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name_new))



class ITC05030402_UpdateVMDisk_vmrun(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-04编辑磁盘-02虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 300, 10):
            LogPrint().info("Start vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Start vm overtime.")
            self.assertTrue(False)
    
    def test_active(self):
        self.flag=True
        r = self.vmdisk_api.updateVmDisk(ModuleData.vm_name, self.dm.disk_name, self.dm.update_disk_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare=DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.update_disk_info), r['result']):
                LogPrint().info("Update  active vmdisk '%s' success."%self.dm.disk_name)
            else:
                LogPrint().info("Update active vmdisk '%s' fail.The disk-info is wrong."%self.dm.disk_name)
                self.flag=False
        else:
            LogPrint().info("Update active vmdisk '%s' fail.The status_code is wrong."%self.dm.disk_name)
            self.flag=False
        self.assertTrue(self.flag)
    
    def test_deactive(self):
        self.flag=True
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
        r = self.vmdisk_api.updateVmDisk(ModuleData.vm_name, self.dm.disk_name, self.dm.update_disk_info)
        if r['status_code']==self.dm.expected_status_code:
            dictCompare=DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.update_disk_info), r['result']):
                LogPrint().info("Update  deactive vmdisk '%s' success."%self.dm.disk_name)
            else:
                LogPrint().info("Update deactive vmdisk '%s' fail.The disk-info is wrong."%self.dm.disk_name)
                self.flag=False
        else:
            LogPrint().info("Update deactive vmdisk '%s' fail.The status_code is wrong."%self.dm.disk_name)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name_new))
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 300, 10):
            LogPrint().info("Stop vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)  
            
class ITC05030501_DeleteVMDisk_option(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-05删除磁盘-01是否永久删除
    '''  
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
    def test_detach(self):
        '''
        @summary: 将磁盘从虚拟机分离，而不删除
        '''
        self.flag=True
        r=self.vmdisk_api.delVmDisk(ModuleData.vm_name, disk_id=self.disk_id,xml_del_disk_option=self.dm.del_disk_option_detach)
        if r['status_code']==self.dm.expected_status_code:
            if not self.vmdisk_api.is_vmdisk_exist(ModuleData.vm_name, self.disk_id) \
            and DiskAPIs().isExist(self.disk_id):
                LogPrint().info("Detach disk from vm success.")
            elif self.vmdisk_api.is_vmdisk_exist(ModuleData.vm_name, self.disk_id):
                LogPrint().error("Detach disk from vm fail.")
                self.flag=False
            elif not DiskAPIs().isExist(self.disk_id):
                LogPrint().error("Disk is also deleted.")
                self.flag=False
        else:
            LogPrint().error("Detach disk from vm fail.Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    
    def test_remove(self):
        '''
        @summary: 将磁盘从虚拟机永久删除
        '''
        self.flag=True
        r=self.vmdisk_api.delVmDisk(ModuleData.vm_name, disk_id=self.disk_id,xml_del_disk_option=self.dm.del_disk_option_remove)
#         time.sleep(30)
        if r['status_code']==self.dm.expected_status_code:
            if not self.vmdisk_api.is_vmdisk_exist(ModuleData.vm_name, self.disk_id) \
            and not DiskAPIs().isExist(self.disk_id):
                LogPrint().info("Remove disk from vm success.")
            elif self.vmdisk_api.is_vmdisk_exist(ModuleData.vm_name, self.disk_id):
                LogPrint().error("Remove disk from vm fail.")
                self.flag=False
            elif DiskAPIs().isExist(self.disk_id):
                LogPrint().error("Disk is still exist.")
                self.flag=False
        else:
            LogPrint().error("Remove disk from vm fail.Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_disk(self.disk_id)) 

class ITC05030502_DeleteActiveVMDisk_vmrun(BaseTestCase):    
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-05删除磁盘-02磁盘激活状态，虚拟机运行
    ''' 
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        #启动虚拟机
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 300, 10):
            LogPrint().info("Start vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Start vm overtime.")
            self.assertTrue(False)
    def test(self):
        self.flag=True
        r=self.vmdisk_api.delVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        if r['status_code'] == self.dm.expected_status_code:
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                    LogPrint().info("PASS:ITC05030502_DeleteActiveVMDisk_vmrun")
                else:
                    LogPrint().error("FAIL:ITC05030502_DeleteActiveVMDisk_vmrun.Error-info is wrong.")
                    self.flag=False
        else:
                LogPrint().error("FAIL:ITC05030502_DeleteActiveVMDisk_vmrun.Status-code is wrong.")
                self.flag=False
        
    def tearDown(self):
        
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 300, 10):
            LogPrint().info("Stop vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))  
        
class ITC05030601_activeVMDisk_vmrun(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-06激活磁盘-01虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
        #启动虚拟机
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 300, 10):
            LogPrint().info("Start vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Start vm overtime.")
            self.assertTrue(False)
    def test_active(self):
        self.flag=True
        r=self.vmdisk_api.activateVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        def is_disk_active():
            return VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name, disk_id=self.disk_id)['result']['disk']['active']=='true'
        if r['status_code']==self.dm.expected_status_code:
            if wait_until(is_disk_active, 60, 10):
                LogPrint().info("Active vmdisk success when vm is down.")
            else:
                LogPrint().error("Active vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("Active vmdisk fail when vm is down.Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 300, 10):
            LogPrint().info("Stop vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))

class ITC05030602_activeVMDisk_vmdown(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-06激活磁盘-02虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
    def test_active(self):
        self.flag=True
        r=self.vmdisk_api.activateVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        def is_disk_active():
            return VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name, disk_id=self.disk_id)['result']['disk']['active']=='true'
        if r['status_code']==self.dm.expected_status_code:
            if wait_until(is_disk_active, 60, 10):
                LogPrint().info("Active vmdisk success when vm is down.")
            else:
                LogPrint().error("Active vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("Active vmdisk fail when vm is down.Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))

class ITC05030701_deactiveVMDisk_vmrun(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-07取消激活磁盘-01虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 300, 10):
            LogPrint().info("Pre-Test:Start vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Pre-Test:Start vm overtime.")
            self.assertTrue(False)
    def test_deactive(self):
        self.flag=True
        r=self.vmdisk_api.deactivateVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        def is_disk_deactive():
            return VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name, disk_id=self.disk_id)['result']['disk']['active']=='false'
        if r['status_code']==self.dm.expected_status_code:
            if wait_until(is_disk_deactive, 60, 10):
                LogPrint().info("Deactive vmdisk success when vm is running.")
            else:
                LogPrint().error("Deactive vmdisk overtime when vm is running.")
                self.flag=False
        else:
            LogPrint().error("Deactive vmdisk fail when vm is running.Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 300, 10):
            LogPrint().info("Stop vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
        
class ITC05030702_deactiveVMDisk_vmdown(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-07取消激活磁盘-02虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
    def test_deactive(self):
        self.flag=True
        r=self.vmdisk_api.deactivateVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        def is_disk_deactive():
            return VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name, disk_id=self.disk_id)['result']['disk']['active']=='false'
        if r['status_code']==self.dm.expected_status_code:
            if wait_until(is_disk_deactive, 60, 10):
                LogPrint().info("Deactive vmdisk success when vm is down.")
            else:
                LogPrint().error("Deactive vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("Deactive vmdisk fail when vm is down.Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))

class ITC05030801_MoveactiveVMDisk_vmdown(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-08移动激活的磁盘-01虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
    def test_move(self):
        self.flag=True
        r=self.vmdisk_api.moveVmDisk(ModuleData.vm_name, self.dm.move_option, self.disk_id)
        def is_disk_ok():
            return VmDiskAPIs().getVmDiskStatus(ModuleData.vm_name, disk_id=self.disk_id)=='ok'
        if r['status_code']==self.dm.expected_status_code:
            if wait_until(is_disk_ok, 600, 10):
                if VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name,disk_id=self.disk_id)['result']['disk']['storage_domains']\
                ['storage_domain']['@id']==StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data2_nfs_name):
                    LogPrint().info("Move vmdisk success when vm is down.")
                else:
                    LogPrint().error("Move vmdisk fail when vm is down.The des-storage is wrong.")
                    self.flag=False
            else:
                LogPrint().error("Move vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("Move vmdisk fail when vm is down.Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))

class ITC05030802_MoveactiveVMDisk_vmrun(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-08移动激活的磁盘-02虚拟机运行
    @note: 虚拟机运行时，磁盘是否共享，移动激活磁盘结果不同
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r_unshare=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info_unshare, self.dm.disk_name_unshare)
        self.disk_id_unshare = r_unshare[1]
        self.assertTrue(r_unshare[0])
        r_share=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info_share, self.dm.disk_name_share)
        self.disk_id_share = r_share[1]
        self.assertTrue(r_share[0])
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 300, 10):
            LogPrint().info("Pre-Test:Start vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Pre-Test:Start vm overtime.")
            self.assertTrue(False)
    def test_move_unshare(self):
        '''
        @note: 磁盘设置为非共享的
        '''
        self.flag=True
        r=self.vmdisk_api.moveVmDisk(ModuleData.vm_name, self.dm.move_option, self.disk_id_unshare)
        def is_disk_ok():
            return VmDiskAPIs().getVmDiskStatus(ModuleData.vm_name, disk_id=self.disk_id_unshare)=='ok'
        if r['status_code']==self.dm.expected_status_code_unshare:
            if wait_until(is_disk_ok, 600, 10):
                if VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name,disk_id=self.disk_id_unshare)['result']['disk']['storage_domains']\
                ['storage_domain']['@id']==StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data2_nfs_name):
                    LogPrint().info("Move vmdisk success when vm is down.")
                else:
                    LogPrint().error("Move vmdisk fail when vm is down.The des-storage is wrong.")
                    self.flag=False
            else:
                LogPrint().error("Move vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("Move vmdisk fail when vm is down.Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
        
    def test_move_share(self):
        '''
        @note: 磁盘设置为共享的
        '''
        self.flag=True
        r=self.vmdisk_api.moveVmDisk(ModuleData.vm_name, self.dm.move_option, self.disk_id_share)
        if r['status_code']==self.dm.expected_status_code_share:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Can't move active and sharable vmdisk when vm is running.")
            else:
                LogPrint().error("FAIL:Error-info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 300, 10):
            LogPrint().info("Stop vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name_share))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name_unshare))

class ITC05030901_MovedeactiveVMDisk_vmdown(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-09移动非激活的磁盘-01虚拟机关机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        #取消激活磁盘
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
    def test_move(self):
        self.flag=True
        r=self.vmdisk_api.moveVmDisk(ModuleData.vm_name, self.dm.move_option, self.disk_id)
        print r
        def is_disk_ok():
            return VmDiskAPIs().getVmDiskStatus(ModuleData.vm_name, disk_id=self.disk_id)=='ok'
        if r['status_code']==self.dm.expected_status_code:
            if wait_until(is_disk_ok, 600, 10):
                if VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name,disk_id=self.disk_id)['result']['disk']['storage_domains']\
                ['storage_domain']['@id']==StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data2_nfs_name):
                    LogPrint().info("Move vmdisk success when vm is down.")
                else:
                    LogPrint().error("Move vmdisk fail when vm is down.The des-storage is wrong.")
                    self.flag=False
            else:
                LogPrint().error("Move vmdisk overtime when vm is down.")
                self.flag=False
        else:
            LogPrint().error("Move vmdisk fail when vm is down.Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
        
class ITC05030902_MovedeactiveVMDisk_vmrun(BaseTestCase):
    '''
    @summary: 05虚拟机管理-03虚拟机磁盘管理-09移动非激活的磁盘-02虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        #启动虚拟机
        VirtualMachineAPIs().startVm(ModuleData.vm_name)
        def is_vm_up():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='up'
        if wait_until(is_vm_up, 300, 10):
            LogPrint().info("Pre-Test:Start vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Pre-Test:Start vm overtime.")
            self.assertTrue(False)
        #取消激活磁盘
        self.assertTrue(smart_deactive_vmdisk(ModuleData.vm_name, self.disk_id))
        
    def test_move(self):
        self.flag=True
        r=self.vmdisk_api.moveVmDisk(ModuleData.vm_name, self.dm.move_option, self.disk_id)
        def is_disk_ok():
            return VmDiskAPIs().getVmDiskStatus(ModuleData.vm_name, disk_id=self.disk_id)=='ok'
        if r['status_code']==self.dm.expected_status_code:
            if wait_until(is_disk_ok, 600, 10):
                if VmDiskAPIs().getVmDiskInfo(ModuleData.vm_name,disk_id=self.disk_id)['result']['disk']['storage_domains']\
                ['storage_domain']['@id']==StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data2_nfs_name):
                    LogPrint().info("Move vmdisk success when vm is down.")
                else:
                    LogPrint().error("Move vmdisk fail when vm is down.The des-storage is wrong.")
                    self.flag=False
            else:
                LogPrint().error("Move vmdisk overtime when vm is down.")
                self.flag=False
        else:
            print r
            LogPrint().error("Move vmdisk fail when vm is down.Status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 300, 10):
            LogPrint().info("Stop vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))

class ITC050310_statisticsVmDisk(BaseTestCase):
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmdisk_api = VmDiskAPIs()
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
    def test(self):
        self.flag=True
        r = self.vmdisk_api.statisticsVmDisk(ModuleData.vm_name, disk_id=self.disk_id)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("PASS:Get statistics of vmdisk success.")
        else:
            LogPrint().error("FAIL:Get statistics of vmdisk fail.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))

class ITC050401_GetVmNicList(BaseTestCase):
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
    def test(self):
        r=self.vmnic_api.getVmNicsList(ModuleData.vm_name)
        if r['status_code']==200:
            LogPrint().info("PASS:Get vmnic list success.")
            self.assertTru(True)
        else:
            LogPrint().error("FAIL:Get vmnic list fail.")
            self.assertTru(False)
          
class ITC050402_GetVmNicInfo(BaseTestCase):
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
    def test(self):
        self.flag=True
        r=self.vmnic_api.getVmNicInfo(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.nic_info), r['result']):
                LogPrint().info("PASS:Get vmnic info success.")
            else:
                LogPrint().error("FAIL:Get vmnic info fail.The info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Get vmnic info.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))

class ITC05040301_CreateVmNic_normal(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-03创建-01正常创建
    @note: 考虑有无配置集的两种情况
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
    def test_noproid(self):
        self.flag=True
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info_noproid)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.nic_info_noproid), r['result']):
                LogPrint().info("PASS:Create vmnic success.")
            else:
                LogPrint().error("FAIL:Create vmnic fail.The info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Create vmnic fail.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def test_proid(self):
        self.flag=True
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info_proid)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.nic_info_proid), r['result']):
                LogPrint().info("PASS:Create vmnic success.")
            else:
                LogPrint().error("FAIL:Create vmnic fail.The info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Create vmnic fail.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
    
class ITC05040302_CreateVmNic_dupname(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-03创建-02重名
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
    def test(self):
        self.flag=True
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Create vmnic success.")
            else:
                LogPrint().error("FAIL:Create vmnic fail.The info is wrong.")
                self.flag=False
                print xmltodict.unparse(r['result'],pretty=True)
        else:
            LogPrint().error("FAIL:Create vmnic fail.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
   
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))

class ITC05040303_CreateVmNic_norequired(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-03创建-03参数完整性
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
    def test_name(self):
        self.flag=True
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Returned status_code and error-info CORRECT.")
            else:
                LogPrint().error("FAIL:Returned error-info is wrong.")
                self.flag=False
                print xmltodict.unparse(r['result'],pretty=True)
        else:
            LogPrint().error("FAIL:Returned status_code is wrong.")
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
            
       
   
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
    
class ITC05040304_CreateVmNic_verifyname(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-03创建-04验证名称合法性
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
    def test(self):
        self.flag=True
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Returned status_code and error-info CORRECT.")
            else:
                LogPrint().error("FAIL:Returned error-info is wrong.")
                self.flag=False
                print xmltodict.unparse(r['result'],pretty=True)
        else:
            LogPrint().error("FAIL:Returned status_code is wrong.")
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)     
   
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))


  
class ITC05040305_CreateVmNic_verifymac(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-03创建-05 验证mac地址合法性
    '''
    def setUp(self): 
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
    def test(self):
        self.flag=True
        r = self.vmnic_api.createVmNic(ModuleData.vm_name, self.dm.nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Returned status_code and error-info CORRECT.")
            else:
                LogPrint().error("FAIL:Returned error-info is wrong.")
                self.flag=False
                print xmltodict.unparse(r['result'],pretty=True)
        else:
            LogPrint().error("FAIL:Returned status_code is wrong.")
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)     
   
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))




class ITC05040401_UpdateVmNic_normal(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-04编辑网络接口-01正常编辑
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
    def test(self):
        r=self.vmnic_api.updateVmNic(ModuleData.vm_name, self.dm.nic_name, self.dm.update_vm_nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.update_vm_nic_info), r['result']):
                LogPrint().info("PASS:Update vmnic success.")
            else:
                LogPrint().error("FAIL:Update vmnic fail.The info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Update vmnic fail.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.new_nic_name))

class ITC05040402_UpdateVmNic_dupname(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-04编辑网络接口-02重名
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info1, self.dm.nic_name1))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info2, self.dm.nic_name2))
    def test(self):
        r=self.vmnic_api.updateVmNic(ModuleData.vm_name, self.dm.nic_name1, self.dm.update_vm_nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Can not update nic dupname.")
            else:
                LogPrint().error("FAIL:The error-info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name1))     
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name2)) 

class ITC05040403_UpdateVmNic_type(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-04编辑网络接口-03编辑接口类型
    @note: 虚拟机运行状态下
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
        r=smart_create_vmdisk(ModuleData.vm_name,self.dm.disk_info, self.dm.disk_name)
        self.assertTrue(r[0])
        self.disk_id=r[1]
        self.assertTrue(smart_start_vm(ModuleData.vm_name))
    def test(self):
        r=self.vmnic_api.updateVmNic(ModuleData.vm_name, self.dm.nic_name, self.dm.update_vm_nic_info)
        print r
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.update_vm_nic_info), r['result']):
                LogPrint().info("PASS:Update vmnic type success.")
            else:
                LogPrint().error("FAIL:Update vmnic type fail.The info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Update vmnic type fail.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 300, 10):
            LogPrint().info("Stop vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        self.assertTrue(smart_delete_disk(self.disk_id))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))

class ITC05040404_UpdateVmNic_dupmac(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-04编辑网络接口-04mac已被使用
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info1, self.dm.nic_name1))
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info2, self.dm.nic_name2))
    def test(self):
        r=self.vmnic_api.updateVmNic(ModuleData.vm_name, self.dm.nic_name1, self.dm.update_vm_nic_info)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Can not update nic dupmac.")
            else:
                LogPrint().error("FAIL:The error-info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name1))     
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name2)) 

class ITC05040501_ActiveVmNic_vmrun(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-05激活网络接口-01虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
        self.assertTrue(smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name))
        self.assertTrue(smart_start_vm(ModuleData.vm_name))
    def test(self):
        r=self.vmnic_api.activateVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if self.vmnic_api.getVmNicInfo(ModuleData.vm_name, self.dm.nic_name)['result']['nic']['active']=='true':
                LogPrint().info("PASS:Active vmnic success when vm is running.")
            else:
                LogPrint().error("FAIL:Active vmnic fail when vm is running.The info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Active vmnic fail when vm is running.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_stop_vm(ModuleData.vm_name))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))

class ITC05040502_ActiveVmNic_vmdown(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-05激活网络接口
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
        
    def test(self):
        r=self.vmnic_api.activateVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if self.vmnic_api.getVmNicInfo(ModuleData.vm_name, self.dm.nic_name)['result']['nic']['active']=='true':
                LogPrint().info("PASS:Active vmnic success when vm is down.")
            else:
                LogPrint().error("FAIL:Active vmnic fail when vm is down.The info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Active vmnic fail when vm is down.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))

class ITC05040601_DeactiveVmNic_vmrun(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-06取消激活网络接口-01虚拟机运行
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
        self.assertTrue(smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name))
        self.assertTrue(smart_start_vm(ModuleData.vm_name))
    def test(self):
        r=self.vmnic_api.deactivateVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if self.vmnic_api.getVmNicInfo(ModuleData.vm_name, self.dm.nic_name)['result']['nic']['active']=='false':
                LogPrint().info("PASS:Deactive vmnic success when vm is running.")
            else:
                LogPrint().error("FAIL:Deactive vmnic fail when vm is running.The info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Deactive vmnic fail when vm is running.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_stop_vm(ModuleData.vm_name))
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))

class ITC05040602_DeactiveVmNic_vmdown(BaseTestCase):

    '''
    @summary: 05虚拟机管理-04网络接口-06取消激活网络接口
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
    def test(self):
        r=self.vmnic_api.deactivateVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if self.vmnic_api.getVmNicInfo(ModuleData.vm_name, self.dm.nic_name)['result']['nic']['active']=='false':
                LogPrint().info("PASS:Deactive vmnic success when vm is down.")
            else:
                LogPrint().error("FAIL:Deactive vmnic fail when vm is down.The info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Deactive vmnic fail when vm is down.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))
        
class ITC05040701_DeleteVmNic_vmdown_plugged(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-07删除网络接口-01虚拟机down
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
    def test(self):
        r=self.vmnic_api.delVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if not self.vmnic_api.isVmNicExist(ModuleData.vm_name, self.dm.nic_name):
                LogPrint().info("PASS:Delete vmnic success.")
            else:
                LogPrint().error("FAIL:Delete vmnic fail.The vmnic is still exist.")
                self.flag=False
        else:
            LogPrint().error("FAIL:Delete vmnic fail.The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))

class ITC05040702_DeleteVmNic_vmrun_plugged(BaseTestCase):
    '''
    @summary: 05虚拟机管理-04网络接口-07删除网络接口-02虚拟机run
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.vmnic_api = VmNicAPIs()
        self.assertTrue(smart_create_vmnic(ModuleData.vm_name, self.dm.nic_info, self.dm.nic_name))
        r=smart_create_vmdisk(ModuleData.vm_name, self.dm.disk_info, self.dm.disk_name)
        self.assertTrue(r[0])
        self.disk_id = r[1]
        self.assertTrue(smart_start_vm(ModuleData.vm_name))
    def test(self):
        r=self.vmnic_api.delVmNic(ModuleData.vm_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if DictCompare().isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS:Can not delete plugged nic when vm is running.")
            else:
                LogPrint().error("FAIL:The error-info is wrong.")
                self.flag=False
        else:
            LogPrint().error("FAIL:The status_code is '%s'."%r['status_code'])
            print xmltodict.unparse(r['result'],pretty=True)
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        VirtualMachineAPIs().stopVm(ModuleData.vm_name)
        def is_vm_down():
            return VirtualMachineAPIs().getVmStatus(ModuleData.vm_name)=='down'
        if wait_until(is_vm_down, 300, 10):
            LogPrint().info("Stop vm success.")
            self.assertTrue(True)
        else:
            LogPrint().info("Stop vm overtime.")
            self.assertTrue(False)
        self.assertTrue(smart_delete_vmdisk(ModuleData.vm_name, self.dm.disk_name))
        self.assertTrue(smart_delete_vmnic(ModuleData.vm_name, self.dm.nic_name))



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
        vmapi=VirtualMachineAPIs()
        #Step1：删除虚拟机
        vmapi.delVm(self.dm.vm_name)
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        # Step2：将export和iso存储域设置为Maintenance状态,然后从数据中心分离
        LogPrint().info("Post-Module-Test-1: Deactivate storage domains '%s'." % self.dm.export1_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        LogPrint().info("Post-Module-Test-1: Detach storage domains '%s'." % self.dm.export1_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        LogPrint().info("Post-Module-Test-1: Deactivate storage domains '%s'." % self.dm.iso1_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.iso1_name))
        LogPrint().info("Post-Module-Test-1: Detach storage domains '%s'." % self.dm.iso1_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.iso1_name))
        # Step3：将data1存储域设置为Maintenance状态，然后从数据中心分离
        LogPrint().info("Post-Module-Test-1: Deactivate data storage domains '%s'." % self.dm.data1_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
        LogPrint().info("Post-Module-Test-1: Detach data storage domains '%s'." % self.dm.data1_nfs_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
        
        # Step3：将data2存储域设置为Maintenance状态，然后从数据中心分离
        LogPrint().info("Post-Module-Test-1: Deactivate data storage domains '%s'." % self.dm.data2_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.data2_nfs_name))
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

if __name__ == "__main__":

    #import sys;sys.argv = ['', 'Test.testName']
    test_cases = ["VirtualMachine.ITC05_TearDown"]


    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)
    
    
