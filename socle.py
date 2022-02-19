#! /usr/bin/env python3.8
# -*- coding: utf-8 -*-



title="""
███████╗ ██████╗  ██████╗██╗     ███████╗
██╔════╝██╔═══██╗██╔════╝██║     ██╔════╝
███████╗██║   ██║██║     ██║     █████╗[blue]v1[/blue]
╚════██║██║   ██║██║     ██║     ██╔══╝[green]TR[/green]
███████║╚██████╔╝╚██████╗███████╗███████╗
╚══════╝ ╚═════╝  ╚═════╝╚══════╝╚══════╝
"""


from rich.console import Console
from rich.panel import Panel
from rich.align import Align
from rich.columns import Columns
from rich.rule import Rule
from rich.text import Text
from rich import box
from rich.console import Group
from rich import box
from rich.markdown import Markdown



import os
import subprocess
import yaml
import _thread
#import argparse
import sys
import fire
import re
from sys import exit

#from rich.traceback import install
#install()


def run_to_x():
	os.system('xhost +')
	_thread.start_new_thread(os.system, ('docker exec -it systemd-debian  bash -c "export DISPLAY=$DISPLAY ; sudo -u user i3 "',))
	#os.system('docker exec -it systemd-debian  bash -c "export DISPLAY=$DISPLAY ; sudo -u user i3 "')
	os.system("clear;bash")
	os.system('sleep 15')
	#exit()


from subprocess import DEVNULL, STDOUT, check_call

def execute(command,message):
	#print(command)
	global glob_output
	console = Console()
	#	os.system(command+" > /dev/null 2>&1")
	with console.status(message) as status:
		try :
			output = subprocess.check_output(command, stderr=subprocess.STDOUT,shell=True,universal_newlines=True)
			#print(type(output))
			#output=check_call(['bash','-c',command], stdout=DEVNULL, stderr=STDOUT)
			console.print(":heavy_check_mark: "+message,style="green")
			glob_output=glob_output+1
		except subprocess.CalledProcessError as exc:
			console.print(":x: fail: "+message,style="red")
			print(exc.output)
			glob_output=glob_output+1+exc.output.count('\n')
			#console.print_exception()

def runScriptInStartx():
	if not  os.getenv('DISPLAY'):
		print("start startx")
		os.system("startx -maximized -bg black -fg white ./socle-docker.py")
		exit()

def runScriptInStartx2():
	if not  os.getenv('DISPLAY'):
		print("start startx")
		exit()


def tui_getcolor(test):
	if re.match('Exited', test):
		return("red")
	if re.match('Up', test):
		return("green")

cmd_get_compatible_containers="docker ps --format '{{ .ID }}' | xargs -I {} docker inspect -f '{{ .Name }}{{ range .Mounts }} {{ .Type }} {{ if eq .Type "+'"bind"'+" }}{{ .Source }}{{ end }}{{ .Name }} => {{ .Destination }}{{ end }}' {} | grep /tmp/.X11-unix | cut -f1 -d' '"
#cmd="docker ps -a --format '{{json  . }}' --no-trunc | grep '/tmp/.X11-unix'"
cmd='docker ps -a --format \'{"Names":"{{.Names}}" ,"Mounts":"{{.Mounts}}","Image":"{{.Image}}","Status":"{{.Status}}"}\' --no-trunc | grep \'/tmp/.X11-unix\''
#cmd_all="docker ps -a --format '{{json  . }}' --no-trunc"
cmd_all='docker ps -a --format \'{"Names":"{{.Names}}" ,"Mounts":"{{.Mounts}}","Image":"{{.Image}}","Status":"{{.Status}}"}\' --no-trunc '
	
