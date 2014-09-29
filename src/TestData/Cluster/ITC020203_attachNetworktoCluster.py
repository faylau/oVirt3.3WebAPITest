#encoding:utf-8

cluster_name = 'test-cluster'
network_name = 'test_network'
status_code = 201

'''
@note: PreData 
'''
nw_info = '''
<network>
    <name>%s</name>
    <description>lalala</description>
    <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/> 
</network>
'''%network_name

cluster_info='''
<cluster>
        <name>%s</name>
        <cpu id="Intel Penryn Family"/>
        <data_center id= "5849b030-626e-47cb-ad90-3ce782d831b3"/>
        <virt_service>true</virt_service>
        <gluster_service>true</gluster_service>
        <tunnel_migration>ture</tunnel_migration>
        <trusted_service>false</trusted_service> 
        <ballooning_enabled>true</ballooning_enabled>  
</cluster>
'''%cluster_name
