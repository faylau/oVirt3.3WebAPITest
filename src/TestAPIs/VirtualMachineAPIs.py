#encoding:utf-8
from Utils.Util import wait_until

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/10      初始版本                                                            Liu Fei
# V0.2           2014/11/04      加入若干smart方法                                        Liu Fei / Keke Wei
#---------------------------------------------------------------------------------
'''

import xmltodict

from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient
from Utils.PrintLog import LogPrint

def smart_create_vm(vm_name, xml_vm_info, status_code=201):
    '''
    @summary: 智能创建虚拟机
    '''
    vm_api = VirtualMachineAPIs()
    r = vm_api.createVm(xml_vm_info)
    if r['status_code'] == status_code:
        LogPrint().info("INFO-PASS: Create vm '%s' success." % vm_name)
        return True
    else:
        LogPrint().warning("INFO-WARN: Create vm '%s' FAILED. Returned status code is wrong." % vm_name)
        return False
    
def smart_del_vm(vm_name, xml_del_vm_option=None, status_code=200):
    '''
    @summary: 智能删除虚拟机（可以包含磁盘）；
    @param vm_name: 虚拟机名称；
    @param xml_del_vm_option: 删除虚拟机时使用的xml选项（不删除磁盘、强制删除等），缺省为None表示删除虚拟机及磁盘；
    '''
    vm_api = VirtualMachineAPIs()
    def is_vm_down():
        return vm_api.getVmStatus(vm_name)=='down'
    if vm_api.searchVmByName(vm_name):
        vm_state = vm_api.getVmStatus(vm_name)
        # 当VM状态为UP时，掉电，然后再删除
        if vm_state == 'up':
            LogPrint().info("INFO-STEP: Stop vm '%s' from 'up' to 'down' state." % vm_name)
            r = vm_api.stopVm(vm_name)
            if wait_until(is_vm_down, 50, 5):
                LogPrint().info("INFO-STEP: Delete vm '%s'." % vm_name)
                r = vm_api.delVm(vm_name)
                return r['status_code']==200
        # 当VM状态为Suspended时，掉电，然后再删除
        elif vm_state == 'suspended':
            LogPrint().info("INFO-STEP: Stop vm '%s' from 'suspended' to 'down' state." % vm_name)
            r = vm_api.stopVm(vm_name)
            if wait_until(is_vm_down, 100, 5):
                LogPrint().info("INFO-STEP: Delete vm '%s'." % vm_name)
                r = vm_api.delVm(vm_name)
                return r['status_code']==200
        # 当VM状态为Down时，直接删除
        elif vm_state == 'down':
            LogPrint().info("INFO-STEP: Delete vm '%s'." % vm_name)
            r = vm_api.delVm(vm_name)
            return r['status_code']==200
    else:
        LogPrint().info("INFO-WARN: Vm '%s' not exist." % vm_name)
        return True
    
def smart_start_vm(vm_name, xml_start_vm_option=None, status_code=200):
    '''
    @summary: 智能启动虚拟机（启动，并等待变为Up状态）
    '''
    vm_api = VirtualMachineAPIs()
    r = vm_api.startVm(vm_name)
    def is_vm_up():
        return vm_api.getVmStatus(vm_name)=='up'
    if wait_until(is_vm_up, 300, 5):
        if r['status_code'] == 200:
            LogPrint().info("INFO-PASS: Start vm '%s' SUCCESS." % vm_name)
            return True
        else:
            LogPrint().error("INFO-FAIL: Start vm '%s' FAILED. Returned status code is INCORRECT." % vm_name)
            return False
    else:
        LogPrint().error("INFO-FAIL: Start vm '%s' FAILED. It's final state is not 'UP'." % vm_name)
        return False
    
def smart_suspend_vm(vm_name, status_code=202):
    '''
    @summary: 智能挂起虚拟机（挂起，并等待变为suspended状态）
    '''
    vm_api = VirtualMachineAPIs()
    def is_vm_suspended():
        return vm_api.getVmStatus(vm_name)=='suspended'
    if vm_api.getVmStatus(vm_name) == 'suspended':
        LogPrint().info("INFO: Vm '%s' already in 'suspended' state." % vm_name)
        return True
    elif vm_api.getVmStatus(vm_name) == 'up':
        r = vm_api.suspendVm(vm_name)
        if wait_until(is_vm_suspended, 300, 5):
            if r['status_code'] == status_code:
                LogPrint().info("INFO-PASS: Suspend vm '%s' SUCCESS." % vm_name)
                return True
            else:
                LogPrint().error("INFO-FAIL: Suspend vm '%s' FAILED. Returned status code is INCORRECT." % vm_name)
                return False
        else:
            LogPrint().error("INFO-FAIL: Suspend vm '%s' FAILED. It's final state is not 'suspended'." % vm_name)
            return False

def smart_create_vmdisk(vm_name,disk_info,disk_alias,status_code=202):
    '''
    @summary: 为虚拟机创建磁盘
    '''
    vmdisk_api = VmDiskAPIs()
    r=vmdisk_api.createVmDisk(vm_name, disk_info)
    def is_disk_ok():
        return vmdisk_api.getVmDiskStatus(vm_name, disk_alias=disk_alias)=='ok'
    if r['status_code']==status_code:
        disk_id = r['result']['disk']['@id']
        if wait_until(is_disk_ok,600,5):
            LogPrint().info("Pre-Test:Create VMDisk success.")
            return [True,disk_id]
        else:
            LogPrint().error("Pre-Test:Create VMDisk overtime")
            return [False,None]
    else:
        LogPrint().error("Pre-Test:Create VMDisk failed.Status-code is wrong.")
        return [False,None]
    
def smart_delete_vmdisk(vm_name,disk_name,status_code=200):
    
    try:
        vmdiskapi = VmDiskAPIs()
        vmdiskapi.getVmDiskInfo(vm_name, disk_alias=disk_name)
        if vmdiskapi.getVmDiskStatus(vm_name, disk_alias=disk_name)!='ok':
            LogPrint().error("Post-Test:Disk '%s' is not ok.Can't delete it."%disk_name)
            return False
        else:
            r = vmdiskapi.delVmDisk(vm_name, disk_alias=disk_name)
            if r['status_code'] == 200:
                LogPrint().info("Post-Test:Delete Disk '%s'success."%disk_name)
                return True
            else:
                LogPrint().error("Post-Test:Delete Disk '%s' fail."%disk_name)
                return False
    except:
        LogPrint().warning("Post-Test:WARN: Disk '%s'is not exist."%disk_name)
        return True

def smart_active_vmdisk(vm_name,disk_id,status_code=200):
    '''
    @summary: 激活虚拟机的磁盘
    ''' 
    vmdisk_api = VmDiskAPIs()
    r = vmdisk_api.activateVmDisk(vm_name, disk_id=disk_id)
    def is_disk_active():
        return VmDiskAPIs().getVmDiskInfo(vm_name, disk_id=disk_id)['result']['disk']['active']=='true' 
    if r['status_code'] == status_code:
        if wait_until(is_disk_active, 100, 5):
            LogPrint().info("Active vmdisk success.")
            return True
        else:
            LogPrint().error("Active vmdisk overtime.")
        return False   
    else:
        LogPrint().error("Active vmdisk fail.")
        return False  

def smart_deactive_vmdisk(vm_name,disk_id,status_code=200):
    '''
    @summary: 取消激活虚拟机的磁盘
    ''' 
    vmdisk_api = VmDiskAPIs()
    r = vmdisk_api.deactivateVmDisk(vm_name, disk_id=disk_id)
    def is_disk_deactive():
        return VmDiskAPIs().getVmDiskInfo(vm_name, disk_id=disk_id)['result']['disk']['active']=='false'  
    if r['status_code'] == status_code:
        if wait_until(is_disk_deactive, 100, 5):
            LogPrint().info("Deactive vmdisk success.")
            return True
        else:
            LogPrint().error("Deactive vmdisk overtime.")
        return False   
    else:
        LogPrint().error("Deactive vmdisk fail.")
        return False    
def smart_create_vmnic(vm_name,nic_info,nic_name,status_code=201):
    vmnic_api=VmNicAPIs()
    r=vmnic_api.createVmNic(vm_name, nic_info)
    print r
    if r['status_code']==status_code:
        LogPrint().info("Create vmnic success.")
        return True
    else:
        LogPrint().error("Create vmnic fail.")
        return False
def smart_delete_vmnic(vm_name,nic_name,status_code=200):
    try:
        VmNicAPIs().getVmNicInfo(vm_name, nic_name)
        r=VmNicAPIs().delVmNic(vm_name, nic_name)
        if r['status_code']==status_code:
            LogPrint().info("Delete vmnic success.")
            return True
        else:
            LogPrint().error("Delete vmnic fail.")
            return False
    except:
        LogPrint().info("Vminc is not exist.")
        return True
            
        
        

class VirtualMachineAPIs(BaseAPIs):
    '''
    @summary: 提供VM各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义VM相关API的base_url，如'https://10.1.167.2/api/vms'
        '''
        self.base_url = '%s/vms' % WebBaseApiUrl
        
    def searchVmByName(self, vm_name):
        '''
        @summary: 根据名称查找VM
        @param vm_name: 集群名称
        @return: (1)字典格式的VM信息（以vm节点开头的单个VM信息）；（2）None。
        '''
        return self.searchObject('vms', vm_name)['result']['vms']
    
    def getVmIdByName(self, vm_name):
        '''
        @summary: 根据VM名称返回其id
        @param vm_name: VM名称
        @return: （1）VM的id；（2）None
        '''
        vm = self.searchVmByName(vm_name)
        if vm:
            return vm['vm']['@id']
        else:
            return None
    
    def getVmNameById(self, vm_id):
        '''
        @summary: 根据VM id获取其名称
        @param vm_id: 虚拟机id
        @return: 虚拟机名称
        '''
        api_url = '%s/%s' % (self.base_url, vm_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code==200:
            return xmltodict.parse(r.text)['vm']['name']
        
    def getVmsList(self):
        '''
        @summary: 获取全部虚拟机列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（全部虚拟机列表）。
        '''
        api_url = self.base_url
        method = "GET"
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)} 
    
    def getVmInfo(self, vm_name=None, vm_id=None):
        '''
        @summary: 根据集群名称，获取集群详细信息
        @param cluster_name: 集群名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的数据中心信息
        @raise HTTPError等: 通过raise_for_status()抛出失败请求
        '''
        if not vm_id and vm_name:
            vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s' % (self.base_url, vm_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        # 若出现无效HTTP响应时，抛出HTTPError异常
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getVmStatus(self, vm_name):
        '''
        @summary: 获取虚拟机状态
        @param vm_name: 虚拟机名称
        @return: 虚拟机当前状态
        '''
        return self.getVmInfo(vm_name)['result']['vm']['status']['state']
    
    def createVm(self, xml_vm_info):
        '''
        @summary: 创建虚拟机（从Blank模板/指定模板）
        @param xml_vm_info: XML格式的虚拟机配置信息：
        (1) 通常情况下，name/template/cluster是必须提供的:
            <vm>
                <name>vm-new</name>
                <description>Virtual Machine 2</description>
                <type>server</type>
                <memory>536870912</memory>
                <cluster>
                    <name>Default</name>
                </cluster>
                <template>
                    <name>Blank</name>
                </template>
                <cpu>
                    <topology sockets="2" cores="1"/>
                    <cpu_tune>
                        <vcpu_pin vcpu="0" cpu_set="1-4,^2"/>
                        <vcpu_pin vcpu="1" cpu_set="0,1"/>
                        <vcpu_pin vcpu="2" cpu_set="2,3"/>
                        <vcpu_pin vcpu="3" cpu_set="0,4"/>
                    </cpu_tune>
                    <cpu_mode>host_passthrough</cpu_mode>
                </cpu>
                <os>
                    <boot dev="hd"/>
                    <type>RHEL5</type>
                    <kernel/>
                    <initrd/>
                    <cmdline/>
                </os>
                <highly_available>
                    <enabled>true</enabled>
                    <priority>50</priority>
                </highly_available>
                <display>
                    <type>vnc</type>
                    <port>5910</port>
                    <monitors>1</monitors>
                    <smartcard_enabled>true</smartcard_enabled>
                </display>
                <stateless>false</stateless>
                <placement_policy>
                    <host id="2ab5e1da-b726-4274-bbf7-0a42b16a0fc3"/>
                    <affinity>migratable</affinity>
                </placement_policy>
                <memory_policy>
                    <guaranteed>536870912</guaranteed>
                </memory_policy>
                <usb>
                    <enabled>true</enabled>
                </usb>
                <custom_properties>
                    <custom _property value="124" name="sndbuf"/>
                </custom_properties>
            </vm>
        (2) 未验证：从模板创建虚拟机，对应的XML如下（若选择“克隆”，则disks下的clone设置为true）：
            <vm>
                <name>cloned_vm</name>
                <template id="64d4aa08-58c6-4de2-abc4-89f19003b886"/>
                <cluster id="99408929-82cf-4dc7-a532-9d998063fa95"/>
                <disks>
                    <clone>true</clone>
                    <disk id="4825ffda-a997-4e96-ae27-5503f1851d1b">
                        <format>COW</format>
                    </disk>
                    <disk id="42aef10d-3dd5-4704-aa73-56a023c1464c">
                        <format>COW</format>
                    </disk>
                </disks>
            </vm>
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_vm_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def updateVm(self, vm_name, xml_vm_update_info):
        '''
        @summary: 编辑虚拟机信息
        @param vm_name: 待编写的虚拟机名称
        @param xml_vm_update_info: 要编辑的信息（格式基本同创建虚拟机的XML文件），要注意的是：
        (1)以下元素可以在虚拟机创建之后（应该是Down状态时）：
            name/description/cluster/type/memory/cpu/os/high_availability/display/timezone/
            domain/stateless/placement_policy/memory_policy/usb/payloads/origin/custom_properties；
        (2)当虚拟机处于其他状态时，有一些项是无法编辑的，如内存。
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s' % (self.base_url, vm_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_vm_update_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def delVm(self, vm_name, xml_del_vm_option=None):
        '''
        @summary: 删除虚拟机（以不同形式删除）
        @param vm_name: 要删除的虚拟机名称
        @param xml_del_vm_option: XML格式的删除虚拟机选项，如强制删除、是否删除磁盘等：
        (1) 在不提供XML的情况下，删除VM时连同删除虚拟磁盘；
        (2) 删除VM时设置是否删除磁盘（detach_only为true时，不删除磁盘）：
            <action>
                <vm>
                    <disks>
                        <detach_only>true</detach_only>
                    </disks>
                </vm>
            </action>
        (3) 强制删除虚拟机（当VM处于faulty状态时）：
            <action>
                <force>true</force>
            </action>
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s' % (self.base_url, vm_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_del_vm_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def startVm(self, vm_name, xml_start_vm_option='<action/>'):
        '''
        @summary: 启动（运行/只运行一次）虚拟机
        @param vm_name: 虚拟机名称
        @param xml_start_vm_option: 启动虚拟机时的选项（通常是用于设定“只运行一次”中的选项），缺省为<action/>：
        (1) 当xml_start_vm_option为<action/>时，其对应的功能是“运行”虚拟机；
        (2) 当xml_start_vm_option为自定义值时，其对应的功能是“只运行一次”中的设置，下面列出一些常用值：
            <action>
                <pause>true</pause>
                <vm>
                    <stateless>true</stateless>
                    <display>
                        <type>spice</type>
                    </display>
                    <os>
                        <boot dev="cdrom "/>
                    </os>
                    <cdroms>
                        <cdrom>
                            <file id="windows-xp.iso"/>
                        </cdrom>
                    </cdroms>
                    <domain>
                        <name>domain.exam ple.com </nam e>
                        <user>
                            <user_name>domain_user</user_name>
                            <password>domain_password</password>
                        </user>
                    </domain>
                    <placement_policy>
                        <host id="02447ac6-bcba-448d-ba2b-f0f453544ed2"/>
                    </placement_policy>
                    <custom_properties>
                        <custom _property value="124" name="dataplane"/>
                    </custom_properties>
                </vm>
            </action>
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/start' % (self.base_url, vm_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_start_vm_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def stopVm(self, vm_name):
        '''
        @summary: 断电虚拟机
        @param vm_name: 虚拟机名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/stop' % (self.base_url, vm_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def shutdownVm(self, vm_name):
        '''
        @summary: 关闭虚拟机
        @param vm_name: 虚拟机名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/shutdown' % (self.base_url, vm_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def suspendVm(self, vm_name):
        '''
        @summary: 挂起虚拟机
        @param vm_name: 虚拟机名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/suspend' % (self.base_url, vm_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    
    def detachVmFromPool(self, vm_name, pool_name):
        '''
        @summary: 从虚拟机池中分享虚拟机
        @param vm_name: 虚拟机名称
        @param pool_name: 虚拟机池名称
        @return: 
        @todo: 未实现
        '''
        pass
    
    def migrateVm(self, vm_name, xml_migrate_option='<action/>'):
        '''
        @summary: 迁移虚拟机
        @param vm_name: 待迁移的虚拟机名称
        @param xml_migrate_option: 迁移选项，缺少为<action/>：
        (1) 当为缺省值时，自动选择迁移主机；
        (2) 当为非缺省值时，手动选择迁移主机（async和force两项似乎没什么作用）：
            <action>
                <host>
                    <name>host2</name>
                </host>
                <async>false</async>
                <force>true</force>
            </action>
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/migrate' % (self.base_url, vm_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_migrate_option)
        print r.status_code, r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def cancelMigration(self, vm_name):
        '''
        @summary: 取消迁移虚拟机
        @param vm_name: 虚拟机名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/cancelmigration' % (self.base_url, vm_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        print r.status_code, r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def exportVm(self, vm_name, xml_export_vm_option=None):
        '''
        @summary: 导出虚拟机
        @param vm_name: 虚拟机名称
        @param xml_export_vm_option: XML格式的虚拟机导出配置项（示例如下），其中：
        (1) 虚拟机处于Down状态时才能进行Export操作；
        (2) exclusive：当导出域中有同名虚拟机时，将该参数设置为true表示覆盖导出；
        (3) discard_snapshots：设置为true时，表示导出的虚拟机将不包含snapshot；
        (4) async：设置为true时，表示服务器将该请求作异步处理，调用该接口后服务器返回202，表示已接受请求，但同时也可以处理其他请求；
                            若设置为false，则操作完成后服务器端才会返回结果。
            <action>
                <storage_domain>
                    <name>export1</name>
                </storage_domain>
                <async>true</async>
                <exclusive>true</exclusive>
                <discard_snapshots>true</discard_snapshots>
            </action>
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/export' % (self.base_url, vm_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_export_vm_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def ticketVm(self, vm_name, xml_ticket_option):
        '''
        @summary: 暂不清楚该接口的功能（可能是设置虚拟机显示过期时间）
        @todo: 未实现
        '''
        pass
    
    def statisticsVm(self, vm_name):
        '''
        @summary: 统计虚拟机信息
        @param vm_name: 虚拟机名称
        @return: 字典：（1）status_code：请求返回码（200）；（2）result：dict形式的VM统计信息。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/statistics' % (self.base_url, vm_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    
