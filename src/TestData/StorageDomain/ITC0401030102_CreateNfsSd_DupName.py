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
data1 = DataStorages['nfs']['data2']
data1_ip = data1['ip']
data1_path = data1['path']

'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''
data1_name = ModuleData.data1_nfs_name
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
@note: Post-Test-Data
-------------------------------------------------------------------------------------------------
'''


'''
-------------------------------------------------------------------------------------------------
@note: ExpectedResult
-------------------------------------------------------------------------------------------------
'''
expected_status_code_create_sd_dup_name = 409
expected_info_create_sd_dup_name = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add Storage. The Storage Domain name is already in use.]</detail>
</fault>
'''