#encoding:utf-8


'''
@PreData
'''
dc_name_list = ['DC-ITC01010403-1', 'DC-ITC01010403-2']
pre_dc_info = '''
<data_driver>
    <data_center>
        <name>%s</name>
        <storage_type>nfs</storage_type>
        <version minor="1" major="3"/>
    </data_center>
    <data_center>
        <name>%s</name>
        <storage_type>nfs</storage_type>
        <version minor="1" major="3"/>
    </data_center>
</data_driver>
''' % (dc_name_list[0], dc_name_list[1])

'''
@note: TestData
'''
target_dc_name = dc_name_list[1]
test_dc_info = '''
    <data_center>
        <name>%s</name>
    </data_center>
''' % dc_name_list[0]



'''
@note: ExpectedResult
'''
expected_status_code = 409
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot edit Data Center. The Data Center name is already in use.]</detail>
</fault>
'''