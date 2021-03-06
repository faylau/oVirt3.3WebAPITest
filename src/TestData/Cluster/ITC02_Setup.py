#encoding:utf-8

__authors__ = ['wei keke']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                         
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
dc_name = 'DC-ITC02-NFS'
dc_name_list = [dc_name]
dc_info = '''
    <data_center>
        <name>%s</name>
        <local>false</local>
        <version major="3" minor="4"/>
    </data_center>
''' % (dc_name)

########################################################################
# 1个集群信息                                                                                                                                    
########################################################################
cluster_name = 'Cluster-ITC02-NFS'
cluster_name_list = [cluster_name]
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
# 1个主机信息（node1加入NFS数据中心）                                                                                                                                    
########################################################################
host1 = Hosts['node1']
host1_name = 'node-ITC02-1'
host1_ip = host1['ip']
host1_password = host1['password']
host_info = '''
    <host>
        <cluster>
            <name>%s</name>
        </cluster>
        <name>%s</name>
        <address>%s</address>
        <root_password>%s</root_password>
    </host>
''' % (cluster_name, host1_name, host1_ip, host1_password)

#######################################################################################
# 4个存储域信息（data1/data2，1个ISO和1个Export域）                                                                                                                               
#######################################################################################
data1_nfs_name = 'data1-nfs-ITC02'
data1_nfs = DataStorages['nfs']['data1']
data1_nfs_ip = data1_nfs['ip']
data1_nfs_path = data1_nfs['path']
data2_nfs_name = 'data2-nfs-ITC02'
data2_nfs = DataStorages['nfs']['data2']
data2_nfs_ip = data2_nfs['ip']
data2_nfs_path = data2_nfs['path']
export1_name = 'export1-ITC02'
export1 =  ExportStorages['Export-Storage2']
export1_ip = export1['ip']
export1_path = export1['path']
iso1_name = 'iso1-ITC02'
iso1 = IsoStorages['ISO-Storage1']
iso1_ip = iso1['ip']
iso1_path = iso1['path']

storage_info = '''
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
</data_driver>
''' % (data1_nfs_name, host1_name, data1_nfs_ip, data1_nfs_path, 
       data2_nfs_name, host1_name, data2_nfs_ip, data2_nfs_path, 
       export1_name, host1_name, export1_ip, export1_path,
       iso1_name, host1_name, iso1_ip, iso1_path)


'''
@note: 存储域名称应该由该模块的Setup用例初始化获得，这里暂时用字符串代替
'''
vm1_name = 'VM1-ITC02'
vm1_info='''
<vm>
        <name>%s</name>
        <description>Virtual Machine for Module Test.</description>
        <type>server</type>
        <memory>536870912</memory>
        <cluster>
            <name>%s</name>
        </cluster>
        <template>
            <name>Blank</name>
        </template>
        <cpu>
            <topology sockets="2" cores="1"/>
        </cpu>
        <os>
            <boot dev="cdrom"/>
            <boot dev="hd"/>
        </os>
    </vm>
''' % (vm1_name, cluster_name)

vm2_name = 'VM2-ITC02'
vm2_info='''
<vm>
        <name>%s</name>
        <description>Virtual Machine for Module Test.</description>
        <type>server</type>
        <memory>536870912</memory>
        <cluster>
            <name>%s</name>
        </cluster>
        <template>
            <name>Blank</name>
        </template>
        <cpu>
            <topology sockets="2" cores="1"/>
        </cpu>
        <os>
            <boot dev="cdrom"/>
            <boot dev="hd"/>
        </os>
    </vm>
''' % (vm2_name, cluster_name)

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

