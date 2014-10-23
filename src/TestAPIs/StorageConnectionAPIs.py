#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/20      初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import xmltodict

from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

class StorageConnectionAPIs(BaseAPIs):
    '''
    @summary: 提供存储域连接各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义storage connection相关API的base_url，如'https://10.1.167.2/api/storageconnections'
        '''
        self.base_url = '%s/storageconnections' % WebBaseApiUrl
        
    def getStorageConnectionInfo(self, sc_id):
        '''
        @summary: 获得Storage Connection的信息
        '''
        api_url = '%s/%s' % (self.base_url, sc_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getStorageConnectionsList(self):
        '''
        @summary: 获得全部storage connection的列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def createStorageConnection(self, xml_sd_info):
        '''
        @summary: 创建存储域（游离状态，未附加到任何数据中心）
        '''
        pass
    
    def updateStorageConnection(self, sd_name, xml_update_info):
        '''
        @summary: 更新存储域信息
        '''
        pass
    
    def delStorageConnection(self, sc_id, xml_del_option):
        '''
        @summary: 删除存储域（包括删除、销毁）
        @param xml_del_option: 
            <host>
                <name>Host_Name</name>
            </host>
        '''
        api_url = '%s/%s' % (self.base_url, sc_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_del_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)} 
    


if __name__ == "__main__":
    sc_api = StorageConnectionAPIs()
    
    xml_del_option = '''
    <host>
        <name>node-ITC04-1</name>
    </host>
    '''
    sc_api.delStorageConnection('638d5125-60f5-48cf-90f6-9f0ac69636e3', xml_del_option)
    
    
    