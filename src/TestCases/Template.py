#encoding:utf-8
__authors__ = ['"Wei Keke" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/09          初始版本                                                            Wei Keke 
#---------------------------------------------------------------------------------
'''
import unittest
from BaseTestCase import BaseTestCase
from TestAPIs.DiskAPIs import DiskAPIs
from TestAPIs.ProfilesAPIs import ProfilesAPIs
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare,wait_until
#from Utils.HTMLTestRunner import HTMLTestRunner
from TestAPIs.DataCenterAPIs import DataCenterAPIs,smart_attach_storage_domain,smart_deactive_storage_domain,\
smart_detach_storage_domain
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs,VmDiskAPIs
from TestAPIs.TemplatesAPIs import TemplatesAPIs, TemplateDisksAPIs,\
    TemplateNicsAPIs,smart_create_template,smart_create_tempnic,smart_delete_template
from TestAPIs.HostAPIs import smart_create_host,smart_del_host
from TestAPIs.StorageDomainAPIs import smart_create_storage_domain,smart_del_storage_domain,\
    StorageDomainAPIs
from TestAPIs.NetworkAPIs import NetworkAPIs
from TestData.Template import ITC07_SetUp as ModuleData

import xmltodict
 
class ITC07_SetUp(BaseTestCase):
    '''
    @summary: 模板管理模块级测试用例，初始化模块测试环境；
    @note: （1）创建一个NFS类型数据中心；
    @note: （2）创建一个集群；
    @note: （3）创建一个主机，并等待其变为UP状态；
    @note: （4）创建3个存储域（data1/data2/Export）；
    @note: （5）将 data1 附加到数据中心；
    @note: （6）创建一个虚拟机
    @note: （7）创建一个磁盘
    @note: （8）将磁盘附加到虚拟机
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
          
        # 将创建的的data1、data2和export域附加到NFS/ISCSI数据中心里。
        LogPrint().info("Pre-Module-Test-5: Attach the data storages to data centers.")
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.data2_nfs_name))
        self.assertTrue(smart_attach_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        #创建一个虚拟机
        self.vmapi = VirtualMachineAPIs()
        r = self.vmapi.createVm(self.dm.vm_info)
        if r['status_code'] == 201:
            self.vm_name = r['result']['vm']['name']
        else:
            LogPrint().error("Create vm failed.Status-code is WRONG.")
            self.assertTrue(False)
        #创建一个磁盘    
        self.diskapi = DiskAPIs()
        sd_id = StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data1_nfs_name)
        r = self.diskapi.createDisk(self.dm.disk_info, sd_id)
        def is_disk_ok():
            return self.diskapi.getDiskStatus(self.disk_id)=='ok'
        if r['status_code'] == 202:
            self.disk_id = r['result']['disk']['@id']
            if wait_until(is_disk_ok, 200, 5):
                LogPrint().info("Create disk ok.")
        else:
            LogPrint().error("Create disk failed.Status-code is WRONG.")
            self.assertTrue(False)
        #将磁盘附加到虚拟机    
        self.vmdiskapi = VmDiskAPIs()
        r=self.vmdiskapi.attachDiskToVm(self.vm_name, self.disk_id)
        if r['status_code'] == 200:
            LogPrint().info("Attach Disk to vm SUCCESS.")
        else:
            LogPrint().error("Attach Disk to vm fail.Status-code is WRONG.")
            self.assertTrue(False)
  
