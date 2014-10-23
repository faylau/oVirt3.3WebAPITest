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

from Configs.GlobalConfig import DataStorages, IsoStorages, ExportStorages
from TestData.StorageDomain import ITC04_SetUp as ModuleData
from TestAPIs.HostAPIs import HostAPIs

'''
-------------------------------------------------------------------------------------------------
@note: Pre-Test-Data
-------------------------------------------------------------------------------------------------
'''
data1 = DataStorages['nfs']['data2']
iso2 = IsoStorages['ISO-Storage2']
export2 = ExportStorages['Export-Storage2']
data1_ip = data1['ip']
data1_path = data1['path']
iso2_ip = iso2['ip']
iso2_path = iso2['path']
export2_ip = export2['ip']
export2_path = export2['path']



'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''
host_id = HostAPIs().getHostIdByName(ModuleData.host1_name)
data1_name = ['data2-nfs-ITC0401030101', 'iso1-ITC0401030101', 'export1-ITC0401030101']
data1_info_xml = '''
<data_driver>
    <storage_domain>
        <name>%s</name>
        <type>data</type>
        <host id="%s"/>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
    <storage_domain>
        <name>%s</name>
        <type>iso</type>
        <host id="%s"/>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
    <storage_domain>
        <name>%s</name>
        <type>export</type>
        <host id="%s"/>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
</data_driver>
''' % (data1_name[0], host_id, data1_ip, data1_path,
       data1_name[1], host_id, iso2_ip, iso2_path, 
       data1_name[2], host_id, export2_ip, export2_path)

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
expected_status_code_create_sd = 201
expected_status_code_del_sd = 200