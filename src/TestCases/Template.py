#encoding:utf-8
'''
@author: keke
'''
import unittest
from BaseTestCase import BaseTestCase
from TestAPIs.DiskAPIs import DiskAPIs
from Utils.PrintLog import LogPrint
from Utils.Util import DictCompare,wait_until
from Utils.HTMLTestRunner import HTMLTestRunner
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs,VmDiskAPIs
from TestAPIs.TemplatesAPIs import TemplatesAPIs, TemplateDisksAPIs

import xmltodict
class ITC07_Setup(BaseTestCase):
    def test_Setup(self):
        pass

class ITC0701_GetTemplateList(BaseTestCase):


    def test_GetTemplateList(self):
        pass
class ITC0702_GetTemplateInfo(BaseTestCase):


    def test_GetTemplateInfo(self):
        pass
class ITC07030101_CreateTemplate(BaseTestCase):
    '''
    @summary: 07模板管理-03创建模板-01成功创建-01最小测试集
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
            
        #创建磁盘
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
        self.vm_id = self.vmapi.getVmIdByName(self.vm_name)
        r=self.vmdiskapi.attachDiskToVm(self.vm_name, self.disk_id)
        if r['status_code'] == 200:
            LogPrint().info("Attach Disk to vm success.")
        else:
            LogPrint().error("Attach Disk to vm fail.Status-code is wrong.")
            self.assertTrue(False)
    def test_CreateTemplate(self):
        self.tempapi = TemplatesAPIs()
        r = self.tempapi.createTemplate(self.dm.temp_info, self.vm_id)
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
        r = self.tempapi.delTemplate(self.dm.temp_name)
        if r['status_code'] == 200:
            LogPrint().info("Delete template success.")
        else:
            LogPrint().error("Delete template success")
        r = self.vmapi.delVm(self.vm_name)
        if r['status_code'] == 200:
            LogPrint().info("Delete vm success.")
        else:
            LogPrint().error("Delete vm success")
            
class ITC07030102_CreateTemplate_SD(BaseTestCase):
    '''
    @summary: 07模板管理-03创建模板-01成功创建-02指定存储域
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
            
        #创建磁盘
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
        self.vm_id = self.vmapi.getVmIdByName(self.vm_name)
        r=self.vmdiskapi.attachDiskToVm(self.vm_name, self.disk_id)
        if r['status_code'] == 200:
            LogPrint().info("Attach Disk to vm success.")
        else:
            LogPrint().error("Attach Disk to vm fail.Status-code is wrong.")
            self.assertTrue(False)
            
    def test_CreateTemplate_SD(self):
        self.tempapi = TemplatesAPIs()
        r = self.tempapi.createTemplate(self.dm.temp_info, self.vm_id,self.disk_id,self.dm.sd_id)
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
        r = self.tempapi.delTemplate(self.dm.temp_name)
        if r['status_code'] == 200:
            LogPrint().info("Delete template success.")
        else:
            LogPrint().error("Delete template success")
        r = self.vmapi.delVm(self.vm_name)
        if r['status_code'] == 200:
            LogPrint().info("Delete vm success.")
        else:
            LogPrint().error("Delete vm success")        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    test_cases = ["Template.ITC07030102_CreateTemplate_SD"]
    testSuite = unittest.TestSuite()
    loader = unittest.TestLoader()
    tests = loader.loadTestsFromNames(test_cases)
    testSuite.addTests(tests)
 
    unittest.TextTestRunner(verbosity=2).run(testSuite)