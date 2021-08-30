import telepot
import urllib.parse
import os


class TelegramClient:
    ComandosDownload=["/DownloadSD","/DownloadHD"];
    ComandoStart="/start";
    def __init__(self,bot,msg):
        #puede ser para buscar o para obtener el link(ya sea un link como text o contestan a un mensaje enviado)
        content_type, chat_type, chat_id = telepot.glance(msg);
        self.ChatId=chat_id;
        self.Bot=bot;
        self.Message=msg;
        self.Id=msg["chat"]["id"];
        self.DownloadHD=None;
        self.IsStartCommand="text" in msg and TelegramClient.ComandoStart in msg["text"];
        #mirar si reenvian un video para obtener su link de descarga
        if  "text" in msg and "http" not in msg["text"] and "reply_to_message" not in msg:
            self.IsAnUrl=False;
        else:
            self.IsAnUrl=True;
            if "reply_to_message" in msg:
                self._setUrl(msg["reply_to_message"]["text"]); 
            
            elif "caption" in msg:
                self._setUrl(msg["caption"]);
            elif "text" in msg:#enviaron una url
                self._setUrl(msg["text"]);
                    
    def _setUrl(self,message):
        msg=message.lower();
        pos=0;
        total=len(TelegramClient.ComandosDownload);
        while self.DownloadHD is None and pos<total:
            if TelegramClient.ComandosDownload[pos].lower() in msg:
                self.DownloadHD=pos==1;
                message=message.replace(TelegramClient.ComandosDownload[pos],"").replace(" ","");
            pos+=1;
        if "http" in message:
            if "\n" in message:
                camposUrl=message.split("\n");
                self.Url=camposUrl[-1];
            else:
                self.Url=message; 
        else:
            self.IsAnUrl=False;

    def SendPhoto(self,urlImg,desc=""):
        self.Bot.sendPhoto(self.ChatId,urlImg,desc);

    def SendText(self,text):
        self.Bot.sendMessage(self.ChatId,text);
    
    def SendVideo(self,videoUrl,desc=""):
        self.Bot.sendVideo(self.ChatId,videoUrl,caption=desc);


 
    
