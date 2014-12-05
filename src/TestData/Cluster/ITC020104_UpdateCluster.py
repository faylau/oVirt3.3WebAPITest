#encoding:utf-8
import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs
'''
更新集群-01成功更改集群的名称和cpu类型
'''
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_name = 'Cluster-ITC020104'
cluster_name_new = 'Cluster-ITC020104-New'

'''-------------------------------------------------------------------------------------------
@note: PreData
-------------------------------------------------------------------------------------------'''
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="%s"/>
</cluster>
''' % (cluster_name, dc_id)

'''-------------------------------------------------------------------------------------------
@note: TestData
-------------------------------------------------------------------------------------------'''
cluster_info_new = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Nehalem Family"/>
        <data_center  id="%s"/>
</cluster>
''' % (cluster_name_new, dc_id)

'''-------------------------------------------------------------------------------------------
@note: ExpectedData
-------------------------------------------------------------------------------------------'''
status_code = 200