class ITC070101_GetTemplateList(BaseTestCase):
    '''
    @summary: 07模板管理-01基本操作-01获取模板列表
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
         
    def test_GetTemplateList(self):
        '''
        @summary: 获取模板列表
        @note: 操作成功，验证返回状态码
        '''
        temp_api = TemplatesAPIs()
        LogPrint().info("Test: Get template list.")
        r = temp_api.getTemplatesList()
        if r['status_code'] == 200:
            LogPrint().info("PASS: Get TemplateList SUCCESS.")
            self.assertTrue(True)
        else:
            LogPrint().error("FAIL: Returned status code is WRONG.")
            self.assertTrue(False)
         
class ITC070102_GetTemplateInfo(BaseTestCase):
    '''
    @summary: 07模板管理-01基本操作-02获取模板详情
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.temp_api = TemplatesAPIs()
        LogPrint().info("Pre-Test: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
 
    def test_GetTemplateInfo(self):
        '''
        @summary: 获取模板详情
        @note: 操作成功，验证返回状态码和返回信息
        '''
        self.flag=True
        LogPrint().info("Test: Get info of template %s."%self.dm.temp_name)
        r = self.temp_api.getTemplateInfo(self.dm.temp_name)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("PASS: Get TemplateInfo SUCCESS.")
        else:
            LogPrint().error("FAIL: Get TemplateInfo fail.The Template info is WRONOG.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        
class ITC0701030101_CreateTemplate(BaseTestCase):
    '''
    @summary: 07模板管理-01基本操作-03创建模板-01成功创建-01最小测试集
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        
    def test_CreateTemplate(self):
        '''
        @summary: 创建模板
        @note: 操作成功，验证返回状态码和返回信息
        '''
        self.tempapi = TemplatesAPIs()
        self.expected_result_index = 0
        @BaseTestCase.drive_data(self, self.dm.temp_info)
        def do_test(xml_info):
            self.flag=True
            LogPrint().info("Test: Create template %s."%self.dm.temp_name[self.expected_result_index])
            r = self.tempapi.createTemplate(xml_info)
            def is_temp_ok():
                return self.tempapi.getTemplateInfo(temp_name=self.dm.temp_name[self.expected_result_index])['result']['template']['status']['state']=='ok'
            if r['status_code'] == self.dm.expected_status_code:
                if wait_until(is_temp_ok, 600, 10):
                    LogPrint().info("PASS: Create Template '%s'ok."%self.dm.temp_name[self.expected_result_index])
                else:
                    LogPrint().error("FAIL: Create Template '%s'overtime"%self.dm.temp_name[self.expected_result_index])
                    self.flag=False
            else:
                LogPrint().error("FAIL: Create Template '%s'failed.Status-code is WRONG."%self.dm.temp_name[self.expected_result_index])
                self.flag=False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
        
    def tearDown(self):
        for index in range(0,5):
            LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name[index])
            self.assertTrue(smart_delete_template(self.dm.temp_name[index]))
          
class ITC0701030102_CreateTemplate_SD(BaseTestCase):
    '''
    @summary: 07模板管理-01基本操作-03创建模板-01成功创建-02指定存储域
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
    
    def test_CreateTemplate_SD(self):
        '''
        @summary: 创建模板,指定存储域
        @note: 操作成功，验证返回状态码和返回信息
        '''
        self.tempapi = TemplatesAPIs()
        LogPrint().info("Test: Create template %s."%self.dm.temp_name)
        r = self.tempapi.createTemplate(self.dm.temp_info)
        print r
        def is_temp_ok():
            return self.tempapi.getTemplateInfo(temp_name=self.dm.temp_name)['result']['template']['status']['state']=='ok'
        if r['status_code'] == self.dm.expected_status_code:
            if wait_until(is_temp_ok, 600, 10):
                LogPrint().info("PASS: Create Template ok.")
            else:
                LogPrint().error("FAIL: Create Template overtime")
                self.assertTrue(False)
        else:
            LogPrint().error("FAIL: Create Template failed.Status-code is WRONG.")
            self.assertTrue(False)
            
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name)) 
           

class ITC0701030201_CreateTemplate_DupName(BaseTestCase):
    '''
    @summary: 07模板管理-03创建模板-02创建失败-01模板重名
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a template %s for TC."%self.dm.temp_name)
        smart_create_template(self.dm.temp_name, self.dm.temp_info)
            
    def test_CreateTemplate_DupName(self):
        '''
        @summary: 创建模板,重名
        @note: 操作失败，验证返回状态码和返回信息
        '''
        self.tempapi = TemplatesAPIs()
        LogPrint().info("Test: Create dupname template %s."%self.dm.temp_name)
        r = self.tempapi.createTemplate(self.dm.temp_info)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            d1 = xmltodict.parse(self.dm.expected_info)
            if dictCompare.isSubsetDict(d1, r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when create host with dup name.")
            else:
                LogPrint().error("FAIL: Returned messages are incorrectly.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Status-code is WRONG.")
            self.assertTrue(False)
            
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))     

class ITC0701030202_CreateTemplate_VerifyName(BaseTestCase):
    '''
    @summary: 07模板管理-03创建模板-02创建失败-02验证名称合法性
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
            
    def test_CreateTemplate_VerifyName(self):
        '''
        @summary: 创建模板,名称不合法
        @note: 操作失败，验证返回状态码和返回信息
        '''
        self.tempapi = TemplatesAPIs()
        LogPrint().info("Test: Create template %s."%self.dm.temp_name)
        r = self.tempapi.createTemplate(self.dm.temp_info)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            d1 = xmltodict.parse(self.dm.expected_info)
            if dictCompare.isSubsetDict(d1, r['result']):
                LogPrint().info("PASS: Returned status code and messages are CORRECT when create host with dup name.")
            else:
                LogPrint().error("FAIL: Returned messages are incorrectly.")
                self.flag = False
        else:
            LogPrint().error("FAIL: Status-code is WRONG.")
            self.assertTrue(False)

