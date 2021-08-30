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
        if telegramClient.IsAnUrl:
            video=VideoFacebook(telegramClient.Url);
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
        else:
                telegramClient.SendText("Solo links a videos de Facebook!");
