# -*- coding: utf-8 -*-

__authors__ = ['"Liu Fei" <fei.liu@cs2c.com.cn>']
__version__ = "V0.1"

'''
# ChangeLog:
#---------------------------------------------------------------------------------
# Version        Date            Desc                            Author
#---------------------------------------------------------------------------------
# V0.1           2014/08/29      V0.1                            Liu Fei 
#---------------------------------------------------------------------------------
'''

import psycopg2
import MySQLdb

class DBManager(object):
    '''
    @summary: A class to connect different database, such as MySQL, PostgreSQL. 
              To create database connection, execute query statements and return
              query result.
    @author: fei.liu@cs2c.com.cn
    @version: V0.1
    '''

    def __init__(self, database_type=""):
        '''
        Constructor
        '''
        self.database_type = database_type
        
    def get_db_connection(self, db_type, db_host, db_user, db_pwd, db_name, db_port=None):
        '''
        @summary: Get the database connection
        @param db_type: mysql or pgsql
        @param db_host: database host name or ip
        @param db_user: database user name
        @param db_pwd: database password
        @param db_port: database port, mysql is 2206, pgsql is 5432
        @return: a database connection
        '''
        if self.database_type == "mysql":
            self.connection = MySQLdb.connect(db_host, db_user, db_pwd, db_name, db_port=3306)
        elif self.database_type == "pgsql":
            self.connection = psycopg2.connect(db_host, db_user, db_pwd, db_name, db_port=5432)
        
    def get_mysql_connection(self, db_host, db_user, db_pwd, db_name, db_port=3306):
        '''
        @summary: Get a mysql database connection.
        @param db_host: mysql host name or ip.
        @param db_user: mysql db user name (root or other).
        @param db_pwd: mysql db password.
        @param db_port: mysql port, default 3306.
        '''
        self.connection = MySQLdb.connect(db_host, db_user, db_pwd, db_name, db_port)
    
    def get_pgsql_connection(self, db_host, db_user, db_pwd, db_name, db_port=5432):
        '''
        @summary: Get a pgsql database connection.
        @param db_host: pgsql host name or ip.
        @param db_user: pgsql db user name (root or other).
        @param db_pwd: pgsql db password.
        @param db_port: pgsql port, default 5432.
        '''
        self.connection = psycopg2.connect(db_host, db_user, db_pwd, db_name, db_port)
    
    def get_query_result(self, sql):
        '''
        @summary: Execute a Query statement and return the result (a tuple).
        @param sql: The Query statement.
        @return: Query result (a tuple).
        '''
        self.cursor = self.connection.cursor()
        self.cursor.execute(sql)
        return self.cursor.fetchall()
#         for row in rows:
#             print row
    
    def close_db_connection(self):
        '''
        @summary: Close the database connection.
        '''
        self.cursor.close()
        self.connection.close()
        
if __name__ == "__main__":
    db_type = "pgsql"
    db_host = "10.1.167.2"
    db_user = "root"
    db_pwd = "qwer1234"
    db_name = "engine"
    sql = "SELECT * FROM vds_groups"
    dbmanager = DBManager()
#     dbmanager.get_db_connection("pgsql", db_host, db_user, db_pwd, db_name)
    dbmanager.get_pgsql_connection(db_host, db_user, db_pwd, db_name)
    rows = dbmanager.get_query_result(sql)
    for row in rows:
        print row
    dbmanager.close_db_connection()
