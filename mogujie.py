import requests,re,time,pymysql
from lxml import etree
from selenium import webdriver

class WxlMogujieSpider(object):
    def __init__(self,url):
        self.url = url

    def start_project(self):
        self.parse_first_url()
    
    def db(self):
        client = pymysql.connect(host='localhost', port=3306,database='mogujie',user='root', password='python3..', charset='utf8')
        print('连接成功')
        return client
    
    #存放数据
    def insert_data(self,db,data,table_name):
        #创建游标
        cursor = db.cursor()
        #数据库去重的关键字,INSERT IGNORE INTO 或者 REPLACE INTO
        sql = """
        INSERT INTO {}(%s) VALUES(%s)
        """.format(table_name)%(','.join([k for k,v in data.items()]),
        ','.join(['%s' for k,v in data.items()]),
        )
        try:
            cursor.execute(sql,[v for k,v in data.items()])
            db.commit()
        except:
            print('失败')
            db.rollback()


    #selenium配置
    def selenium_peizhi(self,url):
        opt = webdriver.ChromeOptions()
        opt.set_headless()
        #创建chrome无界面对象
        driver = webdriver.Chrome(
                options=opt, executable_path='/home/wxl/桌面/chromedriver')
        time.sleep(3)
        driver.get(url)
        # driver.implicitly_wait(10)
        #获取页面的源码信息
        html = driver.page_source
        soup = etree.HTML(html)
        return soup


    #提取首页一级菜单,使用selenium属于耗时操作
    def parse_first_url(self):
        #调用selenium驱动
        soup = self.selenium_peizhi(self.url)
        zong = soup.xpath('//div[@class="pc_indexPage_nav_menu fl cube-acm-node has-log-mod"]/ul/li')    
        #设置插入主键id
        nums = 1
        for i in zong:
            title1 = i.xpath('./dl/dt/a/text()')[0]
            url1 = i.xpath('./dl/dt/a/@href')[0]
            ctx = {
                'id':nums,
                'title':title1,
                'url':url1
            }
            db = self.db()
            self.insert_data(db,ctx,'yiji_fenlei')
            url = 'https:{}'.format(url1)
            self.parse_er_url(url,nums)


            title2 = i.xpath('./dl/dd/span//a/text()')
            url2 = i.xpath('./dl/dd/span//a/@href')
            #去除列表里面空格方法
            while ' ' in title2:
                title2.remove(' ')
            num = 0
            for title in title2:
                nums+=1
                ctx1 = {
                    'id':nums,
                    'title':title,
                    'url':url2[num]
                }              
                db = self.db()
                self.insert_data(db,ctx1,'yiji_fenlei')         
                url = url2[num]
                url1 = 'https:{}'.format(url)
                self.parse_er_url(url1,nums)
                num+=1
            nums+=1

    #提取第二页的所有url,这些url使用selenium属于耗时操作
    def parse_er_url(self,url,nums):
        soup = self.selenium_peizhi(url)
        result = soup.xpath('//div[@id="wall_goods_box"]/div[2]/div/div/a[2]/@href')
        for url in result:
            self.parse_detail_data(url,nums)

    #提取详情页数据字段
    def parse_detail_data(self,url,nums):
        print(nums)
        soup = self.selenium_peizhi(url)
        ctx = {}
        #图片地址
        img = soup.xpath('//div[@id="J_GoodsImg"]/div[1]/button/img/@src')
        if img != []:
            ctx['img'] = img[0]
        #标题
        title = soup.xpath('//div[@id="J_GoodsInfo"]/div/h1/span[2]/text()')
        if title != []:
            ctx['title'] = title[0]
        #原价格
        original_price = soup.xpath('//span[@id="J_OriginPrice"]/text()')
        if original_price != []:
            ctx['original_price'] = original_price[0]
        #促销价
        promotional_price = soup.xpath('//span[@id="J_NowPrice"]/text()')
        if promotional_price != []:
            ctx['promotional_price'] = promotional_price[0]
        #评价
        evaluate = soup.xpath('//dd[@class="property-extra fr"]/span[1]/span/text()')
        if evaluate != []:
            ctx['evaluate'] = evaluate[0]
        #累积销量
        cumulative_sales_volume = soup.xpath('//dd[@class="property-extra fr"]/span[2]/span/text()')
        if cumulative_sales_volume != []:
            ctx['cumulative_sales_volume'] = cumulative_sales_volume[0]
        #库存
        stock = soup.xpath('//div[@class="J_GoodsStock goods-stock fl"]/text()')
        if stock != []:
            ctx['stock'] = stock[0]
        #商品描述
        commodity_Description = soup.xpath('//div[@class="graphic-text"]/text()')
        if commodity_Description != []:
            ctx['commodity_Description'] = commodity_Description[0]
        #商品参数
        ctx['commodity_parameter'] = ','.join(soup.xpath('//table[@id="J_ParameterTable"]/tbody/tr//td/text()'))
        #穿着效果
        ctx['wearing_effect'] = ','.join(soup.xpath('//div[@id="J_Graphic_穿着效果"]//div/div/img/@src'))     
        ctx['title_id_id'] = nums
        print(ctx)
        db = self.db()
        self.insert_data(db,ctx,'parse_data')



def main():
    url = 'https://market.mogujie.com/?acm=3.mce.1_10_1ksak.128391.0.0j2UMrjgbMFJt.pos_0-m_484866sd_119&ptp=1.n5T00.0.0.1ijE6HZX'

    wxlmogujie = WxlMogujieSpider(url)
    wxlmogujie.start_project()

if __name__ == "__main__":
    main()






