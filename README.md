![](https://i.imgur.com/PbtZEzV.png)
# SOCLE
**S**ystems **O**n **C**ontainers with **L**ightweight **E**nvironment

**SOCLE** is a python script to easily run a linux distribution in docker containers with a desktop environment attached to your x server,
It is made only for Users who want to easily use or change distribution without breaking the OS of their machine and without using a virtual machine

SOCLE is not made for production environments (contrary to the philosophy of 1 process in 1 container, and security has not been considered)

## Requirements
- linux
- docker
- curl

## Install

```
curl -L https://raw.githubusercontent.com/socle-py/SOCLE/main/install.sh | bash
```

## Usage

**list all templates available** or go https://socle-py.github.io/socle-vitrine/

```
socle.py list-templates
```

**create container from template**

```
socle.py create [TEMPLATE_NAME] [NAME]
```

**start x on compatible container**

```
socle.py x [CONTAINER_NAME]
```




### To-DO
- replace docker os command with docker library
- replace os curl command by python code
- adapt for windows
