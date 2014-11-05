#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestAPIs.ProfilesAPIs import ProfilesAPIs
from TestAPIs.NetworkAPIs import NetworkAPIs
import TestData.VirtualMachines.ITC05_SetUp as ModuleData
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
nic_info_noproid='''
<nic>
    <name>%s</name>
</nic>
'''%(nic_name)
nic_info_proid='''
<nic>
    <name>%s</name>
    <vnic_profile id ="%s"/>
</nic>
'''%(nic_name,pro_id)
'''
@note: ExpectedData
'''
expected_status_code = 201
