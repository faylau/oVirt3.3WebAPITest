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

from Configs.GlobalConfig import IsoStorages
from TestData.StorageDomain import ITC04_SetUp as ModuleData
from TestAPIs.HostAPIs import HostAPIs

'''
-------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
-------------------------------------------------------------------------------------------------
'''
iso = IsoStorages['ISO-Storage1']
iso_ip = iso['ip']
iso_path = iso['path']
host_id = HostAPIs().getHostIdByName(ModuleData.host1_name)
iso_name = 'iso1-ITC04010601'
xml_iso_info = '''
    <storage_domain>
        <name>%s</name>
        <type>iso</type>
        <host id="%s"/>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
''' % (iso_name, host_id, iso_ip, iso_path)
'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''
xml_destroy_iso_option = '''
<storage_domain>
    <host>
        <name>%s</name>
    </host>
    <destroy>true</destroy>
    <async>false</async>
</storage_domain>
''' % ModuleData.host1_name

'''
-------------------------------------------------------------------------------------------------
@note: Post-Test-Data
-------------------------------------------------------------------------------------------------
'''
xml_import_iso_info = '''
    <storage_domain>
        <type>iso</type>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
        <host id="%s"/>
    </storage_domain>
''' % (iso_ip, iso_path, host_id)

xml_del_iso_option = '''
    <storage_domain>
        <host id="%s"/>
        <format>true</format>
        <async>false</async>
    </storage_domain>
''' % host_id


'''
-------------------------------------------------------------------------------------------------
@note: ExpectedResult
-------------------------------------------------------------------------------------------------
'''
expected_status_code_create_sd = 201
expected_status_code_destroy_sd = 200
expected_status_code_import_sd = 201
expected_status_code_del_sd = 200