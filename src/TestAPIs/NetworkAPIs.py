#encoding:utf-8


__authors__ = ['keke.wei@cs2c.com.cn']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/03      初始版                                                                     wei keke
#---------------------------------------------------------------------------------
from __builtin__ import False
'''
from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient
from TestAPIs.DataCenterAPIs import DataCenterAPIs
from Utils.PrintLog import LogPrint

import xmltodict

def smart_create_network(nw_info,nw_name,status_code=201):
    nw_api = NetworkAPIs()
    r = nw_api.createNetwork(nw_info)
    if r['status_code'] == status_code:
        LogPrint().info("Pre-Test:Create network '%s'success."%nw_name)
        return True
    else:
        LogPrint().error("Pre-Test:Create network '%s' fail."%nw_name)
        return False

def smart_delete_network(nw_name,dc_name,status_code=200):

    nw_api = NetworkAPIs()
    try:
        print nw_api.getNetworkInfo(nw_name=nw_name,dc_name=dc_name)
        r = nw_api.delNetwork(nw_name,dc_name)
        if r ['status_code'] == status_code:
            LogPrint().info("Post-Test:Delete network '%s'success."%nw_name)
            return True
        else:
            LogPrint().error("Post-Test:Delete network '%s' fail."%nw_name)
            return False
    except:
        LogPrint().info("Post-Test:network '%s' is not exist"%nw_name)
        return True

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
    
    def isNetworkExist(self,nw_name,dc_name):
        '''
        @summary: 检查网络是否在数据中心内存在
        @param nw_name:网络名称
        @param dc_name:数据中心名称
        @return: True or False  
        ''' 
        nw_api = NetworkAPIs()
        dc_api = DataCenterAPIs()
        
        if not nw_api.searchNetworkByName(nw_name)['result']['networks']:
            return False
        if not dc_api.searchDataCenterByName(dc_name)['result']['data_centers']:
            return False
        nw_list = nw_api.searchNetworkByName(nw_name)['result']['networks']['network']
        if isinstance(nw_list, dict):
            if dc_api.getDataCenterNameById(nw_list['data_center']['@id'])==dc_name:
                return True
            else:
                return False
        else:
            self.flag=False
            for nw in nw_list:
                dc_id = nw['data_center']['@id']
                dc_name = dc_api.getDataCenterNameById(dc_id)
                if dc_name == dc_name:
                    self.flag=True
            return self.flag
        
            
            
        
                
    def getNetworksList(self):
        '''
        @summary: 获取全部网络列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = "GET"
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
    
    def getNetworkInfo(self, nw_name=None, nw_id=None,dc_name=None):
        '''
        @summary: 根据网络名称或网络id，获取网络详细信息;若提供网络名称则需要提供数据中心名称
        @param nw_name: 网络名称
        @param nw_id: 网络id
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的数据中心信息
        '''
        if not nw_id and nw_name and dc_name:
            nw_id = self.getNetworkIdByName(nw_name,dc_name)
        api_url = '%s/%s' % (self.base_url, nw_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
            
    def createNetwork(self, nw_info):
        '''
        @summary: 创建网络
        @param nw_info: XML形式的集群信息，调用接口时需要传递此xml数据
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=nw_info)
        #r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}      
    
    def updateNetwork(self, nw_name, dc_name,update_info):
        '''
        @summary: 编辑某数据中心的网络
        @param nw_name: 网络名称
        @param dc_name: 数据中心名称
        @param update_info: 更新的内容，xml文件
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        nw_id = self.getNetworkIdByName(nw_name, dc_name)
        api_url = '%s/%s' % (self.base_url, nw_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=update_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
        
        
    def delNetwork(self, nw_name, dc_name,async=None):
        '''
        @summary: 删除某数据中心的网络
        @param nw_name: 网络名称
        @param dc_name: 数据中心名称
        @param async: 是否异步,XML文件
        <action>
            <async>false</async>
        </action>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        nw_id = self.getNetworkIdByName(nw_name, dc_name)
        if nw_id:
            api_url = '%s/%s' % (self.base_url, nw_id)
            method = 'DELETE'
            r = HttpClient.sendRequest(method=method, api_url=api_url, data=async)
        #r.raise_for_status()
            return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        

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
        api_url = '%s/%s/vnicprofiles' % (self.base_url, nw_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    
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
            return None
        
    def getNetworkProfileInfo(self,nw_id,profile_name):
        '''
        @summary: 获取网络配置集的信息
        @param nw_id: 网络id
        @param profile_name:配置集名称 
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        profile_id = self.getProfileIdbyName(nw_id, profile_name)
        api_url = '%s/%s/vnicprofiles/%s' % (self.base_url, nw_id,profile_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
if __name__=='__main__':
    nwapi = NetworkAPIs()
    print nwapi.isNetworkExist('test1', 'DC-ISCSI')
    print nwapi.searchNetworkByName('ovirtmgmt')['result']['networks']
    #print nwapi.getNetworkIdByName('aaa', 'Default')
    #print nwapi.getNetworksList()
    #print nwapi.getNetworkInfo(nw_id='8fa8a1db-65bc-43e2-bfba-1ac523b556bb')
    #print nwapi.getNetworkInfo(nw_name='network11', dc_name='Default')
    '''
    <name>aaa</name>
    <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>
    '''
    nw_info='''
    <network>
    <name>a3</name>
    <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>
    <vlan id = "2" />
</network>
    '''
    print xmltodict.unparse(nwapi.createNetwork(nw_info)['result'],pretty=True)
    print nwapi.updateNetwork('network123', 'Default', nw_info)
    #print nwapi.delNetwork('network1e1','Default')
    nwprofile=NetworkProfilesAPIs()
    #print nwprofile.getNetworkProfileInfo('aaa', 'aaa', 'Default')
    #print nwprofile.getNetworkProfileList(nw_id)
    #print nwprofile.getProfileIdbyName(nw_id, 'a')
            
    '''
    <name>aaa</name>
    <description>lalala</description>
        
    <ip address="192.168.0.1" netmask="255.255.255.0" gateway="192.168.0.254"/>
    <stp>false</stp>
    <mtu>1500</mtu>
    <display>true</display>
    <usages>
        <usage>vm</usage>
    </usages>
    '''        

        


    
    
    