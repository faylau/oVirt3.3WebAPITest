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

#虚拟机信息
vm_name = 'vm-ITC1003'
cluster_id = ClusterAPIs().getClusterIdByName('Cluster-ITC05-NFS')
template_id = TemplatesAPIs().getTemplateIdByName('Blank')
#使用blank模板创建虚拟机xml
xml_vm_info='''
<vm>
    <name>%s</name>
    <description>Test for ITC1003</description>
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
vm_id = VirtualMachineAPIs().getVmIdByName(vm_name)
#模板信息
temp_name = 'temp_ITC1003'
version_name1 = 'version1'
version_name2 = 'version2'
xml_temp_info = '''
<template>
        <name>temp_ITC1003</name>
        <vm id="%s"/>
</template>
'''

base_temp_id = TemplatesAPIs().getTemplateIdByName(temp_name)
xml_zi_temp_info1 = '''
<template>
        <name>temp_ITC1003</name>
        <vm id="%s"/>
        <version>
            <base_template id="%s"/>
            <version_name>%s</version_name>
        </version>
    </template>
'''%(vm_id,base_temp_id,version_name1)
xml_zi_temp_info2 = '''
<template>
        <name>%s</name>
        <vm id="%s"/>
        <version>
            <base_template id="%s"/>
            <version_name>%s</version_name>
        </version>
    </template>
'''%(temp_name, vm_id, base_temp_id,version_name2)
#使用非blank模板的最新版本创建虚拟机
vm_name_new = 'vm-ITC1003-newest'
xml_vm_info_temp = '''
<vm>
    <name>%s</name>
    <description>Test for ITC1003</description>
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
    <stateless>true</stateless>
    <use_latest_template_version>true</use_latest_template_version>
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
'''% (vm_name_new, cluster_id, base_temp_id)

nic_name = 'nic-ITC1003'
nic_info = '''
<nic>
    <name>%s</name>
</nic>
'''%(nic_name)
'''
---------------------------------------------------------------------------------------------------
@note: Post Test
---------------------------------------------------------------------------------------------------
'''

'''
---------------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------------
'''

status_code_update_vm = 201

