#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

'''-----------------------------------------------------------------------------------------
@note: Pre-TestData
-----------------------------------------------------------------------------------------'''


'''-----------------------------------------------------------------------------------------
@note: Test-Data
-----------------------------------------------------------------------------------------'''
# 主机名称：（1）包含特殊字符；（2）超过255个字符.
host_name_list = ['node-ITC03010304-~!@#$%^',
                  'node-ITC03010304-abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz01234'
                  ]
xml_host_info = '''
<data_driver>
    <host>
        <name>%s</name>
        <address>10.1.167.4</address>
        <root_password>qwer1234</root_password>
    </host>
    <host>
        <name>%s</name>
        <address>10.1.167.4</address>
        <root_password>qwer1234</root_password>
    </host>
</data_driver>
''' % (host_name_list[0], host_name_list[1])

'''-----------------------------------------------------------------------------------------
@note: Post-TestData
-----------------------------------------------------------------------------------------'''
xml_del_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''

'''-----------------------------------------------------------------------------------------
@note: ExpectedResult
-----------------------------------------------------------------------------------------'''
expected_status_code = 400
expected_info_list = [
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Host name must be formed of alphanumeric characters, numbers or "-_."]</detail>
</fault>
''',
'''
<fault>
    <reason>Operation Failed</reason>
    <detail>[size must be between 1 and 255]</detail>
</fault>
'''
]