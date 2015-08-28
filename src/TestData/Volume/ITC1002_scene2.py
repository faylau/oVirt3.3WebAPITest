#encoding:utf-8



from Configs.GlobalConfig import Hosts, DataStorages, IsoStorages, ExportStorages
from TestData.Volume import ITC10_SetUp as ModuleData
from TestAPIs.HostAPIs import HostAPIs
from TestAPIs.ClusterAPIs import ClusterAPIs
from TestAPIs.TemplatesAPIs import TemplatesAPIs
from TestData.VirtualMachine.ITC05010502_DelVm_WithoutDisk import disk_alias
from TestAPIs.StorageDomainAPIs import StorageDomainAPIs
from TestAPIs.VirtualMachineAPIs import VirtualMachineAPIs
'''
---------------------------------------------------------------------------------------------------
@note: ModuleTestData
---------------------------------------------------------------------------------------------------
'''

########################################################################
# 集群名称和两个主机id                                                                                                                                  
########################################################################
cluster_name = ModuleData.cluster_nfs_name
cluster_id = ClusterAPIs().getClusterIdByName(cluster_name)
host1_name = ModuleData.host1_name
host2_name = ModuleData.host2_name
host1_id = HostAPIs().getHostIdByName(host1_name)
host2_id = HostAPIs().getHostIdByName(host2_name)


########################################################################
# 主机的gluster存储目录                                                                                                                       
########################################################################


dir_list = ['/storage/d1','/storage/dd2','/storage/d3','/storage/d4']
'''
---------------------------------------------------------------------------------------------------
@note: Test-Data
----
-----------------------------------------------------------------------------------------------
'''
#卷信息
xml_volume_dis = '''
    <gluster_volume>
    <name>dis</name>
    <volume_type>distribute</volume_type>
    <bricks>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
    </bricks>
    </gluster_volume>
    '''%(host2_id, dir_list[0])
xml_volume_rep = '''
    <gluster_volume>
    <name>rep</name>
    <volume_type>replicate</volume_type>
    <replica_count>2</replica_count>
    <bricks>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
    </bricks>
    </gluster_volume>
    '''%(host1_id, dir_list[1], host2_id, dir_list[1])
xml_volume_disrep = '''
    <gluster_volume>
    <name>disrep</name>
    <volume_type>distributed_replicate</volume_type>
    <replica_count>2</replica_count>
    <bricks>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
    </bricks>
    </gluster_volume>
    '''%(host1_id, dir_list[2], host2_id, dir_list[2], host1_id, dir_list[3], host2_id, dir_list[3])
#brick信息
xml_brick_info='''
<bricks>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
        <brick>
        <server_id>%s</server_id>
        <brick_dir>%s</brick_dir>
        </brick>
</bricks>
'''%(host1_id, dir_list[0], host2_id, dir_list[0])
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
expected_status_code_create_volume = 201
expected_status_code_delete_volume = 201
expected_status_code_start_volume = 200
expected_status_code_add_brick = 201
expected_status_code_stop_volume = 200
expected_status_code_create_sd = 201
expected_status_code_del_cluster = 200

