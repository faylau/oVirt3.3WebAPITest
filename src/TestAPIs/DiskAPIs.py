#encoding:utf-8

__authors__ = ['"keke wei" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#-----------------------------------------------------------------------------------------
# Version        Date            Desc                                            Author
#-----------------------------------------------------------------------------------------
# V0.1           2014/09/16    初始版本                                                                                                     wei keke
#-----------------------------------------------------------------------------------------
# V0.2           2014/11/03    *将searchDiskByName修改为searchDiskByAlias          Liu Fei
#-----------------------------------------------------------------------------------------
# V0.3           2014/11/13    *修改smart_delete_disk方法                                                           Liu Fei
#                              *修改了smart方法中的日志信息内容
#-----------------------------------------------------------------------------------------
# V0.4           2014/11/13    *修改smart_delete_disk方法                                                          wei keke
#                              *修改了smart方法中的日志信息内容
                               *增加isExist方法
#-----------------------------------------------------------------------------------------
'''

import xmltodict

from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient
from Utils.PrintLog import LogPrint
from Utils.Util import wait_until


def smart_create_disk(xml_disk_info, disk_alias=None, status_code=202):
    '''
    @summary: 智能创建磁盘，并等待其状态为ok；
    @param disk_alias: 磁盘别名，缺省为空（若在XML中已经提供）
    @param xml_disk_info: 创建磁盘的XML信息
    @param status_code: 成功创建磁盘后，接口返回的状态码，缺省为202
    @return: True or False
    '''
    disk_api = DiskAPIs()  
    r = disk_api.createDisk(xml_disk_info)
    def is_disk_ok():
        return disk_api.getDiskStatus(disk_id)=='ok'
    if r['status_code'] == status_code:
        disk_id = r['result']['disk']['@id']
        #如果磁盘状态在给定时间内变为ok状态，则继续验证状态码和磁盘信息
        if wait_until(is_disk_ok, 500, 5):
            LogPrint().info("INFO: Create disk '%s' SUCCESS and it's state is 'ok'." % disk_alias)
            return [True, disk_id]
        else:
            LogPrint().error("ERROR: Create Disk FAIED, it's status is not 'ok'." )
            return False
    else:
        LogPrint().error("ERROR: Create Disk FAIED, returned status code '%s' is wrong." % r['status_code'])
        return False
    
def smart_delete_disk(disk_id, status_code=200):
    '''
    @summary: 智能删除磁盘，并等待其状态为ok；
    @param disk_id:待删除的磁盘id
    @param status_code: 成功删除磁盘后，接口返回的状态码，缺省为200
    @return: True or False
    '''
    disk_api = DiskAPIs()
    def is_disk_delete(disk_id):
        return disk_api.isExist(disk_id) == 'False'
    try:
        disk_api.getDiskInfo(disk_id)
        if disk_api.getDiskStatus(disk_id) != 'ok':
            LogPrint().warning("WARN: The disk is not 'ok'. It cannot be deleted.")
            return False
        else: 
            r = disk_api.deleteDisk(disk_id)
            # 2014/11/13: Modified by LiuFei: add 'int' before status_code.
            if r['status_code'] == int(status_code):
                if wait_until(is_disk_delete, 60, 10):
                    LogPrint().info("INFO: Delete disk SUCCESS.")
                    return True
                else:
                    LogPrint().error("INFO: Disk is still exist.")
                    return False

            else:
                LogPrint().error("INFO: Returned status code '%s' is WRONG while deleting disk." % r['status_code'])
                return False
    except:
        LogPrint().warning("INFO: Disk is not exist.")
        return True

class DiskAPIs(BaseAPIs):
    '''
    @summary: 提供磁盘各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义集群相关API的base_url，如'https://10.1.167.2/api/clusters'
        '''
        self.base_url = '%s/disks' % WebBaseApiUrl
        
    def searchDiskByAlias(self, disk_alias):
        '''
        @summary: 根据磁盘名称查找
        @param disk_name: 磁盘名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：搜索到的所有集群（dict格式）。
        '''
        return self.searchObject('disks', disk_alias, search_item='alias')
    
    def getDiskIdByName(self, disk_alias):
        '''
        @summary: 根据磁盘名称获取其ID（前提是磁盘名称唯一）
        '''
        r = self.searchDiskByName(disk_alias)
        return r['result']['disks']['disk']['@id']
    
    def isExist(self,disk_id):
        '''
        @summary: 系统内磁盘是否存在
        '''
        disk_list = DiskAPIs().getDisksList()['result']['disks']['disk']
        flag=False
        for disk in disk_list:
            diskid = disk['@id']
            if diskid == disk_id:
                flag=True
        return flag
                
        
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
        
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getDiskStatus(self,disk_id):
        return DiskAPIs().getDiskInfo(disk_id)['result']['disk']['status']['state']
    
    def createDisk(self, disk_info):
        '''
        @summary: 创建磁盘
        @param disk_info: XML形式的集群信息，调用接口时需要传递此xml数据
                   磁盘大小、存储域、interface、format参数是必需的(不能设置type字段)
                  异常情况说明：
         1）存储域不存在：404
         2）缺少参数或参数错误：400
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=disk_info)
#         print r.status_code
#         print r.text
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
        3）磁盘附加到虚拟机，虚拟机运行，磁盘被激活，删除失败，抛出409
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
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    
if __name__=='__main__':
    diskapi = DiskAPIs()
    #print diskapi.getDisksList()
    print diskapi.isExist('0cf6c057-c60a-4904-bc80-92747e93b')

    disk_test_info = '''
    <disk>
        <alias>disk-aaaaaaaaa</alias>
        <storage_domains>
            <storage_domain>
                <name>data1-ITC040201</name>
            </storage_domain>
        </storage_domains>
        <size>105906176</size>
        <interface>virtio</interface>
        <format>cow</format>
    </disk>
    '''
    #r = diskapi.createDisk(disk_test_info)
    
    disk_info='''
    <disk>
    <alias>Disk-test</alias>
    <name>Disk-test</name>
    <storage_domains>
        <storage_domain>
            <name>Data1-ISCSI</name>
        </storage_domain>
    </storage_domains>
    <size>105906176</size>
    <sparse>true</sparse>
    <interface>virtio</interface>
    <format>cow</format>
    <bootable>true</bootable>
    <shareable>true</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
    '''
    disk_info1 = '''
    <disk>
    <alias>Test-DISK</alias>
    <storage_domains>
        <storage_domain>
            <name>Data1-ISCSI</name>
        </storage_domain>
    </storage_domains>
    <size>1059061760</size>
    <interface>virtio</interface>
</disk>

    '''
    #print xmltodict.unparse(diskapi.createDisk(disk_info)['result'],pretty=True)
    #print diskapi.createDisk(disk_info)['status_code']
    #print diskapi.getDiskInfo()
    '''
    3d5d2e5f-e161-4651-b157-52215737981e 模板
    <fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot remove Virtual Machine Disk. Provided wrong storage domain, which is not related to disk.]</detail>
</fault>
    c1cc6199-9fd9-4274-836c-305895459a92 运行虚拟机
    <fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot remove Virtual Machine Disk. At least one of the VMs is not down.]</detail>
</fault>
    ff31f5cb-ef9b-4cf1-8105-e8e6772a7f91 关机虚拟机
    '''
#     print xmltodict.unparse(diskapi.deleteDisk('3d5d2e5f-e161-4651-b157-52215737981e')['result'],pretty=True)
    #print diskapi.getStaticsofDisk('0cf6c057-c60a-4904-bc80-92747e93b558')
    action = '''
    <action>
    <async>true</async>
    </action>
    '''
    #print diskapi.exportDisk('b72dc92d-bb13-4324-bbd1-e71be947cca5', action)（fail）
    print diskapi.deleteDisk('bba6ad5f-e40b-472a-b15d-1691c99a728b', action)
    
    
   

    
    