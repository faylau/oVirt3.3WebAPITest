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
from Utils.PrintLog import LogPrint
from Utils.Util import wait_until


def smart_create_host(host_name, xml_host_info):
    '''
    @summary: 创建主机，并等待其变为UP状态。
    @param host_name: 新创建的主机名称
    @param xml_host_info: 创建主机的xml格式信息，用于向接口传参数
    @return: True or False
    '''
    host_api = HostAPIs()
    r = host_api.createHost(xml_host_info)
    def is_host_up():
        return host_api.getHostStatus(host_name)=='up'
    if wait_until(is_host_up, 200, 5):
        if r['status_code'] == 201:
            LogPrint().info("INFO-PASS: Create host '%s' SUCCESS." % host_name)
            return True
        else:
            LogPrint().error("INFO-FAIL: Create host '%s' FAILED. Returned status code is INCORRECT." % host_name)
            return False
    else:
        LogPrint().error("INFO-FAIL: Create host '%s' FAILED. It's final state is not 'UP'." % host_name)
        return False

def smart_del_host(host_name, xml_host_del_option):
    '''
    @summary: 在不同的最终状态下删除Host
    @param host_name: 待删除的主机名称
    @param xml_host_del_option: 删除主机时所采用的删除配置项
    @return: True or False
    '''
    host_api = HostAPIs()
    def is_host_maintenance():
        return host_api.getHostStatus(host_name)=='maintenance'
    if host_api.searchHostByName(host_name)['result']['hosts']:
        host_state = host_api.getHostStatus(host_name)
        # 当主机状态为UP时，先设置为“维护”，然后再删除
        if host_state == 'up' or host_state == 'non_responsive':
            LogPrint().info("INFO: Deactivate host '%s' from 'up' to 'maintenance' state." % host_name)
            r = host_api.deactiveHost(host_name)
            if wait_until(is_host_maintenance, 120, 5):
                LogPrint().info("INFO: Delete host '%s' from cluster." % host_name)
                r = host_api.delHost(host_name, xml_host_del_option)
                return r['status_code']==200
        # 当主机状态为maintenance或install_failed时，直接删除
        elif host_state=='maintenance' or host_state=='install_failed':
            LogPrint().info("INFO: Delete host '%s' from cluster." % host_name)
            r = host_api.delHost(host_name, xml_host_del_option)
            return r['status_code']==200
    else:
        LogPrint().warning("INFO-WARN: Host '%s' not exist." % host_name)
        return True

class HostAPIs(BaseAPIs):
    '''
    @summary: 提供主机各种常用操作，通过HttpClient调用相应的REST接口实现。
    @attention: 与虚拟化主机Nic和逻辑网络相关的接口尚未完全调试，建议在V0.1版本中暂时不要调用或测试。
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
    
    def getHostInfo(self, host_name=None, host_id=None):
        '''
        @summary: 获取虚拟化主机详细信息（可根据主机名称或id）
        @param host_name: 虚拟化主机名称，缺省为None
        @param host_id: 虚拟化主机id，缺少为None
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：虚拟化主机详细信息（dict格式）。
        '''
        if not host_id and host_name:
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
    
    def getSPMInfo(self, host_name):
        '''
        @summary: 判断虚拟化主机是否为SPM
        @param host_name: 虚拟化主机名称
        @return: 字典，key为：（1）spm_priority（SPM优先级）；（2）is_spm（True or False）。
        '''
        isSPM = self.getHostInfo(host_name)['result']['host']['storage_manager']['#text']
        priority = self.getHostInfo(host_name)['result']['host']['storage_manager']['@priority']
        return {'spm_priority':priority, 'is_spm':isSPM}

    def createHost(self, xml_host_info):
        '''
        @summary: 创建虚拟化主机
        @param xml_host_info: XML形式的虚拟化主机信息，用于创建主机：
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
    
    def iscsiLogin(self, host_name, xml_target_info):
        '''
        @summary: ISCSI存储登陆（挂载）
        @param host_name: 主机名称
        @param xml_target_info: 要登录的ISCSI存储信息，至少包括ip、target_name等信息，举例如下：
            <action>
                <iscsi>
                    <address>mysan.exam ple.com </address>
                    <target>iqn.2009-08.com .exam...</target>
                    <username>jimmy</username>
                    <password>s3kr37</password>
                </iscsi>
            </action>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式，host挂载的target信息）      
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/iscsilogin' % (self.base_url, host_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_target_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def commitNetConfig(self, host_name, xml_action='<action/>'):
        '''
        @summary: 提交保存虚拟化主机网络配置
        @param host_name: 虚拟化主机名称
        @param xml_action: XML格式的action，向服务器发送POST请求时需要传输的数据，取值只能是'<action/>'
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式，包括操作结果）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/commitnetconfig' % (self.base_url, host_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_action)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def forceSelectSPM(self, host_name, xml_action='<action/>'):
        '''
        @summary: 强制将虚拟化主机设置为SPM
        @param host_name: 虚拟化主机名称
        @param xml_action: XML格式的action，向服务器发送POST请求时需要传输的数据，取值只能是'<action/>'
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式，包括操作结果）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/forceselectspm' % (self.base_url, host_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_action)
#         print r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getHostStatistics(self, host_name):
        '''
        @summary: 获取虚拟化主机统计信息（包括memory、swap、cpu）
        @param host_name: 虚拟化主机名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式，包括操作结果）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/statistics' % (self.base_url, host_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
