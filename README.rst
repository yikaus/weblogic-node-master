wlnm 0.2.0 (Weblogic Node Master)
======================

.. contents::

Changes
-------
**0.2.0**: add remote contol ablitity , which can be used multi-machine weblogic admin

**0.1.0**: initial drop

Requirements
-------------
1. Weblogic Server 9,10,11 installed . Weblogic domain and nodemanager server configued 

2. Python 2.6 + installed if run from source

3. pip if run from source


Installation
------------

1. Install through pip.

    $ sudo pip install wlnm

2. Install from source.

    $ wget --no-check-certificate https://pypi.python.org/packages/source/w/wlnm/wlnm-0.2.0.tar.gz
    
    $ tar xvf wlnm-<version>.tar.gz
    
    $ sudo python setup.py install	

3. Install from RPM (build on Centos 64bit)
    
    $ wget --no-check-certificate https://pypi.python.org/packages/2.6/w/wlnm/wlnm-0.2.0-1.noarch.rpm
    
    $ sudo rpm -Uvh wlnm-<version>.noarch.rpm  

4. Run directly from git source if you don't have sudo access
    
    $ git clone https://github.com/yikaus/wlnm
    
    $ ./wlnm/wlnm/wlnm.py



Summary
-------

wlnm (Weblogic node master) is command tool to manage local weblogic installation and server instance ,node manager . It is based on metadata searching from config.xml and nodemanager.properties . You can use this tool directly without any configuration or enviroment setup . The tool itself will gathering all weblogic metadata infomations by go through all weblogic directories. It provides the function like list all domains , installation , servers and nodemanager information , start/kill local server instance also remote managedserver which through buildin WLST script. Welcome to test /use in your dev and test enviroment . As it is still in early version better not to use in production enviroment .

Usage Examples::

1. Run wlnm as daemon process and accept client request
    
    $ wlnm -d -p <portNumber>
    
    or 
    
    $ wlnm --daemon --port <portNumber>
	Start wlnm as daemon process listen on the port <portNumber>

    $ wlnm -k
    
    or 
    
    $ wlnm --kill
	Kill wlnm daemon process

2. Run wlnm locally or as client

The tool is used as interactive command mode , you need to enter wlnm prompt then use below command 

    
    wlnm
    >> connect <hostname/ip> <port>
	 Connect remote wlnm daemon process

    >> disconnect <hostname/ip> <port>
	 Disconnect remote wlnm daemon connection

    >> ls
         List all weblogic domains with servers belong to it.

    >> ls [domainName] ...*
         List weblogic domain by domain name , multi name supported 

    >> lsd 
          List weblogic all domains , not include servers  
         
    >> lswls
         List all version weblogic installation as well as nodemnager informations

    >> lsp
         List all running weblogic instances

    >> init
         This tool will search all weblogic domain at frist time use , once domain configure changed you can research weblogic 
	 informations and update local store
    
    >> startadmin [domainname] ...* 
         Start admin server by domain name , multiple name supported . 

    >> start [managedserverName] ...*
        start managed server by servername ,including remote server , multiple name supported

    >> stop [managedserverName] ...*
        stop managed server by servername ,including remote server , multiple name supported

    >> kill  [port|servername] ...*
        kill process of server by port or servername ,local instances only , multiple name supported . 
	* sometimes managed server is not able to be killed as autostart configured in weblogic domain.
    
    >> nmstart [port] ...*
        start node manager by port.  multiple port supported

    >> help
        Show help page .

    >> quit
        quit weblogic node master.







