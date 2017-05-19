# -*- encoding:utf-8 -*-
##############################
__author__ = "LiBaiwei"
__date__ = "2016/10/06"
###############################

import requests
from bs4 import BeautifulSoup
import urllib
import re
def login():
    loginUrl = 'https://accounts.douban.com/login'
    formData={
        "redir":"https://movie.douban.com/people/beattywell/collect",
        "form_email":'775891727@qq.com',
        "form_password":'qwe123456789',
        "login":u'登录'
    }
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:48.0) Gecko/20100101 Firefox/48.0"}
    r = requests.post(loginUrl,data=formData,headers=headers)
    page = r.text

    '''''获取验证码图片'''
    #利用bs4获取captcha地址
    soup = BeautifulSoup(page,"html.parser")
    captchaAddr = soup.find('img',id='captcha_image')['src']
    #利用正则表达式获取captcha的ID
    reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
    captchaID = re.findall(reCaptchaID,page)
    #print captchaID
    #保存到本地
    urllib.urlretrieve(captchaAddr,"captcha.jpg")
    captcha = raw_input('please input the captcha:')

    formData['captcha-solution'] = captcha
    formData['captcha-id'] = captchaID

    r = requests.post(loginUrl,data=formData,headers=headers)
    page = r.text
    if r.url=='https://movie.douban.com/people/beattywell/collect':
        print 'Login successfully!!!'
        print '我看过的电影','-'*60
        #获取看过的电影
        soup = BeautifulSoup(page,"html.parser")
        result = soup.findAll('li',attrs={"class":"title"})
        pattern = re.compile('https://movie.douban.com/subject/(.*)/')
        for item in result:
            match = re.search(pattern,str(item))
            print match.group(1)
    else:
        print "failed!"
if __name__ == '__main__':
    login()