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
nic_name = ['nic1','nic-1','nic_1']
nic_data='''
<data_driver>
    <nic>
        <name>%s</name>
    </nic>
    <nic>
        <name>%s</name>
    </nic>
    <nic>
        <name>%s</name>
    </nic>
</data_driver>
'''%(nic_name[0],nic_name[1],nic_name[2])

'''
@note: ExpectedData
'''
expected_status_code = 201

