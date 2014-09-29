#encoding:utf-8

cluster_name = 'test-cluster'
status_code = 409

'''
@note: PreData and TestData
'''
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="5849b030-626e-47cb-ad90-3ce782d831b3"/>  
</cluster>
''' % cluster_name

error_info = '''
<fault>
    <reason>Operation Failed</reason>
    <detail>[Cannot create Cluster. Cluster name is already in use.]</detail>
</fault>
'''