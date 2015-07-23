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

'''---------------------------------------------------------------------------------------------
@note: PreData 
---------------------------------------------------------------------------------------------'''
dc_name = ModuleData.dc_name
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_name = 'Cluster-ITC020204'
cluster_info='''
<cluster>
        <name>%s</name>
        <cpu id="Intel Conroe Family"/>
        <data_center id="%s"/>
</cluster>
''' % (cluster_name, dc_id)

# network name必须在15个字符以内，且只能是大小写字母、数字或_。
nw_name = 'nw_ITC020204'
nw_info = '''
<network>
    <name>%s</name>
    <data_center id= "%s"/> 
</network>
''' % (nw_name, dc_id)

'''---------------------------------------------------------------------------------------------
@note: ExpectedResult
---------------------------------------------------------------------------------------------'''
status_code = 200
