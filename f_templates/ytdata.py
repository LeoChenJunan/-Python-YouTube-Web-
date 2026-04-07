from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

from flask import Flask, render_template,request
from datetime import date,datetime
import pyodbc,time,os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

chrome_options = Options()

chrome_options.add_argument("--mute-audio")
chrome_options.add_argument('blink-settings=imagesEnabled=false')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options)
ftpath=r"C:\Users\h7236\OneDrive\桌面\f_templates"
app = Flask(__name__, template_folder=ftpath)
conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=DESKTOP-BAKUBIS\MSSQLSERVER01;'
    'Database=testdb;'
    'Trusted_Connection=yes;'
    )
 #'charset="utf8";'
font_path = r'C:\Windows\Fonts\kaiu.ttf'
plt.rcParams['font.sans-serif'] = ['DFKai-SB']
plt.rcParams['axes.unicode_minus'] = False
#months = mdates.MonthLocator()
#days = mdates.DayLocator()
#timeFmt = mdates.DateFormatter('%m')

def driverfind(x):
    nn=0
    while(True):
        try:
            x1=driver.find_element(By.XPATH,x)
            return x1
        except:
            if nn!=0 and nn%20==0:
                driver.refresh()
                print('def ref')
            time.sleep(0.2)
            #print('def nn',nn)
            nn+=1

def driverfinds(x):
    try:
        x1=driver.find_elements(By.XPATH,x)
        return x1
    except:
        time.sleep(0.2)
        
def get_time():
    ti=datetime.now()
    print('時間:',ti.hour,ti.minute,ti.second)

def get_ldate(x):
    driver.get(f'{x}/about')
    a='''
        DROP TABLE IF EXISTS bdata;
        CREATE TABLE bdata (
            link_name NVARCHAR(300),
            link NVARCHAR(max),
        )
    '''
    conn.execute(a)
    conn.commit()
    time.sleep(1)
    try:
        x1=driver.find_elements(By.XPATH,f'//*[@id="link-list-container"]/a')
        x2=[j.get_attribute('href') for j in x1]
        x4=driver.find_elements(By.XPATH,f'//*[@id="link-list-container"]/a/yt-formatted-string')
        x5=[i2.text for i2 in x4]
    except:
        time.sleep(0.2)
    #print(len(x2))
    x3=int(len(x2)) 
    #print(x4)
    #print(x5)
    #print(x1)
    #print(x2)

    #print(x3)
    for i in range(0,x3):
        a = f'''INSERT INTO bdata (link_name,link) VALUES
                (?,'{x2[i]}')
        '''
        conn.execute(a,x5[i])
        conn.commit()

def get_cadate(x):
    driver.get(f'{x}/about')
    a='''
        DROP TABLE IF EXISTS adata;
        CREATE TABLE adata (
            cdate NVARCHAR(300),
            videos_number NVARCHAR(300),
            watchs_number NVARCHAR(300),
            location NVARCHAR(300),
        )
    '''#introduction NVARCHAR(300),
    conn.execute(a)
    conn.commit()

    aa=driverfind('//*[@id="right-column"]/yt-formatted-string[2]/span[2]')
    aa=f'加入日期：{aa.text}'

    zz=driverfind('//*[@id="videos-count"]/span[1]')
    yy=(f'影片數量：{zz.text}部')
    print(yy)

    
    ss=driverfind('//*[@id="right-column"]/yt-formatted-string[3]')
    tt=ss.text
    print(tt)

    ee=driverfind('//*[@id="details-container"]/table/tbody/tr[2]/td[2]/yt-formatted-string')
    ee=ee.text
    if ee=='':
        ee='不公開'
    ee=f'位置：{ee}'

    '''
    jj=driverfind('//*[@id="description-container"]').text
    print('---------------------------------------------------------------')
    print(jj)
    print('---------------------------------------------------------------')
    ii='<br>'.join(jj.split('\n'))
    print('---------------------------------------------------------------')
    print(ii)
    print('---------------------------------------------------------------')  
    if ii=='':
      #  ii.append('沒有簡介')
        ii=('沒有簡介')
    print(ii)
    print(jj)
    '''
    global ii
    jj=driverfind('//*[@id="description-container"]').text
    if jj=='':
        ii='無'
    else:
        jj=jj.split('\n')
        ii=jj[1:len(jj)]

    a = f'''INSERT INTO adata (cdate,videos_number,watchs_number,location) VALUES
            ('{aa}','{yy}','{tt}','{ee}')
        '''
    #,introduction ,'{ii}'
    conn.execute(a)
    conn.commit()
    