class VmDiskAPIs(VirtualMachineAPIs):
    '''
    @summary: VM的磁盘管理子接口类，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义VM相关API的base_url，如'https://10.1.167.2/api/vms'
        '''
        self.base_url = '%s/vms' % WebBaseApiUrl
        self.sub_url_disks = 'disks'
        
    def getVmDisksList(self, vm_name):
        '''
        @summary: 获取虚拟机磁盘列表
        @param vm_name: 虚拟机名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的VM磁盘列表。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_disks)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def getVmDiskIdByName(self, vm_name, disk_alias):
        '''
        @summary: 根据虚拟机磁盘名称返回磁盘ID
        @param vm_name: 虚拟机名称
        @param disk_name: 虚拟机磁盘别名
        @attention: 该函数执行的前提是，同一虚拟机的磁盘名称唯一
        @return: 返回虚拟机磁盘ID
        '''
        vm_disks = self.getVmDisksList(vm_name)['result']['disks']['disk']
        if isinstance(vm_disks, list):
            for disk in vm_disks:
                if disk['alias']==disk_alias:
                    return disk['@id']
        else:
            if vm_disks['alias']==disk_alias:
                return vm_disks['@id']
    
    def getVmDiskInfo(self, vm_name, disk_alias=None, disk_id=None):
        '''
        @summary: 根据虚拟机名称、磁盘别名获取虚拟机磁盘信息
        @param vm_name: 虚拟机名称
        @param disk_alias: 磁盘别名
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的VM磁盘信息。
        '''
        if disk_alias and not disk_id:
            disk_id = self.getVmDiskIdByName(vm_name, disk_alias)
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_disks, disk_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        print r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getVmDiskStatus(self, vm_name, disk_alias=None, disk_id=None):
        '''
        @summary: 获取虚拟机磁盘的状态
        @param vm_name: 虚拟机名称
        @param disk_alias: 虚拟机磁盘别名
        @return: 磁盘状态（illegal、locked、ok）
        '''
        disk_info = self.getVmDiskInfo(vm_name, disk_alias, disk_id)
        return disk_info['result']['disk']['status']['state']
    
    def is_vmdisk_exist(self,vm_name,disk_id):
        '''
        @summary: 虚拟机内是否存在该磁盘
        '''
        flag=False
        vm_disks = self.getVmDisksList(vm_name)['result']['disks']
        if not vm_disks:
            return flag
        vm_disks = self.getVmDisksList(vm_name)['result']['disks']['disk']
        if isinstance(vm_disks, list):
            for disk in vm_disks:
                if disk['@id']==disk_id:
                    flag=True
        else:
            if vm_disks['@id']==disk_id:
                flag=True
        return flag
                
        
        
    def createVmDisk(self, vm_name, xml_disk_info):
        '''
        @summary: 为虚拟机添加磁盘（包括创建、附加等功能）
        @param vm_name: 虚拟机名称
        @param xml_disk_info: XML格式的创建磁盘信息：
        (1) 创建内部磁盘：
            <disk>
                <storage_domains>
                    <storage_domain>
                        <name>data</name>
                    </storage_domain>
                </storage_domains>
                <alias>test1_Disk2</alias>
                <size>1073741824</size>        # 单位为B
                <type>system</type>            # system为系统盘（可引导的），不写该字段时为普通盘；
                <interface>virtio</interface>
                <sparse>false</sparse>         # false：Preallocated（raw）；true：thin Provision（cow）
                <format>cow</format>           # 可取值为cow/raw，分别与thin/preallocated对应
                <bootable>true</bootable>      # 可启动的（注意，与可引导的不同）
                <shareable>true</shareable>    # 可共享的
                <wipe_after_delete>true</wipe_after_delete> # 删除后清理
            </disk>
        (2) 创建外部磁盘：此处XML如何组织尚未研究
        (3) 附加游离状态的磁盘：
            <disk id="a1a4b4aa-8239-4ab8-a14b-d0d31a73561c"/>
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        @bug: 该接口可能存在问题，可以同时定义多个bootable的磁盘
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_disks)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_disk_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def updateVmDisk(self, vm_name, disk_alias, xml_update_disk_info):
        '''
        @summary: 更新虚拟机磁盘
        @param vm_name: 虚拟机名称
        @param disk_alias: 虚拟机磁盘别名
        @param xml_update_disk_info: XML格式的更新信息；
                    包括name/description/storage_domains/interface/bootable/shareable/wipe_after_delete/propagate_errors等字段信息
            <disk>
                <name>Disk22222222</name>
                <description>hahahahaah</description>
                <bootable>false</bootable>
                <shareable>true</shareable>
            </disk>
        @return: 
        '''
        vm_id = self.getVmIdByName(vm_name)
        disk_id = self.getVmDiskIdByName(vm_name, disk_alias)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_disks, disk_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_update_disk_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def delVmDisk(self, vm_name, disk_alias=None, disk_id=None, xml_del_disk_option=None):
        '''
        @summary: 删除虚拟机磁盘（分离/彻底删除）
        @param vm_name: 虚拟机名称
        @param disk_id: 虚拟机磁盘id（磁盘的id和name至少要有一个）
        @param disk_alias: 虚拟机磁盘别名（磁盘的id和name至少要有一个）
        @param xml_del_disk_option: XML格式的删除磁盘选项：
        (1) 缺省为None（进行的是分离操作）
        (2) 彻底删除虚拟机磁盘（detach设置为false）：
            <action>
                <detach>false</detach>
            </action>
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        if not disk_id:
            disk_id = self.getVmDiskIdByName(vm_name, disk_alias)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_disks, disk_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_del_disk_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def statisticsVmDisk(self, vm_name, disk_id=None, disk_alias=None):
        '''
        @summary: 获取虚拟机磁盘（附加在虚拟机中的磁盘）统计信息
        @param vm_name: 虚拟机名称
        @param disk_id: 虚拟机磁盘ID（缺省为None，可以不提供，推荐提供）
        @param disk_alias: 虚拟机磁盘别名（缺省为None，与disk_id必须提供其中一个参数）
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        if not disk_id:
            disk_id = self.getVmDiskIdByName(vm_name, disk_alias)
        api_url = '%s/%s/%s/%s/statistics' % (self.base_url, vm_id, self.sub_url_disks, disk_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def attachDiskToVm(self, vm_name, disk_id):
        '''
        @summary: 将已有磁盘附加到VM
        @param vm_name: 虚拟机名称
        @param disk_id: 虚拟磁盘ID，缺省为None
        @bug: 目前不支持使用disk_name（因为disks接口中没有根据disk名称获取id的函数）
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        xml_disk_info = '''<disk id="%s"/>'''% disk_id
        return self.createVmDisk(vm_name, xml_disk_info)
#         api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_disks)
#         method = 'POST'
#         xml_attach_disk = '''<disk id="%s"/>'''% disk_id
#         r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_attach_disk)
#         return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def detachDiskFromVm(self, vm_name, disk_id):
        '''
        @summary: 将已有磁盘从VM分离（功能同delVmDisk函数中当detach=true时的功能）
        @param vm_name: 虚拟机名称
        @param disk_id: 虚拟磁盘ID，缺省为None
        @bug: 目前不支持使用disk_name（因为disks接口中没有根据disk名称获取id的函数）
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        xml_del_disk_option = '''
        <action>
            <detach>true</detach>
        </action>
        '''
        return self.delVmDisk(vm_name, disk_id=disk_id, xml_del_disk_option=xml_del_disk_option)
#         vm_id = self.getVmIdByName(vm_name)
#         api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_disks)
#         method = 'POST'
#         xml_attach_disk = '''<disk id="%s"/>'''% disk_id
#         r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_attach_disk)
#         return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}

    def activateVmDisk(self, vm_name, disk_id=None, disk_alias=None):
        '''
        @summary: 激活虚拟机的磁盘
        @param vm_name: 虚拟机名称
        @param disk_id: 待激活的虚拟机磁盘id，缺省为None
        @param disk_alias: 待激活的虚拟机磁盘别名，缺省为None（disk_id和disk_name必须提供其中之一，推荐使用disk_id）
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        if not disk_id:
            disk_id = self.getVmDiskIdByName(vm_name, disk_alias)
        api_url = '%s/%s/%s/%s/activate' % (self.base_url, vm_id, self.sub_url_disks, disk_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def deactivateVmDisk(self, vm_name, disk_id=None, disk_alias=None):
        '''
        @summary: 取消激活虚拟机的磁盘
        @param vm_name: 虚拟机名称
        @param disk_id: 待激活的虚拟机磁盘id，缺省为None
        @param disk_alias: 待激活的虚拟机磁盘别名，缺省为None（disk_id和disk_name必须提供其中之一，推荐使用disk_id）
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        if not disk_id:
            disk_id = self.getVmDiskIdByName(vm_name, disk_alias)
        api_url = '%s/%s/%s/%s/deactivate' % (self.base_url, vm_id, self.sub_url_disks, disk_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def moveVmDisk(self, vm_name, xml_move_option, disk_id=None, disk_alias=None):
        '''
        @summary: 移动虚拟机磁盘到指定的存储域
        @param vm_name: 虚拟机名称
        @param disk_id: 待激活的虚拟机磁盘id，缺省为None
        @param disk_alias: 待激活的虚拟机磁盘别名，缺省为None（disk_id和disk_name必须提供其中之一，推荐使用disk_id）
        @param xml_move_info: XML格式的虚拟机磁盘移动设置信息：
            <action>
                <storage_domain>
                    <name>storage2</name>
                </storage_domain>
                <async>false</async>
            </action>
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        if not disk_id:
            disk_id = self.getVmDiskIdByName(vm_name, disk_alias)
        api_url = '%s/%s/%s/%s/move' % (self.base_url, vm_id, self.sub_url_disks, disk_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_move_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def exportVmDisk(self, vm_name, xml_export_option, disk_id=None, disk_alias=None):
        '''
        @summary: 导出虚拟机磁盘
        @param vm_name: 虚拟机名称
        @param xml_export_info: XML格式的虚拟机磁盘导出设置
        @param disk_id: 待激活的虚拟机磁盘id，缺省为None
        @param disk_alias: 待激活的虚拟机磁盘别名，缺省为None（disk_id和disk_name必须提供其中之一，推荐使用disk_id）
        @return: 
        @bug: 该接口调试未通过，UI上对应的功能也无法使用。
        '''
        vm_id = self.getVmIdByName(vm_name)
        if not disk_id:
            disk_id = self.getVmDiskIdByName(vm_name, disk_alias)
        api_url = '%s/%s/%s/%s/export' % (self.base_url, vm_id, self.sub_url_disks, disk_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_export_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
class VmNicAPIs(VirtualMachineAPIs):
    '''
    @summary: VM的网络接口管理子接口类，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义VM Nic相关API的base_url，如'https://10.1.167.2/api/vms'
        '''
        self.base_url = '%s/vms' % WebBaseApiUrl
        self.sub_url_nics = 'nics'
    def isVmNicExist(self,vm_name,nic_name):
        '''
        @summary: 检查虚拟机的网络接口是否存在，存在返回True，否则返回False
        '''
        nic_list = self.getVmNicsList(vm_name)['result']['nics']['nic']
        flag = False
        if isinstance(nic_list, dict):
            if nic_list['name'] == nic_name:
                return True
            else:
                return False
        else:
            for nic in nic_list:
                if nic['name'] == nic_name:
                    flag=True
            return flag
            
    
    def getVmNicIdByName(self, vm_name, nic_name):
        '''
        @summary: 根据虚拟机Nic的名称返回其id
        @param vm_name: 虚拟机名称
        @param nic_name: 虚拟机Nic名称
        @return: 虚拟机Nic的ID
        '''
        vm_nics = self.getVmNicsList(vm_name)['result']['nics']['nic']
        if isinstance(vm_nics, list):
            for nic in vm_nics:
                if nic['name']==nic_name:
                    return nic['@id']
        else:
            if vm_nics['name']==nic_name:
                return vm_nics['@id']
        
    def getVmNicsList(self, vm_name):
        '''
        @summary: 获取虚拟机的Nic列表
        @param vm_name: 虚拟机名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的虚拟机Nic列表。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_nics)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getVmNicInfo(self, vm_name, nic_name):
        '''
        @summary: 获取指定的虚拟机Nic详细信息
        @param vm_name: 虚拟机名称
        @param nic_name: 虚拟机Nic名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的Nic详细信息。
        '''
        vm_id = self.getVmIdByName(vm_name)
        nic_id = self.getVmNicIdByName(vm_name, nic_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_nics, nic_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def createVmNic(self, vm_name, xml_vm_nic_info):
        '''
        @summary: 为虚拟机创建网络接口
        @param vm_name: 虚拟机名称
        @param xml_vm_nic_info: XML格式的，要创建的虚拟机Nic信息：
        (1) name是必须要指定的，其他都是可选字段（有缺省值）；
        (2) vnic_profile若不指定则为空，若指定则必须提供vnic_profile的id；
            <nic>
                <name>nic2</name>
                <vnic_profile id="6f1bff46-d0aa-49d2-9206-0bc9a4adf6aa"/>
                <interface>virtio</interface>
                <linked>false</linked>
                <plugged>false</plugged>
                <mac address="00:1a:4a:16:84:07"/>
            </nic>
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的Nic详细信息及操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_nics)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_vm_nic_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def updateVmNic(self, vm_name, nic_name, xml_update_vm_nic_info):
        '''
        @summary: 更新虚拟机Nic信息
        @param vm_name: 虚拟机名称
        @param nic_name: 虚拟机Nic名称
        @param xml_update_vm_nic_info: XML格式，虚拟机Nic的更新信息：
            <nic>
                <name>nic22</name>
                <vnic_profile id="6f1bff46-d0aa-49d2-9206-0bc9a4adf6aa"/>
                <interface>e1000</interface>
                <linked>false</linked>
                <plugged>false</plugged>
                <mac address="00:1a:4a:16:84:08"/>
            </nic>
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的Nic更新后信息。
        '''
        vm_id = self.getVmIdByName(vm_name)
        nic_id = self.getVmNicIdByName(vm_name, nic_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_nics, nic_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_update_vm_nic_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def delVmNic(self, vm_name, nic_name):
        '''
        @summary: 删除虚拟机Nic
        @param vm_name: 虚拟机名称
        @param nic_name: 虚拟机Nic名称（每个VM中的Nic名称是唯一的）
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的删除操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        nic_id = self.getVmNicIdByName(vm_name, nic_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_nics, nic_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def statisticsVmNic(self, vm_name, nic_name):
        '''
        @summary: 获取虚拟机Nic的统计信息
        @param vm_name: 虚拟机名称
        @param nic_name: 虚拟机Nic名称
        @return: （1）status_code：请求返回码；（2）result：dict形式的统计结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        nic_id = self.getVmNicIdByName(vm_name, nic_name)
        api_url = '%s/%s/%s/%s/statistics' % (self.base_url, vm_id, self.sub_url_nics, nic_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def activateVmNic(self, vm_name, nic_name):
        '''
        @summary: 激活虚拟机Nic
        @param vm_name: 虚拟机名称
        @param nic_name: 虚拟机Nic名称
        @return: （1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        nic_id = self.getVmNicIdByName(vm_name, nic_name)
        api_url = '%s/%s/%s/%s/activate' % (self.base_url, vm_id, self.sub_url_nics, nic_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def deactivateVmNic(self, vm_name, nic_name):
        '''
        @summary: 取消激活虚拟机Nic
        @param vm_name: 虚拟机名称
        @param nic_name: 虚拟机Nic名称
        @return: （1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        nic_id = self.getVmNicIdByName(vm_name, nic_name)
        api_url = '%s/%s/%s/%s/deactivate' % (self.base_url, vm_id, self.sub_url_nics, nic_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
class VmCdromAPIs(VirtualMachineAPIs):
    '''
    @summary: VM的CDROM管理子接口类，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义VM Nic相关API的base_url，如'https://10.1.167.2/api/vms'
        '''
        self.base_url = '%s/vms' % WebBaseApiUrl
        self.sub_url_cdroms = 'cdroms'
        
    def getVmCdromsList(self, vm_name):
        '''
        @summary: 获取虚拟机CDROMs列表
        @param vm_name: 虚拟机名称
        @return: （1）status_code：请求返回码；（2）result：dict形式的虚拟机CD列表。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_cdroms)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def getVmCdromInfo(self, vm_name, cdrom_id='00000000-0000-0000-0000-000000000000'):
        '''
        @summary: 获取虚拟机的CDROM信息
        @param vm_name: 虚拟机名称
        @return: 
        @note: 目前每个vm只有一个CDROM，且ID是固定的。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_cdroms, cdrom_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def addCdromFile(self, vm_name, file_id, cdrom_id='00000000-0000-0000-0000-000000000000'):
        '''
        @summary: 为虚拟机添加CDROM文件
        @param vm_name: 虚拟机名称
        @param file_id: CDROM文件ID（与名称一致）
        @param cdrom_id: 虚拟机CDROM的ID
        @return: 
        @todo: 未完成（接口本身可能存在问题）
        '''
        pass
    
    def changeCdromFile(self):
        '''
        @summary: 为虚拟机添加CDROM文件
        @param vm_name: 虚拟机名称
        @param file_id: CDROM文件ID（与名称一致）
        @param cdrom_id: 虚拟机CDROM的ID
        @return: 
        @todo: 未完成（接口本身可能存在问题）
        '''
        pass
    
class VmSnapshotAPIs(VirtualMachineAPIs):
    '''
    @summary: VM的Snapshot管理子接口类，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义VM Snapshot相关API的base_url，如'https://10.1.167.2/api/vms'
        '''
        self.base_url = '%s/vms' % WebBaseApiUrl
        self.sub_url_snapshots = 'snapshots'
        
    def getVmSnapshotsList(self, vm_name):
        '''
        @summary: 查看虚拟机全部Snapshot列表
        @param vm_name: 虚拟机名称
        @return: （1）status_code：请求返回码；（2）result：dict形式的虚拟机快照列表。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_snapshots)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getVmSnapshotInfo(self, vm_name, snapshot_id):
        '''
        @summary: 根据snapshot id获取虚拟机Snapshot信息
        @param vm_name: 虚拟机名称
        @param snapshot_id: 快照ID
        @return: （1）None（snapshot不存在） ；（2）status_code：请求返回码；result：dict形式的快照信息。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_snapshots, snapshot_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code == 404:
            print "The snapshot not exist. Details: %s, %s" % (r.status_code, r.text)
            return None
        else:
            return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def createVmSnapshot(self, vm_name, xml_snapshot_info):
        '''
        @summary: 创建虚拟机快照（包括在线快照、离线快照、带内存快照等）
        @param vm_name: 虚拟机名称
        @param xml_snapshot_info: 要创建的快照信息，如：
        (1) 根据persist_memorystate参数来指定是否创建带内存的快照；
        (2) 当创建离线快照时，persist_memorystate参数无效；
            <snapshot>
                <description>snapshot3</description>
                <persist_memorystate>false</persist_memorystate>
            </snapshot>
        @return: （1）status_code：请求返回码；（2）result：dict形式的新建快照信息。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_snapshots)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_snapshot_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def restoreVmSnapshot(self, vm_name, snapshot_id, xml_restore_option='<action/>'):
        '''
        @summary: 恢复虚拟机快照
        @param vm_name: 虚拟机名称
        @param snapshot_id: 虚拟机快照ID
        @param xml_restore_option: 恢复虚拟机快照的操作选项同，缺省值为<action/>
        @return: （1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s/%s/restore' % (self.base_url, vm_id, self.sub_url_snapshots, snapshot_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_restore_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def cloneVmFromSnapshot(self, xml_clone_vm_option):
        '''
        @summary: 从快照克隆虚拟机（实际上调用的是创建虚拟机的API：VirtualMachineAPIs.createVm）
        @param xml_clone_vm_option: XML格式的克隆设置项：
        (1) 最基本的形式如下：只设定vm名称、cluster以及snapshot id，就可以完成直接从快照克隆虚拟机
            <vm>
                <name>vmSnapshot</name>
                <cluster>
                    <name>Cluster-ISCSI</name>
                </cluster>
                <snapshots>
                    <snapshot id="xxxxxxxxxx"/>
                </snapshots>
            </vm>
        (2) 在指定snapshot id的同时，也可以对VM的常规设置项进行配置，具体可参见createVm的接口参数。
        @return: （1）status_code：请求返回码（202）；（2）result：dict形式的新建VM信息。
        '''
        return self.createVm(xml_clone_vm_option)
    
    def delVmSnapshot(self, vm_name, snapshot_id):
        '''
        @summary: 删除虚拟机快照
        @param vm_name: 虚拟机名称
        @param 快照id: 
        @return: （1）status_code：请求返回码（202）；（2）result：dict形式的操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_snapshots, snapshot_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}

