#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/01      初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import xmltodict
from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

class StorageDomainAPIs(BaseAPIs):
    '''
    @summary: 提供存储域各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义storage domain相关API的base_url，如'https://10.1.167.2/api/storagedomains'
        '''
        self.base_url = '%s/storagedomains' % WebBaseApiUrl
    
    def searchStorageDomainByName(self, sd_name):
        '''
        @summary: 根据存储域名称查找（调用storage_domain接口中的search方法）
        @param dc_name: 数据中心名称
        '''
        return self.searchObject('storagedomains', sd_name)
    
    def getStorageDomainIdByName(self, sd_name):
        '''
        @summary: 根据存储域名称返回其ID
        @param sd_name: 存储域名称
        @return: 存储域id
        '''
        sd_list = self.searchStorageDomainByName(sd_name)
        return sd_list['result']['storage_domains']['storage_domain']['@id']

        

if __name__ == "__main__":
    pass
    
    
    