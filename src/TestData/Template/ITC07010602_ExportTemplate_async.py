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
temp_name = 'Template-ITC07010602'
temp_info='''
<template>
    <name>%s</name>
    <vm id="%s"/>
</template>
''' % (temp_name, vm_id)

action='''
<action>
    <async>true</async>
</action>
'''

'''---------------------------------------------------------------------------------------------------
@note: ExpectedData
---------------------------------------------------------------------------------------------------'''
expected_status_code = 202