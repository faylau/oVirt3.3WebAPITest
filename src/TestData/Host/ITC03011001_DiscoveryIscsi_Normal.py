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

'''
@note: Pre-TestData
'''
host = GlobalConfig.Hosts['node1']
host_name = 'node-ITC03011001'
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

'''
@note: Test-Data
'''
iscsi_server = GlobalConfig.DataStorages['iscsi']['data1-iscsi']
xml_iscsi_info = '''
<action>
    <iscsi>
        <address>%s</address>
        <port>%s</port>
    </iscsi>
</action>
''' % (iscsi_server['ip'], iscsi_server['port'])

'''
@note: Post-TestData
'''
# 资源清理时删除host所用的选项（强制删除/同步）
xml_host_del_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''

'''
@note: ExpectedResult
'''
expected_status_code_create_host = 201          # 创建主机操作的期望状态码
expected_status_code_discovery_iscsi = 200      # 成功探测到iscsi服务器时，返回状态码
expected_status_code_deactive_host = 200        # 维护主机操作的期望状态码
expected_status_code_del_host = 200             # 删除主机操作的期望状态码
