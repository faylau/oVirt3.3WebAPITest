#coding:utf-8


__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/11/02          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from TestData.VirtualMachines import ITC05_SetUp as ModuleData

'''
---------------------------------------------------------------------------------------------
@note: Pre-TestData
---------------------------------------------------------------------------------------------
'''


'''
---------------------------------------------------------------------------------------------
@note: Test-Data
---------------------------------------------------------------------------------------------
'''
# 主机名称：（1）包含特殊字符；（2）超过64个字符.
vm_name_list = ['vm-ITC05010304-~!@#$%^',
                'node-ITC03010304-012345678901234567890123456789012345678901234567'
                ]
xml_vm_info = '''
<data_driver>
    <vm>
        <name>%s</name>
        <memory>536870912</memory>
        <cluster><name>%s</name></cluster>
        <template><name>Blank</name></template>
    </vm>
    <vm>
        <name>%s</name>
        <memory>536870912</memory>
        <cluster><name>%s</name></cluster>
        <template><name>Blank</name></template>
    </vm>
</data_driver>
''' % (vm_name_list[0], ModuleData.cluster_nfs_name,
       vm_name_list[1], ModuleData.cluster_nfs_name)


'''
---------------------------------------------------------------------------------------------
@note: Post-TestData
---------------------------------------------------------------------------------------------
'''



'''
---------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------
'''
expected_status_code_create_vm_invalid_name = 400
expected_info_list = [
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Can not add VM. The given name contains special characters. Only lower-case and upper-case letters, numbers, '_', '-', '.' are allowed.]</detail>
</fault>
''', 
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add VM. The given name is too long.]</detail>
</fault>
'''
]