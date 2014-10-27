#_*_encoding:cp936_*_
import urllib,urllib2,re,os


class sogouMusic:
    
    def __init__(self):
        self.song_name = raw_input("������Ҫ���ҵĸ���:")
        self.get_song_info()#��ȡ������Ϣ��������Ϣ��self.song_info
        if self.song_info:
            self.display_song()
            self.get_song_url()
    
    def get_song_info(self):
        url = 'http://mp3.sogou.com/music.so?query='+self.song_name
        music_page = urllib.urlopen(url).read()
        #print(music_page)
        regexp = re.compile('qqDownload\({(.*?)}\)',re.MULTILINE)
        self.song_info = regexp.findall(music_page)
            

    #��ʾ�����ĸ���
    def display_song(self):
        i = 0
        self.song_name = []
        for song in self.song_info:
            info = song.split("@@")
            self.song_name.append(info[3]+'-'+info[1]+'('+info[5]+').mp3')#���������б�
            print("���"+str(i)+": "+self.song_name[i])
            i+=1

    #���ظ���
    def get_song_url(self):
        down = True
        while down:
            global prev
            prev = 0
            action = raw_input("����Ҫ���صĸ������:")
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
                    post2 = post[1]#����post����
                    data = urllib.urlencode({'t':0,'f':post2})#����post����
                    headers = {
                        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64; rv:32.0) Gecko/20100101 Firefox/32.0",
                        "referer":"http://mp3.sogou.com/music.so"
                        }
                    request = urllib2.Request('http://soso.music.qq.com/fcgi-bin/fcg_song.fcg',data,headers)
                    down_page = urllib2.urlopen(request).read()
                    song_url = re.findall('<dd><a.*?href="(.*?)"',down_page)#������ַ
                    self.song_url = song_url[0]#����mp3��ַ
                    #print(self.song_url)
                    self.down(index)#���ض���
                
    #���ݸ���id����
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
            print("|%s|\n|%s|\n|%s|"%(line,"����Ŭ������,�Ȼ���ͺ���".ljust(titlelen),line))
            print "[",
            if urllib.urlretrieve(song_url,'audio/'+song_name,reporthook = report):
                print "]\n"
                msg = '�ɹ���,o(^��^)o�����ַ'+os.getcwd()+'\\audio\\'+song_name
                print("|%s|\n|%s|\n|%s|"%(line,msg.ljust(titlelen),line))

        else:
            print("|%s|\n|%s|\n|%s|"%(line,"�Ѿ������˾Ͳ�Ҫ�ظ�����,(-__-)b".ljust(titlelen),line))

        
def report(a,b,c):
    #@a:�Ѿ����ص����ݿ�
    #@b:���ݿ��С
    #@c:Զ���ļ���С
    #�����趨�õ�titlelen����ʾ����
    #title = "songtaste����������,ճ���������ҳ��,�Ϳ�������Ŷ(by huchao)"
    #titlelen = 60 
    global prev
    block = 60*a*b/c#��ǰ����
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

