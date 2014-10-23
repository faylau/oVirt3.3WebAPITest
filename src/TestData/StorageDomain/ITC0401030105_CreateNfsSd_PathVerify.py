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
sd_name = 'data1-ITC0401030105'
sd = DataStorages['nfs']['data2']
sd_ip = sd['ip']
sd_path_list = [':/storage/data2', 'storage/data2']
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
            <path>%s</path>
        </storage>
    </storage_domain>
</data_driver>
''' % (sd_name, host_name, sd_ip, sd_path_list[0],
       sd_name, host_name, sd_ip, sd_path_list[1]
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
expected_status_code_create_sd_fail = 400
expected_info_create_sd_fail = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Mount path is illegal, please use [IP:/path or FQDN:/path] convention.]</detail>
</fault>
'''
expected_status_code_del_sd = 200