class VmWatchdogAPIs(VirtualMachineAPIs):
    '''
    @summary: VM的Watchdog管理子接口类，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义VM Watchdog相关API的base_url，如'https://10.1.167.2/api/vms'
        '''
        self.base_url = '%s/vms' % WebBaseApiUrl
        self.sub_url_watchdogs = 'watchdogs'
        
    def getVmWatchdogsList(self, vm_name):
        '''
        @summary: 获取虚拟机的watchdog设备列表
        @param vm_name: 虚拟机名称
        @return: （1）status_code：请求返回码（200）；（2）result：None或Watchdog列表。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_snapshots)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getVmWatchdogInfo(self, vm_name, watchdog_id='00000000-0000-0000-0000-000000000000'):
        '''
        @summary: 获取虚拟机Watchdog信息（目前每个VM只能有一个Watchdog，所以Watchdog是唯一的）
        @param vm_name: 虚拟机名称
        @param watchdog_id: 虚拟机watchdog的id，缺省为00000000-0000-0000-0000-000000000000
        @return: （1）None：watchdog不存在；或：（2）Dict格式，包括状态码和返回的watchdog信息。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_watchdogs, watchdog_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code == 404:
            print 'There is no watchdog with %s. Details: %s, %s' % (vm_name, r.status_code, r.text)
        else:
            return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def createVmWatchdog(self, vm_name, xml_watchdog_info):
        '''
        @summary: 为虚拟机增加watchdog设备
        @param vm_name: 虚拟机名称
        @param xml_watchdog_info: watchdog设备信息，如：
            <watchdog>
                <model>i6300esb</model>
                <action>reset</action>
            </watchdog>
        @return: （1）status_code：请求返回码（201）；（2）result：XML格式的，创建的watchdog信息。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_watchdogs)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_watchdog_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def updateVmWatchdog(self, vm_name, xml_watchdog_update_info, watchdog_id='00000000-0000-0000-0000-000000000000'):
        '''
        @summary: 更新虚拟机watchdog信息
        @param vm_name: 虚拟机名称
        @param xml_watchdog_update_info: 更新的watchdog配置信息:
            <watchdog>
                <model>i6300esb</model>
                <action>dump</action>
            </watchdog> 
        @param watchdog_id: 虚拟机watchdog设备id，有缺省值
        @return: （1）status_code：请求返回码（200）；（2）result：（XML格式）更新后的watchdog信息。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_watchdogs, watchdog_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_watchdog_update_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def delVmWatchdog(self, vm_name, wathchdog_id='00000000-0000-0000-0000-000000000000', xml_del_optoin=None):
        '''
        @summary: 删除虚拟机watchdog
        @param vm_name: 虚拟机名称
        @param watchdog_id: 虚拟机watchdog的id
        @return:  （1）status_code：请求返回码；（2）result：（XML格式）删除操作结果。
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, vm_id, self.sub_url_watchdogs, wathchdog_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code == 404:
            print "No watchdog for vm '%s'. Details: %s, %s" % (vm_id, r.status_code, r.text)
            return None
        else:
            return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}

class VmAppAPIs(VirtualMachineAPIs):
    '''
    @summary: VM的Applicatoins管理子接口类，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义VM Watchdog相关API的base_url，如'https://10.1.167.2/api/vms'
        '''
        self.base_url = '%s/vms' % WebBaseApiUrl
        self.sub_url_applications = 'applications'
        
    def getVmAppsList(self, vm_name):
        '''
        @summary: 获取虚拟机Applications列表
        @param vm_name: 虚拟机名称
        @return: 
        @note: 该接口可能存在bug，当application为空时，接口抛出异常，返回500状态码
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/%s' % (self.base_url, vm_id, self.sub_url_applications)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        print r.status_code, r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getVmAppInfo(self, vm_name, app_id):
        '''
        @summary: 获取Application的具体信息
        @param vm_name: 虚拟机名称
        @todo: 未完成，Application信息较少等需要使用该方法的时候再进行补充。
        '''
        pass

    
