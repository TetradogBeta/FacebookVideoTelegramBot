from VideoBot import VideoBot
from os.path import exists
import os
import sys

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

print("Iniciando FacebookVideo Bot V2.0");
VideoBot(token).Start().run_forever();