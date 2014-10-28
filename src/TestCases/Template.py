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
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs,VmDiskAPIs,VmNicAPIs
from TestAPIs.TemplatesAPIs import TemplatesAPIs, TemplateDisksAPIs,\
    TemplateNicsAPIs,smart_create_template,smart_create_tempnic,smart_delete_template,\
    smart_delete_tempnic

import xmltodict
from TestData.Cluster.ITC020202_GetClusterNetworkInfo import network_name
from TestAPIs.NetworkAPIs import NetworkAPIs


   
class ITC07_SetUp(BaseTestCase):
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        
    def test_create_vm(self):
        self.vmapi = VirtualMachineAPIs()
        #创建一个虚拟机
        r = self.vmapi.createVm(self.dm.vm_info)
        if r['status_code'] == 201:
            self.vm_name = r['result']['vm']['name']
        else:
            LogPrint().error("Create vm failed.Status-code is wrong.")
            self.assertTrue(False)
        #创建一个磁盘    
        self.diskapi = DiskAPIs()
        r = self.diskapi.createDisk(self.dm.disk_info)
        def is_disk_ok():
            return self.diskapi.getDiskStatus(self.disk_id)=='ok'
        if r['status_code'] == 202:
            self.disk_id = r['result']['disk']['@id']
            if wait_until(is_disk_ok, 200, 5):
                LogPrint().info("Create disk ok.")
        else:
            LogPrint().error("Create disk failed.Status-code is wrong.")
            self.assertTrue(False)
        #将磁盘附加到虚拟机    
        self.vmdiskapi = VmDiskAPIs()
        r=self.vmdiskapi.attachDiskToVm(self.vm_name, self.disk_id)
        if r['status_code'] == 200:
            LogPrint().info("Attach Disk to vm success.")
        else:
            LogPrint().error("Attach Disk to vm fail.Status-code is wrong.")
            self.assertTrue(False)

class ITC070101_GetTemplateList(BaseTestCase):

    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
    def test_GetTemplateList(self):
        temp_api = TemplatesAPIs()
        r = temp_api.getTemplatesList()
        if r['status_code'] == 200:
            LogPrint().info("Get TemplateList success.")
            self.assertTrue(True)
        else:
            LogPrint().error("Get TemplateList fail.The status_code is wrong.")
            self.assertTrue(False)
        
class ITC070102_GetTemplateInfo(BaseTestCase):
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.temp_api = TemplatesAPIs()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))

    def test_GetTemplateInfo(self):
        self.flag=True
        r = self.temp_api.getTemplateInfo(self.dm.temp_name)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("Get TemplateInfo success.")
        else:
            LogPrint().error("Get TemplateInfo fail.The Template info is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))
       
class ITC0701030101_CreateTemplate(BaseTestCase):
    '''
    @summary: 07模板管理-03创建模板-01成功创建-01最小测试集
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
    def test_CreateTemplate(self):
        self.tempapi = TemplatesAPIs()
        self.expected_result_index = 0
        @BaseTestCase.drive_data(self, self.dm.temp_info)
        def do_test(xml_info):
            self.flag=True
            r = self.tempapi.createTemplate(xml_info)
            def is_temp_ok():
                return self.tempapi.getTemplateInfo(temp_name=self.dm.temp_name[self.expected_result_index])['result']['template']['status']['state']=='ok'
            if r['status_code'] == self.dm.expected_status_code:
                if wait_until(is_temp_ok, 600, 10):
                    LogPrint().info("Create Template '%s'ok."%self.dm.temp_name[self.expected_result_index])
                else:
                    LogPrint().error("Create Template '%s'overtime"%self.dm.temp_name[self.expected_result_index])
                    self.flag=False
            else:
                LogPrint().error("Create Template '%s'failed.Status-code is wrong."%self.dm.temp_name[self.expected_result_index])
                self.flag=False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
    def tearDown(self):
       for index in range(0,4):
           self.assertTrue(smart_delete_template(self.dm.temp_name[index]))
        
            
class ITC0701030102_CreateTemplate_SD(BaseTestCase):
    '''
    @summary: 07模板管理-03创建模板-01成功创建-02指定存储域
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
    
    def test_CreateTemplate_SD(self):
        self.tempapi = TemplatesAPIs()
        r = self.tempapi.createTemplate(self.dm.temp_info)
        def is_temp_ok():
            return self.tempapi.getTemplateInfo(temp_name=self.dm.temp_name)['result']['template']['status']['state']=='ok'
        if r['status_code'] == self.dm.expected_status_code:
            if wait_until(is_temp_ok, 600, 10):
                LogPrint().info("Create Template ok.")
            else:
                LogPrint().error("Create Template overtime")
                self.assertTrue(False)
        else:
            LogPrint().error("Create Template failed.Status-code is wrong.")
            self.assertTrue(False)
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name)) 
           

