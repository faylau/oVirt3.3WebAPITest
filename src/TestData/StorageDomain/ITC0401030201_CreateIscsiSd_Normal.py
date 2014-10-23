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
data1 = DataStorages['iscsi']['data1-iscsi']
data1_ip = data1['ip']
data1_port = data1['port']
data1_target = data1['target']
data1_lun_id = data1['lun_id']

'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
-------------------------------------------------------------------------------------------------
'''
host_id = HostAPIs().getHostIdByName(ModuleData.host1_name)
data1_name = 'data1-iscsi-ITC0401030201'
data1_info_xml = '''
    <storage_domain>
        <name>%s</name>
        <type>data</type>
        <host id="%s"/>
        <storage>
            <type>iscsi</type>
            <logical_unit id="%s">
                <address>%s</address>
                <port>%s</port>
                <target>%s</target>
                <serial>SLENOVO_LIFELINE-DISK</serial>
                <vendor_id>LENOVO</vendor_id>
                <product_id>LIFELINE-DISK</product_id>
                <lun_mapping>0</lun_mapping>
            </logical_unit>
            <override_luns>true</override_luns>
        </storage>
    </storage_domain>
''' % (data1_name, host_id, data1_lun_id, data1_ip, data1_port, data1_target)

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