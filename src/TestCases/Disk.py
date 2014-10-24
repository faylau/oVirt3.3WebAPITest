#encoding:utf-8
'''

@author: keke
'''

import unittest

from BaseTestCase import BaseTestCase
from TestAPIs.DiskAPIs import DiskAPIs
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare,wait_until
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs,VmDiskAPIs
from TestAPIs.TemplatesAPIs import TemplatesAPIs, TemplateDisksAPIs

import xmltodict

def smart_create_disk(xml_disk_info, disk_alias=None, status_code=202):
    '''
    @summary: 智能创建磁盘，并等待其状态为ok；
    @param disk_alias: 磁盘别名，缺省为空（若在XML中已经提供）
    @param xml_disk_info: 创建磁盘的XML信息
    @param status_code: 成功创建磁盘后，接口返回的状态码，缺省为202
    @return: True or False
    '''
    disk_api = DiskAPIs()  
    r = disk_api.createDisk(xml_disk_info)
    def is_disk_ok():
        return disk_api.getDiskStatus(disk_id)=='ok'
    if r['status_code'] == status_code:
        disk_id = r['result']['disk']['@id']
        #如果磁盘状态在给定时间内变为ok状态，则继续验证状态码和磁盘信息
        if wait_until(is_disk_ok, 500, 5):
            LogPrint().info("PASS: Create disk '%s' SUCCESS and it's state is 'ok'." % disk_alias)
            return [True, disk_id]
        else:
            LogPrint().error("FAIL: Create Disk FAIED, it's status is not 'ok'." )
            return False
    else:
        LogPrint().error("FAIL: Create Disk FAIED, returned status code '%s' is wrong." % r['status_code'])
        return False
    
def smart_delete_disk(disk_id, xml_del_option='<action><async>false</async></action>', status_code=200):
    '''
    @summary: 智能删除磁盘，并等待其状态为ok；
    @param disk_alias: 磁盘别名，缺省为空（若在XML中已经提供）
    @param xml_disk_info: 创建磁盘的XML信息
    @param status_code: 成功创建磁盘后，接口返回的状态码，缺省为200
    @return: True or False
    '''
    disk_api = DiskAPIs()
    try:
        disk_api.getDiskInfo(disk_id)
        if disk_api.getDiskStatus(disk_id) != 'ok':
            LogPrint().warning("WARN: The disk is not 'ok'. It cannot be deleted.")
            return False
        else: 
            r = disk_api.deleteDisk(disk_id)
            if r['status_code']==status_code:
                LogPrint().info("PASS: Delete disk SUCCESS.")
                return True
            else:
                LogPrint().error("FAIL: Returned status code '%s' is WRONG while deleting disk." % r['status_code'])
                return False
    except:
        LogPrint().warning("WARN: Disk is not exist.")
        return True


