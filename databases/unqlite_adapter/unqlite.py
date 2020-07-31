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
#U0uIDImWMmOVi

import logging
import operator
from unqlite import UnQLite
from datetime import datetime
from viur.xeno.databases.unqlite_adapter import Entity,Key,Query
from functools import partial
#from viur.core import utils

__db__ = UnQLite("database.udb")
logging.error("DB INIT ")

'''
base,string,color,email,key,password,selectOne,text
date
file,hierarchy,relational,record,treedir,treeitem,user
numeric
selectMulti






'''



#_generateNewId = partial(utils.generateRandomString, length=20)




def buildfilter(filterlist):
	'''

	:param filterlist:   [('name_idx', '>=', 'admin@xeno.appspot.com')]
	:return:
	'''

	def filtertest(dbval,oper,filterval):
		ops = {
			'>':  operator.gt,
			'<':  operator.lt,
			'>=': operator.ge,
			'<=': operator.le,
			'=':  operator.eq,
			"in": operator.contains
		}

		if isinstance(dbval,list) and oper == "=":
			oper = "in"

		return ops[oper](dbval,filterval)

	def filter(entity):
		retValue = False

		for filterObj in filterlist:
			field, oper, value = filterObj

			if "." in field:
				fieldobj = field.split(".")
				currentDbVal = entity.get(fieldobj[0])
				for fieldpart in fieldobj[1:]:
					currentDbVal = currentDbVal.get(fieldpart)
				dbval = currentDbVal
			else:
				dbval = entity.get(field)

			if isinstance(dbval,bytes):
				dbval = dbval.decode()
			elif isinstance(dbval,list):
				nlist = []
				for val in dbval:
					if isinstance(val, bytes):
						nlist.append(val.decode())
				dbval=nlist

			currenttest = filtertest(dbval,oper,value)
			if currenttest:
				retValue = True
			else:
				retValue = False
				break # is only filter False this entity doesnt match

		return retValue
	return filter

def dbobj_to_Entity(kind,dbobj) -> Entity:
	for k,v in dbobj.items():

		if isinstance(v,bytes) and k not in ["password"]:
			dbobj[k] = v.decode()

			try:
				dbobj[k] = datetime.strptime(dbobj[k], "%Y-%m-%d %H:%M:%S")
			except ValueError:
				pass

		elif isinstance(v, list):
			nlist = []
			for val in v:
				if isinstance(val, bytes):
					nlist.append(val.decode())
			dbobj[k] = nlist

	#logging.error(dbobj)
	key = Key(kind, dbobj["__key__"])
	entity = Entity(key = key)
	del dbobj["__key__"]
	entity.update(dbobj)
	return entity

def Entity_to_dbobj(Entity):
	for k, v in Entity.items():
		if isinstance(v,datetime):
			Entity[k] = v.strftime("%Y-%m-%d %H:%M:%S")
	return Entity

def connect():
	pass

def put(entity:Entity):
	#logging.error("PUT")
	collection = __db__.collection(entity.kind)
	collection.create()

	key = entity.key
	entity = Entity_to_dbobj(entity)
	raw_entity = dict(entity)
	raw_entity["__key__"] = str(key.id_or_name) #unqlite doesnot support presetting __id :(

	entities = get_multi([key])
	if not entities:
		collection.store(raw_entity) #add
	else:
		collection.update(entities[0]["__id"],raw_entity) #update


def get_multi(keys:[Key]):
	entities = []

	if not keys:
		return entities

	for key in keys:
		kind = key.kind
		dbkey = str(key.id_or_name).encode()

		collection = __db__.collection(kind) #ensure that collection exists
		collection.create()

		result = collection.filter(lambda entity: entity["__key__"] == dbkey)
		if result:
			entities.append(dbobj_to_Entity(kind,result[0]))
	#logging.error(entities)
	return entities

def delete(key:Key):
	kind = key.kind

	entities = get_multi([key])
	if not entities:
		return False

	collection = __db__.collection(kind)  # ensure that collection exists
	collection.create()

	collection.delete(entities[0]["__id"])


def query(query:Query):
	'''
	logging.error("FFFFFFFFF")
	logging.error(query.filters)
	logging.error(query.kind)
	logging.error(query.order)
	logging.error(dir(query))
	'''


	collection = __db__.collection(query.kind)  # ensure that collection exists
	collection.create()

	entities = []

	if query.filters:
		currentFilter = buildfilter(query.filters)
		entities = collection.filter(currentFilter)
	else:
		entities = collection.all()

	if query.order:
		pass

	if query.keys_only:
		entities = [dbobj_to_Entity(query.kind, e).key for e in entities]
	else:
		entities = [dbobj_to_Entity(query.kind,e) for e in entities]
		#logging.error(entities)
	return entities

def transaction_start():
	__db__.begin()

def transaction_commit():
	__db__.commit()

def transaction_rollback():
	__db__.rollback()

def get(key): #not used
	pass
