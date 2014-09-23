#encoding:utf-8

import urllib
import xmltodict

from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

class BaseAPIs(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        pass
    
    def searchObject(self, obj_type, search_str):
        '''
        @summary: 根据字符串对指定目标进行搜索
        @param obj_type: 要查找的目标类型，如datacenters、hosts等
        @param search_str: 要搜索的字符串，如数据中心名称，状态等
        @return: 字典，（1）返回状态码；（2）Dict类型搜索结果
        '''
        url = '%s/%s?search=name%s%s' % (WebBaseApiUrl, obj_type, urllib.quote('='), search_str)
        method = 'GET'
        r = HttpClient.sendRequest(method, url)
        #r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getProductInfo(self):
        '''
        @summary: 获取虚拟化产品信息（包括name、vendor、version、full_version）
        @return: 
        '''
        api_url = WebBaseApiUrl
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code==200:
            return xmltodict.parse(r.text)['api']['product_info']
        else:
            print 'Error occurs. Details: %s, %s' % (r.status_code, r.text)
            return None
        
    def getVmsQuantity(self):
        '''
        @summary: 获取当前全部VM的数量信息（VM总数、Active状态VM数）
        @return: dict['total']，dict['active']
        '''
        api_url = WebBaseApiUrl
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code==200:
            return xmltodict.parse(r.text)['api']['summary']['vms']
        else:
            print 'Error occurs. Details: %s, %s' % (r.status_code, r.text)
            return None
        
    def getHostsQuantity(self):
        '''
        @summary: 获取当前全部Host的数量信息（总数、Active数）
        @return: dict['total']，dict['active']
        '''
        api_url = WebBaseApiUrl
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code==200:
            return xmltodict.parse(r.text)['api']['summary']['hosts']
        else:
            print 'Error occurs. Details: %s, %s' % (r.status_code, r.text)
            return None
        
    def getUsersQuantity(self):
        '''
        @summary: 获取当前全部登录用户的数量信息（总数、Active数）
        @return: dict['total']，dict['active']
        '''
        api_url = WebBaseApiUrl
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code==200:
            return xmltodict.parse(r.text)['api']['summary']['users']
        else:
            print 'Error occurs. Details: %s, %s' % (r.status_code, r.text)
            return None
        
    def getStorageDomainsQuantity(self):
        '''
        @summary: 获取当前全部存储域的数量信息（总数、Active数）
        @return: dict['total']，dict['active']
        '''
        api_url = WebBaseApiUrl
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code==200:
            return xmltodict.parse(r.text)['api']['summary']['storage_domains']
        else:
            print 'Error occurs. Details: %s, %s' % (r.status_code, r.text)
            return None
        
        
    
if __name__=='__main__':
    bapi = BaseAPIs()
#     print bapi.searchObject('datacenters', 'Default')
#     print bapi.getProductInfo()
#     print bapi.getVmsQuantity()
#     print bapi.getHostsQuantity()
#     print bapi.getUsersQuantity()
    print bapi.getStorageDomainsQuantity()