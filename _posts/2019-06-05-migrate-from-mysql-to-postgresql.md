---
layout: post
title: 记录一次从 MySQL 迁移至 PostgreSQL 数据库
date: 2019-06-05 21:44:17 +0800
categories: 开发 数据库
show_excerpt_image: true
---

首先查找了一些开源项目，采用 mysqldump 导出数据，然后使用该脚本 [MySQL to PostgreSQL Converter](https://github.com/lanyrd/mysql-postgresql-converter) 转换一些换行符，将单引号转换至双引号。然后查看了 StackOverflow 的一些资料：

> but even then you will have to change escaped chars (replacing\t with ^I,\n with ^M, single quote (‘) with doubled single quote and double (escaped) backslash (\) with a single backslash). This can’t be trivially done with sed command.

> you need to use—default-character-set=utf8 when exporting your mysqldump to make it work.

由于项目比较小，数据量也不大，最终决定自己写转换脚本以确保转换过程可控。

`psql -f databasename.psql`

## 最终选择方案
* dump MySQL 的表结构，调整字段，创建表
* 通过 Python 简易脚本导入数据

```
import mysql.connector
import psycopg2
import traceback

mydb = mysql.connector.connect(
   host="localhost",
   user="root",
   passwd="******",
   db="mic"
)

psdb = psycopg2.connect(
   host="localhost",
   user="rthel",
   password="******",
   database="mic"
)

def insertToPSQL(db, table_name, data):
   cursor = db.cursor()
   query = "insert into %s values("

   for col in data:
       # 处理单引号与百分号
       if isinstance(col, str):
           col = col.replace("'", "\'\'")
           col = col.replace("%", "%%")
       # 将 None 转为 null 并在字符串两侧增加单引号
       if col != None:
           query += "'" + str(col) + "',"
       else:
           query += "null,"

   query = query[:-1]
   query += ")"
   cursor.execute(query % table_name)
   db.commit()

for tablename in ["image", "recommendation", "user"]:
   mycursor = mydb.cursor()
   mycursor.execute("select * from " + tablename)
   myresult = mycursor.fetchall()

   for result in myresult:
       try:
           insertToPSQL(psdb, tablename, result)
       except Exception as e:
           traceback.print_exc()
           exit()
```

## 配置变动
增加依赖

```
<dependency>
<groupId>org.postgresql</groupId>
<artifactId>postgresql</artifactId>
<version>42.2.6</version>
</dependency>
```

修改配置项

```
spring.datasource.url = jdbc:mysql://localhost:3306/mic?serverTimezone=GMT
spring.datasource.url = jdbc:postgresql://localhost:5432/mic?serverTimezone=GMT
spring.jpa.database-platform = org.hibernate.dialect.MySQL8Dialect
spring.jpa.database-platform = org.hibernate.dialect.PostgreSQLDialect
```
