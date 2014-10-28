#encoding:utf-8
import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs

'''
@note: PreData
'''
dc_name = ModuleData.dc_name
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)

nw_name1 = 'network001'
nw_name2 = 'network002'
nw_info1 = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/> 
    <vlan id = "2"/>
        
</network>
''' %(nw_name1,dc_id)
'''
@note: TestData
'''
nw_info2 = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/> 
    <vlan id = "2"/>
</network>
''' %(nw_name2,dc_id)
'''
@note: ExpectedData
'''
expected_status_code = 409
expected_info ='''
<fault>
    <reason>Operation Failed</reason>
    <detail>[The specified VLAN ID (2) is already in use.]</detail>
</fault>
'''
