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

from TestData.StorageDomain import ITC04_SetUp as ModuleData
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs

'''
-------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
-------------------------------------------------------------------------------------------------
'''
data1_name = ModuleData.data1_nfs_name
data1_id = StorageDomainAPIs().getStorageDomainIdByName(data1_name)
disk_name = 'disk-ITC04020301-1'
xml_disk_info = '''
<disk>
    <alias>%s</alias>
    <storage_domains>
        <storage_domain id="%s"/>
    </storage_domains>
    <size>105906176</size>
    <interface>virtio</interface>
    <format>cow</format>
</disk>
''' % (disk_name, data1_id)


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
expected_status_code_create_disk = 202
expected_status_code_get_disk_info = 200
expected_status_code_del_disk = 200