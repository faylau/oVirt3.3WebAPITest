#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
import TestData.VirtualMachine.ITC05_SetUp as ModuleData
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''
nic_name = 'nic+'
sd_id = StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data1_nfs_name)
nic_info='''
<nic>
    <name>%s</name>
</nic>
'''%nic_name

'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Name must be formed of alphanumeric characters, numbers or "-_.".]</detail>
</fault>
'''

