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
nic_name1 = 'nic-ITC05-1'
nic_name2 = 'nic-ITC05-2'
nic_info1='''
<nic>
    <name>%s</name>
    <mac address="00:1a:4a:16:84:17"/>
</nic>
'''%(nic_name1)
nic_info2='''
<nic>
    <name>%s</name>
    <mac address="00:1a:4a:16:84:18"/>
</nic>
'''%(nic_name2)
'''
@note: Test-Data
'''
update_vm_nic_info='''
<nic>
    <mac address="00:1a:4a:16:84:18"/>
</nic>
'''


'''
@note: ExpectedData
'''
expected_status_code = 409
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[MAC Address is already in use.]</detail>
</fault>
'''
