#coding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/11/04          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from TestData.VirtualMachine import ITC05_SetUp as ModuleData

'''
---------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
---------------------------------------------------------------------------------------------------
'''
vm_name = "vm-ITC05010504"
xml_vm_info='''
<vm>
    <name>%s</name>
    <type>server</type>
    <memory>536870912</memory>
    <cluster>
        <name>%s</name>
    </cluster>
    <template>
        <name>Blank</name>
    </template>
    <cpu>
        <topology sockets="1" cores="1"/>
    </cpu>
    <delete_protected>true</delete_protected>
</vm>
''' % (vm_name, ModuleData.cluster_nfs_name)


'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
---------------------------------------------------------------------------------------------------
'''



'''
---------------------------------------------------------------------------------------------------
@note: Post-Test-Data
---------------------------------------------------------------------------------------------------
'''
xml_vm_update_info = '''
<vm>
    <delete_protected>false</delete_protected>
</vm>
'''

xml_del_vm_force = '''
    <action>
        <force>true</force>
    </action>
'''



'''
---------------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------------
'''
expected_status_code_update_vm = 200
expected_status_code_del_vm_fail = 409
expected_info_del_vm_fail = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot remove VM. Delete protection is enabled. In order to delete, disable Delete protection first.]</detail>
</fault>
'''

