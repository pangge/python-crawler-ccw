import sys
import re
import time
import math
import threading, zipfile
import urllib
import urllib.request
from urllib.parse import urlparse
from urllib.parse import urlsplit
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from Queue import Queue
from tkinter import filedialog



FILEDIR = 'H:/python程序/file/'

Urls_Content = {}
class FetchPage:
	"""docstring for fetchpage"""
	def __init__(self, url):
		self.url = url
	def fetch(self):
		req=urllib.request.Request(self.url)
		#req.add_header('Referer', 'self.url')
		req.add_header('User-agent', 'Mozilla/5.0')
		response = urllib.request.urlopen(req)
		return response
	def getcategory(self):
		filepdf = re.search(r'\.pdf\Z',self.url,re.IGNORECASE)
		if filepdf:
			try:
				self.getpdf()
			except:
				print('some error  ignored!')
				return None
			return 'pdf'
		filedoc = re.search(r'\.doc|\.docx\Z',self.url,re.IGNORECASE)
		if filedoc:
			try:
				self.getdoc()
			except:
				print('some error  ignored!')
				return None
			return 'doc'
		return None
	def getpdf(self):
		response = self.fetch()
		pdfurl = urlsplit(self.url)
		pdfname = pdfurl.geturl()
		purename = re.split('/',pdfname)
		f = open(FILEDIR+purename[-1],'wb')
		#print(Urls_Content)
		#f = open(PDFDIR+'/'+Urls_Content[url]+purename[-1],'wb')
		f.write(response.read())
		f.close()
		textin('PDF : '+purename[-1]+' 已下载...... ')
	def getdoc(self):
		response = self.fetch()
		pdfurl = urlsplit(self.url)
		pdfname = pdfurl.geturl()
		purename = re.split('/',pdfname)
		f = open(FILEDIR+purename[-1],'wb')
		f.write(response.read())
		f.close()
		textin('DOC : '+purename[-1]+' 已下载...... ')

class Crawl:
	def __init__(self,root_url):
		self.root=root_url
		self.urls=set()
		self.host = urlparse(root_url)[1]
	def craw(self):
		html_depth = 0
		Que = Queue()
		Que.put(self.root)
		Que.put('#level#') #help to count the html tree depth

		while not Que.empty():
			url = Que.get()
			#html_depth += 1
			if html_depth == 10:
				break
			if url == '#level#':
				html_depth += 1
				Que.put('#level#')
				print('html_deep ->'+html_depth.__str__())
				continue

			fetchpage = FetchPage(url)
			# download  file
			filetype = fetchpage.getcategory()
			if filetype is not None:
				continue

			self.urls.add(url)
			try:
				self.page = fetchpage.fetch()
			except:
				print('some error  ignored!')
				continue
			soup = BeautifulSoup(self.page)
			urllist = soup.findAll({'a':True})
			#print(urllist)
			for item in urllist:
				url_temp = item.get('href')
				url_content = item.get_text()#item.get('content')
				m = urlparse(url_temp)
				#print(m.geturl())
				url_temp = urljoin(url,m.geturl())
				if url_temp is not None and url_temp not in self.urls:
					#print(url_temp+url_content)
					Que.put(url_temp)
					self.urls.add(url_temp)
					Urls_Content[url_temp]=url_content

class multiSuperSpider(threading.Thread):
    def __init__(self, host,num):
        threading.Thread.__init__(self)
        self.host = host
        self.num = num
    def run(self):
        Crawler = Crawl(self.host)
        Crawler.craw()
        #textin('litte spider:',self.num.__str__(),+'--->'+self.host)

#Crawler = Crawl('http://papers.nips.cc/paper/5138-the-randomized-dependence-coefficient')
#Crawler.craw()

from tkinter import *
from tkinter import ttk
from tkinter import messagebox

hosts = set()
def textin(msg):
    t['state'] = 'normal'
    t.insert('end','\n'+msg)
    t['state'] = 'disabled'
