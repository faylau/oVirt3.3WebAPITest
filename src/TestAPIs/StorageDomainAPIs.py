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
#             print sd_id
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
        (4) FC类型存储描述文件：应该是同(2)，更改一下类型即可，缺少环境未调试。
        @attention: lun_id的获取有两种思路：（1）手动写在xml文件中；（2）写一个getLunIdByName方法，执行login操作后，通过hosts/host-id/storage接口根据name获得lun_id。
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_sd_info)
#         print r.status_code, r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def updateStorageDomain(self, sd_name, xml_update_info):
        '''
        @summary: 更新存储域信息
        @param xml_update_info: XML格式的待更新存储域信息，通过该接口可以编辑NFS、ISCSC和FC类型存储域，如下：
        (1) 编辑NFS类型存储域（NFS类型存储域只能编辑名称、描述等字段）：
            <storage_domain>
                <name>data-new</name>
                <description>aaa</description>
            </storage_domain>
        (2) 编辑ISCSI/FC类型存储域（编辑名称、描述）
            <storage_domain>
                <name>Data2-ISCSI</name>
                <description>bbb</description>
                <storage>
                    <type>iscsi</type>
                    <logical_unit id="35005907f57002df5"/>
                    <override_luns>true</override_luns>
                </storage>
            </storage_domain>
        (3) 编辑ISCSI/FC类型存储域（添加LUN，前提是主机已经登陆该Target）
            <storage_domain>
                <host>
                    <name>node2</name>
                </host>
                <storage>
                    <type>iscsi</type>
                    <logical_unit id="35005907f57002df5"/>
                    <override_luns>true</override_luns>
                </storage>
            </storage_domain>
        (4) 编辑ISCSI/FC类型存储域（添加LUN，前提是主机未登录该Target）
            <storage_domain>
                <host>
                    <name>node2</name>
                </host>
                <storage>
                    <type>iscsi</type>
                    <logical_unit id="35005907f57002df5">
                        <address>10.1.161.61</address>
                        <port>3260</port>
                        <target>iqn.2012-07.com.lenovoemc:ix12.px12-TI3111.wangyy</target>
                        <serial>SLENOVO_LIFELINE-DISK</serial>
                        <vendor_id>LENOVO</vendor_id>
                        <product_id>LIFELINE-DISK</product_id>
                        <lun_mapping>1</lun_mapping>
                    </logical_unit>
                    <override_luns>true</override_luns>
                </storage>
            </storage_domain>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        sd_id = self.getStorageDomainIdByName(sd_name)
        api_url = '%s/%s' % (self.base_url, sd_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_update_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def delStorageDomain(self, sd_name, xml_del_option):
        '''
        @summary: 删除存储域（包括删除、销毁）
        @param sd_name: 存储域名称
        @param xml_del_option: XML格式的删除选项信息；如下：
        <storage_domain>
            <host>
                <name>node2</name>
            </host>
            <format>true</format>
            <destroy>true</destroy>
            <async>false</async>
        </storage_domain>
        @attention: 
        (1) <host>字段是必须提供的；（2）<destroy>字段表示销毁操作，销毁时不需要另外指定<format>字段；
        (3)<format>字段表示是否格式化域，在进行删除操作时必须指定该字段；（4）<async>表示是否异步返回。
        @attention: (1)Maintenance状态可以销毁；（2）游离状态可以删除。
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        sd_id = self.getStorageDomainIdByName(sd_name)
        api_url = '%s/%s' % (self.base_url, sd_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_del_option)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}

    def importStorageDomain(self, xml_sd_info):
        '''
        @summary: 导入被销毁的ISO/Export域
        @attention: 该接口只能完成导入域操作，导入之后的存储域处于游离状态，需要调用其他接口将其附加到某个数据中心。
        @param xml_sd_info: XML格式的待导入的存储域信息，如：
        <storage_domain>
            <type>iso</type>
            <storage>
                <type>nfs</type>
                <address>10.1.167.2</address>
                <path>/storage/iso</path>
            </storage>
            <host>
                <name>node2</name>
            </host>
        </storage_domain>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_sd_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
class DataStorageAPIs(StorageDomainAPIs):
    '''
    @summary: Data存储域磁盘管理子接口，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义Data存储域磁盘管理子接口的base_url，如'https://10.1.167.2/api/storagedomains/<sd-id>/disks'
        '''
        self.base_url = '%s/storagedomains' % WebBaseApiUrl
        self.sub_url = 'disks'
        
    def getDisksListFromDataStorage(self, ds_name):
        '''
        @summary: 从指定的Data存储域中获取磁盘列表
        @param ds_name: Data存储域名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（存储域中磁盘列表）。
        '''
        ds_id = self.getStorageDomainIdByName(ds_name)
        api_url = '%s/%s/%s' % (self.base_url, ds_id, self.sub_url)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getDiskInfoFromDataStorage(self, ds_name, disk_name=None, disk_id=None):
        '''
        @summary: 获取指定的虚拟磁盘详细信息
        @param ds_name: Data存储域名称
        @param disk_name: 虚拟磁盘名称
        @param disk_id: 虚拟磁盘ID
        @return: 
        @todo: 未完成，由于同一存储域中的disk名称可以重复，无法根据disk name进行定位。
        '''
        # todo
        pass
        
    def delDiskFromDataStorage(self, ds_name, disk_name=None, disk_id=None):
        '''
        @summary: 从Data存储域中删除指定的磁盘
        @todo: 问题同上
        '''
        # todo
        pass
    
class ISOStorageAPIs(StorageDomainAPIs):
    '''
    @summary: ISO存储域文件管理子接口，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义ISO域文件管理子接口的base_url，如'https://10.1.167.2/api/storagedomains/<sd-id>/files'
        '''
        self.base_url = '%s/storagedomains' % WebBaseApiUrl
        self.sub_url = 'files'
        
    def getFilesListFromISOStorage(self, is_name):
        '''
        @summary: 从ISO域获取文件列表
        @param is_name: ISO域名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（ISO域中文件列表）。
        '''
        is_id = self.getStorageDomainIdByName(is_name)
        api_url = '%s/%s/%s' % (self.base_url, is_id, self.sub_url)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getFileInfoFromISOStorage(self, is_name, file_name):
        '''
        @summary: 获取ISO域中镜像文件详细信息
        @param is_name: ISO域名称
        @param file_name: 文件名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（文件详细信息）。
        '''
        is_id = self.getStorageDomainIdByName(is_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, is_id, self.sub_url, file_name)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}

class ExportStorageAPIs(StorageDomainAPIs):
    '''
    @summary: Export存储域管理子接口（VM和Template），通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义Export域管理子接口的base_url，如'https://10.1.167.2/api/storagedomains/<sd-id>/files'
        '''
        self.base_url = '%s/storagedomains' % WebBaseApiUrl
        self.sub_url_vms = 'vms'
        self.sub_url_templates = 'templates'
        self.subz_url_disks = 'disks'
        
    def getVmIdByNameFromExportStorage(self, es_name, vm_name):
        '''
        @summary: 根据Export域中的VM名称获取VM的ID
        @param es_name: Export域名称
        @param vm_name: Export域中的VM名称
        @return: Export域中的VM的ID
        '''
        vms = self.getVmsListFromExportStorage(es_name)['result']['vms']['vm']
        if isinstance(vms, list):
            for vm in vms:
                if vm['name']==vm_name:
                    return vm['@id']
        else:
            if vms['name']==vm_name:
                return vms['@id']
        
    def getVmsListFromExportStorage(self, es_name):
        '''
        @summary: 获取Export域中待导入虚拟机列表
        @param es_name: Export域名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（Export域中的VM列表）。
        '''
        es_id = self.getStorageDomainIdByName(es_name)
        api_url = '%s/%s/%s' % (self.base_url, es_id, self.sub_url_vms)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getVmInfoFromExportStorage(self, es_name, vm_name):
        '''
        @summary: 获取Export域中待导入虚拟机详细信息
        @param es_name: Export域名称
        @param vm_name: 待导入虚拟机名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（Export域中的VM信息）。
        '''
        vm_id = self.getVmIdByNameFromExportStorage(es_name, vm_name)
        es_id = self.getStorageDomainIdByName(es_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, es_id, self.sub_url_vms, vm_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def importVmFromExportStorage(self, es_name, vm_name, xml_import_vm_info):
        '''
        @summary: 从Export域导入虚拟机
        @param es_name: Export域名称
        @param vm_name: 待导入的VM名称
        @param xml_import_vm_info: XML格式的导入虚拟机的设置信息，如下：
        (1) 进行最普通的导入虚拟机操作，只需要指定cluster、storage_domain即可，其中<async>设定是否异步，<collapse_snapshot>如果不指定，则缺省值为false（导入的虚拟机带有原来的快照）：
        <action>
            <cluster>
                <name>Default</name>
            </cluster>
            <async>false</async>
            <storage_domain>
                <name>Data2-ISCSI</name>
            </storage_domain>
        (2) 其他几个参数的意义，举例如下：
            (a)<clone>：是否克隆，若克隆则必须设定<collapse_snapshot>为true；
            (b)<collapse_snapshot>：是否去掉快照：
            <action>
                <cluster>
                    <name>Default</name>
                </cluster>
                <async>false</async>
                <storage_domain>
                    <name>data</name>
                </storage_domain>
                <clone>true</clone>
                <vm>
                    <name>new</name>
                    <snapshots>
                        <collapse_snapshots>true</collapse_snapshots>
                    </snapshots>
                </vm>
            </action>
        (3) 导入VM时，若需要更改磁盘的分配策略和存储域，则需要在上述<vm>下增加如下字段：
        <disks>
            <disk id="">
                <storage_domains>
                    <storage_domain id=""/>
                    <sparse></sparse>
                    <format></format>
                </storage_domains>
            </disk>
        </disks>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（操作结果等信息）。
        @todo: xml_info中的第(3)未验证
        '''
        es_id = self.getStorageDomainIdByName(es_name)
        vm_id = self.getVmIdByNameFromExportStorage(es_name, vm_name)
        api_url = '%s/%s/%s/%s/import' % (self.base_url, es_id, self.sub_url_vms, vm_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_import_vm_info)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def delVmFromExportStorage(self, es_name, vm_name):
        '''
        @summary: 从Export域删除待导入的虚拟机
        @param es_name: Export域名称
        @param vm_name: 虚拟机名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（操作结果等信息）。
        '''
        es_id = self.getStorageDomainIdByName(es_name)
        vm_id = self.getVmIdByNameFromExportStorage(es_name, vm_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, es_id, self.sub_url_vms, vm_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getTemplatesListFromExportStorage(self, es_name):
        '''
        @summary: 获取Export域中的模板列表
        @param es_name: Export域名称
        @return: @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（模板列表）。
        '''
        es_id = self.getStorageDomainIdByName(es_name)
        api_url = '%s/%s/%s' % (self.base_url, es_id, self.sub_url_templates)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getTemplateIdByNameFromExportStorage(self, es_name, template_name):
        '''
        @summary: 根据Export域中的模板名称获取模板的ID
        @param es_name: Export域名称
        @param template_name: Export域中的模板名称
        @return: Export域中的模板的ID
        '''
        temps = self.getTemplatesListFromExportStorage(es_name)['result']['templates']['template']
        if isinstance(temps, list):
            for temp in temps:
                if temp['name']==template_name:
                    return temp['@id']
        else:
            if temps['name']==template_name:
                return temps['@id']
    
    def getTemplateInfoFromExportStorage(self, es_name, template_name):
        '''
        @summary: 获取Export域中的模板详细信息
        @param es_name: Export域名称
        @param template_name: Export域中模板名称
        @return: @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（模板详细信息）。
        '''
        es_id = self.getStorageDomainIdByName(es_name)
        template_id = self.getTemplateIdByNameFromExportStorage(es_name, template_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, es_id, self.sub_url_templates, template_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def importTemplateFromExportStorage(self, es_name, template_name, xml_import_temp_info):
        '''
        @summary: 从Export域导入模板
        @param es_name: Export域名称
        @param template_name: Export域中的模板名称
        @param xml_import_temp_info: XML格式的导入模板选项：
        (1) 在通常情况下（不需要克隆），只需指定<storage_domain>、<cluster>即可，另个<async>设定是否异步：
        <action>
            <storage_domain>
                <name>images0</name>
            </storage_domain>
            <cluster>
                <name>Default</name>
            </cluster>
            <async>false</async>
        </action>
        (2) 在需要克隆的情况下，还需要指定<clone>、<template><name>项：
        <action>
            <storage_domain>
                <name>images0</name>
            </storage_domain>
            <cluster>
                <name>Default</name>
            </cluster>
            <clone>true</clone>
            <async>false</async>
            <template>
                <name>NewABC</name>
            </template>
        </action>
        (3) 若导入模板时需要对其disk进行操作，还需要增加如下disks相关字段（类似import vm时的设置，暂未验证）：
        <disks>
            <disk id="">
                ...
            </disk>
        </disks>
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（操作结果）。
        '''
        es_id = self.getStorageDomainIdByName(es_name)
        temp_id = self.getTemplateIdByNameFromExportStorage(es_name, template_name)
        api_url = '%s/%s/%s/%s/import' % (self.base_url, es_id, self.sub_url_templates, temp_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=xml_import_temp_info)
#         print r.status_code, r.text
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def delTemplateFromExportStorage(self, es_name, template_name):
        '''
        @summary: 从Export域中删除Template
        @param es_name: Export域名称
        @param template_name: 待删除的模板名称
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（操作结果）。
        '''
        es_id = self.getStorageDomainIdByName(es_name)
        temp_id = self.getTemplateIdByNameFromExportStorage(es_name, template_name)
        api_url = '%s/%s/%s/%s' % (self.base_url, es_id, self.sub_url_templates, temp_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}



if __name__ == "__main__":
    sdapi = StorageDomainAPIs()
    dsdapi = DataStorageAPIs()
    isoapi = ISOStorageAPIs()
    exportapi = ExportStorageAPIs()
    
    print exportapi.delTemplateFromExportStorage('export1', 'template-osvtest')
    
    xml_import_temp_info = '''
    <action>
        <storage_domain>
            <name>Data1-ISCSI</name>
        </storage_domain>
        <cluster>
            <name>Cluster-ISCSI</name>
        </cluster>
        <async>false</async>
    </action>
    '''
    xml_import_temp_info_1 = '''
    <action>
        <storage_domain>
            <name>Data1-ISCSI</name>
        </storage_domain>
        <cluster>
            <name>Cluster-ISCSI</name>
        </cluster>
        <async>false</async>
        <clone>true</clone>
        <template>
            <name>NewABC</name>
        </template>
    </action>
    '''
#     print exportapi.importTemplateFromExportStorage('export1', 'template-haproxy-osv', xml_import_temp_info_1)
    
#     print exportapi.getTemplateInfoFromExportStorage('export1', 'template-haproxy-osv')
#     print exportapi.getTemplateIdByNameFromExportStorage('export1', 'template-osvtest')
#     print exportapi.getTemplatesListFromExportStorage('export1')
#     print exportapi.delVmFromExportStorage('export', 'test1')
    
    xml_import_vm_info = '''
    <action>
        <cluster>
            <name>Default</name>
        </cluster>
        <storage_domain>
            <name>data</name>
        </storage_domain>
        <async>false</async>
    </action>
    '''
    xml_import_vm_info_1 = '''
    <action>
        <cluster>
            <name>Default</name>
        </cluster>
        <async>false</async>
        <storage_domain>
            <name>data</name>
        </storage_domain>
        <clone>true</clone>
        <vm>
            <name>new</name>
            <snapshots>
                <collapse_snapshots>true</collapse_snapshots>
            </snapshots>
        </vm>

    </action>
    '''
#     print exportapi.importVmFromExportStorage('export', 'test1', xml_import_vm_info_1)
    
#     print exportapi.getVmInfoFromExportStorage('export', 'test1')
#     print exportapi.getVmIdByNameFromExportStorage('export', 'test1')
#     print exportapi.getVmsListFromExportStorage('export1')
    
#     print isoapi.getFileInfoFromISOStorage('ISO', 'ns60-adv-x64-b43.lic.iso')
#     print isoapi.getFilesListFromISOStorage('ISO')
    
#     print dsdapi.getDisksListFromDataStorage('data')
    
    xml_sd_import_info = '''
    <storage_domain>
        <type>export</type>
        <storage>
            <type>nfs</type>
            <address>10.1.167.2</address>
            <path>/storage/export</path>
        </storage>
        <host>
            <name>node1.com</name>
        </host>
    </storage_domain>
    '''    
#     print sdapi.importStorageDomain(xml_sd_import_info)
    
    xml_del_sd_option = '''
    <storage_domain>
        <host><name>node1.com</name></host>
        <destroy>true</destroy>
        <async>false</async>
    </storage_domain>
    '''
#     print sdapi.delStorageDomain('export', xml_del_sd_option)
    
    xml_update_nfs_info = '''
    <storage_domain>
        <name>data1</name>
        <description>aaa</description>
    </storage_domain>
    '''
    xml_update_iscsi_info = '''
    <storage_domain>
        <name>Data2-ISCSI-new</name>
        <description>bbb</description>
        <host>
            <name>node2</name>
        </host>
        <storage>
            <type>iscsi</type>
            <logical_unit id="35005907f57002df5"/>
            <override_luns>true</override_luns>
        </storage>
    </storage_domain>
    '''
    xml_update_iscsi_info_1 = '''
    <storage_domain>
        <host>
            <name>node2</name>
        </host>
        <storage>
            <type>iscsi</type>
            <logical_unit id="35005907f57002df5">
                <address>10.1.161.61</address>
                <port>3260</port>
                <target>iqn.2012-07.com.lenovoemc:ix12.px12-TI3111.wangyy</target>
                <serial>SLENOVO_LIFELINE-DISK</serial>
                <vendor_id>LENOVO</vendor_id>
                <product_id>LIFELINE-DISK</product_id>
                <lun_mapping>1</lun_mapping>
            </logical_unit>
            <override_luns>true</override_luns>
        </storage>
    </storage_domain>
    '''
#     print sdapi.updateStorageDomain('Data2-ISCSI', xml_update_iscsi_info_1)
    
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
#     print sdapi.createStorageDomain(xml_iscsi_sd_info_2)
    
#     print sdapi.getStorageDomainInfo('data1')
#     print xmltodict.unparse(sdapi.getStorageDomainInfo('data1')['result'], pretty=True)
#     print xmltodict.unparse(sdapi.getStorageDomainsList()['result'], pretty=True)
    
    
    