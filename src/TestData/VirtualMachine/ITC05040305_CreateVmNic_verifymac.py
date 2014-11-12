#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
import TestData.VirtualMachine.ITC05_SetUp as ModuleData
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''
nic_name = 'nic_ITC05'
sd_id = StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data1_nfs_name)
nic_info='''
<nic>
    <name>%s</name>
    <mac address="00:1a:4a:16:84:"/>
</nic>
'''%nic_name

'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[MAC address must be in format "HH:HH:HH:HH:HH:HH" where H is a hexadecimal character (either a digit or A-F, case is insignificant).]</detail>
</fault>
'''

