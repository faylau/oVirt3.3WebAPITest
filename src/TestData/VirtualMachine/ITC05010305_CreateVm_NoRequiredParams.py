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

from TestData.VirtualMachine import ITC05_SetUp as ModuleData

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
# 虚拟机名称
vm1_name = ''
vm2_name = 'vm-ITC05010305-2'
vm3_name = 'vm-ITC05010305-3'

# vm1缺少name
xml_vm1_info = '''
<vm>
    <name>%s</name>
    <cluster><name>%s</name></cluster>
    <template><name>Blank</name></template>
</vm>
''' % (vm1_name, ModuleData.cluster_nfs_name)

# vm2缺少cluster
xml_vm2_info = '''
<vm>
    <name>%s</name>
    <cluster><name></name></cluster>
    <template><name>Blank</name></template>
</vm>
''' % vm2_name

# vm3缺少template
xml_vm3_info = '''
<vm>
    <name>%s</name>
    <cluster><name>%s</name></cluster>
    <template><name></name></template>
</vm>
''' % (vm3_name, ModuleData.cluster_nfs_name)


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
expected_status_code_create_vm_no_name = 400
expected_status_code_create_vm_no_cluster = 400
expected_status_code_create_vm_no_template = 400
expected_status_code_list = [expected_status_code_create_vm_no_name, expected_status_code_create_vm_no_cluster, expected_status_code_create_vm_no_template]

expected_info_create_vm1 = '''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>VM [name] required for add</detail>
</fault>
'''
expected_info_create_vm2 = '''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>VM [cluster.id|name] required for add</detail>
</fault>
'''
expected_info_create_vm3 = '''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>VM [template.id|name] required for add</detail>
</fault>
'''
expected_info_list = [expected_info_create_vm1, expected_info_create_vm2, expected_info_create_vm3]