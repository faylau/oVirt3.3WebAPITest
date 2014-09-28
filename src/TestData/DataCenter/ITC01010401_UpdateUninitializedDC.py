#encoding:utf-8


'''
@PreData
'''
pre_dc_name = 'DC-ITC01010401-1'
pre_dc_info = '''
    <data_center>
        <name>%s</name>
        <storage_type>nfs</storage_type>
        <version minor="1" major="3"/>
    </data_center>
''' % pre_dc_name


'''
@note: TestData
'''

test_dc_name = 'DC-ITC01010401-2'
test_dc_info = '''
    <data_center>
        <name>%s</name>
        <storage_type>iscsi</storage_type>
        <version minor="3" major="3"/>
    </data_center>
''' % test_dc_name

'''
@note: ExpectedResult
'''
expected_status_code = 200
expected_info = '''

'''