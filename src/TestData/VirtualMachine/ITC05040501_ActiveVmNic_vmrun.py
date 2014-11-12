#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestAPIs.ProfilesAPIs import ProfilesAPIs
from TestAPIs.NetworkAPIs import NetworkAPIs
import TestData.VirtualMachine.ITC05_SetUp as ModuleData
'''
@note: PreData
'''
'''
@note: 这里使用数据中心自带的ovirtmgmt/ovirtmgmt配置集
'''
nic_name = 'nic-ITC05'
sd_id = StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data1_nfs_name)
nw_id= NetworkAPIs().getNetworkIdByName('ovirtmgmt', ModuleData.dc_nfs_name)
pro_id = ProfilesAPIs().getProfileIdByName('ovirtmgmt', nw_id)
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
@note: ExpectedData
'''
expected_status_code = 200
