#encoding:utf-8
from TestAPIs.DataCenterAPIs import DataCenterAPIs
nw_name = 'network001'
dc_name = 'Default'
dc_id = DataCenterAPIs().getDataCenterIdByName(dc_name)
profile_name = 'p001'

'''
@note: PreData
'''
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/>    
</network>
''' %(nw_name,dc_id)


profile_info = '''
    <vnic_profile>
        <name>p001</name>
        <description>shelled</description>
        <network id="%s"/>
        <port_mirroring>false</port_mirroring>
    </vnic_profile>
'''

'''
@note: ExpectedData
'''
expected_status_code = 201
