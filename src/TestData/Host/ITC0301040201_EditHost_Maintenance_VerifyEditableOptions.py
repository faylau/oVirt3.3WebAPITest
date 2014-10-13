#encoding:utf-8


from Configs import GlobalConfig
from TestAPIs.ClusterAPIs import ClusterAPIs
import ITC03_SetUp as DM

'''
@note: Pre-TestData
'''
init_host_name = 'node-ITC0301040201'
cluster1_name = 'cluster-ITC0301040201'
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
''' % (init_host_name, GlobalConfig.Hosts['node4']['ip'], GlobalConfig.Hosts['node4']['password'], DM.cluster_name)
# 前提2：创建一个新的Cluster，用于修改主机的所属Cluster
xml_cluster1_info = '''
<cluster>
    <name>%s</name>
    <cpu id="Intel Conroe Family"/>
    <data_center>
        <name>%s</name>
    </data_center>
</cluster>
''' % (cluster1_name, DM.dc_name)


'''
@note: Test-Data
'''
new_name = 'node-ITC0301040201-new'
new_desc = 'new description'
xml_host_update_info = '''
<host>
    <name>%s</name>
    <comment>%s</comment>
    <cluster>
        <name>%s</name>
    </cluster>
</host>
''' % (new_name, new_desc, cluster1_name)

'''
@note: Post-TestData
'''
xml_host_del_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''
xml_cluster_del_option = '''
<action>
    <async>false</async>
</action>
'''

'''
@note: ExpectedResult
'''
expected_status_code_create_host = 201          # 创建主机操作成功，状态码
expected_status_code_create_cluster = 201       # 创建集群操作成功，状态码
expected_status_code_edit_host = 200            # 编辑主机操作成功，状态码
expected_status_code_deactive_host = 200        # 维护主机操作成功，状态码
expected_status_code_del_host = 200             # 删除主机操作成功，状态码
expected_status_code_del_cluster = 200          # 删除集群操作成功，状态码