class ITC0701030203_CreateTemplate_NoRequired(BaseTestCase):
    '''
    @summary: 07模板管理-03创建模板-02创建失败-03验证参数完整性
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
            
    def test_CreateTemplate_NoRequired(self):
        '''
        @summary: 创建模板,缺少必填项
        @note: 操作失败，验证返回状态码和返回信息
        '''
        self.tempapi = TemplatesAPIs()
        self.expected_result_index = 0
        @BaseTestCase.drive_data(self, self.dm.temp_info)
        def do_test(xml_info):
            self.flag = True
            r = self.tempapi.createTemplate(xml_info)
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
        
class ITC070105_DeleteTemplate(BaseTestCase):
    '''
    @summary: 07模板管理-01基本操作-05删除模板
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
            
    def test_DeleteTemplate(self):
        '''
        @summary: 删除模板
        @note: 操作成功，验证返回状态码和返回信息
        '''
        self.flag=True
        self.tempapi = TemplatesAPIs()
        LogPrint().info("Test: Delete template %s."%self.dm.temp_name)
        r = self.tempapi.delTemplate(self.dm.temp_name)
        def temp_not_exist():
            return self.tempapi.searchTemplateByName(self.dm.temp_name)['result']['templates'] ==None
        if r['status_code'] == self.dm.expected_status_code:
            if wait_until(temp_not_exist,300, 5):
                LogPrint().info("PASS: Delete Template SUCCESS.")
            else:
                LogPrint().info("FAIL: Delete Template failed.The Template still exist")
                self.flag=False
        else:
            LogPrint().info("FAIL: Delete Template failed.The status_code is WRONG")
            self.flag=False
        self.assertTrue(self.flag)
 
# class ITC07010601_ExportTemplate_sync(BaseTestCase): 
#     '''
#     @summary: 07模板管理-01基本操作-06导出模板-01同步
#     @bug: 该功能目前在web界面上失败，暂时只能通过返回状态码来判断
#     '''
#     def setUp(self):
#         self.dm = super(self.__class__, self).setUp()
#         self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
#     def test_exportTemplate_sync(self):
#         self.flag=True
#         self.tempapi = TemplatesAPIs()
#         r = self.tempapi.exportTemplate(self.dm.temp_name, self.dm.action)
#         if r['status_code'] == self.dm.expected_status_code:
#             LogPrint().info("Export template SUCCESS.")
#         else:
#             LogPrint().error("Export template failed.The status_code is WRONG.")
#             self.flag=False
#         self.assertTrue(self.flag)
#     def tearDown(self):
#         self.assertTrue(smart_delete_template(self.dm.temp_name))
# 
# class ITC07010602_ExportTemplate_async(BaseTestCase): 
#     '''
#     @summary: 07模板管理-01基本操作-06导出模板-02异步
#     @bug: 该功能目前在web界面上失败，暂时只能通过返回状态码来判断
#     '''
#     def setUp(self):
#         self.dm = super(self.__class__, self).setUp()
#         self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
#     def test_exportTemplate_sync(self):
#         self.flag=True
#         self.tempapi = TemplatesAPIs()
#         r = self.tempapi.exportTemplate(self.dm.temp_name, self.dm.action)
#         if r['status_code'] == self.dm.expected_status_code:
#             LogPrint().info("Export template SUCCESS.")
#         else:
#             LogPrint().error("Export template failed.The status_code is WRONG.")
#             self.flag=False
#         self.assertTrue(self.flag)                           

