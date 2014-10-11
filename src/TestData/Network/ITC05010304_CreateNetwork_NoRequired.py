#encoding:utf-8

nw_name = 'network001'



'''
@note: TestData
'''
nw_info = '''
<data_driver>
    <network>
        <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>    
    </network>
    <network>
        <name>%s</name>   
    </network>
</data_driver>
'''%nw_name

'''
@note: ExpectedData
'''
expected_status_code = 400
expected_info_list =['''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>Network [name] required for add</detail>
</fault>
'''
,
'''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>Network [dataCenter.name|id] required for add</detail>
</fault>
'''
]
