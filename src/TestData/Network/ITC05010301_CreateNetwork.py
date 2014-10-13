#encoding:utf-8

nw_name = 'network001'
dc_name = 'Default'


'''
@note: TestData
'''
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>    
</network>
''' %nw_name

'''
@note: ExpectedData
'''
expected_status_code = 201