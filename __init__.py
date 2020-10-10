__author__ = "Andreas H. Kelch"

# xeno-Project - A no Google, no cloud ViUR Framework
#
# Copyright (c) 2019-2020 Andreas H. Kelch
#
# This library is free software; you can redistribute it and/or modify it
# under the terms of version 2.1 of the GNU Lesser General Public License
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

import os, logging
from viur.xeno import conf as xeno_conf
import gunicorn.app.base
from viur.xeno.databases import unqlite_adapter as datastore

class gunicornServer(gunicorn.app.base.BaseApplication):
	'''
		custom webserver
	'''
	def __init__(self, app, options=None):
		self.options = options or {}
		self.application = app
		super().__init__()

	def load_config(self):
		config = {
			key: value for key, value in self.options.items()
				if key in self.cfg.settings and value is not None}
		for key, value in config.items():
			self.cfg.set(key.lower(), value)

	def load(self):
		return self.application

def loadConfiguration():
	os.environ[ 'GAE_ENV' ] = "xeno"
	os.environ[ "GAE_APPLICATION" ] = "h"

	xeno_conf.conf[ "xeno.application.projectroot" ] = os.path.abspath( "." )
	xeno_conf.loadYaml()

	return xeno_conf.conf

def init(conf):
	'''
	imported in viur.core.__init__.py:42
	preinitialization
	'''
	initScheduler()
	conf.update(xeno_conf.conf)

def setup():
	'''
	stuff to run after module initialization viur.core.__init__.py:315
	:return:
	'''
	pass

def run( application ):
	'''
	stuff to run on startup
	called from app.py
	:return:
	'''

	startCron()

	options = {
		'bind': xeno_conf.conf["xeno.application.host"],
		'workers': 1,
		'threads': 2,
		'reload' : True
	}

	gunicornServer(application, options).run()

# ------------------------------------------------------------------
# Static routes
# ------------------------------------------------------------------
def static_routes( req, environ, start_response ):
	'''
	Inject static routes server.__init__.py:336
	:param req:
	:param environ:
	:param start_response:
	:return:
	'''
	from webob import static as webobstatic
	from viur.core import conf

	if req.path_info.startswith("/xeno/simplestorage"):
		from viur.xeno.files import fileUpload
		if "key" in req.params and "file" in req.params:
			fileUpload(req.params["key"],req.params["file"])
		else:
			raise

	for staticpath, staticfolder in conf[ "xeno.application.static_dirs" ].items():

		if req.path_info.startswith(staticpath):
			req.path_info = req.path_info.replace( staticpath, "" )  # remove staticpath from url

			if staticpath.endswith("/"): #serve Directory
				controllerStatic = webobstatic.DirectoryApp(
					os.path.join(conf["xeno.application.projectroot"], staticfolder))
				return controllerStatic(environ, start_response)

			else: #serve Files
				controllerStatic = webobstatic.FileApp(
					os.path.join(conf["xeno.application.projectroot"], staticfolder))
				return controllerStatic(environ, start_response)

	return False

# ------------------------------------------------------------------
# Tasks
# ------------------------------------------------------------------
def initScheduler():
	from apscheduler.schedulers.background import BackgroundScheduler
	from apscheduler.executors.pool import ProcessPoolExecutor

	logging.getLogger( "apscheduler.scheduler" ).setLevel( logging.WARNING )
	logging.getLogger( 'apscheduler.executors.default' ).propagate = False
	jobstores = { }  # dont store any task data
	executors = {
			'default'    : { 'type': 'threadpool', 'max_workers': 20 },
			'processpool': ProcessPoolExecutor( max_workers = 5 )
			}
	job_defaults = {
			'coalesce'     : False,
			'max_instances': 3
			}
	scheduler = BackgroundScheduler( timezone = "Europe/Berlin" )
	scheduler.configure( jobstores = jobstores, executors = executors, job_defaults = job_defaults, timezone = "Europe/Berlin" )
	scheduler.start()
	xeno_conf.conf[ "xeno.scheduler" ] = scheduler
	logging.warning("SCHEDULER STARTED")

def startCron():
	from viur.core import conf
	from datetime import datetime, timedelta
	import requests

	def callCron(*args,**kwargs):
		# whitelist localhost
		#global _appengineServiceIPs
		#_appengineServiceIPs.extend(["localhost", "127.0.0.1"])

		taskurl = "http://%s/_tasks/cron"%conf["xeno.application.host"]
		headers = {"X-Appengine-Cron":"1",
				   "X_APPENGINE_USER_IP":"10.0.0.1"}

		resp = requests.post(taskurl,headers=headers)

	mainTask = conf[ "xeno.scheduler" ].add_job(
			callCron,
			'cron',
			minute = '*/5',
			next_run_time = datetime.now() + timedelta( seconds = 1 ) )

def callDeferred_hook( func, args, kwargs ):
	from datetime import datetime, timedelta
	from viur.core import conf

	#rundate = datetime.now() + timedelta( seconds = 30 )  # 3 seconds delay
	#logging.error(conf[ "xeno.scheduler" ].print_jobs())

	job = conf[ "xeno.scheduler" ].add_job( func,
											#id = "%s.%s" % (func.__module__, func.__name__),
											args = args,
											kwargs = kwargs,
											#trigger = "date",
											#run_date = rundate
											)
	return job