if __name__=='__main__':
    vmapi = VirtualMachineAPIs()
    vmdiskapi = VmDiskAPIs()
    vmnicapi = VmNicAPIs()
    print vmnicapi.isVmNicExist('vm-ITC05', 'nic3')
    vmcdromapi = VmCdromAPIs()
    vmsnapshotapi = VmSnapshotAPIs()
    vmwatchdogapi = VmWatchdogAPIs()
    vmappapi = VmAppAPIs()
    print vmdiskapi.is_vmdisk_exist('vm-ITC05', 'f3057dff-5f5d-4b80-87e6-3f9884e72f57')
    
#     print vmdiskapi.getVmDiskInfo('aa', disk_id='5a4356cd-b6fb-4760-b95e-db3981b65df5')
#     print vmdiskapi.getVmDiskStatus('aa', disk_id='5a4356cd-b6fb-4760-b95e-db3981b65df5')
    
#     print vmappapi.getVmAppsList('test1')
    
#     print vmwatchdogapi.delVmWatchdog('test1')
    
    xml_watchdog_update_info = '''
    <watchdog>
        <model>i6300esb</model>
        <action>None</action>
    </watchdog>
    '''
#     print vmwatchdogapi.updateVmWatchdog('test1', xml_watchdog_update_info)
    
    xml_watchdog_info = '''
    <watchdog>
        <model>i6300esb</model>
        <action>reset</action>
    </watchdog>
    '''
