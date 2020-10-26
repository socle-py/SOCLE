#!/usr/local/bin/python3.9

import os
import subprocess
import lxc
#import rich
import fire
import yaml, json
from os.path import expanduser

#import rich objects
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns


nameCategory1="lxc"
config={}
#create socle conf yaml if not exist
pathFileConf=expanduser("~")+'/.socle.conf'
if not os.path.exists(pathFileConf):
    with open(pathFileConf, 'w') as f:
        yaml.dump(config, f, allow_unicode=True)

#initialize config object, yaml conf to json 
with open(pathFileConf) as f:
    config=yaml.load(f,Loader=yaml.FullLoader)
    print(config)

#create type if not exist
for key in 'os','pref':
    print(key)
    if key not in config.keys():
        config[key]={}
        with open(pathFileConf, 'w') as f:
            yaml.dump(config, f, allow_unicode=True)

for att in 'distrib','release':
    for key in config["os"].keys():
        if att not in config["os"][key].keys():
            config["os"][key][att]="null"
            with open(pathFileConf, 'w') as f:
                yaml.dump(config, f, allow_unicode=True)

   

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

    def create(self,distrib,release,name):
        """Create lxc container
        :param distrib: chose the os to install/download
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
        if container.create("download",1,{"dist":distrib,"release":release,"arch":arch}) == False:
            console.print("[red]ERROR container creation[/red]")
            
        print("lxc container created ",distrib,name)
        config["os"][name]={}
        config["os"][name]["distrib"]=distrib
        config["os"][name]["release"]=release

        with open(pathFileConf, 'w') as f:
            yaml.dump(config, f, allow_unicode=True)
        

    def ls(self):
        """list containers
        """
        #for key in config["os"].keys:
             
        os_renderables = [Panel(key+"\n"+lxc.Container(key).state+"\n"+config["os"][key]["distrib"]+"\n"+config["os"][key]["release"], style="red on blue" , expand=True) for key in config["os"].keys()]
        console.print(Columns(os_renderables))
        console.print(Columns(os_renderables))
        print(lxc.list_containers())

    def add(self,name):
        """Add containers to socle management
        """
        if name in config["os"].keys():
            console.print("[red]ERROR container already managed by socle[/red]")
            quit(1)

        if name not in lxc.list_containers():
            console.print("[red]ERROR container not present  in lxc[/red]")
            quit(1)
        
        config["os"][name]={}
        with open(pathFileConf, 'w') as f:
            yaml.dump(config, f, allow_unicode=True)
        
    def addVagrant(self,name):
        """Add vagrant machine to socle management
        """
    
    def addAllVagrant(self):
        """Add all vagrant to socle management
        """

    def addDocker(self,name):
        """Add docker container to socle management
        """

    def addAllDocker(self):
        """Add all docker containers to socle management
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