class HostNicAPIs(HostAPIs):
    '''
    @summary: 虚拟化主机网络接口子接口，提供主机网络各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义HostNic相关子接口的base_url，如'https://10.1.167.2/api/hosts/<host_id>/nics'
        '''
        self.base_url = '%s/hosts' % WebBaseApiUrl
        self.sub_url = 'nics'
        
    def getHostNicIdByName(self, host_name, nic_name):
        '''
        @summary: 根据虚拟化主机网络接口名称获得其ID
        @param host_name: 虚拟化主机名称
        @param nic_name: 虚拟化主机网络接口名称（如eth0等）
        @return: 虚拟化主机网络接口ID
        '''
        host_nics_list = self.getHostNicsList(host_name)['result']['host_nics']['host_nic']
        for nic in host_nics_list:
            if nic['name']==nic_name:
                return nic['@id']
            
    def getHostNicsList(self, host_name):
        '''
        @summary: 获取虚拟化主机网络接口列表
        @param host_name: 虚拟化主机名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式主机网络接口列表）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/%s' % (self.base_url, host_id, self.sub_url)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getHostNicInfo(self, host_name, nic_name):
        '''
        @summary: 获取虚拟化主机网络接口信息
        @param host_name: 虚拟化主机名称
        @param nic_name: 虚拟化主机网络接口名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式网络接口信息）
        '''
        host_id = self.getHostIdByName(host_name)
        nic_id = self.getHostNicIdByName(host_name, nic_name)
        api_url = '%s/%s/nics/%s' % (self.base_url, host_id, nic_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code==200:
            return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        else:
            return {'status_code':r.status_code, 'result':r.text}
        
    def updateHostNic(self, host_name, nic_name, xml_nic_info):
        '''
        @summary: 更新虚拟化主机网络接口信息
        @param host_name: 虚拟化主机名称
        @param nic_name: 虚拟化主机网络接口名称
        @param xml_nic_info: 要修改的网络接口信息，如：
            <host_nic>
                <boot_protocol>static</boot_protocol>
                <ip address="192.168.0.1" netmask="255.255.255.0" gateway="192.168.1.1"/>
            </host_nic>
        @return: 
        @attention: 通过验证，目前暂未完成明白该接口实现的功能
        '''
        host_id = self.getHostIdByName(host_name)
        nic_id = self.getHostNicIdByName(host_name, nic_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, host_id, self.sub_url, nic_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_nic_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def attachNicWithNetwork(self, host_name, nic_name, network_name):
        '''
        @summary: 将虚拟化主机网卡与逻辑网络绑定（附加）
        @param host_name: 虚拟化主机名称
        @param nic_name: 虚拟化主机网络接口名称
        @param xml_network_info: network的XML信息（需提供network的name或id），如：
            <action>
                <network id="id"/>
            </action>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容
        @todo: 其功能只是将逻辑网络与物理网卡绑定，至于具体的配置需要调用其他接口？
        '''
        host_id = self.getHostIdByName(host_name)
        nic_id = self.getHostNicIdByName(host_name, nic_name)
        api_url = '%s/%s/%s/%s/attach' % (self.base_url, host_id, self.sub_url, nic_id)
        method = 'POST'
        xml_network_info = '''
        <action>
            <network>
                <name>%s</name>
            </network>
        </action>
        ''' % network_name
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_network_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def detachNicFromNetwork(self, host_name, nic_name, network_name):
        '''
        @summary: 解决虚拟化主机网卡与逻辑网络的绑定（分离）
        @param host_name: 虚拟化主机名称
        @param nic_name: 虚拟化主机网络接口名称
        @param network_name: 逻辑网络名称
        @attention: 通过接口调用时，要求主机处于维护状态才能进行detach操作，与UI不一致，原因不明确
        @return: 
        '''
        host_id = self.getHostIdByName(host_name)
        nic_id = self.getHostNicIdByName(host_name, nic_name)
        api_url = '%s/%s/%s/%s/detach' % (self.base_url, host_id, self.sub_url, nic_id)
        method = 'POST'
        xml_network_info = '''
        <action>
            <network>
                <name>%s</name>
            </network>
        </action>
        ''' % network_name
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_network_info)
        print r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def setupNetworks(self, host_name, xml_networks_info):
        '''
        @summary: 对虚拟化主机上的多个网络接口进行配置
        @param xml_networks_info: 虚拟化主机网络配置信息，如：
            <action>
                <host_nics>
                    <host_nic id="41561e1c-c653-4b45-b9c9-126630e8e3b9">
                        <name>em1</name>
                        <network id="00000000-0000-0000-0000-000000000009"/>
                        <boot_protocol>dhcp</boot_protocol>
                    </host_nic>
                    <host_nic id="3c3f442f-948b-4cdc-9a48-89bb0593cfbd">
                        <name>em2</name>
                        <network id="00000000-0000-0000-0000-000000000010"/>
                        <ip address="10.35.1.247" netmask="255.255.254.0" gateway="10.35.1.254"/>
                        <boot_protocol>static</boot_protocol>
                    </host_nic>
                    <checkConnectivity>true</checkConnectivity>
                    <connectivityTimeout>60</connectivityTimeout>
                    <force>false</force>
                </host_nics>
            </action>
        @attention: 没有指定的nic是否直接设置为空？
        @return: 
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/%s/setupnetworks' % (self.base_url, host_id, self.sub_url)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_networks_info)
        print r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getHostNicStatistics(self, host_name, nic_name):
        '''
        @summary: 获取虚拟化主机Nic的统计信息
        @param host_name: 虚拟化主机名称
        @param nic_name: 虚拟化主机网络接口名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（Nic的速率信息）
        '''
        host_id = self.getHostIdByName(host_name)
        nic_id = self.getHostNicIdByName(host_name, nic_name)
        api_url = '%s/%s/%s/%s/statistics' % (self.base_url, host_id, self.sub_url, nic_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
class HostStorageAPIs(HostAPIs):
    '''
    @summary: 虚拟化主机网络接口子接口，提供主机存储相关操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义HostNic相关子接口的base_url，如'https://10.1.167.2/api/hosts/<host_id>/nics'
        '''
        self.base_url = '%s/hosts' % WebBaseApiUrl
        self.sub_url = 'storage'
        
    def getHostStoragesList(self, host_name):
        '''
        @summary: 获取主机可用的iSCSI或FC存储域
        @param host_name: 虚拟化主机名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（主机可用的iSCSI或FC存储）
        '''
        host_id = self.getHostIdByName(host_name)
        api_url = '%s/%s/%s' % (self.base_url, host_id, self.sub_url)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}

    
        