#     print vmwatchdogapi.createVmWatchdog('test1', xml_watchdog_info)
    
#     print vmwatchdogapi.getVmWatchdogInfo('ns6.0')
#     print vmwatchdogapi.getVmWatchdogsList('ns6.0')
    
#     print vmapi.statisticsVm('test1')
#     print vmsnapshotapi.delVmSnapshot('test1', '6bc34709-f21c-4832-a703-437888d65767')
    
    xml_clone_vm_option = '''
    <vm>
        <name>vmSnapshot</name>
        <cluster>
            <name>Default</name>
        </cluster>
        <snapshots>
            <snapshot id="5806b12f-a9e9-4666-933b-86ca9dc395fd"/>
        </snapshots>
    </vm>
    '''
#     print vmsnapshotapi.cloneVmFromSnapshot(xml_clone_vm_option)
    
#     print vmsnapshotapi.restoreVmSnapshot('test1', '5806b12f-a9e9-4666-933b-86ca9dc395fd')
    
    xml_snapshot_info = '''
    <snapshot>
        <description>snapshot3</description>
        <persist_memorystate>false</persist_memorystate>
    </snapshot>
    '''
#     print vmsnapshotapi.createVmSnapshot('test1', xml_snapshot_info)
    
#     print vmsnapshotapi.getVmSnapshotInfo('test1', '5806b12f-a9e9-4666-933b-86ca9dc395fd')
#     print vmsnapshotapi.getVmSnapshotsList('test1')
    
