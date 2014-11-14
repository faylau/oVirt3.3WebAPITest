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
    <plugged>true</plugged>
</nic>
'''%(nic_name)

'''
@note: ExpectedData
'''
expected_status_code = 200
