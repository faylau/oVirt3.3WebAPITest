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
@note: TestData
---------------------------------------------------------------------------------------------------'''
vm_id = VirtualMachineAPIs().getVmIdByName(ModuleData.vm_name)
temp_name = 'Template-0701030201'
temp_info='''
<template>
    <name>%s</name>
    <vm id="%s"/>
</template>
''' % (temp_name, vm_id)

'''---------------------------------------------------------------------------------------------------
@note: ExpectedData
---------------------------------------------------------------------------------------------------'''
expected_status_code = 400
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add Template. The Template name is already in use, please choose a unique name and try again.]</detail>
</fault>
'''

