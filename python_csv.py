import csv
from faker import Faker

#写入数据到csv文件
def write_csv():
    #实例化faker库,zh-CN允许生成中文
    fake = Faker('zh-CN')

    #open()打开一个csv文件,以a+追加方式打开,encoding='utf-8'允许插入中文
    with open('data.csv','a+',encoding='utf-8') as csvfile:
        #设置字段
        fieldnames = ['id','name','phone','python']
        #DictWriter以字典形式写入csv文件
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        #调用writerheader()先写入头信息
        writer.writeheader()
        for i in range(1,100000000):
            ctx = {
                'id':i,
                'name':fake.name(),
                'phone':fake.phone_number(),
                'python':fake.sha256(raw_output=False)
            }
            print(ctx)
            
            #调用writerows方法写入多行,方法使用:writerows([])
            writer.writerows([ctx])

#读取csv文件内容
def read_csv():
    with open('data.csv','r',encoding='utf-8') as csvfile:
        #reader()读取文件内容
        reader = csv.reader(csvfile)
        for row in reader:
            print(row)



if __name__ == "__main__":
    write_csv()
    read_csv()

