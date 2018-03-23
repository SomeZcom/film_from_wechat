#-*-coding:utf-8-*- #编码声明，不要忘记！
import requests  #这里使用requests，小脚本用它最合适！
import bs4 #BeautifulSoup简直碉堡了！！！
import os

#豆瓣模拟登录，最简单的是cookie，会这个方法，80%的登录网站可以搞定
headers = {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie' : 'll="118318"; \
        bid=RSlv1g9RSbA; ps=y; __yadk_uid=fAPsIpqMTPbkm9QSDh50Q0iNfZzLcNUh; \
        gr_user_id=34aee960-cd0f-4c1d-9df0-94ef392e33f9; _ga=GA1.2.788953411.1510563465; \
        _gid=GA1.2.236300223.1512569678; dbcl2="144671833:GvBY0DfS5aI"; ck=bw7b; ap=1; __utmt=1; \
        _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1512655780%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; \
        _pk_id.100001.4cf6=322fc668e86bcae3.1511008950.16.1512655780.1512649639.; _pk_ses.100001.4cf6=*; \
        __utma=30149280.788953411.1510563465.1512649639.1512654463.26; __utmb=30149280.12.10.1512654463; \
        __utmc=30149280; __utmz=30149280.1512654463.26.23.utmcsr=hao123.com|utmccn=(referral)|utmcmd=referral|utmcct=/; \
        __utmv=30149280.14467; __utma=223695111.788953411.1510563465.1512649639.1512655780.17; __utmb=223695111.0.10.1512655780; \
        __utmc=223695111; __utmz=223695111.1512655780.17.15.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; \
        push_noty_num=0; push_doumail_num=0; \
        _vwo_uuid_v2=8E3342D9DCEB15E83D1877914B03EA57|de1882244f8c60aeaef140b263d6f400',
        'Host':'movie.douban.com',
        'Referer':'https://www.douban.com/',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',
    }
proxies = {'http':'http://114.228.8.82:80'}

img_header = {'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36 LBBROWSER',}

#重点来了！用requests，装载headers，请求网站
def get_tree(url):
    
    try:
        page = requests.get(url, headers = headers, proxies = proxies)
        tree = bs4.BeautifulSoup(page.text, 'lxml')
        print(page.status_code)
        return tree
    except:
        get_tree(url)

#获得正在上映的电影打开衔接
def get_hot_film():

    hot_movie_tree = get_tree('https://movie.douban.com/')
    li_title = hot_movie_tree.find_all('li', class_='title')

    name_html = {} #名字对应html的字典
    
    for html in li_title:
        open_html = html.a['href']  #每个电影对应的html
        film_name = html.a.text

        name_html[film_name] = open_html
        print(html)
 
    return name_html
        

        
#获取电影信息
def get_movie_info(html):
    
    movie_info = {}
    movie_tree = get_tree(html)

    movie_average = movie_tree.find('strong', property='v:average')
    movie_info['豆瓣评分'] = movie_average.text + '\n'
    try:
        movie_runtime = movie_tree.find('span', property='v:runtime')
        movie_info['时长'] = movie_runtime.text + '\n'
    except AttributeError:
        pass

    movie_name = movie_tree.find('span', property='v:itemreviewed')
    movie_info['电影名'] = movie_name.text + '\n'

    movie_years = movie_tree.find_all('span', property='v:initialReleaseDate')
    movie_info['上映年份'] = ''
    for year in movie_years: 
        movie_info['上映年份'] += (year.text + ' ')
    movie_info['上映年份'] += '\n'

    movie_types = movie_tree.find_all('span', property='v:genre')
    movie_info['类型'] = ''
    for movie_type in movie_types:
        movie_info['类型'] += (movie_type.text + ' ')
    movie_info['类型'] += '\n'

    span_attrs = movie_tree.find_all('span', class_='attrs')
    try:
        movie_info['导演'] = span_attrs[0].text.replace(' / ', ' ') + '\n'
        movie_info['编剧'] = span_attrs[1].text.replace(' / ', ' ') + '\n'
        movie_info['主演'] = span_attrs[2].text.replace(' / ', ' ') + '\n'
    except IndexError:
        movie_info['导演'] = span_attrs[0].text.replace(' / ', ' ') + '\n'
        movie_info['主演'] = span_attrs[1].text.replace(' / ', ' ') + '\n'

    span_pls = movie_tree.find_all('span', class_='pl')
    for span_pl in span_pls:
        if span_pl.text == '制片国家/地区:':
            movie_info['制片国家/地区'] = span_pl.next_sibling + '\n'
        elif span_pl.text == '语言:':
            movie_info['语言'] = span_pl.next_sibling.replace(' / ', ' ') + '\n'
        elif span_pl.text == 'IMDb链接:':
            movie_info['IMDb链接'] = span_pl.next_sibling.next_sibling['href'] + '\n'
        

    print(movie_info)

    return movie_info
    
#下载电影海报
def download_poster(url, recur):

    if recur:
        movie_tree = get_tree(url)
        movie_poster = movie_tree.find('div', id='mainpic')
        print(movie_poster.a['href'])
        url = movie_poster.a['href']
    img_tree = get_tree(url)

    posters = img_tree.find_all('div', 'cover')
    for poster in posters:
        print(poster.a.img['src'])
        html = poster.a.img['src'].replace('webp', 'jpg')
        img_content = requests.get(html, headers = img_header).content
        filename = html.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(img_content)
            

    span_next = img_tree.find('span', class_='next')
    print(span_next)
    if span_next == None:
        print('span_next = None')
    else:
        try:
            next_poster_page = span_next.a['href']
            print(next_poster_page)
            download_poster(next_poster_page, False)
        except TypeError:
            pass

