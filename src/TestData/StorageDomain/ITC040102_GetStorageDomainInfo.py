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

'''
@note: ModuleTestData
'''

dc_nfs_name = 'DC-ITC04-NFS'
dc_iscsi_name = 'DC-ITC04-ISCSI'
dc_fc_name = 'DC-ITC04-FC'
dc_name_list = [dc_nfs_name, dc_iscsi_name, dc_fc_name]

cluster_nfs_name = 'Cluster-ITC04-NFS'
cluster_iscsi_name = 'Cluster-ITC04-ISCSI'
cluster_fc_name = 'Cluster-ITC04-FC'
cluster_name_list = [cluster_nfs_name, cluster_iscsi_name, cluster_fc_name]

dc_info = '''
<data_driver>
    <data_center>
        <name>%s</name>
        <storage_type>nfs</storage_type>
        <version minor="3" major="3"/>
    </data_center>
    <data_center>
        <name>%s</name>
        <storage_type>iscsi</storage_type>
        <version minor="3" major="3"/>
    </data_center>
    <data_center>
        <name>%s</name>
        <storage_type>fcp</storage_type>
        <version minor="3" major="3"/>
    </data_center>
</data_driver>
''' % (dc_nfs_name, dc_iscsi_name, dc_fc_name)

cluster_info = '''
<data_driver>
    <cluster>
        <name>%s</name>
        <cpu id="Intel Conroe Family"/>
        <data_center>
            <name>%s</name>
        </data_center>
    </cluster>
    <cluster>
        <name>%s</name>
        <cpu id="Intel Conroe Family"/>
        <data_center>
            <name>%s</name>
        </data_center>
    </cluster>
    <cluster>
        <name>%s</name>
        <cpu id="Intel Conroe Family"/>
        <data_center>
            <name>%s</name>
        </data_center>
    </cluster>
</data_driver>
''' % (cluster_nfs_name, dc_nfs_name, cluster_iscsi_name, dc_iscsi_name, cluster_fc_name, dc_fc_name)

'''
@note: ExpectedResult
'''
expected_status_code_create_dc = 201
expected_status_code_create_cluster = 201
expected_status_code_del_dc = 200
expected_status_code_del_cluster = 200