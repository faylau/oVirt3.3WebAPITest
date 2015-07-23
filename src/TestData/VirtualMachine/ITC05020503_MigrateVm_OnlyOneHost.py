#coding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/11/05          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from Configs.GlobalConfig import Hosts
from TestData.VirtualMachine import ITC05_SetUp as ModuleData

'''
---------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
---------------------------------------------------------------------------------------------------
'''
# 前提1：创建虚拟机的信息
vm_name = "vm-ITC05020503"
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
</vm>
''' % (vm_name, ModuleData.cluster_nfs_name)

# 前提2：创建磁盘的信息
disk_alias = 'disk-ITC05020503'
xml_disk_info = '''
<disk>
    <alias>%s</alias>
    <storage_domains>
        <storage_domain><name>%s</name></storage_domain>
    </storage_domains>
    <size>1073741824</size>
    <type>system</type>
    <interface>virtio</interface>
    <format>cow</format>
    <bootable>true</bootable>
</disk>
''' % (disk_alias, ModuleData.data1_nfs_name)



'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
---------------------------------------------------------------------------------------------------
'''
# 迁移时自动选择主机
xml_migrate_vm_option = '''
    <action>
        <async>false</async>
    </action>
'''



'''
---------------------------------------------------------------------------------------------------
@note: Post-Test-Data
---------------------------------------------------------------------------------------------------
'''




'''
---------------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------------
'''
expected_status_code_migrate_vm_fail = 409
expected_info_migrate_vm_fail = '''
<action>
    <async>false</async>
    <status>
        <state>failed</state>
    </status>
    <fault>
        <reason>Operation Failed</reason>
        <detail>[Cannot migrate VM. There is no host that satisfies current scheduling constraints. See below for details:]</detail>
    </fault>
</action>
'''


