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
from TestAPIs.NetworkAPIs import NetworkProfilesAPIs
'''

import xmltodict

from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient
from NetworkAPIs import NetworkAPIs,NetworkProfilesAPIs



class ProfilesAPIs(BaseAPIs):
    '''
    @summary: 提供网络配置集各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义网相关API的base_url，如'https://10.1.167.2/api/networks'
        '''
        self.base_url = '%s/vnicprofiles' % WebBaseApiUrl
        
    
    
    def getProfileIdByName(self, profile_name,nw_id):
        '''
        @summary: 根据配置集名称获得其id（同一网络内配置集名称唯一）
        @param profile_name: 配置集名称
        @param nw_id:网络id
        @return: 配置集id
        if self.searchProfileByName(profile_name)['result']['vnic_profiles']:
            profile_list = self.searchProfileByName(profile_name)['result']['vnic_profiles']['vnic_profile']
            if isinstance(profile_list, dict):
                return profile_list['@id']
                print 'aaa'
            else:
                print profile_list
                #print xmltodict.unparse(profile_list,pretty=True)
                for profile in profile_list:
                    if nw_id == profile['network']['@id']:
                        return profile['@id']
        else:
            return None           
        
        '''
        nwproapi = NetworkProfilesAPIs()
        profile_list = nwproapi.getNetworkProfileList(nw_id)['result']['vnic_profiles']['vnic_profile']
        if isinstance(profile_list, dict):
            if profile_list['name'] == profile_name:
                return profile_list['@id']
        else:
            for profile in profile_list:
                if profile['name'] == profile_name:
                    return profile['@id']
                
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
        @summary: 根据配置集名称或id获取其详细信息，若是提供配置集名称则需要提供网络id
        @param profile_name: 配置集名称
        @param profile_id: 配置集id
        @param nw_id:网络id 
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的数据中心信息
        '''
        if not profile_id and profile_name and nw_id:
            profile_id = self.getProfileIdByName(profile_name, nw_id)
            print profile_id
        api_url = '%s/%s' % (self.base_url, profile_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def isExist(self, profile_name, nw_id):
        '''
        @summary: 查看网络中是否存在某配置集
        @param profile_name: 配置集名称
        @param nw_id:网络id 
        @return: True或 False
        '''
        r =  ProfilesAPIs().getProfileInfo(profile_name=profile_name, nw_id=nw_id)
        if r:
            return True
        else:
            return False
            
    def createProfiles(self, profile_info,nw_id=None):
        '''
        @summary: 创建指定网络的配置集
        @param profile_info: XML文件
                    输入说明：
        1）配置集名称只能由数字、字母、-、_组成
        2）名称和网络id是必须的，网络名称无效
        @param nw_id:指定网络id
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        @note: 有两种使用情况
        1）nw_id可以通过外部传参，此时xml文件中network id为变量
        <vnic_profile>
            <name>abc#</name>
            <description>shelled</description>
            <network id="%s"/>
            <port_mirroring>false</port_mirroring>
        </vnic_profile>
        2）nw_id为空，此时xml文件中需为network id赋值
        <vnic_profile>
            <name>abc#</name>
            <description>shelled</description>
            <network id="字符串"/>
            <port_mirroring>false</port_mirroring>
        </vnic_profile>
        '''
        api_url = self.base_url
        method = 'POST'
        if nw_id:
            r = HttpClient.sendRequest(method=method, api_url=api_url, data=(profile_info %nw_id))
        else:
            r = HttpClient.sendRequest(method=method, api_url=api_url, data=profile_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}      
    
    def updateProfile(self, profile_name, nw_id,update_info):
        '''
        @summary: 编辑某网络配置集信息
        @param profile_name: 配置集名称
        @param nw_id: 网络id
        @param update_info: 更新的内容，xml文件
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        profile_id = self.getProfileIdByName(profile_name, nw_id)
        api_url = '%s/%s' % (self.base_url, profile_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=update_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
        
        
    def delProfile(self, profile_name, nw_id,async=None):
        '''
        @summary: 删除某网络的配置集
        @param profile_name: 配置集名称
        @param nx_id: 网络id
        @param async: 是否异步，xml文件
        <action>
            <async>false</async>
        </action>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        profile_id = self.getProfileIdByName(profile_name, nw_id)
        api_url = '%s/%s' % (self.base_url, profile_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=async)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        


            
if __name__=='__main__':
    profileapi = ProfilesAPIs()
    #print profileapi.getProfileIdByName('aaa', 'e98b6c1f-4021-4875-b6a8-691c923d0d30')
    #print profileapi.getProfilesList()
    #print profileapi.getProfileIdByName('sd', nw_id='76c060f3-4b0c-43e5-bba5-012d5e16b26')
    print profileapi.getProfileInfo('pp', nw_id='0b1de2ef-aa48-47f7-834c-8335ffa7d9a6')
    print profileapi.isExist('pp', nw_id='0b1de2ef-aa48-47f7-834c-8335ffa7d9a6')
    profile_info = '''
    <vnic_profile>
        <name>pp</name>
        <network id="0b1de2ef-aa48-47f7-834c-8335ffa7d9a6"/>
        <port_mirroring>false</port_mirroring>
    </vnic_profile>
    '''
    print profileapi.createProfiles(profile_info)
    #print profileapi.updateProfile('peanuts', 'e98b6c1f-4021-4875-b6a8-691c923d0d30',profile_info)
    #print xmltodict.unparse(profileapi.updateProfile('peanuts', 'e98b6c1f-4021-4875-b6a8-691c923d0d30',profile_info)['result'],pretty=True)
    #print xmltodict.unparse(profileapi.createProfiles(profile_info)['result'],pretty=True) 
    print profileapi.delProfile('aaa', 'e98b6c1f-4021-4875-b6a8-691c923d0d30')     
    '''
    'e98b6c1f-4021-4875-b6a8-691c923d0d30'
    <network id="%s"/>
    <network id="e98b6c1f-4021-4875-b6a8-691c923d0d30"/>
    '''      

        


    
    
    