#encoding:utf-8
import TestData.Network.ITC05_Setup as ModuleData
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
</network>
''' %(nw_name1,dc_id)

nw_info2 = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/>    
</network>
''' %(nw_name2,dc_id)

'''
@note:TestData 
'''
update_info = '''
<network>
    <name>%s</name>
    <description>lalala</description>   
    <mtu>2000</mtu>
</network>
'''%nw_name2

'''
@note:ExpectedData
'''
expected_status_code = 409
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot edit Network. The logical network's name is already used by an existing logical network in the same data-center.
-Please choose a different name.]</detail>
</fault>
'''