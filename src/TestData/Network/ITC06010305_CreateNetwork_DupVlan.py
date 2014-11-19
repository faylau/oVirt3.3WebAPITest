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

nw_name1 = 'network001'
nw_name2 = 'network002'
vlan_id = '2'
nw_info1 = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/> 
    <vlan id = "%s"/>
        
</network>
''' %(nw_name1,dc_id,vlan_id)
'''
@note: TestData
'''
nw_info2 = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/> 
    <vlan id = "%s"/>
</network>
''' %(nw_name2,dc_id,vlan_id)
'''
@note: ExpectedData
'''
expected_status_code = 409
expected_info ='''
<fault>
    <reason>Operation Failed</reason>
    <detail>[The specified VLAN ID (%s) is already in use.]</detail>
</fault>
'''%vlan_id
