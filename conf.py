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

import yaml
import logging
conf = {}

def loadYaml():
	'''
	load app.yaml
	all needed data will be stored in viur conf variable
	conf["xeno.application.xxx] = yyy

	:return:
	'''

	# load project.yaml
	# ------------------------------------------------

	projectdata = loadYamlFile("./project.yaml")
	if projectdata:
		conf["xeno.application.projectID"] = ( "_", projectdata["application"] )
		conf["xeno.application.databaseConnection"] = (projectdata["database_ip"], projectdata["database_port"])
		conf["xeno.application.host"] = projectdata["server_ip"]
	else:
		conf["xeno.application.projectID"] = None
		logging.critical("project.yaml needed!")
		exit()

	# load app.yaml
	#------------------------------------------------

	appdata = loadYamlFile("./app.yaml")
	if appdata:
		try:
			# collect static routes
			static_dirs = {}
			for route in appdata["handlers"]:
				if "static_dir" in route:
					if not route["url"].endswith("/"): route["url"] += "/"

					static_dirs.update({route["url"]: route["static_dir"]})
				if "static_files" in route:
					static_dirs.update({route["url"]: route["static_files"]})

			conf["xeno.application.static_dirs"] = static_dirs

		except Exception as e:
			logging.exception(e)
	else:
		conf["xeno.application.static_dirs"] = None

	# load cron.yaml
	# ------------------------------------------------

	crondata = loadYamlFile("./cron.yaml")
	if crondata:
		conf["xeno.application.cron"] = crondata["cron"]
	else:
		conf["xeno.application.cron"] = None


def loadYamlFile(path):
	try:
		cronYaml = open(path, "r")
		cronYamlObj = yaml.load(cronYaml, Loader=yaml.Loader)
		return cronYamlObj
	except:
		logging.error("%s not loaded!"%path)
		return None

