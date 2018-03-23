import itchat
from itchat.content import *
import os
import hot_film
import time

name_htmls = hot_film.get_hot_film() #热映电影对应的html
print(name_htmls)
#将电影名字转换成字符串
all_name = ''
for name in name_htmls:
    all_name += (name + ' ' + '\n')

itchat.auto_login(hotReload = True)

@itchat.msg_register(TEXT, isFriendChat=True, isGroupChat=True)
def simple_reply(msg):
    #当消息为热映电影时发送热映电影名字
    if msg.Text == '热映电影':
        if msg.toUserName == itchat.search_friends(name='那颗骄傲而不知疲惫的心')[0]['UserName']: #如果接收方是本人，仅发送给发送方，否则发给接收方（即本人发送）
            itchat.send_msg(all_name, toUserName=msg.FromUserName)
        else:
            itchat.send_msg(all_name, toUserName=msg.toUserName)
    #通过消息判断电影并将其信息发送
    for name in name_htmls: #迭代key
        if msg.text in name:
            film_html = name_htmls[name]    #通过名称得到html
            film_info = hot_film.get_movie_info(film_html)  #获取电影信息
            infos = ''
            for info in film_info:  #将消息转化为字符串
                infos += (info + ':' + film_info[info])
            if msg.toUserName == itchat.search_friends(name='那颗骄傲而不知疲惫的心')[0]['UserName']:                
                itchat.send_msg(infos, toUserName=msg.FromUserName)
            else:

                itchat.send_msg(infos, toUserName=msg.toUserName)
            #return infos
    for name in name_htmls:
        movie_name = msg.Text.split('海报')[0]
        if '海报' in msg.Text and movie_name in name: #判断消息中是否含有海报并且含有热映电影名
            if msg.toUserName == itchat.search_friends(name='那颗骄傲而不知疲惫的心')[0]['UserName']:            
                itchat.send_msg('Please wait a minute...', toUserName=msg.FromUserName)
            else:
                itchat.send_msg('Please wait a minute...', toUserName=msg.toUserName)
            print(movie_name)
            dir_name = name.split(':')[0].split('.')[0] #将字典中key去除‘：’和‘.’
            print(dir_name)
            #创建文件夹，如果已经创建--pass
            try:
                os.mkdir(dir_name)
                os.chdir(dir_name)

                film_html = name_htmls[name]
                hot_film.download_poster(film_html, True)
            
                os.chdir(os.pardir)
            except FileExistsError:
                print("Error!")
                pass
            #遍历工作文件夹
            movie_dir = os.walk(os.curdir)
            for each in movie_dir:
                movie_name = name.split(':')[0].split('.')[0] #去除消息中的':'和'.'
                if movie_name in each[0]:
                    os.chdir(movie_name)
                    movie_poster = os.walk(os.curdir)
                    for posters in movie_poster:
                        print(posters)
                        for each_poster in posters[2]:
                            time.sleep(1)
                            if msg.toUserName == itchat.search_friends(name='那颗骄傲而不知疲惫的心')[0]['UserName']:            
                                itchat.send_image(each_poster, toUserName=msg.FromUserName)
                            else:
                                itchat.send_image(each_poster, toUserName=msg.toUserName)
                    os.chdir(os.pardir)
itchat.run()

