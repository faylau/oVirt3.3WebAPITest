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
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''

vm_id = VirtualMachineAPIs().getVmIdByName(ModuleData.vm_name)
disk_name = ModuleData.disk_name
temp_name = 'template-ke'
temp_info='''
<template>
    <name>template-ke</name>
    <vm id="%s"/>
</template>
'''%vm_id

'''
@note: TestData
@note: 目标存储域也由Setup用例测试数据提供，这里暂时用字符串代替
'''
des_sd_name = ModuleData.data2_nfs_name
des_sd_id = StorageDomainAPIs().getStorageDomainIdByName(des_sd_name)
copy_data = '''
<action>
    <storage_domain id = "%s"/>
    <async>true</async>
</action> 
'''%des_sd_id
'''
@note: ExpectedData
'''
expected_status_code = 202

