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
    
    def getStorageDomainNameById(self, sd_id):
        '''
        @summary: 根据存储域id返回其名称
        @param sd_id: storage domain的id
        @todo: 目前没有这个需要，暂未实现
        '''
        pass
    
    def getStorageDomainsList(self):
        '''
        @summary: 获得全部storage domain的列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getStorageDomainInfo(self, sd_name=None, sd_id=None):
        '''
        @summary: 根据存储域name或id获取其详细信息
        @param sd_name: 存储域名称，缺省为None
        @param sd_id: 存储域id，缺省为None
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（存储域详细信息）。
        '''
        if not sd_id and sd_name:
            sd_id = self.getStorageDomainIdByName(sd_name)
            print sd_id
        api_url = '%s/%s' % (self.base_url, sd_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def createStorageDomain(self, xml_sd_info):
        '''
        @summary: 创建存储域（游离状态，未附加到任何数据中心）
        @param xml_sd_info: XML格式的待创建存储域相关信息，通过该xml文件可以创建NFS或iSCSI/FC类型存储域，格式如下：
        (1) NFS类型存储域描述文件
            <storage_domain>
                <name>data1</name>
                <type>data</type>
                <host>
                    <name>node1.com</name>
                </host>
                <format>true</format>
                <storage>
                    <type>nfs</type>
                    <address>10.1.167.2</address>
                    <path>/storage/data1</path>
                </storage>
            </storage_domain>
        (2) iSCSI类型存储域描述文件：若主机已经执行了login_iscsi操作，则只需提供lun_id，storage_type等信息便可完成创建，如下：
            <storage_domain>
                <name>Data2-ISCSI</name>
                <type>data</type>
                <host>
                    <name>node3.com</name>
                </host>
                <storage>
                    <type>iscsi</type>
                    <logical_unit id="35005907f72e55e1b"/>
                    <override_luns>true</override_luns>
                </storage>
            </storage_domain>
        (3) iSCSI类型存储域描述文件：直接提供完整的iSCSI lun信息，在创建iSCSI存储域时自动执行login_iscsi操作，如下：
            <storage_domain>
                <name>Data2-ISCSI</name>
                <type>data</type>
                <host>
                    <name>node3.com</name>
                </host>
                <storage>
                    <type>iscsi</type>
                    <logical_unit id="35005907f72e55e1b">
                        <address>10.1.161.61</address>
                        <port>3260</port>
                        <target>iqn.2012-07.com.lenovoemc:ix12.px12-TI3111.mari</target>
                        <serial>SLENOVO_LIFELINE-DISK</serial>
                        <vendor_id>LENOVO</vendor_id>
                        <product_id>LIFELINE-DISK</product_id>
                        <lun_mapping>1</lun_mapping>
                    </logical_unit>
                    <override_luns>true</override_luns>
                </storage>
            </storage_domain>
        (3) FC类型存储描述文件：应该是同(2)，更改一下类型即可，缺少环境未调试。
        @attention: lun_id的获取有两种思路：（1）手动写在xml文件中；（2）写一个getLunIdByName方法，执行login操作后，通过hosts/host-id/storage接口根据name获得lun_id。
        @return: 
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_sd_info)
        print r.status_code, r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def updateStorageDomain(self, sd_name, xml_update_info):
        '''
        @summary: 更新存储域信息
        @param xml_update_info: XML格式的待更新存储域信息
        @return: 
        '''
        pass

if __name__ == "__main__":
    sdapi = StorageDomainAPIs()
    
    xml_nfs_sd_info = '''
    <storage_domain>
        <name>data1</name>
        <type>data</type>
        <host>
            <name>node1.com</name>
        </host>
        <storage>
            <type>nfs</type>
            <address>10.1.167.2</address>
            <path>/storage/data1</path>
        </storage>
    </storage_domain>
    '''
    xml_iscsi_sd_info_1 = '''
    <storage_domain>
        <name>Data2-ISCSI</name>
        <type>data</type>
        <host>
            <name>node3.com</name>
        </host>
        <storage>
            <type>iscsi</type>
            <logical_unit id="35005907f72e55e1b"/>
            <override_luns>true</override_luns>
        </storage>
    </storage_domain>
    '''
    xml_iscsi_sd_info_2 = '''
    <storage_domain>
        <name>Data2-ISCSI</name>
        <type>data</type>
        <host>
            <name>node3.com</name>
        </host>
        <storage>
            <type>iscsi</type>
            <logical_unit id="35005907f72e55e1b">
                <address>10.1.161.61</address>
                <port>3260</port>
                <target>iqn.2012-07.com.lenovoemc:ix12.px12-TI3111.mari</target>
                <serial>SLENOVO_LIFELINE-DISK</serial>
                <vendor_id>LENOVO</vendor_id>
                <product_id>LIFELINE-DISK</product_id>
                <lun_mapping>1</lun_mapping>
            </logical_unit>
            <override_luns>true</override_luns>
        </storage>
    </storage_domain>
    '''
    print sdapi.createStorageDomain(xml_iscsi_sd_info_2)
    
#     print sdapi.getStorageDomainInfo('data1')
#     print xmltodict.unparse(sdapi.getStorageDomainInfo('data1')['result'], pretty=True)
#     print xmltodict.unparse(sdapi.getStorageDomainsList()['result'], pretty=True)
    
    
    