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
host_name = 'node-ITC0301040202'
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
    <address>10.1.85.242</address>
    <root_password>qwer1235</root_password>
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
expected_status_code_edit_host_fail = 400       # 编辑主机操作失败，期望状态码
expected_info_edit_host = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Host Address can not be modified due to Security restrictions.  In order to change Host Address, Host has to be reinstalled]</detail>
</fault>
'''
expected_status_code_deactive_host = 200        # 维护主机操作成功，期望状态码
expected_status_code_del_host = 200             # 删除主机操作成功，期望状态码
