#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from Configs.GlobalConfig import DataStorages
from TestData.StorageDomain import ITC04_SetUp as ModuleData

'''
-------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
-------------------------------------------------------------------------------------------------
'''


'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''
host_name = ModuleData.host1_name
sd_name = 'data1-ITC0401030106'
sd = DataStorages['nfs']['data1']
sd_ip = sd['ip']
sd_path = sd['path']
xml_sd_info_list = '''
<data_driver>
    <storage_domain>
        <name></name>
        <type>data</type>
        <host>
            <name>%s</name>
        </host>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
    <storage_domain>
        <name>%s</name>
        <type></type>
        <host>
            <name>%s</name>
        </host>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
    <storage_domain>
        <name>%s</name>
        <type>data</type>
        <host>
            <name></name>
        </host>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
    <storage_domain>
        <name>%s</name>
        <type>data</type>
        <host>
            <name>%s</name>
        </host>
        <storage>
            <type></type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
    <storage_domain>
        <name>%s</name>
        <type>data</type>
        <host>
            <name>%s</name>
        </host>
        <storage>
            <type>nfs</type>
            <address></address>
            <path>%s</path>
        </storage>
    </storage_domain>
    <storage_domain>
        <name>%s</name>
        <type>data</type>
        <host>
            <name>%s</name>
        </host>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path></path>
        </storage>
    </storage_domain>
</data_driver>
''' % (host_name, sd_ip, sd_path,
       sd_name, host_name, sd_ip, sd_path,
       sd_name, sd_ip, sd_path,
       sd_name, host_name, sd_ip, sd_path,
       sd_name, host_name, sd_path,
       sd_name, host_name, sd_ip
       )

'''
-------------------------------------------------------------------------------------------------
@note: Post-Test-Data
-------------------------------------------------------------------------------------------------
'''
xml_del_sd_option = '''
<storage_domain>
    <host>
        <name>%s</name>
    </host>
    <format>true</format>
    <destroy>false</destroy>
    <async>true</async>
</storage_domain>
''' % ModuleData.host1_name

'''
-------------------------------------------------------------------------------------------------
@note: ExpectedResult
-------------------------------------------------------------------------------------------------
'''
expected_info_create_sd = 201
expected_info_1 = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[size must be between 1 and 250, Storage Domain name must be formed of "a-z0-9A-Z" or "-_"]</detail>
</fault>
'''
expected_info_2 = '''
<fault>
    <reason>Invalid value</reason>
    <detail>is not a member of StorageDomainType. Possible values for StorageDomainType are: data, iso, export, image</detail>
</fault>
'''
expected_info_3 = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>Entity not found: Hosts: name=</detail>
</fault>
'''
expected_info_4 = '''
<fault>
    <reason>Invalid value</reason>
    <detail>is not a member of StorageType. Possible values for StorageType are: iscsi, fcp, nfs, localfs, posixfs, glusterfs, glance</detail>
</fault>
'''
expected_info_5 = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Mount path is illegal, please use [IP:/path or FQDN:/path] convention.]</detail>
</fault>
'''
expected_info_6 = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Mount path is illegal, please use [IP:/path or FQDN:/path] convention.]</detail>
</fault>
'''
expected_return_info_list = [(400, expected_info_1), (400, expected_info_2), (404, expected_info_3),
                             (400, expected_info_4), (400, expected_info_5), (400, expected_info_6)]

expected_status_code_del_sd = 200