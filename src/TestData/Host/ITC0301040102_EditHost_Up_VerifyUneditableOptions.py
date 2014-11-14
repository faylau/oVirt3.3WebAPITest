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

from Configs import GlobalConfig
import ITC03_SetUp as DM

'''-----------------------------------------------------------------------------------------
@note: Pre-TestData
-----------------------------------------------------------------------------------------'''
host = GlobalConfig.Hosts['node1']
host_name = 'node-ITC0301040102'
xml_host_info = '''
<host>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
    <cluster>
        <name>%s</name>
    </cluster>
</host>
''' % (host_name, host['ip'], host['password'], DM.cluster_name)

'''-----------------------------------------------------------------------------------------
@note: Test-Data
-----------------------------------------------------------------------------------------'''
xml_host_update_info = '''
<host>
    <address>192.168.0.254</address>
    <password>abcdefg</password>
    <cluster>
        <name>Default</name>
    </cluster>
</host>
'''

'''-----------------------------------------------------------------------------------------
@note: Post-TestData
-----------------------------------------------------------------------------------------'''
xml_host_del_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''

'''-----------------------------------------------------------------------------------------
@note: ExpectedResult
-----------------------------------------------------------------------------------------'''
expected_status_code_create_host = 201          # 创建主机操作成功，期望状态码
expected_status_code_edit_host = 409            # 编辑主机操作失败，期望状态码
expected_info_edit_host = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot edit Host. Host parameters cannot be modified while Host is operational.
Please switch Host to Maintenance mode first.]</detail>
</fault>
'''
expected_status_code_deactive_host = 200        # 维护主机操作成功，期望状态码
expected_status_code_del_host = 200             # 删除主机操作成功，期望状态码
