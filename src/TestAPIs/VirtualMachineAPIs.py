#coding:utf-8

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
        @summary: 根据VM名称查找
        @param vm_name: 集群名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：搜索到的VM（dict格式）。
        '''
        return self.searchObject('vms', vm_name)
    
    def getVmIdByName(self, vm_name):
        '''
        @summary: 根据VM名称返回其id
        @param vm_name: VM名称
        @return: VM的id
        '''
        vm_list = self.searchVmByName(vm_name)
        return vm_list['result']['vms']['vm']['@id']
    
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
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
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
        '''
        if not vm_id and vm_name:
            vm_id = self.getVmIdByName(vm_name)
        api_url = '%s/%s' % (self.base_url, vm_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    

    
if __name__=='__main__':
    pass

    
    