def examineinput(url):
    match = re.search(r'http://\w+\.', url,re.IGNORECASE)
    match1 = re.search(r'http://http://', url,re.IGNORECASE)
    if match1:
            return False
    if match:
        return True
    return False
def _ok(*args):
    urlname = name.get()
    url = 'http://'+urlname
    if examineinput(url)==False:
        messagebox.showinfo(message='输入网址(URL)格式错误')
        return
    name.state(['readonly'])#='readonly'
    ok.state(['disabled'])
    p.grid(column=0, row=4,columnspan=4,sticky=(N, S, E, W), rowspan=1,pady=5)
    p.start()
    textin('开始检索，主要搜索PDF和DOC/DOCX文档')
    #initial threads of spider
    fetchpage = FetchPage(url)
    urls = fetchpage.fetch()
    soup = BeautifulSoup(urls)
    urllist = soup.findAll({'a':True})
    for item in urllist:
        url_temp = item.get('href')
        m = urlparse(url_temp)
        url_temp = urljoin(url,m.geturl())
        hosts.add(url_temp)
    #run
    i=1
    for host in hosts:
        #print(host)
        #textin(host)
        if examineinput(host):
            backspider = multiSuperSpider(host,i)
            backspider.start()
            #backspider.setDaemon(True)
            i+=1
    return
def _output():
    t.grid(column=0,row=5,columnspan=4,pady=10)
    About.grid(column=1,row=6,columnspan=2)
    output.state(['disabled'])

def _Set(*args):
    def _savadir():
        dirname = filedialog.askdirectory()
        FILEDIR=dirname
        textin('存储路径修改为：'+FILEDIR)
        direction.set(FILEDIR)
    setwin = Toplevel(root)
    setwin.resizable(FALSE,FALSE)
    setwin.title('参数设置')
    setwin.geometry('500x178+1200+400')
    content = ttk.Frame(setwin, padding=(3,3,3,3))
    LabelDir = ttk.Label(content, text='文件存储路径')
    direction=StringVar()
    DIR = ttk.Entry(content,state='readonly',textvariable=direction,width=32)
    ok = ttk.Button(content, text="修改",command=_savadir)
    
    content.grid(column=0, row=0,sticky=(N, S, E, W))
    LabelDir.grid(column=0, row=0,pady = 5)
    DIR.grid(column=1, row=0)
    ok.grid(column=2, row=0)
    direction.set(FILEDIR)
    #DIR.insert(0, FILEDIR)
    
    setwin.mainloop()
def _about():
        aboutwin = Toplevel(root)
        aboutwin.resizable(FALSE,FALSE)
        aboutwin.title('关于我')
        aboutwin.geometry('+1200+500')
        ll = ttk.Frame(aboutwin, padding=(23,13,23,13))
        Labelme = ttk.Label(ll, text='个人主页: www.goldencui.org')
        ll.grid(column=0, row=0,sticky=(N, S, E, W))
        Labelme.grid(column=0, row=0)
        #aboutwin.mainloop()
def _Exit(*args):
    exit()


root = Tk()
root.resizable(FALSE,FALSE)
root.title('资源搜索爬虫 Beta1')
root.geometry('+800+400')
content = ttk.Frame(root, padding=(20,3,20,3))
image = PhotoImage(file='title.gif')
Labelurl = ttk.Label(content)
Labelurl['image']=image


lf = ttk.Labelframe(content, text='输入要抓取网址')

namelbl = ttk.Label(lf, text="http://")
url=StringVar()
name = ttk.Entry(lf,textvariable=url)
example = ttk.Label(lf, text="例如:www.baidu.com")

p = ttk.Progressbar(content, orient=HORIZONTAL, length=380, mode='indeterminate')

ok = ttk.Button(content, text="搜索",command=_ok,width=8)
output = ttk.Button(content, text="输出",command=_output,width=8)
Set = ttk.Button(content, text="设置",command=_Set,width=8)
Exit = ttk.Button(content, text="退出",command=_Exit,width=8)
t = Text(content, width=53, height=20,state='disabled',yscrollcommand='yview')
About = ttk.Button(content, text="关于",command=_about,width=10)


