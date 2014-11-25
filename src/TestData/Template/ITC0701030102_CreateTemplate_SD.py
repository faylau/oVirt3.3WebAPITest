#encoding:utf-8
__authors__ = ['"Wei Keke" <keke.wei@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/09          初始版本                                                            Wei Keke 
#---------------------------------------------------------------------------------
'''
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
sd_name = ModuleData.data1_nfs_name
sd_id = StorageDomainAPIs().getStorageDomainIdByName(sd_name)
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

