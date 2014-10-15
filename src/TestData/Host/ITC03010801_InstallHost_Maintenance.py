#encoding:utf-8


from Configs import GlobalConfig
import ITC03_SetUp as DataModule

'''
@note: Pre-TestData
'''
host_name = 'node-ITC030108'
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
''' % (host_name, GlobalConfig.Hosts['node4']['ip'], GlobalConfig.Hosts['node4']['password'], DataModule.cluster_name)

'''
@note: Test-Data
'''
xml_install_option = '''
<action>
    <root_password>%s</root_password>
</action>
''' % GlobalConfig.Hosts['node4']['password']

'''
@note: Post-TestData
'''
xml_host_del_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''

'''
@note: ExpectedResult
'''
expected_status_code_create_host = 201          # 创建主机操作成功，状态码
expected_status_code_install_host = 200         # 安装主机操作成功，状态码
expected_status_code_deactive_host = 200        # 维护主机操作成功，状态码
expected_status_code_del_host = 200             # 删除主机操作成功，状态码
