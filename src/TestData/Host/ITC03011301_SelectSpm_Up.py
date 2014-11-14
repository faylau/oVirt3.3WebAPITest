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
from Configs.GlobalConfig import DataStorages

'''-----------------------------------------------------------------------------------------
@note: Pre-TestData
-----------------------------------------------------------------------------------------'''
# 配置数据中心信息
dc1_name = 'DC-ITC03011301-NFS'
xml_dc1_info = '''
    <data_center>
        <name>%s</name>
        <storage_type>nfs</storage_type>
        <version minor="3" major="3"/>
    </data_center>

''' % dc1_name

# 配置集群信息
cluster1_name = 'Cluster-ITC03011301'
xml_cluster1_info = '''
<cluster>
    <name>%s</name>
    <cpu id="Intel Conroe Family"/>
    <data_center>
        <name>%s</name>
    </data_center>
</cluster>
''' % (cluster1_name, dc1_name)

# 配置host1和host2的相关信息
host1 = GlobalConfig.Hosts['node1']
host2 = GlobalConfig.Hosts['node4']
host1_name = 'node-ITC03011301-1'
host2_name = 'node-ITC03011301-2'
xml_host1_info = '''
<host>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
    <cluster>
        <name>%s</name>
    </cluster>
</host>
''' % (host1_name, host1['ip'], host1['password'], cluster1_name)
xml_host2_info = '''
<host>
    <name>%s</name>
    <address>%s</address>
    <root_password>%s</root_password>
    <cluster>
        <name>%s</name>
    </cluster>
</host>
''' % (host2_name, host2['ip'], host2['password'], cluster1_name)

# 配置存储域data1-nfs信息
data1_nfs_name = 'data1-ITC03011301'
data1_nfs = DataStorages['nfs']['data1']
data1_nfs_ip = data1_nfs['ip']
data1_nfs_path = data1_nfs['path']
xml_data1_info = '''
<storage_domain>
    <name>%s</name>
    <type>data</type>
    <host>
        <name>%s</name>
    </host>
    <storage>
        <type>nfs</type>
        <address>%s</address>
        <path>%s</path>
    </storage>
</storage_domain>
''' % (data1_nfs_name, host1_name, data1_nfs_ip, data1_nfs_path)

'''-----------------------------------------------------------------------------------------
@note: Test-Data
-----------------------------------------------------------------------------------------'''


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

xml_del_sd_option = '''
<storage_domain>
    <host>
        <name>%s</name>
    </host>
    <format>true</format>
    <async>false</async>
</storage_domain>
''' % host1_name

'''-----------------------------------------------------------------------------------------
@note: ExpectedResult
-----------------------------------------------------------------------------------------'''
expected_status_code_create_host = 201          # 创建主机操作的期望状态码
expected_status_code_del_dc = 200               # 删除数据中心，成功，返回状态码
expected_status_code_del_cluster = 200          # 删除集群，成功，返回状态码
expected_status_code_select_spm = 200           # 手动设置SPM操作成功，返回状态码
expected_status_code_deactive_host = 200        # 维护主机操作的期望状态码
expected_status_code_del_host = 200             # 删除主机操作的期望状态码

