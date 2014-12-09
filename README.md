oVirt3.3WebAPITest
==================

The automation test project for REST API of oVirt3.3.

一、前提条件
1.Python版本必须为2.7.x；
2.下载安装Requests包
（1）安装之前修改requests/packages/urllib3/connectionpool.py文件，将730行至734行注释掉，以pass语句替换；实际上是注释掉了_validate_conn(self, conn)函数中的if not conn.is_verified语句；
（2）目的是为了在使用Requests发送未Verify的请求时，避免Requests产生不相关的警告日志，减小日志的大小）；
（3）也可以不修改，只是最终测试结果中的日志信息会比较多一些（冗余，不美观~~）；
3.下载安装xmltodict包；

二、安装配置oVirt测试环境
1.至少需要1个engine和2个node（至少1个有IPMI电源管理）；
2.至少需要配置3个NFS类型data域、3个ISO域、3个Export域；
3.至少需要配置1个ISCSI类型data域；
4.在Configs/GlobalConfig.py文件中填写相应的主机（主机名/IP/网卡/电源管理等）、存储域（NFS路径/iSCSI路径等）、Web管理平台地址、用户名/密码等相关信息。

三、测试执行
1.缺省是按模块运行；
2.可以修改TestRun/ModuleConf.xml文件，将需要测试的模块的run标记位修改为True，不需要测试的改为False；
3.若不想按模块运行，还提供了按用例执行、BVT等方式（但这些配置文件目前还没有写好），只需修改TestRun/GlobalConf.xml文件，将exec_type字段修改为其他（暂不可用）；
4.配置好要执行的用例之后，运行TestRun/TestCenter.py文件即可开始测试（在终端可以观察到测试执行的进度）；
5.测试结束后，在Results目录下生成测试结果（html文件，以测试执行日期/时间开头命名）。
