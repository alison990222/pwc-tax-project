
# 增值税税收分类编码自动匹配模型 

- Develop VAT classification code automatic matching system (Given a random product name, the system will output the matching/recommend VAT code)
- Skills used: NLP(Python Sklearn), web crawler(crawling Taobao), server deployment(AWS ubuntu), web application(Django)

### 1. 数据简介

- 商品和服务税收分类编码表.xls中共有409大类，4205小类

- 轻工业，重工业类，化学类的细项看起来比较多一些。


 <img src="https://github.com/alison990222/pwc-tax-project/blob/master/pic/1.png" width = "400"  align=center />

- 主要选择食品类的部分进行研究（44类）

![image](https://github.com/alison990222/pwc-tax-project/blob/master/pic/2.png)


  

### 2.  数据扩充：淘宝爬虫

   - 扩充方法：

     使用 `商品和服务分类简称` 关键字在淘宝（天猫）进行搜索，爬取搜索到的商品加入到数据库。

   - 爬取到的raw data 存储在webCrawlData.csv

   - 步骤：

     - 去除部分`商品和服务分类简称`（部分的搜索关键字不合适）。如：
       - 名称含有“其他”：其他未列明水果
       - 含有数字的关键词：每吨不超过3000元的啤酒
       - 去括号：暂时保藏水果及坚果（原料）
     - 网页端登入后获取cookie（淘宝需登入才能搜索）
     - 将cookie加入到头部，随机每15～30发送一次请求（避免频繁操作账号被锁起）
     - 每个商品分类爬取maximum48个数据（淘宝网页版一页48个数据）
     - 共爬取到10420条数据（仅爬取食物相关商品）

- 数据清理：去掉国名，量词，数字，（包邮，直营，网红），【第二件半价】，不符合期望标题者（如下）

  绿豆：中秋月饼模具绿豆糕模型印具家用烘焙冰皮糕点心不沾手压花工模具

  苹果：apple 产品

### 3. 核心算法介绍：文本分类算法

> 流程：输入商品名 -> 使用分类模型获取商品分类（大类，搜索结果） -> 使用分类模型获取商品具体分类（细项，结果排序）->  输出编码

分大类细项的原因是大类之下的细项有些并不能从名称体现。譬如：“轻量可收成小包羽绒背心”可以是女上衣也可以是男上衣，需要用户自己选择分属哪个细项。或者像“打发淡奶油”，“卡仕达奶油” 根据成分分成两个编码，无法单从名称得知，需用户自己选择。此外使用两段式分类有助于分类的准确性，譬如先将结果分到400类中的其中一类，再分10类，会比一次性将数据分到4000类中的一类佳。

<img src="https://github.com/alison990222/pwc-tax-project/blob/master/pic/3.png" width = "600"  align=center />


- 几个商品分类的 top15 关键词展示

 <img src="https://github.com/alison990222/pwc-tax-project/blob/master/pic/4.png" width = "800"  align=center />


- 难点，尝试：

  - 尝试模型训练的一些performance：

    这个训练集是最basic的4205条数据划分7:3（训练, 测试）的表现。

 <img src="https://github.com/alison990222/pwc-tax-project/blob/master/pic/5.png" width = "300"  align=center />


  - 小分类部分：

    原本想使用字符串相似度进行这部分的分离，但是发现了几个问题：

    1. 太过复杂的字符串比对时间较长
    2. 文本近似度distance 方法在字符串较短时表现很好，但在字符串长时经常跑不出结果
    3. word2vec是一个计算近似度经典的算法，但是实验结果不佳。

    以上实验都可以在classification.ipynb查看。最终还是使用了文本分类算法进行二次分类，训练label改成商品小项名称。


### 4. 交互介绍

   - 客户端：

 <img src="https://github.com/alison990222/pwc-tax-project/blob/master/pic/6.png" width = "500"  align=center />

   - 网页端（管理员）可查看服务器上的数据

 <img src="https://github.com/alison990222/pwc-tax-project/blob/master/pic/7.png" width = "500"  align=center />

### 5. 其他功能

   - 用户可以新增数据到服务器数据库。每24小时会重新训练模型(GridSearch会自动挑选最佳参数，无需人为操作)。

### 6. 文件介绍

   - webCrawl.ipynb：爬取淘宝数据的代码，使用jupyter notebook。
   - multiLabel.ipynb：多标签分类 MultiLabel
   - classification.ipynb：分类
   - taxProject：server（后端代码）
   - webCrawlData.csv：淘宝爬取，尚未清洗的数据
   - chineseStopWords.txt：停词表

### 7. 测试流程

   - 仅运行客户端：（自动连接到服务器）
     1. 安装PyQt5  `sudo python3 -m pip install pyqt5==5.14`
     2. 运行python3 client.py

   - 使用API测试：

| url: 13.125.23.237:8000 | 方法 | 字段                                            | 说明               |
| ----------------------- | ---- | ----------------------------------------------- | ------------------ |
| /encoding               | GET  | -                                               | 查看编码表         |
| /database               | GET  | -                                               | 查看数据库中的数据 |
| /search                 | GET  | productName                                     | 搜索               |
| /insert                 | POST | item, code, <br />firstCategory, secondCategory | 插入数据           |

   - 在笔记本上运行server & client

     在 taxProject 文件夹下操作：

     1. 安装包 `pip install -r requirements.txt`

     2. 启动mysql 数据库，新建 `taxProject` 数据库。其他设定如下

     <img src="https://github.com/alison990222/pwc-tax-project/blob/master/pic/8.png" width = "200"  align=center />


     3. 运行 `python3 manage.py makemigrations` , `python3 manage.py migrate` , 插入数据

     4. 运行 `python3 manage.py runserver` 即启动 server

     5. 客户端启动方式如上（1）。此外client.py 第87行应更改为：server_ip = "127.0.0.1"。

### 8. 实验环境 / 语言

   - 主要开发语言：python3.6
   - 后端：使用Django RESTful API 

   - 前端：
     - 用户客户端： PyQT5
     - 管理者网页端：Django 

   - 数据库：MySQL （两张表。一张为encoding说明，另一张为产品对应的表）

   - 服务器：AWS EC2

### 9. 参考资料

   word2vec：https://www.kaggle.com/jerrykuo7727/word2vec

   text classification：https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge

