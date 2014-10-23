#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestData.Template import ITC07_SetUp as ModuleData
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''

vm_id = VirtualMachineAPIs().getVmIdByName(ModuleData.vm_name)
temp_name = 'template-ke'
temp_info='''
<template>
    <name>template-ke</name>
    <vm id="%s"/>
</template>
'''%vm_id

'''
@note: TestData
'''
nic_data='''
<nic>

</nic>
'''

'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info='''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>NIC [name] required for add</detail>
</fault>
'''

