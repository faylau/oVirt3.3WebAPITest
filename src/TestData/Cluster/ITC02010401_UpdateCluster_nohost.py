#encoding:utf-8
import TestData.Cluster.ITC02_Setup as ModuleData
from TestAPIs.DataCenterAPIs import DataCenterAPIs
'''
更新集群-01成功更改集群的名称和cpu类型
'''
dc_id = DataCenterAPIs().getDataCenterIdByName(ModuleData.dc_name)
cluster_name = 'test-cluster'
cluster_name_new = 'test-cluster-new'

'''
@note: PreData
'''
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="%s"/>
</cluster>
''' %(cluster_name,dc_id)

'''
@note: TestData
@note: 当集群内无主机时，更改集群的名称、cpu类型以及升高cpu级别
'''
cluster_info_new = '''
<data_driver>
<cluster>
        <cpu id="Intel Haswell"/>
</cluster>
<cluster>
        <cpu id="AMD Opteron G3"/>
</cluster>
<cluster>
        <name>%s</name>
</cluster>
</data_driver>
''' %(cluster_name_new)

'''
@note: ExpectedData
'''
status_code = 200