#     print vmcdromapi.getVmCdromsList('test1')
#     print vmcdromapi.getVmCdromInfo('test1')
#     print vmnicapi.deactivateVmNic('test1', 'nic1')
#     print vmnicapi.activateVmNic('test1', 'nic1')
#     print vmnicapi.statisticsVmNic('test1', 'nic1')
#     print vmnicapi.delVmNic('test1', 'nic22')
    
    xml_update_vm_nic_info = '''
    <nic>
        <name>nic22</name>
        <vnic_profile id="54cdf976-03cd-4143-bd87-dbdc26508f28"/>
        <interface>e1000</interface>
        <linked>false</linked>
        <plugged>false</plugged>
        <mac address="00:1a:4a:16:84:08"/>
    </nic>
    '''
#     print vmnicapi.updateVmNic('test1', 'nic2', xml_update_vm_nic_info)
    
    xml_vm_nic_info = '''
    <nic>
        <name>nic2</name>
        <network>
            <name>aaa</name>
        </network>
        <vnic_profile>
            <name>test2</name>
        </vnic_profile>
        <interface>virtio</interface>
        <linked>true</linked>
        <plugged>true</plugged>
        <mac address="00:1a:4a:16:84:07"/>
    </nic>
    '''
#     print vmnicapi.createVmNic('test1', xml_vm_nic_info)
    