class ITC0701030201_CreateTemplate_DupName(BaseTestCase):
    '''
    @summary: 07模板管理-03创建模板-02创建失败-01模板重名
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        smart_create_template(self.dm.temp_name, self.dm.temp_info)
            
    def test_CreateTemplate_DupName(self):
        self.tempapi = TemplatesAPIs()
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
            LogPrint().error("Status-code is wrong.")
            self.assertTrue(False)
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))     

class ITC0701030202_CreateTemplate_VerifyName(BaseTestCase):
    '''
    @summary: 07模板管理-03创建模板-02创建失败-02验证名称合法性
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
            
    def test_CreateTemplate_VerifyName(self):
        self.tempapi = TemplatesAPIs()
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
            LogPrint().error("Status-code is wrong.")
            self.assertTrue(False)

class ITC0701030203_CreateTemplate_NoRequired(BaseTestCase):
    '''
    @summary: 07模板管理-03创建模板-02创建失败-03验证参数完整性
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
            
    def test_CreateTemplate_NoRequired(self):
        self.tempapi = TemplatesAPIs()
        self.expected_result_index = 0
        @BaseTestCase.drive_data(self, self.dm.temp_info)
        def do_test(xml_info):
            self.flag = True
            r = self.tempapi.createTemplate(xml_info)
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
        
class ITC070105_DeleteTemplate(BaseTestCase):
    '''
    @summary: 07模板管理-01基本操作-05删除模板
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
            
    def test_DeleteTemplate(self):
        self.flag=True
        self.tempapi = TemplatesAPIs()
        r = self.tempapi.delTemplate(self.dm.temp_name)
        def temp_not_exist():
            return self.tempapi.searchTemplateByName(self.dm.temp_name)['result']['templates'] ==None
        if r['status_code'] == self.dm.expected_status_code:
            if wait_until(temp_not_exist,300, 5):
                LogPrint().info("Delete Template success.")
            else:
                LogPrint().info("Delete Template failed.The Template still exist")
                self.flag=False
        else:
            LogPrint().info("Delete Template failed.The status_code is wrong")
            self.flag=False
        self.assertTrue(self.flag)
 
class ITC07010601_ExportTemplate_sync(BaseTestCase): 
    '''
    @summary: 07模板管理-01基本操作-06导出模板-01同步
    @bug: 该功能目前在web界面上失败，暂时只能通过返回状态码来判断
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_exportTemplate_sync(self):
        self.flag=True
        self.tempapi = TemplatesAPIs()
        r = self.tempapi.exportTemplate(self.dm.temp_name, self.dm.action)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("Export template success.")
        else:
            LogPrint().error("Export template failed.The status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))

class ITC07010602_ExportTemplate_async(BaseTestCase): 
    '''
    @summary: 07模板管理-01基本操作-06导出模板-02异步
    @bug: 该功能目前在web界面上失败，暂时只能通过返回状态码来判断
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_exportTemplate_sync(self):
        self.flag=True
        self.tempapi = TemplatesAPIs()
        r = self.tempapi.exportTemplate(self.dm.temp_name, self.dm.action)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("Export template success.")
        else:
            LogPrint().error("Export template failed.The status_code is wrong.")
            self.flag=False
        self.assertTrue(self.flag)                           

