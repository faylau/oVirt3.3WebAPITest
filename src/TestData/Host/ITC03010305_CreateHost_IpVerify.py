#encoding:utf-8


'''
@note: Pre-TestData
'''


'''
@note: Test-Data
'''
# 主机名称：（1）包含特殊字符；（2）超过255个字符.
ip_list = ['256.1.1.1',
           'a.1.167.4',
           '10.1.167',
           '10.1.167.4#'
           ]
xml_host_info = '''
<data_driver>
    <host>
        <name>node-ITC03010305-1</name>
        <address>%s</address>
        <root_password>qwer1234</root_password>
    </host>
    <host>
        <name>node-ITC03010305-2</name>
        <address>%s</address>
        <root_password>qwer1234</root_password>
    </host>
    <host>
        <name>node-ITC03010305-3</name>
        <address>%s</address>
        <root_password>qwer1234</root_password>
    </host>
    <host>
        <name>node-ITC03010305-4</name>
        <address>%s</address>
        <root_password>qwer1234</root_password>
    </host>
</data_driver>
''' % (ip_list[0], ip_list[1], ip_list[2], ip_list[3])

'''
@note: Post-TestData
'''


'''
@note: ExpectedResult
'''
expected_status_code = 400
expected_info ='''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Host address must be a FQDN or a valid IP address]</detail>
</fault>
'''