#     print vmnicapi.getVmNicInfo('test1', 'nic1')
#     print vmnicapi.getVmNicIdByName('test1', 'nic1')
#     print vmnicapi.getVmNicsList('test1')
    
    xml_export_option = '''
    <action>
        <storage_domain>
            <name>data1</name>
        </storage_domain>
    </action>
    '''
#     print vmdiskapi.exportVmDisk('test1', xml_export_option, disk_alias='test1_Disk2')
    
    xml_move_info = '''
    <action>
        <storage_domain>
            <name>data</name>
        </storage_domain>
    </action>
    '''
#     print vmdiskapi.moveVmDisk('test1', xml_move_info, disk_alias='test1_Disk2')
    
#     print vmdiskapi.activateVmDisk('test1', disk_id='a1a4b4aa-8239-4ab8-a14b-d0d31a73561c')
#     print vmdiskapi.deactivateVmDisk('test1', disk_id='a1a4b4aa-8239-4ab8-a14b-d0d31a73561c')
    
#     disk_id = 'a1a4b4aa-8239-4ab8-a14b-d0d31a73561c'
#     print vmdiskapi.attachDiskToVm('test1', disk_id)
#     print vmdiskapi.detachDiskFromVm('test1', disk_id)
    
#     print vmdiskapi.statisticsVmDisk(vm_name='test1', disk_alias='test1_Disk1')
    
    xml_del_disk_option = '''
    <action>
        <detach>false</detach>
    </action>
    '''
