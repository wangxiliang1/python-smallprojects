import requests
from lxml import etree
import pymysql


class Wxlxiangmu(object):
    def __init__(self,url,req_headers):
        self.url = url
        self.req_headers = req_headers
    
    def db(self):
        # print('开始链接')
        client = pymysql.connect(host='localhost',user='root',port=3306,database='zufang',password='python3..',charset='utf8')
        # print('连接成功')
        return client


    def insert_ershou(self,d,data):
        cursor = d.cursor()
        sql = """
        INSERT INTO ershou_parse(%s) VALUE(%s)
        """%(','.join([k for k,v in data.items()]),
        ','.join(['%s' for k,v in data.items()]),
        )

        try:
            cursor.execute(sql,[v for k,v in data.items()])
            d.commit()
        except:
            print('失败')
            d.rollback()
    


    def hebingzidian(self,d,data):
        cursor = d.cursor()
        sql = """
        INSERT INTO zufang_parse(%s) VALUE(%s)
        """%(','.join([k for k,v in data.items()]),
        ','.join(['%s' for k,v in data.items()]),
        )

        try:
            cursor.execute(sql,[v for k,v in data.items()])
            d.commit()
        except:
            print('失败')
            d.rollback()
    
    def parse_url(self):
        response = requests.get(self.url,self.req_headers)
        # print(response.text)
        result = etree.HTML(response.text)
        # print(result)
        #获取二手房的url链接
        ershou_url = result.xpath('//div[@class="nav typeUserInfo"]/ul/li[1]/a/@href')[0]
        # print(ershou_url)
        self.ershoufang_parse(ershou_url)

        #获取租房的url链接
        zufang_url = result.xpath('//div[@class="nav typeUserInfo"]/ul/li[3]/a/@href')[0]
        # print(zufang_url)
        self.zufang_parse(zufang_url)

    def ershoufang_parse(self,ershou_url):
        # print(ershou_url)
        response = requests.get(ershou_url,self.req_headers)
        # print(response.text)
        result1 = etree.HTML(response.text)
        zong = result1.xpath('//div[@class="info clear"]')
        # print(zong)
        for i in zong:
            ctx = {}
            #标题
            title = i.xpath('./div[@class="title"]/a/text()')[0]
            # print(title)
            a = i.xpath('./div[@class="address"]/div[@class="houseInfo"]/text()')
            #型号，一室一厅
            xinghao = a[0]
            #面积
            area = a[1]
            #方向
            fangxiang = a[2]
            #精装
            jingzhuang = a[3]
            #有无电梯
            if len(a) > 4:
                dianti = a[4]
                ctx1 = {
                    'dianti':dianti[0]
                }
                #update方法将字典更新到另一个字典里面
                ctx.update(ctx1)
            b = i.xpath('./div[@class="flood"]/div[@class="positionInfo"]/text()')
            # print(b)
            #楼层
            louceng = b[0]
            #建楼时间
            date = b[1]
            c = i.xpath('./div[@class="followInfo"]/text()')
            # print(c)
            #多少人关注
            num = c[0]
            #多少次观看
            movie = c[1]
            price = i.xpath('./div[@class="followInfo"]/div[@class="priceInfo"]/div[@class="totalPrice"]/span/text()')[0]
            # print(price)
            # 单价
            danjia = i.xpath('./div[@class="followInfo"]/div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()')[0]
            # print(danjia)

            ctx2 = {
                'title':title,
                'xinghao':xinghao,
                'area':area,
                'fangxiang':fangxiang,
                'jingzhuang':jingzhuang,
                'louceng':louceng,
                'date':date,
                'num':num,
                'movie':movie,
                'price':price,
                'danjia':danjia,
            }
            ctx.update(ctx2)
            # print(ctx)
            d = self.db()
            self.insert_ershou(d,ctx)






    def zufang_parse(self,zufang_url):
        response = requests.get(zufang_url,self.req_headers)
        result = etree.HTML(response.text)
        # print(result)
        zong = result.xpath('//ul[@id="house-lst"]/li')
        # print(len(zong))
        for i in zong:
            wxldict = {}
            #标题
            title = i.xpath('.//div[@class="info-panel"]/h2/a/text()')[0]
            # print(title)
            #地址
            address = i.xpath('.//div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/a/span/text()')[0]
            # print(address)
            #房子型号,二室一厅
            xinghao = i.xpath('.//div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span[@class="zone"]/span/text()')[0]
            # print(xinghao)
            #房子面积
            area = i.xpath('.//div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span[2]/text()')[0]
            # print(area)
            #房子方向
            fangxiang = i.xpath('.//div[@class="info-panel"]/div[@class="col-1"]/div[@class="where"]/span[3]/text()')[0]
            # print(fangxiang)
            #某某租房
            moumouzufang = i.xpath('.//div[@class="info-panel"]/div[@class="col-1"]/div[@class="other"]/div[@class="con"]/a/text()')[0]
            # print(moumouzufang)
            #楼层与建楼时间
            zongshu = i.xpath('.//div[@class="info-panel"]/div[@class="col-1"]/div[@class="other"]/div[@class="con"]/text()')
            # print(louceng)
            louceng = zongshu[0]
            date = zongshu[1]
            # print(louceng,date)
            #交通，距离车站
            jiaotong = i.xpath('.//div[@class="info-panel"]/div[@class="col-1"]/div[@class="chanquan"]/div[@class="left agency"]/div[@class="view-label left"]/span[@class="fang-subway-ex"]/span/text()')
            if len(jiaotong) > 0:
                dict1 = {
                    'jiaotong':jiaotong[0]
                }
                wxldict.update(dict1)
                
            #精装修
            jingzhuangxiu = i.xpath('.//div[@class="info-panel"]/div[@class="col-1"]/div[@class="chanquan"]/div[@class="left agency"]/div[@class="view-label left"]/span[@class="decoration-ex"]/span/text()')
            if len(jingzhuangxiu) > 0:
                dict2 = {
                    'jingzhuangxiu':jingzhuangxiu[0]
                }
                wxldict.update(dict2)
            #集中供暖
            jizhonggongnuan = i.xpath('.//div[@class="info-panel"]/div[@class="col-1"]/div[@class="chanquan"]/div[@class="left agency"]/div[@class="view-label left"]/span[@class="heating-ex"]/span/text()') 
            if len(jizhonggongnuan) > 0:
                dict3 = {
                    'jizhonggongnuan':jizhonggongnuan[0]
                }
                wxldict.update(dict3)
                
                    
            #房月租
            price = i.xpath('.//div[@class="info-panel"]/div[@class="col-3"]/div[@class="price"]/span[@class="num"]/text()')[0]
            # print(price) 
            # 更新时间      
            gengxinshijian = i.xpath('.//div[@class="price-pre"]/text()')[0]
            # print(gengxinshijian)
            
            dict4 = {
                'title':title,
                'address':address,
                'xinghao':xinghao,
                'area':area,
                'fangxiang':fangxiang,
                'moumouzufang':moumouzufang,
                'louceng':louceng,
                'date':date,
                'price':price,
                'gengxinshijian':gengxinshijian,
                
            }
            wxldict.update(dict4)
            # print(wxldict)
            d = self.db()
            self.hebingzidian(d,wxldict)
            

def main():
    url = 'https://bj.lianjia.com/'
    req_headers = {
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    }
    wxl = Wxlxiangmu(url,req_headers)
    wxl.parse_url()

if __name__ == '__main__':
    main()




