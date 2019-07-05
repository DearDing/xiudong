# -*- coding: utf-8 -*- 
# @File : mysqlhelper.py

import pymysql


class MysqlHelper():

    config = {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "LBLB1212@@",
        "database": "dbforpymysql"
    }

    def __init__(self, host=config.get("host"), port=config.get("port"), database=config.get("database"),
                 user=config.get("user"), password=config.get("password"), charset='utf8'):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.charset = charset

    def connect(self):
        self.conn = pymysql.connect(host=self.host, port=self.port, database=self.database, user=self.user,
                                    password=self.password,
                                    charset=self.charset)
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def get_one(self, sql, params=()):
        result = None
        try:
            self.connect()
            self.cursor.execute(sql, params)
            result = self.cursor.fetchone()
            self.close()
        except Exception as e:
            print(e.message)
        return result

    def get_all(self, sql, params=()):
        list = ()
        try:
            self.connect()
            self.cursor.execute(sql, params)
            list = self.cursor.fetchall()
            self.close()
        except Exception as e:
            print(e.message)
        return list

    def insert(self, sql, params=()):
        return self.__edit(sql, params)

    def update(self, sql, params=()):
        return self.__edit(sql, params)

    def delete(self, sql, params=()):
        return self.__edit(sql, params)

    def __edit(self, sql, params):
        count = 0
        try:
            self.connect()
            count = self.cursor.execute(sql, params)
            self.conn.commit()
            self.close()
        except Exception as e:
            print(e.message)
        return count
