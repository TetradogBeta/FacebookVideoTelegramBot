from datetime import datetime
from tqdm import tqdm
from Stream import Stream

import re
import requests

#source:https://github.com/sameera-madushan/Facebook-Video-Downloader/blob/master/downloader.py

class Video:

    def __init__(self,urlVideo):
        self.Url=urlVideo;

        self.Html=None;
        self.Qualities=None;
        self.HasHD=None;
        self.HasSD=None;


    def Load(self):
        if self.Html is None:
            self.Html=requests.get(self.Url).content.decode('utf-8');
            _qualityhd = re.search('hd_src:"https', self.Html);
            _qualitysd = re.search('sd_src:"https', self.Html);
            _hd = re.search('hd_src:null', self.Html);
            _sd = re.search('sd_src:null', self.Html);
            _thelist = [_qualityhd, _qualitysd, _hd, _sd];
            self.HasHD=False;
            self.HasSD=False;
            for id,val in enumerate(_thelist):
                if val is not None:
                    if id%2==0:
                        self.HasHD=True;
                    else:
                        self.HasSD=True;
    def GetMessage(self):
        message="";
        self.Load();
        link=self.GetSDLink();
        if link is not None:
            message="SD: "+link+"\n";
        link=self.GetHDLink();
        if link is not None:
            message+="HD: "+link;
        return message;
                        
    def GetSDLink(self):
        result=None;
        if self.HasSD is None:
            self.Load();
        if self.HasSD:
            result=self._GetUrl("SD");
        return result;

    def GetHDLink(self):
        result=None;
        if self.HasHD is None:
            self.Load();
        if self.HasHD:
            result=self._GetUrl("HD");
        return result;
    
    def _GetUrl(self,quality):
        try:
            result= re.search(rf'{quality.lower()}_src:"(.+?)"', self.Html).group(1);
        except:
            result=None;
        return result;
    
    @staticmethod
    def Download(url):
        return Stream(requests.get(url, stream=True));
        
    
    @staticmethod
    def DownloadVideo(url,qualityDefault="HD",fileName=None,blockSize=1024):
        video=Video(url);
        result=None;
        video.Load();
        if qualityDefault == "HD" and video.HasHD:
            videoUrl=video.GetHDLink();
        else:
            videoUrl=video.GetSDLink();
        if videoUrl is not None:
            videoStream=Video.Download(videoUrl);
            if fileName is None:
                fileName = datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S');
            t = tqdm(total=videoStream.Total, unit='B', unit_scale=True, desc=fileName, ascii=True);
            fileName=fileName + '.mp4';
            with open(fileName , 'wb') as f:
                for data in videoStream.iter_content(blockSize):
                    t.update(len(data));
                    f.write(data);

            videoStream.Close();
            t.close();
            result=fileName;
        return result;



