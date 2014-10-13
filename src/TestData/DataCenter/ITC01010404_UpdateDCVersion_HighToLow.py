#encoding:utf-8


'''
@note: PreData
'''
dc_name = 'DC-ITC01010404'
pre_dc_info = '''
<data_center>
    <name>%s</name>
    <storage_type>nfs</storage_type>
    <version minor="3" major="3"/>
</data_center>
''' % dc_name

'''
@note: TestData
'''
update_dc_info = '''
<data_center>
    <version minor="1" major="3"/>
</data_center>
'''

'''
@note: ExpectedResult
'''
expected_status_code = 400
expected_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot decrease data center compatibility version.]</detail>
</fault>
'''