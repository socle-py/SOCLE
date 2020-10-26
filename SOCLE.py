#!/usr/bin/python3

import os
import subprocess
#import lxc
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

    def create(self,dist,release,name):
        """Create lxc container
        :param dist: chose the os to install/download
        :param release: chose the release to install/download
        :param name: chose the name of os
        """
        if name in config["os"].keys():
            console.print("[red]ERROR container name already used in socleManagement[/red]")
            quit(1)
        if name in lxc.list_containers():
            console.print("[red]ERROR container name already used in lxc[/red]")
            quit(1)
        try:
            with open(os.path.devnull, "w") as devnull:
                dpkg = subprocess.Popen(['dpkg', '--print-architecture'],
                                        stderr=devnull, stdout=subprocess.PIPE,
                                        universal_newlines=True)

                if dpkg.wait() == 0:
                    arch = dpkg.stdout.read().strip()
        except:
            pass

        container=lxc.Container(name)
        if container.create("download",1,{"dist":dist,"release":release,"arch":arch}) == False:
            console.print("[red]ERROR container creation[/red]")
            
        print("lxc container created ",dist,name)
        config["os"][name]={}
        with open(pathFileConf, 'w') as f:
            json.dump(config, f, ensure_ascii=False)

        

    def ls(self):
        """list containers
        """
        print(lxc.list_containers())

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