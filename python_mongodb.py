#　mongodb与python的交互
# sudo pip3 install pymongo
import pymongo
from bson.objectid import ObjectId

class Python_Mongodb(object):
    def __init__(self):
        #创建mongo客户端链接
        self.mongoConn = pymongo.MongoClient('localhost',27017)

        #有账号和密码的连接
        #mongoConn = pymongo.MongoClient('mongodb://user:pwd@localhost:27017/')

        #获取要操作的数据库
        self.use_db = self.mongoConn.mongotest

        #获取数据库下要操作的集合
        self.use_col = self.use_db.wxl

    # 增
    def add_data(self):
        document = {
            'name':'liyong',
            'age':20,
            'gender':'男',
        }

        document1 = {
            'name':'lihua',
            'age':22,
            'gender':'男',
        }      
        result = self.use_col.insert([document,document1])
        print(result)
    
    # 删
    def delete_data(self):
        #删除集合中所有数据
        result = self.use_col.remove()
        print(result)

    # 改
    def update_data(self):
        #默认情况下只修改一条
        # result = self.use_col.update({'name':'liyong'},{'$set':{'age':23}})
        # print(result)
        #全文档更新只修改一条
        # result = self.use_col.update({'name':'liyong'},{'name':'lisi','age':23})
        # print(result)
        #更新超照到的全部结果修改多条
        # result = self.use_col.update_many({'name':'liyong'},{'$set':{'age':23}})
        # print(result)
        #　使用save做更新操作,全文档更新
        #注意：name 'ObjectId' is not defined,导入Bson模块下的objectid
        result = self.use_col.save({'_id':ObjectId("5b836b9711575e79be9af0c7"),'name':'wangwu'})
    
    
    # 查
    def find_data(self):
        # 查询集合中所有数据,我们要拿到数据，需要遍历
        result = self.use_col.find()
        print(result)
        print([i for i in result])

    
if __name__ == '__main__':
    python_mongo = Python_Mongodb()
    # python_mongo.add_data()
    # python_mongo.find_data()
    python_mongo.delete_data()


