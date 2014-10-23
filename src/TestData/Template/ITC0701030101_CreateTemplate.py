#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestData.Template import ITC07_SetUp as ModuleData
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs
'''
@note: TestData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''

vm_id = VirtualMachineAPIs().getVmIdByName(ModuleData.vm_name)
temp_name = ['template-ke','template_ke','template.ke','TEMPLATE','123456']
temp_info='''
<data_driver>
<template>
    <name>template-ke</name>
    <vm id="%s"/>
</template>
<template>
    <name>template_ke</name>
    <vm id="%s"/>
</template>
<template>
    <name>template.ke</name>
    <vm id="%s"/>
</template>
<template>
    <name>TEMPLATE</name>
    <vm id="%s"/>
</template>
<template>
    <name>123456</name>
    <vm id="%s"/>
</template>
</data_driver>
'''%(vm_id,vm_id,vm_id,vm_id,vm_id)
'''
@note: ExpectedData
'''
expected_status_code = 202

