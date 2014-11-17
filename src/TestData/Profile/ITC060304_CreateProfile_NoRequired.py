#encoding:utf-8

from TestAPIs.DataCenterAPIs import DataCenterAPIs
from TestData.Profile import ITC06_SetUp as ModuleData

'''
@note: PreData
'''
nw_name = 'network_ITC06'
dc_name = ModuleData.dc_name
dc_id = DataCenterAPIs().getDataCenterIdByName(dc_name)
profile_name = 'profile_ITC06'
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/>    
</network>
''' %(nw_name,dc_id)


'''
@note: TestData
包括三种情况：缺少配置集名称；缺少网络id；网络名称而非id；
'''
profile_info = '''
<data_driver>
    <vnic_profile>
        <description>shelled</description>
    </vnic_profile>
    <vnic_profile>
        <name>p001</name>
        <description>shelled</description>
    </vnic_profile>
    <vnic_profile>
        <name>p001</name>
        <network name="aaa"/>
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
    <reason>Incomplete parameters</reason>
    <detail>VnicProfile [name, network.id] required for validateParameters</detail>
</fault>

'''
,
'''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>VnicProfile [network.id] required for validateParameters</detail>
</fault>
'''
,
'''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>VnicProfile [network.id] required for validateParameters</detail>
</fault>
'''
]
