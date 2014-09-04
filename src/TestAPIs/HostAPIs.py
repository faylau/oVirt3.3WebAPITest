#encoding:utf-8

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

class HostAPIs(BaseAPIs):
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
        
        

        
    

if __name__ == "__main__":
    pass

    
    