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
data = DataStorages['nfs']['data2']
data_ip = data['ip']
data_path = data['path']
host_id = HostAPIs().getHostIdByName(ModuleData.host1_name)
data_name = 'data2-nfs-ITC0401040101'
xml_data_info = '''
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
''' % (data_name, host_id, data_ip, data_path)
'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''
data_name_new = 'data2-nfs-ITC0401040101-new'
xml_data_info_new = '''
<storage_domain>
    <name>%s</name>
</storage_domain>
''' % data_name_new

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
expected_status_code_create_sd = 201
expected_status_code_edit_sd_unattached = 409
expected_info_edit_sd_unattached = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot edit Storage. The relevant Storage Domain is inaccessible.
-Please handle Storage Domain issues and retry the operation.]</detail>
</fault>
'''
expected_status_code_del_sd = 200