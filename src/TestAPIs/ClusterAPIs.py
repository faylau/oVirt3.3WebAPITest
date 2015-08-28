#encoding:utf-8

from telnetlib import STATUS
from _multiprocessing import flags
from __builtin__ import True



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
from VirtualMachineAPIs import VirtualMachineAPIs

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
def smart_create_volume(xml_volume_info,cluster_name,volume_name,status_code=201):
    '''
    @return: True/False  
    '''
    volume_api = GlusterVolumeAPIs()
    r = volume_api.createGlusterVolume(cluster_name, xml_volume_info)
    if r ['status_code'] == status_code:
        LogPrint().info("Create Volume '%s'success."%volume_name)
        return True
    else:
        LogPrint().error("Create Volume '%s' fail."%volume_name)
        return False 
      
def smart_start_volume(cluster_name, volume_name,status_code=200):
        r = volumeapi.startGlusterVolume(cluster_name, volume_name)
        if r['status_code'] == status_code:
            def is_volume_up():
                return volumeapi.getClusterVolumeStatus(cluster_name, volume_name) == "up"
            if wait_until(is_volume_up, 600, 5):
                LogPrint().info("Start volume success.")
                return True
            else:
                LogPrint().error("Start volume failed.Status is not UP.")
                return False
        else:
            LogPrint().error("Status_code is WRONG.")
            return False
        
def smart_stop_volume(cluster_name, volume_name,status_code=200):
        r = volumeapi.stopGlusterVolume(cluster_name, volume_name)
        if r['status_code'] == status_code:
            def is_volume_down():
                return volumeapi.getClusterVolumeStatus(cluster_name, volume_name) == "down"
            if wait_until(is_volume_down, 600, 5):
                LogPrint().info("Start volume success.")
                return True
            else:
                LogPrint().error("Start volume failed.Status is not UP.")
                return False
        else:
            LogPrint().error("Status_code is WRONG.")
            return False  
             
def smart_delete_volume(cluster_name, volume_name,status_code=201):
        r = volumeapi.deleteGlusterVolume(cluster_name, volume_name)
        if r['status_code'] == status_code:
            LogPrint().info("Start volume success.")
            return True
        else:
            LogPrint().error("Status_code is WRONG.")
            return False     
def smart_create_affinitygroups(cluster_name,group_info,group_name,status_code=201):
    '''
    @summary: 创建亲和组
    @param cluster_name: 亲和组所属的集群名称
    @param group_info: 亲和组的xml信息
    @param group_name: 亲和组名称
    @param status_code: 创建亲和组返回的状态码，成功为201
    @return: True/False
    '''
    affinitygroups_api = AffinityGroupsAPIs()
    r = affinitygroups_api.createAffinityGroups(cluster_name, group_info)
    if r['status_code'] == status_code:
        LogPrint().info("Create AffinityGroups '%s' success." % group_name)
        return True
    else:
        LogPrint().error("Create AffinityGroups '%s' fail." % group_name)
        return False
    
