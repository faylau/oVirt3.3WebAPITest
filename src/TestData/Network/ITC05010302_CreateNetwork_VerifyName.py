#encoding:utf-8

'''
@note: TestData
nw_name_list[0]：含有特殊字符
nw_name_list[1]：16个字符（刚好超过15个）
'''

nw_name_list = ['Network-1*#*', 
                'network123456789NETWORK']

nw_info = '''
<data_driver>
    <network>
        <name>%s</name>
        <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>    
    </network>
    <network>
        <name>%s</name>
        <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>    
    </network>
</data_driver>
'''%(nw_name_list[0],nw_name_list[1])

'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info_list = [
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Network name must be 1-15 long and can contain only 'A-Z', 'a-z', '0-9', '_' characters]</detail>
</fault>
'''
,
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Network name must be 1-15 long and can contain only 'A-Z', 'a-z', '0-9', '_' characters]</detail>
</fault>
'''
                      
]