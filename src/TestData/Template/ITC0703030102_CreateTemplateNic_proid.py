#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestData.Template import ITC07_SetUp as ModuleData
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs
'''
@note: PreData
'''
'''
@note: 数据中心名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''
dc_name ='DC-ISCSI'
vm_id = VirtualMachineAPIs().getVmIdByName(ModuleData.vm_name)
temp_name = 'template-ke'
temp_info='''
<template>
    <name>template-ke</name>
    <vm id="%s"/>
</template>
'''%vm_id
nic_name = 'nic1'
nic_data='''
<nic>
    <name>nic1</name>
    <vnic_profile id="%s"/>
</nic>
'''
profile_name ='pp'
profile_info = '''
<vnic_profile>
        <name>pp</name>
        <network id="%s"/>
</vnic_profile>
'''
'''
@note: ExpectedData
'''
expected_status_code = 201

