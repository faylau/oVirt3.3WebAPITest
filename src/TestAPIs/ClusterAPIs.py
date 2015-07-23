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
from Utils.PrintLog import LogPrint
import xmltodict

from BaseAPIs import BaseAPIs
from NetworkAPIs import NetworkAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient
from DataCenterAPIs import DataCenterAPIs

def smart_create_cluster(cluster_info,cluster_name,status_code=201):
    '''
    @summary: 创建集群，属于Default数据中心
    @param cluster_info:创建集群的xml信息
    @param cluster_name:集群名称 
    @param status_code:创建集群返回的状态码，成功为201
    @return: True/False  
    '''
    cluster_api = ClusterAPIs()
    r = cluster_api.createCluster(cluster_info)
    if r ['status_code'] == status_code:
        LogPrint().info("Create Cluster '%s'success."%cluster_name)
        return True
    else:
        LogPrint().error("Create Cluster '%s' fail."%cluster_name)
        return False
        
def smart_delete_cluster(cluster_name,status_code=200):
    '''
    @summary: 删除集群
    @param cluster_name:待删除的集群名称
    @param status_code:删除集群返回的状态码，成功为200
    @return: True/False  
    '''
    cluster_api = ClusterAPIs()
    try:
        cluster_api.getClusterInfo(cluster_name)
        r = cluster_api.delCluster(cluster_name)
        if r ['status_code'] == status_code:
            LogPrint().info("Delete Cluster '%s'success."%cluster_name)
            return True
        else:
            LogPrint().error("Delete Cluster '%s' fail."%cluster_name)
            return False
    except:
        LogPrint().info("Cluster '%s' is not exist"%cluster_name)
        return True
    
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
        if cluster_list['result']['clusters']:
            return cluster_list['result']['clusters']['cluster']['@id']
        else:
            return None
    
    def getClusterNameById(self, cluster_id):
        '''
        @summary: 根据集群id获取名称
        @param dc_id: 集群id
        @return: 集群名称
        '''
        api_url = '%s/%s' % (self.base_url, cluster_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code==200:
            return xmltodict.parse(r.text)['cluster']['name']
        
    def getClustersList(self):
        '''
        @summary: 获取全部集群列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = "GET"
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        #r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)} 
    
    def getClusterInfo(self, cluster_name=None, cluster_id=None):
        '''
        @summary: 根据集群名称或集群id，获取集群详细信息
        @param cluster_name: 集群名称
        @param cluster_id: 集群id
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的数据中心信息
        '''
        if not cluster_id and cluster_name:
            cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s' % (self.base_url, cluster_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        #r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def createCluster(self, cluster_info):
        '''
        @summary: 创建集群
        @param cluster_info: XML形式的集群信息，调用接口时需要传递此xml数据
        创建集群时集群名称、cpuid和数据中心为必需，其余为可选；
    1)内存优化
    <memory_policy>
        <overcommit percent="150"/>  ；100，150，200，默认为200
        <transparent_hugepages>
            <enabled>true</enabled>  ；默认false
        </transparent_hugepages>
    </memory_policy>  
    2）cpu线程
    <threads_as_cores>false</threads_as_cores> ；默认为false
    3）弹性策略
    <error_handling>
        <on_error>migrate_highly_available</on_error>；包括migrate，migrate_highly_available，do_not_migrate，默认为migrate
    </error_handling>
    4）集群策略
    <scheduling_policy>
         <policy>power_saving</policy>   ；包括none（默认），power_saving，evenly_distributed三种，其中none无需输入，evenly_distributed需要输入high和duration两个参数
         <thresholds low="20" high="80" duration="120"/>
    </scheduling_policy>
    5）其他
    <virt_service>true</virt_service>
    <gluster_service>false</gluster_service>
    <tunnel_migration>false</tunnel_migration>
    <trusted_service>false</trusted_service> ；若设置true，前提是配置服务，否则创建失败
    <ballooning_enabled>false</ballooning_enabled>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=cluster_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)} 
    
    def updateCluster(self, cluster_name, update_info):
        '''
        @summary: 编辑集群
        @param cluster_name: 集群名称
        @param update_info: 更新的内容，xml文件
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s' % (self.base_url, cluster_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=update_info)
        #r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
        
    def delCluster(self, cluster_name, async=None):
        '''
        @summary: 根据集群名称删除集群，包含同步和异步
        @param cluster_name: 集群名称
        @param async: 是否异步，xml文件
        <action>
            <async>false</async>
        </action>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s' % (self.base_url, cluster_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=async)
        #r.raise_for_status()
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
        #r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getClusterNetworkInfo(self,cluster_name,network_name):
        '''
        @summary: 根据集群名称获取其关联网络的详细信息
        @param cluster_name: 集群名称
        @param network_name: 网络名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        network_list = self.getClusterNetworkList(cluster_name)['result']['networks']['network']
        if isinstance(network_list, dict):
            print network_list
            if network_list['name']==network_name:
                return {'network':network_list}
        else:
            for network in network_list:
                if network['name']==network_name:
                    return {'network':network}
            
           
    def attachNetworkToCluster(self, cluster_name, nw_info):
        '''
        @summary: 将网络附加到集群
        @param cluster_name: 集群名称
        @param nw_info: 网络信息（名称或id），xml文件
        <network>
            <name>test1</name>
        </network>
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容。
        '''
        api_url = '%s/%s/networks' % (self.base_url, self.getClusterIdByName(cluster_name))
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=nw_info)
        #r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def detachNetworkFromCluster(self, cluster_name, nw_name, async=None):
        '''
        @summary: 将附加到集群的网络进行分离
        @param cluster_name: 集群名称
        @param nw_name: 网络名称
        @param async: 是否异步，xml文件
        <action>
            <async>true</async>
        </action>
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        dc_id = self.getClusterInfo(cluster_name)['result']['cluster']['data_center']['@id']
        dc_name = DataCenterAPIs().getDataCenterNameById(dc_id)
        nw_id = NetworkAPIs().getNetworkIdByName(nw_name, dc_name)
        method = 'DELETE'
        api_url = '%s/%s/networks/%s' % (self.base_url, cluster_id, nw_id)
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        #r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def updateNetworkOfCluster(self, cluster_name, nw_name,data):
        '''
        @summary: 更新附加到集群的网络信息
        @param cluster_name: 集群名称
        @param nw_name: 网络名称
        @param data:更新的信息，xml文件
        <network>
            <display>false</display>
            <usages>
                <usage>VM</usage>
                <usage>DISPLAY</usage>
            </usages>
        </network>
        @return: 字典，（1）status_code：请求返回状态码；（2）result：请求返回的内容。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        dc_id = self.getClusterInfo(cluster_name)['result']['cluster']['data_center']['@id']
        dc_name = DataCenterAPIs().getDataCenterNameById(dc_id)
        nw_id = NetworkAPIs().getNetworkIdByName(nw_name, dc_name)
        method = 'PUT'
        api_url = '%s/%s/networks/%s' % (self.base_url, cluster_id, nw_id)
        r = HttpClient.sendRequest(method=method, api_url=api_url,data=data)
        #r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
if __name__=='__main__':
    clusterapi = ClusterAPIs()
    #print clusterapi.searchClusterByName('Default')
    #print clusterapi.getClusterIdByName('Default1')
    #print clusterapi.getClusterNameById('46951ef6-5bdb-4da3-89e0-092782b35487')
    #print clusterapi.getClustersList()
    #print clusterapi.getClusterInfo('aaaa')
    #print clusterapi.getClusterInfo(cluster_id='46951ef6-5bdb-4da3-89e0-092782b35487')
    dc_id = DataCenterAPIs().getDataCenterIdByName("Default")
    print dc_id
    data = '''
    <cluster>
        <name>aaa</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="00000002-0002-0002-0002-000000000146"/>
