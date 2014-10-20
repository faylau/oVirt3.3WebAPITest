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
from TestAPIs.HostAPIs import HostAPIs

'''
-------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
-------------------------------------------------------------------------------------------------
'''
ip_list = ['256.1.1.1',
           'a.1.167.4',
           '10.1.167',
           '10.1.167.4#'
           ]

'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''
host_name = ModuleData.host1_name
sd_name = 'data1-ITC0401030104'
xml_sd_info_list = '''
<data_driver>
    <storage_domain>
        <name>%s</name>
        <type>data</type>
        <host>
            <name>%s</name>
        </host>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>/storage/data1</path>
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
            <path>/storage/data1</path>
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
            <path>/storage/data1</path>
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
            <path>/storage/data1</path>
        </storage>
    </storage_domain>
</data_driver>
''' % (sd_name, host_name, ip_list[0], 
       sd_name, host_name, ip_list[1], 
       sd_name, host_name, ip_list[2],
       sd_name, host_name, ip_list[3])

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
expected_status_code_create_sd_fail = 400
expected_info_create_sd_fail = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Mount path is illegal, please use [IP:/path or FQDN:/path] convention.]</detail>
</fault>
'''
expected_status_code_del_sd = 200