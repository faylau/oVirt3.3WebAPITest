#encoding:utf-8



from Configs.GlobalConfig import Hosts, DataStorages, IsoStorages, ExportStorages
from TestData.Volume import ITC10_SetUp as ModuleData
from TestAPIs.HostAPIs import HostAPIs
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.TemplatesAPIs import TemplatesAPIs
from TestData.VirtualMachine.ITC05010502_DelVm_WithoutDisk import disk_alias
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs
'''
---------------------------------------------------------------------------------------------------
@note: ModuleTestData
---------------------------------------------------------------------------------------------------
'''

########################################################################
# 集群名称和两个主机id                                                                                                                                  
########################################################################
cluster_name = ModuleData.cluster_nfs_name
host1_name = ModuleData.host1_name
host2_name = ModuleData.host2_name
host1_id = HostAPIs().getHostIdByName(host1_name)
host2_id = HostAPIs().getHostIdByName(host2_name)


########################################################################
# 主机的gluster存储目录                                                                                                                       
########################################################################


dir_list = ['/storage/d1','/storage/dd2','/storage/d3','/storage/d4']
'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
----
-----------------------------------------------------------------------------------------------
'''
#卷信息
xml_volume_dis = '''
    <gluster_volume>
    <name>dis</name>
    <volume_type>distribute</volume_type>
    <bricks>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
    </bricks>
    </gluster_volume>
    '''%(host2_id, dir_list[0])
xml_volume_rep = '''
    <gluster_volume>
    <name>rep</name>
    <volume_type>replicate</volume_type>
    <replica_count>2</replica_count>
    <bricks>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
    </bricks>
    </gluster_volume>
    '''%(host1_id, dir_list[1], host2_id, dir_list[1])
xml_volume_disrep = '''
    <gluster_volume>
    <name>disrep</name>
    <volume_type>distributed_replicate</volume_type>
    <replica_count>2</replica_count>
    <bricks>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
    </bricks>
    </gluster_volume>
    '''%(host1_id, dir_list[2], host2_id, dir_list[2], host1_id, dir_list[3], host2_id, dir_list[3])
#数据域相关信息
sd_name= 'gluster-ITC1001'
dc_name =  ModuleData.dc_nfs_name
xml_sd_info = '''
<storage_domain>
        <name>%s</name>
        <type>data</type>
        <host id="%s"/>
        <storage>
            <type>glusterfs</type>
            <path>10.1.123.17:disrep</path>
            <vfs_type>glusterfs</vfs_type>    
        </storage>
</storage_domain>
'''%(sd_name, host1_id)

#虚拟机信息
vm_name = 'vm-ITC1001'
cluster_id = ClusterAPIs().getClusterIdByName(ModuleData.cluster_nfs_name)
template_id = TemplatesAPIs().getTemplateIdByName('Blank')
xml_vm_info='''
<vm>
    <name>%s</name>
    <description>Test for ITC1001</description>
    <type>server</type>
    <memory>536870912</memory>
    <cluster id="%s"/>
    <template id="%s"/>
    <cpu>
        <topology sockets="1" cores="1"/>
    </cpu>
    <os type="NKAS6x64">
        <boot dev="hd"/>
    </os>
    <high_availability>
        <enabled>true</enabled>
        <priority>50</priority>
    </high_availability>
    <display>
        <type>vnc</type>
        <monitors>1</monitors>
        <smartcard_enabled>true</smartcard_enabled>
    </display>
    <stateless>false</stateless>
    <placement_policy>
        <affinity>migratable</affinity>
    </placement_policy>
    <memory_policy>
        <guaranteed>536870912</guaranteed>
    </memory_policy>
    <usb>
        <enabled>false</enabled>
    </usb>
</vm>
''' % (vm_name, cluster_id, template_id)
#虚拟机磁盘信息
disk_alias = 'disk-ITC1001'
sd_id = StorageDomainAPIs().getStorageDomainIdByName(sd_name)
xml_disk_info = '''
<disk>
    <name>%s</name>
    <storage_domains>
        <storage_domain id = "%s"/>
    </storage_domains>
    <size>1059061760</size>
    <sparse>false</sparse>
    <interface>virtio</interface>
    <format>raw</format>
    <bootable>true</bootable>
    <shareable>false</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
'''%(disk_alias, sd_id)

#模板信息
base_temp_name = 'temp_ITC1001'
temp_name = 'temp_ITC1001'
vm_id = VirtualMachineAPIs().getVmIdByName(vm_name)
temp_info = '''
<template>
        <name>%s</name>
        <vm id="%s"/>
    </template>
'''%(base_temp_name, vm_id)
base_temp_id = TemplatesAPIs().getTemplateIdByName(base_temp_name)
zi_temp_info = '''
<template>
        <name>%s</name>
        <vm id="%s"/>
        <version>
            <base_template id="%s"/>
            <version_name>%s</version_name>
        </version>
    </template>
'''%(temp_name, vm_id, base_temp_id,temp_name)
'''
---------------------------------------------------------------------------------------------------
@note: Post Test
---------------------------------------------------------------------------------------------------
'''
xml_del_sd_option='''
<storage_domain>
    <host>
        <name>%s</name>
    </host>
    <format>true</format>
</storage_domain>
'''%host1_name
'''
---------------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------------
'''
expected_status_code_create_volume = 201
expected_status_code_delete_volume = 201
expected_status_code_start_volume = 200
expected_status_code_stop_volume = 200
expected_status_code_create_sd = 201
expected_status_code_del_cluster = 200

