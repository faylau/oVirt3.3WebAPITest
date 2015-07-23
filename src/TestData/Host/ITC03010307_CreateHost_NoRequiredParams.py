#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                            Liu Fei 
# V0.2                                更改了报错提示信息                                      wei keke
#---------------------------------------------------------------------------------
'''

'''-----------------------------------------------------------------------------------------
@note: Pre-TestData
-----------------------------------------------------------------------------------------'''


'''-----------------------------------------------------------------------------------------
@note: Test-Data
-----------------------------------------------------------------------------------------'''
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

'''-----------------------------------------------------------------------------------------
@note: Post-TestData
-----------------------------------------------------------------------------------------'''


'''-----------------------------------------------------------------------------------------
@note: ExpectedResult
-----------------------------------------------------------------------------------------'''
expected_status_code = 400
expected_info_list = [
'''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>Host [name] required for add</detail>
</fault>
''',
'''
<fault>
    <reason>Incomplete parameters</reason>
    <detail>Host [address] required for add</detail>
</fault>
''',
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot install Host with empty password.]</detail>
</fault>
'''
]