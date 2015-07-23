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

from Configs.GlobalConfig import Hosts, DataStorages, IsoStorages, ExportStorages

'''
---------------------------------------------------------------------------------------------------
@note: ModuleTestData
---------------------------------------------------------------------------------------------------
'''
########################################################################
# 1个数据中心信息                                                                                                                                    
########################################################################
dc_nfs_name = 'DC-ITC01-NFS'
dc_name_list = [dc_nfs_name]
xml_dc_info = '''
    <data_center>
        <name>%s</name>
        <local>false</local>
        <version major="3" minor="4"/>
    </data_center>
''' % (dc_nfs_name)

########################################################################
# 1个集群信息                                                                                                                                    
########################################################################
cluster_nfs_name = 'Cluster-ITC01-NFS'
cluster_name_list = [cluster_nfs_name]
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
host1 = Hosts['node1']
host1_name = 'node-ITC01-1'
host1_ip = host1['ip']
host1_password = host1['password']
xml_host_info = '''
    <host>
        <cluster>
            <name>%s</name>
        </cluster>
        <name>%s</name>
        <address>%s</address>
        <root_password>%s</root_password>
    </host>
''' % (cluster_nfs_name, host1_name, host1_ip, host1_password)

#######################################################################################
# 4个存储域信息（data1/data2，1个ISO和1个Export域）                                                                                                                               
#######################################################################################
data1_nfs_name = 'data1-nfs-ITC01'
data1_nfs = DataStorages['nfs']['data1']
data1_nfs_ip = data1_nfs['ip']
data1_nfs_path = data1_nfs['path']
data2_nfs_name = 'data2-nfs-ITC01'
data2_nfs = DataStorages['nfs']['data2']
data2_nfs_ip = data2_nfs['ip']
data2_nfs_path = data2_nfs['path']
iso1_name = 'iso1-ITC01'
iso1 = IsoStorages['ISO-Storage1']
iso1_ip = iso1['ip']
iso1_path = iso1['path']
export1_name = 'export1-ITC01'
export1 =  ExportStorages['Export-Storage2']
export1_ip = export1['ip']
export1_path = export1['path']

xml_storage_info = '''
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
       data2_nfs_name, host1_name, data2_nfs_ip, data2_nfs_path, 
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