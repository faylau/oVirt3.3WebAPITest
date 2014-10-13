#encoding:utf-8


'''
@note: PreData
'''
dc_name = 'DC-ITC01010501'
pre_dc_info = '''
<data_center>
    <name>%s</name>
    <storage_type>nfs</storage_type>
    <version minor="1" major="3"/>
</data_center>
''' % dc_name

'''
@note: TestData
'''
del_dc_option = '''
'''

'''
@note: ExpectedResult
'''
expected_status_code = 200
expected_info = '''
<action>
    <status>
        <state>complete</state>
    </status>
</action>
'''