#     print vmdiskapi.delVmDisk('test1', disk_alias='test1_Disk2', xml_del_disk_option=xml_del_disk_option)
    
    xml_update_disk_info = '''
    <disk>
        <name>Disk22222222</name>
        <description>hahahahaah</description>
        <shareable>true</shareable>
    </disk>
    '''
#     print vmdiskapi.updateVmDisk('test1', 'test1_Disk2', xml_update_disk_info)
    
    xml_disk_info = '''
    <disk>
        <storage_domains>
            <storage_domain>
                <name>data</name>
            </storage_domain>
        </storage_domains>
        <alias>test1_Disk2</alias>
        <size>1073741824</size>
        <type></type>
        <interface>virtio</interface>
        <sparse>false</sparse>
        <format>raw</format>
        <bootable>false</bootable>
        <shareable>false</shareable>
        <wipe_after_delete>false</wipe_after_delete>
    </disk>
    '''
#     xml_disk_info_1 = '''<disk id="a1a4b4aa-8239-4ab8-a14b-d0d31a73561c"/>'''
#     print vmdiskapi.createVmDisk('test1', xml_disk_info_1)
    
#     print vmdiskapi.getVmDiskIdByName('test1', 'aaatest1_Disk2')
#     print xmltodict.unparse(vmdiskapi.getVmDisksList('test1')['result'], pretty=True)
    
    xml_export_vm_option = '''
    <action>
        <storage_domain>
            <name>export</name>
        </storage_domain>
        <async>false</async>
        <exclusive>true</exclusive>
        <discard_snapshots>true</discard_snapshots>
    </action>
    '''
#     print vmapi.exportVm('test1', xml_export_vm_option)
    
#     print vmapi.cancelMigration('haproxy-qcow2')
    
    xml_migrate_option = '''
        <action/>
    '''
#     print vmapi.migrateVm('haproxy-qcow2', xml_migrate_option)
    
#     print vmapi.suspendVm('haproxy-qcow2')
#     print vmapi.shutdownVm('VM2')
#     print vmapi.stopVm('VM2')
    
    xml_start_vm_option = '''
        <action>
            <pause>false</pause>
            <vm>
                <stateless>true</stateless>
            </vm>
            <async>false</async>
        </action>
    '''
#     print vmapi.startVm('VM2', xml_start_vm_option)
    
    xml_del_vm_option = '''
    <action>
        <vm>
            <disks>
                <detach_only>false</detach_only>
            </disks>
        </vm>
        <force>true</force>
    </action>
    '''
#     print vmapi.delVm('VM2', xml_del_vm_option)
    
    xml_vm_update_info = '''
    <vm>
        <memory>1073741824</memory>
    </vm>
    '''
#     print vmapi.updateVm('VM2', xml_vm_update_info)
    
    xml_vm_info = '''
    <vm>
        <name>vm2</name>
        <description>Virtual Machine 2</description>
        <type>server</type>
        <memory>536870912</memory>
        <cluster>
            <name>Cluster-ISCSI</name>
        </cluster>
        <template>
            <name>Blank</name>
        </template>
        <cpu>
            <topology sockets="2" cores="1"/>
        </cpu>
        <os>
            <boot dev="cdrom"/>
            <boot dev="hd"/>
        </os>
    </vm>
    '''
#     print vmapi.createVm(xml_vm_info)
#     print vmapi.getVmInfo('VM11')
#     print vmapi.getVmIdByName('VM11')
#     print vmapi.searchVmByName('VM11')
#     print vmapi.getVmInfo('VM22')
#     print vmapi.getVmStatus('VM2')
    