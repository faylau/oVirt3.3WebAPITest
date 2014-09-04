#coding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/08/29      初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import xmltodict

from BaseAPIs import BaseAPIs
from StorageDomainAPIs import StorageDomainAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

class DataCenterAPIs(BaseAPIs):
    '''
    @summary: 提供数据中心各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义datacenter相关API的base_url，如'https://10.1.167.2/api/datacenters'
        '''
        self.base_url = '%s/datacenters' % WebBaseApiUrl
        
    def searchDataCenterByName(self, dc_name):
        '''
        @summary: 根据数据中心名称查找（调用datacenters接口中的search方法）
        @param dc_name: 数据中心名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：搜索到的所有数据中心（dict格式）。
        '''
        return self.searchObject('datacenters', dc_name)
        
        
    def getDataCenterIdByName(self, dc_name):
        '''
        @summary: 根据数据中心名称返回其id
        @param dc_name: 数据中心名称
        @return: 数据中心id
        '''
        dc_list = self.searchDataCenterByName(dc_name)
        return dc_list['result']['data_centers']['data_center']['@id']
    
    def getDataCenterNameById(self, dc_id):
        '''
        @summary: 根据数据中心的id返回其名称
        @param dc_id: 数据中心id
        @return: 数据中心名称
        @todo: 无需实现该功能，后续如果有需要再实现。
        '''
        pass
    
    def getDataCentersList(self):
        '''
        @summary: 获取全部数据中心列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = "GET"
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getDataCenterInfo(self, dc_name):
        '''
        @summary: 根据数据中心名称，获取数据中心详细信息
        @param dc_name: 数据中心名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的数据中心信息
        '''
        dc_id = self.getDataCenterIdByName(dc_name)
        api_url = '%s/%s' % (self.base_url, dc_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getDataCenterStatus(self, dc_name):
        '''
        @summary: 查看数据中心状态
        @param dc_name: 数据中心名称
        @return: 数据中心状态
        '''
        return self.getDataCenterInfo(dc_name)['result']['data_center']['status']['state']
    
    def createDataCenter(self, dc_info):
        '''
        @summary: 创建数据中心
        @param dc_info: XML形式的数据中心信息，调用接口时需要传递此xml数据
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=dc_info)
#         print r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def updateDataCenter(self, dc_name, update_info):
        '''
        @summary: 编辑数据中心
        @param dc_name: 数据中心名称
        @param update_info: 更新的内容
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        dc_id = self.getDataCenterIdByName(dc_name)
        api_url = '%s/%s' % (self.base_url, dc_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=update_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def delDataCenter(self, dc_name, data=None):
        '''
        @summary: 根据数据中心名称删除指定的数据中心（包括普通删除、强制删除等方式，由data中的参数设置确定）
        @param dc_name: 数据中心名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        dc_id = self.getDataCenterIdByName(dc_name)
        print dc_id
        api_url = '%s/%s' % (self.base_url, dc_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=data)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getDCStorageDomainsList(self, dc_name):
        '''
        @summary: 获取指定数据中心的存储域列表
        @param dc_name: 数据中心名称
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容。
        '''
        api_url = '%s/%s/storagedomains' % (self.base_url, self.getDataCenterIdByName(dc_name))
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}        
    
    def getDCStorageDomainInfo(self, dc_name, sd_name):
        '''
        @summary: 获取数据中心的存储域信息
        @param dc_name: 数据中心名称
        @param sd_name: 存储域名称
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容。
        '''
        # 调用StorageDomainAPIs模块中的getStorageDomainIdByName()方法获得存储域id
        sdapi = StorageDomainAPIs()
        sd_id = sdapi.getStorageDomainIdByName(sd_name)
        dc_id = self.getDataCenterIdByName(dc_name)
        api_url = '%s/%s/storagedomains/%s' % (self.base_url, dc_id, sd_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def attachStorageDomainToDC(self, dc_name, sd_name=None, data=None):
        '''
        @summary: 将存储域附加到数据中心
        @param dc_name: 数据中心名称
        @param sd_name: 存储域名称（可选参数，若不指定，则必须按规则在data中指定相应参数）
        @param data: 存储域的xml数据（可选参数，若提供了sd_name，则不需要提供该参数；若未提供sd_name，则需提供相应的xml字符串）
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容。
        '''
        api_url = '%s/%s/storagedomains' % (self.base_url, self.getDataCenterIdByName(dc_name))
        method = 'POST'
        if sd_name:
            data = '''<storage_domain><name>%s</name></storage_domain>''' % sd_name
            r = HttpClient.sendRequest(method=method, api_url=api_url, data=data)
        elif data:
            r = HttpClient.sendRequest(method=method, api_url=api_url, data=data)
        else:
            raise Exception(u'至少需要提供storage_name或xml数据来完成分离操作。')
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def detachStorageDomainFromDC(self, dc_name, sd_name, data=None):
        '''
        @summary: 将维护状态的存储从数据中心分离
        @param dc_name: 数据中心名称
        @param sd_name: 存储名称
        @param data: 可选参数，如<action><async>true</async></action>
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容。
        '''
        sdapi = StorageDomainAPIs()
        dc_id = self.getDataCenterIdByName(dc_name)
        sd_id = sdapi.getStorageDomainIdByName(sd_name)
        method = 'DELETE'
        api_url = '%s/%s/storagedomains/%s' % (self.base_url, dc_id, sd_id)
#         data = '''<action><async>true</async></action>'''
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def activeDCStorageDomain(self, dc_name, sd_name):
        '''
        @summary: 激活数据中心中的存储域
        @param dc_name: 数据中心名称
        @param sd_name: 存储域名称
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容。
        '''
        dc_id = self.getDataCenterIdByName(dc_name)
        sd_id = StorageDomainAPIs().getStorageDomainIdByName(sd_name)
        api_url = '%s/%s/storagedomains/%s/activate' % (self.base_url, dc_id, sd_id)
        method = 'POST'
        data = '''<action/>'''
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=data)
#         print r.status_code, r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def deactiveDCStorageDomain(self, dc_name, sd_name):
        '''
        @summary: 取消激活数据中心中的存储域
        @param dc_name: 数据中心名称
        @param sd_name: 存储域名称
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容。
        '''
        dc_id = self.getDataCenterIdByName(dc_name)
        sd_id = StorageDomainAPIs().getStorageDomainIdByName(sd_name)
        api_url = '%s/%s/storagedomains/%s/deactivate' % (self.base_url, dc_id, sd_id)
        method = 'POST'
        data = '<action/>'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=data)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getDCClustersList(self, dc_name):
        '''
        @summary: 获取数据中心的集群列表
        @param dc_name: 数据中心名称
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容（数据中心的集群列表）。
        '''
        dc_id = self.getDataCenterIdByName(dc_name)
        api_url = '%s/%s/clusters' % (self.base_url, dc_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getDCQuotasList(self, dc_name):
        '''
        @summary: 获取数据中心的Quota列表
        @param dc_name: 数据中心名称
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容（数据中心的Quota列表）；
        @todo: 
        '''
        pass
    
    def getDCQuotaInfo(self, dc_name, quota_id):
        '''
        @todo: 
        '''
        pass
    
    def createDCQuota(self, dc_name):
        '''
        @summary: 创建数据中心Quota
        @param dc_name: 数据中心名称
        @param quota_name: Quota名称
        @todo: 
        '''
        pass
        
    

if __name__ == "__main__":
    dcapi = DataCenterAPIs()
    data = '''
    <data_center>
        <name>NewDatacenter</name>
        <storage_type>nfs</storage_type>
        <version minor="1" major="3"/>
    </data_center>
    '''
    dcapi.createDataCenter(data)
#     print dcapi.getDCClustersList('Default')
#     print dcapi.deactiveDCStorageDomain('Default', 'data1')
#     print dcapi.activeDCStorageDomain('Default', 'data1')
#     print dcapi.detachStorageDomainFromDC('Default', 'data1')
#     print dcapi.attachStorageDomainToDC('Default', 'data1')
#     print dcapi.getDataCenterStatus('DC-ISCSI')
#     data = '''<storage_domain><name>data1</name></storage_domain>'''
#     print dcapi.attachStorageDomainToDC('Default', data=data)
#     d = dcapi.getDCStorageDomainInfo('Default', 'data1')
#     print dcapi.getDCStorageDomainsList('Default')
#     print dcapi.getDataCenterIdByName('DC-ISCSI')
#     data = '''
#     <action>
#         <force>true</force>
#         <async>false</async>
#     </action>
#     '''
#     print dcapi.delDataCenter('ABC', data=data)

    
    