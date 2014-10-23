#encoding:utf-8
import xmltodict

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
@note: Pre-Test-Data
'''
data_storage_name = ModuleData.data1_nfs_name
xml_data_storage_info = {}
xml_data_storage_info['storage_domain'] = xmltodict.parse(ModuleData.xml_datas_info)['data_driver']['storage_domain'][0]

'''
@note: Test-Data
'''


'''
@note: Post-Test-Data
'''


'''
@note: ExpectedResult
'''
expected_statsu_code_get_sd_info = 200