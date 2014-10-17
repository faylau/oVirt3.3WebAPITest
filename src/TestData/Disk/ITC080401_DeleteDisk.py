#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''
disk_name = 'Test-DISK'
sd_name = 'Data1-ISCSI'
sd_id = StorageDomainAPIs().getStorageDomainIdByName(sd_name)
disk_info='''
<disk>
    <alias>%s</alias>
    <name>%s</name>
    <storage_domains>
        <storage_domain id = "%s"/>
    </storage_domains>
    <size>21474836480</size>
    <sparse>false</sparse>
    <interface>virtio</interface>
    <format>raw</format>
    <bootable>true</bootable>
    <shareable>true</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
'''%(disk_name,disk_name,sd_id)

async1 = '''
<action>
    <async>true</async>
</action>
'''
async2 = '''
<action>
    <async>false</async>
</action>
'''
'''
@note: ExpectedData
'''
expected_status_code = 200
