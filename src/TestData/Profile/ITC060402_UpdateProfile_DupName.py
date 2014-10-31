#encoding:utf-8

from TestAPIs.DataCenterAPIs import DataCenterAPIs
nw_name = 'network001'
dc_name = 'Default'
dc_id = DataCenterAPIs().getDataCenterIdByName(dc_name)

'''
@note: PreData
'''
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/>    
</network>
''' %(nw_name,dc_id)

profile_name1 = 'p001'
profile_name2 = 'p002'
profile_info1 = '''
    <vnic_profile>
        <name>p001</name>
        <description>shelled</description>
        <network id="%s"/>
    </vnic_profile>
'''
profile_info2 = '''
    <vnic_profile>
        <name>p002</name>
        <description>shelled</description>
        <network id="%s"/>
    </vnic_profile>
'''
'''
@note: TestData
'''
update_info = '''
<vnic_profile>
        <name>p002</name>
        <description>shelled</description>
        <port_mirroring>true</port_mirroring>
    </vnic_profile>
'''

'''
@note: ExpectedData
'''
expected_status_code = 409
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot edit VM network interface profile. The VM network interface profile's name is already used by an existing profile for the same network.
-Please choose a different name.]</detail>
</fault>
'''

