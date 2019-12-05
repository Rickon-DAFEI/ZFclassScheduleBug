import requests
import io
import sys
from bs4 import BeautifulSoup
from PIL import Image
import urllib3
import codecs
import os
#import getMassage
session = None
res = requests.Session()
rqs = requests.session()
Origin_url = "http://jwxt.zjyc.edu.cn/" # 教务系统网址
url = "http://jwxt.zjyc.edu.cn//default2.aspx"
checkcodeURL = Origin_url+'CheckCode.aspx'  #验证码网址
head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36","Connection": "keep-alive"}
post_data = {"Textbox1" : "" ,"txtSecretCode":"","RadioButtonList1":"%D1%A7%C9%FA","Button1":"","lbLanguage":"","hidPdrs":"","hidsc":"", 'Button1': ''}
#user_name = '201808140313'
#user_password = 'wy012233'
user_name=input("请输入学号")
user_password = input("请输入密码")

def xm_Code(xmcode):
    heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'}
    code_data = {'content': xmcode,'charsetSelect': 'gb2312','en': 'UrlEncode编码'}
    code_url = 'http://tool.chinaz.com/tools/urlencode.aspx'
    coding_site = rqs.post(code_url,headers =heads,data = code_data)
    s = coding_site.content
    coding_site=str(s)
    code_bs = BeautifulSoup(coding_site,"html.parser")
    xm_str = code_bs.find('textarea',id = "content").text
    return xm_str

def setHeaders(refererURL):
        headers = self.originHeaders
        headers['Referer'] = refererURL
        return headers

def get_photo(URL):
    checkcode = res.get(checkcodeURL, headers=head)
    with open('code.gif', 'wb') as fp:  #保存验证码图片
         fp.write(checkcode.content)
    image = Image.open('code.gif'.format(os.getcwd()))
    image.show()
    post_data['txtSecretCode'] = input("请输入图片中的验证码: ")  

def login():
    post_data["txtUserName"] = user_name
    post_data["TextBox2"]=  user_password 
    login_page_url = Origin_url + "default2.aspx"
    head['Referer'] = login_page_url
    get_photo(url)
    loginPage = rqs.get(url)
    loginPage = str(loginPage.content.decode('gbk'))
    VIEW= BeautifulSoup(loginPage,"html.parser")
    post_data['__VIEWSTATE'] = VIEW.find('input', attrs={'name': '__VIEWSTATE'})['value']
    #<input type="hidden" name="__VIEWSTATE" value="dDwxNTMxMDk5Mzc0Ozs+jtB/FDqlGA8WDqG9qEJzHroJ09U=">
    #print(post_data['__VIEWSTATE'])
    homePage = res.post(login_page_url, data=post_data, headers=head) 
    cookies = homePage.cookies
    with open('1.html','wb')as file:
        file.write(homePage.content)
    homePage = str(homePage.content.decode('gbk'))
    bs = BeautifulSoup(homePage,"html.parser")
    try:
        xm= bs.find('span',id="xhxm").text
        xmcode=xm[:-2]
        print("学生："+xmcode+"登陆成功")
        xmcode = xm_Code(xmcode)
        getClassSchedule(xmcode)
    except:
        print("验证码输入错误!")

def getClassSchedule(xm):
    #jwxt.zjyc.edu.cn/xskbcx.aspx?xh=201808140313&xm=%CD%F5%D3%EE&gnmkdm=N121603
    res.headers['Referer'] = Origin_url + "/xs_main.aspx?xh="+user_name
    url = Origin_url +'xskbcx.aspx?xh='+user_name+"&xm="+xm+"&gnmkdm=N121603"
    response = res.get(url, allow_redirects=False)
    with open('课表.html','wb')as f:
        f.write(response.content)
  #  viewState = getClassScheduleFromHtml(response)["__VIEWSTATE"]
  #  content=getClassScheduleFromHtml(response)["content"]

def class_table(table_html):
      pass 
def main():
    res = login() 
    class_table(res)
if __name__ == "__main__":
    main() 