</cluster>
    '''
    print clusterapi.createCluster(data)
    #print xmltodict.unparse(clusterapi.createCluster(data)['result']) 
    #print clusterapi.updateCluster('NewCluster22',data)
    data1 = '''
    <action>
        <async>false</async>    
    </action>
    '''
    #print clusterapi.delCluster('NewCluster1',data1)
    #print clusterapi.getClusterNetworkList('aaaa')
    #print clusterapi.getClusterNetworkInfo('aaaa','aa')
    data2 = '''
    <network id="ef00d7c4-7d9a-4c3b-934c-b1ac7298eaf1">    
    </network>
    '''
    data3 = '''
    <network>
       <name>test1</name>
    </network>
    '''
   
    #print clusterapi.attachNetworkToCluster('Default',data3)
    #print clusterapi.attachNetworkToCluster(cluster_name='Default')
    #print clusterapi.detachNetworkFromCluster(nw_name='aaa')
    data4 = '''
    <network>
    <display>false</display>
    <usages>
        <usage>VM</usage>
        <usage>DISPLAY</usage>
    </usages>
   
    '''
    #print clusterapi.updateNetworkOfCluster('Default','network11',data4)
    #print clusterapi.updateNetworkOfCluster('Default', 'aaa', data4)
#test
   

    
    