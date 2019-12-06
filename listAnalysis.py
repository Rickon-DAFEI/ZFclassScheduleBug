import requests
import io
import sys
from bs4 import BeautifulSoup
from PIL import Image
import urllib3
import os
import codecs

f = open('名单.html','rt')
l = BeautifulSoup( f ,"html.parser")
studentList__VIEWSTATE = l.find('input', attrs={'name': '__VIEWSTATE'})['value']
List = {}
a_list = l.find(id="kcmc")
classList = a_list.contents

