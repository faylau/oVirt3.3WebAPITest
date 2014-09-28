#encoding:utf-8


'''
@PreData
'''


'''
@note: TestData
dc_name_list[0]：含有特殊字符
dc_name_list[1]：41个字符（刚好超过40个）
'''

dc_name_list = ['DC-ITC0101030302-~!@#$%^', 
                'DC-ITC0101030302-2-0123456789012345678901']
dc_info = '''
<data_driver>
    <data_center>
        <name>%s</name>
        <storage_type>nfs</storage_type>
        <version minor="3" major="3"/>
    </data_center>
    <data_center>
        <name>%s</name>
        <storage_type>nfs</storage_type>
        <version minor="3" major="3"/>
    </data_center>
</data_driver>
''' % (dc_name_list[0], dc_name_list[1])

'''
@note: ExpectedResult
'''
expected_status_code = 400
expected_info_list = [
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Data Center name must be formed of alphanumeric characters, numbers or "-_"]</detail>
</fault>
''',
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[size must be between 1 and 40]</detail>
</fault>
'''
]