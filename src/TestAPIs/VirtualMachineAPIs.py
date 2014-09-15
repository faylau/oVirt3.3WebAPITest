#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/10      初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import xmltodict

from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

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
        @summary: 创建虚拟机
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
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的操作结果。
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_vm_info)
        r.raise_for_status()
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
        @return: 
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
        @return: 
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
        @return: 
        '''
        vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s/cancelmigration' % (self.base_url, vm_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        print r.status_code, r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    
if __name__=='__main__':
    vmapi = VirtualMachineAPIs()
    
    print vmapi.cancelMigration('haproxy-qcow2')
    
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
                <detach_only>true</detach_only>
            </disks>
        </vm>
    </action>
    '''
#     print vmapi.delVm('vm2', xml_del_vm_option)
    
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
    