class ITC070201_GetTemplateDiskList(BaseTestCase): 
    '''
    @summary: 07模板管理-02模板磁盘管理-01获取模板磁盘列表
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        
    def test_GetTemplateDiskList(self):
        '''
        @summary: 获取模板的磁盘列表
        @note: 操作成功，验证返回状态码和返回信息
        '''
        self.flag = True
        tempdisk_api = TemplateDisksAPIs()
        LogPrint().info("Test: Get disk list of template %s."%self.dm.temp_name)
        r = tempdisk_api.getTemplateDiskList(self.dm.temp_name)  
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("PASS: Get disk list of template %s SUCCESS."%self.dm.temp_name)
        else:
            LogPrint().error("FAIL: The status_code is WRONG")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))

class ITC070202_GetTemplateDiskInfo(BaseTestCase): 
    '''
    @summary: 07模板管理-02模板磁盘管理-02获取模板磁盘详情
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        
    def test_GetTemplateDiskInfo(self):
        '''
        @summary: 获取模板的磁盘详情
        @note: 操作成功，验证返回状态码和返回信息
        '''
        self.flag = True
        tempdisk_api = TemplateDisksAPIs()
        LogPrint().info("Test: Get disk info of template %s."%self.dm.temp_name)
        r = tempdisk_api.getTemplateDiskInfo(self.dm.temp_name,self.dm.disk_name)  
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse(self.dm.disk_info)
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("PASS: Get disk info of template %s SUCCESS."%self.dm.temp_name)
            else:
                LogPrint().error("FAIL: The disk_info is WRONG")
                self.flag = False
        else:
            LogPrint().error("FAIL: The status_code is WRONG")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))     

class ITC07020301_CopyTemplateDisk_sync(BaseTestCase): 
    '''
    @summary: 07模板管理-02模板磁盘管理-03复制模板-01同步
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        
    def test_CopyTemplateDisk_sync(self):
        '''
        @summary: 拷贝模板磁盘，同步
        @note: 操作成功，验证返回状态码，检查磁盘的存储域变化
        '''
        self.flag = True
        tempdisk_api = TemplateDisksAPIs()
        LogPrint().info("Test: Copy disk of template %s sync."%self.dm.temp_name)
        r = tempdisk_api.copyTemplateDisk(self.dm.temp_name, self.dm.disk_name, self.dm.copy_data)  
        def is_tempdisk_ok():
            return tempdisk_api.getTemplateDiskStatus(self.dm.temp_name, self.dm.disk_name)=='ok'
        def check_tempdisk_sd(temp_name,disk_name,sd_id):
            '''
            @summary: 检查模板磁盘所在的存储域是否包含源和目的存储域
            @param temp_name: 模板名称
            @param disk_name: 磁盘名称
            @param sd_id:存储域id 
            @return: True or False
            '''
            sd_list = tempdisk_api.getTemplateDiskSdList(temp_name, disk_name)
            flag = False
            for index in range(len(sd_list)):
                if sd_list[index]['@id'] == sd_id:
                    flag = True
            return flag 
        if r['status_code'] == self.dm.expected_status_code:
            if wait_until(is_tempdisk_ok, 300, 10):
                if check_tempdisk_sd(self.dm.temp_name, self.dm.disk_name, self.dm.des_sd_id):
                    LogPrint().info("PASS: Copy Template Disk sync SUCCESS.")
                else:
                    LogPrint().error("FAIL: The des sd is not %s."%self.dm.des_sd_name)
                    self.flag= False
            else:
                LogPrint().error("FAIL: CopyTemplateDisk overtime")
                self.flag= False
        else:
            LogPrint().error("FAIL: The status_code is WRONG")
            self.flag= False
        self.assertTrue(self.flag) 
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name)) 

class ITC07020302_CopyTemplateDisk_async(BaseTestCase): 
    '''
    @summary: 07模板管理-02模板磁盘管理-03复制模板-01异步
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Test: Copy disk of template %s sync."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        
    def test_CopyTemplateDisk_async(self):
        '''
        @summary: 拷贝模板磁盘，异步
        @note: 操作成功，验证返回状态码，检查磁盘的存储域变化
        '''
        LogPrint().info("Test: Copy disk of template %s async."%self.dm.temp_name)
        self.flag = True
        tempdisk_api = TemplateDisksAPIs()
        r = tempdisk_api.copyTemplateDisk(self.dm.temp_name, self.dm.disk_name, self.dm.copy_data)  
        print r
        def is_tempdisk_ok():
            return tempdisk_api.getTemplateDiskStatus(self.dm.temp_name, self.dm.disk_name)=='ok'
        def check_tempdisk_sd(temp_name,disk_name,sd_id):
            '''
            @summary: 检查模板磁盘所在的存储域是否包含源和目的存储域
            @param temp_name: 模板名称
            @param disk_name: 磁盘名称
            @param sd_id:存储域id 
            @return: True or False
            '''
            sd_list = tempdisk_api.getTemplateDiskSdList(temp_name, disk_name)
            flag = False
            for index in range(len(sd_list)):
                if sd_list[index]['@id'] == sd_id:
                    flag = True
            return flag 
        if r['status_code'] == self.dm.expected_status_code:
            if wait_until(is_tempdisk_ok, 300, 10):
                if check_tempdisk_sd(self.dm.temp_name, self.dm.disk_name, self.dm.des_sd_id):
                    LogPrint().info("PASS: Copy Template Disk sync SUCCESS")
                else:
                    LogPrint().error("FAIL: The des sd is not %s."%self.dm.des_sd_name)
                    self.flag= False
            else:
                LogPrint().error("FAIL: CopyTemplateDisk overtime")
                self.flag= False
        else:
            LogPrint().error("FAIL: The status_code is WRONG")
            self.flag= False
        self.assertTrue(self.flag) 
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))  
              
