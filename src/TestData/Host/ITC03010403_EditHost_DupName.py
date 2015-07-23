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
host1 = GlobalConfig.Hosts['node1']
host2 = GlobalConfig.Hosts['node2']
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
''' % (host1_name, host1['ip'], host1['password'], DM.cluster_name)
xml_host2_info = '''
<host>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
    <cluster>
        <name>%s</name>
    </cluster>
</host>
''' % (host2_name, host2['ip'], host2['password'], DM.cluster_name)

'''-----------------------------------------------------------------------------------------
@note: Test-Data
-----------------------------------------------------------------------------------------'''
# 将host2的名称修改为与host1同名
xml_host2_update_info = '''
<host>
    <name>%s</name>
</host>
''' % (host1_name)

'''-----------------------------------------------------------------------------------------
@note: Post-TestData
-----------------------------------------------------------------------------------------'''
# 资源清理时删除host所用的选项（强制删除/同步）
xml_host_del_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''

'''-----------------------------------------------------------------------------------------
@note: ExpectedResult
-----------------------------------------------------------------------------------------'''
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