def get_cdata(x):
    a='''
        DROP TABLE IF EXISTS cdata;
        CREATE TABLE cdata (
            cheadsrc NVARCHAR(300),
            cname NVARCHAR(100),
            csub NVARCHAR(100),
            curl NVARCHAR(300)
        )
    '''
    conn.execute(a)
    conn.commit()
    def channels(x):#頻道圖片
        driver.get(f'https://m.youtube.com/results?search_query={x}&sp=EgIQAg%253D%253D')
        time.sleep(2)
        img = driverfinds('//*[@id="img"]')#圖片
        uptimes = 10 
        times = 0
        actions = ActionChains(driver)
        while times < uptimes:
            actions.send_keys(Keys.PAGE_DOWN)
            actions.perform()
            times += 1
            src = [i.get_attribute('src') for i in img]
            if src is None:
                break
        return src

    def names(x):
        #container = driver.find_elements(By.XPATH, '//*[@id="text"]')
        container = driverfinds('//*[@id="text"]')
        nam = [j.text for j in container]
        return nam

    def num(x):
        #num1 = driver.find_elements(By.XPATH, '//*[@id="video-count"]')
        num1 = driverfinds('//*[@id="video-count"]')
        num2= [j.text if j.text != '' else '0位訂閱者' for j in num1]
        return num2

    def web(x):
        #web1=driver.find_elements(By.XPATH,'//*[@id="avatar-section"]/a')
        web1=driverfinds('//*[@id="avatar-section"]/a')
        web2=[l.get_attribute('href') for l in web1]
        return web2
    
    a1=channels(x)
    b1=names(x)
    c1=num(x)
    d1=web(x)

    l=min(len(a1),len(b1),len(c1),len(d1))
    if l>16:
        l=16
    for i in range(l):#('{a1[i]}', '{b1[i]}', '{c1[i]}','{d1[i]}')
        a = f'''INSERT INTO cdata (cheadsrc,cname,csub,curl) VALUES
                ('{a1[i]}', ?, '{c1[i]}','{d1[i]}')
            '''
        conn.execute(a,b1[i])
        conn.commit() 
    
    #l=min(len(a1),len(b1),len(c1),len(d1))
    #if l>16:
    #    l=16
    #for i in range(l):#('{a1[i]}', '{b1[i]}', '{c1[i]}','{d1[i]}')
    #    a = f'''INSERT INTO cdata (cheadsrc,cname,csub,curl) VALUES
    #            ('{a1[i]}', ?, '{c1[i]}','{d1[i]}')
    #    '''
    #    conn.execute(a,b1[i])
    #    conn.commit() 

def get_tdate(x):
    driver.get(f'{x}/videos')

    a='''
        DROP TABLE IF EXISTS tdata;
        CREATE TABLE tdata (
            videos NVARCHAR(300)
        )
    '''
    conn.execute(a)
    conn.commit()
    '''
    while(True):
        try:
            aa=driver.find_element(By.XPATH,'//*[@id="videos-count"]/span[1]')
            break
        except:
            time.sleep(0.2)
    '''
    aa=driverfind('//*[@id="videos-count"]/span[1]')
    cc=int(aa.text)
    dd=round(cc/3)
    uptimes =int(dd)
    times = 0
    actions = ActionChains(driver)
    while times < uptimes:
        actions.send_keys(Keys.PAGE_DOWN)
        actions.perform()
        times += 1
        #img_element = driver.find_element(By.XPATH, '//*[@id="video-title-link"]')
        img_element = driverfind('//*[@id="video-title-link"]')
        img_src = img_element.get_attribute('href')
        if img_src is None:
            break
    #po1=driver.find_elements(By.XPATH,'//*[@id="video-title-link"]')
    po1=driverfinds('//*[@id="video-title-link"]')
    po2 = [j.get_attribute('href') for j in po1]
    print('lenpo2',len(po2))
    for i in range(len(po2)):
        a = f'''INSERT INTO tdata (videos) VALUES
                ('{po2[i]}')
        '''
        conn.execute(a)
        conn.commit()

