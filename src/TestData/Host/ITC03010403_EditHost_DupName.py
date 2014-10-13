#encoding:utf-8


from Configs import GlobalConfig
import ITC03_SetUp as DM

'''
@note: Pre-TestData
'''
host1_name = 'node-ITC03010403-1'
host2_name = 'node-ITC03010403-2'
xml_host1_info = '''
<host>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
    <cluster>
        <name>%s</name>
    </cluster>
</host>
''' % (host1_name, GlobalConfig.Hosts['node1']['ip'], GlobalConfig.Hosts['node1']['password'], DM.cluster_name)
xml_host2_info = '''
<host>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
    <cluster>
        <name>%s</name>
    </cluster>
</host>
''' % (host2_name, GlobalConfig.Hosts['node4']['ip'], GlobalConfig.Hosts['node4']['password'], DM.cluster_name)

'''
@note: Test-Data
'''
# 将host2的名称修改为与host1同名
xml_host2_update_info = '''
<host>
    <name>%s</name>
</host>
''' % (host1_name)

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
expected_status_code_edit_host_fail = 400       # 编辑主机操作失败的期望状态码
expected_info_edit_host_dup_name = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot edit Host. The Host name is already in use, please choose a unique name and try again.]</detail>
</fault>
'''
expected_status_code_deactive_host = 200        # 维护主机操作的期望状态码
expected_status_code_del_host = 200             # 删除主机操作的期望状态码
