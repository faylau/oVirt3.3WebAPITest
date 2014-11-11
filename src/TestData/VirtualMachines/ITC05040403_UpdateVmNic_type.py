#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestAPIs.ProfilesAPIs import ProfilesAPIs
from TestAPIs.NetworkAPIs import NetworkAPIs
import TestData.VirtualMachines.ITC05_SetUp as ModuleData
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''
nic_name = 'nic-ITC05'
sd_id = StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data1_nfs_name)

nic_info='''
<nic>
    <name>%s</name>
    <interface>virtio</interface>
    <linked>false</linked>
    <plugged>false</plugged>
</nic>
'''%(nic_name)
disk_name = 'disk-ITC05'
disk_info='''
<disk>
    <alias>%s</alias>
    <name>%s</name>
    <storage_domains>
        <storage_domain id = "%s"/>
    </storage_domains>
    <size>1059061760</size>
    <sparse>false</sparse>
    <interface>virtio</interface>
    <format>raw</format>
    <bootable>true</bootable>
    <shareable>true</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
'''%(disk_name,disk_name,sd_id)
'''
@note: Test-Data
'''
update_vm_nic_info='''
<nic>
    <interface>e1000</interface>
</nic>
'''


'''
@note: ExpectedData
'''
expected_status_code = 200
