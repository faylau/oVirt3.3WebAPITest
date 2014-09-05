#encoding:utf-8

__authors__ = ['"keke wei" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/04      初始版本                         wei keke
#---------------------------------------------------------------------------------
'''

import xmltodict

from BaseAPIs import BaseAPIs
from StorageDomainAPIs import StorageDomainAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

class ClusterAPIs(BaseAPIs):
    '''
    @summary: 提供集群各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义集群相关API的base_url，如'https://10.1.167.2/api/clusters'
        '''
        self.base_url = '%s/clusters' % WebBaseApiUrl
        
    def searchClusterByName(self, cluster_name):
        '''
        @summary: 根据集群名称查找
        @param cluster_name: 集群名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：搜索到的所有集群（dict格式）。
        '''
        return self.searchObject('clusters', cluster_name)
    
    def getClusterIdByName(self, cluster_name):
        '''
        @summary: 根据集群名称返回其id
        @param dc_name: 集群名称
        @return: 集群id
        '''
        cluster_list = self.searchClusterByName(cluster_name)
        return cluster_list['result']['clusters']['cluster']['@id']
        
    def getClustersList(self):
        '''
        @summary: 获取全部集群列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = "GET"
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)} 
    
    def getClusterInfo(self, cluster_name):
        '''
        @summary: 根据集群名称，获取集群详细信息
        @param cluster_name: 集群名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的数据中心信息
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s' % (self.base_url, cluster_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def createCluster(self, cluster_info):
        '''
        @summary: 创建集群
        @param cluster_info: XML形式的集群信息，调用接口时需要传递此xml数据
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=cluster_info)
        print r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)} 
    
    def updateCluster(self, cluster_name, update_info):
        '''
        @summary: 编辑集群
        @param cluster_name: 集群名称
        @param update_info: 更新的内容
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s' % (self.base_url, cluster_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=update_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def delCluster(self, cluster_name, async=None):
        '''
        @summary: 根据集群名称删除集群，包含同步和异步
        @param cluster_name: 集群名称
        @param async: 是否异步
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s' % (self.base_url, cluster_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=async)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getClusterNetworkList(self,cluster_name):
        '''
        @summary: 根据集群名称获取关联的网络列表
        @param cluster_name: 集群名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s/networks' % (self.base_url, cluster_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getClusterNetworkInfo(self,cluster_name,network_name):
        '''
        @summary: 根据集群名称获取其关联网络的详细信息
        @param cluster_name: 集群名称
        @param network_name: 网络名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        network_list = self.getClusterNetworkList(cluster_name)['result']['networks']['network']
        for network in network_list:
            if network['name']==network_name:
                return network
           
if __name__=='__main__':
    clusterapi = ClusterAPIs()
    #print clusterapi.searchClusterByName('Default')
    #print clusterapi.getClusterIdByName('Default')
    #print clusterapi.getClustersList()
    #print clusterapi.getClusterInfo('Default')
    data = '''
    <cluster>
        <name>NewCluster1</name>
        <cpu id="Intel Nehalem Family"/>
        <data_center href="/api/datacenters/8cfa5137-e11f-445b-bbd5-c5611338d8eb" id="8cfa5137-e11f-445b-bbd5-c5611338d8eb"/>
    </cluster>
    '''
    #print clusterapi.createCluster(data)
    #print clusterapi.updateCluster('NewCluster',data)
    data1 = '''
    <action>
        <async>false</async>
    </action>
    '''
    #print clusterapi.delCluster('NewCluster1',data1)
    #print clusterapi.getClusterNetworkList('Default')
    print clusterapi.getClusterNetworkInfo('Default','aaa')
    #test

    
    