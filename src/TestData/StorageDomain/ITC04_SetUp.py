#coding:utf-8


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

from Configs.GlobalConfig import Hosts, DataStorages, IsoStorages, ExportStorages

'''
---------------------------------------------------------------------------------------------------
@note: ModuleTestData
---------------------------------------------------------------------------------------------------
'''
########################################################################
# 数据中心信息                                                                                                                                 
########################################################################
dc_name = 'DC-ITC04'
dc_info = '''
<data_center>
        <name>%s</name>
        <local>false</local>
        <version minor="4" major="3"/>
</data_center>   
''' % dc_name

########################################################################
# 3个集群信息                                                                                                                                    
########################################################################
cluster_name = 'Cluster-ITC04'

cluster_info = '''
    <cluster>
        <name>%s</name>
        <cpu id="Intel Conroe Family"/>
        <data_center>
            <name>%s</name>
        </data_center>
    </cluster>
    
''' % (cluster_name, dc_name)
########################################################################
# 2个主机信息（node1加入NFS数据中心，node4加入ISCSI数据中心）                                                                                                                                    
########################################################################
host4 = Hosts['node2']
host4_name = 'node-ITC04-2'
host4_ip = host4['ip']
host4_password = host4['password']

host1 = Hosts['node1']
host1_name = 'node-ITC04-1'
host1_ip = host1['ip']
host1_password = host1['password']
hosts_info_xml = '''
<data_driver>
    <host>
        <cluster>
            <name>%s</name>
        </cluster>
        <name>%s</name>
        <address>%s</address>
        <root_password>%s</root_password>
    </host>
    <host>
        <cluster>
            <name>%s</name>
        </cluster>
        <name>%s</name>
        <address>%s</address>
        <root_password>%s</root_password>
    </host>
</data_driver>
''' % (cluster_name, host1_name, host1_ip, host1_password,
       cluster_name, host4_name, host4_ip, host4_password)

#######################################################################################
# 4个存储域信息（2个Data域分别附加到NFS/ISCSI数据中心，1个ISO和1个Export域附加到NFS数据中心）                                                                                                                               
#######################################################################################
data1_nfs_name = 'data1-nfs-ITC04'
data1_nfs = DataStorages['nfs']['data1']
data1_nfs_ip = data1_nfs['ip']
data1_nfs_path = data1_nfs['path']
# data1_iscsi_name = 'data1-iscsi-ITC04'
# data1_iscsi = DataStorages['iscsi']['data1-iscsi']
# data1_iscsi_ip = data1_iscsi['ip']
# data1_iscsi_port = data1_iscsi['port']
# data1_iscsi_target = data1_iscsi['target']
# data1_iscsi_lun_id = data1_iscsi['lun_id']
iso1_name = 'iso1-ITC04'
iso1 = IsoStorages['ISO-Storage1']
iso1_ip = iso1['ip']
iso1_path = iso1['path']
export1_name = 'export1-ITC04'
export1 =  ExportStorages['Export-Storage2']
export1_ip = export1['ip']
export1_path = export1['path']

xml_datas_info = '''
<data_driver>
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
    <storage_domain>
        <name>%s</name>
        <type>iso</type>
        <host>
            <name>%s</name>
        </host>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
    <storage_domain>
        <name>%s</name>
        <type>export</type>
        <host>
            <name>%s</name>
        </host>
        <storage>
            <type>nfs</type>
            <address>%s</address>
            <path>%s</path>
        </storage>
    </storage_domain>
</data_driver>
''' % (data1_nfs_name, host1_name, data1_nfs_ip, data1_nfs_path, 
       iso1_name, host1_name, iso1_ip, iso1_path, 
       export1_name, host1_name, export1_ip, export1_path )

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

xml_del_sd_option = '''
<storage_domain>
    <host>
        <name>%s</name>
    </host>
    <format>true</format>
</storage_domain>
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