class ITC070201_GetTemplateDiskList(BaseTestCase): 
    '''
    @summary: 07模板管理-02模板磁盘管理-01获取模板磁盘列表
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_GetTemplateDiskList(self):
        self.flag = True
        tempdisk_api = TemplateDisksAPIs()
        r = tempdisk_api.getTemplateDiskList(self.dm.temp_name)  
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("GetTemplateDiskList success.")
        else:
            LogPrint().error("GetTemplateDiskList fail.The status_code is wrong")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))

class ITC070202_GetTemplateDiskInfo(BaseTestCase): 
    '''
    @summary: 07模板管理-02模板磁盘管理-02获取模板磁盘详情
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_GetTemplateDiskInfo(self):
        self.flag = True
        tempdisk_api = TemplateDisksAPIs()
        r = tempdisk_api.getTemplateDiskInfo(self.dm.temp_name,self.dm.disk_name)  
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse(self.dm.disk_info)
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("GetTemplateDiskInfo success.")
            else:
                LogPrint().error("GetTemplateDiskInfo fail.The disk_info is wrong")
                self.flag = False
        else:
            LogPrint().error("GetTemplateDiskInfo fail.The status_code is wrong")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))     

class ITC07020301_CopyTemplateDisk_sync(BaseTestCase): 
    '''
    @summary: 07模板管理-02模板磁盘管理-03复制模板-01同步
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_CopyTemplateDisk_sync(self):
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
                    LogPrint().info("CopyTemplateDisk success.")
                else:
                    LogPrint().error("CopyTemplateDisk to storagedomain '%s' fail."%self.dm.des_sd_name)
                    self.flag= False
            else:
                LogPrint().error("CopyTemplateDisk overtime")
                self.flag= False
        else:
            LogPrint().error("CopyTemplateDisk fail.The status_code is wrong")
            self.flag= False
        self.assertTrue(self.flag) 
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name)) 

class ITC07020302_CopyTemplateDisk_async(BaseTestCase): 
    '''
    @summary: 07模板管理-02模板磁盘管理-03复制模板-01异步
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_CopyTemplateDisk_async(self):
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
                    LogPrint().info("CopyTemplateDisk success.")
                else:
                    LogPrint().error("CopyTemplateDisk to storagedomain '%s' fail."%self.dm.des_sd_name)
                    self.flag= False
            else:
                LogPrint().error("CopyTemplateDisk overtime")
                self.flag= False
        else:
            LogPrint().error("CopyTemplateDisk fail.The status_code is wrong")
            self.flag= False
        self.assertTrue(self.flag) 
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))  
              