if __name__ == "__main__":
    hostapi = HostAPIs()
    hostnicapi = HostNicAPIs()
    
#     print hostapi.getHostStatistics('node1.com')
#     print HostStorageAPIs().getHostStoragesList('node1.com')
#     print hostnicapi.getHostNicStatistics('node3.com', 'eth2')
    
#     xml_networks_info='''
#     <action>
#         <host_nics>
#             <host_nic>
#                 <name>eth1</name>
#                 <network>
#                     <name>test1</name>
#                 </network>
#                 <ip address="10.35.1.247" netmask="255.255.254.0" gateway="10.35.1.254"/>
#                 <boot_protocol>static</boot_protocol>
#             </host_nic>
#         </host_nics>
#     </action>
#     '''
#     print hostnicapi.setupNetworks('node3.com', xml_networks_info)
    
#     xml_nic_info = '''
#     <host_nic>
#         <boot_protocol>static</boot_protocol>
#         <ip address="192.168.0.1" netmask="255.255.255.0" gateway="192.168.1.1"/>
#     </host_nic>
#     '''
#     print hostnicapi.updateHostNic('node3.com', 'eth1', xml_nic_info)
    
#     print hostnicapi.detachNicFromNetwork('node3.com', 'eth1', 'test1')
#     print hostnicapi.attachNicWithNetwork('node3.com', 'eth1', 'test1')
#     print hostnicapi.getHostNicInfo('node1.com', 'eth3')
#     print hostnicapi.getHostNicIdByName('node1.com', 'eth1')
#     print hostnicapi.getHostNicsList('node3.com')
    
#     print hostapi.getSPMInfo('node2')
#     print hostapi.forceSelectSPM('node2')
#     print hostapi.commitNetConfig('node3.com')
    
    xml_target_info = '''
    <action>
        <iscsi>
            <address>10.1.161.61</address>
            <target>iqn.2012-07.com.lenovoemc:ix12.px12-TI3111.mari</target>
        </iscsi>
    </action>
    '''
    print xmltodict.unparse(hostapi.iscsiLogin('node3.com', xml_target_info)['result'], pretty=True)
    
#     xml_iscsi_info = '''
#     <action>
#         <iscsi>
#             <address>10.1.161.61</address>
#                 <port>3260</port>
#         </iscsi>
#     </action>
#     '''
#     print xmltodict.unparse(hostapi.iscsiDiscoverByHost('node3.com', xml_iscsi_info)['result'], pretty=True)
    
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
    

    
    