from TelegramHelper.Bot import Bot
from TelegramHelper.DicMetodo import DicMetodo

from VideoFacebook import Video

from os.path import exists

import os


def Main():
    fileConfig="Config";

    if exists(fileConfig):
        fConfig = open(fileConfig, "r");
        config = fConfig.readlines();
        fConfig.close();
        token=config[0].replace("\n","");
    elif len(sys.argv)>1:
        token=sys.argv[1];
        fConfig = open(fileConfig, 'w');
        fConfig.writelines([token]);
        fConfig.close();

    filtroUrl=r'^(https:|)[/][/]www.([^/]+[.])*facebook.com';

    comandos=["Start","DownloadSD","DownloadHD"];

    bot=Bot(token,"Video Facebook V3.0");

    bot.AddCommand(comandos[0],lambda cli:cli.SendMessage("1- URL\n2- /"+comandos[1]+" URL\n3- /"+comandos[2]+" URL"));

    dicMetodoSD=DicMetodo();
    dicMetodoSD.AddRegex(filtroUrl,DownloadSD);
    bot.AddCommandPlus(comandos[1], dicMetodoSD);

    dicMetodoHD=DicMetodo();
    dicMetodoHD.AddRegex(filtroUrl,DownloadHD);
    bot.AddCommandPlus(comandos[2], dicMetodoHD);

    bot.Default.AddRegex(filtroUrl,SendLinks);
    bot.Default.Default=lambda cli:cli.SendMessage("Solo links de videos del Facebook!");
    
    bot.Start();

def SendLinks(cli):
    video=GetVideo(cli);
    cli.SendMessage(video.GetMessage());

def DownloadSD(cli):
    Download(cli,GetVideo(cli).HasSD);

def DownloadHD(cli):
    Download(cli,GetVideo(cli).HasHD);

def Download(cli,tieneLaCalidad):
    if tieneLaCalidad:
        pathFile=Video.DownloadVideo(cli.Args[0]);
        cli.SendVideo(pathFile);
        os.remove(pathFile);
    else:
        cli.SendMessage("No está disponible en esa calidad!");

def GetVideo(cli):
    video=Video(cli.Args[0]);
    video.Load();
    return video;

Main();
