#encoding:utf-8
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
'''
@note: PreData
'''
'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''
vm_name = 'vm3'
vm_info='''
<vm>
        <name>vm3</name>
        <description>Virtual Machine 2</description>
        <type>server</type>
        <memory>536870912</memory>
        <cluster>
            <name>Cluster-ISCSI</name>
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
'''
disk_name = 'testkeke'
disk_info='''
<disk>
    <alias>testkeke</alias>
    <name>testkeke</name>
    <storage_domains>
        <storage_domain>
            <name>Data1-ISCSI</name>
        </storage_domain>
    </storage_domains>
    <size>114748364</size>
    <sparse>false</sparse>
    <interface>virtio</interface>
    <format>raw</format>
    <bootable>true</bootable>
    <shareable>false</shareable>
    <wipe_after_delete>false</wipe_after_delete>
</disk>
'''
'''
@note: 目标存储域由环境初始化时获得，这里先定义变量
'''
sd_id = '2170acd2-6fd0-4e88-a566-293a20fca97a'
temp_name = 'template-ke'
temp_info='''
<template>
    <name>template-ke</name>
    <vm id="%s">
        <disks>
            <disk id="%s">
            <storage_domains>
                <storage_domain id="%s"/>  
            </storage_domains>
            </disk>
        </disks>
    </vm>
</template>
'''
'''
@note: ExpectedData
'''
expected_status_code = 202

