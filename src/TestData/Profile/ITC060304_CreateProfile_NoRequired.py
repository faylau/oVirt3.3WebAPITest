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
