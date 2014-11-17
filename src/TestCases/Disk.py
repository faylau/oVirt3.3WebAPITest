#encoding:utf-8
'''

@author: keke
'''

import unittest
import time

from BaseTestCase import BaseTestCase
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare,wait_until
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs,VmDiskAPIs,\
    smart_create_vm,smart_del_vm, smart_start_vm, smart_stop_vm, smart_active_vmdisk
from TestAPIs.TemplatesAPIs import TemplatesAPIs, TemplateDisksAPIs,smart_create_template,smart_delete_tempnic,\
    smart_delete_template
from TestAPIs.DataCenterAPIs import DataCenterAPIs,smart_attach_storage_domain,smart_deactive_storage_domain
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.StorageDomainAPIs import smart_create_storage_domain,smart_del_storage_domain
from TestAPIs.DiskAPIs import DiskAPIs,smart_create_disk,smart_delete_disk
from TestAPIs.HostAPIs import smart_create_host,smart_del_host
import xmltodict


class ITC08_SetUp(BaseTestCase):
    '''
    @summary: 磁盘管理模块级测试用例，初始化模块测试环境；
    @note: （1）创建一个NFS类型数据中心；
    @note: （2）创建一个集群；
    @note: （3）创建一个主机，并等待其变为UP状态；
    @note: （4）创建3个存储域（data1/data2/ISO/Export）；
    @note: （5）将 data1 附加到数据中心。
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = super(self.__class__, self).setUp()
  
    def test_CreateModuleTestEnv(self):
        '''
        @summary: 创建Disk模块测试环境
        '''
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
      
        # 为NFS数据中心创建Data（data1/data2）。
        @BaseTestCase.drive_data(self, self.dm.xml_storage_info)
        def create_storage_domains(xml_storage_domain_info):
            sd_name = xmltodict.parse(xml_storage_domain_info)['storage_domain']['name']
            LogPrint().info("Pre-Module-Test-4: Create Data Storage '%s'." % sd_name)
            self.assertTrue(smart_create_storage_domain(sd_name, xml_storage_domain_info))
        create_storage_domains()
          
        # 将创建的的data1附加到NFS/ISCSI数据中心里（data2/Iso/Export处于游离状态）。
        LogPrint().info("Pre-Module-Test-5: Attach the data storages to data centers.")
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
  
    def tearDown(self):
        '''
        @summary: 资源清理
        '''
        pass
#  
#  
class ITC0801_GetDiskList(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-01获取所有磁盘列表
    '''
    def setUp(self):
        pass
    '''
    @summary: 测试用例执行步骤
    @note: （1）获取磁盘列表
                            （2）操作成功，验证返回状态码    
    '''
    def test_GetDiskList(self):
        LogPrint().info("Test: Get disk list.")
        diskapi = DiskAPIs()
        r = diskapi.getDisksList()
        if r['status_code'] == 200:
            LogPrint().info('PASS: Get Disk list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error("FAIL: Returned status code is %s. "% r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
     
class ITC0802_GetDiskInfo(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-02获取指定磁盘信息
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        #首先新建一个磁盘并获取id
        LogPrint().info("Pre-Test-1: Create Disk %s for TC."% self.dm.disk_name)
        r = smart_create_disk(self.dm.disk_info,self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
       
    def test_GetDiskInfo(self):
        '''
        @summary: 根据磁盘id获取磁盘信息
        @note: 操作成功，验证返回状态码，验证磁盘信息
        '''
        LogPrint().info("Test: Get disk %s info."% self.dm.disk_name)
        diskapi = DiskAPIs() 
        r = diskapi.getDiskInfo(self.disk_id)
        if r['status_code'] == self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.disk_info)
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("PASS:Get disk %s info SUCCESS."% self.dm.disk_name)
#                 return True
            else:
                LogPrint().error("FAIL:Returned disk info is WRONG.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is %s. "% r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        LogPrint().info("Post-Test-1: Delete Disk %s."% self.dm.disk_name)
        self.assertTrue(smart_delete_disk(self.disk_id))     
  
class ITC080301_CreateDisk(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-03创建磁盘-01成功创建
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
           
    def test_CreateDisk_iscsi_cow(self): 
        '''
        @note: 在iscsi存储域内创建cow类型磁盘
        @note: sprase必须设为true，sharable必须为false，否则报错
        '''
        self.flag = True
        diskapi = DiskAPIs()
        LogPrint().info("Test: Create cow type disk.")
        r = diskapi.createDisk(self.dm.disk_info_cow)
        def is_disk_ok():
            return diskapi.getDiskStatus(self.disk_id)=='ok'
        if r['status_code'] == self.dm.expected_status_code:
            self.disk_id = r['result']['disk']['@id']
            #如果磁盘状态在给定时间内变为ok状态，则继续验证状态码和磁盘信息
            if wait_until(is_disk_ok, 200, 5):
                dict_actual = r['result']
                dict_expected = xmltodict.parse(self.dm.disk_info_cow)
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(dict_expected, dict_actual):
                    LogPrint().info("PASS: Create cow disk SUCCESS." )
#                 return True
                else:
                    LogPrint().error("FAIL: The disk_info is WRONG")
                    self.flag = False
            else:
                LogPrint().error("FAIL: The disk status is not OK. " )
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is %s. "% r['status_code'])
            self.flag = False
          
    def test_CreateDisk_iscsi_raw(self): 
        '''
        @note: 在iscsi存储域内创建raw类型磁盘
        @note: 若format=raw，则sparse必须为false，否则报错
        '''
        self.flag = True
        diskapi = DiskAPIs()
        LogPrint().info("Test: Create raw type disk.")
        r = diskapi.createDisk(self.dm.disk_info_raw)
        def is_disk_ok():
            return diskapi.getDiskStatus(self.disk_id)=='ok'
        if r['status_code'] == self.dm.expected_status_code:
            self.disk_id = r['result']['disk']['@id']
            #如果磁盘状态在给定时间内变为ok状态，则继续验证状态码和磁盘信息
            if wait_until(is_disk_ok, 200, 5):
                dict_actual = r['result']
                dict_expected = xmltodict.parse(self.dm.disk_info_raw)
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(dict_expected, dict_actual):
                    LogPrint().info("PASS: Create raw disk SUCCESS." )
#                 return True
                else:
                    LogPrint().error("FAIL: The disk_info is WRONG")
                    self.flag = False
            else:
                LogPrint().error("FAIL: The disk status is not OK. " )
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is %s. "% r['status_code'])
            self.flag = False
             
    def tearDown(self):
        LogPrint().info("Post-Test-1: Delete Disk %s."% self.dm.disk_name)
        self.assertTrue(smart_delete_disk(self.disk_id))  
           
class ITC080302_CreateDisk_VerifyName(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-03创建磁盘-02验证名称合法性
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()  
           
    def test_CreateDisk_VerifyName(self):
        '''
        @summary: 验证名称合法性：包含非法字符
        @note: 操作失败，验证返回状态码及报错信息
        ''' 
        diskapi = DiskAPIs()
        LogPrint().info("Test: Create disk and verify name.")
        r = diskapi.createDisk(self.dm.disk_info)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS: The returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECT.")
                self.flag = False
        else:
                LogPrint().error("FAIL: The returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
                self.flag = False
        self.assertTrue(self.flag)
#          
class ITC080303_CreateDisk_NoRequired(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-03创建一个配置集-03验证参数完整性
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()  
           
    def test_CreateDisk_NoRequired(self):
        '''
        @summary: 分为四种情况,1）缺少存储域 2）缺少大小 3）缺少interface 4）缺少format 
        @note: 操作失败，验证错误验证码及错误信息
        ''' 
        self.expected_result_index = 0
        diskapi = DiskAPIs()
        @BaseTestCase.drive_data(self, self.dm.disk_info)
        def do_test(xml_info):
            self.flag = True
            r = diskapi.createDisk(xml_info)
            if r['status_code'] == self.dm.expected_status_code:
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
     
# class ITC080304_CreateDisk_ErrorSet(BaseTestCase):
#     '''
#     @summary: ITC-08磁盘管理-03创建一个配置集-04错误配置
#     @note: 该用例在ISCSI存储环境下生效
#     '''
#     def setUp(self):
#         '''
#         @summary: 测试用例执行前的环境初始化（前提）
#         '''
#         self.dm = super(self.__class__, self).setUp()
#           
#     def test_CreateDisk_ErrorSet(self):
#         '''
#         @summary: 分为三种情况
#         1）format=raw，sparse=true
#         2）format=cow，sparse=false
#         3）format=cow，sparse=true,sharable=true
#         @note: 操作失败，验证返回状态码及报错信息
#         ''' 
#         self.expected_result_index = 0
#         diskapi = DiskAPIs()
#         @BaseTestCase.drive_data(self, self.dm.disk_info)
#         def do_test(xml_info):
#             self.flag = True
#             r = diskapi.createDisk(xml_info)
#             print r
#             if r['status_code'] == self.dm.expected_status_code[self.expected_result_index]:
#                 dictCompare = DictCompare()
#                 if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info_list[self.expected_result_index]), r['result']):
#                     LogPrint().info("PASS: The returned status code and messages are CORRECT.")
#                 else:
#                     LogPrint().error("FAIL: The returned messages are INCORRECT.")
#                     self.flag = False
#             else:
#                 LogPrint().error("FAIL: The returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
#                 self.flag = False
#             self.assertTrue(self.flag)
#             self.expected_result_index += 1
#         do_test()
            
class ITC080401_DeleteDisk(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-04删除磁盘-01磁盘无关联
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test-1: Create disk %s for TC."% self.dm.disk_name)
        r = smart_create_disk(self.dm.disk_info, self.dm.disk_name)
        self.disk_id = r[1]
        self.assertTrue(r[0])
     
    def test_DeleteDisk(self):
        '''
        @summary: 测试执行步骤
        @note: 删除一个独立的磁盘，即没有附加在虚拟机和模板上
        @note: 操作成功，验证返回状态码，验证磁盘是否存在
        ''' 
        disk_api =  DiskAPIs()
        self.flag = True
        LogPrint().info("Test: Delete disk %s."% self.disk_id)
        r = disk_api.deleteDisk(self.disk_id)
        if r['status_code'] == self.dm.expected_status_code:
            if not disk_api.isExist(self.disk_id):
                LogPrint().info("PASS: Delete Disk SUCCESS." )
            else:
                LogPrint().error("FAIL: Disk is still exist. " )
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is %s. "% r['status_code'])
            self.flag = False
        self.assertTrue(self.flag)
     
    def tearDown(self):
        LogPrint().info("Post-Test-1: Delete Disk %s."% self.disk_id)
        self.assertTrue(smart_delete_disk(self.disk_id))
             
class ITC080402_DeleteDisk_AttachtoTemp(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-04删除磁盘-02磁盘附加到模板上
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        #创建一个虚拟机
        LogPrint().info("Pre-Test-1: Create vm %s for TC."% self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.vm_info))    
        #创建一块磁盘
        '''
        @note: 创建磁盘时，磁盘的sharable属性必须为false，因为共享磁盘不作为模板的一部份
        '''
        LogPrint().info("Pre-Test-2: Create a disk for TC.")
        r= smart_create_disk(self.dm.disk_info, self.dm.disk_name)
        self.assertTrue(r[0])
        self.disk_id = r[1]    
        #将该磁盘附加到虚拟机上
        LogPrint().info("Pre-Test-3: Attach disk %s to vm %s for TC."% (self.dm.disk_name
                                                                 ,self.dm.vm_name))
        self.vmdiskapi = VmDiskAPIs()
        r=self.vmdiskapi.attachDiskToVm(self.dm.vm_name, self.disk_id)
        if r['status_code'] == 200:
            LogPrint().info("Attach Disk to vm success.")
        else:
            LogPrint().error("Attach Disk to vm fail.Status-code is wrong.")
            self.assertTrue(False)    
        #该虚拟机创建模板   
        LogPrint().info("Pre-Test-4: Create template for vm %s for TC."% self.dm.vm_name)
        self.tempapi = TemplatesAPIs()
        self.vm_id = VirtualMachineAPIs().getVmIdByName(self.dm.vm_name)
        r = self.tempapi.createTemplate(self.dm.temp_info, self.vm_id)
        def is_temp_ok():
            return self.tempapi.getTemplateInfo(temp_name=self.dm.temp_name)['result']['template']['status']['state']=='ok'
        if r['status_code'] == 202:
            if wait_until(is_temp_ok, 600, 10):
                LogPrint().info("Create Template ok.")
            else:
                LogPrint().error("Create Template overtime")
                self.assertTrue(False)
        else:
            LogPrint().error("Create Template failed.Status-code is wrong.")
            self.assertTrue(False)
        #获得模板关联的磁盘id
        r = TemplateDisksAPIs().getTemplateDiskInfo(self.dm.temp_name, self.dm.disk_name) 
        if r['status_code'] == 200:
            self.disk_id_temp = r['result']['disk']['@id']
        else:
            self.assertTrue(False)
         
    def test_DeleteDisk_AttachtoTemp(self): 
        '''
        @summary: 删除附加到模板的磁盘
        @note: 操作失败，验证返回验证码及报错信息
        '''
        self.flag = True
        LogPrint().info("Test: Delete disk attached to template.")
        r = DiskAPIs().deleteDisk(self.disk_id_temp)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS: The returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
            self.flag = False
        self.assertTrue(self.flag)
         
    def tearDown(self):
        LogPrint().info("Post-Test-1: Delete template %s."% self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        LogPrint().info("Post-Test-2: Delete vm %s."% self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
  
class ITC080403_DeleteDisk_AttachtoRunVm(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-04删除磁盘-03磁盘附加到运行的虚拟机上
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.diskapi = DiskAPIs()
        #创建一个虚拟机
        LogPrint().info("Pre-Test-1: Create vm %s for TC."% self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.vm_info)) 
             
        #创建一块磁盘
        '''
        @note: 创建磁盘时，磁盘的sharable属性必须为false，因为共享磁盘不作为模板的一部份
        '''
        LogPrint().info("Pre-Test-2: Create a disk for TC.")
        r= smart_create_disk(self.dm.disk_info, self.dm.disk_name)
        self.assertTrue(r[0])
        self.disk_id = r[1]   
        #将该磁盘附加到虚拟机
        LogPrint().info("Pre-Test-3: Attach disk %s to vm %s for TC."% (self.dm.disk_name
                                                                 ,self.dm.vm_name))
        self.vmdiskapi = VmDiskAPIs()
        r=self.vmdiskapi.attachDiskToVm(self.dm.vm_name, self.disk_id)
        if r['status_code'] == 200:
            LogPrint().info("Attach Disk to vm success.")
        else:
            LogPrint().error("Attach Disk to vm fail.Status-code is wrong.")
            self.assertTrue(False)
        #启动虚拟机
        LogPrint().info("Pre-Test-4: Start vm for TC.")
        self.assertTrue(smart_start_vm(self.dm.vm_name))
        #激活磁盘
        LogPrint().info("Pre-Test-5: Active vmdisk for TC.")
        self.assertTrue(smart_active_vmdisk(self.dm.vm_name,self.disk_id))
         
    def test_DeleteDisk_AttachtoRunVm(self): 
        '''
        @summary: 删除附加到运行虚拟机的磁盘
        @note: 操作失败，验证返回状态码和报错信息
        '''
        self.flag = True
        LogPrint().info("Test: Delete disk %s attached to running vm %s."% (self.dm.disk_name, self.dm.vm_name))
        r = self.diskapi.deleteDisk(self.disk_id)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS: The returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL: The returned messages are INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The returned status code is '%s' while it should be '%s'." % (r['status_code'], self.dm.expected_status_code))
            self.flag = False
        self.assertTrue(self.flag)
         
    def tearDown(self):
        self.flag = True
        LogPrint().info("Post-Test-1: Stop vm %s."%self.dm.vm_name)
        self.assertTrue(smart_stop_vm(self.dm.vm_name))
        LogPrint().info("Post-Test-2: Delete vm %s."%self.dm.vm_name)
        self.assertTrue(smart_del_vm(self.dm.vm_name))
 
class ITC080404_DeleteDisk_AttachtoDownVm(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-04删除磁盘-04磁盘附加到已关机的虚拟机
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        #创建一个虚拟机
        LogPrint().info("Pre-Test-1: Create vm %s for TC."% self.dm.vm_name)
        self.assertTrue(smart_create_vm(self.dm.vm_name, self.dm.vm_info)) 
             
        #创建一块磁盘
        '''
        @note: 创建磁盘时，磁盘的sharable属性必须为false，因为共享磁盘不作为模板的一部份
        '''
        LogPrint().info("Pre-Test-2: Create a disk for TC.")
        r= smart_create_disk(self.dm.disk_info, self.dm.disk_name)
        self.assertTrue(r[0])
        self.disk_id = r[1]   
        #将该磁盘附加到虚拟机
        LogPrint().info("Pre-Test-3: Attach disk %s to vm %s for TC."% (self.dm.disk_name
                                                                 ,self.dm.vm_name))
        self.vmdiskapi = VmDiskAPIs()
        r=self.vmdiskapi.attachDiskToVm(self.dm.vm_name, self.disk_id)
        if r['status_code'] == 200:
            LogPrint().info("Attach Disk to vm success.")
        else:
            LogPrint().error("Attach Disk to vm fail.Status-code is wrong.")
            self.assertTrue(False)
             
    def test_DeleteDisk_AttachtoDownVm(self):
        '''
        @summary: 删除附加到运行虚拟机的磁盘
        @note: 操作成功，验证返回状态码，验证磁盘是否存在
        ''' 
        diskapi = DiskAPIs()
        self.flag = True
        LogPrint().info("Test: Delete disk %s attached to down vm %s."% (self.dm.disk_name, self.dm.vm_name))
        r = diskapi.deleteDisk(self.disk_id)
        if r['status_code'] == self.dm.expected_status_code:
            if not diskapi.isExist(self.disk_id):
                LogPrint().info("PASS: Delete Disk attached to down vm SUCCESS." )
            else:
                LogPrint().error("FAIL: Disk is still exist. " )
                self.flag = False
        else:
            LogPrint().error("FAIL: Returned status code is %s. "% r['status_code'])
            self.flag = False
        self.assertTrue(self.flag) 
         
    def tearDown(self):
        LogPrint().info("Post-Test: Delete vm %s."% self.dm.vm_name)
        VirtualMachineAPIs().delVm(self.dm.vm_name) 

class ITC0805_GetStaticsofDisk(BaseTestCase):   
    '''
    @summary: 08磁盘管理-05获取磁盘统计信息
    '''   
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a disk for TC.")
        r=smart_create_disk(self.dm.disk_info)
        self.disk_id = r[1]
        self.assertTrue(r[0])
        
    def test_GetStaticsofDisk(self):
        '''
        @summary: 获取磁盘的统计信息
        @note: 操作成功，验证返回状态码
        '''
        self.flag=True
        diskapi = DiskAPIs()
        LogPrint().info("Test: Get statics of disk.")
        r = diskapi.getStaticsofDisk(self.disk_id)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("PASS: Get statics of disk SUCCESS.")
        else:
            LogPrint().error("FAIL: Returned status code is %s. "% r['status_code']) 
            self.flag=False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete the disk.")
        self.assertTrue(smart_delete_disk(self.disk_id))   
                      
class ITC08_TearDown(BaseTestCase):
    '''
    @summary: “磁盘管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: （1）将数据中心里的Data域（data1）设置为Maintenance状态；
    @note: （2）删除数据中心dc（非强制）；
    @note: （3）删除所有unattached状态的存储域（data1/data2）；
    @note: （4）删除主机host1；
    @note: （5）删除集群cluster1。
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = self.initData('ITC08_SetUp')
        
    def test_TearDown(self):
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        time.sleep(30)
        # Step1：将data1存储域设置为Maintenance状态
        LogPrint().info("Post-Module-Test-1: Deactivate data storage domains '%s'." % self.dm.data1_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
        
        # Step2：删除数据中心dc1（非强制，之后存储域变为Unattached状态）
        if dcapi.searchDataCenterByName(self.dm.dc_nfs_name)['result']['data_centers']:
            LogPrint().info("Post-Module-Test-2: Delete DataCenter '%s'." % self.dm.dc_nfs_name)
            self.assertTrue(dcapi.delDataCenter(self.dm.dc_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)
                
        # Step3：删除4个Unattached状态存储域（data1/data2/iso1/export1）
        LogPrint().info("Post-Module-Test-3: Delete all unattached storage domains.")
        dict_sd_to_host = [self.dm.data1_nfs_name, self.dm.data2_nfs_name]
        for sd in dict_sd_to_host:
            smart_del_storage_domain(sd, self.dm.xml_del_sd_option, host_name=self.dm.host1_name)
        
        # Step4：删除主机（host1）
        LogPrint().info("Post-Module-Test-6: Delete host '%s'." % self.dm.host1_name)
        self.assertTrue(smart_del_host(self.dm.host1_name, self.dm.xml_del_host_option))
        
        # Step5：删除集群cluster1
        if capi.searchClusterByName(self.dm.cluster_nfs_name)['result']['clusters']:
            LogPrint().info("Post-Module-Test-5: Delete Cluster '%s'." % self.dm.cluster_nfs_name)
            self.assertTrue(capi.delCluster(self.dm.cluster_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test_cases = ["Disk.ITC0802_GetDiskInfo"]
    #ITC080403_DeleteDisk_AttachtoRunVm
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)