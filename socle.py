#! /usr/bin/env python3
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
from rich.columns import Columns
from rich.text import Text
from rich import box


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
cmd="docker ps -a --format '{{json  . }}' --no-trunc | grep '/tmp/.X11-unix'"
cmd_all="docker ps -a --format '{{json  . }}' --no-trunc"
	
def printContainers(all=False):
	useCmd=cmd
	if all==True:
		useCmd=cmd_all

	console = Console()
	console.print(title, style="red", justify="center")
	console.rule("[bold red]Detect compatible containers")

	try:
		x = subprocess.check_output(useCmd,shell=True)
		conts=str(x.decode("utf-8")).split('\n')[:-1]
	except subprocess.CalledProcessError:
		console.print(":grinning: pas trouvé")
		conts =""
	user_renderables = [Panel(Text.assemble((yaml.load(cont)["Names"]+"\n", "green"),(yaml.load(cont)["Image"]+"\n"),  (yaml.load(cont)["Status"]+"\n", tui_getcolor(yaml.load(cont)["Status"])),(yaml.load(cont)["Mounts"])    ), expand=True, box=box.SQUARE) for cont in conts]
	console.print(Columns(user_renderables,padding=0))

        
	with console.capture() as capture:
		console.print(Columns(user_renderables,padding=0))
		console.print(title, style="red", justify="center")
		console.rule("[bold red]Detect compatible containers")
	nlines = capture.get().count('\n')
	return(nlines)
	print(str(nlines))





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
def create(choice,*name):
	"""create a container"""
        # make option force to delete container present
	#print(doc[choice])
	console = Console()
	#with console.status(' '.join(map(str, sys.argv))+"...") as status:
	for i in name:
		execute(doc[choice].replace("$NAME",i), "create container")
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
	tui(all=True)



# EXECUTE X WINDOW

# SI detection windows manager


#MAIN
doc=yaml.load(open('/home/throc/.config/socle.yml', 'r'),Loader=yaml.SafeLoader)
	
#a={"create":{ } }
a={}
for i in doc:
	a[i]=None	

glob_output=0

if len(sys.argv) > 1: 
	fire.Fire({
		'start': start,
		'stop': stop,
		'rm': rm,
		'create': create,
		'x': x,
		'list': printContainers,
		'all': tui_all,
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