class ITC07020303_CopyTemplateDisk_nosd(BaseTestCase): 
    '''
    @summary: 07模板管理-02模板磁盘管理-03复制模板-03缺少存储域
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        
    def test_CopyTemplateDisk_nosd(self):
        '''
        @summary: 拷贝模板磁盘，未指定存储域
        @note: 操作失败，验证返回状态码和返回信息
        '''
        self.flag = True
        tempdisk_api = TemplateDisksAPIs()
        LogPrint().info("Test: Copy disk of template %s without SD."%self.dm.temp_name)
        r = tempdisk_api.copyTemplateDisk(self.dm.temp_name, self.dm.disk_name, self.dm.copy_data)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("PASS: Returned status code ans messages are CORRECT.")
            else:
                LogPrint().error("FAIL: The error_log is WRONG.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The status_code is WRONG.")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))
    
class ITC070301_GetTemplateNicList(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-01获取网络接口列表
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        
    def test_GetTemplateNicList(self):
        '''
        @summary: 获取模板的网络接口列表
        @note: 操作成功，验证返回状态码
        '''
        tempnic_api = TemplateNicsAPIs()
        LogPrint().info("Test: Get nic list of template %s."%self.dm.temp_name)
        r=tempnic_api.getTemplateNicList(self.dm.temp_name)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("PASS: GetTemplateNicList SUCCESS.")
        else:
            LogPrint().error("FAIL: GetTemplateNicList fail.The status_code is WRONG")
            self.flag = False
        self.assertTrue(self.flag)
    
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        
class ITC070302_GetTemplateNicInfo(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-02获取网络接口详情
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test-1: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        LogPrint().info("Pre-Test-2: Create a nic for template %s."%self.dm.temp_name)
        self.assertTrue(smart_create_tempnic(self.dm.temp_name, self.dm.nic_data))
        
    def test_GetTemplateNicInfo(self):
        '''
        @summary: 获取模板的网络接口详情
        @note: 操作成功，验证返回状态码和返回信息
        '''
        tempnic_api = TemplateNicsAPIs()
        LogPrint().info("Test: Get nic %s info of template %s."%(self.dm.nic_name, self.dm.temp_name))
        r =  tempnic_api.getTemplateNicInfo(self.dm.temp_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse(self.dm.nic_data)
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("PASS: Get nic %s info of template %s SUCCESS."%(self.dm.nic_name, self.dm.temp_name))
            else:
                LogPrint().error("FAIL: Returned nic info is WRONG")
                self.flag = False
        else:
            LogPrint().error("FAIL: The status_code is WRONG")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))     
            
class ITC0703030101_CreateTemplateNic(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-03新建网络接口-01成功创建-01测试最小集
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test-1: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        
    def test_CreateTemplateNic(self):  
        '''
        @summary: 创建模板的网络接口
        @note: 操作成功，验证返回状态码和返回信息
        '''
        tempnic_api = TemplateNicsAPIs()
        self.expected_result_index = 0
        @BaseTestCase.drive_data(self, self.dm.nic_data)
        def do_test(xml_info):
            LogPrint().info("Test: Create nic %s for template %s."%(self.dm.nic_name[self.expected_result_index], self.dm.temp_name))
            r =  tempnic_api.createTemplateNic(self.dm.temp_name, xml_info)
            if r['status_code'] == self.dm.expected_status_code:
                dictCompare = DictCompare()
                print xml_info
                expected_result = xmltodict.parse(xml_info)
                actual_result = r['result']
                if dictCompare.isSubsetDict(expected_result,actual_result):
                    LogPrint().info("PASS: Create Nic %s SUCCESS."%self.dm.nic_name[self.expected_result_index])
                else:
                    LogPrint().error("FAIL: The nic %s info is WRONG"%self.dm.nic_name[self.expected_result_index])
                    self.flag = False
            else:
                LogPrint().error("FAIL: The status_code is WRONG")
                self.flag = False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        
class ITC0703030102_CreateTemplateNic_proid(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-03新建网络接口-01成功创建-02指定配置集
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test-1: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        #为所在数据中心的ovirtmgmt网络创建一个配置集
        LogPrint().info("Pre-Test-2: Create a profile %s for ovirtmgmt."%self.dm.profile_name)
        self.nw_id = NetworkAPIs().getNetworkIdByName('ovirtmgmt', self.dm.dc_name)
        print self.nw_id
        r =ProfilesAPIs().createProfiles(self.dm.profile_info, self.nw_id)
        if r['status_code'] == 201:
            self.proid = r['result']['vnic_profile']['@id']
            LogPrint().info("Create Profile SUCCESS.")
        else:
            LogPrint().error("Create Profile fail.The status_code is WRONG.")
    
    def test_CreateTemplateNic_proid(self): 
        '''
        @summary: 为模板创建网络接口，指定配置集
        @note: 操作成功，验证返回状态码和返回信息
        ''' 
        tempnic_api = TemplateNicsAPIs()
        LogPrint().info("Test-: Create a nic %s with profile %s for template %s."%(self.dm.nic_name, self.dm.profile_name, self.dm.temp_name))
        r =  tempnic_api.createTemplateNic(self.dm.temp_name, self.dm.nic_data,self.proid)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse((self.dm.nic_data %self.proid))
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("PASS: Create a nic %s with profile %s for template %s SUCCESS."%(self.dm.nic_name, self.dm.profile_name, self.dm.temp_name))
            else:
                LogPrint().error("FAIL: The nic_info is WRONG")
                self.flag = False
        else:
            LogPrint().error("FAIL: The status_code is WRONG")
            self.flag = False
        self.assertTrue(self.flag)   
         
    def tearDown(self):
        LogPrint().info("Post-Test-1: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        LogPrint().info("Post-Test-2: Delete profile %s."%self.dm.profile_name)
        ProfilesAPIs().delProfile(self.dm.profile_name, self.nw_id)
        
class ITC0703030201_CreateTemplateNic_DupName(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-03新建网络接口-01创建失败-01重名
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test-1: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        LogPrint().info("Pre-Test-2: Create a nic %s for this template."%self.dm.nic_name)
        self.assertTrue(smart_create_tempnic(self.dm.temp_name, self.dm.nic_data))
        
    def test_CreateTemplateNic_DupName(self):
        '''
        @summary: 为模板创建网络接口，重名
        @note: 操作失败，验证返回状态码和返回信息
        '''   
        tempnic_api = TemplateNicsAPIs()
        LogPrint().info("Test: Create dupname nic %s for this template."%self.dm.nic_name)
        r =  tempnic_api.createTemplateNic(self.dm.temp_name, self.dm.nic_data)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse(self.dm.expected_info)
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("PASS: The returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL: Returned messages are incorrectly.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The status_code is WRONG")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        
class ITC0703030202_CreateTemplateNic_VerifyName(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-03新建网络接口-01创建失败-02验证名称合法性
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        
    def test_CreateTemplateNic_VerifyName(self): 
        '''
        @summary: 为模板创建网络接口，名称不合法
        @note: 操作失败，验证返回状态码和返回信息
        '''    
        tempnic_api = TemplateNicsAPIs()
        LogPrint().info("Test: Create nic %s for this template."%self.dm.nic_name)
        r =  tempnic_api.createTemplateNic(self.dm.temp_name, self.dm.nic_data)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse(self.dm.expected_info)
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("PASS: The returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL: Returned messages are incorrectly.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The status_code is WRONG")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))

class ITC0703030203_CreateTemplateNic_NoRequired(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-03新建网络接口-01创建失败-03缺少必填项
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        
    def test_CreateTemplateNic_NoRequired(self):  
        '''
        @summary: 为模板创建网络接口，缺少必填项
        @note: 操作失败，验证返回状态码和返回信息
        '''    
        tempnic_api = TemplateNicsAPIs()
        LogPrint().info("Test: Create nic for this template.")
        r =  tempnic_api.createTemplateNic(self.dm.temp_name, self.dm.nic_data)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse(self.dm.expected_info)
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("PASS: The returned status code and messages are CORRECT.")
            else:
                LogPrint().error("FAIL: Returned messages are incorrectly.")
                self.flag = False
        else:
            LogPrint().error("FAIL: The status_code is WRONG")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))

class ITC07030401_UpdateTemplateNic(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-04编辑网络接口-01成功
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test-1: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        LogPrint().info("Pre-Test-2: Create a nic %s for this template."%self.dm.nic_name)
        self.assertTrue(smart_create_tempnic(self.dm.temp_name, self.dm.nic_data))
        #为所在数据中心的ovirtmgmt网络创建一个配置集
        self.nw_id = NetworkAPIs().getNetworkIdByName('ovirtmgmt', self.dm.dc_name)
        r =ProfilesAPIs().createProfiles(self.dm.profile_info, self.nw_id)
        if r['status_code'] == 201:
            self.proid = r['result']['vnic_profile']['@id']
            LogPrint().info("Create Profile SUCCESS.")
        else:
            LogPrint().error("Create Profile fail.The status_code is WRONG.")

    def test_UpdateTemplateNic(self):
        '''
        @summary: 为模板编辑网络接口
        @note: 操作成功，验证返回状态码和返回信息
        '''    
        self.flag = True  
        tempnic_api = TemplateNicsAPIs()
        LogPrint().info("Test: Update nic %s for this template."%self.dm.nic_name)
        r =  tempnic_api.updateTemplateNic(self.dm.temp_name, self.dm.nic_name,self.dm.update_info,self.proid)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse((self.dm.update_info %self.proid))
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("PASS: UpdateTemplateNic SUCCESS.")
            else:
                LogPrint().error("FAIL: UpdateTemplateNic fail.The nic_info is WRONG")
                self.flag = False
        else:
            LogPrint().error("FAIL: UpdateTemplateNic fail.The status_code is WRONG")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test-1: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        LogPrint().info("Post-Test-2: Delete profile %s."%self.dm.profile_name)
        ProfilesAPIs().delProfile(self.dm.profile_name, self.nw_id)
        
class ITC070305_DeleteTemplateNic(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-05删除网络接口
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        LogPrint().info("Pre-Test-1: Create a template %s for TC."%self.dm.temp_name)
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        LogPrint().info("Pre-Test-2: Create a nic %s for this template."%self.dm.nic_name)
        self.assertTrue(smart_create_tempnic(self.dm.temp_name, self.dm.nic_data))
    
    def test_DeleteTemplateNic(self):  
        '''
        @summary: 删除模板网络接口
        @note: 操作成功，验证返回状态码，检查接口是否存在
        '''    
        tempnic_api = TemplateNicsAPIs()
        LogPrint().info("Test: Delete nic %s for this template %s."%(self.dm.nic_name, self.dm.temp_name))
        r =  tempnic_api.deleteTemplateNic(self.dm.temp_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if not tempnic_api.getNicIdByName(self.dm.temp_name, self.dm.nic_name):
                LogPrint().info("PASS: Delete nic %s for this template %s SUCCESS."%(self.dm.nic_name, self.dm.temp_name))
            else:
                LogPrint().error("FAIL: The nic %s is still exist."%self.dm.nic_name)
                self.flag = False
        else:
            LogPrint().error("FAIL: The status_code is WRONG")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        LogPrint().info("Post-Test: Delete template %s."%self.dm.temp_name)
        self.assertTrue(smart_delete_template(self.dm.temp_name))  
         
class ITC07_TearDown(BaseTestCase):
    '''
    @summary: “模板管理”模块测试环境清理（执行完该模块所有测试用例后，需要执行该用例清理环境）
    @note: （1）删除虚拟机（删除磁盘）
    @note: （2）将导出域和data域（data2）设置为Maintenance状态；分离导出域；
    @note: （3）将数据中心里的Data域（data1）设置为Maintenance状态；
    @note: （4）删除数据中心dc（非强制）；
    @note: （5）删除所有unattached状态的存储域（data1/data2）；
    @note: （6）删除主机host1；
    @note: （7）删除集群cluster1。
    '''
    def setUp(self):
        '''
        @summary: 模块测试环境初始化（获取测试数据
        '''
        # 调用父类方法，获取该用例所对应的测试数据模块
        self.dm = self.initData('ITC07_SetUp')
         
    def test_TearDown(self):
        vmapi=VirtualMachineAPIs()
        #Step1：删除虚拟机
        vmapi.delVm(self.dm.vm_name)
        dcapi = DataCenterAPIs()
        capi = ClusterAPIs()
        # Step2：将export存储域和data2存储域设置为Maintenance状态,然后从数据中心分离
        LogPrint().info("Post-Module-Test-1: Deactivate storage domains '%s'." % self.dm.export1_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        LogPrint().info("Post-Module-Test-2: Detach storage domains '%s'." % self.dm.export1_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.export1_name))
        
        LogPrint().info("Post-Module-Test-3: Deactivate data storage domains '%s'." % self.dm.data2_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.data2_nfs_name))
        LogPrint().info("Post-Module-Test-4: Detach data storage domains '%s'." % self.dm.data2_nfs_name)
        self.assertTrue(smart_detach_storage_domain(self.dm.dc_nfs_name, self.dm.data2_nfs_name))
        # Step3：将data1存储域设置为Maintenance状态
        LogPrint().info("Post-Module-Test-5: Deactivate data storage domains '%s'." % self.dm.data1_nfs_name)
        self.assertTrue(smart_deactive_storage_domain(self.dm.dc_nfs_name, self.dm.data1_nfs_name))
         
        # Step4：删除数据中心dc1（非强制，之后存储域变为Unattached状态）
        if dcapi.searchDataCenterByName(self.dm.dc_nfs_name)['result']['data_centers']:
            LogPrint().info("Post-Module-Test-6: Delete DataCenter '%s'." % self.dm.dc_nfs_name)
            self.assertTrue(dcapi.delDataCenter(self.dm.dc_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)
                 
        # Step5：删除3个Unattached状态存储域（data1/data2/export1）
        LogPrint().info("Post-Module-Test-7: Delete all unattached storage domains.")
        dict_sd_to_host = [self.dm.data1_nfs_name, self.dm.data2_nfs_name,self.dm.export1_name]
        for sd in dict_sd_to_host:
            smart_del_storage_domain(sd, self.dm.xml_del_sd_option, host_name=self.dm.host1_name)
         
        # Step6：删除主机（host1）
        LogPrint().info("Post-Module-Test-8: Delete host '%s'." % self.dm.host1_name)
        self.assertTrue(smart_del_host(self.dm.host1_name, self.dm.xml_del_host_option))
         
        # Step7：删除集群cluster1
        if capi.searchClusterByName(self.dm.cluster_nfs_name)['result']['clusters']:
            LogPrint().info("Post-Module-Test-9: Delete Cluster '%s'." % self.dm.cluster_nfs_name)
            self.assertTrue(capi.delCluster(self.dm.cluster_nfs_name)['status_code']==self.dm.expected_status_code_del_dc)
                                              
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test_cases = ["Template.ITC07_TearDown"]
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)