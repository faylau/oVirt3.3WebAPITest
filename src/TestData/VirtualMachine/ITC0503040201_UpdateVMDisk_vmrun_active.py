#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
import TestData.VirtualMachine.ITC05_SetUp as ModuleData
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''
disk_name = 'DISK-1%s'%ModuleData.vm_name
sd_id = StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data1_nfs_name)
disk_info='''
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
    <shareable>true</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
'''%(disk_name,sd_id)

'''
@note: TestData
'''
sd_id_new = StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data2_nfs_name)
disk_name_new = 'DISK-1-NEW%s'%ModuleData.vm_name
update_disk_info='''
<disk>
    <name>%s</name>
    <interface>ide</interface>
    <shareable>false</shareable>
</disk>
'''%(disk_name_new)
'''
@note: ExpectedData
'''
expected_status_code = 409
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot edit Virtual Machine Disk. At least one of the VMs is not down.]</detail>
</fault>

'''