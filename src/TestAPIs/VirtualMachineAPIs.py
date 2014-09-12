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
        r.raise_for_status()    # 若出现无效HTTP响应时，抛出HTTPError异常
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
        (1) 通常情况下，name/template/cluster必须提供:
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
            </os>
            <highly_available>
                <enabled>true</enabled>
                <priority>50</priority>
            </highly_available>
        </vm>
        @return: 
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_vm_info)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    

    
if __name__=='__main__':
    vmapi = VirtualMachineAPIs()
    
#     print vmapi.getVmInfo('VM11')
#     print vmapi.getVmIdByName('VM11')
#     print vmapi.searchVmByName('VM11')
#     print vmapi.getVmInfo('VM22')
#     print vmapi.getVmStatus('VM2')

    
    