#encoding:utf-8
from TestAPIs.DataCenterAPIs import DataCenterAPIs

__authors__ = ['']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/01      初始版
#---------------------------------------------------------------------------------
'''

import xmltodict
from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

class NetworkAPIs(BaseAPIs):
    '''
    @summary: 提供网络各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义网相关API的base_url，如'https://10.1.167.2/api/networks'
        '''
        self.base_url = '%s/networks' % WebBaseApiUrl
    
    def searchNetworkByName(self, nw_name):
        '''
        @summary: 根据网络名称查找
        @param nw_name: 网络
        '''
        return self.searchObject('networks', nw_name)
    
    def getNetworkIdByName(self, nw_name,dc_name):
        '''
        @summary: 根据网络名称返回其ID
        @param nw_name: 网络名称
        @param dc_name: 数据中心名称（每个数据中心内网络名称是唯一的）
        @return: 网络id
        '''
        if self.searchNetworkByName(nw_name)['result']['networks']:
            nw_list = self.searchNetworkByName(nw_name)['result']['networks']['network']
            dc_id = DataCenterAPIs().getDataCenterIdByName(dc_name)
            if isinstance(nw_list, dict):
                return nw_list['@id']
            else:
                for network in nw_list:
                    if dc_id == network['data_center']['@id']:
                        return network['@id']
        else:
            return None           
        
                
    def getNetworksList(self):
        '''
        @summary: 获取全部网络列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = "GET"
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        print r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
    
    def getNetworkInfo(self, nw_name=None, nw_id=None,dc_name=None):
        '''
        @summary: 根据网络名称或网络id，获取网络详细信息
        @param nw_name: 网络名称
        @param nw_id: 网络id
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的数据中心信息
        '''
        if not nw_id and nw_name and dc_name:
            nw_id = self.getNetworkIdByName(nw_name,dc_name)
        if nw_id:
            api_url = '%s/%s' % (self.base_url, nw_id)
            method = 'GET'
            r = HttpClient.sendRequest(method=method, api_url=api_url)
            return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        else:
            print '不存在该网络'
            
    def createNetwork(self, nw_info):
        '''
        @summary: 创建网络
        @param nw_info: XML形式的集群信息，调用接口时需要传递此xml数据
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=nw_info)
        print r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}      
    
    def updateNetwork(self, nw_name, dc_name,update_info):
        '''
        @summary: 编辑某数据中心的网络
        @param nw_name: 网络名称
        @param dc_name: 数据中心名称
        @param update_info: 更新的内容
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        nw_id = self.getNetworkIdByName(nw_name, dc_name)
        if nw_id:
            api_url = '%s/%s' % (self.base_url, nw_id)
            method = 'PUT'
            r = HttpClient.sendRequest(method=method, api_url=api_url, data=update_info)
            return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
        else:
            return None
        
    def delNetwork(self, nw_name, dc_name,async=None):
        '''
        @summary: 删除某数据中心的网络
        @param nw_name: 网络名称
        @param dc_name: 数据中心名称
        @param async: 是否异步
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        nw_id = self.getNetworkIdByName(nw_name, dc_name)
        if nw_id:
            api_url = '%s/%s' % (self.base_url, nw_id)
            method = 'DELETE'
            r = HttpClient.sendRequest(method=method, api_url=api_url, data=async)
            return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        else:
            return None

class NetworkProfilesAPIs(NetworkAPIs):
    '''
    @summary: 提供网络配置集基本操作
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义网相关API的base_url，如'https://10.1.167.2/api/networks'
        '''
        self.base_url = '%s/networks' % WebBaseApiUrl
         
        
    def getNetworkProfileList(self,nw_id):
        '''
        @summary: 获取网络的配置集列表
        @param nw_id: 网络id
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        if nw_id:
            api_url = '%s/%s/vnicprofiles' % (self.base_url, nw_id)
            method = 'GET'
            r = HttpClient.sendRequest(method=method, api_url=api_url)
            return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        else:
            return None
    
    def getProfileIdbyName(self,nw_id,profile_name):
        '''
        @summary: 通过配置集名称获取其id
        @param nw_id: 网络id
        @param profile_name:配置集名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        profile_list =  self.getNetworkProfileList(nw_id)['result']['vnic_profiles']['vnic_profile']
        if isinstance(profile_list, dict): 
            if profile_list['name'] == profile_name:
                return profile_list['@id']  
            else:
                return None
        else:
            for profile in profile_list:
                if profile['name'] == profile_name:
                    return profile['@id']
        
    def getNetworkProfileInfo(self,nw_name,profile_name,dc_name):
        '''
        @summary: 删除某数据中心的网络
        @param nw_name: 网络名称
        @param dc_name: 数据中心名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        nw_id = self.getNetworkIdByName(nw_name, dc_name)
        if nw_id:
            profile_id = self.getProfileIdbyName(nw_id, profile_name)
            api_url = '%s/%s/vnicprofiles/%s' % (self.base_url, nw_id,profile_id)
            method = 'GET'
            r = HttpClient.sendRequest(method=method, api_url=api_url)
            return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        else:
            return None
            
if __name__=='__main__':
    nwapi = NetworkAPIs()
    #print nwapi.searchNetworkByName('network111')
    nw_id = nwapi.getNetworkIdByName('network11', 'Default')
    #print nwapi.getNetworkIdByName('aaa', 'Default')
    #print nwapi.getNetworksList()
    #print nwapi.getNetworkInfo(nw_id='8fa8a1db-65bc-43e2-bfba-1ac523b556bb')
    #print nwapi.getNetworkInfo(nw_name='network11', dc_name='Default')
    nw_info='''
    <network>
    <name>network1</name>
    <description>lalala</description>
    <data_center>
        <name>Default</name>
    </data_center>
    <vlan id="2"/>
    <ip address="192.168.0.1" netmask="255.255.255.0" gateway="192.168.0.254"/>
    <stp>false</stp>
    <mtu>1500</mtu>
    <display>true</display>
    <usages>
        <usage>vm</usage>
    </usages>
</network>
    '''
    #nwapi.createNetwork(nw_info)
    #print nwapi.updateNetwork('aaaa', 'Default', nw_info)
    #print nwapi.delNetwork('ovirtmgmt', 'Default')
    nwprofile=NetworkProfilesAPIs()
    #print nwprofile.getNetworkProfileInfo('aaa', 'aaa', 'Default')
    #print nwprofile.getNetworkProfileList(nw_id)
    print nwprofile.getProfileIdbyName(nw_id, 'a')
            
            

        


    
    
    