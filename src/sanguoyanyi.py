#需求：爬取三国演义小说所有的章节标题和章节内容http://www.shicimingju.com/book/sanguoyanyi.html
import requests
from bs4 import BeautifulSoup
import re

def pre_process(text):
    regex = re.compile(r' |　|	|\n| |')  # 建立模式，匹配多种空格（直接从输出文档中选取）和html语言（&nbsp;）
    text = re.sub(regex, '', text)   # 将上一行匹配的空格之类的东西替换成空，也就是删掉
    # text.replace(u'\xa0', u' ')
    return text

if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36 Edg/95.0.1020.40',
    }
    url = 'https://www.shicimingju.com/book/sanguoyanyi.html'
    page_text = requests.get(url=url, headers=headers).text
    # print(page_text)
    soup = BeautifulSoup(page_text, 'html.parser')   # 此处使用html.parser  若使用lxml需要先安装，指令：pip install lxml
    title_list = soup.select('.book-mulu > ul > li')   # 匹配到标题元素   .book-mulu是class选择器
    # print(title_list)
    with open('../output/sanguo.txt', 'w', encoding='utf-8') as fp:
        # 遍历列表中每个标题
        for i in range(len(title_list)):
            # 网页的编码方式为iso-8859-1（获取方法：网页F12的控制台输入命令：document.charset）
            title_text = title_list[i].a.string.encode('iso-8859-1').decode('utf-8')  # 转码（处理乱码）

            detail_url = 'https://www.shicimingju.com' + title_list[i].a['href']  # 构造详细页的url

            detail_page = requests.get(url=detail_url, headers=headers)
            detail_page.encoding = detail_page.apparent_encoding  # 处理乱码

            detail_page_text = detail_page.text
            # print(detail_page_text)
            detail_soup = BeautifulSoup(detail_page_text, 'lxml')  # 需要先pip install lxml，否则报错，也可以替换成上面用的html.parser

            content = detail_soup.select('.chapter_content')  # class选择器
            content_text = content[0].text   # 因为返回的（好像）是一个列表，所以要切片，即[0]
            content_text = pre_process(content_text)   # 调用函数对数据进行处理，去除空格和不必要的换行，函数定义见上
            #content_text.encode('iso-8859-1').decode('utf-8')
            # print(content_text)

            # print(content_text)
            fp.write(title_text + '\n' + content_text + '\n\n')
            print(title_text + ' 爬取成功')

