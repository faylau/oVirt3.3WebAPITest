#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/04      初始版本                                                           Liu Fei 
#---------------------------------------------------------------------------------
'''

import xmltodict

from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

class HostAPIs(BaseAPIs):
    '''
    @summary: 提供主机各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义Host相关API的base_url，如'https://10.1.167.2/api/hosts'
        '''
        self.base_url = '%s/hosts' % WebBaseApiUrl
        
    def searchHostByName(self, host_name):
        '''
        @summary: 根据Host名称查找（调用hosts接口中的search方法）
        @param host_name: 主机名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：搜索到的所有Host（dict格式）。
        '''
        return self.searchObject('hosts', host_name)
    
    def getHostIdByName(self, host_name):
        '''
        @summary: 根据Host名称获取其id
        @param host_name: Host名称（在oVirt中是唯一的）
        @return: Host的id
        '''
        host_list = self.searchHostByName(host_name)
        return host_list['result']['hosts']['host']['@id']
    
    def getHostNameById(self, host_id):
        '''
        @summary: 根据数据中心的id返回其名称
        @param dc_id: 数据中心id
        @return: 数据中心名称
        @todo: 无需实现该功能，后续如果有需要再实现。
        '''
        pass
    
    def getHostsList(self):
        '''
        @summary: 获取全部虚拟化主机列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getHostInfo(self, host_name):
        '''
        @summary: 获取虚拟化主机详细信息
        @param host_name: 虚拟化主机名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：虚拟化主机详细信息（dict格式）。
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s' % (self.base_url, host_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def getHostStatus(self, host_name):
        '''
        @summary: 获取虚拟化主机状态
        @param host_name: 虚拟化主机名称
        @return: 虚拟化主机状态（up、maintenance等）
        '''
        return self.getHostInfo(host_name)['result']['host']['status']['state']

    def createHost(self, xml_host_info):
        '''
        @summary: 创建虚拟化主机
        @param xml_host_info: XML形式的虚拟化主机信息，用于创建主机
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式的新建主机信息）
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_host_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def updateHost(self, host_name, xml_update_info):
        '''
        @summary: 编辑虚拟主机信息
        @param host_name: 虚拟主机名称
        @param xml_update_info: 待编辑的虚拟主机信息（XML格式）
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式的编辑主机信息）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s' % (self.base_url, host_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_update_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def delHost(self, host_name, xml_option=None):
        '''
        @summary: 删除虚拟化主机
        @param host_name: 虚拟化主机名称
        @param xml_option: 删除虚拟化主机时使用的选项（XML格式，如强制删除、是否同步等）
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s' % (self.base_url, host_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def activeHost(self, host_name, xml_option='<action/>'):
        '''
        @summary: 激活虚拟化主机
        @param host_name: 虚拟化主机名称
        @param xml_option: 激活虚拟化主机时需要POST的数据，缺省值是（只能是）'<action/>'
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式操作结果）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/activate' % (self.base_url, host_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def deactiveHost(self, host_name, xml_option='<action/>'):
        '''
        @summary: 取消激活虚拟化主机（维护）
        @param host_name: 虚拟化主机名称
        @param xml_option: 取消激活（维护）虚拟化主机时需要POST的数据，缺省值是（只能是）'<action/>'
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式操作结果）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/deactivate' % (self.base_url, host_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def approveHost(self, host_name, xml_option):
        '''
        @summary: 将RHEV-H类型主机迁移至其他集群（一般情况下都是RHEL类型主机，无法进行approve操作）
        @param host_name: 主机名称
        @param xml_option: 
        @return: 
        @todo: 未完成
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/approve' % (self.base_url, host_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_option)
        print r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def installHost(self, host_name, xml_install_option):
        '''
        @summary: 在RHEL类型虚拟化主机上安装VDSM及相关软件包
        @param host_name: 虚拟化主机名称
        @param xml_install_option: 需要向服务器POST的XML数据
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式操作结果）
        @attention: 虚拟化版中实际已经安装了VDSM，所以Create就完成了添加+安装的操作，而一般情况下无需使用该方法
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/install' % (self.base_url, host_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_install_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def fenceHost(self, host_name, xml_fence_option):
        '''
        @summary: 通过电源管理对主机进行manual/restart/start/stop/status等操作
        @param host_name: 虚拟化主机名称（已配置电源管理）
        @param xml_fence_option: 形式如下：
            <action>
                <fence_type>start</fence_type>
            </action>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式操作结果）
        @attention: 此API尚未验证（缺少电源管理功能的主机）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/fence' % (self.base_url, host_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_fence_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def iscsiDiscoverByHost(self, host_name, xml_iscsi_info):
        '''
        @summary: ISCSI存储发现
        @param host_name: 主机名称
        @param xml_iscsi_info: iSCSI目标地址、端口等信息
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式，包括target列表）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/iscsidiscover' % (self.base_url, host_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_iscsi_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
        
    

if __name__ == "__main__":
    hostapi = HostAPIs()
    
    xml_iscsi_info = '''
    <action>
        <iscsi>
            <address>10.1.161.61</address>
                <port>3260</port>
        </iscsi>
    </action>
    '''
    print xmltodict.unparse(hostapi.iscsiDiscoverByHost('node3.com', xml_iscsi_info)['result'], pretty=True)
    
#     xml_install_option = '''
#     <action>
#         <root_password>qwer1234</root_password>
#     </action>
#     '''
#     print hostapi.installHost('node3.com', xml_install_option)
    
#     print hostapi.activeHost('node3.com')
#     print hostapi.deactiveHost('node3.com')

#     xml_approve_option = '''
#     <action>
#         <cluster>
#             <name>new</name>
#         </cluster>
#         <async>false</async>
#     </action>
#     '''
#     print hostapi.approveHost('node3.com', xml_approve_option)
    
#     xml_del_option = '''
#     <action>
#         <force>true</force>
#         <async>false</async>
#     </action>
#     '''
#     print hostapi.delHost('node3.com', xml_del_option)

#     print hostapi.searchHostByName('node3.com')
#     print hostapi.getHostIdByName('node3.com')
#     print hostapi.getHostsList()
#     print hostapi.getHostInfo('node1.com')
#     print hostapi.getHostStatus('node3.com')

#     xml_host_info = '''
#     <host>
#         <cluster>
#             <name>Cluster-ISCSI</name>
#         </cluster>
#         <name>node3.com</name>
#         <address>10.1.167.3</address>
#         <root_password>qwer1234</root_password>
#     </host>
#     '''
#     print hostapi.createHost(xml_host_info)
    
#     xml_update_info = '''
#     <host>
#         <cluster><name>NewCluster</name></cluster>
#     </host>
#     '''
#     print hostapi.updateHost('node3.com', xml_update_info)
    

    
    