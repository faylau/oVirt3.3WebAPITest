#coding:utf-8


__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/24          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

from Configs.GlobalConfig import Hosts
from TestData.DataCenter import ITC01_SetUp as ModuleData

'''
---------------------------------------------------------------------------------------------------
@note: ModuleTestData
---------------------------------------------------------------------------------------------------
'''
########################################################################
# 1个数据中心信息                                                                                                                                    
########################################################################
dc_nfs_name = 'DC-ITC0102030101-NFS'
xml_dc_info = '''
    <data_center>
        <name>%s</name>
        <local>false</local>
        <version minor="4" major="3"/>
    </data_center>
''' % (dc_nfs_name)

########################################################################
# 1个集群信息                                                                                                                                    
########################################################################
cluster_nfs_name = 'Cluster-ITC0102030101-NFS'
xml_cluster_info = '''
    <cluster>
        <name>%s</name>
        <cpu id="Intel Conroe Family"/>
        <data_center>
            <name>%s</name>
        </data_center>
    </cluster>
''' % (cluster_nfs_name, dc_nfs_name)

########################################################################
# 1个主机信息（node1加入NFS数据中心）                                                                                                                                    
########################################################################
host = Hosts['node2']
host_name = 'node-ITC0102030101'
host_ip = host['ip']
host_password = host['password']
xml_host_info = '''
    <host>
        <cluster>
            <name>%s</name>
        </cluster>
        <name>%s</name>
        <address>%s</address>
        <root_password>%s</root_password>
    </host>
''' % (cluster_nfs_name, host_name, host_ip, host_password)

#######################################################################################
# 1个存储域信息（只需要提供存储域名称，因为它是在模块测试环境中已经创建的data2_nfs）                                                                                                                               
#######################################################################################
data_nfs_name = ModuleData.data2_nfs_name

'''
---------------------------------------------------------------------------------------------------
@note: Post-Test-Data
---------------------------------------------------------------------------------------------------
'''
xml_del_host_option = '''
<action>
    <force>true</force>
    <async>false</async>
</action>
'''



'''
---------------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------------
'''
expected_status_code_create_dc = 201
expected_status_code_create_cluster = 201
expected_status_code_del_dc = 200
expected_status_code_del_cluster = 200