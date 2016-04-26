import requests
from lxml import html
import re
import os
from timeit import default_timer
from pymongo import MongoClient


def make_dict(img_urls, c_name):
    comic = {'name': c_name,
             'urls': img_urls}
    return comic

headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/47.0.2526.111 Safari/537.36',
    }

def do_everything():
    cookie = {
        'mfsid':'3blafc8l8g3b1dp2bhr9ei2p93',
        'mfvb_sessionhash':'6a6dbe85cb66ffa95616a34e5be5f84d',
        'mfvb_lastvisit':'1453771288',
        '__unam':'657356c-1527b857651-27ac629d-41',
    }
    headers = {
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/47.0.2526.111 Safari/537.36',
    }

    start = default_timer()

    print('finding urls...')
    find_name = re.compile("/(c.*)/")
    page = requests.get('http://mangafox.me/manga/onepunch_man',
                        cookies=cookie,headers=headers)
    tree = html.fromstring(page.content)
    bad_urls = tree.xpath("//ul[contains(@class,'chlist')]//@href")
    urls = list(filter(lambda x: 'action' not in x, bad_urls))

    client = MongoClient()
    db = client.one_punch
    punch = db.one_punch

    for i in range(len(urls)):
        # getting urls for each comic issue
        urls[i] = urls[i].replace('1.html', '')
        page = requests.get(urls[i])
        tree = html.fromstring(page.content)

        # getting the number of pages for each comic issue
        count = tree.xpath("//div[contains(@class,'l')]//option//text()")
        count = list(set(count))
        count = list(filter(lambda x: x.isdigit(), count))
        count = len(count)

        # the name of each comic issue
        c_name = (re.findall(find_name, urls[i])[0].replace('.', '_'))

        img_urls = []
        print(default_timer()-start)
        # each of the pages image urls
        for j in range(1, count+1):
            page = requests.get(urls[i] + str(j) + '.html')
            print(default_timer() - start)
            tree = html.fromstring(page.content)
            img_src = tree.xpath('//div[contains(@class,'
                                 '"read_img")]//img//@src',)[0]
            if isinstance(img_src, str):
                img_urls.append(img_src)
        dict_urls = (make_dict(img_urls, c_name))
        punch.insert_one(dict_urls)
    return 'done'


def make_folders(final, comic_name):
    print('making folders')
    headers = {'Content-Type': 'image/jpeg'}
    for name, urls in final[0].items():
        os.makedirs('/Users/jasminder88/Desktop/' + comic_name + '/' + name +
                    '/')

        for index, url in enumerate(urls):
            print(url)
            filename = 'page_{0}.jpg'.format(index)
            file_name = '/Users/jasminder88/Desktop/' + comic_name + '/' + \
                        name + '/' + filename

            resp = requests.get(url, headers=headers)
            f = open(file_name, 'wb')
            f.write(resp.content)
            f.close()


def make_folder_from_db(path):
    client = MongoClient()
    db = client.one_punch
    punch = db.one_punch
    os.makedirs(path)
    timer = default_timer()
    for doc in punch.find():
        urls = doc['urls']
        name = doc['name']
        os.makedirs(path + '/' + name)
        for page_num in range(len(urls)):
            page = 'page_{0}.jpg'.format(page_num+1)
            file_name = path + '/' + name + '/' + page

            response = requests.get(urls[page_num],headers=headers)

            f = open(file_name, 'wb')
            f.write(response.content)
            f.close()
        print(default_timer()-timer)

if __name__ == '__main__':

    print('start')
    comic_name = 'One_Punch_Man'
    path = 'comics/' + comic_name

    make_folder_from_db(path)

    print('done')
