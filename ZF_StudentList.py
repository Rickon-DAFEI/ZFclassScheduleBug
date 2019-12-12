import requests
import io
import sys
from bs4 import BeautifulSoup
from PIL import Image
import urllib3
import os
import codecs

session  = None

res = requests.Session()
rqs = requests.session()

Origin_url = "http://jwxt.zjyc.edu.cn/"
login_url = "http://jwxt.zjyc.edu.cn//default2.aspx"

check_codeUrl = Origin_url+"CheckCode.aspx"

head = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36","Connection": "keep-alive"}
post_data = {'Textbox1':'none',"Button1":"","lbLanguage":"","hidPdrs":"","hidsc":""}
user_name = #
user_password = #
xm = user_name

def login():
    loginPage = rqs.get(login_url)
    loginPage = str(loginPage.content.decode('gbk'))
    VIEW= BeautifulSoup(loginPage,"html.parser")
    __VIEWSTATE= VIEW.find('input', attrs={'name': '__VIEWSTATE'})['value']
    post_data = {
            '__VIEWSTATE': __VIEWSTATE,
            'txtUserName': user_name,
            'TextBox2': user_password,
            'txtSecretCode': get_photo(),
            'RadioButtonList1': ("教师").encode('gb2312'),
            'Button1': '',
            'lbLanguage': '',
            'hidPdrs': '',
            'hidsc': '',
        }
    head['Referer'] = login_url
    homePage = res.post(login_url, data=post_data, headers=head) 
    cookies = homePage.cookies	
    with open('1.html','wb')as file:
        file.write(homePage.content)
    homePage = str(homePage.content.decode('gbk'))
    bs = BeautifulSoup(homePage,"html.parser")
    try:
        xm= bs.find('span',id="xhxm").text
        xmcode=xm[:-2]
        print("教师："+xmcode+"登陆成功")
    except:
        print("验证码输入错误!")
    xmcode = xm_Code(xmcode)
    get_classList()

def get_classList():
    res.headers['Referer'] ="http://jwxt.zjyc.edu.cn/js_main.aspx?xh="+user_name
    url = Origin_url+"/js_xkqk_gcxy.aspx?zgh="+user_name+"&xm="+xm+"&gnmkdm=N122304"   
    response = res.get(url, allow_redirects=False)
    with open('名单.html','wb')as f:
        f.write(response.content)
    response = str(response.content.decode('gbk'))
    classSoup = BeautifulSoup(response,"html.parser")
    studentList__VIEWSTATE = classSoup.find('input', attrs={'name': '__VIEWSTATE'})['value']
    a_list =classSoup.find(id="kcmc")
    classList = a_list.contents
    for each in classList:
        print(each.find('')["value"])

def get_photo():
    checkcode = res.get(check_codeUrl, headers=head)
    with open('code.gif', 'wb') as fp:
         fp.write(checkcode.content)
    image = Image.open('code.gif'.format(os.getcwd()))
    image.show()
    imageCode = input("请输入图片中的验证码: ") 
    return imageCode

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

def class_table(table_html):
      pass 

def main():
    res = login() 
    class_table(res)
if __name__ == "__main__":
    main() 
