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

import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs

'''-------------------------------------------------------------------------------------------------
@note: TestData
-------------------------------------------------------------------------------------------------'''
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_name = 'Cluster-ITC02010301'
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="%s"/>
        <virt_service>true</virt_service>
        <gluster_service>true</gluster_service>
        <tunnel_migration>true</tunnel_migration>
        <trusted_service>false</trusted_service> 
        <ballooning_enabled>true</ballooning_enabled>  
</cluster>
''' % (cluster_name, dc_id)

'''-------------------------------------------------------------------------------------------------
@note: ExpectResult
-------------------------------------------------------------------------------------------------'''
status_code = 201