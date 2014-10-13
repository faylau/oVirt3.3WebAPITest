#encoding:utf-8

nw_name = 'network001'
dc_name = 'Default'
profile_name = 'p001'

'''
@note: PreData
'''
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>    
</network>
''' %nw_name

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
expected_status_code = 200
