#coding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/24          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from TestData.DataCenter import ITC01_SetUp as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs

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
# 实际上是ModuleData中data1_nfs的信息，用于与接口得到的信息做对比
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_nfs_name)
xml_sd_info = '''
<storage_domain>
    <name>%s</name>
    <data_center id="%s"/>
    <type>data</type>
    <storage>
        <type>nfs</type>
        <address>%s</address>
        <path>%s</path>
    </storage>
</storage_domain>
''' % (ModuleData.data1_nfs_name, dc_id, ModuleData.data1_nfs_ip, ModuleData.data1_nfs_path)

'''
-------------------------------------------------------------------------------------------------
@note: Post-Test-Data
-------------------------------------------------------------------------------------------------
'''

expected_status_code_get_sd_info = 200