class ITC0801_GetDiskList(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-01获取所有磁盘列表
    '''
  
    def test_GetDiskList(self):
        
        self.diskapi = DiskAPIs()
        r = self.diskapi.getDisksList()
        if r['status_code']==200:
            LogPrint().info('Get Disk list SUCCESS.')
            self.flag = True
        else:
            LogPrint().error('Get Disk list FAIL.')
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
        self.diskapi = DiskAPIs()  
        #首先新建一个磁盘并获取id
        self.disk_id = self.diskapi.createDisk(self.dm.disk_info)['result']['disk']['@id']
        
    
    def test_GetDiskInfo(self):
        '''
        @summary: 根据磁盘id获取磁盘信息
        '''
        r = self.diskapi.getDiskInfo(self.disk_id)
        if r['status_code']==self.dm.expected_status_code:
            dict_actual = r['result']
            dict_expected = xmltodict.parse(self.dm.disk_info)
            print dict_actual
            print dict_expected
            dictCompare = DictCompare()
            if dictCompare.isSubsetDict(dict_expected, dict_actual):
                LogPrint().info("Get Disk info SUCCESS." )
#                 return True
            else:
                LogPrint().error("Get Disk info INCORRECT.")
                self.flag = False
        else:
            LogPrint().error("Get Disk info FAILED. " )
            self.flag = False
        self.assertTrue(self.flag)
    def tearDown(self):
        '''
        @summary: 测试结束后的资源清理（恢复初始环境）
        '''
        self.diskapi.deleteDisk(self.disk_id, self.dm.async)     

class ITC080301_CreateDisk(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-03创建磁盘-01成功创建
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.diskapi = DiskAPIs()  
         
    def test_CreateDisk_iscsi_raw(self): 
        '''
        @note: 在iscsi存储域内创建raw类型磁盘
        @note: 若format=raw，则sparse必须为false，否则报错
        '''
        self.flag = True
        self.diskapi = DiskAPIs()
        r = self.diskapi.createDisk(self.dm.disk_info_raw)
        def is_disk_ok():
            return self.diskapi.getDiskStatus(self.disk_id)=='ok'
        if r['status_code'] == self.dm.expected_status_code:
            self.disk_id = r['result']['disk']['@id']
            #如果磁盘状态在给定时间内变为ok状态，则继续验证状态码和磁盘信息
            if wait_until(is_disk_ok, 200, 5):
                dict_actual = r['result']
                dict_expected = xmltodict.parse(self.dm.disk_info_raw)
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(dict_expected, dict_actual):
                    LogPrint().info("Create Disk SUCCESS-raw." )
#                 return True
                else:
                    LogPrint().error("Create Disk INCORRECT.The disk_info is wrong")
                    self.flag = False
            else:
                LogPrint().error("Create Disk FAIED,The status is not ok " )
                self.flag = False
        else:
            LogPrint().error("Create Disk FAIED,The status-code is wrong")
            self.flag = False
        
    def test_CreateDisk_iscsi_cow(self): 
        '''
        @note: 在iscsi存储域内创建cow类型磁盘
        @note: sprase必须设为true，sharable必须为false，否则报错
        '''
        self.flag = True
        self.diskapi = DiskAPIs()
        r = self.diskapi.createDisk(self.dm.disk_info_cow)
        def is_disk_ok():
            return self.diskapi.getDiskStatus(self.disk_id)=='ok'
        if r['status_code'] == self.dm.expected_status_code:
            self.disk_id = r['result']['disk']['@id']
            #如果磁盘状态在给定时间内变为ok状态，则继续验证状态码和磁盘信息
            if wait_until(is_disk_ok, 200, 5):
                dict_actual = r['result']
                dict_expected = xmltodict.parse(self.dm.disk_info_cow)
                dictCompare = DictCompare()
                if dictCompare.isSubsetDict(dict_expected, dict_actual):
                    LogPrint().info("Create Disk SUCCESS-raw." )
#                 return True
                else:
                    LogPrint().error("Create Disk INCORRECT.The disk_info is wrong")
                    self.flag = False
            else:
                LogPrint().error("Create Disk FAIED,The status is not ok " )
                self.flag = False
        else:
            LogPrint().error("Create Disk FAIED,The status-code is wrong")
            self.flag = False
            
    def tearDown(self):
        #print self.disk_id_raw
        #print self.disk_id_cow
#         self.diskapi.deleteDisk(self.disk_id_raw, self.dm.async)
        self.diskapi.deleteDisk(self.disk_id, self.dm.async)  
        

class ITC080302_CreateDisk_VerifyName(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-03创建磁盘-02验证名称合法性
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.diskapi = DiskAPIs()  
          
    def test_CreateDisk_VerifyName(self):
        '''
        @summary: 验证名称合法性：包含非法字符
        ''' 
        self.diskapi = DiskAPIs()
        r = self.diskapi.createDisk(self.dm.disk_info)
        if r['status_code']==self.dm.expected_status_code:
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
      
   

        
class ITC080303_CreateDisk_NoRequired(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-03创建一个配置集-03验证参数完整性
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.diskapi = DiskAPIs()  
          
    def test_CreateDisk_NoRequired(self):
        '''
        @summary: 分为四种情况,1）缺少存储域 2）缺少大小 3）缺少interface 4）缺少format 
        ''' 
        self.expected_result_index = 0
        self.diskapi = DiskAPIs()
        @BaseTestCase.drive_data(self, self.dm.disk_info)
        def do_test(xml_info):
            self.flag = True
            r = self.diskapi.createDisk(xml_info)
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

class ITC080304_CreateDisk_ErrorSet(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-03创建一个配置集-04错误配置
    '''
    def setUp(self):
        '''
        @summary: 测试用例执行前的环境初始化（前提）
        '''
        self.dm = super(self.__class__, self).setUp()
        self.diskapi = DiskAPIs()  
          
    def test_CreateDisk_ErrorSet(self):
        '''
        @summary: 分为三种情况
        1）format=raw，sparse=true
        2）format=cow，sparse=false
        3）format=cow，sparse=true,sharable=true
        ''' 
        self.expected_result_index = 0
        self.diskapi = DiskAPIs()
        @BaseTestCase.drive_data(self, self.dm.disk_info)
        def do_test(xml_info):
            self.flag = True
            r = self.diskapi.createDisk(xml_info)
            if r['status_code']==self.dm.expected_status_code[self.expected_result_index]:
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

        
class ITC080401_DeleteDisk(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-04删除磁盘-01磁盘无关联
    @note: 删除一个独立的磁盘，即没有附加在虚拟机和模板上
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.diskapi = DiskAPIs()  
        r = self.diskapi.createDisk(self.dm.disk_info)
        def is_disk_ok():
            return self.diskapi.getDiskStatus(self.disk_id)=='ok'
        if r['status_code'] ==202:
            self.disk_id = r['result']['disk']['@id']
            if wait_until(is_disk_ok, 200, 5):
                self.assertTrue(True)
            else:
                LogPrint.error("Create Disk overtime.Setup Failed.")
                self.assertTrue(False)
        else:
            LogPrint.error("Create Disk failed.Setup Failed.")
            self.assertTrue(False)
        
    def test_DeleteDisk_async(self): 
        self.flag = True
        r = self.diskapi.deleteDisk(self.disk_id, self.dm.async1)
        
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("Delete Disk async  SUCCESS." )
        else:
            LogPrint().error("Delete Disk async FAILED. " )
            self.flag = False
        self.assertTrue(self.flag)
    def test_DeleteDisk_sync(self): 
        self.flag = True
        r = self.diskapi.deleteDisk(self.disk_id, self.dm.async2)
        
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("Delete Disk sync SUCCESS." )
        else:
            LogPrint().error("Delete Disk sync FAILED. " )
            self.flag = False
        self.assertTrue(self.flag)
            
class ITC080402_DeleteDisk_AttachtoTemp(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-04删除磁盘-02磁盘附加到模板上
    @note: 待定
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.diskapi = DiskAPIs()
        self.vmapi = VirtualMachineAPIs()
        #创建一个虚拟机
        r = self.vmapi.createVm(self.dm.vm_info)
        if r['status_code'] == 201:
            self.vm_name = r['result']['vm']['name']
        else:
            LogPrint().error("Create vm failed.Status-code is wrong.")
            self.assertTrue(False)
            
        #创建一块磁盘
        '''
        @note: 创建磁盘时，磁盘的sharable属性必须为false，因为共享磁盘不作为模板的一部份
        '''
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
            
        #将该磁盘附加到虚拟机上
        self.vmdiskapi = VmDiskAPIs()
        r=self.vmdiskapi.attachDiskToVm(self.vm_name, self.disk_id)
        if r['status_code'] == 200:
            LogPrint().info("Attach Disk to vm success.")
        else:
            LogPrint().error("Attach Disk to vm fail.Status-code is wrong.")
            self.assertTrue(False)
            
        #该虚拟机创建模板   
        self.tempapi = TemplatesAPIs()
        self.vm_id = self.vmapi.getVmIdByName(self.vm_name)
        r = self.tempapi.createTemplate(self.dm.temp_info,self.vm_id)
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
            print self.disk_id_temp
        else:
            self.assertTrue(False)
        
    def test_DeleteDisk_AttachtoTemp(self): 
        self.flag = True
        r = self.diskapi.deleteDisk(self.disk_id_temp)
        print r
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
        self.tempapi.delTemplate(self.dm.temp_name)
        self.vmapi.delVm(self.vm_name)
 
class ITC080403_DeleteDisk_AttachtoRunVm(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-04删除磁盘-03磁盘附加到运行的虚拟机上
    @note: 待定
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.diskapi = DiskAPIs()
        self.vmapi = VirtualMachineAPIs()
        #创建一个虚拟机
        r = self.vmapi.createVm(self.dm.vm_info)
        if r['status_code'] == 201:
            self.vm_name = r['result']['vm']['name']
        else:
            LogPrint().error("Create vm failed.Status-code is wrong.")
            self.assertTrue(False)
            
        #创建一块磁盘
        '''
        @note: 创建磁盘时，磁盘的sharable属性必须为false，因为共享磁盘不作为模板的一部份
        '''
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
            
        #将该磁盘附加到虚拟机上
        self.vmdiskapi = VmDiskAPIs()
        r=self.vmdiskapi.attachDiskToVm(self.vm_name, self.disk_id)
        if r['status_code'] == 200:
            LogPrint().info("Attach Disk to vm success.")
        else:
            LogPrint().error("Attach Disk to vm fail.")
            self.assertTrue(False)
        #启动虚拟机
        r = self.vmapi.startVm(self.vm_name)
        def is_vm_up():
            return self.vmapi.getVmStatus(self.vm_name)=='up'
        if r['status_code'] == 200:
            if wait_until(is_vm_up, 300, 5):
                LogPrint().info("Start vm success.")
            else:
                LogPrint().error("Start vm overtime.")
                self.assertTrue(False)
                
        else:
            LogPrint().error("Start vm failed.Status-code is wrong.")
            self.assertTrue(False)
        #激活磁盘
        r = self.vmdiskapi.activateVmDisk(self.vm_name, self.disk_id)
        def is_vmdisk_ok():
            return self.vmdiskapi.getVmDiskStatus(self.vm_name, disk_id=self.disk_id)=='ok'
        if r['status_code'] == 200:
            if wait_until(is_vmdisk_ok,100,5):
                LogPrint().info("Activate vm disk success.")
            else:
                LogPrint().error("Activate vm disk overtime.")
                self.assertTrue(False)
        else:
            LogPrint().error("Activate vm disk fail.")
            self.assertTrue(False)
        
    def test_DeleteDisk_AttachtoRunVm(self): 
        self.flag = True
        r = self.diskapi.deleteDisk(self.disk_id)
        print r
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
        r = self.vmapi.stopVm(self.vm_name)
        def is_vm_down():
            return self.vmapi.getVmStatus(self.vm_name)=='down'
        if r['status_code'] == 200:
            if wait_until(is_vm_down, 100, 5):
                LogPrint().info("Stop vm success.")
            else:
                LogPrint().error("Stop vm overtime.")
        else:
            LogPrint().error("Stop vm fail.Status-code is wrong.")
        r = self.vmapi.delVm(self.vm_name)
        if r['status_code'] == 200:
            LogPrint().info("Delete vm success.")
        else:
            LogPrint().error("Delete vm success")

class ITC080404_DeleteDisk_AttachtoDownVm(BaseTestCase):
    '''
    @summary: ITC-08磁盘管理-04删除磁盘-04磁盘附加到已关机的虚拟机
    @note: 待定
    '''
    def setUp(self):
        self.dm = super(self.__class__, self).setUp()
        self.diskapi = DiskAPIs()
        self.vmapi = VirtualMachineAPIs()
        #创建一个虚拟机
        r = self.vmapi.createVm(self.dm.vm_info)
        if r['status_code'] == 201:
            self.vm_name = r['result']['vm']['name']
        else:
            LogPrint().error("Create vm failed.Status-code is wrong.")
            self.assertTrue(False)
            
        #创建一块磁盘
        '''
        @note: 创建磁盘时，磁盘的sharable属性必须为false，因为共享磁盘不作为模板的一部份
        '''
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
            
        #将该磁盘附加到虚拟机上
        self.vmdiskapi = VmDiskAPIs()
        r=self.vmdiskapi.attachDiskToVm(self.vm_name, self.disk_id)
        if r['status_code'] == 200:
            LogPrint().info("Attach Disk to vm success.")
        else:
            LogPrint().error("Attach Disk to vm fail.")
            self.assertTrue(False)
    def test_DeleteDisk_AttachtoDownVm(self): 
        self.flag = True
        r = self.diskapi.deleteDisk(self.disk_id)
        if r['status_code'] == self.dm.expected_status_code:
            LogPrint().info("Delete Disk  SUCCESS." )
        else:
            LogPrint().error("Delete Disk  FAILED. " )
            self.flag = False
        self.assertTrue(self.flag) 
        
    def tearDown(self):
        self.vmapi.delVm(self.vm_name)                  

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test_cases = ["Disk.ITC080404_DeleteDisk_AttachtoDownVm"]
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)