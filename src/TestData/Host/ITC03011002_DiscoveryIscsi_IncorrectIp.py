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
# 配置电源管理选项的host的相关信息
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
''' % (host_name, host['ip'], \
       host['password'], \
       DM.cluster_name)

'''-----------------------------------------------------------------------------------------
@note: Test-Data
-----------------------------------------------------------------------------------------'''
iscsi_server = GlobalConfig.DataStorages['iscsi']['data1-iscsi']
xml_iscsi_info_list = '''
<data_driver>
    <action>
        <iscsi>
            <address>%s</address>
            <port>3266</port>
        </iscsi>
    </action>
    <action>
        <iscsi>
            <address>192.168.0.250</address>
            <port>%s</port>
        </iscsi>
    </action>
</data_driver>
''' % (iscsi_server['ip'], iscsi_server['port'])

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
expected_status_code_discovery_iscsi_fail = 400 # 探测iscsi服务器失败，返回状态码
expected_info_discovery_iscsi_fail = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>Failed discovery of iSCSI targets</detail>
</fault>
'''
expected_status_code_deactive_host = 200        # 维护主机操作的期望状态码
expected_status_code_del_host = 200             # 删除主机操作的期望状态码
