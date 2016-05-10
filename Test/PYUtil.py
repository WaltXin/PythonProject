import urllib
import random

def plus(*args):
    total = 0
    for n in args:
        total+=n
    print(total)

def multiplication(*args):
    total = 1
    for n in args:
        total*=n
    print(total)

def download_image(url):
    name = str(random.randrange(1, 100))+'.jpg'
    urllib.request.urlretrieve(url, 'a.jpg')

def createFile():
    fw = open('sample.txt', 'w')
    fw.write('this is a test file\n')
    fw.write(':)\n')
    fw.close()


def storage():
    name = {'walt': 'super handsome', 'mark': 'tall', 'dave': 'smart'}
    if 'walt' in name:
        print(name['walt'])
        for k, v in name.items():
            print(k + v)









