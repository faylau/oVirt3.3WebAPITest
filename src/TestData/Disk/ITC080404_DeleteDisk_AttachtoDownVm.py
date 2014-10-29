#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
import TestData.Disk.ITC08_SetUp as ModuleData
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''
sd_name = ModuleData.data2_nfs_name
cluster_name = ModuleData.cluster_nfs_name
vm_info='''
<vm>
        <name>vm3</name>
        <description>Virtual Machine 2</description>
        <type>server</type>
        <memory>536870912</memory>
        <cluster>
            <name>%s</name>
        </cluster>
        <template>
            <name>Blank</name>
        </template>
        <cpu>
            <topology sockets="2" cores="1"/>
        </cpu>
        <os>
            <boot dev="cdrom"/>
            <boot dev="hd"/>
        </os>
    </vm>
'''%cluster_name
disk_info='''
<disk>
    <alias>testkeke</alias>
    <name>testkeke</name>
    <storage_domains>
        <storage_domain>
            <name>%sCSI</name>
        </storage_domain>
    </storage_domains>
    <size>1147483648</size>
    <sparse>false</sparse>
    <interface>virtio</interface>
    <format>raw</format>
    <bootable>true</bootable>
    <shareable>false</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
'''%sd_name

'''
@note: ExpectedData
'''
expected_status_code = 200

