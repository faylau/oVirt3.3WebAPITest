#encoding:utf-8

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date                Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/10/17          初始版本                                                            Liu Fei 
#---------------------------------------------------------------------------------
'''

'''-----------------------------------------------------------------------------------------
@note: ModuleTestData
-----------------------------------------------------------------------------------------'''
dc_name = 'DC-ITC03-NFS'
cluster_name = 'Cluster-ITC03'

dc_info = '''
<data_center>
    <name>%s</name>
    <storage_type>nfs</storage_type>
    <version minor="3" major="3"/>
</data_center>
''' % dc_name

cluster_info = '''
<cluster>
    <name>%s</name>
    <cpu id="Intel Conroe Family"/>
    <data_center>
        <name>%s</name>
    </data_center>
</cluster>
''' % (cluster_name, dc_name)

'''-----------------------------------------------------------------------------------------
@note: ExpectedResult
-----------------------------------------------------------------------------------------'''