class ITC07020303_CopyTemplateDisk_nosd(BaseTestCase): 
    '''
    @summary: 07模板管理-02模板磁盘管理-03复制模板-03缺少存储域
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_CopyTemplateDisk_nosd(self):
        self.flag = True
        tempdisk_api = TemplateDisksAPIs()
        r = tempdisk_api.copyTemplateDisk(self.dm.temp_name, self.dm.disk_name, self.dm.copy_data)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(xmltodict.parse(self.dm.expected_info), r['result']):
                LogPrint().info("CopyTemplateDisk_nosd success.")
            else:
                LogPrint().error("CopyTemplateDisk_nosd fail.The error_log is wrong.")
                self.flag = False
        else:
            LogPrint().error("CopyTemplateDisk_nosd fail.The status_code is wrong.")
            self.flag = False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))
    
        
class ITC070301_GetTemplateNicList(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-01获取网络接口列表
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_GetTemplateNicList(self):
        tempnic_api = TemplateNicsAPIs()
        r=tempnic_api.getTemplateNicList(self.dm.temp_name)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("GetTemplateNicList success.")
        else:
            LogPrint().error("GetTemplateNicList fail.The status_code is wrong")
            self.flag = False
        self.assertTrue(self.flag)
    
class ITC070302_GetTemplateNicInfo(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-02获取网络接口详情
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        self.assertTrue(smart_create_tempnic(self.dm.temp_name, self.dm.nic_data))
    def test_GetTemplateNicInfo(self):
        tempnic_api = TemplateNicsAPIs()
        r =  tempnic_api.getTemplateNicInfo(self.dm.temp_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse(self.dm.nic_data)
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("GetTemplateNicInfo success.")
            else:
                LogPrint().error("GetTemplateNicInfo fail.The nic_info is wrong")
                self.flag = False
        else:
            LogPrint().error("GetTemplateNicInfo fail.The status_code is wrong")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))     
            
class ITC0703030101_CreateTemplateNic(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-03新建网络接口-01成功创建-01测试最小集
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_CreateTemplateNic(self):  
        tempnic_api = TemplateNicsAPIs()
        self.expected_result_index = 0
        @BaseTestCase.drive_data(self, self.dm.nic_data)
        def do_test(xml_info):
            r =  tempnic_api.createTemplateNic(self.dm.temp_name, xml_info)
            if r['status_code'] == self.dm.expected_status_code:
                dictCompare = DictCompare()
                print xml_info
                expected_result = xmltodict.parse(xml_info)
                actual_result = r['result']
                if dictCompare.isSubsetDict(expected_result,actual_result):
                    LogPrint().info("CreateTemplateNic success.")
                else:
                    LogPrint().error("CreateTemplateNic fail.The nic_info is wrong")
                    self.flag = False
            else:
                LogPrint().error("CreateTemplateNic fail.The status_code is wrong")
                self.flag = False
            self.assertTrue(self.flag)
            self.expected_result_index += 1
        do_test()
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))
class ITC0703030102_CreateTemplateNic_proid(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-03新建网络接口-01成功创建-02指定配置集
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        #为所在数据中心的ovirtmgmt网络创建一个配置集
        self.nw_id = NetworkAPIs().getNetworkIdByName('ovirtmgmt', self.dm.dc_name)
        r =ProfilesAPIs().createProfiles(self.dm.profile_info, self.nw_id)
        if r['status_code'] == 201:
            self.proid = r['result']['vnic_profile']['@id']
            LogPrint().info("Create Profile success.")
        else:
            LogPrint().error("Create Profile fail.The status_code is wrong.")
    def test_CreateTemplateNic_proid(self):  
        tempnic_api = TemplateNicsAPIs()
        r =  tempnic_api.createTemplateNic(self.dm.temp_name, self.dm.nic_data,self.proid)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse((self.dm.nic_data %self.proid))
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("CreateTemplateNic success.")
            else:
                LogPrint().error("CreateTemplateNic fail.The nic_info is wrong")
                self.flag = False
        else:
            LogPrint().error("CreateTemplateNic fail.The status_code is wrong")
            self.flag = False
        self.assertTrue(self.flag)    
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        TemplateNicsAPIs().deleteTemplateNic(self.dm.temp_name, self.dm.nic_name)
        ProfilesAPIs().delProfile(self.dm.profile_name, self.nw_id)
class ITC0703030201_CreateTemplateNic_DupName(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-03新建网络接口-01创建失败-01重名
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        self.assertTrue(smart_create_tempnic(self.dm.temp_name, self.dm.nic_data))
    def test_CreateTemplateNic_DupName(self):  
        tempnic_api = TemplateNicsAPIs()
        r =  tempnic_api.createTemplateNic(self.dm.temp_name, self.dm.nic_data)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse(self.dm.expected_info)
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("CreateTemplateNic_DupName pass.")
            else:
                LogPrint().error("CreateTemplateNic_DupName fail.The error_info is wrong")
                self.flag = False
        else:
            LogPrint().error("CreateTemplateNic_DupName fail.The status_code is wrong")
            self.flag = False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        
class ITC0703030202_CreateTemplateNic_VerifyName(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-03新建网络接口-01创建失败-02验证名称合法性
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_CreateTemplateNic_VerifyName(self):  
        tempnic_api = TemplateNicsAPIs()
        r =  tempnic_api.createTemplateNic(self.dm.temp_name, self.dm.nic_data)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse(self.dm.expected_info)
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("CreateTemplateNic_VerifyName pass.")
            else:
                LogPrint().error("CreateTemplateNic_VerifyName fail.The error_info is wrong")
                self.flag = False
        else:
            LogPrint().error("CreateTemplateNic_VerifyName fail.The status_code is wrong")
            self.flag = False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))

class ITC0703030203_CreateTemplateNic_NoRequired(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-03新建网络接口-01创建失败-03缺少必填项
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
    def test_CreateTemplateNic_NoRequired(self):  
        tempnic_api = TemplateNicsAPIs()
        r =  tempnic_api.createTemplateNic(self.dm.temp_name, self.dm.nic_data)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse(self.dm.expected_info)
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("CreateTemplateNic_NoRequired pass.")
            else:
                LogPrint().error("CreateTemplateNic_NoRequired fail.The error_info is wrong")
                self.flag = False
        else:
            LogPrint().error("CreateTemplateNic_NoRequired fail.The status_code is wrong")
            self.flag = False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))

class ITC07030401_UpdateTemplateNic(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-04编辑网络接口-01成功
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        self.assertTrue(smart_create_tempnic(self.dm.temp_name, self.dm.nic_data))
        #为所在数据中心的ovirtmgmt网络创建一个配置集
        self.nw_id = NetworkAPIs().getNetworkIdByName('ovirtmgmt', self.dm.dc_name)
        r =ProfilesAPIs().createProfiles(self.dm.profile_info, self.nw_id)
        if r['status_code'] == 201:
            self.proid = r['result']['vnic_profile']['@id']
            LogPrint().info("Create Profile success.")
        else:
            LogPrint().error("Create Profile fail.The status_code is wrong.")
    def test_UpdateTemplateNic(self):
        self.flag = True  
        tempnic_api = TemplateNicsAPIs()
        r =  tempnic_api.updateTemplateNic(self.dm.temp_name, self.dm.nic_name,self.dm.update_info,self.proid)
        if r['status_code'] == self.dm.expected_status_code:
            dictCompare = DictCompare()
            expected_result = xmltodict.parse((self.dm.update_info %self.proid))
            actual_result = r['result']
            if dictCompare.isSubsetDict(expected_result,actual_result):
                LogPrint().info("UpdateTemplateNic success.")
            else:
                LogPrint().error("UpdateTemplateNic fail.The nic_info is wrong")
                self.flag = False
        else:
            LogPrint().error("UpdateTemplateNic fail.The status_code is wrong")
            self.flag = False
        self.assertTrue(self.flag)
        
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))
        ProfilesAPIs().delProfile(self.dm.profile_name, self.nw_id)
class ITC070305_DeleteTemplateNic(BaseTestCase):
    '''
    @summary: 07模板管理-03模板网络接口-05删除网络接口
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.assertTrue(smart_create_template(self.dm.temp_name, self.dm.temp_info))
        self.assertTrue(smart_create_tempnic(self.dm.temp_name, self.dm.nic_data))
    def test_DeleteTemplateNic(self):  
        tempnic_api = TemplateNicsAPIs()
        r =  tempnic_api.deleteTemplateNic(self.dm.temp_name, self.dm.nic_name)
        if r['status_code'] == self.dm.expected_status_code:
            if not tempnic_api.getNicIdByName(self.dm.temp_name, self.dm.nic_name):
                LogPrint().info("DeleteTemplateNic pass.")
            else:
                LogPrint().error("DeleteTemplateNic fail.The nic is still exist.")
                self.flag = False
        else:
            LogPrint().error("DeleteTemplateNi fail.The status_code is wrong")
            self.flag = False
        self.assertTrue(self.flag)
    def tearDown(self):
        self.assertTrue(smart_delete_template(self.dm.temp_name))   
                                             
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test_cases = ["Template.ITC070102_GetTemplateInfo"]
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)