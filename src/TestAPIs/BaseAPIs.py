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
    
if __name__=='__main__':
    bapi = BaseAPIs()
    print bapi.searchObject('datacenters', 'Default')