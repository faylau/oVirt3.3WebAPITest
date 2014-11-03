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
expected_status_code_create_vm_no_cluster = 404
expected_status_code_create_vm_no_template = 404
expected_status_code_list = [expected_status_code_create_vm_no_name, expected_status_code_create_vm_no_cluster, expected_status_code_create_vm_no_template]

expected_info_create_vm1 = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Can not add VM. The given name contains special characters. Only lower-case and upper-case letters, numbers, '_', '-', '.' are allowed., size must be between 1 and 255]</detail>
</fault>
'''
expected_info_create_vm2 = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>Entity not found: Cluster: name=</detail>
</fault>
'''
expected_info_create_vm3 = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>Entity not found: Template: name=</detail>
</fault>
'''
expected_info_list = [expected_info_create_vm1, expected_info_create_vm2, expected_info_create_vm3]