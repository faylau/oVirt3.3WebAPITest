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


'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''
data1_name = 'data1-nfs-ITC0401030101'
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
expected_status_code_del_sd = 200