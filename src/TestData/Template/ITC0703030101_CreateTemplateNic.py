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

from TestData.Template import ITC07_SetUp as ModuleData
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs

'''---------------------------------------------------------------------------------------------------
@note: PreData
---------------------------------------------------------------------------------------------------'''
vm_id = VirtualMachineAPIs().getVmIdByName(ModuleData.vm_name)
temp_name = 'Template-ITC0703030101'
temp_info='''
<template>
    <name>%s</name>
    <vm id="%s"/>
</template>
''' % (temp_name, vm_id)

'''---------------------------------------------------------------------------------------------------
@note: TestData
---------------------------------------------------------------------------------------------------'''
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
''' % (nic_name[0], nic_name[1], nic_name[2])

'''---------------------------------------------------------------------------------------------------
@note: ExpectedData
---------------------------------------------------------------------------------------------------'''
expected_status_code = 201