#encoding:utf-8
__authors__ = ['keke.wei@cs2c.com.cn']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/09/11     初始版                            wei keke
#---------------------------------------------------------------------------------
'''

import xmltodict

from BaseAPIs import BaseAPIs
from Configs.GlobalConfig import WebBaseApiUrl
from Utils.HttpClient import HttpClient

class TemplatesAPIs(BaseAPIs):
    '''
    @summary: 提供模板各种常用操作，通过HttpClient调用相应的REST接口实现。
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义网相关API的base_url，如'https://10.1.167.2/api/networks'
        '''
        self.base_url = '%s/templates' % WebBaseApiUrl
        
    def searchTemplateByName(self, temp_name):
        '''
        @summary: 根据模板名称查找
        @param temp_name: 模板名称
        '''
        return self.searchObject('templates', temp_name)
    
    
    def getTemplateIdByName(self, temp_name):
        '''
        @summary: 根据模板名称获得其id(系统中模板名称唯一)
        @param temp_name: 模板名称
        @return: 模板id
        '''
        if self.searchTemplateByName(temp_name)['result']['templates']:
            return self.searchTemplateByName(temp_name)['result']['templates']['template']['@id']
        else:
            return None
    
    def getTemplateNameById(self, temp_id):
        '''
        @summary: 根据模板id获取名称
        @param temp_id: 模板id
        @return: 模板名称
        '''
        api_url = '%s/%s' % (self.base_url,temp_id)
        method = "GET"
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        if r.status_code==200:
            return xmltodict.parse(r.text)['template']['name']
                
    def getTemplatesList(self):
        '''
        @summary: 获取全部模板列表
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）。
        '''
        api_url = self.base_url
        method = "GET"
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
    
    def getTemplateInfo(self, temp_name=None,temp_id=None):
        '''
        @summary: 根据模板名称或id获取其详细信息
        @param temp_name: 模板名称
        @param temp_id: 模板id
        @return: 字典：（1）status_code：请求返回码；（2）result：dict形式的数据中心信息
        '''
        if not temp_id and temp_name:
            temp_id = self.getTemplateIdByName(temp_name)
        api_url = '%s/%s' % (self.base_url, temp_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
            
    def createTemplate(self, temp_info):
        '''
        @summary: 创建模板
        @param temp_info: XML形式的集群信息，调用接口时需要传递此xml数据
                   创建模板的测试数据说明：
         1)测试数据最小集: 模板名称和虚拟机id,且模板名称唯一且虚拟机状态为down,创建成功并返回代码202(异步)
         2)通过虚拟机名称表示虚拟机对象,创建失败并返回代码400
         3)虚拟机状态非down,创建失败并返回代码409
         4)其他参数:
           <permissions>
              <clone>true</clone>   ;是否复制虚拟机权限
           </permissions>
           *************************************************
           <vm id="91fab0d3-5ee0-4d81-9e4e-342327d0e362">
              <disks>
                 <disk id="7aa205f0-f292-415b-8bf4-91c009e573d1">
                    <storage_domains>
                       <storage_domain id="ae2d5d54-38d5-41a2-835b-1c966c199855"/>  
                    </storage_domains>
                 </disk>
              </disks>
           </vm> ;为虚拟机的某个磁盘指定存放的存储域
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容（dict格式）
        '''
        api_url = self.base_url
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=temp_info)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}      
    
    def updateTemplate(self, temp_name,update_info):
        '''
        @summary: 编辑模板信息
        @param temp_name: 模板名称
        @param update_info: 更新的内容
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        api_url = '%s/%s' % (self.base_url, temp_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=update_info)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}   
        
        
    def delTemplate(self, temp_name,async=None):
        '''
        @summary: 删除模板
        @param temp_name: 模板名称
        @param async: 是否异步
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        api_url = '%s/%s' % (self.base_url, temp_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=async)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
   
    def exportTemplate(self, temp_name,action):
        '''
        @summary: 导出模板
        @param temp_name: 模板名称
        @param action : 导出配置
        @return: 字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容。
                   设置同步，返回200；设置异步，返回202
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        api_url = '%s/%s/export' % (self.base_url, temp_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url, data=action)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
        
