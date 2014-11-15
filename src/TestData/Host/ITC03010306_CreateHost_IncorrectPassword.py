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
from Configs import GlobalConfig

host = GlobalConfig.Hosts['node1']

'''-----------------------------------------------------------------------------------------
@note: Test-Data
-----------------------------------------------------------------------------------------'''
# 主机名称：（1）包含特殊字符；（2）超过255个字符.
password = 'abcdefghijklmn'
xml_host_info = '''
<host>
    <name>node-ITC03010306</name>
    <address>%s</address>
    <root_password>%s</root_password>
</host>
''' % (host['ip'], password)

'''-----------------------------------------------------------------------------------------
@note: Post-TestData
-----------------------------------------------------------------------------------------'''


'''-----------------------------------------------------------------------------------------
@note: ExpectedResult
-----------------------------------------------------------------------------------------'''
expected_status_code = 409
expected_info ='''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot add Host. SSH authentication failed, verify authentication parameters are correct (Username/Password, public-key etc.) You may refer to the engine.log file for further details.]</detail>
</fault>
'''