#!/usr/bin/env python

'''

webserver.py
==========

Desc: web server of wlnm


Author: Kevin Yi<yikaus @ gmail>

License  : BSD 


'''

import os
from os import environ as env
from sys import argv
import bottle
from bottle import route, run, static_file, redirect, request, error
from beaker.middleware import SessionMiddleware
from wlnm import server ,util

bottle.debug(True)

# session set up
app = bottle.default_app()
session_opts = {
	#'session.type': 'file',
	'session.cookie_expires': 30000,
	#'session.data_dir': './session',
	'session.auto': True,
	'session.type': 'memory',
	#'session.key' : 'wlnm',
	#session.secret = 0cb243f53ad865a0f70099c0414ffe9cfcfe03ac
}
app = SessionMiddleware(app, session_opts)


# static files (js,css,templates) set up

@route('/lib/:path#.+#')
def server_static(path):
    return static_file(path, root='./app/lib/')

@route('/scenarios.js')
def scenario():
    return static_file('scenarios.js',root='./test/e2e/')

@route('/favicon.ico')
def favicon():
    return static_file('favicon.ico', root='./app/')

@route('/js/:path#.+#')
def server_static(path):
    return static_file(path, root='./app/js/')

@route('/css/:path#.+#')
def server_static(path):
    return static_file(path, root='./app/css/')

@route('/img/:path#.+#')
def server_static(path):
    return static_file(path, root='./app/img/')

@route('/templates/:path#.+#')
def server_static(path):
    return static_file(path, root='./app/templates/')

# route set up
@route('/settings',method='POST')
def save_settings():
    s = request.environ.get('beaker.session')
    s['wlnm'] = request.POST.get('machine').strip()
    s.save()
    redirect ('/')


@route('/command/:id',method='GET')
def get_commands(id):
     args = id.split(" ")[1:]
     cmd = id.split(" ")[0]
     result = run_command(cmd,args)
     return result


@route('/')
@route('/index.html')
def index():
    raise static_file('index.html', root='./app')

@route('/tests')
def tests():
    raise static_file('runner.html', root='./test/e2e/')

@error(404)
def mistake404(code):
    return static_file('404.html', root='./app')


def runServer(port):
    bottle.run(app=app,host='0.0.0.0', port=port)

def saveMachine(machine):
	s = request.environ.get('beaker.session')

	s['machine'] = machine

	s.save()

	return 'Machine %s is used !' % machine

def ifSession(key):
	try :
		s = request.environ.get('beaker.session')
		print s
		if key in s.keys():
			return True
		else :
			return False
	except :
		return False


def run_command(cmd,args=[]):
	

	machine =''
	
	if ifSession('machine'):
		s = request.environ.get('beaker.session')
		machine = s['machine']
		print machine


	cmddict={'init':server.initMachine,
		'ls':server.show,
		'lswls':server.showWLS,
		'lsd':server.showDomains,
		'lsm':server.showMachines,
		'nmstart':server.nmstart,
		'help':util.help,
		'startadmin':server.startAdmin,
		'start':server.startServer,
		'stop':server.stopServer,
		'lsp':server.listprocess,
		'kill':server.kill,
		'use':server.useMachine,
		# 'disconnect':server.disconnect,
		}
	
	if cmd not in cmddict.keys():
		return 'invalid command , use help to check commands.'

	if cmd not in ['help','lsm','use','init'] and not machine :
		return 'you must connect one machine to use %s' % cmd
		
	
	if cmd == 'help' :
		mystdout,old_stdout = util.redirectStdout()
		cmddict[cmd]()
		util.finishRedirectStdout(old_stdout)
		return mystdout.getvalue()
	elif cmd == 'use' :
		try:
			result = cmddict[cmd](args) 
			port = int(result)
			saveMachine(args[0])
			return '%s is ready to use . ' % args[0]
			
		except:
			return result
	elif cmd == 'lsm' :
		return util.decode_output(cmddict[cmd]())
	elif cmd in ['lswls','lsp','lsd']:
		return util.decode_output(cmddict[cmd](machine))
	else :
		#args.insert(0,cmd)
		args.insert(0,machine)
		print args
		return util.decode_output(cmddict[cmd](args))

	

# start application
bottle.run(app=app,host='0.0.0.0', port=argv[1])