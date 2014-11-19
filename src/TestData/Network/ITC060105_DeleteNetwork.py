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
@note: PreData
'''
dc_name = ModuleData.dc_name
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
nw_name = 'network001'
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/>    
</network>
''' %(nw_name,dc_id)

'''
@note: ExpectedData
'''
expected_status_code = 200
expected_info = '''
<action>
    <status>
        <state>complete</state>
    </status>
</action>
'''