def get_vdata(urls):
    a = '''
        DROP TABLE IF EXISTS vdata 
        CREATE TABLE vdata (
        likes int,
        watchs bigint,
        year int,
        month int,
        day int,
        title nvarchar(100),
        url nvarchar(100)
    )'''#messages int,
    conn.execute(a)
    conn.commit() 
    for url in urls:
        get_time()
        url=url[0]
        #print(url)
        driver.get(url)
        time.sleep(1.2)
        '''
        while(True):
            try:
                a=driver.find_element(By.XPATH,'//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span')
                break
            except:
                time.sleep(0.2)
        '''
        a=driverfind('//*[@id="segmented-like-button"]/ytd-toggle-button-renderer/yt-button-shape/button/div[2]/span')
        if a.text[len(a.text)-1]=='萬':
            likes=int(float(a.text[0:len(a.text)-1])*10000)
        elif a.text=='喜歡':
            likes=0
        else:
            likes=int(a.text)
        '''
        while(True):
            try:
                driver.find_element(By.XPATH,'//*[@id="expand"]').click()
                break
            except:
                time.sleep(0.2)
        '''
        driverfind('//*[@id="expand"]').click()
        time.sleep(0.3)

        #b=driver.find_element(By.XPATH,'//*[@id="info"]/span[1]')
        b=driverfind('//*[@id="info"]/span[1]')
        b=b.text
        #print(b[len(b)-6:len(b)])
        if b[len(b)-5:len(b)]=='觀眾等待中':
            watchs=0
        else:
            watchs=int(''.join((b[5:len(b)-1]).split(',')))

        #c=driver.find_element(By.XPATH,'//*[@id="info"]/span[3]')
        c=driverfind('//*[@id="info"]/span[3]')
        t=c.text
        if t[0:5]=='首播日期：':
            t=t[5:len(t)]
        if t[0]=='於':
            t = str(date.today())
            year=int(t[0:4])
            month=int(t[5:7])
            day=int(t[8:10])
        else:
            for i in range(len(t)):
                if t[i]=='年':
                    a1=i
                if t[i]=='月':
                    a2=i
            year=int(t[0:a1])
            month=int(t[a1+1:a2])
            day=int(t[a2+1:len(t)-1])
        #e=driver.find_element(By.XPATH,'//*[@id="title"]/h1/yt-formatted-string')
        e=driverfind('//*[@id="title"]/h1/yt-formatted-string')
        title=e.text

        print(f'{likes},{watchs},{year},{month},{day},{title}')#{messages}
        a=f'''insert into vdata (url, likes, watchs, year, month, day, title) values
                ('{url}',{likes},{watchs},{year},{month},{day},?)
        '''#,{messages}
        conn.execute(a,title)
        conn.commit() 

 

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/submit1', methods=['POST'])
def submit1():
    channel=request.values['channel']
    driver.get(f'https://m.youtube.com/results?search_query={channel}&sp=EgIQAg%253D%253D')
    time.sleep(2)
    #container = driver.find_element(By.XPATH, '//*[@id="text"]')
    container = driverfind('//*[@id="text"]')
    #print('container',container.text)
    if container.text=='':
        return render_template('f1.html')
    else:
        get_cdata(channel)
        a = "SELECT * FROM cdata"
        results = conn.execute(a)
        data = results.fetchall()
        return render_template('s1.html',**locals())


@app.route('/submit4', methods=['POST'])
def submit4():
    channel_url=request.values['channel_url']
    t=0
    try:
        driver.get(channel_url)
        time.sleep(2)
    except:
        t=1
    #print('container',container.text)
    if t==1:
        t=0
        return render_template('f2.html')
    else:
        csubs = driver.find_element(By.XPATH,'//*[@id="subscriber-count"]')
        csubs=csubs.text
        cimg=driverfind('//*[@id="img"]').get_attribute('src')
        cname=driverfind('//*[@id="text"]').text
        data=[(cimg,cname,csubs,channel_url)]
        return render_template('s1.html',**locals())

@app.route('/submit3', methods=['POST'])
def submit3():
    
    channel_url=request.values['channel_url']
    img_src=request.values['img_src']
    channel_name=request.values['channel_name']
    subs=request.values['subs']

    get_ldate(channel_url)
    get_cadate(channel_url)

    a = "SELECT * FROM adata"#ca
    r = conn.execute(a)
    cd = r.fetchall()
    cd=cd[0]

    a = "SELECT * FROM bdata"#l
    r = conn.execute(a)
    ahref = r.fetchall()
    if ahref==[]:
        ahref='無'

    introduction=ii
    return render_template('s2.html',**locals())

