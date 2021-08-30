from TelegramBot import TelegramBot
from TelegramClient import TelegramClient
from VideoFacebook import VideoFacebook
from os.path import exists
import os


class VideoBot:
    def __init__(self,token):
        self.Bot=TelegramBot(token);
    
    def Start(self):
        metodo=lambda cli:self._DoIt(cli);
        return self.Bot.Start(metodo);
    
    def _DoIt(self,telegramClient):
        if telegramClient.IsStartCommand:
            telegramClient.SendText("/DownloadSD o /DownloadHD espacio y URL");
        elif telegramClient.IsAnUrl:
            video=VideoFacebook(telegramClient.Url);
            video.Load();
            if telegramClient.DownloadHD is None:
                if video.IsAFacebookVideoLink:
                    urlSD=video.GetSDLink();
                    urlHD=video.GetHDLink();
                    mensaje=None;
                    if urlSD is not None:
                        mensaje="SD:"+urlSD;
                    if urlHD is not None:
                        if mensaje is None:
                            mensaje="HD:"+urlHD;
                        else:
                            mensaje+="\nHD:"+urlHD;
                    if mensaje is not None:
                        telegramClient.SendText(mensaje);
                    else:
                        telegramClient.SendText("No hay videos ni HD ni SD...");    
                else:
                    telegramClient.SendText("Link incorrecto, solo videos de Facebook!");
            elif telegramClient.DownloadHD:
                if video.HasHD:
                    telegramClient.SendVideo(video.GetHDLink(),"HD");
                else:
                    telegramClient.SendText("No está en HD");
            else:
                if video.HasSD:
                    telegramClient.SendVideo(video.GetSDLink(),"SD");
                else:
                    telegramClient.SendText("No está en SD");     



        else:
                telegramClient.SendText("Solo links a videos de Facebook!");
