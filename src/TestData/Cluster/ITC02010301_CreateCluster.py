#encoding:utf-8

cluster_name = 'test-cluster'
status_code = 201

'''
@note: TestData
'''
cluster_info = '''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center  id="5849b030-626e-47cb-ad90-3ce782d831b3"/>
        <virt_service>true</virt_service>
        <gluster_service>true</gluster_service>
        <tunnel_migration>true</tunnel_migration>
        <trusted_service>false</trusted_service> 
        <ballooning_enabled>true</ballooning_enabled>  
</cluster>
''' % cluster_name