#_*_encoding:cp936_*_
import urllib,urllib2,re,os


class sogouMusic:
    
    def __init__(self):
        self.song_name = raw_input("输入需要查找的歌曲:")
        self.get_song_info()#获取歌曲信息，歌曲信息在self.song_info
        if self.song_info:
            self.display_song()
            self.get_song_url()
    
    def get_song_info(self):
        url = 'http://mp3.sogou.com/music.so?query='+self.song_name
        music_page = urllib.urlopen(url).read()
        #print(music_page)
        regexp = re.compile('qqDownload\({(.*?)}\)',re.MULTILINE)
        self.song_info = regexp.findall(music_page)
            

    #显示搜索的歌曲
    def display_song(self):
        i = 0
        self.song_name = []
        for song in self.song_info:
            info = song.split("@@")
            self.song_name.append(info[3]+'-'+info[1]+'('+info[5]+').mp3')#歌曲名称列表
            print("序号"+str(i)+": "+self.song_name[i])
            i+=1

    #下载歌曲
    def get_song_url(self):
        down = True
        while down:
            global prev
            prev = 0
            action = raw_input("输入要下载的歌曲序号:")
            if(action.isdigit()):
                index = int(action,10)
            elif action == 'exit':
                down = False
            else:
                continue
            
            if down:
                song = self.song_info[index]
                if song:
                    post = song.split("\'")
                    post2 = post[1]#歌曲post数据
                    data = urllib.urlencode({'t':0,'f':post2})#建立post数据
                    headers = {
                        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0",
                        "referer":"http://mp3.sogou.com/music.so"
                        }
                    request = urllib2.Request('http://soso.music.qq.com/fcgi-bin/fcg_song.fcg',data,headers)
                    down_page = urllib2.urlopen(request).read()
                    song_url = re.findall('<dd><a.*?href="(.*?)"',down_page)#歌曲地址
                    self.song_url = song_url[0]#歌曲mp3地址
                    #print(self.song_url)
                    self.down(index)#下载动作
                
    #根据歌曲id下载
    def down(self,index):
        titlelen = 60
        song_url = self.song_url.replace("amp;","")
        #print song_url
        song_name = self.song_name[index]
        if not os.path.exists('audio/'+song_name):
            '''headers = {
            #    "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0",
            #    
"referer":"http://soso.music.qq.com/fcgi-bin/fcg_song.fcg"
            #    }
            #request = urllib2.Request(url=song_url,headers=headers)
            #audio_content = urllib2.urlopen(request).read()
            #if audio_content:
            #    fp = open('audio/'+song_name,'wb')
            #    fp.write(audii_content)
            #    fp.flush()
            #    fp.close()'''
            print("|%s|\n|%s|\n|%s|"%(line,"正在努力下载,等会儿就好了".ljust(titlelen),line))
            print "[",
            if urllib.urlretrieve(song_url,'audio/'+song_name,reporthook = report):
                print "]\n"
                msg = '成功啦,o(^▽^)o保存地址'+os.getcwd()+'\\audio\\'+song_name
                print("|%s|\n|%s|\n|%s|"%(line,msg.ljust(titlelen),line))

        else:
            print("|%s|\n|%s|\n|%s|"%(line,"已经下载了就不要重复下了,(-__-)b".ljust(titlelen),line))

        
def report(a,b,c):
    #@a:已经下载的数据块
    #@b:数据块大小
    #@c:远程文件大小
    #根据设定好的titlelen来显示进度
    #title = "songtaste歌曲下载器,粘贴你听歌的页面,就可以下载哦(by huchao)"
    #titlelen = 60 
    global prev
    block = 60*a*b/c#当前进度
    per = block-prev
    if per>1:
        print "=",
        prev = block



line = ''
prev = 0
for i in range(60):
    line+='-'              
while True:
    sm = sogouMusic()

