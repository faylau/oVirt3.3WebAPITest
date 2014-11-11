#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
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
    <vnic_profile id="6f1bff46-d0aa-49d2-9206-0bc9a4adf6aa"/>
    <interface>virtio</interface>
    <linked>false</linked>
</nic>
'''

'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info = '''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>NIC [name] required for add</detail>
</fault>
'''

