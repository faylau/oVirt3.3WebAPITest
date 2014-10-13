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
<data_driver>
    <vnic_profile>
        <name>p001#</name>
        <description>shelled</description>
        <network id="%s"/>
        <port_mirroring>false</port_mirroring>
    </vnic_profile>
    <vnic_profile>
        <name>p00&</name>
        <description>shelled</description>
        <network id="%s"/>
        <port_mirroring>false</port_mirroring>
    </vnic_profile>
</data_driver>
'''
'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info_list = [
''' 
<fault>
    <reason>Operation Failed</reason>
    <detail>[Name must be formed of alphanumeric characters, numbers or "-_".]</detail>
</fault>
'''
]
