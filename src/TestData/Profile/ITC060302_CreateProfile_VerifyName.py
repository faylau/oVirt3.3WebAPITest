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
