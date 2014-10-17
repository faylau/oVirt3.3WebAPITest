from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
'''
@note: PreData
'''
disk_name = 'Test-DISK'
sd_name = 'Data1-ISCSI'
sd_id = StorageDomainAPIs().getStorageDomainIdByName(sd_name)
disk_info='''
<data_driver>
<disk>
    <alias>Disk-test</alias>
    <name>Disk-test</name>
    <storage_domains>
        <storage_domain>
            <name>Data1-ISCSI</name>
        </storage_domain>
    </storage_domains>
    <size>105906176</size>
    <sparse>true</sparse>
    <interface>virtio</interface>
    <format>raw</format>
    <bootable>true</bootable>
    <shareable>false</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
<disk>
    <alias>Disk-test</alias>
    <name>Disk-test</name>
    <storage_domains>
        <storage_domain>
            <name>Data1-ISCSI</name>
        </storage_domain>
    </storage_domains>
    <size>105906176</size>
    <sparse>false</sparse>
    <interface>virtio</interface>
    <format>cow</format>
    <bootable>true</bootable>
    <shareable>true</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
<disk>
    <alias>Disk-test</alias>
    <name>Disk-test</name>
    <storage_domains>
        <storage_domain>
            <name>Data1-ISCSI</name>
        </storage_domain>
    </storage_domains>
    <size>105906176</size>
    <sparse>true</sparse>
    <interface>virtio</interface>
    <format>cow</format>
    <bootable>true</bootable>
    <shareable>true</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
</data_driver>
'''
'''
@note: ExpectedData
'''
expected_status_code = [400,400,409]
expected_info_list = [
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add Virtual Machine Disk. Disk configuration (RAW Sparse) is incompatible with the storage domain type.]</detail>
</fault>
'''
,
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add Virtual Machine Disk. Disk configuration (COW Preallocated) is incompatible with the storage domain type.]</detail>
</fault>
'''
,
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add Virtual Machine Disk. Disk's volume format is not supported for shareable disk.]</detail>
</fault>
'''
                      ]
