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
vm_name = "vm-ITC05020501"
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
    <placement_policy>
        <affinity>pinned</affinity>
    </placement_policy>
</vm>
''' % (vm_name, ModuleData.cluster_nfs_name)

# 前提2：创建磁盘的信息
disk_alias = 'disk-ITC05020501'
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

# 前提3：创建主机的信息
host2 = Hosts['node1']
host2_name = 'node-ITC05020501'
host2_ip = host2['ip']
host2_password = host2['password']
xml_host2_info = '''
    <host>
        <cluster>
            <name>%s</name>
        </cluster>
        <name>%s</name>
        <address>%s</address>
        <root_password>%s</root_password>
    </host>
''' % (ModuleData.cluster_nfs_name, host2_name, host2_ip, host2_password)


'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
---------------------------------------------------------------------------------------------------
'''
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
xml_del_host_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''



'''
---------------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------------
'''
expected_status_code_migrate_vm_not_allow = 409
expected_info_migrate_vm_not_allow = '''
<action>
    <status>
        <state>failed</state>
    </status>
    <fault>
        <reason>Operation Failed</reason>
        <detail>[Cannot migrate VM. VM is pinned to Host.]</detail>
    </fault>
</action>
'''

