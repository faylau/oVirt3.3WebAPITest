#encoding:utf-8

__authors__ = ['wei keke']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                         
#---------------------------------------------------------------------------------
'''

import TestData.Network.ITC06_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs




'''
@note: TestData
nw_name_list[0]：含有特殊字符
nw_name_list[1]：16个字符（刚好超过15个）
'''
dc_name = ModuleData.dc_name
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
nw_name_list = ['Network-1*#*', 
                'network123456789NETWORK']

nw_info = '''
<data_driver>
    <network>
        <name>%s</name>
        <data_center id= "%s"/>    
    </network>
    <network>
        <name>%s</name>
        <data_center id= "%s"/>    
    </network>
</data_driver>
'''%(nw_name_list[0],dc_id,nw_name_list[1],dc_id)

'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info_list = [
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Network name must be 1-15 long and can contain only 'A-Z', 'a-z', '0-9', '_' characters]</detail>
</fault>
'''
,
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Network name must be 1-15 long and can contain only 'A-Z', 'a-z', '0-9', '_' characters]</detail>
</fault>
'''
                      
]