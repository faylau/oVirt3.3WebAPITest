#encoding:utf-8

__authors__ = ['"Wei Keke" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/09          初始版本                                                            Wei Keke 
#---------------------------------------------------------------------------------
'''

from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
import TestData.Disk.ITC08_SetUp as ModuleData

'''---------------------------------------------------------------------------------------------------
@note: PreData
---------------------------------------------------------------------------------------------------'''
disk_name = 'DISK-ITC080301'
sd_id = StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data1_nfs_name)
disk_info_raw = '''
<disk>
    <alias>%s</alias>
    <name>%s</name>
    <storage_domains>
        <storage_domain id = "%s"/>
    </storage_domains>
    <size>2147483648</size>
    <sparse>false</sparse>
    <interface>virtio</interface>
    <format>raw</format>
    <bootable>true</bootable>
    <shareable>true</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
'''% (disk_name, disk_name, sd_id)

disk_info_cow = '''
<disk>
    <alias>%s</alias>
    <name>%s</name>
    <storage_domains>
        <storage_domain id = "%s"/>
    </storage_domains>
    <size>2147483648</size>
    <sparse>true</sparse>
    <interface>virtio</interface>
    <format>cow</format>
    <bootable>true</bootable>
    <shareable>false</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
'''% (disk_name, disk_name, sd_id)

'''---------------------------------------------------------------------------------------------------
@note: ExpectedData
---------------------------------------------------------------------------------------------------'''
expected_status_code = 202