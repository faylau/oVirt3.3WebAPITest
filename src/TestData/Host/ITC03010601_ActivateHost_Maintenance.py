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
import ITC03_SetUp as DataModule

'''-----------------------------------------------------------------------------------------
@note: Pre-TestData
-----------------------------------------------------------------------------------------'''
host = GlobalConfig.Hosts['node1']
host_name = 'node-ITC03010601'
# 前提1：创建一个主机
xml_host_info = '''
<host>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
    <cluster>
        <name>%s</name>
    </cluster>
</host>
''' % (host_name, host['ip'], host['password'], DataModule.cluster_name)

'''-----------------------------------------------------------------------------------------
@note: Test-Data
-----------------------------------------------------------------------------------------'''


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
expected_status_code_create_host = 201          # 创建主机操作成功，状态码
expected_status_code_deactive_host = 200        # 维护主机操作成功，状态码
expected_status_code_active_host = 200          # 激活主机操作成功，状态码
expected_status_code_del_host = 200             # 删除主机操作成功，状态码
