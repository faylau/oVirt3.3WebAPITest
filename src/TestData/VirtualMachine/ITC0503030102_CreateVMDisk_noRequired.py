#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
import TestData.VirtualMachine.ITC05_SetUp as ModuleData
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''
disk_name = ['Test-DISK-1','Test-DISK-2','Test-DISK-3','Test-DISK-4']
sd_id = StorageDomainAPIs().getStorageDomainIdByName(ModuleData.data1_nfs_name)
disk_info='''
<data_driver>
<disk>
    <name>%s</name>
    <storage_domains>
        <storage_domain id = "%s"/>
    </storage_domains>
    <size>1059061760</size>
    <sparse>false</sparse>
    <interface>virtio</interface>
    <bootable>true</bootable>
    <shareable>true</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
<disk>
    <name>%s</name>
    <storage_domains>
        <storage_domain id = "%s"/>
    </storage_domains>
    <size>1059061760</size>
    <sparse>false</sparse>
    <format>cow</format>
    <bootable>true</bootable>
    <shareable>false</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
<disk>
    <alias>%s</alias>
    <size>1059061760</size>
    <interface>virtio</interface>
    <format>raw</format>
</disk>
<disk>
    <alias>%s</alias>
    <storage_domains>
        <storage_domain id = "%s"/>
    </storage_domains>
    <interface>virtio</interface>
    <format>raw</format>
</disk>
</data_driver>
'''%(disk_name[0],sd_id,disk_name[1],sd_id,disk_name[2],disk_name[3],sd_id)

'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info_list = [
'''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>Disk [format] required for add</detail>
</fault>
'''
,
'''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>Disk [interface] required for add</detail>
</fault>
'''
,
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add Virtual Machine Disk. Storage Domain doesn't exist.]</detail>
</fault>
'''
,
'''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>Disk [provisionedSize|size] required for add</detail>
</fault>
'''
                      ]
