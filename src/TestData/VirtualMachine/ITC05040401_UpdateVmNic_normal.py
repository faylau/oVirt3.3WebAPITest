#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestAPIs.ProfilesAPIs import ProfilesAPIs
from TestAPIs.NetworkAPIs import NetworkAPIs
import TestData.VirtualMachine.ITC05_SetUp as ModuleData
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
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
    <mac address="00:1a:4a:16:84:07"/>
</nic>
'''%(nic_name)

'''
@note: Test-Data
'''
new_nic_name = 'nic-ITC05-NEW'
update_vm_nic_info='''
<nic>
    <name>%s</name>
    <vnic_profile id = "%s"/>
    <interface>e1000</interface>
    <linked>true</linked>
    <plugged>true</plugged>
    <mac address="00:1a:4a:16:84:07"/>
</nic>
'''%(new_nic_name,pro_id)


'''
@note: ExpectedData
'''
expected_status_code = 200
