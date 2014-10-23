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
data = DataStorages['iscsi']['data1-iscsi']
data_ip = data['ip']
data_port = data['port']
data_target = data['target']
data_lun_id = data['lun_id']
host_id = HostAPIs().getHostIdByName(ModuleData.host1_name)
data_name = 'data1-iscsi-ITC0401050201'
xml_data_info = '''
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
''' % (data_name, host_id, data_lun_id, data_ip, data_port, data_target)
'''
-------------------------------------------------------------------------------------------------
@note: Test-Data
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
@note: Post-Test-Data
-------------------------------------------------------------------------------------------------
'''


'''
-------------------------------------------------------------------------------------------------
@note: ExpectedResult
-------------------------------------------------------------------------------------------------
'''
expected_status_code_create_sd = 201
expected_status_code_del_sd = 200