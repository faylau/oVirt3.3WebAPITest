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


'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''
host_id = HostAPIs().getHostIdByName(ModuleData.host1_name)
data1 = DataStorages['nfs']['data1']
data1_ip = data1['ip']
data1_path = data1['path']
sd_name_list = ['~!@#$']
sd_info_list = '''
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
''' % (sd_name_list[0], host_id, data1_ip, data1_path)

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
expected_status_code_create_sd_incorrect_name = 400
expected_info_create_sd_incorrect_name = '''

'''
expected_status_code_del_sd = 200