def printContainers(all=False):
	useCmd=cmd
	if all==True:
		useCmd=cmd_all

	console = Console()

	try:
		x = subprocess.check_output(useCmd,shell=True)
		conts=str(x.decode("utf-8")).split('\n')[:-1]
	except subprocess.CalledProcessError:
		console.print(":grinning: pas trouvé")
		conts =""

	user_renderables = [Panel(Text.assemble((yaml.safe_load(cont)["Names"]+"\n", "green"),(yaml.safe_load(cont)["Image"]+"\n"),  (yaml.safe_load(cont)["Status"]+"\n", tui_getcolor(yaml.safe_load(cont)["Status"])),(yaml.safe_load(cont)["Mounts"])    ), expand=True,) for cont in conts]
	#user_renderables = "test" 
	panelTitle=Panel(title, style="red",box=box.SIMPLE)
	md_help = """
**updates official templates** (*update file `/usr/local/share/socle/socle.yml`*)

```
socle.py update-templates
```

**list all templates available** (*defined in `~/.config/socle/*.yml`,`/usr/local/share/socle/socle.yml`*)

```
socle.py list-templates
```

**create container from template**

```
socle.py create [TEMPLATE_NAME] [NAME]
```

"""

	md_help2="""    

**start x on compatible container**

```
socle.py x [CONTAINER_NAME]
```

**get example config** (*optional if you want custom os*)

``` Bash
cp /usr/local/share/socle/socle.yml ~/.socle/socle.yml
```



More help `socle.py --help`
"""
	from rich.table import Table

	panelHelp=Panel(Markdown(md_help),title="[bold white]QuickStart/Help",border_style="green",style="",box=box.SIMPLE)
	panelHelp2=Panel(Markdown(md_help2),title="",border_style="green",style="",box=box.SIMPLE)
	header = Table.grid(expand=True)
	#header.add_row("",panelTitle,style="on black")
	header.add_row(panelHelp,panelHelp2,style="on #0e1111")
	compatibleContainers=Panel(Columns(user_renderables,padding=0),title="[bold red]Detect compatible containers",border_style="green",style="on #0e1111")
	#console.print(Panel(Group(Align(panelTitle,align="center"),panelHelp,compatibleContainers,),box=box.HEAVY_EDGE,border_style="#ffd064"))
	console.print(Panel(Group(Align(panelTitle,align="center",style="on black"),header,compatibleContainers,),box=box.HEAVY_EDGE,border_style="#ffd064"))

	#with console.capture() as capture:
	#	console.print(Columns(user_renderables,padding=0))
	#	console.print(title, style="red", justify="center")
	#	console.rule("[bold red]Detect compatible containers")
	#nlines = capture.get().count('\n')
	#return(nlines)
	#print(str(nlines))





#CLI

def list(all=False):
	"""list  containers"""
	printContainers()
	exit()


def start(*container):
	"""start a container"""
	for i in container:
		execute("docker start "+i, "start "+i)
	exit()

def stop(*container):
	"""stop a container"""
	for i in container:
		execute("docker stop "+i, "stop container "+i)
	exit()

def rm(*container,force=False):
	"""rm a container, use --force to force"""
	for i in container:
		if force==False:
			execute("docker rm "+i, "rm "+i)
		if force==True:
			execute("docker rm -f "+i, "rm force "+i)
	exit()



# possible dexectuer un container directement sur un tty de libre ? peut etre .. besoin detre root de pense
def list_templates():
	"""list templates"""

	#print(configContainers)
	user_renderables = [Panel(Text.assemble((cont+"\n", "green"),(configContainers[cont]["description"]["longText"]+"\n")), expand=True) for cont in configContainers]
	console = Console()
	console.print(Panel(Columns(user_renderables,padding=0),title="[bold red]ListTemplates",border_style="green",style=""))



	#fire.Fire({
	#	'templates': start,
	#	'container': stop,
	#	})

def list_containers(All=False):
	"""list containers"""
	printContainers()
	#fire.Fire({
	#	'templates': start,
	#	'container': stop,
	#	})

def update_templates():
	"""updates templates"""
	execute("sudo mkdir -p  /usr/local/share/socle","")
	execute("sudo curl -Lo /usr/local/share/socle/socle.yml https://raw.githubusercontent.com/thomas1version is version0/SOCLE/main/socle.yml?token=GHSAT0AAAAAABMZ6KXRG3JCBP44FKUC7RZCYQKYSTQ","")


