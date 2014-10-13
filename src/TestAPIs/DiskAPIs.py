#encoding:utf-8
__authors__ = ['"keke wei" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/16      初始版本                         wei keke
#---------------------------------------------------------------------------------
'''

import xmltodict

from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

class DiskAPIs(BaseAPIs):
    '''
    @summary: 提供磁盘各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义集群相关API的base_url，如'https://10.1.167.2/api/clusters'
        '''
        self.base_url = '%s/disks' % WebBaseApiUrl
        
    def searchDiskByName(self, disk_name):
        '''
        @summary: 根据磁盘名称查找
        @param disk_name: 磁盘名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：搜索到的所有集群（dict格式）。
        '''
        return self.searchObject('disks', disk_name)
        
    def getDisksList(self):
        '''
        @summary: 获取全部磁盘列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = "GET"
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)} 
    
    def getDiskInfo(self,disk_id):
        '''
        @summary: 根据磁盘id，获取磁盘详细信息
        @param disk_id: 磁盘id
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的数据中心信息
        '''
        api_url = '%s/%s' % (self.base_url, disk_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def createDisk(self, disk_info):
        '''
        @summary: 创建磁盘
        @param disk_info: XML形式的集群信息，调用接口时需要传递此xml数据
                   名称（name或alias只需一个）、存储域、interface、format参数是必需的
                  异常情况说明：
         1）存储域不存在：404
         2）缺少参数或参数错误：400
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=disk_info)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)} 
    
    
        
    def deleteDisk(self, disk_id, async=None):
        '''
        @summary: 删除磁盘
        @param disk_id: 磁盘id
        @param async: 是否异步，xml文件
        <action>
            <async>false</async>
        </action>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        1）磁盘附加到模板：删除失败，抛出400
        2）磁盘附加到虚拟机，虚拟机关机，删除成功
        3）磁盘附加到虚拟机，虚拟机运行，删除失败，抛出409
        '''
        api_url = '%s/%s' % (self.base_url, disk_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=async)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def exportDisk(self, disk_id,action):
        '''
        @summary: 导出磁盘
        @param disk_id: 磁盘id
        @param action: 导出配置，xml文件
        <action>
            <storage_domain id="2170acd2-6fd0-4e88-a566-293a20fca97a"/>
        </action>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        @bug: 执行失败
        '''
        api_url = '%s/%s/export' % (self.base_url, disk_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=action)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getStaticsofDisk(self,disk_id):
        '''
        @summary: 获取磁盘的统计信息
        @param disk_id: 磁盘id
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        api_url = '%s/%s/statistics' % (self.base_url, disk_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    
if __name__=='__main__':
    diskapi = DiskAPIs()
    #print diskapi.getDisksList()
    '''
          
    '''
    disk_info='''
    <disk>
    <alias>Disk-test</alias>
    <name>Disk-test</name>
    <storage_domains>
        <storage_domain>
            <name>data</name>
        </storage_domain>
    </storage_domains>
    <size>105906176</size>
    <type>system</type>
    <sparse>false</sparse>
    <interface>virtio</interface>
    <format>raw</format>
    <bootable>true</bootable>
    <shareable>true</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
    '''
    print diskapi.createDisk(disk_info)
   
    #print diskapi.getDiskInfo()
    '''
    
    '''
    #print diskapi.deleteDisk('1cc9077d-e166-4aec-ac31-fc8a621e4098',False)
    #print diskapi.getStaticsofDisk('0cf6c057-c60a-4904-bc80-92747e93b558')
    action = '''
    <action>
    <storage_domain id="2170acd2-6fd0-4e88-a566-293a20fca97a"/>
    </action>
    '''
    #print diskapi.exportDisk('b72dc92d-bb13-4324-bbd1-e71be947cca5', action)（fail）
    
    
    
   

    
    