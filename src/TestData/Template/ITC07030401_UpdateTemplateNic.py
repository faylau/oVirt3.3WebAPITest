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
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''

vm_id = VirtualMachineAPIs().getVmIdByName(ModuleData.vm_name)
temp_name = 'template-ke'
temp_info='''
<template>
    <name>template-ke</name>
    <vm id="%s"/>
</template>
'''%vm_id
'''
@note: PreData
'''
nic_name = 'nic1'
nic_data='''
    <nic>
        <name>%s</name>
    </nic>
'''%nic_name
dc_name = ModuleData.dc_nfs_name
profile_name ='pp'
profile_info = '''
<vnic_profile>
        <name>pp</name>
        <network id="%s"/>
</vnic_profile>
'''
'''
@note: TestData
'''
nic_name_new = 'nic1-new'
update_info = '''
<nic>
    <name>nic1-new</name>
    <vnic_profile id="%s"/>
    <interface>e1000</interface>
    <linked>true</linked>
    <plugged>false</plugged>
</nic>
'''
'''
@note: ExpectedData
'''
expected_status_code = 200

