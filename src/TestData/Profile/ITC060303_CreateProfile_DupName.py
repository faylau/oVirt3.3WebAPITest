#encoding:utf-8

nw_name = 'network001'
dc_name = 'Default'


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
expected_status_code = 409
expected_info = ''' 
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add VM network interface profile. The VM network interface profile's name is already used by an existing profile for the same network.
-Please choose a different name.]</detail>
</fault>
'''

