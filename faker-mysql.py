#常用方法查询:https://www.jianshu.com/p/d227d6522428

# Faker 是一个可以让你生成伪造数据的Python包

#pip3 install pymysql
import pymysql
#pip3 install faker
from faker import Faker


class Faker_mysql(object):
    def __init__(self,conn):
        self.conn = conn

    #建表语句函数,这里给出表结构，如果使用已存在的表，可以不创建表。
    def create_table(self):
        create_table_sql="""
        create table user(
        id int PRIMARY KEY auto_increment,
        username VARCHAR(20),
        password VARCHAR(20),
        address VARCHAR(35) 
        )
        """
        
        return create_table_sql

    #插入数据
    def insert_data(self):
        #创建游标
        cursor = self.conn.cursor()

        #调用建表函数
        # create_table = self.create_table()
        #执行sql语句
        # cursor.execute(create_table)

        
        #实例化Faker库，选择中文 zh-CN
        fake = Faker("zh-CN")
        while True:
            #使用Faker库生成假数据,将其转为字典格式,方便插入数据库
            ctx = {
                'username':fake.name(),
                'password':fake.password(special_chars=False),
                'address':fake.address()
            }
            print(ctx)
            sql="""
            insert into user(%s) value(%s)"""%(','.join([k for k,v in ctx.items()]),
            ','.join(['%s' for k,v in ctx.items()])
            )

            try:
                cursor.execute(sql,[v for k,v in ctx.items()])
                self.conn.commit()

            except:
                print('失败')
                self.conn.rollback()
        

if __name__ == "__main__":
    #连接数据库
    #host(ip地址),prot(端口号),user(用户),password(密码),database/db(数据库),charset='utf8'
    conn = pymysql.connect(host="localhost",
                            port=3306,
                            user="root",
                            password="python3..",
                            db="fakerceshi",
                            charset="utf8")
    print('链接成功')  
    
    faker_mysql = Faker_mysql(conn)   
    faker_mysql.insert_data()

