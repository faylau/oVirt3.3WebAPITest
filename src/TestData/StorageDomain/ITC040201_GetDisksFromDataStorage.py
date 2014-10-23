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
host_id = HostAPIs().getHostIdByName(ModuleData.host1_name)
data1_name = 'data1-ITC040201'
xml_data_storage_info = '''
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
''' % (data1_name, host_id, data1_ip, data1_path)

disk_name = 'disk-ITC040201-1'
xml_disk_info = '''
<disk>
    <alias>%s</alias>
    <name>%s</name>
    <storage_domains>
        <storage_domain>
            <name>%s</name>
        </storage_domain>
    </storage_domains>
    <size>105906176</size>
    <interface>virtio</interface>
    <format>cow</format>
</disk>
''' % (disk_name, disk_name, ModuleData.host1_name)


'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''


'''
-------------------------------------------------------------------------------------------------
@note: Post-Test-Data
-------------------------------------------------------------------------------------------------
'''
xml_del_ds_option = '''
    <storage_domain>
        <host id="%s"/>
        <format>true</format>
        <async>false</async>
    </storage_domain>
''' % host_id

xml_del_disk_option = '''
    <action>
        <async>false</async>
    </action>
'''

'''
-------------------------------------------------------------------------------------------------
@note: ExpectedResult
-------------------------------------------------------------------------------------------------
'''
expected_status_code_create_sd = 201
expected_status_code_create_disk = 202
expected_status_code_get_disk_list_in_data_storage = 200
expected_status_code_del_disk = 200
expected_status_code_del_sd = 200