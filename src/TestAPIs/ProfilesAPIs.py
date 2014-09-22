#encoding:utf-8
__authors__ = ['keke.wei@cs2c.com.cn']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/10     初始版                            wei keke
#---------------------------------------------------------------------------------
'''

import xmltodict

from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

class ProfilesAPIs(BaseAPIs):
    '''
    @summary: 提供网络配置集各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义网相关API的base_url，如'https://10.1.167.2/api/networks'
        '''
        self.base_url = '%s/vnicprofiles' % WebBaseApiUrl
        
    def searchProfileByName(self, profile_name):
        '''
        @summary: 根据配置集名称查找
        @param profile_name: 配置集名称
        '''
        return self.searchObject('vnicprofiles', profile_name)
    
    
    def getProfileIdByName(self, profile_name,nw_id):
        '''
        @summary: 根据配置集名称获得其id（同一网络内配置集名称唯一）
        @param profile_name: 配置集名称
        @param nw_id:网络id
        @return: 配置集id
        '''
        if self.searchProfileByName(profile_name)['result']['vnic_profiles']:
            profile_list = self.searchProfileByName(profile_name)['result']['vnic_profiles']['vnic_profile']
            if isinstance(profile_list, dict):
                return profile_list['@id']
            else:
                for profile in profile_list:
                    if nw_id == profile['network']['@id']:
                        return profile['@id']
        else:
            return None           
        
                
    def getProfilesList(self):
        '''
        @summary: 获取全部配置集列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = "GET"
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
    
    def getProfileInfo(self, profile_name=None,profile_id=None,nw_id=None):
        '''
        @summary: 根据配置集名称或id获取其详细信息
        @param profile_name: 配置集名称
        @param profile_id: 配置集id
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的数据中心信息
        '''
        if not profile_id and profile_name and nw_id:
            profile_id = self.getProfileIdByName(profile_name, nw_id)
        api_url = '%s/%s' % (self.base_url, profile_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
            
    def createProfiles(self, profile_info):
        '''
        @summary: 创建网络配置集
        @param nw_info: XML形式的集群信息，调用接口时需要传递此xml数据
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=profile_info)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}      
    
    def updateProfile(self, profile_name, nw_id,update_info):
        '''
        @summary: 编辑某网络配置集信息
        @param profile_name: 配置集名称
        @param nw_id: 网络id
        @param update_info: 更新的内容
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        profile_id = self.getProfileIdByName(profile_name, nw_id)
        api_url = '%s/%s' % (self.base_url, profile_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=update_info)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
        
        
    def delProfile(self, profile_name, nw_id,async=None):
        '''
        @summary: 删除某网络的配置集
        @param profile_name: 配置集名称
        @param nx_id: 网络id
        @param async: 是否异步
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        profile_id = self.getProfileIdByName(profile_name, nw_id)
        api_url = '%s/%s' % (self.base_url, profile_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=async)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        


            
if __name__=='__main__':
    profileapi = ProfilesAPIs()
    print profileapi.getProfilesList()
    print profileapi.getProfileIdByName('sd', nw_id='76c060f3-4b0c-43e5-bba5-012d5e16b26')
    print profileapi.getProfileInfo('sd', nw_id='76c060f3-4b0c-43e5-bba5-012d5e16b26')
    print profileapi.getProfileInfo(nw_id='76c060f3-4b0c-43e5-bba5-012d5e16b26') 
    profile_info = '''
    <vnic_profile>
    <name>peanuts</name>
    <description>shelled</description>
    <network id="76c060f3-4b0c-43e5-bba5-012d5e16b26e"/>
    <port_mirroring>false</port_mirroring>
    </vnic_profile>
    '''
    print profileapi.createProfiles(profile_info)  
    print profileapi.delProfile('peanuts', '76c060f3-4b0c-43e5-bba5-012d5e16b26e')     
            

        


    
    
    