def create(choice,*name):
	"""create a container"""
        # make option force to delete container present
	#print(doc[choice])
	console = Console()
	#with console.status(' '.join(map(str, sys.argv))+"...") as status:
	#if f == "yes":
	#	for i in name:
	#		execute("docker rm -f $NAME", "delete existant container")
	
	for i in name:
		execute(configContainers[choice]["command"].replace("$NAME",i), "create container")
	exit()

def x(container):
	"""start x on container"""

	if os.getenv('XAUTHORITY') is not None and os.getenv('SOCLE_cli') is None:
		print("windows managed detected abort")
		exit()

	if os.getenv('SOCLE_cli') is not None:
                del os.environ['SOCLE_cli']
	if not os.getenv('DISPLAY'):
		print('not x detected start x')
		os.environ["SOCLE_cli"]=' '.join(map(str, sys.argv))
		#os.environ["SOCLE_cli"]=""
		print(' '.join(map(str, sys.argv)))
		os.system("startx -maximized -bg red -fg white "+sys.argv[0])
		#os.system("startx -maximized -bg red -fg white "+sys.argv[0]+" "+x+" "+container )
		exit()

	#if os.getenv('DISPLAY') is not None and os.getenv('XAUTHORITY') is None:
	if os.getenv('DISPLAY') is not None :
		os.system("docker start "+container)
		os.system('xhost +')
		os.system("echo HOST WINDOW !!")
		os.system("echo "+"'"+title+"'")

		#os.system('docker exec -it '+a.container+'  bash -c "export DISPLAY=$DISPLAY ; sudo -u user wm "')
		try:
			#_thread.start_new_thread(os.system, ('bash',))
			#output = subprocess.check_output('docker exec -it '+container+'  bash -c "export DISPLAY=$DISPLAY ; sudo -u user i3 "', stderr=subprocess.STDOUT,shell=True,universal_newlines=True)
			_thread.start_new_thread(os.system, ('docker exec -it '+container+'  bash -c "export DISPLAY=$DISPLAY ; sudo -u user i3"',))
			os.system("clear;bash")
		except subprocess.CalledProcessError as exc:
			print(exc.output)
		#_thread.start_new_thread(os.system, ('docker exec -it '+container+'  bash -c "export DISPLAY=$DISPLAY ; sudo -u user i3"',))
		#os.system('docker exec -it '+container+'  bash -c "export DISPLAY=$DISPLAY ; sudo -u user i3 "' )
		#os.system('exit')
		#os.system("export PS1='TOTOA';bash -c 'export PS1=TOTO ; bash ' ")
		#os.system("PS1='TOTO'")
		exit()
	exit()

def tui_all():
	printContainers(all=True)



# EXECUTE X WINDOW

# SI detection windows manager
mainContainers={}
userContainers={}
def ph(path):
    return os.path.expanduser(path)

#MAIN


configContainers={}
listConfigFiles=['/usr/local/share/socle/socle.yml','~/.local/share/socle/socle.yml','~/.config/socle.yml','~/.local/src/socle.git/socle.yml']
for i in listConfigFiles:
	i=os.path.expanduser(i)
	if os.path.isfile(i):
		a=yaml.load(open(i, 'r'),Loader=yaml.SafeLoader)
		configContainers={**configContainers,**a}

#if not os.path.isfile(pathMainContainers):
#    os.system(ph("mkdir -p ~/.local/share/socle"))
#    os.system(ph("cp ~/.config/socle.yml ~/.local/share/socle/socle.yml"))


#a={"create":{ } }
a={}
for i in configContainers:
	a[i]=None	

glob_output=0

if len(sys.argv) > 1: 
	fire.Fire({
		'start': start,
		'stop': stop,
		'rm': rm,
		'create': create,
		#'createList': createList,
		'x': x,
		'update-templates': update_templates,
		'list-templates': list_templates,
		#'list-containers': list_containers, pas encore implémenté
		#'all': tui_all,
		})
elif not os.getenv('SOCLE_cli') is None and not os.getenv('SOCLE_cli') == "" :
	print(os.getenv('SOCLE_cli'))
	command=os.getenv('SOCLE_cli')
	os.system(command)

else:
	printContainers()	


#runScriptInStartx()


#Display title
#run_to_x()