@app.route('/submit2', methods=['POST'])
def submit2():
    
    channel_url=request.values['channel_url']
    img_src=request.values['img_src']
    channel_name=request.values['channel_name']
    subs=request.values['subs']

    #get_ldate(channel_url)
    #get_cadate(channel_url)

    a = "SELECT * FROM adata"
    r = conn.execute(a)
    cd = r.fetchall()
    cd=cd[0]

    a = "SELECT * FROM bdata"
    r = conn.execute(a)
    ahref = r.fetchall()
    if ahref==[]:
        ahref='無'

    introduction=ii
    print('introduction',introduction)

    get_time()
    get_tdate(channel_url)
    a = "SELECT * FROM tdata"
    result1 = conn.execute(a)
    videous = result1.fetchall()
    get_vdata(videous)
    a = "SELECT * FROM vdata"
    result2 = conn.execute(a)
    videos = result2.fetchall()
    #print(videos)
    #print(videos[0][2],videos[len(videos)-1][2])
    #print(range(int(videos[0][2]),int(videos[len(videos)-1][2]+1)))
    ll=[]
    #print('range',videos[len(videos)-1][2],videos[0][2]+1)
    for i in range(videos[len(videos)-1][2],videos[0][2]+1):#videos[0][2]+1
        #print(i)
        l=[]
        for j in videos:
            if j[2]==i:
                l.append(j)
        ll.append(l)
    n1=1
    #print('n1n1',n1)
    #print('ll',ll)
    while(True):
        #if os.path.exists(fr'C:\Users\h7236\OneDrive\桌面\f_templates\static\img{n1}'):
        if os.path.exists(fr'{ftpath}\static\img{n1}'):
            n1+=1
            #print('n1',n1)
        else:
            #os.mkdir(fr'C:\Users\h7236\OneDrive\桌面\f_templates\static\img{n1}')
            os.mkdir(fr'{ftpath}\static\img{n1}')
            #print('aaaaaaaa')
            break
    nn=0
    #print('n1',nn)
    pathl=[]
    for l in ll:
        dates=[]
        likes=[]
        watchs=[]
        for j in l:
            #print(j[2],j[3],j[4])
            dates.append(date(j[2],j[3],j[4]))
            likes.append(j[0])
            watchs.append(j[1])
        #print(l)
        if l==[]:
            continue
        #font_path = r'C:\Windows\Fonts\kaiu.ttf'
        #plt.rcParams['font.sans-serif'] = ['DFKai-SB']
        #plt.rcParams['axes.unicode_minus'] = False

        #print('dates',dates)
        #print('likes',likes)
        #print('watch',watchs)

        months = mdates.MonthLocator()
        days = mdates.DayLocator()
        fig, ax = plt.subplots(figsize=(7, 4))
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_minor_locator(days)
        timeFmt = mdates.DateFormatter('%m')
        ax.xaxis.set_major_formatter(timeFmt)

        plt.plot(dates,likes,'r-*',label='喜歡數')
        plt.legend()
        #print('lllllllllll',l)
        plt.title(f"{l[0][2]}喜歡數折線圖", fontsize=20)
        plt.xlabel('日期',fontsize=14)
        nn+=1
        pathl.append([f"img{n1}",f"a{nn}.png"])
        #plt.savefig(fr"C:\Users\h7236\OneDrive\桌面\f_templates\static\img{n1}\a{nn}.png")
        plt.savefig(fr"{ftpath}\static\img{n1}\a{nn}.png")
        plt.show()

        fig, ax = plt.subplots(figsize=(7,4))
        ax.xaxis.set_major_locator(months)
        ax.xaxis.set_minor_locator(days)
        timeFmt = mdates.DateFormatter('%m')
        ax.xaxis.set_major_formatter(timeFmt)

        plt.plot(dates,watchs,'y-*',label='觀看數')
        plt.legend()
        plt.title(f"{l[0][2]}觀看數折線圖", fontsize=20)
        plt.xlabel('日期',fontsize=14)
        nn+=1
        pathl.append([f"img{n1}",f"a{nn}.png"])
        #plt.savefig(fr"C:\Users\h7236\OneDrive\桌面\f_templates\static\img{n1}\a{nn}.png")
        plt.savefig(fr"{ftpath}\static\img{n1}\a{nn}.png")
        plt.show()
    #n1=f'img{n1}'
    #print('pathl',pathl)
    #print('n1',n1)
    #driver.close()
    return render_template('ff.html',**locals())

app.run()