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
temp_name = 'template#'
temp_info='''
<template>
    <name>%s</name>
    <vm id="%s"/>
</template>
'''%(temp_name,vm_id)
'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Can not add Template. The given name contains special characters. Only lower-case and upper-case letters, numbers, '_', '-', '.' are allowed.]</detail>
</fault>
'''