def smart_delete_affinitygroups(cluster_name,group_name,status_code=200):
    '''
    @summary: 删除亲和组
    @param cluster_name: 亲和组所属的集群名称
    @param group_name: 亲和组名称
    @param status_code: 删除亲和组返回的状态码，成功为200
    @return: True/False
    '''
    affinitygroups_api = AffinityGroupsAPIs()
    try:
        affinitygroups_api.getAffinityGroupsInfo(cluster_name,group_name)
        r = affinitygroups_api.deleteAffinityGroups(cluster_name,group_name)
        if r['status_code'] == status_code:
            LogPrint().info("Delete AffinityGroups '%s' success." % group_name)
            return True
        else:
            LogPrint().error("Delete AffinityGroups '%s' fail." % group_name)
            return True
    except:
        LogPrint().info("AffinityGroups '%s' is not exist." % group_name)
        return False
    
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
class GlusterVolumeAPIs(ClusterAPIs):
    '''
    @summary: 提供集群各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义集群相关API的base_url，如'https://10.1.167.2/api/clusters'
        '''
        self.base_url = '%s/clusters' % WebBaseApiUrl 
        self.sub_url_volumes = 'glustervolumes'
        
    def getGlusterVolumeList(self, cluster_name):
        '''
        @summary: 获取集群内卷列表
        @param cluster_name: 集群名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的卷列表。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s/%s' % (self.base_url, cluster_id, self.sub_url_volumes)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
    
    def getVolumeIdByName(self, cluster_name, volume_name):
        '''
        @summary: 根据卷名称返回卷ID
        @param cluster_name: 集群名称
        @param volume_name: 卷名称
        @return: 返回卷ID
        '''
        cluster_volumes = self.getGlusterVolumeList(cluster_name)['result']['gluster_volumes']['gluster_volume']
        if isinstance(cluster_volumes, list):
            for volume in cluster_volumes:
                if volume['name']==volume_name:
                    return volume['@id']
        else:
            if cluster_volumes['name']==volume_name:
                return cluster_volumes['@id']
            
    def getGlusterVolumeInfo(self, cluster_name, volume_name):
        '''
        @summary: 获取集群内的卷信息
        @param cluster_name: 集群名称
        @param volume_name: 卷名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的卷信息。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        volume_id = self.getVolumeIdByName(cluster_name, volume_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, cluster_id, self.sub_url_volumes, volume_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
    
    def getClusterVolumeStatus(self, cluster_name, volume_name):
        '''
        @summary: 获取集群内卷的状态
        @param cluster_name: 集群名称
        @param volume_name: 卷名称
        @return: 卷状态（down、up）
        '''
        volume_info = self.getGlusterVolumeInfo(cluster_name, volume_name)
        return volume_info['result']['gluster_volume']['status']['state'] 
    
    def createGlusterVolume(self, cluster_name, xml_volume_info):
        '''
        @summary: 创建一个卷
        @param cluster_name: 集群名称
        @param xml_volume_info: 卷xml配置信息
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的卷信息。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s/%s' % (self.base_url, cluster_id, self.sub_url_volumes)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_volume_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    def startGlusterVolume(self, cluster_name, volume_name):
        '''
        @summary: 启动卷
        @param cluster_name: 集群名称
        @param volume_name: 卷名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的卷信息。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        volume_id = self.getVolumeIdByName(cluster_name, volume_name)
        api_url = '%s/%s/%s/%s/start' % (self.base_url, cluster_id, self.sub_url_volumes, volume_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
    def stopGlusterVolume(self, cluster_name, volume_name):
        '''
        @summary: 关闭卷
        @param cluster_name: 集群名称
        @param volume_name: 卷名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的卷信息。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        volume_id = self.getVolumeIdByName(cluster_name, volume_name)
        api_url = '%s/%s/%s/%s/stop' % (self.base_url, cluster_id, self.sub_url_volumes, volume_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data='<action/>')
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   

    def deleteGlusterVolume(self, cluster_name, volume_name):
        '''
        @summary: 删除卷
        @param cluster_name: 集群名称
        @param volume_name: 卷名称
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的卷信息。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        volume_id = self.getVolumeIdByName(cluster_name, volume_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, cluster_id, self.sub_url_volumes, volume_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    def addbrick(self, cluster_id, volume_id, brick_info):
        '''
        @summary: 为卷添加brick
        @param volume_id: 卷id
        @param brick_info: brick信息
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的卷信息。
        '''
        api_url = '%s/%s/%s/%s/bricks' % (self.base_url, cluster_id, self.sub_url_volumes, volume_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=brick_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    def delbrick(self, cluster_id, volume_id, brick_id):
        '''
        @summary: 为卷删除brick
        @param volume_id: 卷id
        @param brick_id: 卷id
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的卷信息。
        '''
        api_url = '%s/%s/%s/%s/bricks/%s' % (self.base_url, cluster_id, self.sub_url_volumes, volume_id, brick_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
class AffinityGroupsAPIs(ClusterAPIs):
    '''
    @summary: 提供虚拟机亲和组各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义亲和组相关API的base_url，如'https://10.1.167.2/api/clusters'
        '''
        self.base_url = '%s/clusters' % WebBaseApiUrl
        self.sub_url_groups = 'affinitygroups'
            
    def getAffinityGroupsList(self,cluster_name):
        '''
        @summary: 根据集群名称获取关联的亲和组列表
        @param cluster_name: 集群名称 
        @return: 字典，包括：（1）status_code:http请求返回码      （2）result:请求返回的内容
        
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s/%s' % (self.base_url, cluster_id,self.sub_url_groups)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def isGroupExist(self,cluster_name,group_name):
        '''
        @summary: 判断亲和组是否存在
        @param cluster_name: 亲和组所属的集群名称
        @param group_name: 亲和组名称
        @return: 亲和组存在则返回True，不存在则返回False
        
        '''
        affinity_groups = self.getAffinityGroupsList(cluster_name)['result']['affinity_groups']
        if affinity_groups == None:
            return False
        else:
            affinity_groups = self.getAffinityGroupsList(cluster_name)['result']['affinity_groups']['affinity_group']
        flag = False
        if isinstance(affinity_groups, dict):
            if affinity_groups['name'] == group_name:
                return True
            else:
                return False
        else:
            for group in affinity_groups:
                if group['name'] == group_name:
                    flag = True
            return flag
        
    def getGroupIdByName(self,cluster_name,group_name):
        '''
        @summary: 根据亲和组名称获取其id
        @param cluster_name: 亲和组所属的集群名称
        @param group_name: 亲和组名称
        @return: 亲和组的id
        
        '''
        affinity_groups = self.getAffinityGroupsList(cluster_name)['result']['affinity_groups']['affinity_group']
        if isinstance(affinity_groups, list):
            for group in affinity_groups:
                if group['name']==group_name:
                    return group['@id']
        else:
            if affinity_groups['name']==group_name:
                return affinity_groups['@id']
    
    def getAffinityGroupsInfo(self,cluster_name,group_name):
        '''
        @summary: 根据集群名称获取其关联亲和组的详细信息
        @param cluster_name: 集群名称
        @param affinitygroup_name: 亲和组名称
        @return: 字典，包括：（1）status_code:http请求返回码       （2）result:请求返回的内容
        
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        group_id = self.getGroupIdByName(cluster_name, group_name)
        api_url = '%s/%s/%s/%s' % (self.base_url,cluster_id,self.sub_url_groups,group_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def createAffinityGroups(self,cluster_name,group_info):
        '''
        @summary: 创建亲和组
        @param cluster_name: 亲和组所属的集群名称
        @param groups_info: XML形式的亲和组信息，调用接口时需要传递此xml数据
        @return: 字典：包括：（1）status_code:http请求返回码     （2）result:请求返回的内容
        
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        api_url = '%s/%s/%s' % (self.base_url, cluster_id,self.sub_url_groups)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=group_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def addVmtoAffinityGroups(self,cluster_name,group_name,vm_name):
        '''
        @summary: 添加虚拟机到亲和组
        @param cluster_name: 亲和组所属的集群名称
        @param group_name: 亲和组名称
        @param vm_name: 要添加到亲和组的虚拟机名称
        @return: 字典：包括：（1）status_code: http请求返回码      （2）result: 请求返回的内容
        
        '''
        vm_api = VirtualMachineAPIs()
        cluster_id = self.getClusterIdByName(cluster_name)
        group_id = self.getGroupIdByName(cluster_name, group_name)
        vm_info = xmltodict.unparse(vm_api.getVmInfo(vm_name)['result'])
        api_url = '%s/%s/%s/%s/vms' % (self.base_url, cluster_id,self.sub_url_groups,group_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=vm_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def removeVmfromAffinityGroups(self,cluster_name,group_name,vm_name,async=None):
        '''
        @summary: 移除亲和组中的虚拟机
        @param cluster_name: 亲和组所属的集群名称
        @param group_name: 亲和组名称
        @param vm_name: 要从亲和组中移除的虚拟机名称
        @param async: 是否异步，xml文件
        <action>
            <async>false</async>
        </action>
        @return: 字典：包括：（1）status_code: http请求返回码      （2）result: 请求返回的内容
        
        '''
        vm_api = VirtualMachineAPIs()
        cluster_id = self.getClusterIdByName(cluster_name)
        group_id = self.getGroupIdByName(cluster_name, group_name)
        vm_id = vm_api.getVmIdByName(vm_name)
        api_url = '%s/%s/%s/%s/vms/%s' % (self.base_url, cluster_id,self.sub_url_groups,group_id, vm_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=async)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def updateAffinityGroups(self,cluster_name,group_name,update_info):
        '''
        @summary: 编辑虚拟机亲和组
        @param cluster_name: 亲和组所属的集群名称
        @param update_info: XML形式的亲和组信息，调用接口时需要传递此xml数据
        @return: 字典：包括：（1）status_code:http请求返回码     （2）result:请求返回的内容
        
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        group_id = self.getGroupIdByName(cluster_name, group_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, cluster_id,self.sub_url_groups,group_id)
        method = 'PUT'
        r = HttpClient.sendRequest( method=method, api_url=api_url, data=update_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def deleteAffinityGroups(self,cluster_name,group_name,async=None):
        '''
        @summary: 根据集群名称和亲和组名称删除集群下的亲和组，包含同步和异步
        @param cluster_name: 集群名称
        @param group_name: 亲和组名称
        @param async: 是否异步，xml文件
        <action>
            <async>false</async>
        </action>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        cluster_id = self.getClusterIdByName(cluster_name)
        group_id = self.getGroupIdByName(cluster_name, group_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, cluster_id,self.sub_url_groups,group_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=async)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    
if __name__=='__main__':
    clusterapi = ClusterAPIs()
    vm_api = VirtualMachineAPIs()
    affgroups_api = AffinityGroupsAPIs()
    group_name = '1234567'
    group_info = '''
    <affinity_group>
        <name>%s</name>
        <positive>false</positive>
        <enforcing>false</enforcing>
    </affinity_group>
    ''' % (group_name)
    r = affgroups_api.updateAffinityGroups('Cluster-ITC10', group_name, group_info)
    #r = affgroups_api.updateAffinityGroups('Cluster-ITC10', '123456', group_info)
    #r = affgroups_api.addVmtoAffinityGroups('Cluster-ITC10', group_name, '22')
    #r2 = affgroups_api.addVmtoAffinityGroups('Cluster-ITC10', group_name, 'aa')
    #t = vm_api.getVmInfo('22')
    #t1 = xmltodict.unparse(t['result'])
    #print xmltodict.unparse(t['result'], pretty=True)
    #r = affgroups_api.addVmtoAffinityGroups('Cluster-ITC10', group_name, t1)
    #r = affgroups_api.updateAffinityGroups('Cluster-ITC10', group_name, group_info)
    #r = affgroups_api.addVmtoAffinityGroups('Cluster-ITC10', group_name, '22')
    print r['status_code']
    print xmltodict.unparse(r['result'], pretty=True)
    #print r2['status_code']
    #print xmltodict.unparse(r['result'],pretty=True)
    
    #smart_create_affinitygroups('Cluster-ITC10', group_info, group_name, 201)
    #smart_delete_affinitygroups('Cluster-ITC10', group_name, 200)
   
    #print xmltodict.unparse(r['result'], pretty=True)
    #print clusterapi.searchClusterByName('Default')
    #print clusterapi.getClusterIdByName('Default1')
    #print clusterapi.getClusterNameById('46951ef6-5bdb-4da3-89e0-092782b35487')
    #print clusterapi.getClustersList()
    #print clusterapi.getClusterInfo('aaaa')
    #print clusterapi.getClusterInfo(cluster_id='46951ef6-5bdb-4da3-89e0-092782b35487')
    dc_id = DataCenterAPIs().getDataCenterIdByName("Default")
    #print dc_id
    data = '''
    <cluster>
        <name>aaa</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="00000002-0002-0002-0002-000000000146"/>
</cluster>
    '''
    #print clusterapi.createCluster(data)
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
   

    
    
