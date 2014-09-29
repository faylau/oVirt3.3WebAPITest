#encoding:utf-8
'''
更新集群-01成功更改集群的名称和cpu类型
'''
cluster_name = 'test-cluster'
cluster_name_new = 'test-cluster-new'
status_code = 200
'''
@note: PreData
'''
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="5849b030-626e-47cb-ad90-3ce782d831b3"/>
</cluster>
''' % cluster_name

'''
@note: TestData
'''
cluster_info_new = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Nehalem Family"/>
        <data_center  id="5849b030-626e-47cb-ad90-3ce782d831b3"/>
</cluster>
''' % cluster_name_new