#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestData.Template import ITC07_SetUp as ModuleData
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs,VmDiskAPIs
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''

'''
@note: 目标存储域由环境初始化时获得，这里先定义变量
'''
'''
@note: TestData
'''
sd_id = '2170acd2-6fd0-4e88-a566-293a20fca97a'
vm_id = VirtualMachineAPIs().getVmIdByName(ModuleData.vm_name)
disk_id = VmDiskAPIs().getVmDiskIdByName(ModuleData.vm_name, ModuleData.disk_name)
temp_name = 'template-ke'
temp_info='''
<template>
    <name>template-ke</name>
    <vm id="%s">
        <disks>
            <disk id="%s">
            <storage_domains>
                <storage_domain id="%s"/>  
            </storage_domains>
            </disk>
        </disks>
    </vm>
</template>
'''%(vm_id,disk_id,sd_id)
'''
@note: ExpectedData
'''
expected_status_code = 202

