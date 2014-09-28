#encoding:utf-8


'''
@PreData
'''
dc_name = 'Default'

'''
@note: TestData
'''
dc_info = '''
<data_center>
        <name>%s</name>
        <storage_type>nfs</storage_type>
        <version minor="1" major="3"/>
</data_center>
''' % dc_name

'''
@note: ExpectedResult
'''
expected_status_code = 409
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot create Data Center. The Data Center name is already in use.]</detail>
</fault>
'''