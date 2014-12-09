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

'''---------------------------------------------------------------------------------------------------
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
---------------------------------------------------------------------------------------------------'''
vm_id = VirtualMachineAPIs().getVmIdByName(ModuleData.vm_name)
temp_name = ['Template1-ITC0701030101','Template2_ITC0701030101','Template3.ITC0701030101','TEMPLATE4-ITC0701030101','123456']
temp_info='''
<data_driver>
    <template>
        <name>%s</name>
        <vm id="%s"/>
    </template>
    <template>
        <name>%s</name>
        <vm id="%s"/>
    </template>
    <template>
        <name>%s</name>
        <vm id="%s"/>
    </template>
    <template>
        <name>%s</name>
        <vm id="%s"/>
    </template>
    <template>
        <name>%s</name>
        <vm id="%s"/>
    </template>
</data_driver>
''' % (temp_name[0], vm_id, \
       temp_name[1], vm_id, \
       temp_name[2], vm_id, \
       temp_name[3], vm_id, \
       temp_name[4], vm_id)

'''---------------------------------------------------------------------------------------------------
@note: ExpectedData
---------------------------------------------------------------------------------------------------'''
expected_status_code = 202

