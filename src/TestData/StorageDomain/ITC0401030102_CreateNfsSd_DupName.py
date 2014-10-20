#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from Configs.GlobalConfig import DataStorages
from TestData.StorageDomain import ITC04_SetUp as ModuleData
from TestAPIs.HostAPIs import HostAPIs

'''
-------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
-------------------------------------------------------------------------------------------------
'''
data1 = DataStorages['nfs']['data1']
data1_ip = data1['ip']
data1_path = data1['path']
data1_name = 'data1-nfs-ITC0401030102-1'
data1_info_xml = '''
<storage_domain>
    <name>%s</name>
    <type>data</type>
    <host id="%s"/>
    <storage>
        <type>nfs</type>
        <address>%s</address>
        <path>%s</path>
    </storage>
</storage_domain>
''' % (data1_name, HostAPIs().getHostIdByName(ModuleData.host1_name), data1_ip, data1_path)

'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''
data2_info_xml = '''
<storage_domain>
    <name>%s</name>
    <type>data</type>
    <host id="%s"/>
    <storage>
        <type>nfs</type>
        <address>10.1.167.2</address>
        <path>/storage/data2</path>
    </storage>
</storage_domain>
''' % (data1_name, HostAPIs().getHostIdByName(ModuleData.host1_name))

'''
-------------------------------------------------------------------------------------------------
@note: Post-Test-Data
-------------------------------------------------------------------------------------------------
'''
xml_del_sd_option = '''
<storage_domain>
    <host>
        <name>%s</name>
    </host>
    <format>true</format>
    <destroy>false</destroy>
    <async>true</async>
</storage_domain>
''' % ModuleData.host1_name

'''
-------------------------------------------------------------------------------------------------
@note: ExpectedResult
-------------------------------------------------------------------------------------------------
'''
expected_info_create_sd = 201
expected_status_code_create_sd_dup_name = 400
# 实际返回结果中，detail信息显示为空，个人认为是bug。
expected_info_create_sd_dup_name = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add Storage Domain. The Storage Domain name is already in use, please choose a unique name and try again.]</detail>
</fault>
'''
expected_status_code_del_sd = 200