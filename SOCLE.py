#!/usr/bin/python3

import os
import fire
import yaml, json
from os.path import expanduser

#import rich objects
from rich.console import Console
from rich.panel import Panel

#create socle conf yaml if not exist
pathFileConf=expanduser("~")+'/.socle.conf'
if not os.path.exists(pathFileConf):
    with open(pathFileConf, 'w'): pass

#initialize config object, yaml conf to json 
config=""
with open(pathFileConf) as f:
    config=yaml.load(f,Loader=yaml.FullLoader)
    print(config)

#create type if not exist
for key in 'os','pref':
    print(key)
    if key not in config.keys():
        config[key]={}
        with open(pathFileConf, 'w') as f:
            json.dump(config, f, ensure_ascii=False)

#Display title
title="""

███████╗ ██████╗  ██████╗██╗     ███████╗
██╔════╝██╔═══██╗██╔════╝██║     ██╔════╝
███████╗██║   ██║██║     ██║     █████╗[blue]v1[/blue]      
╚════██║██║   ██║██║     ██║     ██╔══╝[green]TR[/green]  
███████║╚██████╔╝╚██████╗███████╗███████╗
╚══════╝ ╚═════╝  ╚═════╝╚══════╝╚══════╝
                                         
"""
console = Console()
console.print(title, style="red", justify="center")

class SOCLE(object):
    """A simple calculator class."""
    def start(self,distrib,name):
        """Start lxc container with gui
        """

    def create(self,distrib,name):
        """Create lxc container
        :param distrib: chose the os to install/download
        :param name: chose the name of os
        """
        print("create lxc container ",distrib,name)
        """tydddddpe""" 

    def ls(self):
        """list containers
        """
    def add(self):
        """Add containers to socle management
        """
    
    def rename(self):
        """Rename containers
        """
    
    def unmanage(self):
        """remove container to socle management
        """
    
    def destroy(self):
        """destroy container
        """

if __name__ == '__main__':
  fire.Fire(SOCLE)