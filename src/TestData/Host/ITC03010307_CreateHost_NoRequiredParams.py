#encoding:utf-8


'''
@note: Pre-TestData
'''


'''
@note: Test-Data
'''
xml_host_info = '''
<data_driver>
    <host>
        <name></name>
        <address>10.1.167.4</address>
        <root_password>qwer1234</root_password>
    </host>
    <host>
        <name>node-ITC03010307-1</name>
        <address></address>
        <root_password>qwer1234</root_password>
    </host>
    <host>
        <name>node-ITC03010307-2</name>
        <address>10.1.167.4</address>
        <root_password></root_password>
    </host>
</data_driver>
'''

'''
@note: Post-TestData
'''


'''
@note: ExpectedResult
'''
expected_status_code = 400
expected_info_list = [
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Host name must be formed of alphanumeric characters, numbers or &quot;-_.&quot;, size must be between 1 and 255]</detail>
</fault>
''',
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Host address must be a FQDN or a valid IP address]</detail>
</fault>
''',
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot install Host with empty password.]</detail>
</fault>
'''
]