class TemplateDisksAPIs(TemplatesAPIs):
    '''
    @summary: 提供模板的磁盘基本操作
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义网相关API的base_url，如'https://10.1.167.2/api/networks'
        '''
        self.base_url = '%s/templates' % WebBaseApiUrl
    
    def getDiskIdByName(self,temp_name,disk_name):
        '''
        @summary: 根据名称获得模板的磁盘id
        @param temp_name:模板名称
        @param disk_name:磁盘名称 
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        '''
        if self.getTemplateDiskList(temp_name)['result']['disks']:
            disk_list =  self.getTemplateDiskList(temp_name)['result']['disks']['disk']
            if isinstance(disk_list, dict): 
                if disk_list['name'] == disk_name:
                    return disk_list['@id']  
                else:
                    return None
            else:
                for disk in disk_list:
                    if disk['name'] == disk_name:
                        return disk['@id']
                return None
    def getTemplateDiskList(self,temp_name):
        '''
        @summary: 获得某个模板的磁盘列表
        @param temp_name:模板名称
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        api_url = '%s/%s/disks' % (self.base_url, temp_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    
    def getTemplateDiskInfo(self,temp_name,disk_name):
        '''
        @summary: 获得某个模板的某个磁盘信息
        @param temp_name:模板名称
        @param disk_name:磁盘名称 
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        disk_id = self.getDiskIdByName(temp_name, disk_name)
        api_url = '%s/%s/disks/%s' % (self.base_url, temp_id,disk_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
            
    def copyTemplateDisk(self,temp_name,disk_name,copy_data):
        '''
        @summary: 复制某个模板的某个磁盘
        @param temp_name:模板名称
        @param disk_name:磁盘名称 
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        disk_id = self.getDiskIdByName(temp_name, disk_name)
        api_url = '%s/%s/disks/%s/copy' % (self.base_url, temp_id,disk_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url,data=copy_data)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
             
    def exportTemplateDisk(self,temp_name,disk_name,export_data):
        '''
        @summary: 导出某个模板的某个磁盘
        @param temp_name:模板名称
        @param disk_name:磁盘名称 
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容 
        @bug: 执行失败 
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        disk_id = self.getDiskIdByName(temp_name, disk_name)
        api_url = '%s/%s/disks/%s/export' % (self.base_url, temp_id,disk_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url,data=export_data)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
            
    def deleteTemplateDisk(self,temp_name,disk_name,delete_data):
        '''
        @summary: 删除某个模板的某个磁盘
        @param temp_name:模板名称
        @param disk_name:磁盘名称 
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        @bug: 执行失败
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        disk_id = self.getDiskIdByName(temp_name, disk_name)
        api_url = '%s/%s/disks/%s' % (self.base_url, temp_id,disk_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url,data=delete_data)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)} 
    
class TemplateNicsAPIs(TemplatesAPIs):   
    '''
    @summary: 提供模板的网络接口基本操作
    '''
    def __init__(self):
        '''
        @summary: 初始化函数，定义网相关API的base_url，如'https://10.1.167.2/api/networks'
        '''
        self.base_url = '%s/templates' % WebBaseApiUrl
    
    def getTemplateNicList(self,temp_name):
        '''
        @summary: 获得某个模板的网络接口列表
        @param temp_name:模板名称
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        api_url = '%s/%s/nics' % (self.base_url, temp_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def getNicIdByName(self,temp_name,nic_name):
        '''
        @summary: 根据名称获得模板的nic id
        @param temp_name:模板名称
        @param nic_name:nic名称 
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        '''
        if self.getTemplateNicList(temp_name)['result']['nics']:
            nic_list =  self.getTemplateNicList(temp_name)['result']['nics']['nic']
            if isinstance(nic_list, dict): 
                if nic_list['name'] == nic_name:
                    return nic_list['@id']  
                else:
                    return None
            else:
                for nic in nic_list:
                    if nic['name'] == nic_name:
                        return nic['@id']
                return None

    def getTemplateNicInfo(self,temp_name,nic_name):
        '''
        @summary: 获得某个模板的某个网络接口信息
        @param temp_name:模板名称
        @param nic_name:网络接口名称 
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        nic_id = self.getNicIdByName(temp_name, nic_name)
        api_url = '%s/%s/nics/%s' % (self.base_url, temp_id,nic_id)
        method = 'GET'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
            
    def createTemplateNic(self,temp_name,nic_data):
        '''
        @summary：为模板创建网络接口
        @param temp_name:模板名称
        @param nic_data:网络接口配置信息
                   网络接口输入说明：
          1）接口名称是必须的，其余是可选的
          2）配置集必须设置id
                  异常情况说明：
          1）接口名称重复（409）
          2）id设置错误（400）
          3）对象不存在（404） 
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        api_url = '%s/%s/nics' % (self.base_url,temp_id)
        method = 'POST'
        r = HttpClient.sendRequest(method=method, api_url=api_url,data=nic_data)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
        
    def updateTemplateNic(self,temp_name,nic_name,update_data):
        '''
        @summary：编辑某个模板的网络接口
        @param temp_name:模板名称
        @param nic_name:网络接口名称 
        @param update_data:网络接口配置信息 
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        nic_id = self.getNicIdByName(temp_name, nic_name)
        api_url='%s/%s/nics/%s' % (self.base_url,temp_id,nic_id)
        method = 'PUT'
        r = HttpClient.sendRequest(method=method, api_url=api_url,data=update_data)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
    
    def deleteTemplateNic(self,temp_name,nic_name):
        '''
        @summary：删除某个模板的网络接口
        @param temp_name:模板名称
        @param nic_name:网络接口名称 
        @return:字典，包括：（1）status_code：http请求返回码；（2）result：请求返回的内容  
        '''
        temp_id = self.getTemplateIdByName(temp_name)
        nic_id = self.getNicIdByName(temp_name, nic_name)
        api_url='%s/%s/nics/%s' % (self.base_url,temp_id,nic_id)
        method = 'DELETE'
        r = HttpClient.sendRequest(method=method, api_url=api_url)
        r.raise_for_status()
        return {'status_code':r.status_code, 'result':xmltodict.parse(r.text)}
            
if __name__=='__main__':
    tempapi = TemplatesAPIs()
    #print vmapi.searchVmByName('test11')
    #print tempapi.getTemplateIdByName('temp')
    #print tempapi.getTemplateNameById(tempapi.getTemplateIdByName('temp'))
    #print tempapi.getTemplatesList()
    print tempapi.getTemplateInfo('temp3')
    '''
          
    '''
    temp_info1 = '''
    <template>
    <name>template-osvtest1</name>
    <vm id="4fbca0c3-e2b7-4cf0-a680-ea43d5a0e778"/>
    <cluster id="46951ef6-5bdb-4da3-89e0-092782b35487"/>
    </template>
    '''
    
    temp_info2 = '''
    <template>
    <name>template-osvtest6</name>
    <vm id="91fab0d3-5ee0-4d81-9e4e-342327d0e362">
              <disks>
                 <disk id="7aa205f0-f292-415b-8bf4-91c009e573d1">
                    <storage_domains>
                       <storage_domain id="ae2d5d54-38d5-41a2-835b-1c966c199855"/>  
                    </storage_domains>
                 </disk>
              </disks>
    </vm>
           
    </template>
    '''
    #print tempapi.createTemplate(temp_info2)
    #print tempapi.delTemplate("aaaq")
    
    action1='''
    <action>
    <storage_domain>
        <name>export</name>
    </storage_domain>
    <exclusive>false</exclusive>
    <async>false</async>
    </action>
    '''
    #print tempapi.exportTemplate('aaa', action1)
    
    '***********************************************************************************'
    
    tempdiskapi = TemplateDisksAPIs()
    #print tempdiskapi.getDiskIdByName('ov', 't')
    print tempdiskapi.getTemplateDiskInfo('ov', 'osvtest_Disk1')
    copy_data = '''
    <action>
    <storage_domain>
        <name>Data2-ISCSI</name>
    </storage_domain>
    <async>false</async>
    </action>
    '''
    export_data = '''
    <action>
    <storage_domain>
        <name>Data2-ISCSI</name>
    </storage_domain>
    <async>false</async>
    </action>
    '''
    
    delete_data = '''
    <action>
    <storage_domain>
        <id>631cd328-55a5-4e70-9e5d-d86471de8ce7</id>
    </storage_domain>
    <async>false</async>
    <force>true</force>
    </action>
    '''
    #print tempdiskapi.copyTemplateDisk('ov', 'osvtest_Disk1',copy_data ) 
    #print tempdiskapi.exportTemplateDisk('ov', 'osvtest_Disk1', export_data) (fail)
    #print tempdiskapi.deleteTemplateDisk('temp', 'VM1_Disk1',delete_data)    (fail) 
    tempnicapi = TemplateNicsAPIs()
    
    nic_data='''
    <nic>
    <name>nic4</name>
    </nic>
    '''
    #print tempnicapi.getTemplateNicList('temp')
    #print tempnicapi.getNicIdByName('temp', 'nic5')
    #print tempnicapi.createTemplateNic('temp1', nic_data)
    #print tempnicapi.updateTemplateNic('temp','nic2', nic_data)
    #print tempnicapi.deleteTemplateNic('temp', 'nic')   


    
    
    