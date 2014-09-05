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
        nw_list = self.searchNetworkByName(nw_name)['result']['networks']['network']
        dc_id = DataCenterAPIs().getDataCenterIdByName(dc_name)
        if len(nw_list)==1:
            return nw_list['@id']
        else:
            for network in nw_list:
                if dc_id == network['data_center']['@id']:
                    return network['@id']
                
            
if __name__=='__main__':
    nwapi = NetworkAPIs()
    #print nwapi.searchNetworkByName('network11')
    print nwapi.getNetworkIdByName('network11', 'Default')
            
            

        


    
    
    