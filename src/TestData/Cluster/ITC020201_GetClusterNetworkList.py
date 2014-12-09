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

'''-----------------------------------------------------------------------------------------
@note: PreData
-----------------------------------------------------------------------------------------'''
cluster_name = 'Cluster-ITC020201'
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center id="%s"/>
</cluster>
''' % (cluster_name, dc_id)

'''-----------------------------------------------------------------------------------------
@note: ExpectedResult
-----------------------------------------------------------------------------------------'''
status_code = 200
