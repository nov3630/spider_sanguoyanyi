import re

# 以下内容为补丁，为了删掉多余的空行
content_all = ''  # 声明储存内容的变量

def is_title(text):
    regex = re.compile(r'^第(.*)回·[\s\S]*')  # 建立匹配标题的模式
    result = regex.search(text)
    # 如果匹配不到标题行，就返回False，匹配到了就返回True
    if result != None:
        return True
    return False

if __name__ == '__main__':
    # 读取文件，并将非空行放进content_all中
    with open('../output/sanguo.txt', 'r', encoding='utf-8') as fp:
        # 对每行进行操作
        for line in fp:
            # 如果是标题行并且不是第一行，那么就在前面增加一个空行，也就是两个换行符
            if is_title(line) and content_all != '':
                content_all += '\n\n'
            # 如果是空行，就删掉
            if len(line) == 0:
                continue
            # 将内容去掉首尾空格添加到content_all里去
            content_all += line.strip()
            # 如果是标题行，就换行
            if is_title(line):
                content_all += '\n'
    # 将content_all写入到文件中
    with open('../output/sanguo_patch.txt', 'w', encoding='utf-8') as fp:
        fp.write(content_all)

